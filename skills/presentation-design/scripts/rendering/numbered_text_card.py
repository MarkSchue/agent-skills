"""
NumberedTextCardRenderer — Three-column list card with optional badge, icon, and
active-row highlight.

Each entry is a single row with up to three columns rendered side by side:

  Col 1 — indicator (number / icon / plain text) with optional badge shape:
           circle, square, rectangle, or none (no background).
           Hidden entirely when no row supplies a col1 value.
  Col 2 — heading (h2-style, may wrap to multiple lines).
  Col 3 — body text (secondary, right side, may wrap to multiple lines).
           Hidden entirely when no row supplies a body value.

The active row is highlighted with a left accent bar.
Row height is dynamic — computed from the tallest column's estimated content.

All visual properties are controlled by CSS tokens on ``.card--numbered-text``.
"""

from __future__ import annotations

from scripts.models.deck import CardModel
from scripts.parsing.inline_markdown import text_and_runs
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class NumberedTextCardRenderer(BaseCardRenderer):
    """Renderer for ``numbered_text_card`` type."""

    variant = "card--numbered-text"

    # ──────────────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────────────

    @staticmethod
    def _estimate_line_count(text: str, max_chars: int) -> int:
        """Word-wrap estimate with improved character-width factor."""
        if max_chars <= 0:
            return max(1, len(text))
        words = text.split()
        if not words:
            return 1
        line_count = 1
        current_len = 0
        for word in words:
            if current_len == 0:
                current_len = len(word)
            elif current_len + 1 + len(word) <= max_chars:
                current_len += 1 + len(word)
            else:
                line_count += 1
                current_len = len(word)
        return line_count

    @staticmethod
    def _normalize_row(entry: object, idx: int) -> dict[str, str]:
        if isinstance(entry, dict):
            return {
                "col1": str(entry.get("col1", "")),
                "heading": str(entry.get("heading", "")),
                "body": str(entry.get("body", "")),
            }
        return {"col1": str(idx + 1), "heading": str(entry), "body": ""}

    # ──────────────────────────────────────────────────────────────────────
    # Rendering
    # ──────────────────────────────────────────────────────────────────────

    def render_body(self, card: CardModel, box: RenderBox) -> None:  # noqa: C901
        content = card.content if isinstance(card.content, dict) else {}
        raw_rows: list = content.get("rows", [])
        highlight: int | None = content.get("highlight")

        if not raw_rows:
            return

        rows = [self._normalize_row(entry, i) for i, entry in enumerate(raw_rows)]

        # Determine which columns are present
        has_col1 = any(r["col1"] for r in rows)
        has_col3 = any(r["body"] for r in rows)

        # ── Highlight bar ────────────────────────────────────────────────
        bar_visible_raw = self.resolve("card-numbered-text-highlight-bar-visible")
        bar_visible = bar_visible_raw in (True, "true", "True")
        bar_color = self.resolve("card-numbered-text-highlight-bar-color") or "#3B82F6"
        bar_width = float(self.resolve("card-numbered-text-highlight-bar-width") or 3)
        bar_gap = float(self.resolve("card-numbered-text-highlight-bar-gap") or 8)

        # ── Column proportions ───────────────────────────────────────────
        col1_pct = float(self.resolve("card-numbered-text-col1-width-pct") or 15) / 100
        col2_pct = float(self.resolve("card-numbered-text-col2-width-pct") or 55) / 100
        # col3 receives the remainder

        # ── Per-column alignments ────────────────────────────────────────
        col1_align = self.resolve("card-numbered-text-col1-alignment") or "center"
        col1_gap = float(self.resolve("card-numbered-text-col1-gap") or 8)
        col2_align = self.resolve("card-numbered-text-col2-alignment") or "left"
        col3_align = self.resolve("card-numbered-text-col3-alignment") or "left"

        # ── Row vertical alignment ───────────────────────────────────────
        row_valign = self.resolve("card-numbered-text-row-vertical-alignment") or "middle"
        row_min_h = float(self.resolve("card-numbered-text-row-min-height") or 0)
        row_padding = float(self.resolve("card-numbered-text-row-padding") or 6)

        # ── Heading (col 2) tokens ───────────────────────────────────────
        h_size = float(self._resolve_tok("numbered-text", "heading-font-size",  14))
        h_color = self._resolve_tok("numbered-text", "heading-font-color")
        h_weight = str(self._resolve_tok("numbered-text", "heading-font-weight", "600"))
        h_style = self._resolve_tok("numbered-text", "heading-font-style",        "normal")
        h_lh = h_size * float(self._resolve_tok("numbered-text", "heading-line-height", 1.3))

        # ── Body (col 3) tokens ──────────────────────────────────────────
        b_size = float(self._resolve_tok("numbered-text", "body-font-size",      12))
        b_color = self._resolve_tok("numbered-text", "body-font-color")
        b_weight = str(self._resolve_tok("numbered-text", "body-font-weight",    "400"))
        b_style = self._resolve_tok("numbered-text", "body-font-style",           "normal")
        b_lh = b_size * float(self._resolve_tok("numbered-text", "body-line-height", 1.3))

        # Gap between heading and body inside same row (when col2 and col3 share the row)
        hb_gap = float(self.resolve("card-numbered-text-heading-body-gap") or 4)

        # ── Col 1 tokens ─────────────────────────────────────────────────
        col1_size = float(self.resolve("card-numbered-text-col1-font-size") or h_size)
        col1_weight = str(self.resolve("card-numbered-text-col1-font-weight") or "700")
        col1_style = self.resolve("card-numbered-text-col1-font-style") or "normal"
        col1_font_family = self.resolve("card-numbered-text-col1-font-family") or ""
        # Badge
        badge_shape = str(
            self.resolve("card-numbered-text-badge-shape") or "circle"
        ).lower()
        badge_color = self.resolve("card-numbered-text-badge-color") or "#3B82F6"
        badge_size = float(self.resolve("card-numbered-text-badge-size") or 28)
        badge_on_color = self.resolve("card-numbered-text-badge-on-color") or "#FFFFFF"
        badge_pad_x = float(self.resolve("card-numbered-text-badge-padding-x") or 8)

        # ── Active state tokens ──────────────────────────────────────────
        active_col1_font_color = (
            self.resolve("card-numbered-text-active-col1-font-color") or badge_on_color
        )
        active_badge_color = (
            self.resolve("card-numbered-text-active-badge-color") or badge_color
        )
        active_h_color = (
            self.resolve("card-numbered-text-active-heading-font-color") or "#1A1A2E"
        )
        active_h_weight = str(
            self.resolve("card-numbered-text-active-heading-font-weight") or "700"
        )
        active_b_color = (
            self.resolve("card-numbered-text-active-body-font-color") or "#374151"
        )
        active_font_style = (
            self.resolve("card-numbered-text-active-font-style") or "normal"
        )

        # ── Row separator ────────────────────────────────────────────────
        sep_visible_raw = self.resolve("card-numbered-text-separator-visible")
        sep_visible = sep_visible_raw in (True, "true", "True")
        sep_color = self.resolve("card-numbered-text-separator-color") or "#E5E7EB"
        sep_width = float(self.resolve("card-numbered-text-separator-width") or 1)
        sep_inset = float(self.resolve("card-numbered-text-separator-inset") or 0)

        # ── Outer gap ────────────────────────────────────────────────────
        gap_top = float(self._resolve_tok("numbered-text", "gap-top", 0))
        gap_bottom = float(self._resolve_tok("numbered-text", "gap-bottom", 0))

        # ── Column geometry ───────────────────────────────────────────────
        # The bar area is always reserved when a highlight index is provided
        # so that columns align uniformly across all rows.
        bar_reserved = (bar_width + bar_gap) if highlight is not None else 0
        usable_w = box.w - bar_reserved

        col1_w = (usable_w * col1_pct) if has_col1 else 0
        # For rectangle badges auto-expand col1_w to fit the longest text single-line
        if has_col1 and badge_shape == "rectangle":
            max_text_len = max((len(r["col1"]) for r in rows if r["col1"]), default=0)
            min_rect_w = max_text_len * col1_size * 0.65 + 2 * badge_pad_x + 2
            col1_w = max(col1_w, min_rect_w)
        col3_w = (usable_w * (1.0 - col1_pct - col2_pct)) if has_col3 else 0
        if has_col1:
            col2_w = max(0.0, usable_w - col1_w - col3_w - col1_gap)
        else:
            col2_w = max(0.0, usable_w - col3_w)

        col1_x = box.x + bar_reserved
        col2_x = col1_x + col1_w + (col1_gap if has_col1 else 0)
        col3_x = col2_x + col2_w

        # ── Estimate row heights ─────────────────────────────────────────
        heading_chars = max(1, int(col2_w / (h_size * 0.48))) if col2_w > 0 else 1
        body_chars = max(1, int(col3_w / (b_size * 0.48))) if col3_w > 0 else 1

        def _row_content_h(row: dict[str, str]) -> float:
            h_lines = (
                self._estimate_line_count(row["heading"], heading_chars)
                if row["heading"]
                else 0
            )
            b_lines = (
                self._estimate_line_count(row["body"], body_chars)
                if (row["body"] and has_col3)
                else 0
            )
            # Col2 and col3 are side-by-side — row height driven by the taller one.
            # Col2 height: heading lines
            col2_content = h_lines * h_lh
            # Col3 height: body lines
            col3_content = b_lines * b_lh
            return max(col2_content, col3_content, badge_size if has_col1 else 0)

        row_heights = [
            max(row_min_h, _row_content_h(r) + 2 * row_padding) for r in rows
        ]

        # Equalise row heights so badges align across all rows
        if row_heights:
            max_row_h = max(row_heights)
            row_heights = [max_row_h] * len(row_heights)

        # Proportional scale-down if total exceeds available height
        avail_h = box.h - gap_top - gap_bottom
        total_h = sum(row_heights)
        if total_h > avail_h > 0:
            scale = avail_h / total_h
            row_heights = [rh * scale for rh in row_heights]

        # ── Render rows ───────────────────────────────────────────────────
        y_cursor = box.y + gap_top

        for i, row in enumerate(rows):
            row_h = row_heights[i]
            is_active = (highlight is not None and i == highlight)
            y = y_cursor

            # Recompute line counts for this row
            h_lines = (
                self._estimate_line_count(row["heading"], heading_chars)
                if row["heading"]
                else 0
            )
            b_lines = (
                self._estimate_line_count(row["body"], body_chars)
                if (row["body"] and has_col3)
                else 0
            )

            # Let the renderer handle vertical centering natively so
            # badge and text stay aligned regardless of line-count estimation.
            col2_y = y
            col3_y = y

            # ── Highlight bar ────────────────────────────────────────────
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

            # ── Col 1 — indicator / badge ────────────────────────────────
            if has_col1 and row["col1"]:
                eff_badge_color = active_badge_color if is_active else badge_color
                eff_col1_color = active_col1_font_color if is_active else badge_on_color
                badge_cx = col1_x + col1_w / 2
                badge_cy = y + row_h / 2

                if badge_shape == "circle":
                    bx = badge_cx - badge_size / 2
                    by = badge_cy - badge_size / 2
                    box.add(
                        {
                            "type": "ellipse",
                            "x": bx,
                            "y": by,
                            "w": badge_size,
                            "h": badge_size,
                            "fill": eff_badge_color,
                            "stroke": "none",
                            "stroke_width": 0,
                        }
                    )
                    box.add(
                        {
                            "type": "text",
                            "x": bx,
                            "y": by,
                            "w": badge_size,
                            "h": badge_size,
                            "text": row["col1"],
                            "font_size": col1_size,
                            "font_color": eff_col1_color,
                            "font_weight": col1_weight,
                            "font_style": col1_style,
                            "alignment": "center",
                            "vertical_align": "middle",
                            "wrap": False,
                            **({"font_family": col1_font_family} if col1_font_family else {}),
                        }
                    )

                elif badge_shape == "square":
                    bx = badge_cx - badge_size / 2
                    by = badge_cy - badge_size / 2
                    box.add(
                        {
                            "type": "rect",
                            "x": bx,
                            "y": by,
                            "w": badge_size,
                            "h": badge_size,
                            "fill": eff_badge_color,
                            "stroke": "none",
                            "stroke_width": 0,
                            "rx": 0,
                        }
                    )
                    box.add(
                        {
                            "type": "text",
                            "x": bx,
                            "y": by,
                            "w": badge_size,
                            "h": badge_size,
                            "text": row["col1"],
                            "font_size": col1_size,
                            "font_color": eff_col1_color,
                            "font_weight": col1_weight,
                            "font_style": col1_style,
                            "alignment": "center",
                            "vertical_align": "middle",
                            "wrap": False,
                            **({"font_family": col1_font_family} if col1_font_family else {}),
                        }
                    )

                elif badge_shape == "rectangle":
                    rect_h = min(badge_size, max(0.0, row_h - 2 * row_padding))
                    rect_w = max(0.0, col1_w - 2)  # full auto-expanded col1 width
                    bx = col1_x + 1
                    by = badge_cy - rect_h / 2
                    box.add(
                        {
                            "type": "rect",
                            "x": bx,
                            "y": by,
                            "w": rect_w,
                            "h": rect_h,
                            "fill": eff_badge_color,
                            "stroke": "none",
                            "stroke_width": 0,
                            "rx": 0,
                        }
                    )
                    box.add(
                        {
                            "type": "text",
                            "x": bx + badge_pad_x,
                            "y": by,
                            "w": max(1.0, rect_w - 2 * badge_pad_x),
                            "h": rect_h,
                            "text": row["col1"],
                            "font_size": col1_size,
                            "font_color": eff_col1_color,
                            "font_weight": col1_weight,
                            "font_style": col1_style,
                            "alignment": "center",
                            "vertical_align": "middle",
                            "wrap": False,
                            **({"font_family": col1_font_family} if col1_font_family else {}),
                        }
                    )

                else:  # badge_shape == "none" — plain text, no background
                    plain_col1_color = (
                        active_col1_font_color
                        if is_active
                        else (
                            self.resolve("card-numbered-text-col1-font-color") or h_color
                        )
                    )
                    box.add(
                        {
                            "type": "text",
                            "x": col1_x,
                            "y": y,
                            "w": col1_w,
                            "h": row_h,
                            "text": row["col1"],
                            "font_size": col1_size,
                            "font_color": plain_col1_color,
                            "font_weight": col1_weight,
                            "font_style": col1_style,
                            "alignment": col1_align,
                            "vertical_align": "middle",
                            "wrap": False,
                            **({"font_family": col1_font_family} if col1_font_family else {}),
                        }
                    )

            # ── Col 2 — heading ──────────────────────────────────────────
            if row["heading"]:
                eff_h_color = active_h_color if is_active else h_color
                eff_h_weight = active_h_weight if is_active else h_weight
                eff_h_style = active_font_style if is_active else h_style
                box.add(
                    {
                        "type": "text",
                        "x": col2_x,
                        "y": col2_y,
                        "w": col2_w,
                        "h": row_h,
                        **text_and_runs(row["heading"]),
                        "font_size": h_size,
                        "line_height": h_lh,
                        "font_color": eff_h_color,
                        "font_weight": eff_h_weight,
                        "font_style": eff_h_style,
                        "alignment": col2_align,
                        "vertical_align": row_valign,
                        "wrap": True,
                    }
                )

            # ── Col 3 — body text ────────────────────────────────────────
            if has_col3 and row["body"]:
                eff_b_color = active_b_color if is_active else b_color
                box.add(
                    {
                        "type": "text",
                        "x": col3_x,
                        "y": col3_y,
                        "w": col3_w,
                        "h": row_h,
                        **text_and_runs(row["body"]),
                        "font_size": b_size,
                        "line_height": b_lh,
                        "font_color": eff_b_color,
                        "font_weight": b_weight,
                        "font_style": b_style,
                        "alignment": col3_align,
                        "vertical_align": row_valign,
                        "wrap": True,
                    }
                )

            # ── Row separator ────────────────────────────────────────────
            if sep_visible and i < len(rows) - 1:
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

            y_cursor += row_h
