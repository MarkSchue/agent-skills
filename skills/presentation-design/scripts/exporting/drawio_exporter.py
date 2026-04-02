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
        elif etype == "placeholder":
            return cell_id  # skip placeholders
        return cell_id

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
        style = (
            f"rounded=1;arcSize={rx};fillColor={fill};"
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

    def _add_text(
        self, mx_root: ET.Element, elem: dict[str, Any], cell_id: int
    ) -> int:
        cell = ET.SubElement(mx_root, "mxCell")
        cell.set("id", str(cell_id))
        cell.set("parent", "1")
        cell.set("vertex", "1")

        font_size = elem.get("font_size", 14)
        # Convert px → pt to match draw.io's internal unit (same as pptx exporter)
        font_size_pt = round(float(font_size) * 72 / 96, 1)
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
        style = (
            f"text;html=1;fontSize={font_size_pt};fontColor={font_color};"
            f"fontStyle={(int(bold) * 1) + (int(italic) * 2)};"
            f"{font_family_attr}"
            f"align={align};verticalAlign={drawio_valign};whiteSpace=wrap;overflow=hidden;"
            f"fillColor=none;strokeColor=none;"
        )
        cell.set("style", style)
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
        style = (
            f"endArrow=none;strokeColor={stroke};strokeWidth={sw};"
            f"edgeStyle=straightEdgeStyle;"
        )
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
        """Render an icon as an embedded base64 SVG image in draw.io."""
        name = str(elem.get("name", ""))
        color = str(elem.get("color") or "#000000")
        font_family = str(elem.get("font_family") or "")

        svg_path = self._icon_resolver.resolve(name, font_family, color)
        if svg_path is not None:
            try:
                svg_b64 = base64.b64encode(svg_path.read_bytes()).decode("ascii")
                data_uri = f"data:image/svg+xml;base64,{svg_b64}"

                cell = ET.SubElement(mx_root, "mxCell")
                cell.set("id", str(cell_id))
                cell.set("parent", "1")
                cell.set("vertex", "1")
                style = (
                    f"shape=image;image={data_uri};"
                    "imageAspect=1;aspect=fixed;"
                    "fillColor=none;strokeColor=none;"
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
                logger.warning("draw.io SVG icon failed for %s: %s — skipping", name, exc)

        # Fallback: skip (icon invisible but at least no crash)
        return cell_id

    def _add_image(
        self, mx_root: ET.Element, elem: dict[str, Any], cell_id: int
    ) -> int:
        src = elem.get("src", "")
        cell = ET.SubElement(mx_root, "mxCell")
        cell.set("id", str(cell_id))
        cell.set("parent", "1")
        cell.set("vertex", "1")

        if src:
            style = f"shape=image;image={src};imageAspect=0;"
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
