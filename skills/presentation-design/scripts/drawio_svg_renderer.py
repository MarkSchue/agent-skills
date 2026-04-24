"""
DrawioSvgRenderer — Converts a named draw.io page to an SVG file.

CLI usage::

    python scripts/drawio_svg_renderer.py assets/diagrams/file.drawio Page-1 \\
        assets/diagrams/Page-1.svg [--width 1200] [--height 800]

Library usage::

    from scripts.drawio_svg_renderer import DrawioSvgRenderer
    renderer = DrawioSvgRenderer()
    svg_path = renderer.ensure_svg(
        drawio_path  = Path("assets/diagrams/file.drawio"),
        page_name    = "Page-1",
        out_dir      = Path("assets/diagrams"),
        target_width = 1200,
        target_height = 700,
    )

Coordinate-system contract
--------------------------
In draw.io (mxGraph), every cell's ``mxGeometry`` stores coordinates relative to
its **container's top-left corner (0, 0)** — regardless of whether the container
is a plain group, a swimlane, or the root layer.  The swimlane ``startSize``
header is a *visual* property only; it does NOT shift the origin for child cells.
The renderer therefore must **never** add ``startSize`` when resolving a child
cell's absolute position.

Edge waypoints (``Array[@as="points"]``) follow the same rule: they are stored in
the coordinate system of the edge's parent container (top-left origin).

Supported mxGraph features
--------------------------
- Rectangle vertices (fillColor, strokeColor, rounded, dashed, opacity, arcSize)
- Ellipse / perimeter=ellipsePerimeter vertices
- Swimlane containers (header + body rendered separately, children clipped)
- Group containers (logical only — no background drawn)
- Text-only vertices (fillColor=none, strokeColor=none)
- Edges with optional arrowheads, waypoints, edge labels
- Orthogonal edge auto-routing when no explicit waypoints are present
- HTML-stripped multi-line labels; full named & numeric HTML entity decoding
- Dashed / dotted stroke styles
- Per-cell opacity
"""

from __future__ import annotations

import argparse
import base64
import logging
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Style defaults
# ---------------------------------------------------------------------------

_DEFAULTS: dict[str, str] = {
    "fillColor":     "#FFFFFF",
    "strokeColor":   "#000000",
    "fontColor":     "#000000",
    "fontSize":      "11",
    "fontStyle":     "0",
    "align":         "center",
    "verticalAlign": "middle",
    "strokeWidth":   "1",
    "rounded":       "0",
    "dashed":        "0",
    "opacity":       "100",
}


# ---------------------------------------------------------------------------
# Style parsing helpers
# ---------------------------------------------------------------------------

def _parse_style(style_str: str) -> dict[str, str]:
    """Parse a semicolon-separated mxGraph style string into a dict."""
    result: dict[str, str] = {}
    for token in (style_str or "").split(";"):
        token = token.strip()
        if not token:
            continue
        if "=" in token:
            k, v = token.split("=", 1)
            result[k.strip()] = v.strip()
        else:
            result[token] = "1"
    return result


def _merged_style(style_str: str) -> dict[str, str]:
    """Merge *style_str* key=value pairs on top of the default style dict."""
    return {**_DEFAULTS, **_parse_style(style_str)}


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

def _esc(text: str) -> str:
    """Escape XML special characters for SVG text content."""
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
    )


def _strip_html(html: str) -> str:
    """Strip HTML tags and decode entities; convert <br> and </p> to newlines."""
    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    # Block-level paragraph endings → newline (so HTML bullet-lists rendered
    # as a series of <p>…</p> survive as separate visual lines).
    text = re.sub(r"</p\s*>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = (
        text.replace("&lt;",     "<")
            .replace("&gt;",     ">")
            .replace("&amp;",    "&")
            .replace("&nbsp;",   " ")
            .replace("&mdash;",  "\u2014")
            .replace("&ndash;",  "\u2013")
            .replace("&bull;",   "\u2022")
            .replace("&middot;", "\u00b7")
            .replace("&times;",  "\u00d7")
            .replace("&rarr;",   "\u2192")
            .replace("&larr;",   "\u2190")
            .replace("&uarr;",   "\u2191")
            .replace("&darr;",   "\u2193")
            .replace("&hellip;", "\u2026")
            .replace("&#xa;",    "\n")
            .replace("&#xA;",    "\n")
    )
    text = re.sub(r"&#[xX]([0-9a-fA-F]+);", lambda m: chr(int(m.group(1), 16)), text)
    text = re.sub(r"&#([0-9]+);",           lambda m: chr(int(m.group(1))),      text)
    return text.strip()


# ---------------------------------------------------------------------------
# SVG element helpers
# ---------------------------------------------------------------------------

def _text_anchor(align: str) -> str:
    return {"left": "start", "right": "end"}.get(align, "middle")


def _svg_rect(x: float, y: float, w: float, h: float, st: dict) -> str:
    fill   = st["fillColor"]
    stroke = st["strokeColor"]
    sw     = st["strokeWidth"]
    rx     = 5.0 if st["rounded"] not in ("0", "") else 0.0
    if "arcSize" in st:
        try:
            rx = min(w, h) * float(st["arcSize"]) / 100.0
        except (ValueError, TypeError):
            pass
    dash   = 'stroke-dasharray="8,4" ' if st["dashed"] not in ("0", "") else ""
    op     = float(st.get("opacity", "100")) / 100.0
    op_a   = f'opacity="{op:.2f}" ' if op < 1.0 else ""
    return (
        f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
        f'rx="{rx:.2f}" ry="{rx:.2f}" {dash}{op_a}/>'
    )


