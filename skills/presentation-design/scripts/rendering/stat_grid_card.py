"""
StatGridCardRenderer — Renders stat-grid-card showing 2–6 large statistic
tiles inside ONE card. Different from kpi-card which holds a single metric;
stat-grid is the consulting "by the numbers" overview pattern.

Each stat = large value + small label. Auto-grid: 2 stats → 1×2, 3 → 1×3,
4 → 2×2, 5–6 → 2×3.
"""

from __future__ import annotations

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


def _grid_for(n: int) -> tuple[int, int]:
    """Return (rows, cols) for n stats."""
    if n <= 1:
        return (1, 1)
    if n == 2:
        return (1, 2)
    if n == 3:
        return (1, 3)
    if n == 4:
        return (2, 2)
    return (2, 3)  # 5 or 6


class StatGridCardRenderer(BaseCardRenderer):
    """Renderer for ``stat-grid-card`` type."""

    variant = "card--stat-grid"

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        content = card.content if isinstance(card.content, dict) else {}
        stats = content.get("stats") or []
        if not stats:
            return
        stats = list(stats)[:6]
        override_cols = self._tok("cols")
        if override_cols is not None:
            try:
                forced_cols = max(1, int(float(override_cols)))
                forced_rows = -(-len(stats) // forced_cols)  # ceiling division
                rows, cols = forced_rows, forced_cols
            except (TypeError, ValueError):
                rows, cols = _grid_for(len(stats))
        else:
            rows, cols = _grid_for(len(stats))

        gap_x = float(self._tok("tile-gap-x") or 16)
        gap_y = float(self._tok("tile-gap-y") or 16)
        sep_visible = str(self._tok("tile-separator-visible") or "true").lower() == "true"
        sep_color = self._tok("tile-separator-color") or self.resolve("color-border") or "#E0E0E0"
        sep_width = float(self._tok("tile-separator-width") or 1)

        value_size = float(self._tok("value-font-size") or 36)
        value_color = self._tok("value-font-color") or self.resolve("color-primary") or "#000099"
        value_weight = self._tok("value-font-weight") or "bold"
        label_size = float(self._tok("label-font-size") or 11)
        label_color = self._tok("label-font-color") or self.resolve("color-text-muted") or "#777"
        label_weight = self._tok("label-font-weight") or "normal"
        sub_size = float(self._tok("sub-font-size") or 10)
        sub_color = self._tok("sub-font-color") or self.resolve("color-text-muted") or "#888"
        align = self._tok("alignment") or "center"

        tile_w = (box.w - gap_x * (cols - 1)) / cols
        tile_h = (box.h - gap_y * (rows - 1)) / rows

        for i, stat in enumerate(stats):
            r = i // cols
            c = i % cols
            tx = box.x + c * (tile_w + gap_x)
            ty = box.y + r * (tile_h + gap_y)

            value = str(stat.get("value", "") if isinstance(stat, dict) else stat)
            label = str(stat.get("label", "") if isinstance(stat, dict) else "")
            sub = str(stat.get("sub", "") if isinstance(stat, dict) else "")

            # Vertical centering of value + label + sub block within tile
            block_h = value_size + (label_size + 6 if label else 0) + (sub_size + 4 if sub else 0)
            cy = ty + (tile_h - block_h) / 2

            # Value (large)
            box.add({
                "type": "text",
                "x": tx,
                "y": cy,
                "w": tile_w,
                "h": value_size + 4,
                "text": value,
                "font_size": value_size,
                "font_color": value_color,
                "font_weight": value_weight,
                "alignment": align,
            })
            cy += value_size + 6

            if label:
                box.add({
                    "type": "text",
                    "x": tx,
                    "y": cy,
                    "w": tile_w,
                    "h": label_size + 2,
                    "text": label,
                    "font_size": label_size,
                    "font_color": label_color,
                    "font_weight": label_weight,
                    "alignment": align,
                })
                cy += label_size + 4

            if sub:
                box.add({
                    "type": "text",
                    "x": tx,
                    "y": cy,
                    "w": tile_w,
                    "h": sub_size + 2,
                    "text": sub,
                    "font_size": sub_size,
                    "font_color": sub_color,
                    "alignment": align,
                })

            # Separator: thin vertical rule between tiles in the same row
            if sep_visible and c < cols - 1:
                sep_x = tx + tile_w + gap_x / 2
                pad = tile_h * 0.15
                box.add({
                    "type": "line",
                    "x1": sep_x,
                    "y1": ty + pad,
                    "x2": sep_x,
                    "y2": ty + tile_h - pad,
                    "stroke": sep_color,
                    "stroke_width": sep_width,
                })
