"""
PptxExporter — Export rendered slides to PowerPoint (.pptx).

Consumes the renderer's element tree (list of RenderBox per slide) and writes
shapes to a python-pptx Presentation object.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any
import uuid

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

from scripts.rendering.base_card import RenderBox
from scripts.exporting.icon_resolver import IconResolver

logger = logging.getLogger(__name__)

# EMU per pixel at 96 DPI (PowerPoint native)
_EMU_PER_PX = 914400 / 96  # = 9525


def _px(val: float) -> int:
    """Convert a pixel value to EMU (all CSS coordinate tokens are in px)."""
    return int(val * _EMU_PER_PX)


def _rgb(hex_color: str) -> RGBColor | None:
    """Parse ``#RRGGBB`` to ``RGBColor``. Returns None for transparent/invalid."""
    if not hex_color or hex_color.lower() == "transparent":
        return None
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        return None
    try:
        return RGBColor(
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
        )
    except (ValueError, TypeError):
        return None


# ── Icon font glyph substitution ────────────────────────────────────────────
# Material Icons/Symbols use CSS text ligatures ("campaign" → icon glyph). This
# is a browser-only feature; PowerPoint does NOT process font ligatures, so the
# literal text sits invisible in the slide. We substitute each known ligature name
# with a standard Unicode symbol that renders in any presentation font at export
# time and is always visible in the right colour.
_ICON_UNICODE_MAP: dict[str, str] = {
    # Navigation / directional
    "home":              "⌂",
    "arrow_forward":     "→",
    "arrow_back":        "←",
    "arrow_upward":      "↑",
    "arrow_downward":    "↓",
    "trending_up":       "↑",
    "trending_down":     "↓",
    "open_in_new":       "↗",
    # Status / feedback
    "check":             "✓",
    "check_circle":      "◉",
    "close":             "✕",
    "error":             "✖",
    "warning":           "⚠",
    "info":              "ℹ",
    "help":              "?",
    "flag":              "⚑",
    # People / social
    "person":            "◉",
    "people":            "◎",
    "groups":            "◎",
    "group":             "◎",
    # Actions / tools
    "settings":          "⚙",
    "engineering":       "⚙",
    "build":             "⚙",
    "search":            "⌕",
    "edit":              "✎",
    "delete":            "✕",
    "add":               "+",
    "remove":            "−",
    "campaign":          "◈",
    "rocket_launch":     "▲",
    # Content / media
    "star":              "★",
    "star_border":       "☆",
    "favorite":          "♥",
    "lightbulb":         "◉",
    "label":             "◆",
    "tag":               "◆",
    "bookmark":          "▼",
    # Data / charts
    "bar_chart":         "▤",
    "pie_chart":         "◔",
    "analytics":         "▤",
    "insights":          "▤",
    "table_chart":       "▦",
    "space_dashboard":   "⊞",
    # Geography / globe
    "public":            "◎",
    "language":          "◎",
    "location_on":       "◎",
    "place":             "◎",
    # Industry / transport
    "elevator":          "▲",
    "escalator":         "▲",
    "business":          "◆",
    "factory":           "◆",
    "precision_manufacturing": "⚙",
    # Additional material symbol fallbacks
    "shield":           "🛡",
    "autorenew":        "↻",
    "visibility":       "👁",
    "gavel":            "⚖",
}
# Fallback glyph when the icon name is not in the map above
_ICON_FALLBACK_GLYPH = "◉"
# Font families that use ligatures (substring match, case-insensitive)
_ICON_FONT_MARKERS = ("material icons", "material symbols")

_ALIGN_MAP = {
    "left": PP_ALIGN.LEFT,
    "center": PP_ALIGN.CENTER,
    "right": PP_ALIGN.RIGHT,
}


