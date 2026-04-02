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

        y = box.y + (box.h - value_size) * 0.35  # vertically center-ish

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
                "alignment": "center",
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
                    "font_size": 14,
                    "font_color": trend_color,
                    "alignment": "center",
                }
            )
            y += 22
        elif comparison:
            box.add(
                {
                    "type": "text",
                    "x": box.x,
                    "y": y,
                    "w": box.w,
                    "text": comparison,
                    "font_size": 12,
                    "font_color": "#888888",
                    "alignment": "center",
                }
            )
            y += 20

        # Supporting label
        if label:
            label_size = float(self.resolve("text-caption-font-size") or 11)
            box.add(
                {
                    "type": "text",
                    "x": box.x,
                    "y": y,
                    "w": box.w,
                    "text": label,
                    "font_size": label_size,
                    "font_color": self.resolve("text-caption-font-color") or "#888888",
                    "alignment": "center",
                }
            )
