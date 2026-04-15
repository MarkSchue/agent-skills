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

    def _tok(self, name: str, default=None):
        """Resolve ``card-table-{name}`` with fallback to ``card-{name}`` (base token)."""
        return self._resolve_tok("table", name, default)

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
            stripe_raw = self._tok("stripe-visible")
            stripe_visible = stripe_raw in (True, "true", "True")

        if not headers and not rows:
            return  # nothing to render

        # ── Token resolution ────────────────────────────────────────────

        # Heading row
        header_bg        = self._tok("heading-bg-color",       "#1A1A2E")
        header_fg        = self._tok("heading-font-color",     "#FFFFFF")
        header_font_size = float(self._tok("heading-font-size", 14))
        header_weight    = self._tok("heading-font-weight",    "bold")
        header_style     = self._tok("heading-font-style",     "normal")
        header_align     = header_alignment_override or self._tok("heading-alignment", "left")
        header_height    = float(self._tok("heading-height",   28))
        header_border_color = self._tok("heading-border-color") or header_bg

        # Body rows
        body_font_size  = float(self._tok("body-font-size",  14))
        body_fg         = self._tok("body-font-color",       "#374151")
        body_weight     = self._tok("body-font-weight",      "normal")
        body_style      = self._tok("body-font-style",       "normal")
        body_height     = float(self._tok("body-height",     24))
        body_min_height = float(self._tok("body-min-height", 20))
        body_bg         = self._tok("body-bg-color")         or "transparent"
        body_align      = self._tok("body-alignment",        "left")

        # Stripe
        stripe_color   = self._tok("stripe-color",           "#F3F4F6")

        # Sum row
        sum_bg         = self._tok("sum-bg-color",           "#E5E7EB")
        sum_fg         = self._tok("sum-font-color",         "#1A1A2E")
        sum_font_size  = float(self._tok("sum-font-size",    12))
        sum_weight     = self._tok("sum-font-weight",        "bold")
        sum_style      = self._tok("sum-font-style",         "normal")
        sum_align      = self._tok("sum-alignment",          "left")
        sum_height     = float(self._tok("sum-height",       28))

        # Grid
        border_color   = self._tok("border-color",           "#E5E7EB")
        border_width   = float(self._tok("border-width",     1))

        # Cell padding
        pad_x          = float(self._tok("padding-x",        8))
        pad_y          = float(self._tok("padding-y",        4))

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
                bg = body_bg if body_bg and body_bg.lower() != "transparent" else "#FFFFFF"

            # Per-column alignment — fall back to body_align
            aligns = []
            for ci in range(n_cols):
                aligns.append(col_alignments[ci] if ci < len(col_alignments) else body_align)

            all_rows.append({
                "cells": cells,
                "bg_color": bg,
                "font_color": body_fg,
                "font_size": body_font_size,
                "font_weight": body_weight,
                "font_style": body_style,
                "row_height": max(body_height, body_min_height),
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
                "row_height": max(sum_height, body_min_height),
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
