"""
SectionDividerCardRenderer — BCG/McKinsey-style chapter break.

Full-bleed coloured panel with an oversized section number (e.g. "02") on
the left and the section title (+ optional subtitle) on the right. Designed
to be used on a grid-1x1 layout to create a strong visual break between
sections of a deck — much bolder than an agenda-card highlight.

Content schema::

    type: section-divider-card
    content:
      number: "02"               # large section number (string, kept as-is)
      title: "The Capability"    # large section title
      subtitle: "Why it outlasts the process layer"   # optional
      eyebrow: "Section"         # optional small uppercase label above number

Layout: number occupies the left ~35 %% of the card; title/subtitle stack
on the right. On very narrow cards the variant degrades gracefully to a
stacked layout.
"""

from __future__ import annotations

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class SectionDividerCardRenderer(BaseCardRenderer):
    """Renderer for ``section-divider-card`` type."""

    variant = "card--section-divider"

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        content = card.content if isinstance(card.content, dict) else {}

        number   = str(content.get("number", "") or "")
        title    = str(content.get("title", "") or "")
        subtitle = str(content.get("subtitle", "") or "")
        eyebrow  = str(content.get("eyebrow", "") or "")

        # ── Token resolution ───────────────────────────────────────────
        # Background panel is supplied by the base card container (so it
        # respects `--card-background` and any per-instance override).
        # Padding is also driven by the base via `--card-padding`.

        number_size   = float(self._tok("number-font-size") or 140)
        number_color  = self._tok("number-font-color") or self.resolve("color-primary") or "#000099"
        number_weight = self._tok("number-font-weight") or "bold"

        title_size    = float(self._tok("title-font-size") or 36)
        title_color   = self._tok("title-font-color") or self.resolve("color-text-default") or "#222"
        title_weight  = self._tok("title-font-weight") or "bold"

        subtitle_size  = float(self._tok("subtitle-font-size") or 16)
        subtitle_color = self._tok("subtitle-font-color") or self.resolve("color-text-muted") or "#666"

        eyebrow_size   = float(self._tok("eyebrow-font-size") or 12)
        eyebrow_color  = self._tok("eyebrow-font-color") or number_color
        eyebrow_weight = self._tok("eyebrow-font-weight") or "bold"

        accent_visible = str(self._tok("accent-visible") or "true").lower() == "true"
        accent_color   = self._tok("accent-color") or number_color
        accent_width   = float(self._tok("accent-width") or 4)

        number_ratio = float(self._tok("number-area-ratio") or 0.35)
        gap          = float(self._tok("number-text-gap") or 32)

        # ── Accent bar (left edge) ─────────────────────────────────────
        if accent_visible and accent_width > 0:
            box.add({
                "type": "rect",
                "x": box.x, "y": box.y,
                "w": accent_width, "h": box.h,
                "fill": accent_color, "stroke": "none",
            })

        inner_x = box.x + max(accent_width, 0) + 24
        inner_y = box.y
        inner_w = box.w - (inner_x - box.x) - 24
        inner_h = box.h

        # ── Number area (left) ─────────────────────────────────────────
        if number:
            num_w = inner_w * number_ratio
            num_h = inner_h
            num_x = inner_x
            num_y = inner_y
            box.add({
                "type": "text",
                "x": num_x, "y": num_y, "w": num_w, "h": num_h,
                "text": number,
                "font_size": number_size,
                "font_color": number_color,
                "font_weight": number_weight,
                "alignment": "left",
                "vertical_align": "middle",
                "wrap": False,
            })
            text_x = num_x + num_w + gap
            text_w = inner_w - num_w - gap
        else:
            text_x = inner_x
            text_w = inner_w

        # ── Eyebrow + title + subtitle (right, vertically centered) ────
        eyebrow_h  = (eyebrow_size + 8) if eyebrow else 0
        title_h    = (title_size * 1.2) if title else 0
        subtitle_h = (subtitle_size * 1.4) if subtitle else 0
        block_h    = eyebrow_h + title_h + (8 if subtitle else 0) + subtitle_h
        cy = inner_y + (inner_h - block_h) / 2

        if eyebrow:
            box.add({
                "type": "text",
                "x": text_x, "y": cy, "w": text_w, "h": eyebrow_size + 4,
                "text": eyebrow.upper(),
                "font_size": eyebrow_size,
                "font_color": eyebrow_color,
                "font_weight": eyebrow_weight,
                "alignment": "left",
                "wrap": False,
            })
            cy += eyebrow_h

        if title:
            box.add({
                "type": "text",
                "x": text_x, "y": cy, "w": text_w, "h": title_h,
                "text": title,
                "font_size": title_size,
                "font_color": title_color,
                "font_weight": title_weight,
                "alignment": "left",
                "vertical_align": "top",
                "wrap": True,
            })
            cy += title_h + (8 if subtitle else 0)

        if subtitle:
            box.add({
                "type": "text",
                "x": text_x, "y": cy, "w": text_w, "h": subtitle_h,
                "text": subtitle,
                "font_size": subtitle_size,
                "font_color": subtitle_color,
                "alignment": "left",
                "vertical_align": "top",
                "wrap": True,
            })
