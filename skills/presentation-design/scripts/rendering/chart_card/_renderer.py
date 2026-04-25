"""ChartCardRenderer — chart-card type, native primitive-based charts.

Supports four chart types selectable via ``content.chart_type``:

  bar     Vertical grouped or stacked bar chart
  line    Line chart with optional point markers
  pie     Pie or donut chart
  combo   Bars for primary series + line overlay for secondary series

See themes/base.css section 7 for design tokens (.card--chart).
"""

from __future__ import annotations

import logging
import math
from pathlib import Path

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox
from scripts.rendering.chart_card._cartesian import draw_cartesian
from scripts.rendering.chart_card._legend import draw_legend
from scripts.rendering.chart_card._palette import resolve_palette, series_color
from scripts.rendering.chart_card._pie import draw_pie

_logger = logging.getLogger(__name__)


class ChartCardRenderer(BaseCardRenderer):
    """Renderer for ``chart-card`` type — native primitive-based charts."""

    variant = "card--chart"

    def __init__(self, theme, *, project_root: str | Path | None = None) -> None:
        super().__init__(theme)
        self.project_root = Path(project_root) if project_root else None

    # Backwards-compat thin wrappers (used by tests / external callers)
    def _palette(self) -> list[str]:
        return resolve_palette(self)

    def _series_color(self, series: list[dict], idx: int) -> str:
        return series_color(self, series, idx)

    # ── Main entry point ──────────────────────────────────────────────

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        content = card.content if isinstance(card.content, dict) else {}

        # Image path shortcut
        image_path = content.get("image", "")
        if image_path:
            self._render_image_fallback(card, box, content, image_path)
            return

        # Shared token resolution
        axis_color       = self._tok("axis-color")
        axis_font_size   = self._f("axis-font-size",          9)
        axis_font_color  = self._tok("axis-font-color",       axis_color)
        grid_color       = self._tok("grid-color")
        legend_font_size = self._f("legend-font-size",        10)
        legend_pos_tok   = self._tok("legend-position",       "bottom")
        caption_font_sz  = self._f("caption-font-size",       10)
        caption_color    = self._tok("caption-font-color")
        caption_align    = self._tok("caption-alignment",     "center")
        label_font_size  = self._f("label-font-size",         9)
        label_font_color = self._tok("label-font-color")
        title_font_size  = self._f("axis-title-font-size",    10)
        title_font_color = self._tok("axis-title-font-color", axis_color)

        # Content fields
        chart_type   = str(content.get("chart_type", "bar")).lower()
        series_raw   = content.get("series", [])
        if not isinstance(series_raw, list):
            series_raw = []
        labels       = [str(l) for l in content.get("labels", [])]
        stacked      = bool(content.get("stacked", False))
        value_labels = bool(content.get("value_labels", False))
        inner_radius = float(content.get("inner_radius", 0.0))
        caption      = str(content.get("caption", ""))

        # Axis config
        x_axis_cfg = content.get("x_axis", {}) or {}
        y_axis_cfg = content.get("y_axis", {}) or {}
        x_visible  = bool(x_axis_cfg.get("visible", True))
        y_visible  = bool(y_axis_cfg.get("visible", True))
        x_title    = str(x_axis_cfg.get("title", ""))
        y_title    = str(y_axis_cfg.get("title", ""))
        y_min_forced  = y_axis_cfg.get("min")
        y_max_forced  = y_axis_cfg.get("max")
        y_step_forced = y_axis_cfg.get("step")
        y_fmt         = str(y_axis_cfg.get("format", ""))

        # Legend config
        legend_cfg  = content.get("legend", {}) or {}
        legend_vis  = bool(legend_cfg.get("visible", True))
        leg_pos_raw = legend_cfg.get("position")
        legend_pos  = str(leg_pos_raw).lower() if leg_pos_raw else legend_pos_tok
        if legend_pos == "none":
            legend_vis = False

        # Space reservations
        cap_h = (caption_font_sz + 6) if caption else 0

        swatch = int(legend_font_size) + 4
        leg_item_h = swatch + 4
        leg_h = leg_w = 0.0
        if legend_vis and series_raw:
            if legend_pos in ("bottom", "top"):
                rows = math.ceil(len(series_raw) / max(1, int(box.w / 120)))
                leg_h = rows * leg_item_h + 6
            elif legend_pos == "right":
                leg_w = 100.0

        x_title_h = (title_font_size + 6) if x_title else 0
        y_title_w = (title_font_size + 6) if y_title else 0

        # Plot area geometry
        pad_left   = 42 + y_title_w
        pad_right  = 8 + leg_w
        pad_top    = (leg_h + 4) if legend_pos == "top" else 8
        pad_bottom = 22 + x_title_h

        plot_x = box.x + pad_left
        plot_y = box.y + pad_top
        plot_w = max(20.0, box.w - pad_left - pad_right)
        plot_h = max(20.0, box.h - pad_top - pad_bottom - cap_h
                     - (leg_h if legend_pos == "bottom" else 0))

        # Dispatch chart type
        if chart_type == "pie":
            draw_pie(self, box, plot_x, plot_y, plot_w, plot_h,
                     series_raw, labels, inner_radius,
                     value_labels, label_font_size, label_font_color,
                     self._draw_placeholder)
        else:
            draw_cartesian(self, box, plot_x, plot_y, plot_w, plot_h,
                           series_raw, labels, chart_type,
                           stacked, value_labels,
                           y_min_forced, y_max_forced, y_step_forced, y_fmt,
                           axis_color, axis_font_size, axis_font_color,
                           grid_color, x_visible, y_visible,
                           label_font_size, label_font_color,
                           self._draw_placeholder)

        # Axis titles
        if x_title:
            box.add({"type": "text",
                     "x": plot_x, "y": plot_y + plot_h + 14,
                     "w": plot_w, "h": title_font_size + 4,
                     "text": x_title, "font_size": title_font_size,
                     "font_color": title_font_color, "alignment": "center",
                     "vertical_align": "middle", "wrap": False})
        if y_title:
            box.add({"type": "text",
                     "x": box.x, "y": plot_y, "w": title_font_size + 4, "h": plot_h,
                     "text": y_title, "font_size": title_font_size,
                     "font_color": title_font_color, "alignment": "center",
                     "vertical_align": "middle", "wrap": False})

        # Legend
        if legend_vis and series_raw:
            draw_legend(self, box, plot_x, plot_y, plot_w, plot_h,
                        series_raw, legend_pos, leg_h, leg_w,
                        legend_font_size, swatch)

        # Caption
        if caption:
            cap_y = box.y + box.h - cap_h
            box.add({"type": "text",
                     "x": box.x, "y": cap_y, "w": box.w, "h": cap_h,
                     "text": caption, "font_size": caption_font_sz,
                     "font_color": caption_color,
                     "alignment": caption_align, "wrap": False})

    # ── Image fallback / placeholder ──────────────────────────────────

    def _render_image_fallback(
        self, card: CardModel, box: RenderBox, content: dict, image_path: str
    ) -> None:
        """Render a plain image + optional caption when chart content supplies an image path."""
        if self.project_root:
            full = self.project_root / "assets" / image_path
            if not full.exists():
                _logger.warning("Chart asset not found: %s (expected at %s)", image_path, full)

        caption = str(content.get("caption", ""))
        caption_h = 20 if caption else 0
        img_h = box.h - caption_h

        box.add({"type": "image",
                 "x": box.x, "y": box.y, "w": box.w, "h": img_h,
                 "src": image_path, "alt": str(content.get("alt", "")),
                 "fit": self._tok("image-fit", "contain"),
                 "border_radius": self._tok("image-border-radius", 4)})

        if caption:
            box.add({"type": "text",
                     "x": box.x, "y": box.y + img_h + 4, "w": box.w,
                     "text": caption,
                     "font_size": self._f("caption-font-size", 11),
                     "font_color": self._tok("caption-font-color"),
                     "alignment": self._tok("caption-alignment", "center")})

    def _draw_placeholder(
        self, box: RenderBox, px: float, py: float, pw: float, ph: float
    ) -> None:
        border = self._tok("grid-color")
        box.add({"type": "rect",
                 "x": px, "y": py, "w": pw, "h": ph,
                 "fill": "#F9FAFB", "stroke": border, "stroke_width": 1, "rx": 4})
        box.add({"type": "text",
                 "x": px, "y": py + ph * 0.4, "w": pw,
                 "text": "[No chart data]",
                 "font_size": 11, "font_color": "#AAAAAA", "alignment": "center"})
