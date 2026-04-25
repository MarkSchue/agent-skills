"""
CalloutCardRenderer — Renders callout-card for "key insight" / "key takeaway"
boxes commonly used in consulting decks (BCG, McKinsey style).

Visual: thick coloured left accent bar + small uppercase eyebrow label
("KEY INSIGHT"), then large readable body text. Designed to make a single
sentence land hard.
"""

from __future__ import annotations

from scripts.models.deck import CardModel
from scripts.parsing.inline_markdown import text_and_runs
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class CalloutCardRenderer(BaseCardRenderer):
    """Renderer for ``callout-card`` type."""

    variant = "card--callout"

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        content = card.content if isinstance(card.content, dict) else {}
        eyebrow = str(content.get("eyebrow", "") or "")
        body = str(content.get("body", "") or "")

        accent_color = self._tok("accent-color") or "#000099"
        accent_width = float(self._tok("accent-width") or 6)
        accent_gap = float(self._tok("accent-gap") or 16)

        eyebrow_size = float(self._tok("eyebrow-font-size") or 11)
        eyebrow_color = self._tok("eyebrow-font-color") or accent_color
        eyebrow_weight = self._tok("eyebrow-font-weight") or "bold"
        eyebrow_letter_spacing = float(self._tok("eyebrow-letter-spacing") or 1)

        body_size = float(self._tok("body-font-size") or 22)
        body_color = self._tok("body-font-color") or self.resolve("text-default-color") or "#262626"
        body_weight = self._tok("body-font-weight") or "600"
        body_align = self._tok("body-alignment") or "left"

        # Quote mark — large bold opening guillemet rendered before the body.
        quote_char_size = float(self._tok("quote-char-size") or body_size * 2.5)
        quote_char = self._tok("quote-char") or "\u201C"  # "

        text_x = box.x + accent_width + accent_gap
        text_w = box.w - accent_width - accent_gap
        y = box.y

        # Measure content height so the accent bar matches actual text height
        content_h = 0.0
        if eyebrow:
            content_h += eyebrow_size + 2 + float(self._tok("eyebrow-margin-bottom") or 12)
        if body:
            line_h = body_size * 1.35
            content_h += quote_char_size * 0.8 + 4  # opening quote
            content_h += max(line_h * 2, body_size + 4)  # body text

        bar_h = max(content_h, body_size * 1.35)

        # Left accent bar — height matched to content, not full card body
        box.add({
            "type": "rect",
            "x": box.x,
            "y": box.y,
            "w": accent_width,
            "h": bar_h,
            "fill": accent_color,
            "rx": 0,
        })

        if eyebrow:
            # Approximate letter spacing by inserting hair spaces between chars
            display_eyebrow = eyebrow.upper()
            if eyebrow_letter_spacing > 0:
                display_eyebrow = " ".join(display_eyebrow)
            box.add({
                "type": "text",
                "x": text_x,
                "y": y,
                "w": text_w,
                "h": eyebrow_size + 2,
                "text": display_eyebrow,
                "font_size": eyebrow_size,
                "font_color": eyebrow_color,
                "font_weight": eyebrow_weight,
                "alignment": body_align,
            })
            y += eyebrow_size + float(self._tok("eyebrow-margin-bottom") or 12)

        if body:
            # Large bold opening quote character
            box.add({
                "type": "text",
                "x": text_x,
                "y": y,
                "w": text_w,
                "h": quote_char_size * 0.8 + 4,
                "text": quote_char,
                "font_size": quote_char_size,
                "font_color": accent_color,
                "font_weight": "bold",
                "alignment": "left",
            })
            y += quote_char_size * 0.6  # overlap slightly so quote feels attached to text

            line_h = body_size * 1.35
            # Generous height — let exporter wrap
            avail_h = max(line_h, box.y + box.h - y)
            box.add({
                "type": "text",
                "x": text_x,
                "y": y,
                "w": text_w,
                "h": avail_h,
                **text_and_runs(body),
                "font_size": body_size,
                "font_color": body_color,
                "font_weight": body_weight,
                "alignment": body_align,
                "wrap": True,
            })
