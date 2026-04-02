"""
AgendaCardRenderer — Renders agenda-card with dynamic column layout and active highlight.
"""

from __future__ import annotations

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class AgendaCardRenderer(BaseCardRenderer):
    """Renderer for ``agenda-card`` type.

    Supports dynamic column layout:
    - 1–4 sections → 1 column
    - 5–8 sections → 2 columns
    - 9+  sections → 3 columns

    The column count can be overridden via ``content.columns``.
    """

    variant = "card--agenda"

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        """Render section list with optional highlight."""
        content = card.content if isinstance(card.content, dict) else {}
        sections: list[str] = content.get("sections", [])
        highlight: int | None = content.get("highlight")
        forced_columns: int | None = content.get("columns")

        if not sections:
            return

        # Determine column count
        n = len(sections)
        if forced_columns:
            cols = int(forced_columns)
        elif n <= 4:
            cols = 1
        elif n <= 8:
            cols = 2
        else:
            cols = 3

        item_size = float(self.resolve("card-agenda-item-font-size") or 14)
        item_color = self.resolve("card-agenda-item-font-color") or "#333333"
        hl_color = self.resolve("card-agenda-highlight-font-color") or "#003087"
        hl_weight = self.resolve("card-agenda-highlight-font-weight") or "bold"
        number_color = self.resolve("card-agenda-number-font-color") or "#888888"
        col_gap = float(self.resolve("card-agenda-column-gap") or 20)

        col_width = (box.w - (cols - 1) * col_gap) / cols
        line_height = item_size * 1.8

        # Distribute items across columns (fill column-first)
        rows_per_col = (n + cols - 1) // cols

        for i, section_title in enumerate(sections):
            col_idx = i // rows_per_col
            row_idx = i % rows_per_col

            x = box.x + col_idx * (col_width + col_gap)
            y = box.y + row_idx * line_height

            is_active = (highlight is not None and i == highlight)
            color = hl_color if is_active else item_color
            weight = hl_weight if is_active else "normal"

            # Number
            box.add(
                {
                    "type": "text",
                    "x": x,
                    "y": y,
                    "text": f"{i + 1}.",
                    "font_size": item_size,
                    "font_color": number_color,
                    "font_weight": weight,
                }
            )

            # Section title
            box.add(
                {
                    "type": "text",
                    "x": x + item_size * 2,
                    "y": y,
                    "w": col_width - item_size * 2,
                    "text": section_title,
                    "font_size": item_size,
                    "font_color": color,
                    "font_weight": weight,
                }
            )