def _svg_ellipse(x: float, y: float, w: float, h: float, st: dict) -> str:
    fill   = st["fillColor"]
    stroke = st["strokeColor"]
    sw     = st["strokeWidth"]
    dash   = 'stroke-dasharray="8,4" ' if st["dashed"] not in ("0", "") else ""
    cx, cy, rx, ry = x + w / 2, y + h / 2, w / 2, h / 2
    return (
        f'<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="{rx:.2f}" ry="{ry:.2f}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {dash}/>'
    )


def _svg_rhombus(x: float, y: float, w: float, h: float, st: dict) -> str:
    """Render a diamond (rhombus) shape as an SVG polygon."""
    fill   = st["fillColor"]
    stroke = st["strokeColor"]
    sw     = st["strokeWidth"]
    dash   = 'stroke-dasharray="8,4" ' if st["dashed"] not in ("0", "") else ""
    cx, cy = x + w / 2, y + h / 2
    # Four cardinal points: top, right, bottom, left
    pts = f"{cx:.2f},{y:.2f} {x+w:.2f},{cy:.2f} {cx:.2f},{y+h:.2f} {x:.2f},{cy:.2f}"
    return (
        f'<polygon points="{pts}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {dash}/>'
    )


def _svg_chevron(x: float, y: float, w: float, h: float, st: dict) -> str:
    """Right-pointing chevron / step (matches drawio ``shape=step``).

    Tip width defaults to ``min(h * 0.5, w * 0.18)`` — tweakable via the
    ``stepSize`` style key (in absolute px).
    """
    fill   = st["fillColor"]
    stroke = st["strokeColor"]
    sw     = st["strokeWidth"]
    dash   = 'stroke-dasharray="8,4" ' if st["dashed"] not in ("0", "") else ""
    try:
        tip = float(st.get("stepSize") or min(h * 0.5, w * 0.18))
    except (TypeError, ValueError):
        tip = min(h * 0.5, w * 0.18)
    pts = (
        f"{x:.2f},{y:.2f} "
        f"{x+w-tip:.2f},{y:.2f} "
        f"{x+w:.2f},{y+h/2:.2f} "
        f"{x+w-tip:.2f},{y+h:.2f} "
        f"{x:.2f},{y+h:.2f} "
        f"{x+tip:.2f},{y+h/2:.2f}"
    )
    return (
        f'<polygon points="{pts}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {dash}/>'
    )


def _svg_arc(
    cx: float, cy: float, ro: float, ri: float,
    start_deg: float, end_deg: float, st: dict,
) -> str:
    """Annular sector as SVG path. Angles in degrees, 0 = east, CW positive."""
    import math
    fill   = st["fillColor"]
    stroke = st["strokeColor"]
    sw     = st["strokeWidth"]
    dash   = 'stroke-dasharray="8,4" ' if st["dashed"] not in ("0", "") else ""
    if end_deg <= start_deg:
        return ""
    sweep = end_deg - start_deg
    # Cap a near-full circle — SVG arc cannot draw a complete circle in one segment.
    if sweep >= 359.999:
        sweep = 359.99
        end_deg = start_deg + sweep
    large_arc = "1" if sweep > 180 else "0"
    s_rad = math.radians(start_deg)
    e_rad = math.radians(end_deg)
    # Outer points (CW from start to end)
    ox1, oy1 = cx + ro * math.cos(s_rad), cy + ro * math.sin(s_rad)
    ox2, oy2 = cx + ro * math.cos(e_rad), cy + ro * math.sin(e_rad)
    if ri <= 0:
        # Pie slice
        d = (
            f"M {cx:.2f},{cy:.2f} "
            f"L {ox1:.2f},{oy1:.2f} "
            f"A {ro:.2f},{ro:.2f} 0 {large_arc} 1 {ox2:.2f},{oy2:.2f} Z"
        )
    else:
        ix1, iy1 = cx + ri * math.cos(s_rad), cy + ri * math.sin(s_rad)
        ix2, iy2 = cx + ri * math.cos(e_rad), cy + ri * math.sin(e_rad)
        d = (
            f"M {ox1:.2f},{oy1:.2f} "
            f"A {ro:.2f},{ro:.2f} 0 {large_arc} 1 {ox2:.2f},{oy2:.2f} "
            f"L {ix2:.2f},{iy2:.2f} "
            f"A {ri:.2f},{ri:.2f} 0 {large_arc} 0 {ix1:.2f},{iy1:.2f} Z"
        )
    return (
        f'<path d="{d}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{sw}" {dash}/>'
    )


