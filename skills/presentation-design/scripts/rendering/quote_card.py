"""
QuoteCardRenderer — Renders quote-card with accent bar, quote text, and attribution.
"""

from __future__ import annotations

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class QuoteCardRenderer(BaseCardRenderer):
    """Renderer for ``quote-card`` type."""

    variant = "card--quote"

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        """Render quote text with left accent bar and attribution, vertically centred."""
        content = card.content if isinstance(card.content, dict) else {}
        quote_text = content.get("quote", "")
        attribution = content.get("attribution", "")
        role = content.get("role", "")

        accent_color = self._tok("accent-color") or "#003087"
        accent_width = float(self._tok("accent-width") or 4)
        quote_size = float(self._tok("body-font-size", 14))
        quote_color = self._tok("body-font-color")
        quote_style = self._tok("body-font-style") or "italic"
        body_size = float(self._tok("attribution-font-size", 14))
        caption_size = float(self._tok("role-font-size", 11))

        text_x = box.x + accent_width + 12
        text_w = box.w - accent_width - 12
        quote_text_align = self._tok("body-alignment") or "left"
        attribution_align = self._tok("attribution-alignment") or "left"

        # Pre-compute total content height for vertical centering
        chars_per_line = max(1, int(text_w / (quote_size * 0.55)))
        quote_lines = max(1, len(quote_text) // chars_per_line + 1)
        content_h = quote_lines * (quote_size * 1.5) + 16
        if attribution:
            content_h += body_size + 4
        if role:
            content_h += caption_size

        # Vertically center the content block within the body box
        y = box.y + max(0, (box.h - content_h) / 2)

        # Left accent bar -- height matches the content block
        bar_x = box.x
        box.add(
            {
                "type": "rect",
                "x": bar_x,
                "y": y,
                "w": accent_width,
                "h": content_h,
                "fill": accent_color,
                "rx": 0,
            }
        )

        # Quote text (indented past the accent bar)
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

        y += quote_lines * (quote_size * 1.5) + 16

        # Attribution
        if attribution:
            box.add(
                {
                    "type": "text",
                    "x": text_x,
                    "y": y,
                    "w": text_w,
                    "text": f"\u2014 {attribution}",
                    "font_size": body_size,
                    "font_color": self._tok("attribution-font-color"),
                    "font_weight": "bold",
                    "alignment": attribution_align,
                }
            )
            y += body_size + 4

        # Role / org
        if role:
            box.add(
                {
                    "type": "text",
                    "x": text_x,
                    "y": y,
                    "w": text_w,
                    "text": role,
                    "font_size": caption_size,
                    "font_color": self._tok("role-font-color"),
                    "alignment": attribution_align,
                }
            )