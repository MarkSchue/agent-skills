"""Legend rendering for chart cards."""

from __future__ import annotations

from scripts.rendering.base_card import RenderBox
from scripts.rendering.chart_card._palette import series_color


def draw_legend(
    renderer, box: RenderBox,
    px: float, py: float, pw: float, ph: float,
    series_raw: list[dict], position: str,
    leg_h: float, leg_w: float,
    font_size: float, swatch: float,
) -> None:
    leg_font_color = renderer._tok("legend-font-color")
    item_w = 115.0

    if position in ("bottom", "top"):
        leg_y = (box.y + box.h - leg_h + 2) if position == "bottom" else (box.y + 2)
        items_per_row = max(1, int(pw / item_w))
        for i, s in enumerate(series_raw):
            row = i // items_per_row
            col = i % items_per_row
            ix = px + col * item_w
            iy = leg_y + row * (swatch + 4)
            color = series_color(renderer, series_raw, i)
            box.add({"type": "rect",
                     "x": ix, "y": iy, "w": swatch, "h": swatch,
                     "fill": color, "stroke": "none", "stroke_width": 0, "rx": 2})
            box.add({"type": "text",
                     "x": ix + swatch + 3, "y": iy,
                     "w": item_w - swatch - 6, "h": swatch,
                     "text": str(s.get("name", f"Series {i + 1}")),
                     "font_size": font_size, "font_color": leg_font_color,
                     "alignment": "left", "vertical_align": "middle",
                     "wrap": False})
    elif position == "right":
        leg_x = px + pw + 6
        for i, s in enumerate(series_raw):
            iy = py + i * (swatch + 4)
            if iy + swatch > py + ph:
                break
            color = series_color(renderer, series_raw, i)
            box.add({"type": "rect",
                     "x": leg_x, "y": iy, "w": swatch, "h": swatch,
                     "fill": color, "stroke": "none", "stroke_width": 0, "rx": 2})
            box.add({"type": "text",
                     "x": leg_x + swatch + 3, "y": iy,
                     "w": leg_w - swatch - 6, "h": swatch,
                     "text": str(s.get("name", f"Series {i + 1}")),
                     "font_size": font_size, "font_color": leg_font_color,
                     "alignment": "left", "vertical_align": "middle",
                     "wrap": False})