def _svg_trapezoid(
    x: float, y: float, w: float, h: float, st: dict, *, orientation: str = "down"
) -> str:
    """Isoceles trapezoid (drawio ``shape=trapezoid``).

    ``orientation = 'down'`` (default) → wider at the bottom (pyramid layer).
    ``orientation = 'up'``             → wider at the top (funnel layer).
    The narrow edge is half the wide edge by default; tweak with the
    ``trapezoidNarrowPct`` style key (0..1 fraction of width).
    """
    fill   = st["fillColor"]
    stroke = st["strokeColor"]
    sw     = st["strokeWidth"]
    dash   = 'stroke-dasharray="8,4" ' if st["dashed"] not in ("0", "") else ""
    try:
        narrow_pct = float(st.get("trapezoidNarrowPct") or 0.5)
    except (TypeError, ValueError):
        narrow_pct = 0.5
    inset = w * (1 - narrow_pct) / 2
    if orientation == "up":
        # narrow at bottom, wide at top
        pts = (
            f"{x:.2f},{y:.2f} "
            f"{x+w:.2f},{y:.2f} "
            f"{x+w-inset:.2f},{y+h:.2f} "
            f"{x+inset:.2f},{y+h:.2f}"
        )
    else:
        # narrow at top, wide at bottom (pyramid layer)
        pts = (
            f"{x+inset:.2f},{y:.2f} "
            f"{x+w-inset:.2f},{y:.2f} "
            f"{x+w:.2f},{y+h:.2f} "
            f"{x:.2f},{y+h:.2f}"
        )
    return (
        f'<polygon points="{pts}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {dash}/>'
    )


def _wrap_text_to_width(text: str, max_w: float, font_size: float) -> list[str]:
    """Greedy word-wrap text to fit within *max_w* pixels.

    Uses an average char width of font_size * 0.55 (proportional-font
    heuristic). Preserves explicit '\\n' line breaks. Long words that
    exceed *max_w* are kept whole on their own line rather than truncated.
    """
    if max_w <= 0 or font_size <= 0:
        return text.split("\n")
    char_w = font_size * 0.55
    max_chars = max(1, int(max_w / char_w))
    out: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            out.append("")
            continue
        words = paragraph.split(" ")
        line = ""
        for w in words:
            candidate = (line + " " + w).strip() if line else w
            if len(candidate) <= max_chars:
                line = candidate
            else:
                if line:
                    out.append(line)
                line = w
        if line:
            out.append(line)
    return out


