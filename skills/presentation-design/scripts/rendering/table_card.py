"""
TableCardRenderer — Renders table-card with themed header row, optional sum/total
row, alternating row stripe, and full design-token control.

PPTX output: emits a ``table`` element dict consumed by PptxExporter._add_table.
draw.io output: emits the same ``table`` element dict consumed by DrawioExporter._add_table.
Both exporters translate the common element dict into their native table representation.
"""

from __future__ import annotations

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class TableCardRenderer(BaseCardRenderer):
    """Renderer for ``table-card`` type."""

    variant = "card--table"

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        """Emit a single ``table`` element that fills the body box."""
        content = card.content if isinstance(card.content, dict) else {}

        headers: list[str] = content.get("headers") or []
        rows: list[list[str]] = content.get("rows") or []
        sum_row: bool = bool(content.get("sum_row", False))
        col_widths: list[float] | None = content.get("col_widths") or None
        col_alignments: list[str] = content.get("col_alignments") or []
        header_alignment_override: str | None = content.get("header_alignment") or None

        # stripe_rows can be driven from content YAML or CSS token
        stripe_content = content.get("stripe_rows")
        if stripe_content is not None:
            stripe_visible = bool(stripe_content)
        else:
            stripe_raw = self.resolve("card-table-stripe-visible")
            stripe_visible = stripe_raw in (True, "true", "True")

        if not headers and not rows:
            return  # nothing to render

        # ── Token resolution ────────────────────────────────────────────

        # Header
        header_bg        = self.resolve("card-table-header-bg-color")       or "#1A1A2E"
        header_fg        = self.resolve("card-table-header-font-color")     or "#FFFFFF"
        header_font_size = float(self.resolve("card-table-header-font-size") or 12)
        header_weight    = self.resolve("card-table-header-font-weight")    or "bold"
        header_style     = self.resolve("card-table-header-font-style")     or "normal"
        header_align     = header_alignment_override or self.resolve("card-table-header-alignment") or "left"
        header_height    = float(self.resolve("card-table-header-height")   or 28)
        header_border_color = self.resolve("card-table-header-border-color") or header_bg

        # Data rows
        row_font_size  = float(self.resolve("card-table-row-font-size")  or 12)
        row_fg         = self.resolve("card-table-row-font-color")       or "#374151"
        row_weight     = self.resolve("card-table-row-font-weight")      or "normal"
        row_style      = self.resolve("card-table-row-font-style")       or "normal"
        row_height     = float(self.resolve("card-table-row-height")     or 24)
        row_min_height = float(self.resolve("card-table-row-min-height") or 20)
        row_bg         = self.resolve("card-table-row-bg-color")         or "transparent"
        row_align      = self.resolve("card-table-row-alignment")        or "left"

        # Stripe
        stripe_color   = self.resolve("card-table-stripe-color")         or "#F3F4F6"

        # Sum row
        sum_bg         = self.resolve("card-table-sum-bg-color")         or "#E5E7EB"
        sum_fg         = self.resolve("card-table-sum-font-color")       or "#1A1A2E"
        sum_font_size  = float(self.resolve("card-table-sum-font-size")  or 12)
        sum_weight     = self.resolve("card-table-sum-font-weight")      or "bold"
        sum_style      = self.resolve("card-table-sum-font-style")       or "normal"
        sum_align      = self.resolve("card-table-sum-alignment")        or "left"
        sum_height     = float(self.resolve("card-table-sum-height")     or 28)

        # Grid
        border_color   = self.resolve("card-table-border-color")         or "#E5E7EB"
        border_width   = float(self.resolve("card-table-border-width")   or 1)

        # Cell padding
        pad_x          = float(self.resolve("card-table-padding-x")      or 8)
        pad_y          = float(self.resolve("card-table-padding-y")      or 4)

        # ── Column widths ───────────────────────────────────────────────
        n_cols = max(len(headers), max((len(r) for r in rows), default=0))
        if n_cols == 0:
            return

        if col_widths and len(col_widths) >= n_cols:
            # Normalise so the fractions sum to 1.0
            total = sum(col_widths[:n_cols])
            col_fracs = [w / total for w in col_widths[:n_cols]]
        else:
            col_fracs = [1.0 / n_cols] * n_cols

        col_w_px = [frac * box.w for frac in col_fracs]

        # ── Row descriptors ─────────────────────────────────────────────
        # Each row dict: {cells, bg_color, font_color, font_size, font_weight,
        #                 font_style, row_height, is_header, is_sum, alignments}
        all_rows: list[dict] = []

        # Header row
        if headers:
            h_cells = list(headers) + [""] * max(0, n_cols - len(headers))
            h_aligns = [header_align] * n_cols
            all_rows.append({
                "cells": h_cells,
                "bg_color": header_bg,
                "font_color": header_fg,
                "font_size": header_font_size,
                "font_weight": header_weight,
                "font_style": header_style,
                "row_height": header_height,
                "is_header": True,
                "is_sum": False,
                "alignments": h_aligns,
                "border_bottom_color": header_border_color,
            })

        # Data rows
        data_rows = rows if not sum_row else rows[:-1]
        last_row  = rows[-1] if (sum_row and rows) else None

        for i, row_data in enumerate(data_rows):
            cells = list(row_data) + [""] * max(0, n_cols - len(row_data))
            # Stripe: odd-indexed rows (0-based: rows 1, 3, 5 …) get stripe colour
            if stripe_visible and (i % 2 == 1):
                bg = stripe_color
            else:
                bg = row_bg if row_bg and row_bg.lower() != "transparent" else "#FFFFFF"

            # Per-column alignment — fall back to row_align
            aligns = []
            for ci in range(n_cols):
                aligns.append(col_alignments[ci] if ci < len(col_alignments) else row_align)

            all_rows.append({
                "cells": cells,
                "bg_color": bg,
                "font_color": row_fg,
                "font_size": row_font_size,
                "font_weight": row_weight,
                "font_style": row_style,
                "row_height": max(row_height, row_min_height),
                "is_header": False,
                "is_sum": False,
                "alignments": aligns,
                "border_bottom_color": border_color,
            })

        # Sum row
        if last_row is not None:
            cells = list(last_row) + [""] * max(0, n_cols - len(last_row))
            s_aligns = []
            for ci in range(n_cols):
                s_aligns.append(col_alignments[ci] if ci < len(col_alignments) else sum_align)
            all_rows.append({
                "cells": cells,
                "bg_color": sum_bg,
                "font_color": sum_fg,
                "font_size": sum_font_size,
                "font_weight": sum_weight,
                "font_style": sum_style,
                "row_height": max(sum_height, row_min_height),
                "is_header": False,
                "is_sum": True,
                "alignments": s_aligns,
                "border_bottom_color": border_color,
            })

        # ── Emit table element ──────────────────────────────────────────
        box.add({
            "type": "table",
            "x": box.x,
            "y": box.y,
            "w": box.w,
            "h": box.h,
            "col_widths": col_w_px,
            "rows": all_rows,
            "border_color": border_color,
            "border_width": border_width,
            "pad_x": pad_x,
            "pad_y": pad_y,
        })
