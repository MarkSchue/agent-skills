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
    # Phosphor icon names
    "trend-up":         "↑",
    "trend-down":       "↓",
    "rocket":           "▲",
    "lightbulb":        "◉",
    "chart-bar":        "▤",
    "chart-line":       "▤",
    "chart-scatter":    "▤",
    "tree":             "◆",
    "tree-structure":   "◆",
    "x":                "✕",
    "check":            "✓",
    "intersect":        "◎",
    "gear":             "⚙",
    "magnifying-glass": "⌕",
    "pencil":           "✎",
    "star":             "★",
    "heart":            "♥",
    "warning":          "⚠",
    "info":             "ℹ",
    "question":         "?",
    "flag":             "⚑",
    "house":            "⌂",
    "arrow-right":      "→",
    "arrow-left":       "←",
    "arrow-up":         "↑",
    "arrow-down":       "↓",
    "arrow-up-right":   "↗",
    "plus":             "+",
    "minus":            "−",
    "shield":           "🛡",
    "eye":              "👁",
    "scales":           "⚖",
    "database":         "◆",
    "cpu":              "⚙",
    "cloud":            "◎",
    "lock":             "◆",
    "user":             "◉",
    "users":            "◎",
    "factory":          "◆",
    "globe":            "◎",
    "map-pin":          "◎",
}
# Fallback glyph when the icon name is not in the map above
_ICON_FALLBACK_GLYPH = "◉"
# Font families that use ligatures (substring match, case-insensitive)
_ICON_FONT_MARKERS = ("material icons", "material symbols", "phosphor")

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
        elif etype == "table":
            self._add_table(slide, elem)
        elif etype == "bullet_list":
            self._add_bullet_list(slide, elem)
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
        stroke_width = float(elem.get("stroke_width", 1))
        if stroke_color and stroke_width > 0:
            from pptx.util import Pt
            shape.line.color.rgb = stroke_color
            shape.line.width = Pt(stroke_width * 72 / 96)
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
            # Apply opacity if specified (0-100).
            # OOXML: a:alpha val="100000" = fully opaque, val="0" = fully transparent.
            opacity_pct = elem.get("opacity")
            if opacity_pct is not None:
                try:
                    from pptx.oxml.ns import qn as _qn
                    from lxml import etree as _lET
                    alpha_val = int(float(opacity_pct) * 1000)  # e.g. 40 → 40000
                    spPr = shape._element.spPr
                    solid_fill = spPr.find(".//" + _qn("a:solidFill"))
                    if solid_fill is not None:
                        srgb = solid_fill.find(_qn("a:srgbClr"))
                        if srgb is not None:
                            alpha_el = _lET.SubElement(srgb, _qn("a:alpha"))
                            alpha_el.set("val", str(alpha_val))
                except Exception:
                    pass
        else:
            shape.fill.background()

        if hasattr(shape, "shadow"):
            try:
                shape.shadow.inherit = False
                shape.shadow.visible = False
            except Exception:
                pass

        stroke_color = _rgb(str(elem.get("stroke", "")))
        stroke_width = float(elem.get("stroke_width", 1))
        if stroke_color and stroke_width > 0:
            shape.line.color.rgb = stroke_color
            shape.line.width = Pt(stroke_width * 72 / 96)
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
        p.alignment = _ALIGN_MAP.get(elem.get("alignment", "left"), PP_ALIGN.LEFT)
        line_height = elem.get("line_height")
        if line_height is not None:
            try:
                p.line_spacing = Pt(float(line_height))
            except Exception:
                pass

        # Font-size tokens are defined in pt — use directly (no px→pt conversion needed)
        font_size_pt = Pt(float(elem.get("font_size", 14)))
        color = _rgb(str(elem.get("font_color", "#000000")))
        weight = elem.get("font_weight", "normal")
        style = str(elem.get("font_style") or "").lower()
        is_bold = str(weight).lower() in ("bold", "700") or "bold" in style
        is_italic = "italic" in style

        runs_data = elem.get("runs")
        if runs_data:
            # Multi-run path — inline bold/italic markup was present.
            # Do NOT use p.text setter; add each run explicitly so per-run
            # bold/italic attributes are preserved.
            for r_data in runs_data:
                run = p.add_run()
                run.text = r_data["text"]
                run.font.size = font_size_pt
                if color:
                    run.font.color.rgb = color
                run.font.bold = is_bold or bool(r_data.get("bold"))
                run.font.italic = is_italic or bool(r_data.get("italic"))
                if font_family:
                    run.font.name = str(font_family)
        else:
            # Single-run path — plain text, no inline markup.
            p.text = raw_text
            # Apply font properties to ALL runs — p.text setter splits on \n and
            # creates multiple <a:r> runs via add_br(); only setting run[0] would
            # leave subsequent runs with the slide-default (large) font size.
            for r in p.runs:
                r.font.size = font_size_pt
                if color:
                    r.font.color.rgb = color
                r.font.bold = is_bold
                r.font.italic = is_italic
                if font_family:
                    r.font.name = str(font_family)

    def _add_bullet_list(self, slide, elem: dict[str, Any]) -> None:
        """Render a bullet list as a single PPTX text box with native bullet paragraph formatting.

        Each bullet item becomes a paragraph with hanging-indent layout and
        ``<a:buChar>`` / ``<a:buClr>`` OOXML attributes so PowerPoint renders
        the marker natively — no separate marker text boxes needed.
        """
        from lxml import etree
        from pptx.oxml.ns import qn

        txBox = slide.shapes.add_textbox(
            _px(elem["x"]), _px(elem["y"]),
            _px(elem["w"]), _px(elem["h"]),
        )
        try:
            txBox.line.fill.background()
            if hasattr(txBox, "shadow"):
                txBox.shadow.inherit = False
                txBox.shadow.visible = False
        except Exception:
            pass

        tf = txBox.text_frame
        tf.margin_top = 0
        tf.margin_bottom = 0
        tf.margin_left = 0
        tf.margin_right = 0
        tf.word_wrap = True

        font_size_pt = Pt(float(elem.get("font_size", 14)))
        font_color_rgb = _rgb(str(elem.get("font_color") or "#000000"))
        weight = elem.get("font_weight", "normal")
        style_str = str(elem.get("font_style") or "").lower()
        is_bold = str(weight).lower() in ("bold", "700") or "bold" in style_str
        is_italic = "italic" in style_str
        align = _ALIGN_MAP.get(elem.get("alignment", "left"), PP_ALIGN.LEFT)

        bullet_char = str(elem.get("bullet_char") or "\u2022")  # fallback: •
        bullet_color_hex = str(
            elem.get("bullet_color") or elem.get("font_color") or "#000000"
        ).lstrip("#")
        bullet_indent_px = float(elem.get("bullet_indent", 16))
        # EMU: left margin for indented text; the hanging indent is the negative mirror
        bullet_indent_emu = int(bullet_indent_px * _EMU_PER_PX)

        items = elem.get("items", [])
        for i, item in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align

            # Hanging-indent layout: marL pushes text right, indent pulls marker left
            pPr = p._p.get_or_add_pPr()
            pPr.set("marL", str(bullet_indent_emu))
            pPr.set("indent", str(-bullet_indent_emu))

            # Bullet colour  <a:buClr><a:srgbClr val="RRGGBB"/></a:buClr>
            if len(bullet_color_hex) == 6:
                buClr = etree.SubElement(pPr, qn("a:buClr"))
                srgbClr = etree.SubElement(buClr, qn("a:srgbClr"))
                srgbClr.set("val", bullet_color_hex)

            # Bullet character (or suppress with buNone when style=none)
            if bullet_char:
                buChar = etree.SubElement(pPr, qn("a:buChar"))
                buChar.set("char", bullet_char)
            else:
                etree.SubElement(pPr, qn("a:buNone"))

            # Text run(s)
            runs_data = item.get("runs")
            if runs_data:
                for r_data in runs_data:
                    run = p.add_run()
                    run.text = r_data["text"]
                    run.font.size = font_size_pt
                    if font_color_rgb:
                        run.font.color.rgb = font_color_rgb
                    run.font.bold = is_bold or bool(r_data.get("bold"))
                    run.font.italic = is_italic or bool(r_data.get("italic"))
            else:
                run = p.add_run()
                run.text = str(item.get("text", ""))
                run.font.size = font_size_pt
                if font_color_rgb:
                    run.font.color.rgb = font_color_rgb
                run.font.bold = is_bold
                run.font.italic = is_italic

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
            if elem.get("dashed"):
                try:
                    from pptx.oxml.ns import qn as _qn2
                    from lxml import etree as _et2
                    spPr = connector._element.spPr
                    ln_el = spPr.find(_qn2("a:ln"))
                    if ln_el is None:
                        ln_el = _et2.SubElement(spPr, _qn2("a:ln"))
                    pd = ln_el.find(_qn2("a:prstDash"))
                    if pd is None:
                        pd = _et2.SubElement(ln_el, _qn2("a:prstDash"))
                    pd.set("val", "dash")
                except Exception:
                    pass
        else:
            connector.line.fill.background()
        try:
            if hasattr(connector, "shadow"):
                connector.shadow.inherit = False
                connector.shadow.visible = False
        except Exception:
            pass

    def _add_icon(self, slide, elem: dict[str, Any]) -> None:
        """Render an icon element — Unicode text for known icons, SVG→PNG for others.

        Logic mirrors draw.io: icons whose names are in ``_ICON_UNICODE_MAP`` and
        whose font-family is a Material Symbols / Phosphor family are rendered as a
        centered Unicode character so they fill their bounding box exactly (SVG
        files from the Google Fonts API have built-in design margins of ~10–15 %
        which would make the glyph visibly smaller than its badge outline).
        Unknown icons fall through to the SVG→PNG path.
        """
        name = str(elem.get("name", ""))
        color = str(elem.get("color") or "#000000")
        font_family = str(elem.get("font_family") or "")
        x, y = elem["x"], elem["y"]
        size = float(elem.get("w") or elem.get("h") or 20)
        # Caller may supply an explicit font_size (e.g. scope card: badge_size * 0.65)
        font_size = float(elem.get("font_size") or size)

        # ── Known icons: render as centered Unicode text (same as draw.io) ──────
        icon_family_lower = font_family.lower()
        if name in _ICON_UNICODE_MAP and any(
            marker in icon_family_lower
            for marker in ("material icons", "material symbols", "phosphor")
        ):
            self._add_text(slide, {
                "type": "text",
                "x": x, "y": y, "w": size, "h": size,
                "text": _ICON_UNICODE_MAP[name],
                "font_size": font_size,
                "font_color": color,
                "font_weight": "bold",
                "alignment": "center",
                "vertical_align": "middle",
            })
            return

        # ── Unknown icons: try SVG→PNG via cairosvg ──────────────────────────────
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

        # ── Final fallback: Unicode symbol, vertically centred ───────────────────
        fallback_char = _ICON_UNICODE_MAP.get(name, _ICON_FALLBACK_GLYPH)
        self._add_text(slide, {
            "type": "text",
            "x": x, "y": y, "w": size, "h": size,
            "text": fallback_char,
            "font_size": font_size,
            "font_color": color,
            "font_weight": "bold",
            "alignment": "center",
            "vertical_align": "middle",
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

                # Compute aspect-ratio-preserving box (fit=contain, centered)
                target_w = float(elem["w"])
                target_h = float(elem["h"])
                fit_x = float(elem["x"])
                fit_y = float(elem["y"])
                fit_w = target_w
                fit_h = target_h
                try:
                    from PIL import Image as _PILImg
                    with _PILImg.open(img_path) as _img:
                        nat_w, nat_h = _img.size
                    if nat_w > 0 and nat_h > 0:
                        scale = min(target_w / nat_w, target_h / nat_h)
                        fit_w = nat_w * scale
                        fit_h = nat_h * scale
                        fit_x = float(elem["x"]) + (target_w - fit_w) / 2
                        fit_y = float(elem["y"]) + (target_h - fit_h) / 2
                except Exception:
                    pass  # PIL unavailable or image unreadable — use full box

                # python-pptx does not support SVG natively; try cairosvg conversion
                if img_path.lower().endswith(".svg"):
                    try:
                        import cairosvg, io
                        png_bytes = cairosvg.svg2png(url=img_path)
                        picture = slide.shapes.add_picture(
                            io.BytesIO(png_bytes),
                            _px(fit_x),
                            _px(fit_y),
                            _px(fit_w),
                            _px(fit_h),
                        )
                    except ImportError:
                        logger.info("cairosvg not available — SVG logo skipped in PPTX (%s)", src)
                else:
                    picture = slide.shapes.add_picture(
                        img_path,
                        _px(fit_x),
                        _px(fit_y),
                        _px(fit_w),
                        _px(fit_h),
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

    def _add_table(self, slide, elem: dict[str, Any]) -> None:
        """Render a ``table`` element as a native python-pptx table shape.

        The table is positioned at the coordinates given in *elem* and sized
        to fit the available body area.  Each row descriptor in ``elem['rows']``
        carries its own styling so header, data, stripe, and sum rows are all
        handled uniformly.
        """
        from pptx.util import Pt
        from pptx.dml.color import RGBColor
        from pptx.enum.text import PP_ALIGN

        all_rows: list[dict] = elem.get("rows", [])
        col_widths_px: list[float] = elem.get("col_widths", [])
        border_color_hex: str = str(elem.get("border_color") or "#E5E7EB")
        border_width_pt: float = float(elem.get("border_width") or 1) * 72 / 96
        pad_x: float = float(elem.get("pad_x") or 8)
        pad_y: float = float(elem.get("pad_y") or 4)

        n_rows = len(all_rows)
        n_cols = len(col_widths_px)
        if n_rows == 0 or n_cols == 0:
            return

        # Total height: sum of row heights, capped to elem["h"]
        total_height = sum(float(r.get("row_height", 24)) for r in all_rows)
        available_h = float(elem.get("h") or total_height)
        # Scale row heights proportionally when they exceed available space
        scale = min(1.0, available_h / total_height) if total_height > 0 else 1.0

        row_heights_px = [float(r.get("row_height", 24)) * scale for r in all_rows]

        # python-pptx wants col widths and row heights in EMU
        col_w_emu = [_px(w) for w in col_widths_px]
        row_h_emu = [_px(h) for h in row_heights_px]

        tbl = slide.shapes.add_table(
            n_rows,
            n_cols,
            _px(elem["x"]),
            _px(elem["y"]),
            _px(elem["w"]),
            _px(available_h),
        ).table

        # Set column widths
        for ci, cw in enumerate(col_w_emu):
            tbl.columns[ci].width = cw

        # Set row heights
        for ri, rh in enumerate(row_h_emu):
            tbl.rows[ri].height = rh

        # Style each cell
        for ri, row_desc in enumerate(all_rows):
            cells: list[str] = row_desc.get("cells", [])
            bg_hex: str = str(row_desc.get("bg_color") or "#FFFFFF")
            fg_hex: str = str(row_desc.get("font_color") or "#000000")
            font_size: float = float(row_desc.get("font_size") or 12)
            weight: str = str(row_desc.get("font_weight") or "normal")
            style: str = str(row_desc.get("font_style") or "normal").lower()
            aligns: list[str] = row_desc.get("alignments") or []
            border_bottom_hex: str = str(row_desc.get("border_bottom_color") or border_color_hex)

            is_bold = str(weight).lower() in ("bold", "700") or "bold" in style
            is_italic = "italic" in style

            for ci in range(n_cols):
                cell = tbl.cell(ri, ci)
                cell_text = cells[ci] if ci < len(cells) else ""
                alignment = aligns[ci] if ci < len(aligns) else "left"

                # Background fill
                bg_rgb = _rgb(bg_hex)
                if bg_rgb:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = bg_rgb
                else:
                    cell.fill.background()

                # Text frame
                tf = cell.text_frame
                tf.margin_top = _px(pad_y)
                tf.margin_bottom = _px(pad_y)
                tf.margin_left = _px(pad_x)
                tf.margin_right = _px(pad_x)
                tf.word_wrap = True

                para = tf.paragraphs[0]
                para.text = cell_text
                para.alignment = _ALIGN_MAP.get(alignment, PP_ALIGN.LEFT)

                if para.runs:
                    run = para.runs[0]
                else:
                    run = para.add_run()
                    run.text = cell_text

                run.font.size = Pt(font_size)
                run.font.bold = is_bold
                run.font.italic = is_italic
                fg_rgb = _rgb(fg_hex)
                if fg_rgb:
                    run.font.color.rgb = fg_rgb

                # Cell borders via tcPr XML — apply uniform border_color
                self._set_table_cell_borders(
                    cell, border_color_hex, border_width_pt,
                    border_bottom_hex if ri == 0 else border_color_hex,
                )

    @staticmethod
    def _set_table_cell_borders(
        cell: Any,
        border_color_hex: str,
        border_width_pt: float,
        bottom_color_hex: str,
    ) -> None:
        """Apply solid borders on all four sides of a python-pptx table cell via OOXML."""
        from lxml import etree
        from pptx.oxml.ns import qn

        def _make_ln(color_hex: str, width_pt: float) -> "etree._Element":
            w_emu = int(width_pt * 12700)  # pt → EMU (1 pt = 12700 EMU)
            ln = etree.Element(qn("a:ln"), attrib={"w": str(w_emu)})
            solid = etree.SubElement(ln, qn("a:solidFill"))
            srgb = etree.Element(qn("a:srgbClr"), attrib={"val": color_hex.lstrip("#")})
            solid.append(srgb)
            return ln

        tc = cell._tc
        tcPr = tc.find(qn("a:tcPr"))
        if tcPr is None:
            tcPr = etree.SubElement(tc, qn("a:tcPr"))

        for tag, color in (
            ("a:lnL", border_color_hex),
            ("a:lnR", border_color_hex),
            ("a:lnT", border_color_hex),
            ("a:lnB", bottom_color_hex),
        ):
            existing = tcPr.find(qn(tag))
            if existing is not None:
                tcPr.remove(existing)
            tcPr.append(_make_ln(color, border_width_pt))
