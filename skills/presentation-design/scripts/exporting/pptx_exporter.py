"""
PptxExporter — Export rendered slides to PowerPoint (.pptx).

Consumes the renderer's element tree (list of RenderBox per slide) and writes
shapes to a python-pptx Presentation object.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

from scripts.rendering.base_card import RenderBox

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

    def export(
        self,
        slides: list[RenderBox],
        output_path: str | Path,
        *,
        canvas_width: int = 1280,
        canvas_height: int = 720,
    ) -> Path:
        """Write the rendered slide boxes to a ``.pptx`` file.

        Args:
            slides: List of ``RenderBox`` objects (one per slide), each containing
                    render elements produced by the layout and card renderers.
            output_path: Destination file path.
            canvas_width: Slide width in px.
            canvas_height: Slide height in px.

        Returns:
            The resolved output ``Path``.
        """
        prs = Presentation()
        prs.slide_width = _px(canvas_width)
        prs.slide_height = _px(canvas_height)

        blank_layout = prs.slide_layouts[6]  # Blank layout

        for slide_box in slides:
            pptx_slide = prs.slides.add_slide(blank_layout)
            for elem in slide_box.elements:
                self._render_element(pptx_slide, elem)

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        prs.save(str(out))
        logger.info("Exported PPTX: %s", out)
        return out

    # ── element rendering ────────────────────────────────────────────────

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
        elif etype == "placeholder":
            pass  # placeholders are not rendered in PPTX
        else:
            logger.debug("Unknown element type: %s", etype)

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
        tf = txBox.text_frame
        # Zero internal margins so element coordinates match visual positions exactly
        tf.margin_top = 0
        tf.margin_bottom = 0
        tf.margin_left = 0
        tf.margin_right = 0
        tf.word_wrap = elem.get("wrap", False)
        p = tf.paragraphs[0]
        p.text = str(elem.get("text", ""))
        p.alignment = _ALIGN_MAP.get(elem.get("alignment", "left"), PP_ALIGN.LEFT)

        run = p.runs[0] if p.runs else p.add_run()
        # font_size tokens are in px; convert to pt (1pt = 96/72 px at 96 DPI)
        run.font.size = Pt(float(elem.get("font_size", 14)) * 72 / 96)
        color = _rgb(str(elem.get("font_color", "#000000")))
        if color:
            run.font.color.rgb = color
        weight = elem.get("font_weight", "normal")
        run.font.bold = weight == "bold"
        run.font.italic = elem.get("font_style") == "italic"
        font_family = elem.get("font_family")
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
        stroke_color = _rgb(str(elem.get("stroke", "#CCCCCC")))
        if stroke_color:
            connector.line.color.rgb = stroke_color
        connector.line.width = Pt(float(elem.get("stroke_width", 1)) * 72 / 96)

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
            slide.shapes.add_picture(
                img_path,
                _px(elem["x"]),
                _px(elem["y"]),
                _px(elem["w"]),
                _px(elem["h"]),
            )
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
