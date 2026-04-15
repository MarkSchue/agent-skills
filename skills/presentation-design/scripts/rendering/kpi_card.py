"""
KpiCardRenderer — Renders kpi-card with large metric value, trend indicator, and label.
"""

from __future__ import annotations

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class KpiCardRenderer(BaseCardRenderer):
    """Renderer for ``kpi-card`` type."""

    variant = "card--kpi"

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        """Render metric value, trend arrow, and supporting label."""
        content = card.content if isinstance(card.content, dict) else {}
        value = content.get("value", "")
        trend = content.get("trend", "neutral")
        label = content.get("label", "")
        comparison = content.get("comparison", "")

        value_size = float(self.resolve("card-kpi-value-font-size") or 48)
        value_color = self.resolve("card-kpi-value-font-color") or "#1A1A1A"
        value_align = self.resolve("card-kpi-value-alignment") or "center"
        value_valign = self.resolve("card-kpi-value-vertical-align") or "middle"
        trend_font_size = float(self.resolve("card-kpi-trend-font-size") or 14)
        comparison_font_size = float(self.resolve("card-kpi-comparison-font-size") or 12)
        trend_align = self.resolve("card-kpi-trend-alignment") or "center"
        label_align = self.resolve("card-kpi-label-alignment") or "center"

        # Compute vertical start position based on value-vertical-align token
        if value_valign == "top":
            y = box.y
        elif value_valign == "bottom":
            y = box.y + box.h - value_size - 8
        else:  # middle (default)
            y = box.y + (box.h - value_size) * 0.35

        # Large metric value
        box.add(
            {
                "type": "text",
                "x": box.x,
                "y": y,
                "w": box.w,
                "text": value,
                "font_size": value_size,
                "font_color": value_color,
                "font_weight": "bold",
                "alignment": value_align,
            }
        )
        y += value_size + 8

        # Trend indicator
        if trend != "neutral":
            arrow = "↑" if trend == "up" else "↓"
            trend_color = (
                self.resolve("card-kpi-trend-color-up")
                if trend == "up"
                else self.resolve("card-kpi-trend-color-down")
            ) or ("#2E7D32" if trend == "up" else "#C62828")
            trend_text = f"{arrow} {comparison}" if comparison else arrow
            box.add(
                {
                    "type": "text",
                    "x": box.x,
                    "y": y,
                    "w": box.w,
                    "text": trend_text,
                    "font_size": trend_font_size,
                    "font_color": trend_color,
                    "alignment": trend_align,
                }
            )
            y += trend_font_size + 8
        elif comparison:
            box.add(
                {
                    "type": "text",
                    "x": box.x,
                    "y": y,
                    "w": box.w,
                    "text": comparison,
                    "font_size": comparison_font_size,
                    "font_color": self.resolve("card-kpi-trend-color-neutral") or "#888888",
                    "alignment": trend_align,
                }
            )
            y += comparison_font_size + 8

        # Supporting label
        if label:
            label_size = float(self._resolve_tok("kpi", "label-font-size", 11))
            box.add(
                {
                    "type": "text",
                    "x": box.x,
                    "y": y,
                    "w": box.w,
                    "text": label,
                    "font_size": label_size,
                    "font_color": self._resolve_tok("kpi", "label-font-color", "#888888"),
                    "alignment": label_align,
                }
            )
