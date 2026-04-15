"""
AgendaCardRenderer — Renders agenda-card with three-column row layout and active highlight.

Each section entry is rendered as a single row with up to three columns:
  Col 1 — number / icon / time indicator (configurable width, default ~15 %)
  Col 2 — section title  (h2-style font,  configurable width, default ~50 %)
  Col 3 — optional extra info such as duration or presenter (remaining width)

The active section is marked with a vertical accent bar on the left edge
and its number + title are rendered in the active font colour / weight.
All visual properties are controlled exclusively through CSS tokens on
the ``.card--agenda`` variant class.
"""

from __future__ import annotations

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class AgendaCardRenderer(BaseCardRenderer):
    """Renderer for ``agenda-card`` type.

    Sections are always rendered in a single vertical column.
    Each row has three logical sub-columns: number, title, info.
    The active section is highlighted with a left accent bar and bold text.
    """

    variant = "card--agenda"

    def _tok(self, name: str, default=None):
        """Resolve ``card-agenda-{name}`` with fallback to ``card-{name}`` (base token)."""
        return self._resolve_tok("agenda", name, default)

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        """Render section list as a three-column single-column layout."""
        content = card.content if isinstance(card.content, dict) else {}
        sections: list = content.get("sections", [])
        highlight: int | None = content.get("highlight")

        if not sections:
            return

        # ── Highlight bar tokens ──────────────────────────────────────────
        bar_visible_raw = self.resolve("card-agenda-highlight-bar-visible")
        bar_visible = bar_visible_raw in (True, "true", "True")
        bar_color = self.resolve("card-agenda-highlight-bar-color") or "#003087"
        bar_width = float(self.resolve("card-agenda-highlight-bar-width") or 3)
        bar_gap = float(self.resolve("card-agenda-highlight-bar-gap") or 8)

        # ── Column proportions (percent of usable row width) ─────────────
        col1_pct = float(self.resolve("card-agenda-col1-width-pct") or 15) / 100
        col2_pct = float(self.resolve("card-agenda-col2-width-pct") or 50) / 100
        # col3 receives the remainder

        # ── Per-column text alignment ─────────────────────────────────────
        col1_align = self.resolve("card-agenda-col1-alignment") or "center"
        col2_align = self.resolve("card-agenda-col2-alignment") or "left"
        col3_align = self.resolve("card-agenda-col3-alignment") or "left"

        # ── Row geometry ───────────────────────────────────────────────────────
        entry_size = float(self._tok("heading-font-size", 14))
        entry_spacing = float(self.resolve("card-agenda-entry-spacing") or 12)
        row_height_token = self.resolve("card-agenda-row-height")
        row_h = None

        if isinstance(row_height_token, (int, float)) and row_height_token > 0:
            row_h = float(row_height_token)
            # Ensure row_h is at least entry_size + a minimal gap.
            if row_h < entry_size + 4:
                row_h = entry_size + 4

        if row_h is None:
            row_h = entry_size + entry_spacing
        else:
            entry_spacing = max(0.0, row_h - entry_size)

        # Left indentation = bar_width + gap (kept constant for all rows so columns align)
        bar_reserved = bar_width + bar_gap

        usable_w = box.w - bar_reserved
        col1_w = usable_w * col1_pct
        col2_w = usable_w * col2_pct
        col3_w = usable_w - col1_w - col2_w

        col1_x = box.x + bar_reserved
        col2_x = col1_x + col1_w
        col3_x = col2_x + col2_w

        # ── Number / indicator column tokens ─────────────────────────────
        number_size = float(self._tok("number-font-size") or entry_size)
        number_color_inactive = self._tok("number-font-color") or "#888888"
        number_weight_inactive = str(self._tok("number-font-weight") or "400")
        number_style_inactive = self._tok("number-font-style") or "normal"

        # ── Title column tokens (inactive / active) ───────────────────────
        # col2 uses heading-specific tokens (h2-style); inactive-color is a
        # secondary fallback so both naming conventions work.
        entry_color_inactive = (
            self._tok("heading-font-color")
            or self._tok("inactive-color")
            or "#888888"
        )
        entry_weight_inactive = str(
            self._tok("heading-font-weight")
            or self._tok("inactive-font-weight")
            or "600"
        )
        entry_style_inactive = self._tok("heading-font-style") or "normal"

        active_number_color = self._tok("active-number-color") or "#003087"
        active_title_color = self._tok("active-heading-color") or "#003087"
        active_info_color = self._tok("active-body-color") or "#374151"
        active_weight = str(self._tok("active-font-weight") or "700")
        active_style = self._tok("active-font-style") or "normal"

        # ── Info column tokens ────────────────────────────────────────────
        info_size = float(self._tok("body-font-size", 12))
        info_color = self._tok("body-font-color") or "#888888"
        info_weight = str(self._tok("body-font-weight") or "400")
        info_style = self._tok("body-font-style") or "normal"

        # ── Row separator tokens ──────────────────────────────────────────
        sep_visible_raw = self.resolve("card-agenda-separator-visible")
        sep_visible = sep_visible_raw in (True, "true", "True")
        sep_color = self.resolve("card-agenda-separator-color") or "#E0E0E0"
        sep_width = float(self.resolve("card-agenda-separator-width") or 1)
        sep_inset = float(self.resolve("card-agenda-separator-inset") or 0)

        # ── Overflow guard — scale row geometry to fit box.h ─────────────
        # When the agenda-card is placed in a small grid cell the token-based
        # row_h can exceed the available body area.  Compress proportionally;
        # if even the minimum readable size won't fit, clip the section list.
        if len(sections) > 0 and box.h > 0:
            total_rows_h = len(sections) * row_h
            if total_rows_h > box.h:
                _min_font = 8.0
                scaled_row_h = box.h / len(sections)
                if scaled_row_h >= _min_font + 2:
                    _scale = scaled_row_h / row_h
                    entry_size = max(_min_font, entry_size * _scale)
                    number_size = max(_min_font, number_size * _scale)
                    info_size = max(6.0, info_size * _scale)
                    row_h = scaled_row_h
                else:
                    # Minimum font floor hit — show only as many rows as fit
                    row_h = _min_font + 2
                    sections = sections[: max(1, int(box.h / row_h))]

        # ── Render each row ───────────────────────────────────────────────
        for i, section in enumerate(sections):
            # Normalize: sections may be plain strings or dicts
            if isinstance(section, dict):
                number_text = str(section.get("number", i + 1))
                title_text = str(section.get("title", ""))
                info_text = str(section.get("info", ""))
            else:
                number_text = str(i + 1)
                title_text = str(section)
                info_text = ""

            is_active = (highlight is not None and i == highlight)
            y = box.y + i * row_h

            # Active accent bar — vertical rectangle on the left edge
            # Height spans the full row slot (entry_size + entry_spacing) so
            # the bar always matches row height regardless of spacing token value.
            if is_active and bar_visible:
                box.add(
                    {
                        "type": "rect",
                        "x": box.x,
                        "y": y,
                        "w": bar_width,
                        "h": row_h,
                        "fill": bar_color,
                        "stroke": bar_color,
                        "stroke_width": 0,
                        "rx": 0,
                    }
                )

            # Col 1 — number / indicator (text box spans full row height, content vertically centred)
            n_color = active_number_color if is_active else number_color_inactive
            n_weight = active_weight if is_active else number_weight_inactive
            n_style = active_style if is_active else number_style_inactive
            box.add(
                {
                    "type": "text",
                    "x": col1_x,
                    "y": y,
                    "w": col1_w,
                    "h": row_h,
                    "text": number_text,
                    "font_size": number_size,
                    "font_color": n_color,
                    "font_weight": n_weight,
                    "font_style": n_style,
                    "alignment": col1_align,
                    "vertical_align": "middle",
                    "wrap": True,
                }
            )

            # Col 2 — section title (h2-style, full row height so text wraps inside)
            t_color = active_title_color if is_active else entry_color_inactive
            t_weight = active_weight if is_active else entry_weight_inactive
            t_style = active_style if is_active else entry_style_inactive
            box.add(
                {
                    "type": "text",
                    "x": col2_x,
                    "y": y,
                    "w": col2_w,
                    "h": row_h,
                    "text": title_text,
                    "font_size": entry_size,
                    "font_color": t_color,
                    "font_weight": t_weight,
                    "font_style": t_style,
                    "alignment": col2_align,
                    "vertical_align": "middle",
                    "wrap": True,
                }
            )

            # Row separator — drawn exactly at the row boundary (y + row_h)
            if sep_visible and i < len(sections) - 1:
                sep_y = y + row_h
                box.add(
                    {
                        "type": "line",
                        "x1": box.x + sep_inset,
                        "y1": sep_y,
                        "x2": box.x + box.w - sep_inset,
                        "y2": sep_y,
                        "stroke": sep_color,
                        "stroke_width": sep_width,
                    }
                )

            # Col 3 — optional info (text-body style, allows 2 lines)
            if info_text and col3_w > 0:
                box.add(
                    {
                        "type": "text",
                        "x": col3_x,
                        "y": y,
                        "w": col3_w,
                        "h": entry_size * 2,  # allow two lines
                        "text": info_text,
                        "font_size": info_size,
                        "font_color": active_info_color if is_active else info_color,
                        "font_weight": info_weight,
                        "font_style": info_style,
                        "alignment": col3_align,
                        "vertical_align": "middle",
                        "wrap": True,
                    }
                )
