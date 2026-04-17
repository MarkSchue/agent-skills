"""
TextCardRenderer — Renders text-card content with body text and optional bullet lists.
"""

from __future__ import annotations

from scripts.models.deck import CardModel
from scripts.parsing.inline_markdown import text_and_runs, strip_inline
from scripts.rendering.base_card import BaseCardRenderer, RenderBox

# Maps CSS token value → bullet marker character
_BULLET_CHAR: dict[str, str] = {
    "disc":   "•",
    "circle": "○",
    "square": "■",
    "dash":   "–",
    "arrow":  "›",
    "none":   "",
}


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
        font_color = self.resolve("text-body-font-color")
        line_height = font_size * 1.5
        body_align = self.resolve("card-body-alignment") or "left"
        bullet_indent = float(self.resolve("card-body-bullet-indent") or 12)
        bullet_gap = float(self.resolve("card-bullet-gap") or 8)
        bullet_spacing = float(self.resolve("card-bullet-spacing") or 4)

        # Bullet style tokens
        bullet_style_raw = self.resolve("card-bullet-style") or "disc"
        bullet_char = _BULLET_CHAR.get(str(bullet_style_raw).strip().lower(), "•")
        bullet_color_raw = self.resolve("card-bullet-color")
        bullet_color = str(bullet_color_raw) if bullet_color_raw else font_color
        try:
            bullet_size_raw = self.resolve("card-bullet-size")
            bullet_size = float(bullet_size_raw) if bullet_size_raw and float(bullet_size_raw) > 0 else font_size
        except (ValueError, TypeError):
            bullet_size = font_size

        chars_per_line_full = max(1, int(box.w / (font_size * 0.6)))
        chars_per_line_indent = max(1, int((box.w - bullet_indent - bullet_gap) / (font_size * 0.6)))

        # Body paragraph
        if body_text:
            plain = strip_inline(str(body_text))
            num_lines = max(1, len(plain) // chars_per_line_full + 1)
            body_h = num_lines * line_height
            box.add(
                {
                    "type": "text",
                    "x": box.x,
                    "y": y,
                    "w": box.w,
                    "h": body_h,
                    **text_and_runs(str(body_text)),
                    "font_size": font_size,
                    "font_color": font_color,
                    "font_weight": self.resolve("text-body-font-weight") or "normal",
                    "alignment": body_align,
                    "wrap": True,
                }
            )
            y += body_h + 8

        # Bullet list — emit as a single "bullet_list" element so exporters can use
        # native shape types (PPTX text box with buChar paragraphs, draw.io HTML list)
        if bullets:
            items = []
            total_h = 0.0
            for bullet in bullets:
                bullet_str = str(bullet)
                plain_bullet = strip_inline(bullet_str)
                num_lines = max(1, len(plain_bullet) // chars_per_line_indent + 1)
                bullet_h = num_lines * line_height + bullet_spacing
                items.append({**text_and_runs(bullet_str), "h": bullet_h})
                total_h += bullet_h

            box.add(
                {
                    "type": "bullet_list",
                    "x": box.x,
                    "y": y,
                    "w": box.w,
                    "h": total_h,
                    "items": items,
                    "font_size": font_size,
                    "font_color": font_color,
                    "font_weight": self.resolve("text-body-font-weight") or "normal",
                    "alignment": body_align,
                    "bullet_char": bullet_char,
                    "bullet_color": bullet_color,
                    "bullet_size": bullet_size,
                    "bullet_indent": bullet_indent,
                    "bullet_gap": bullet_gap,
                    "bullet_spacing": bullet_spacing,
                    "line_height": line_height,
                    "wrap": True,
                }
            )
            y += total_h

