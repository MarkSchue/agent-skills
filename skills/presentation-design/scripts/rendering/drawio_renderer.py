"""
DrawioRenderer — Converts draw.io diagram pages to SVG files at build time.

Supports the presentation-design skill's draw.io diagram workflow:

  YAML reference:   image: "diagrams/application-landscape.drawio#current-state"
  Source file:      assets/diagrams/application-landscape.drawio  (multi-tab mxfile)
  Generated SVG:    assets/diagrams/current-state.svg             (auto, mtime-tracked)

Only the following mxGraph features are supported (the "presentation-design subset"):
  - Rectangle vertices (fillColor, strokeColor, strokeWidth, rounded, dashed, opacity)
  - Ellipse vertices   (same style props)
  - Text-only vertices (fillColor=none, strokeColor=none)
  - Edge/connector cells with optional arrowheads and waypoints
  - Multi-line labels via newlines or <br> in the value attribute
  - HTML-strip for html=1 labels (tags are removed; plain text kept)

Design diagrams at the image-card body dimensions (see diagram-principles in SKILL.md)
so the SVG fills the allocated slide area without letterboxing.
"""

from __future__ import annotations

import base64
import logging
import re
import urllib.parse
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Style defaults (applied when a property is absent from the cell's style)
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
# Helpers
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
    """Merge style string on top of defaults."""
    return {**_DEFAULTS, **_parse_style(style_str)}


def _esc(text: str) -> str:
    """Escape XML special characters for SVG text content."""
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
    )


def _strip_html(html: str) -> str:
    """Strip HTML tags and decode common entities; preserve newline intent."""
    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = (
        text.replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&amp;", "&")
            .replace("&nbsp;", " ")
            .replace("&#xa;", "\n")
            .replace("&#xA;", "\n")
    )
    return text.strip()


def _text_anchor(align: str) -> str:
    return {"left": "start", "right": "end"}.get(align, "middle")


def _baseline_dy(v_align: str, font_size: float, total_h: float, n_lines: int, line_h: float) -> float:
    """Return the Y offset for the first text line given vertical alignment."""
    text_block_h = n_lines * line_h
    if v_align == "top":
        return font_size + 2
    elif v_align == "bottom":
        return total_h - text_block_h + font_size
    else:  # middle
        return (total_h - text_block_h) / 2 + font_size


# ---------------------------------------------------------------------------
# SVG element builders
# ---------------------------------------------------------------------------

def _svg_rect(x: float, y: float, w: float, h: float, style: dict) -> str:
    fill   = style["fillColor"] if style["fillColor"] not in ("none",) else "none"
    stroke = style["strokeColor"] if style["strokeColor"] not in ("none",) else "none"
    sw     = style["strokeWidth"]
    rx     = 5 if style["rounded"] not in ("0", "") else 0
    if "arcSize" in style:
        rx = min(w, h) * float(style["arcSize"]) / 100
    dash   = 'stroke-dasharray="8,4"' if style["dashed"] not in ("0", "") else ""
    op     = float(style.get("opacity", "100")) / 100
    op_attr = f'opacity="{op}"' if op < 1 else ""
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" rx="{rx}" ry="{rx}" '
        f'{dash} {op_attr}/>'
    )


def _svg_ellipse(x: float, y: float, w: float, h: float, style: dict) -> str:
    fill   = style["fillColor"] if style["fillColor"] != "none" else "none"
    stroke = style["strokeColor"] if style["strokeColor"] != "none" else "none"
    sw     = style["strokeWidth"]
    dash   = 'stroke-dasharray="8,4"' if style["dashed"] not in ("0", "") else ""
    cx, cy, rx, ry = x + w / 2, y + h / 2, w / 2, h / 2
    return (
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {dash}/>'
    )


