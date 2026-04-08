"""
TextCardRenderer — Renders text-card content with body text and optional bullet lists.
"""

from __future__ import annotations

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class TextCardRenderer(BaseCardRenderer):
    """Renderer for ``text-card`` type."""

    variant = None  # Uses base card tokens only

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        """Render body text and optional bullet list."""
        content = card.content if isinstance(card.content, dict) else {}
        body_text = content.get("body", "")
        bullets = content.get("bullets", [])

        y = box.y
        font_size = float(self.resolve("text-body-font-size") or 14)
        font_color = self.resolve("text-body-font-color") or "#333333"
        line_height = font_size * 1.5
        body_align = self.resolve("card-body-alignment") or "left"
        bullet_indent = float(self.resolve("card-body-bullet-indent") or 12)

        chars_per_line_full = max(1, int(box.w / (font_size * 0.6)))
        chars_per_line_indent = max(1, int((box.w - bullet_indent) / (font_size * 0.6)))

        # Body paragraph
        if body_text:
            num_lines = max(1, len(body_text) // chars_per_line_full + 1)
            body_h = num_lines * line_height
            box.add(
                {
                    "type": "text",
                    "x": box.x,
                    "y": y,
                    "w": box.w,
                    "h": body_h,
                    "text": body_text,
                    "font_size": font_size,
                    "font_color": font_color,
                    "font_weight": self.resolve("text-body-font-weight") or "normal",
                    "alignment": body_align,
                    "wrap": True,
                }
            )
            y += body_h + 8

        # Bullet list
        for bullet in bullets:
            bullet_text = f"• {bullet}"
            num_lines = max(1, len(bullet_text) // chars_per_line_indent + 1)
            bullet_h = num_lines * line_height
            box.add(
                {
                    "type": "text",
                    "x": box.x + bullet_indent,
                    "y": y,
                    "w": box.w - bullet_indent,
                    "h": bullet_h,
                    "text": bullet_text,
                    "font_size": font_size,
                    "font_color": font_color,
                    "alignment": body_align,
                    "wrap": True,
                }
            )
            y += bullet_h