def _svg_label(
    label: str,
    x: float, y: float, w: float, h: float,
    st: dict,
    padding: float = 4.0,
) -> str:
    """Render a multi-line label inside the given bounding box."""
    if not label:
        return ""

    font_size  = float(st.get("fontSize", "11"))
    font_color = st.get("fontColor", "#000000")
    font_flag  = int(st.get("fontStyle", "0"))
    fw = "bold"   if font_flag & 1 else "normal"
    fi = "italic" if font_flag & 2 else "normal"
    align   = st.get("align",         "center")
    v_align = st.get("verticalAlign", "middle")
    anchor  = _text_anchor(align)
    line_h  = font_size * 1.3

    # Word-wrap if the cell style requests it (drawio whiteSpace=wrap),
    # otherwise just split on explicit newlines. Padding is reserved on
    # both sides of the box.
    wrap_w = max(1.0, w - 2 * padding)
    if str(st.get("whiteSpace", "")).lower() == "wrap":
        lines = _wrap_text_to_width(label, wrap_w, font_size)
    else:
        lines = label.split("\n")
    n = len(lines)
    text_h = n * line_h

    # Horizontal anchor
    if align == "left":
        tx = x + padding
    elif align == "right":
        tx = x + w - padding
    else:
        tx = x + w / 2

    # First-line baseline Y
    if v_align == "top":
        first_y = y + font_size + padding
    elif v_align == "bottom":
        first_y = y + h - text_h + font_size - padding
    else:
        first_y = y + (h - text_h) / 2 + font_size

    attrs = (
        f'fill="{font_color}" font-size="{font_size:.1f}" '
        f'font-weight="{fw}" font-style="{fi}" text-anchor="{anchor}"'
    )

    if n == 1:
        return f'<text x="{tx:.2f}" y="{first_y:.2f}" {attrs}>{_esc(label)}</text>'

    parts = [f'<text x="{tx:.2f}" y="{first_y:.2f}" {attrs}>']
    for i, line in enumerate(lines):
        dy = "" if i == 0 else f' dy="{line_h:.1f}"'
        parts.append(f'  <tspan x="{tx:.2f}"{dy}>{_esc(line)}</tspan>')
    parts.append("</text>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Absolute position computation — the critical fix
# ---------------------------------------------------------------------------

def _build_abs_positions(root_elem: ET.Element) -> dict[str, tuple[float, float]]:
    """Return cell_id → (abs_x, abs_y) for every cell in *root_elem*.

    **Key rule**: child coordinates are always relative to the parent's top-left
    corner (0, 0).  The swimlane ``startSize`` header is a *visual* overlay and
    does NOT shift the child coordinate origin.  Adding ``startSize`` to child
    positions (as a naive implementation might) would displace all children of
    swimlane containers by the header height — causing shapes to appear below
    where they should be.
    """
    cells: dict[str, ET.Element] = {
        c.get("id", ""): c for c in root_elem.findall("mxCell")
    }
    cache: dict[str, tuple[float, float]] = {}

    def _get(cid: str) -> tuple[float, float]:
        if cid in cache:
            return cache[cid]
        if cid in ("", "0", "1"):
            cache[cid] = (0.0, 0.0)
            return (0.0, 0.0)

        cell = cells.get(cid)
        if cell is None:
            cache[cid] = (0.0, 0.0)
            return (0.0, 0.0)

        geo = cell.find("mxGeometry")
        cx = float(geo.get("x", 0) or 0) if geo is not None else 0.0
        cy = float(geo.get("y", 0) or 0) if geo is not None else 0.0

        parent_id = cell.get("parent", "1")
        if parent_id == cid:
            result = (cx, cy)
        elif parent_id in ("", "0", "1"):
            result = (cx, cy)
        else:
            p_abs  = _get(parent_id)
            # Child coordinates are relative to the parent's top-left corner.
            # Never offset by startSize — that would double-count the header.
            result = (p_abs[0] + cx, p_abs[1] + cy)

        cache[cid] = result
        return result

    for cid in list(cells.keys()):
        _get(cid)
    return cache


# ---------------------------------------------------------------------------
# Cell rendering — vertices
# ---------------------------------------------------------------------------

def _render_vertex(
    cell: ET.Element,
    abs_pos_map: dict[str, tuple[float, float]],
    elems: list[str],
    clip_defs: dict[str, str],
) -> None:
    geo = cell.find("mxGeometry")
    if geo is None:
        return

    cid = cell.get("id", "")
    ax, ay = abs_pos_map.get(cid, (0.0, 0.0))
    w = float(geo.get("width",  0) or 0)
    h = float(geo.get("height", 0) or 0)
    if w <= 0 or h <= 0:
        return

    style_str = cell.get("style", "")
    parsed = _parse_style(style_str)
    st     = _merged_style(style_str)

    # Group cells are logical containers — no visual rendering
    if "group" in parsed:
        return

    # Image cells (logos, embedded raster/SVG): emit an <image> tag using the
    # data URI from the style. Without this branch the cell falls through to
    # default rect rendering and shows as an empty white box with a black border.
    if parsed.get("shape") == "image" and "image" in parsed:
        img_uri = parsed["image"]
        # Data URIs may have been URL-encoded by the exporter to avoid the
        # draw.io style-string semicolon parser. Decode for SVG embedding.
        if img_uri.startswith("data:image/svg+xml,") and "%3C" in img_uri:
            from urllib.parse import unquote as _url_unquote
            prefix, _, encoded = img_uri.partition(",")
            img_uri = prefix + "," + _url_unquote(encoded)
        elems.append(
            f'<image x="{ax:.2f}" y="{ay:.2f}" '
            f'width="{w:.2f}" height="{h:.2f}" '
            f'preserveAspectRatio="xMidYMid meet" href="{_esc(img_uri)}"/>'
        )
        return

    value   = _strip_html(cell.get("value", "") or "")
    is_swim = "swimlane" in parsed
    is_text = (
        "text" in parsed
        and st["fillColor"] in ("none", "")
        and st["strokeColor"] in ("none", "")
    )
    is_ell  = (
        "ellipse" in parsed
        or st.get("shape") == "ellipse"
        or "perimeter=ellipsePerimeter" in style_str
    )
    is_rhombus = (
        "rhombus" in parsed
        or st.get("shape") == "rhombus"
        or "perimeter=rhombusPerimeter" in style_str
    )
    is_step = (
        st.get("shape") == "step"
        or "shape=step" in style_str
    )
    is_trapezoid = (
        st.get("shape") == "trapezoid"
        or "shape=trapezoid" in style_str
    )
    trap_orientation = "up" if "direction=north" in style_str else "down"
    is_arc = (
        st.get("shape") == "mxgraph.basic.partConcEllipse"
        or "shape=mxgraph.basic.partConcEllipse" in style_str
    )

    if is_swim:
        start_size = float(parsed.get("startSize", "26"))
        sw         = st["strokeWidth"]
        stroke     = st["strokeColor"]
        header_fill = st["fillColor"]
        # Derive body fill: use swimlaneBody style key if present; else white
        body_fill = parsed.get("swimlaneBody", "#FFFFFF")
        if body_fill in ("", "none"):
            body_fill = "#FFFFFF"

        rx = 0.0
        if st["rounded"] not in ("0", ""):
            rx = 5.0
        if "arcSize" in st:
            try:
                rx = min(w, h) * float(st["arcSize"]) / 100.0
            except (ValueError, TypeError):
                pass

        # 1. Full body background
        body_y = ay + start_size
        body_h = h - start_size
        if body_h > 0:
            elems.append(
                f'<rect x="{ax:.2f}" y="{body_y:.2f}" width="{w:.2f}" '
                f'height="{body_h:.2f}" fill="{body_fill}" '
                f'stroke="{stroke}" stroke-width="{sw}" rx="{rx:.2f}" ry="{rx:.2f}"/>'
            )
        # 2. Header bar
        elems.append(
            f'<rect x="{ax:.2f}" y="{ay:.2f}" width="{w:.2f}" '
            f'height="{start_size:.2f}" fill="{header_fill}" '
            f'stroke="{stroke}" stroke-width="{sw}" rx="{rx:.2f}" ry="{rx:.2f}"/>'
        )
        # 3. Outer border (no fill — visual edge crisp-up)
        elems.append(
            f'<rect x="{ax:.2f}" y="{ay:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'fill="none" stroke="{stroke}" stroke-width="{sw}" '
            f'rx="{rx:.2f}" ry="{rx:.2f}"/>'
        )
        # 4. Header label (centred in header strip)
        elems.append(
            _svg_label(value, ax, ay, w, start_size,
                       {**st, "fontColor": "#FFFFFF", "verticalAlign": "middle"})
        )
        return

    if is_text:
        elems.append(_svg_label(value, ax, ay, w, h, st))
        return

    if is_ell:
        elems.append(_svg_ellipse(ax, ay, w, h, st))
    elif is_rhombus:
        elems.append(_svg_rhombus(ax, ay, w, h, st))
    elif is_step:
        elems.append(_svg_chevron(ax, ay, w, h, st))
    elif is_trapezoid:
        elems.append(_svg_trapezoid(ax, ay, w, h, st, orientation=trap_orientation))
    elif is_arc:
        # Convert drawio's partConcEllipse parameters back to our angle space
        # (0 = north, CW positive, fractions of circle) → (0 = east, CW, deg).
        try:
            d_start = float(st.get("startAngle", "0"))
            d_end   = float(st.get("endAngle", "1"))
            arc_w   = float(st.get("arcWidth", "1"))
        except (TypeError, ValueError):
            d_start, d_end, arc_w = 0.0, 1.0, 1.0
        cx_v = ax + w / 2
        cy_v = ay + h / 2
        ro = min(w, h) / 2
        ri = ro * (1 - max(0.0, min(1.0, arc_w)))
        # Drawio: 0 = north (12 o'clock), CW positive, 0..1 = fraction of circle
        # Our:    0 = east  (3  o'clock), CW positive, degrees
        start_deg = (d_start * 360.0) - 90.0
        end_deg   = (d_end   * 360.0) - 90.0
        # Handle wrap-around (end < start after modulo)
        if end_deg <= start_deg:
            end_deg += 360.0
        elems.append(_svg_arc(cx_v, cy_v, ro, ri, start_deg, end_deg, st))
    else:
        elems.append(_svg_rect(ax, ay, w, h, st))

    elems.append(_svg_label(value, ax, ay, w, h, st))


# ---------------------------------------------------------------------------
# Cell rendering — edges
# ---------------------------------------------------------------------------

def _render_edge(
    cell: ET.Element,
    abs_pos_map: dict[str, tuple[float, float]],
    all_cells: dict[str, ET.Element],
    elems: list[str],
    defs: dict[str, str],
) -> None:
    geo = cell.find("mxGeometry")
    if geo is None:
        return

    style_str    = cell.get("style", "")
    st           = _parse_style(style_str)
    stroke       = st.get("strokeColor", "#000000")
    stroke_width = st.get("strokeWidth", "1")
    end_arrow    = st.get("endArrow",   "block")
    end_fill     = st.get("endFill",    "1")
    start_arrow  = st.get("startArrow", "none")
    dashed       = st.get("dashed", "0") not in ("0", "")
    edge_style   = st.get("edgeStyle", "")

    # Parent offset for waypoints: top-left of the edge's parent container.
    # Waypoints are stored in the parent's coordinate system (origin = top-left).
    edge_parent_id = cell.get("parent", "1")
    if edge_parent_id in ("", "0", "1"):
        parent_off = (0.0, 0.0)
    else:
        parent_off = abs_pos_map.get(edge_parent_id, (0.0, 0.0))

    # --- helpers --------------------------------------------------------

    def _cell_rect(cid: str | None) -> tuple[float, float, float, float] | None:
        """Return (ax, ay, cw, ch) for a vertex cell, or None."""
        if not cid:
            return None
        c = all_cells.get(cid)
        if c is None:
            return None
        g = c.find("mxGeometry")
        if g is None:
            return None
        ax2, ay2 = abs_pos_map.get(cid, (0.0, 0.0))
        cw2 = float(g.get("width",  0) or 0)
        ch2 = float(g.get("height", 0) or 0)
        return ax2, ay2, cw2, ch2

    def _boundary_pt(ax2, ay2, cw2, ch2,
                     other_x: float, other_y: float) -> tuple[float, float]:
        """Point on the boundary of (ax2, ay2, cw2, ch2) facing (other_x, other_y)."""
        cx2, cy2 = ax2 + cw2 / 2.0, ay2 + ch2 / 2.0
        dx, dy = other_x - cx2, other_y - cy2
        if cw2 == 0 or ch2 == 0 or (dx == 0 and dy == 0):
            return cx2, cy2
        # Compare normalised deltas to decide which edge to exit from
        if abs(dx / cw2) >= abs(dy / ch2):
            return (ax2 + cw2, cy2) if dx >= 0 else (ax2, cy2)
        else:
            return (cx2, ay2 + ch2) if dy >= 0 else (cx2, ay2)

    # --- parse explicit waypoints first (needed for snap direction) ------

    pts_elem  = geo.find('Array[@as="points"]')
    waypoints: list[tuple[float, float]] = []
    if pts_elem is not None:
        for p in pts_elem.findall("mxPoint"):
            wx = float(p.get("x", 0)) + parent_off[0]
            wy = float(p.get("y", 0)) + parent_off[1]
            waypoints.append((wx, wy))

    # --- source connection point ----------------------------------------

    src_rect = _cell_rect(cell.get("source"))
    tgt_rect = _cell_rect(cell.get("target"))

    src_pt: tuple[float, float] | None = None
    tgt_pt: tuple[float, float] | None = None

    if src_rect:
        ax, ay, cw, ch = src_rect
        ex, ey = st.get("exitX"), st.get("exitY")
        if ex is not None and ey is not None:
            try:
                src_pt = (ax + cw * float(ex), ay + ch * float(ey))
            except (ValueError, TypeError):
                pass
        if src_pt is None:
            # Snap to the boundary edge facing the next waypoint (or target center)
            if waypoints:
                ref = waypoints[0]
            elif tgt_rect:
                ref = (tgt_rect[0] + tgt_rect[2] / 2.0, tgt_rect[1] + tgt_rect[3] / 2.0)
            else:
                ref = (ax + cw / 2.0, ay + ch / 2.0)
            src_pt = _boundary_pt(ax, ay, cw, ch, ref[0], ref[1])

    if tgt_rect:
        ax, ay, cw, ch = tgt_rect
        enx, eny = st.get("entryX"), st.get("entryY")
        if enx is not None and eny is not None:
            try:
                tgt_pt = (ax + cw * float(enx), ay + ch * float(eny))
            except (ValueError, TypeError):
                pass
        if tgt_pt is None:
            # Snap to the boundary edge facing the last waypoint (or source center)
            if waypoints:
                ref = waypoints[-1]
            elif src_rect:
                ref = (src_rect[0] + src_rect[2] / 2.0, src_rect[1] + src_rect[3] / 2.0)
            else:
                ref = (ax + cw / 2.0, ay + ch / 2.0)
            tgt_pt = _boundary_pt(ax, ay, cw, ch, ref[0], ref[1])

    # Fallback: explicit source/target mxPoint coordinates (floating edges)
    if src_pt is None:
        for pt in geo.findall("mxPoint"):
            if pt.get("as") == "sourcePoint":
                src_pt = (
                    float(pt.get("x", 0)) + parent_off[0],
                    float(pt.get("y", 0)) + parent_off[1],
                )
    if tgt_pt is None:
        for pt in geo.findall("mxPoint"):
            if pt.get("as") == "targetPoint":
                tgt_pt = (
                    float(pt.get("x", 0)) + parent_off[0],
                    float(pt.get("y", 0)) + parent_off[1],
                )

    if src_pt is None or tgt_pt is None:
        return

    # Auto-route orthogonal edges when no explicit waypoints exist
    if "orthogonal" in edge_style.lower() and not waypoints:
        _synthesise_orthogonal(src_pt, tgt_pt, st, waypoints, src_rect, tgt_rect)

    all_pts = [src_pt] + waypoints + [tgt_pt]
    d = "M " + " L ".join(f"{px:.1f},{py:.1f}" for px, py in all_pts)

    # Arrowhead marker defs
    def _arrow_def(prefix: str, color: str, filled: bool) -> str:
        mid = f"arr_{prefix}_{len(defs)}"
        if filled:
            defs[mid] = (
                f'<marker id="{mid}" markerWidth="10" markerHeight="8" '
                f'refX="9" refY="3" orient="auto" markerUnits="strokeWidth">'
                f'<path d="M0,0 L0,6 L9,3 z" fill="{color}"/></marker>'
            )
        else:
            defs[mid] = (
                f'<marker id="{mid}" markerWidth="10" markerHeight="8" '
                f'refX="9" refY="3" orient="auto" markerUnits="strokeWidth">'
                f'<path d="M0,0 L9,3 L0,6" fill="none" stroke="{color}" stroke-width="1.5"/></marker>'
            )
        return mid

    m_end = m_start = ""
    if end_arrow not in ("none", ""):
        mid = _arrow_def("e", stroke, end_fill not in ("0", ""))
        m_end = f'marker-end="url(#{mid})"'
    if start_arrow not in ("none", ""):
        mid = _arrow_def("s", stroke, True)
        m_start = f'marker-start="url(#{mid})"'

    dash_a = 'stroke-dasharray="8,4" ' if dashed else ""
    elems.append(
        f'<path d="{d}" stroke="{stroke}" stroke-width="{stroke_width}" '
        f'fill="none" {dash_a}{m_end} {m_start}/>'
    )

    # Edge label at path midpoint
    label = _strip_html(cell.get("value", "") or "")
    if label and len(all_pts) >= 2:
        mid_i = len(all_pts) // 2
        lx = (all_pts[mid_i - 1][0] + all_pts[mid_i][0]) / 2
        ly = (all_pts[mid_i - 1][1] + all_pts[mid_i][1]) / 2
        fc = st.get("fontColor", "#000000")
        fs = float(st.get("fontSize", "10"))
        elems.append(
            f'<text x="{lx:.1f}" y="{ly - 4:.1f}" fill="{fc}" '
            f'font-size="{fs}" text-anchor="middle">{_esc(label)}</text>'
        )


def _synthesise_orthogonal(
    src: tuple[float, float],
    tgt: tuple[float, float],
    st: dict[str, str],
    waypoints: list[tuple[float, float]],
    src_rect: tuple[float, float, float, float] | None = None,
    tgt_rect: tuple[float, float, float, float] | None = None,
) -> None:
    """Append waypoints for a simple axis-aligned elbow route.

    The exit direction is inferred from the boundary point position relative to
    the source cell rectangle.  When no rectangle is available the style's
    exitX/exitY values are used as a fallback.
    """
    sx, sy = src
    tx, ty = tgt

    # Determine whether the source exits horizontally or vertically.
    exit_horiz: bool | None = None
    if src_rect:
        ax, ay, cw, ch = src_rect
        tol = 2.0
        if abs(sx - (ax + cw)) < tol or abs(sx - ax) < tol:
            exit_horiz = True   # exits left or right
        elif abs(sy - (ay + ch)) < tol or abs(sy - ay) < tol:
            exit_horiz = False  # exits top or bottom

    if exit_horiz is None:
        # Fallback: use style hints
        try:
            ex_f = float(st.get("exitX", 0.5))
            ey_f = float(st.get("exitY", 0.5))
        except (ValueError, TypeError):
            ex_f, ey_f = 0.5, 0.5
        if ex_f in (0.0, 1.0):
            exit_horiz = True
        elif ey_f in (0.0, 1.0):
            exit_horiz = False

    dx = abs(sx - tx)
    dy = abs(sy - ty)

    if exit_horiz is True and dy > 4:
        # Horizontal exit → route via vertical mid column
        mid_x = (sx + tx) / 2.0
        waypoints += [(mid_x, sy), (mid_x, ty)]
    elif exit_horiz is False and dx > 4:
        # Vertical exit → route via horizontal mid row
        mid_y = (sy + ty) / 2.0
        waypoints += [(sx, mid_y), (tx, mid_y)]


# ---------------------------------------------------------------------------
# Core renderer class
# ---------------------------------------------------------------------------

class DrawioSvgRenderer:
    """Parse a draw.io file and render a named page to SVG."""

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    def _decode_diagram(self, diag_elem: ET.Element) -> ET.Element | None:
        """Extract the mxGraphModel element from a ``<diagram>`` node.

        draw.io stores diagram content in one of three ways:
        1. As a child ``<mxGraphModel>`` element.
        2. As raw XML text inside ``<diagram>``.
        3. As base64 + deflate-compressed, URL-encoded text (desktop default).
        """
        mxg = diag_elem.find("mxGraphModel")
        if mxg is not None:
            return mxg

        content = (diag_elem.text or "").strip()
        if not content:
            return None

        # Attempt compressed (draw.io desktop format)
        try:
            raw          = base64.b64decode(content)
            decompressed = zlib.decompress(raw, -15)
            xml_str      = urllib.parse.unquote(decompressed.decode("utf-8"))
            return ET.fromstring(xml_str)
        except Exception:
            pass

        # Attempt raw XML text
        try:
            return ET.fromstring(content)
        except ET.ParseError:
            pass

        return None

    def extract_page(self, drawio_path: Path, page_name: str) -> ET.Element:
        """Return the mxGraphModel element for the named page."""
        tree = ET.parse(drawio_path)
        root = tree.getroot()

        # Legacy: file IS the mxGraphModel
        if root.tag == "mxGraphModel":
            if page_name:
                logger.warning(
                    "%s has no named pages; using single diagram (requested: '%s').",
                    drawio_path, page_name,
                )
            return root

        # Multi-page mxfile — match by name
        for diag in root.findall("diagram"):
            if diag.get("name") == page_name:
                mxg = self._decode_diagram(diag)
                if mxg is not None:
                    return mxg
                raise ValueError(
                    f"Page '{page_name}' in {drawio_path} has unreadable content."
                )

        # Fallback to first page
        for diag in root.findall("diagram"):
            mxg = self._decode_diagram(diag)
            if mxg is not None:
                logger.warning(
                    "Page '%s' not found in %s; falling back to first page '%s'.",
                    page_name, drawio_path, diag.get("name", ""),
                )
                return mxg

        raise ValueError(f"No readable diagram page found in {drawio_path}")

    # ------------------------------------------------------------------
    # SVG rendering
    # ------------------------------------------------------------------

    def render_to_svg(
        self,
        mxgraph_model: ET.Element,
        target_width:  float | None = None,
        target_height: float | None = None,
    ) -> str:
        """Convert an mxGraphModel element to a complete SVG string."""
        page_w = float(mxgraph_model.get("pageWidth",  1654))
        page_h = float(mxgraph_model.get("pageHeight", 1169))
        bg     = mxgraph_model.get("background", "#FFFFFF") or "#FFFFFF"

        root_elem = mxgraph_model.find("root")
        if root_elem is None:
            return self._empty_svg(page_w, page_h, target_width, target_height, bg)

        all_cells: dict[str, ET.Element] = {
            c.get("id", ""): c for c in root_elem.findall("mxCell")
        }
        abs_pos_map = _build_abs_positions(root_elem)

        elems: list[str] = []
        defs:  dict[str, str] = {}
        clip_defs: dict[str, str] = {}

        # Vertices first (z-order: containers behind their children)
        for cell in root_elem.findall("mxCell"):
            if cell.get("vertex") == "1" and cell.find("mxGeometry") is not None:
                _render_vertex(cell, abs_pos_map, elems, clip_defs)

        # Edges on top
        for cell in root_elem.findall("mxCell"):
            if cell.get("edge") == "1":
                _render_edge(cell, abs_pos_map, all_cells, elems, defs)

        # Compute tight viewBox from vertex bounds
        min_x = min_y = float("inf")
        max_x = max_y = float("-inf")
        for cell in root_elem.findall("mxCell"):
            if cell.get("vertex") != "1":
                continue
            geo = cell.find("mxGeometry")
            if geo is None:
                continue
            if "group" in _parse_style(cell.get("style", "")):
                continue
            cid = cell.get("id", "")
            ax, ay = abs_pos_map.get(cid, (0.0, 0.0))
            cw = float(geo.get("width",  0) or 0)
            ch = float(geo.get("height", 0) or 0)
            if cw > 0 and ch > 0:
                min_x = min(min_x, ax)
                min_y = min(min_y, ay)
                max_x = max(max_x, ax + cw)
                max_y = max(max_y, ay + ch)

        PAD = 16.0
        if min_x == float("inf"):
            vb_x, vb_y, vb_w, vb_h = 0.0, 0.0, page_w, page_h
        else:
            vb_x = max(0.0, min_x - PAD)
            vb_y = max(0.0, min_y - PAD)
            vb_w = (max_x + PAD) - vb_x
            vb_h = (max_y + PAD) - vb_y

        # Adjust viewBox to match the target frame's aspect ratio exactly.
        # This prevents PowerPoint (and browsers) from stretching or letterboxing
        # the SVG when it is placed in a container with a different aspect ratio.
        if target_width and target_height and vb_w > 0 and vb_h > 0:
            target_ar = target_width / target_height
            content_ar = vb_w / vb_h
            if content_ar > target_ar:
                # Content wider than frame → expand viewBox height
                new_h = vb_w / target_ar
                vb_y -= (new_h - vb_h) / 2.0
                vb_h = new_h
            elif content_ar < target_ar:
                # Content taller than frame → expand viewBox width
                new_w = vb_h * target_ar
                vb_x -= (new_w - vb_w) / 2.0
                vb_w = new_w

        all_defs = {**clip_defs, **defs}
        defs_block = ("<defs>" + "\n".join(all_defs.values()) + "</defs>") if all_defs else ""

        w_attr = f' width="{int(target_width)}"'   if target_width  else ""
        h_attr = f' height="{int(target_height)}"' if target_height else ""

        body = "\n  ".join(e for e in elems if e)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg"'
            f' viewBox="{vb_x:.1f} {vb_y:.1f} {vb_w:.1f} {vb_h:.1f}"'
            f'{w_attr}{h_attr}'
            f' preserveAspectRatio="xMidYMid meet"'
            f' font-family="Segoe UI, Arial, sans-serif">\n'
            f'  <rect x="{vb_x:.1f}" y="{vb_y:.1f}" '
            f'width="{vb_w:.1f}" height="{vb_h:.1f}" fill="{bg}"/>\n'
            f'  {defs_block}\n'
            f'  {body}\n'
            f'</svg>'
        )

    @staticmethod
    def _empty_svg(pw, ph, tw, th, bg) -> str:
        w_attr = f' width="{int(tw)}"' if tw else ""
        h_attr = f' height="{int(th)}"' if th else ""
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {pw} {ph}"{w_attr}{h_attr} '
            f'preserveAspectRatio="xMidYMid meet">'
            f'<rect width="{pw}" height="{ph}" fill="{bg}"/></svg>'
        )

    # ------------------------------------------------------------------
    # Cache-aware entry point
    # ------------------------------------------------------------------

    def ensure_svg(
        self,
        drawio_path:   Path,
        page_name:     str,
        out_dir:       Path,
        target_width:  float | None = None,
        target_height: float | None = None,
    ) -> Path:
        """Return path to an up-to-date SVG for *page_name* in *drawio_path*.

        The SVG is written to ``{out_dir}/{page_name}.svg`` and regenerated
        only when the ``.drawio`` source is newer than the cached SVG.
        """
        out_dir.mkdir(parents=True, exist_ok=True)
        svg_path      = out_dir / f"{page_name}.svg"
        drawio_mtime  = drawio_path.stat().st_mtime
        svg_mtime     = svg_path.stat().st_mtime if svg_path.exists() else 0

        if drawio_mtime <= svg_mtime:
            logger.debug("SVG up-to-date: %s", svg_path)
            return svg_path

        logger.info("Rendering '%s' from %s → %s", page_name, drawio_path.name, svg_path.name)
        model       = self.extract_page(drawio_path, page_name)
        svg_content = self.render_to_svg(model, target_width, target_height)
        svg_path.write_text(svg_content, encoding="utf-8")
        return svg_path


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    ap = argparse.ArgumentParser(
        description="Export a named draw.io page to SVG.",
    )
    ap.add_argument("drawio",    help="Path to the .drawio source file")
    ap.add_argument("page",      help="Page / tab name to export")
    ap.add_argument("output",    help="Output SVG file path")
    ap.add_argument("--width",   type=float, default=None, help="Target SVG width  (px)")
    ap.add_argument("--height",  type=float, default=None, help="Target SVG height (px)")
    args = ap.parse_args()

    drawio_path = Path(args.drawio)
    if not drawio_path.exists():
        print(f"ERROR: {drawio_path} not found", file=sys.stderr)
        sys.exit(1)

    out_path = Path(args.output)
    renderer = DrawioSvgRenderer()
    model    = renderer.extract_page(drawio_path, args.page)
    svg      = renderer.render_to_svg(model, args.width, args.height)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(svg, encoding="utf-8")
    print(f"✓ Wrote {out_path}")


if __name__ == "__main__":
    main()