def _svg_label(
    label: str,
    x: float, y: float, w: float, h: float,
    style: dict,
) -> str:
    """Render a multi-line text label centred in the given box."""
    if not label:
        return ""
    font_size = float(style.get("fontSize", "11"))
    font_color = style.get("fontColor", "#000000")
    font_style_flag = int(style.get("fontStyle", "0"))
    fw = "bold" if font_style_flag & 1 else "normal"
    fi = "italic" if font_style_flag & 2 else "normal"
    align = style.get("align", "center")
    v_align = style.get("verticalAlign", "middle")
    anchor = _text_anchor(align)
    line_h = font_size * 1.25

    lines = label.split("\n")
    n = len(lines)

    # Horizontal anchor point
    if align == "left":
        tx = x + 4
    elif align == "right":
        tx = x + w - 4
    else:
        tx = x + w / 2

    # First-line Y offset from box top
    first_dy = _baseline_dy(v_align, font_size, h, n, line_h)
    first_y  = y + first_dy

    if n == 1:
        return (
            f'<text x="{tx}" y="{first_y}" '
            f'fill="{font_color}" font-size="{font_size}" '
            f'font-weight="{fw}" font-style="{fi}" text-anchor="{anchor}">'
            f'{_esc(label)}</text>'
        )

    parts = [
        f'<text x="{tx}" y="{first_y}" '
        f'fill="{font_color}" font-size="{font_size}" '
        f'font-weight="{fw}" font-style="{fi}" text-anchor="{anchor}">'
    ]
    for i, line in enumerate(lines):
        dy_attr = "" if i == 0 else f'dy="{line_h}"'
        parts.append(f'<tspan x="{tx}" {dy_attr}>{_esc(line)}</tspan>')
    parts.append("</text>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Cell rendering
# ---------------------------------------------------------------------------

def _render_vertex(cell: ET.Element, elems: list[str], _defs: dict[str, str]) -> None:
    geo = cell.find("mxGeometry")
    if geo is None:
        return
    x = float(geo.get("x", 0))
    y = float(geo.get("y", 0))
    w = float(geo.get("width", 0))
    h = float(geo.get("height", 0))

    style_str = cell.get("style", "")
    st = _merged_style(style_str)
    value = _strip_html(cell.get("value", "") or "")

    is_text = "text" in _parse_style(style_str) and st["fillColor"] in ("none",)
    is_ellipse = (
        "ellipse" in _parse_style(style_str)
        or st.get("shape") == "ellipse"
        or "perimeter=ellipsePerimeter" in style_str
    )

    if not is_text:
        if is_ellipse:
            elems.append(_svg_ellipse(x, y, w, h, st))
        else:
            elems.append(_svg_rect(x, y, w, h, st))

    elems.append(_svg_label(value, x, y, w, h, st))


def _render_edge(
    cell: ET.Element,
    all_cells: dict[str, ET.Element],
    elems: list[str],
    defs: dict[str, str],
) -> None:
    geo = cell.find("mxGeometry")
    if geo is None:
        return

    style_str = cell.get("style", "")
    st = _parse_style(style_str)
    stroke       = st.get("strokeColor", "#000000")
    stroke_width = st.get("strokeWidth", "1")
    end_arrow    = st.get("endArrow", "block")
    start_arrow  = st.get("startArrow", "none")
    dashed       = st.get("dashed", "0") not in ("0", "")

    def _center(cid: str | None) -> tuple[float, float] | None:
        if not cid:
            return None
        c = all_cells.get(cid)
        if c is None:
            return None
        g = c.find("mxGeometry")
        if g is None:
            return None
        cx = float(g.get("x", 0)) + float(g.get("width", 0)) / 2
        cy = float(g.get("y", 0)) + float(g.get("height", 0)) / 2
        return cx, cy

    src_pt = _center(cell.get("source"))
    tgt_pt = _center(cell.get("target"))

    # Collect explicit waypoints
    pts_elem = geo.find('Array[@as="points"]')
    waypoints: list[tuple[float, float]] = []
    if pts_elem is not None:
        waypoints = [
            (float(p.get("x", 0)), float(p.get("y", 0)))
            for p in pts_elem.findall("mxPoint")
        ]

    # Fallback: source/target from mxPoint children in geometry
    if src_pt is None:
        for pt in geo.findall("mxPoint"):
            if pt.get("as") == "sourcePoint":
                src_pt = (float(pt.get("x", 0)), float(pt.get("y", 0)))
    if tgt_pt is None:
        for pt in geo.findall("mxPoint"):
            if pt.get("as") == "targetPoint":
                tgt_pt = (float(pt.get("x", 0)), float(pt.get("y", 0)))

    if src_pt is None or tgt_pt is None:
        return  # cannot draw without endpoints

    # Build path
    all_pts = [src_pt] + waypoints + [tgt_pt]
    d = "M " + " L ".join(f"{px} {py}" for px, py in all_pts)

    # Arrowhead markers
    def _arrow_marker(arrow_type: str, color: str, prefix: str) -> str:
        mid = f"arr_{len(defs)}_{prefix}"
        defs[mid] = (
            f'<marker id="{mid}" markerWidth="10" markerHeight="10" '
            f'refX="9" refY="3" orient="auto">'
            f'<path d="M0,0 L0,6 L9,3 z" fill="{color}"/></marker>'
        )
        return mid

    marker_end_attr = ""
    marker_start_attr = ""
    if end_arrow not in ("none", ""):
        mid = _arrow_marker(end_arrow, stroke, "e")
        marker_end_attr = f'marker-end="url(#{mid})"'
    if start_arrow not in ("none", ""):
        mid = _arrow_marker(start_arrow, stroke, "s")
        marker_start_attr = f'marker-start="url(#{mid})"'

    dash_attr = 'stroke-dasharray="8,4"' if dashed else ""
    elems.append(
        f'<path d="{d}" stroke="{stroke}" stroke-width="{stroke_width}" '
        f'fill="none" {dash_attr} {marker_end_attr} {marker_start_attr}/>'
    )


# ---------------------------------------------------------------------------
# Core renderer
# ---------------------------------------------------------------------------

class DrawioRenderer:
    """Read a draw.io file, extract a named page, and render it to SVG.

    Usage::

        renderer = DrawioRenderer()
        svg_path = renderer.ensure_svg(
            drawio_path  = project_root / "assets/diagrams/application-landscape.drawio",
            page_name    = "current-state",
            out_dir      = project_root / "assets/diagrams",
            target_width = box_w,    # image-card body width  in px
            target_height= box_h,    # image-card body height in px
        )
        # svg_path == project_root / "assets/diagrams/current-state.svg"
    """

    # ------------------------------------------------------------------
    # File parsing
    # ------------------------------------------------------------------

    def _decode_diagram_content(self, diagram_elem: ET.Element) -> ET.Element | None:
        """Return the mxGraphModel element from a <diagram> node.

        draw.io stores page content in one of three ways:
        1. As a child <mxGraphModel> element (preferred for programmatic files).
        2. As raw XML text inside the <diagram> element.
        3. As base64 + deflate-compressed, URL-encoded text (draw.io desktop default).
        """
        # 1. Child mxGraphModel
        mxg = diagram_elem.find("mxGraphModel")
        if mxg is not None:
            return mxg

        # 2 & 3. Text content
        content = (diagram_elem.text or "").strip()
        if not content:
            return None

        # Try compressed (draw.io desktop format)
        try:
            raw = base64.b64decode(content)
            decompressed = zlib.decompress(raw, -15)
            xml_str = urllib.parse.unquote(decompressed.decode("utf-8"))
            return ET.fromstring(xml_str)
        except Exception:
            pass

        # Try raw XML text
        try:
            return ET.fromstring(content)
        except ET.ParseError:
            pass

        return None

    def extract_page(self, drawio_path: Path, page_name: str) -> ET.Element:
        """Return the <mxGraphModel> for the named page.

        Also handles legacy single-page files (bare <mxGraphModel> root).
        """
        tree = ET.parse(drawio_path)
        root = tree.getroot()

        # Legacy: the file IS the mxGraphModel (no <mxfile> wrapper)
        if root.tag == "mxGraphModel":
            if page_name:
                logger.warning(
                    "File %s has no named pages; using the single diagram "
                    "(requested page: '%s').",
                    drawio_path, page_name,
                )
            return root

        # Multi-page mxfile
        for diag in root.findall("diagram"):
            if diag.get("name") == page_name:
                mxg = self._decode_diagram_content(diag)
                if mxg is not None:
                    return mxg
                raise ValueError(
                    f"Page '{page_name}' in {drawio_path} has no readable mxGraphModel content."
                )

        # Fallback: first page
        for diag in root.findall("diagram"):
            mxg = self._decode_diagram_content(diag)
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
        target_width: float | None = None,
        target_height: float | None = None,
    ) -> str:
        """Convert an mxGraphModel element to an SVG string.

        Args:
            mxgraph_model: Parsed <mxGraphModel> element.
            target_width:  Desired rendered width (SVG width attribute, px).
            target_height: Desired rendered height (SVG height attribute, px).
                           The viewBox always uses the model's pageWidth/pageHeight,
                           so the diagram scales without distortion.

        Returns:
            Complete SVG document as a string.
        """
        page_w = float(mxgraph_model.get("pageWidth", 1280))
        page_h = float(mxgraph_model.get("pageHeight", 720))
        bg     = mxgraph_model.get("background", "#FFFFFF")
        if bg in ("", "none"):
            bg = "#FFFFFF"

        root = mxgraph_model.find("root")
        if root is None:
            return self._empty_svg(page_w, page_h, target_width, target_height, bg)

        # Index all cells by id for edge source/target lookup
        all_cells: dict[str, ET.Element] = {
            c.get("id", ""): c for c in root.findall("mxCell")
        }

        elems: list[str] = []
        defs:  dict[str, str] = {}

        # Render vertices first (z-order: backgrounds under foregrounds)
        for cell in root.findall("mxCell"):
            if cell.get("vertex") == "1" and cell.find("mxGeometry") is not None:
                _render_vertex(cell, elems, defs)

        # Then edges (drawn on top of shapes)
        for cell in root.findall("mxCell"):
            if cell.get("edge") == "1":
                _render_edge(cell, all_cells, elems, defs)

        defs_block = ""
        if defs:
            defs_block = "<defs>" + "\n".join(defs.values()) + "</defs>"

        w_attr = f' width="{int(target_width)}"'   if target_width  else ""
        h_attr = f' height="{int(target_height)}"' if target_height else ""

        return (
            f'<svg xmlns="http://www.w3.org/2000/svg"'
            f' viewBox="0 0 {page_w} {page_h}"{w_attr}{h_attr}'
            f' preserveAspectRatio="xMidYMid slice"'
            f' font-family="Segoe UI, Arial, sans-serif">\n'
            f'  <rect width="{page_w}" height="{page_h}" fill="{bg}"/>\n'
            f'  {defs_block}\n'
            + "\n".join(f"  {e}" for e in elems if e)
            + "\n</svg>"
        )

    @staticmethod
    def _empty_svg(pw, ph, tw, th, bg) -> str:
        w_attr = f' width="{int(tw)}"' if tw else ""
        h_attr = f' height="{int(th)}"' if th else ""
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {pw} {ph}"{w_attr}{h_attr}'
            f' preserveAspectRatio="xMidYMid slice">'
            f'<rect width="{pw}" height="{ph}" fill="{bg}"/></svg>'
        )

    # ------------------------------------------------------------------
    # Cache-aware entry point
    # ------------------------------------------------------------------

    def ensure_svg(
        self,
        drawio_path: Path,
        page_name: str,
        out_dir: Path,
        target_width:  float | None = None,
        target_height: float | None = None,
    ) -> Path:
        """Ensure a current SVG exists for *page_name* in *drawio_path*.

        The SVG is written to ``{out_dir}/{page_name}.svg``.
        It is (re-)generated when the draw.io file is newer than the SVG or the
        SVG does not yet exist.

        Args:
            drawio_path:   Absolute path to the ``.drawio`` source file.
            page_name:     Name of the diagram page/tab to render.
            out_dir:       Directory where the SVG is written.
            target_width:  Image-card body width in px  (sets SVG width attr).
            target_height: Image-card body height in px (sets SVG height attr).

        Returns:
            Path to the generated (or cached) SVG file.
        """
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        svg_path   = out_dir / f"{page_name}.svg"
        drawio_mtime = drawio_path.stat().st_mtime
        svg_mtime    = svg_path.stat().st_mtime if svg_path.exists() else 0

        if drawio_mtime <= svg_mtime:
            logger.debug("SVG is up-to-date: %s", svg_path)
            return svg_path

        logger.info(
            "Generating SVG for page '%s' from %s → %s",
            page_name, drawio_path.name, svg_path.name,
        )
        mxgraph_model = self.extract_page(drawio_path, page_name)
        svg_content   = self.render_to_svg(mxgraph_model, target_width, target_height)
        svg_path.write_text(svg_content, encoding="utf-8")
        return svg_path


# ---------------------------------------------------------------------------
# Module-level singleton (reused across renderers in a single build)
# ---------------------------------------------------------------------------
_renderer = DrawioRenderer()


def ensure_diagram_svg(
    drawio_path: Path,
    page_name: str,
    out_dir: Path,
    target_width: float | None = None,
    target_height: float | None = None,
) -> Path:
    """Convenience wrapper around ``DrawioRenderer.ensure_svg``."""
    return _renderer.ensure_svg(drawio_path, page_name, out_dir, target_width, target_height)
