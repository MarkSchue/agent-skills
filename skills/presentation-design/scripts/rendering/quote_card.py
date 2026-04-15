"""
QuoteCardRenderer — Renders quote-card with accent bar, quote text, and attribution.
"""

from __future__ import annotations

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class QuoteCardRenderer(BaseCardRenderer):
    """Renderer for ``quote-card`` type."""

    variant = "card--quote"

    def _tok(self, name: str, default=None):
        """Resolve ``card-quote-{name}`` with fallback to ``card-{name}`` (base token)."""
        return self._resolve_tok("quote", name, default)

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        """Render quote text with left accent bar and attribution."""
        content = card.content if isinstance(card.content, dict) else {}
        quote_text = content.get("quote", "")
        attribution = content.get("attribution", "")
        role = content.get("role", "")

        accent_color = self._tok("accent-color") or "#003087"
        accent_width = float(self._tok("accent-width") or 4)
        quote_size = float(self._tok("body-font-size", 14))
        quote_color = self._tok("body-font-color") or "#333333"
        quote_style = self._tok("body-font-style") or "italic"

        y = box.y

        # Left accent bar
        bar_x = box.x
        box.add(
            {
                "type": "rect",
                "x": bar_x,
                "y": y,
                "w": accent_width,
                "h": box.h * 0.6,
                "fill": accent_color,
                "rx": 0,
            }
        )

        # Quote text (indented past the accent bar)
        text_x = bar_x + accent_width + 12
        text_w = box.w - accent_width - 12
        quote_text_align = self._tok("body-alignment") or "left"
        attribution_align = self._tok("attribution-alignment") or "left"
        box.add(
            {
                "type": "text",
                "x": text_x,
                "y": y + 4,
                "w": text_w,
                "text": f"\u201C{quote_text}\u201D",
                "font_size": quote_size,
                "font_color": quote_color,
                "font_style": quote_style,
                "alignment": quote_text_align,
                "wrap": True,
            }
        )

        # Estimate quote text height
        chars_per_line = max(1, int(text_w / (quote_size * 0.55)))
        quote_lines = max(1, len(quote_text) // chars_per_line + 1)
        y += quote_lines * (quote_size * 1.5) + 16

        # Attribution
        if attribution:
            body_size = float(self.resolve("text-body-font-size") or 14)
            box.add(
                {
                    "type": "text",
                    "x": text_x,
                    "y": y,
                    "w": text_w,
                    "text": f"\u2014 {attribution}",
                    "font_size": body_size,
                    "font_color": self.resolve("text-body-font-color"),
                    "font_weight": "bold",
                    "alignment": attribution_align,
                }
            )
            y += body_size + 4

        # Role / org
        if role:
            caption_size = float(self.resolve("text-caption-font-size") or 11)
            box.add(
                {
                    "type": "text",
                    "x": text_x,
                    "y": y,
                    "w": text_w,
                    "text": role,
                    "font_size": caption_size,
                    "font_color": self.resolve("text-caption-font-color"),
                    "alignment": attribution_align,
                }
            )