class PptxExporter:
    """Export rendered slides to a ``.pptx`` file.

    Args:
        project_root: Path to the presentation project folder (for asset resolution).
    """

    def __init__(self, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root) if project_root else None
        _cache = (self.project_root / "assets" / "icons") if self.project_root else Path("/tmp/pptx_icon_cache")
        self._icon_resolver = IconResolver(_cache)

    def export(
        self,
        slides: list[RenderBox],
        output_path: str | Path,
        *,
        canvas_width: int = 1280,
        canvas_height: int = 720,
        slide_titles: list[str] | None = None,
        section_breaks: dict[int, str] | None = None,
    ) -> Path:
        """Write the rendered slide boxes to a ``.pptx`` file.

        Args:
            slides: List of ``RenderBox`` objects (one per slide), each containing
                    render elements produced by the layout and card renderers.
            output_path: Destination file path.
            canvas_width: Slide width in px.
            canvas_height: Slide height in px.
            slide_titles: Optional list of slide titles; used as the slide name
                          shown in PowerPoint's slide panel.
            section_breaks: Optional mapping of slide-index → section name;
                            injects PowerPoint sections at those boundaries.

        Returns:
            The resolved output ``Path``.
        """
        prs = Presentation()
        prs.slide_width = _px(canvas_width)
        prs.slide_height = _px(canvas_height)

        blank_layout = prs.slide_layouts[6]  # Blank layout

        for slide_idx, slide_box in enumerate(slides):
            pptx_slide = prs.slides.add_slide(blank_layout)
            # Name the slide after its title so it appears in the slides panel
            title = (
                (slide_titles[slide_idx] if slide_titles and slide_idx < len(slide_titles) else None)
                or f"Slide {slide_idx + 1}"
            )
            pptx_slide._element.cSld.set("name", title)
            for elem in slide_box.elements:
                self._render_element(pptx_slide, elem)

        # Inject PPTX sections if provided
        if section_breaks:
            self._inject_sections(prs, section_breaks)

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        prs.save(str(out))
        logger.info("Exported PPTX: %s", out)
        return out

    # ── element rendering ────────────────────────────────────────────────

    @staticmethod
    def _inject_sections(prs: "Presentation", section_breaks: dict[int, str]) -> None:
        """Inject PowerPoint section markers into *prs* using OOXML p14 namespace.

        Sections are a PowerPoint 2010+ feature stored in ``<p14:sectionLst>``
        as a direct child of ``<p:presentation>``.  Each section lists the
        numeric IDs of the slides it contains, taken from ``<p:sldIdLst>``.

        Args:
            prs: The python-pptx ``Presentation`` object (not yet saved).
            section_breaks: Maps slide-index (0-based) → section name.
        """
        from lxml import etree

        P14_NS = "http://schemas.microsoft.com/office/powerpoint/2010/main"
        P14 = f"{{{P14_NS}}}"

        # Collect slide numeric IDs in order from the presentation sldIdLst
        prs_elem = prs._element
        sld_id_lst = prs_elem.find(
            "{http://schemas.openxmlformats.org/presentationml/2006/main}sldIdLst"
        )
        if sld_id_lst is None:
            logger.warning("Cannot inject PPTX sections: sldIdLst not found")
            return

        slide_ids = [
            int(el.get("id"))
            for el in sld_id_lst
            if el.get("id") is not None
        ]
        n_slides = len(slide_ids)

        # Build ordered list of (start_index, section_name)
        breaks_sorted = sorted(section_breaks.items())

        # Build <p14:sectionLst>
        sec_lst = etree.Element(f"{P14}sectionLst", nsmap={"p14": P14_NS})

        for i, (start_idx, name) in enumerate(breaks_sorted):
            end_idx = breaks_sorted[i + 1][0] if i + 1 < len(breaks_sorted) else n_slides
            sec = etree.SubElement(sec_lst, f"{P14}section")
            sec.set("name", name)
            sec.set("id", "{" + str(uuid.uuid4()).upper() + "}")
            sld_id_lst_sec = etree.SubElement(sec, f"{P14}sldIdLst")
            for idx in range(start_idx, min(end_idx, n_slides)):
                sld_id_el = etree.SubElement(sld_id_lst_sec, f"{P14}sldId")
                sld_id_el.set("id", str(slide_ids[idx]))

        # Append to <p:presentation> — PowerPoint expects it as the last child
        prs_elem.append(sec_lst)
        logger.debug("Injected %d PPTX sections", len(breaks_sorted))

    def _render_element(self, slide, elem: dict[str, Any]) -> None:
        """Dispatch a single render element to the appropriate PPTX shape."""
        etype = elem.get("type", "")
        if etype == "rect":
            self._add_rect(slide, elem)
        elif etype == "text":
            self._add_text(slide, elem)
        elif etype == "line":
            self._add_line(slide, elem)
        elif etype == "image":
            self._add_image(slide, elem)
        elif etype == "icon":
            self._add_icon(slide, elem)
        elif etype == "ellipse":
            self._add_ellipse(slide, elem)
        elif etype == "placeholder":
            pass  # placeholders are not rendered in PPTX
        else:
            logger.debug("Unknown element type: %s", etype)

    def _add_ellipse(self, slide, elem: dict[str, Any]) -> None:
        shape = slide.shapes.add_shape(
            9,  # MSO_AUTO_SHAPE_TYPE.OVAL
            _px(elem["x"]),
            _px(elem["y"]),
            _px(elem["w"]),
            _px(elem["h"]),
        )
        fill_color = _rgb(str(elem.get("fill", "#FFFFFF")))
        if fill_color:
            shape.fill.solid()
            shape.fill.fore_color.rgb = fill_color
        else:
            shape.fill.background()
        if hasattr(shape, "shadow"):
            try:
                shape.shadow.inherit = False
                shape.shadow.visible = False
            except Exception:
                pass
        stroke_color = _rgb(str(elem.get("stroke", "")))
        if stroke_color:
            from pptx.util import Pt
            shape.line.color.rgb = stroke_color
            shape.line.width = Pt(float(elem.get("stroke_width", 1)) * 72 / 96)
        else:
            shape.line.fill.background()

    def _add_rect(self, slide, elem: dict[str, Any]) -> None:
        from pptx.util import Emu

        shape = slide.shapes.add_shape(
            1,  # MSO_SHAPE.RECTANGLE
            _px(elem["x"]),
            _px(elem["y"]),
            _px(elem["w"]),
            _px(elem["h"]),
        )
        fill_color = _rgb(str(elem.get("fill", "#FFFFFF")))
        if fill_color:
            shape.fill.solid()
            shape.fill.fore_color.rgb = fill_color
        else:
            shape.fill.background()

        if hasattr(shape, "shadow"):
            try:
                shape.shadow.inherit = False
                shape.shadow.visible = False
            except Exception:
                pass

        stroke_color = _rgb(str(elem.get("stroke", "")))
        if stroke_color:
            shape.line.color.rgb = stroke_color
            shape.line.width = Pt(float(elem.get("stroke_width", 1)) * 72 / 96)
        else:
            shape.line.fill.background()

    def _add_text(self, slide, elem: dict[str, Any]) -> None:
        from pptx.util import Emu
        w = elem.get("w", 200)
        h = elem.get("h", elem.get("font_size", 14) * 2)
        txBox = slide.shapes.add_textbox(
            _px(elem["x"]),
            _px(elem["y"]),
            _px(w),
            _px(h),
        )
        try:
            txBox.line.fill.background()
            if hasattr(txBox, "shadow"):
                txBox.shadow.inherit = False
                txBox.shadow.visible = False
        except Exception:
            pass
        tf = txBox.text_frame
        # Zero internal margins so element coordinates match visual positions exactly
        tf.margin_top = 0
        tf.margin_bottom = 0
        tf.margin_left = 0
        tf.margin_right = 0
        tf.word_wrap = elem.get("wrap", False)

        # Vertical alignment via XML bodyPr anchor attribute
        v_align = elem.get("vertical_align", "top")
        _ANCHOR_MAP = {"top": "t", "middle": "ctr", "bottom": "b"}
        anchor_val = _ANCHOR_MAP.get(v_align, "t")
        _NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
        body_pr = tf._txBody.find(f"{{{_NS}}}bodyPr")
        if body_pr is not None:
            body_pr.set("anchor", anchor_val)

        # ── Icon font substitution ────────────────────────────────────────
        # Material Symbols/Icons uses CSS text ligatures which PPTX does not
        # process. Substitute the ligature name with a standard Unicode symbol
        # and drop the special font requirement so the glyph is always visible.
        raw_text = str(elem.get("text", ""))
        font_family = elem.get("font_family")
        if font_family and any(m in font_family.lower() for m in _ICON_FONT_MARKERS):
            # Ligature name heuristic: all-lowercase, may contain underscores
            if raw_text and (raw_text.islower() or "_" in raw_text):
                raw_text = _ICON_UNICODE_MAP.get(raw_text, _ICON_FALLBACK_GLYPH)
                font_family = None  # standard font — glyph is in BMP, no icon font needed

        p = tf.paragraphs[0]
        p.text = raw_text
        p.alignment = _ALIGN_MAP.get(elem.get("alignment", "left"), PP_ALIGN.LEFT)
        line_height = elem.get("line_height")
        if line_height is not None:
            try:
                p.line_spacing = Pt(float(line_height) * 72 / 96)
            except Exception:
                pass

        run = p.runs[0] if p.runs else p.add_run()
        # font_size tokens are in px; convert to pt (1pt = 96/72 px at 96 DPI)
        run.font.size = Pt(float(elem.get("font_size", 14)) * 72 / 96)
        color = _rgb(str(elem.get("font_color", "#000000")))
        if color:
            run.font.color.rgb = color
        weight = elem.get("font_weight", "normal")
        style = str(elem.get("font_style") or "").lower()
        run.font.bold = str(weight).lower() in ("bold", "700") or "bold" in style
        run.font.italic = "italic" in style
        if font_family:
            run.font.name = str(font_family)

    def _add_line(self, slide, elem: dict[str, Any]) -> None:
        connector = slide.shapes.add_connector(
            1,  # MSO_CONNECTOR.STRAIGHT
            _px(elem["x1"]),
            _px(elem["y1"]),
            _px(elem["x2"]),
            _px(elem["y2"]),
        )
        stroke_color = _rgb(str(elem.get("stroke", "")))
        if stroke_color:
            connector.line.color.rgb = stroke_color
            connector.line.width = Pt(float(elem.get("stroke_width", 1)) * 72 / 96)
        else:
            connector.line.fill.background()
        try:
            if hasattr(connector, "shadow"):
                connector.shadow.inherit = False
                connector.shadow.visible = False
        except Exception:
            pass

    def _add_icon(self, slide, elem: dict[str, Any]) -> None:
        """Render an icon element — SVG download preferred, Unicode fallback."""
        name = str(elem.get("name", ""))
        color = str(elem.get("color") or "#000000")
        font_family = str(elem.get("font_family") or "")
        x, y = elem["x"], elem["y"]
        size = float(elem.get("w") or elem.get("h") or 20)

        # Try SVG→PNG conversion for PPTX (python-pptx uses PIL which can't read SVG)
        png_path = self._icon_resolver.resolve_png(name, font_family, color, size=int(size * 2))
        if png_path is not None:
            try:
                slide.shapes.add_picture(
                    str(png_path),
                    _px(x), _px(y), _px(size), _px(size),
                )
                return
            except Exception as exc:
                logger.warning("PPTX PNG picture failed for %s: %s — falling back to Unicode", name, exc)

        # Fallback: Unicode symbol substitution
        fallback_char = _ICON_UNICODE_MAP.get(name, _ICON_FALLBACK_GLYPH)
        self._add_text(slide, {
            "type": "text",
            "x": x, "y": y, "w": size, "h": size,
            "text": fallback_char,
            "font_size": size,
            "font_color": color,
            "font_weight": "normal",
            "alignment": "center",
        })

    def _add_image(self, slide, elem: dict[str, Any]) -> None:
        src = elem.get("src", "")
        if not src:
            # Render placeholder rect instead
            self._add_rect(
                slide,
                {
                    "x": elem["x"],
                    "y": elem["y"],
                    "w": elem["w"],
                    "h": elem["h"],
                    "fill": "#F5F5F5",
                    "stroke": "#CCCCCC",
                    "stroke_width": 1,
                },
            )
            return

        # Resolve path
        img_path = None
        if self.project_root:
            candidate = self.project_root / "assets" / src
            if candidate.exists():
                img_path = str(candidate)

        if img_path:
            try:
                picture = None
                # python-pptx does not support SVG natively; try cairosvg conversion
                if img_path.lower().endswith(".svg"):
                    try:
                        import cairosvg, io
                        png_bytes = cairosvg.svg2png(url=img_path)
                        picture = slide.shapes.add_picture(
                            io.BytesIO(png_bytes),
                            _px(elem["x"]),
                            _px(elem["y"]),
                            _px(elem["w"]),
                            _px(elem["h"]),
                        )
                    except ImportError:
                        logger.info("cairosvg not available — SVG logo skipped in PPTX (%s)", src)
                else:
                    picture = slide.shapes.add_picture(
                        img_path,
                        _px(elem["x"]),
                        _px(elem["y"]),
                        _px(elem["w"]),
                        _px(elem["h"]),
                    )
                if picture is not None:
                    try:
                        picture.line.fill.background()
                        if hasattr(picture, "shadow"):
                            picture.shadow.inherit = False
                            picture.shadow.visible = False
                    except Exception:
                        pass
            except Exception as exc:
                logger.warning("Failed to add image %s to PPTX: %s", src, exc)
        else:
            logger.warning("Image not found: %s — rendering placeholder", src)
            # Placeholder with missing path text
            self._add_rect(
                slide,
                {
                    "x": elem["x"],
                    "y": elem["y"],
                    "w": elem["w"],
                    "h": elem["h"],
                    "fill": "#FFF3E0",
                    "stroke": "#FF9800",
                    "stroke_width": 1,
                },
            )
            self._add_text(
                slide,
                {
                    "x": elem["x"],
                    "y": elem["y"] + elem["h"] * 0.4,
                    "w": elem["w"],
                    "text": f"[missing: {src}]",
                    "font_size": 10,
                    "font_color": "#FF9800",
                    "alignment": "center",
                },
            )
