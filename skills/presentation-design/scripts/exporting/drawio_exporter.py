"""
DrawioExporter — Export rendered slides to draw.io (.drawio) XML format.

Each slide becomes a separate page in the draw.io document. Render elements
are mapped to mxGraph XML cells.
"""

from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
import base64

from scripts.rendering.base_card import RenderBox
from scripts.exporting.icon_resolver import IconResolver

logger = logging.getLogger(__name__)


class DrawioExporter:
    """Export rendered slides to a ``.drawio`` file.

    Args:
        project_root: Path to the presentation project folder.
    """

    def __init__(self, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root) if project_root else None
        _cache = (self.project_root / "assets" / "icons") if self.project_root else Path("/tmp/drawio_icon_cache")
        self._icon_resolver = IconResolver(_cache)

    def export(
        self,
        slides: list[RenderBox],
        output_path: str | Path,
        *,
        canvas_width: int = 1280,
        canvas_height: int = 720,
        slide_titles: list[str] | None = None,
    ) -> Path:
        """Write the rendered slide boxes to a ``.drawio`` file.

        Args:
            slides: List of ``RenderBox`` objects (one per slide).
            output_path: Destination file path.
            canvas_width: Slide width in px.
            canvas_height: Slide height in px.
            slide_titles: Optional list of slide titles used as diagram tab names.

        Returns:
            The resolved output ``Path``.
        """
        root = ET.Element("mxfile")
        root.set("host", "presentation-design")

        for page_idx, slide_box in enumerate(slides):
            # Tab name: slide title when available, else generic fallback
            tab_name = (
                (slide_titles[page_idx] if slide_titles and page_idx < len(slide_titles) else None)
                or f"Slide {page_idx + 1}"
            )
            diagram = ET.SubElement(root, "diagram")
            diagram.set("name", tab_name)
            diagram.set("id", f"slide-{page_idx}")

            mx_model = ET.SubElement(diagram, "mxGraphModel")
            mx_model.set("dx", "0")
            mx_model.set("dy", "0")
            mx_model.set("grid", "1")
            mx_model.set("gridSize", "10")
            mx_model.set("guides", "1")
            mx_model.set("tooltips", "1")
            mx_model.set("connect", "1")
            mx_model.set("arrows", "1")
            mx_model.set("fold", "1")
            mx_model.set("page", "1")
            mx_model.set("pageScale", "1")
            mx_model.set("pageWidth", str(canvas_width))
            mx_model.set("pageHeight", str(canvas_height))

            mx_root = ET.SubElement(mx_model, "root")
            # Default parent cells required by draw.io
            cell0 = ET.SubElement(mx_root, "mxCell")
            cell0.set("id", "0")
            cell1 = ET.SubElement(mx_root, "mxCell")
            cell1.set("id", "1")
            cell1.set("parent", "0")

            cell_id = 2
            for elem in slide_box.elements:
                cell_id = self._add_element(mx_root, elem, cell_id, page_idx)

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(str(out), encoding="utf-8", xml_declaration=True)
        logger.info("Exported draw.io: %s", out)
        return out

    # ── element rendering ────────────────────────────────────────────────

    def _add_element(
        self, mx_root: ET.Element, elem: dict[str, Any], cell_id: int, page_idx: int
    ) -> int:
        """Add a draw.io mxCell for the given element. Return next cell_id."""
        etype = elem.get("type", "")
        if etype == "rect":
            return self._add_rect(mx_root, elem, cell_id)
        elif etype == "text":
            return self._add_text(mx_root, elem, cell_id)
        elif etype == "line":
            return self._add_line(mx_root, elem, cell_id)
        elif etype == "image":
            return self._add_image(mx_root, elem, cell_id)
        elif etype == "icon":
            return self._add_icon(mx_root, elem, cell_id)
        elif etype == "ellipse":
            return self._add_ellipse(mx_root, elem, cell_id)
        elif etype == "table":
            return self._add_table(mx_root, elem, cell_id, page_idx)
        elif etype == "bullet_list":
            return self._add_bullet_list(mx_root, elem, cell_id)
        elif etype == "placeholder":
            return cell_id  # skip placeholders
        return cell_id

    def _add_bullet_list(
        self, mx_root: ET.Element, elem: dict[str, Any], cell_id: int
    ) -> int:
        """Render a bullet list as a single draw.io HTML text cell.

        All bullet items are combined into one mxCell whose value is an HTML
        string: each item is one line with a colour-spanned marker followed by
        the item text, joined by ``<br/>``.  This avoids the older pattern of
        one separate marker cell + one text cell per bullet.
        """
        cell = ET.SubElement(mx_root, "mxCell")
        cell.set("id", str(cell_id))
        cell.set("parent", "1")
        cell.set("vertex", "1")

        font_size = float(elem.get("font_size", 14))
        font_size_pt = round(font_size, 1)
        font_color = str(elem.get("font_color") or "#000000")
        weight = elem.get("font_weight", "normal")
        style_str = str(elem.get("font_style") or "").lower()
        is_bold = str(weight).lower() in ("bold", "700") or "bold" in style_str
        is_italic = "italic" in style_str
        align = elem.get("alignment", "left")
        font_style_num = (1 if is_bold else 0) + (2 if is_italic else 0)

        bullet_char = str(elem.get("bullet_char") or "\u2022")
        bullet_color = str(elem.get("bullet_color") or font_color)
        bullet_gap_px = float(elem.get("bullet_gap", 8))
        bullet_spacing_px = float(elem.get("bullet_spacing", 4))
        # &nbsp; is ~0.25em wide at the current font size.
        gap_nbsp_count = max(1, round(bullet_gap_px / 4))
        gap_nbsp = "&nbsp;" * gap_nbsp_count
        # Hanging indent: first line has the marker + gap at the left; wrapped
        # lines are pushed right so they align under the text start, not the
        # bullet glyph.  hang_em ≈ bullet glyph width (0.7em) + gap nbsp width.
        hang_em = round(0.7 + gap_nbsp_count * 0.25, 2)

        style = (
            f"text;html=1;fontSize={font_size_pt};fontColor={font_color};"
            f"fontStyle={font_style_num};"
            f"align={align};verticalAlign=top;whiteSpace=wrap;"
            f"fillColor=none;strokeColor=none;overflow=hidden;"
        )
        cell.set("style", style)

        # Build one HTML <p> per bullet item; bottom-margin creates vertical spacing
        parts: list[str] = []
        for item in elem.get("items", []):
            runs_data = item.get("runs")
            if runs_data:
                text_parts: list[str] = []
                for r_data in runs_data:
                    t = (
                        str(r_data["text"])
                        .replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;")
                    )
                    r_bold = bool(r_data.get("bold"))
                    r_italic = bool(r_data.get("italic"))
                    if r_bold and r_italic:
                        t = f"<b><i>{t}</i></b>"
                    elif r_bold:
                        t = f"<b>{t}</b>"
                    elif r_italic:
                        t = f"<i>{t}</i>"
                    text_parts.append(t)
                item_html = "".join(text_parts)
            else:
                item_html = (
                    str(item.get("text", ""))
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                )

            if bullet_char:
                marker = f'<span style="color:{bullet_color}">{bullet_char}</span>{gap_nbsp}'
            else:
                marker = ""
            # padding-left + negative text-indent = CSS hanging indent:
            # first line (marker) sits at x=0; wrapped lines indent by hang_em.
            spacing_style = (
                f'margin:0 0 {int(bullet_spacing_px)}px 0;'
                f'padding-left:{hang_em}em;text-indent:-{hang_em}em'
            )
            parts.append(f'<p style="{spacing_style}">{marker}{item_html}</p>')

        cell.set("value", "".join(parts))

        geo = ET.SubElement(cell, "mxGeometry")
        geo.set("x", str(elem["x"]))
        geo.set("y", str(elem["y"]))
        geo.set("width", str(elem["w"]))
        geo.set("height", str(elem["h"]))
        geo.set("as", "geometry")
        return cell_id + 1

    def _add_ellipse(
        self, mx_root: ET.Element, elem: dict[str, Any], cell_id: int
    ) -> int:
        cell = ET.SubElement(mx_root, "mxCell")
        cell.set("id", str(cell_id))
        cell.set("parent", "1")
        cell.set("vertex", "1")
        fill = elem.get("fill", "#FFFFFF")
        stroke = elem.get("stroke", "none")
        sw = elem.get("stroke_width", 1)
        style = (
            f"ellipse;fillColor={fill};"
            f"strokeColor={stroke};strokeWidth={sw};"
        )
        cell.set("style", style)
        cell.set("value", "")
        geo = ET.SubElement(cell, "mxGeometry")
        geo.set("x", str(elem["x"]))
        geo.set("y", str(elem["y"]))
        geo.set("width", str(elem["w"]))
        geo.set("height", str(elem["h"]))
        geo.set("as", "geometry")
        return cell_id + 1

    def _add_rect(
        self, mx_root: ET.Element, elem: dict[str, Any], cell_id: int
    ) -> int:
        cell = ET.SubElement(mx_root, "mxCell")
        cell.set("id", str(cell_id))
        cell.set("parent", "1")
        cell.set("vertex", "1")

        fill = elem.get("fill", "#FFFFFF")
        stroke = elem.get("stroke", "none")
        sw = elem.get("stroke_width", 1)
        rx = elem.get("rx", 0)
        opacity = elem.get("opacity")  # 0-100; None means fully opaque
        style = (
            f"rounded=1;arcSize={rx};fillColor={fill};"
            f"strokeColor={stroke};strokeWidth={sw};"
        )
        if opacity is not None:
            style += f"opacity={int(opacity)};"
        cell.set("style", style)
        cell.set("value", "")

        geo = ET.SubElement(cell, "mxGeometry")
        geo.set("x", str(elem["x"]))
        geo.set("y", str(elem["y"]))
        geo.set("width", str(elem["w"]))
        geo.set("height", str(elem["h"]))
        geo.set("as", "geometry")

        return cell_id + 1

    def _add_text(
        self, mx_root: ET.Element, elem: dict[str, Any], cell_id: int
    ) -> int:
        cell = ET.SubElement(mx_root, "mxCell")
        cell.set("id", str(cell_id))
        cell.set("parent", "1")
        cell.set("vertex", "1")

        font_size = elem.get("font_size", 14)
        # Font-size tokens are defined in pt — use directly
        font_size_pt = round(float(font_size), 1)
        font_color = elem.get("font_color", "#000000")
        weight = elem.get("font_weight", "normal")
        style = str(elem.get("font_style") or "").lower()
        bold = "1" if (str(weight).lower() in ("bold", "700") or "bold" in style) else "0"
        italic = "1" if "italic" in style else "0"
        align = elem.get("alignment", "left")
        font_family = elem.get("font_family", "")
        font_family_attr = f"fontFamily={font_family};" if font_family else ""

        v_align = elem.get("vertical_align", "top")
        drawio_valign = {"top": "top", "middle": "middle", "bottom": "bottom"}.get(v_align, "top")
        line_height = elem.get("line_height")
        line_spacing_style = ""
        if line_height is not None:
            try:
                spacing_ratio = float(line_height) / float(font_size)
                line_spacing_style = f"lineSpacing={spacing_ratio:.2f};"
            except Exception:
                line_spacing_style = ""

        wrap_val = elem.get("wrap", True)
        ws = "wrap" if wrap_val else "nowrap"
        # Allow wrapped text to flow slightly beyond cell bounds (subtitle, take-away)
        # so long text is not clipped. Non-wrapping text stays clipped.
        overflow = "visible" if wrap_val else "hidden"
        style = (
            f"text;html=1;fontSize={font_size_pt};fontColor={font_color};"
            f"fontStyle={(int(bold) * 1) + (int(italic) * 2)};"
            f"{font_family_attr}"
            f"align={align};verticalAlign={drawio_valign};whiteSpace={ws};"
            f"{line_spacing_style}"
            f"fillColor=none;strokeColor=none;overflow={overflow};"
        )
        cell.set("style", style)

        runs_data = elem.get("runs")
        if runs_data:
            # Build an HTML string where each run is wrapped in <b>/<i> as needed.
            # draw.io already uses html=1 in the style string above, so HTML tags
            # in the value are rendered correctly.
            parts: list[str] = []
            for r_data in runs_data:
                t = (
                    str(r_data["text"])
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                )
                r_bold = bool(r_data.get("bold"))
                r_italic = bool(r_data.get("italic"))
                if r_bold and r_italic:
                    t = f"<b><i>{t}</i></b>"
                elif r_bold:
                    t = f"<b>{t}</b>"
                elif r_italic:
                    t = f"<i>{t}</i>"
                parts.append(t)
            cell.set("value", "".join(parts))
        else:
            cell.set("value", str(elem.get("text", "")))

        w = elem.get("w", 200)
        h = elem.get("h", float(font_size) + 8)
        geo = ET.SubElement(cell, "mxGeometry")
        geo.set("x", str(elem["x"]))
        geo.set("y", str(elem["y"]))
        geo.set("width", str(w))
        geo.set("height", str(h))
        geo.set("as", "geometry")

        return cell_id + 1

    def _add_line(
        self, mx_root: ET.Element, elem: dict[str, Any], cell_id: int
    ) -> int:
        cell = ET.SubElement(mx_root, "mxCell")
        cell.set("id", str(cell_id))
        cell.set("parent", "1")
        cell.set("edge", "1")
        cell.set("source", "")
        cell.set("target", "")

        stroke = elem.get("stroke", "#CCCCCC")
        sw = elem.get("stroke_width", 1)
        dashed = elem.get("dashed", False)
        style = (
            f"endArrow=none;strokeColor={stroke};strokeWidth={sw};"
            f"edgeStyle=straightEdgeStyle;"
        )
        if dashed:
            style += "dashed=1;"
        cell.set("style", style)
        cell.set("value", "")

        geo = ET.SubElement(cell, "mxGeometry")
        geo.set("relative", "1")
        geo.set("as", "geometry")

        src_pt = ET.SubElement(geo, "mxPoint")
        src_pt.set("x", str(elem["x1"]))
        src_pt.set("y", str(elem["y1"]))
        src_pt.set("as", "sourcePoint")

        tgt_pt = ET.SubElement(geo, "mxPoint")
        tgt_pt.set("x", str(elem["x2"]))
        tgt_pt.set("y", str(elem["y2"]))
        tgt_pt.set("as", "targetPoint")

        return cell_id + 1

    def _add_icon(
        self, mx_root: ET.Element, elem: dict[str, Any], cell_id: int
    ) -> int:
        """Render an icon as an embedded URL-encoded SVG image in draw.io.

        draw.io's style-string parser splits on ``;`` which breaks
        ``data:image/svg+xml;base64,...`` URIs (the ``;base64`` separator is
        treated as the start of a new token).  Using
        ``data:image/svg+xml,<url-encoded-svg>`` avoids any semicolon inside
        the URI, so the complete image value is preserved.
        """
        from urllib.parse import quote as _url_quote  # noqa: PLC0415

        name = str(elem.get("name", ""))
        color = str(elem.get("color") or "#000000")
        font_family = str(elem.get("font_family") or "")

        from scripts.exporting.pptx_exporter import _ICON_UNICODE_MAP, _ICON_FALLBACK_GLYPH  # noqa: PLC0415

        icon_family_lower = font_family.lower()
        if name in _ICON_UNICODE_MAP and any(marker in icon_family_lower for marker in ("material icons", "material symbols", "phosphor")):
            fallback_char = _ICON_UNICODE_MAP[name]
            icon_size = elem.get("w") or elem.get("h") or 20
            return self._add_text(mx_root, {
                "x": elem["x"],
                "y": elem["y"],
                "w": icon_size,
                "h": int(icon_size * 1.2),  # buffer for font descent in draw.io
                "text": fallback_char,
                "font_size": int(icon_size),
                "font_color": color,
                "font_weight": "bold",
                "alignment": "center",
                "vertical_align": "middle",
            }, cell_id)

        svg_path = self._icon_resolver.resolve(name, font_family, color)
        if svg_path is not None:
            try:
                svg_text = svg_path.read_text(encoding="utf-8")
                # URL-encode everything including ";" so no raw semicolons remain.
                encoded = _url_quote(svg_text, safe="")
                data_uri = f"data:image/svg+xml,{encoded}"

                cell = ET.SubElement(mx_root, "mxCell")
                cell.set("id", str(cell_id))
                cell.set("parent", "1")
                cell.set("vertex", "1")
                # Place image= LAST so other tokens come before it and the
                # encoded value (which contains no raw ";") ends cleanly.
                style = (
                    "shape=image;imageAspect=1;aspect=fixed;"
                    f"fillColor=none;strokeColor=none;image={data_uri};"
                )
                cell.set("style", style)
                cell.set("value", "")

                geo = ET.SubElement(cell, "mxGeometry")
                geo.set("x", str(elem["x"]))
                geo.set("y", str(elem["y"]))
                geo.set("width", str(elem.get("w", 20)))
                geo.set("height", str(elem.get("h", 20)))
                geo.set("as", "geometry")
                return cell_id + 1
            except Exception as exc:
                logger.warning("draw.io SVG icon failed for %s: %s \u2014 falling back to Unicode", name, exc)

        fallback_char = _ICON_UNICODE_MAP.get(name, _ICON_FALLBACK_GLYPH)
        icon_size = elem.get("w") or elem.get("h") or 20
        return self._add_text(mx_root, {
            "x": elem["x"],
            "y": elem["y"],
            "w": icon_size,
            "h": int(icon_size * 1.2),  # buffer for font descent in draw.io
            "text": fallback_char,
            "font_size": int(icon_size),
            "font_color": color,
            "font_weight": "bold",
            "alignment": "center",
            "vertical_align": "middle",
        }, cell_id)

    def _add_image(
        self, mx_root: ET.Element, elem: dict[str, Any], cell_id: int
    ) -> int:
        import mimetypes
        src = elem.get("src", "")

        # Embed the image as a base64 data URI so draw.io can display it
        # without needing local file access (file paths are opaque to draw.io).
        #
        # draw.io's style-string parser splits on ALL ";" characters, so
        # "data:image/png;base64,..." is split at ";base64" — the image value
        # is truncated to "data:image/png".  Percent-encoding the semicolon
        # ("%3B") prevents the split while remaining a valid data URI (the
        # browser/draw.io renderer decodes %3B back to ";" when loading).
        data_uri = None
        if src and self.project_root:
            img_path = self.project_root / "assets" / src
            if img_path.exists():
                if img_path.suffix.lower() == ".svg":
                    # SVG: URL-encode the text — identical to _add_icon's approach.
                    # shape=image with a data:image/svg+xml,<url-encoded> URI is
                    # the only draw.io mechanism that reliably renders SVG. The
                    # html=1 / value approach doesn't work because draw.io's HTML
                    # label renderer strips <svg> elements entirely.
                    from urllib.parse import quote as _url_quote
                    svg_text = img_path.read_text(encoding="utf-8")
                    encoded = _url_quote(svg_text, safe="")
                    data_uri = f"data:image/svg+xml,{encoded}"

                    fit_mode = elem.get("fit", "contain")
                    # cover: imageAspect=0 — draw.io fills the cell geometry;
                    #   the SVG's own preserveAspectRatio="xMidYMid slice" then
                    #   fills without letterboxing and clips edges symmetrically.
                    # contain: imageAspect=1;aspect=fixed — draw.io letterboxes
                    #   the image to maintain aspect ratio within the cell.
                    if fit_mode == "cover":
                        img_style = (
                            f"shape=image;imageAspect=0;"
                            f"fillColor=none;strokeColor=none;image={data_uri};"
                        )
                    else:
                        img_style = (
                            f"shape=image;imageAspect=1;aspect=fixed;"
                            f"fillColor=none;strokeColor=none;image={data_uri};"
                        )

                    cell = ET.SubElement(mx_root, "mxCell")
                    cell.set("id", str(cell_id))
                    cell.set("parent", "1")
                    cell.set("vertex", "1")
                    cell.set("style", img_style)
                    cell.set("value", "")

                    geo = ET.SubElement(cell, "mxGeometry")
                    geo.set("x", str(elem["x"]))
                    geo.set("y", str(elem["y"]))
                    geo.set("width", str(elem["w"]))
                    geo.set("height", str(elem["h"]))
                    geo.set("as", "geometry")

                    return cell_id + 1
                else:
                    # Raster images: base64 with percent-encoded semicolon so
                    # draw.io's style parser doesn't split at ";base64".
                    mime = mimetypes.guess_type(str(img_path))[0] or "image/png"
                    img_b64 = base64.b64encode(img_path.read_bytes()).decode("ascii")
                    data_uri = f"data:{mime}%3Bbase64,{img_b64}"
            else:
                logger.warning("Image not found: %s \u2014 rendering placeholder", src)

        cell = ET.SubElement(mx_root, "mxCell")
        cell.set("id", str(cell_id))
        cell.set("parent", "1")
        cell.set("vertex", "1")

        # Place image= LAST so draw.io's ";" style-string parser doesn't
        # truncate the data URI at the ";base64" separator.
        if data_uri:
            style = f"shape=image;imageAspect=1;aspect=fixed;image={data_uri}"
        elif src:
            style = f"shape=image;imageAspect=1;aspect=fixed;image={src}"
        else:
            style = "rounded=1;fillColor=#F5F5F5;strokeColor=#CCCCCC;"
        cell.set("style", style)
        cell.set("value", elem.get("alt", ""))

        geo = ET.SubElement(cell, "mxGeometry")
        geo.set("x", str(elem["x"]))
        geo.set("y", str(elem["y"]))
        geo.set("width", str(elem["w"]))
        geo.set("height", str(elem["h"]))
        geo.set("as", "geometry")

        return cell_id + 1

    def _add_table(
        self,
        mx_root: ET.Element,
        elem: dict[str, Any],
        cell_id: int,
        page_idx: int,
    ) -> int:
        """Render a ``table`` element as a draw.io table using stacked rect+text cells.

        draw.io's native ``shape=table`` is interactive/editable only in the
        draw.io desktop app, and its XML format has changed across versions.
        For maximum compatibility and visual fidelity we build the table from
        individual rect (background fill) + text (cell content) mxCell pairs —
        one pair per cell — which matches the style of all other primitive
        elements in this exporter.
        """
        all_rows: list[dict] = elem.get("rows", [])
        col_widths_px: list[float] = elem.get("col_widths", [])
        border_color: str = str(elem.get("border_color") or "#E5E7EB")
        border_width: float = float(elem.get("border_width") or 1)
        pad_x: float = float(elem.get("pad_x") or 8)
        pad_y: float = float(elem.get("pad_y") or 4)

        n_rows = len(all_rows)
        n_cols = len(col_widths_px)
        if n_rows == 0 or n_cols == 0:
            return cell_id

        # Scale row heights to fit available height
        total_height = sum(float(r.get("row_height", 24)) for r in all_rows)
        available_h = float(elem.get("h") or total_height)
        scale = min(1.0, available_h / total_height) if total_height > 0 else 1.0
        row_heights = [float(r.get("row_height", 24)) * scale for r in all_rows]

        base_x = float(elem["x"])
        base_y = float(elem["y"])

        y_cursor = base_y
        for ri, row_desc in enumerate(all_rows):
            rh = row_heights[ri]
            x_cursor = base_x

            cells_text: list[str] = row_desc.get("cells", [])
            bg_color: str = str(row_desc.get("bg_color") or "#FFFFFF")
            fg_color: str = str(row_desc.get("font_color") or "#000000")
            font_size: float = float(row_desc.get("font_size") or 12)
            font_size_pt = round(font_size, 1)
            weight: str = str(row_desc.get("font_weight") or "normal")
            style_str: str = str(row_desc.get("font_style") or "normal").lower()
            aligns: list[str] = row_desc.get("alignments") or []
            bottom_border: str = str(row_desc.get("border_bottom_color") or border_color)
            is_bold = str(weight).lower() in ("bold", "700") or "bold" in style_str
            is_italic = "italic" in style_str
            font_style_num = (1 if is_bold else 0) + (2 if is_italic else 0)

            for ci, cw in enumerate(col_widths_px):
                cell_text = cells_text[ci] if ci < len(cells_text) else ""
                align = aligns[ci] if ci < len(aligns) else "left"

                # Bottom border is thicker/different for header row
                b_color = bottom_border if ri == 0 else border_color

                # Background rect with borders simulated via stroke
                bg_cell = ET.SubElement(mx_root, "mxCell")
                bg_cell.set("id", str(cell_id))
                bg_cell.set("parent", "1")
                bg_cell.set("vertex", "1")
                bg_style = (
                    f"fillColor={bg_color};"
                    f"strokeColor={border_color};strokeWidth={border_width};"
                    "rounded=0;"
                )
                # Override bottom stroke for header row
                if ri == 0:
                    bg_style += f"strokeBottom={b_color};"
                bg_cell.set("style", bg_style)
                bg_cell.set("value", "")
                bg_geo = ET.SubElement(bg_cell, "mxGeometry")
                bg_geo.set("x", str(round(x_cursor, 2)))
                bg_geo.set("y", str(round(y_cursor, 2)))
                bg_geo.set("width", str(round(cw, 2)))
                bg_geo.set("height", str(round(rh, 2)))
                bg_geo.set("as", "geometry")
                cell_id += 1

                # Text cell on top
                txt_cell = ET.SubElement(mx_root, "mxCell")
                txt_cell.set("id", str(cell_id))
                txt_cell.set("parent", "1")
                txt_cell.set("vertex", "1")
                txt_style = (
                    f"text;html=1;fontSize={font_size_pt};"
                    f"fontColor={fg_color};fontStyle={font_style_num};"
                    f"align={align};verticalAlign=middle;"
                    f"whiteSpace=wrap;overflow=hidden;"
                    f"fillColor=none;strokeColor=none;"
                )
                txt_cell.set("style", txt_style)
                txt_cell.set("value", str(cell_text))
                txt_geo = ET.SubElement(txt_cell, "mxGeometry")
                txt_geo.set("x", str(round(x_cursor + pad_x, 2)))
                txt_geo.set("y", str(round(y_cursor, 2)))
                txt_geo.set("width", str(round(max(cw - 2 * pad_x, 4), 2)))
                txt_geo.set("height", str(round(rh, 2)))
                txt_geo.set("as", "geometry")
                cell_id += 1

                x_cursor += cw

            y_cursor += rh

        return cell_id
