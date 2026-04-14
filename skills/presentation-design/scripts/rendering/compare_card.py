"""
CompareCardRenderer — Renders a feature/option comparison matrix.

Layout::

    ┌──────────────┬─────────────┬─────────────┬─────────────┐
    │ (Topic hdr)  │  Column A   │  Column B*  │  Column C   │
    ├──────────────┼─────────────┼─────────────┼─────────────┤
    │ ① Feature 1  │  ✓          │  ✓          │  ✗          │
    │ ② Feature 2  │  Limited    │  Full       │  Full       │
    ├──────────────┼─────────────┼─────────────┼─────────────┤
    │ Verdict      │             │  Best Pick  │             │
    └──────────────┴─────────────┴─────────────┴─────────────┘

    * Column B is highlighted (different header background).

Columns
-------
``content.columns`` — list of up to 5 comparison column descriptors.
Each entry:  ``{label, highlight}`` (both optional).

Topic column
------------
Optional left column, controlled by ``content.topic_col.visible`` or
``--card-compare-topic-col-visible``.  The topic label in each row may be
accompanied by a sequential badge or a custom icon:

``--card-compare-topic-marker``  ``none`` | ``number`` | ``icon``
  ``number``  → sequential 1-based integer rendered inside a badge shape.
  ``icon``    → value from ``topic.icon`` rendered inside a badge shape.
  ``none``    → plain text label only (default).

Badge shape is controlled by ``--card-compare-topic-badge-shape``:
  ``circle`` (default, uses ``ellipse`` element), ``square`` (uses ``rect``),
  ``none`` (no background behind the number/icon).

Cells
-----
Each cell in ``content.rows[].cells`` can be:

- A plain string  → rendered as a ``text`` element.
- A dict with ``value``, ``icon``, ``color``, ``alignment``, ``highlighted``,
  ``bg_color`` keys (all optional).
  - When ``icon`` is a non-empty Material Symbols ligature name (e.g. ``"check"``),
    an ``icon`` element is rendered instead of text.
  - ``color`` overrides the resolved font / icon colour for that cell.
  - ``bg_color`` paint a per-cell background rect.

Summary row
-----------
``content.summary`` — optional dict ``{topic, cells}`` that appends a styled
result row at the bottom.  Set ``cells[n].highlighted: true`` to apply the
accent background to that cell.

CSS token naming
----------------
All tokens follow ``--card-compare-{element}-{property}``.  Resolution goes
through the standard four-level chain: per-card → per-slide → variant class →
base class → Python fallback.
"""

from __future__ import annotations

from typing import Any

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class CompareCardRenderer(BaseCardRenderer):
    """Renderer for ``compare-card`` type."""

    variant = "card--compare"

    # ── Helpers ──────────────────────────────────────────────────────────

    def _tok(self, name: str, default: Any = None) -> Any:
        """Resolve ``card-compare-{name}`` with fallback to ``card-{name}``."""
        return self._resolve_tok("compare", name, default)

    @staticmethod
    def _is_false(value: Any) -> bool:
        return value in (False, "false", "False", "0", 0)

    @staticmethod
    def _is_true(value: Any) -> bool:
        return value in (True, "true", "True", "1", 1)

    @staticmethod
    def _normalize_cell(raw: object) -> dict[str, Any]:
        """Normalise a raw cell value (string or dict) to a uniform dict."""
        if isinstance(raw, dict):
            return {
                "value": str(raw.get("value", raw.get("text", "")) or ""),
                "icon": str(raw.get("icon", "") or ""),
                "color": str(raw.get("color", "") or ""),
                "alignment": str(raw.get("alignment", "") or ""),
                "highlighted": bool(raw.get("highlighted", False)),
                "bg_color": str(raw.get("bg_color", "") or ""),
            }
        return {
            "value": str(raw) if raw is not None else "",
            "icon": "",
            "color": "",
            "alignment": "",
            "highlighted": False,
            "bg_color": "",
        }

    @staticmethod
    def _normalize_topic(raw: object) -> dict[str, Any]:
        """Normalise a raw topic value to a uniform dict."""
        if isinstance(raw, dict):
            return {
                "text": str(raw.get("text", "") or ""),
                "icon": str(raw.get("icon", "") or ""),
                "number": raw.get("number"),
            }
        return {"text": str(raw) if raw is not None else "", "icon": "", "number": None}

    def _add_badge(
        self,
        box: RenderBox,
        bx: float,
        by: float,
        badge_size: float,
        badge_shape: str,
        badge_bg: str,
        # content: one of number_text or icon_name must be non-empty
        number_text: str = "",
        icon_name: str = "",
        font_size: float = 8,
        font_color: str = "#FFFFFF",
        icon_font_family: str = "Material Symbols Outlined",
    ) -> None:
        """Emit badge background shape + number or icon content."""
        if badge_shape == "circle":
            box.add({
                "type": "ellipse",
                "x": bx, "y": by,
                "w": badge_size, "h": badge_size,
                "fill": badge_bg,
                "stroke": "none", "stroke_width": 0,
            })
        elif badge_shape == "square":
            box.add({
                "type": "rect",
                "x": bx, "y": by,
                "w": badge_size, "h": badge_size,
                "fill": badge_bg,
                "stroke": "none", "stroke_width": 0,
                "rx": 0,
            })
        # badge_shape == "none" → no background

        if number_text:
            box.add({
                "type": "text",
                "x": bx, "y": by,
                "w": badge_size, "h": badge_size,
                "text": number_text,
                "font_size": font_size,
                "font_color": font_color,
                "font_weight": "700",
                "alignment": "center",
                "vertical_align": "middle",
                "wrap": False,
            })
        elif icon_name:
            box.add({
                "type": "icon",
                "x": bx, "y": by,
                "w": badge_size, "h": badge_size,
                "name": icon_name,
                "font_family": icon_font_family,
                "font_size": badge_size * 0.65,
                "color": font_color,
            })

    # ── Body rendering ────────────────────────────────────────────────────

    def render_body(self, card: CardModel, box: RenderBox) -> None:  # noqa: C901
        """Render the comparison matrix into *box*."""
        content = card.content if isinstance(card.content, dict) else {}

        # ── Parse columns ──────────────────────────────────────────────
        raw_cols = content.get("columns") or []
        columns: list[dict[str, Any]] = []
        for c in raw_cols[:5]:
            if isinstance(c, dict):
                columns.append({
                    "label": str(c.get("label", "") or ""),
                    "highlight": bool(c.get("highlight", False)),
                })
            else:
                columns.append({"label": str(c) if c is not None else "", "highlight": False})

        n_cols = max(1, len(columns))

        # ── Parse topic column config ──────────────────────────────────
        topic_cfg = content.get("topic_col") or {}
        if isinstance(topic_cfg, dict):
            topic_label = str(topic_cfg.get("label", "") or "")
            _tv_raw = topic_cfg.get("visible")
            _tw_raw = topic_cfg.get("width_pct")
        else:
            topic_label = ""
            _tv_raw = None
            _tw_raw = None

        # topic-col visibility: content overrides CSS token
        if _tv_raw is not None:
            topic_visible = not self._is_false(_tv_raw)
        else:
            _tv = self._tok("label-col-visible")
            topic_visible = not self._is_false(_tv) if _tv is not None else True

        # ── Parse rows ─────────────────────────────────────────────────
        raw_rows: list = content.get("rows") or []
        rows: list[dict[str, Any]] = []
        for i, r in enumerate(raw_rows):
            if isinstance(r, dict):
                topic = self._normalize_topic(r.get("topic"))
                cells = [self._normalize_cell(c) for c in (r.get("cells") or [])]
            else:
                topic = self._normalize_topic(None)
                cells = []
            while len(cells) < n_cols:
                cells.append(self._normalize_cell(None))
            rows.append({"topic": topic, "cells": cells[:n_cols]})

        n_rows = len(rows)

        # ── Parse summary row ──────────────────────────────────────────
        raw_summary = content.get("summary")
        has_summary = False
        summary: dict[str, Any] | None = None

        if raw_summary is not None:
            if isinstance(raw_summary, dict):
                summ_cells = [
                    self._normalize_cell(c) for c in (raw_summary.get("cells") or [])
                ]
                while len(summ_cells) < n_cols:
                    summ_cells.append(self._normalize_cell(None))
                summary = {
                    "topic_text": str(raw_summary.get("topic", "") or ""),
                    "cells": summ_cells[:n_cols],
                }
                has_summary = True

        if not has_summary:
            _sv = self._tok("summary-visible")
            has_summary = self._is_true(_sv) if _sv is not None else False

        # ── Token resolution ───────────────────────────────────────────
        icon_font_family = str(
            self.resolve("icon-font-family") or "Material Symbols Outlined"
        )

        # Heading row
        header_h = float(self._tok("heading-height", 28))
        header_bg = str(
            self._tok("heading-bg-color")
            or self.resolve("color-primary")
            or "#1A1A2E"
        )
        header_fg = str(
            self._tok("heading-font-color")
            or self.resolve("color-text-inverse")
            or "#FFFFFF"
        )
        header_size = float(self._tok("heading-font-size", 9))
        header_weight = str(self._tok("heading-font-weight") or "700")
        header_style = str(self._tok("heading-font-style") or "normal")
        header_align = str(self._tok("heading-alignment") or "center")

        # Highlighted column overrides
        hl_header_bg = str(
            self._tok("highlight-col-heading-bg-color")
            or self.resolve("color-accent")
            or "#3B82F6"
        )
        hl_header_fg = str(self._tok("highlight-col-heading-font-color") or "#FFFFFF")
        hl_col_bg_raw = self._tok("highlight-col-bg-color")
        hl_col_bg = str(hl_col_bg_raw) if hl_col_bg_raw else ""

        # Label column
        topic_col_pct = float(
            _tw_raw or self._tok("label-col-width-pct", 25)
        ) / 100
        topic_col_bg = str(
            self._tok("label-col-bg-color")
            or self.resolve("color-surface-sunken")
            or "#F3F4F6"
        )
        topic_col_header_bg = str(
            self._tok("label-col-heading-bg-color") or header_bg
        )
        topic_col_header_fg = str(
            self._tok("label-col-heading-font-color") or header_fg
        )
        topic_size = float(self._tok("label-font-size", 11))
        topic_color = str(
            self._tok("label-font-color")
            or self.resolve("color-text-default")
            or "#1F2937"
        )
        topic_weight = str(self._tok("label-font-weight") or "700")
        topic_style = str(self._tok("label-font-style") or "normal")
        topic_align = str(self._tok("label-alignment") or "left")

        # Label marker / badge
        topic_marker = str(self._tok("label-marker") or "none").lower()
        topic_badge_shape = str(self._tok("label-badge-shape") or "circle").lower()
        topic_badge_color = str(
            self._tok("label-badge-color")
            or self.resolve("color-accent")
            or "#3B82F6"
        )
        topic_badge_size = float(self._tok("label-badge-size", 18))
        topic_badge_fs = float(self._tok("label-badge-font-size", 8))
        topic_badge_fc = str(self._tok("label-badge-font-color") or "#FFFFFF")
        topic_badge_gap = float(self._tok("label-badge-gap", 6))

        # Body cells
        cell_size = float(self._tok("body-font-size", 11))
        cell_color = str(
            self._tok("body-font-color")
            or self.resolve("color-text-subtle")
            or "#374151"
        )
        cell_weight = str(self._tok("body-font-weight") or "400")
        cell_style = str(self._tok("body-font-style") or "normal")
        cell_align = str(self._tok("body-alignment") or "center")
        cell_bg_tok = self._tok("body-bg-color")
        cell_bg = str(cell_bg_tok) if cell_bg_tok else ""
        cell_icon_size = float(self._tok("body-icon-size", 14))
        cell_icon_color = str(
            self._tok("body-icon-color")
            or self.resolve("color-text-default")
            or "#374151"
        )
        pad_x = float(self._tok("body-padding-x", 6))
        pad_y = float(self._tok("body-padding-y", 4))

        # Row geometry
        row_h_tok = self._tok("row-height")
        row_min_h = float(self._tok("row-min-height", 24))

        # Stripe
        stripe_vis_raw = self._tok("row-stripe-visible")
        stripe_visible = self._is_true(stripe_vis_raw) if stripe_vis_raw is not None else False
        stripe_color = str(
            self._tok("row-stripe-color")
            or self.resolve("color-surface-sunken")
            or "#F3F4F6"
        )

        # Separators
        row_sep_vis_raw = self._tok("row-separator-visible")
        row_sep_visible = not self._is_false(row_sep_vis_raw) if row_sep_vis_raw is not None else True
        row_sep_color = str(
            self._tok("row-separator-color")
            or self.resolve("color-border")
            or "#E5E7EB"
        )
        row_sep_width = float(self._tok("row-separator-width", 1))

        col_sep_vis_raw = self._tok("col-separator-visible")
        col_sep_visible = not self._is_false(col_sep_vis_raw) if col_sep_vis_raw is not None else True
        col_sep_color = str(
            self._tok("col-separator-color")
            or self.resolve("color-border")
            or "#E5E7EB"
        )
        col_sep_width = float(self._tok("col-separator-width", 1))

        # Grid border (outer)
        grid_bdr_vis_raw = self._tok("grid-border-visible")
        grid_bdr_visible = not self._is_false(grid_bdr_vis_raw) if grid_bdr_vis_raw is not None else True
        grid_bdr_color = str(
            self._tok("grid-border-color")
            or self.resolve("color-border")
            or "#E5E7EB"
        )
        grid_bdr_width = float(self._tok("grid-border-width", 1))

        # Summary row
        summ_h = float(self._tok("summary-height", 32))
        summ_bg = str(
            self._tok("summary-bg-color")
            or self.resolve("color-primary")
            or "#1A1A2E"
        )
        summ_fg = str(
            self._tok("summary-font-color")
            or self.resolve("color-text-inverse")
            or "#FFFFFF"
        )
        summ_size = float(self._tok("summary-font-size", 11))
        summ_weight = str(self._tok("summary-font-weight") or "700")
        summ_style = str(self._tok("summary-font-style") or "normal")
        summ_align = str(self._tok("summary-alignment") or "center")
        summ_hl_bg = str(
            self._tok("summary-highlight-bg-color")
            or self.resolve("color-accent")
            or "#3B82F6"
        )
        summ_hl_fg = str(self._tok("summary-highlight-font-color") or "#FFFFFF")

        # ── Column geometry ────────────────────────────────────────────
        topic_col_w = box.w * topic_col_pct if topic_visible else 0.0
        compare_total_w = box.w - topic_col_w

        # Per-comparison-column fractional widths (from content.col_widths or equal)
        raw_col_widths = content.get("col_widths")
        if raw_col_widths and len(raw_col_widths) >= n_cols:
            total_w = sum(float(w) for w in raw_col_widths[:n_cols]) or 1.0
            col_fracs = [float(w) / total_w for w in raw_col_widths[:n_cols]]
        else:
            col_fracs = [1.0 / n_cols] * n_cols

        col_xs: list[float] = []   # x start of each comparison column
        col_ws: list[float] = []   # width of each comparison column
        _cx = box.x + topic_col_w
        for frac in col_fracs:
            _cw = compare_total_w * frac
            col_xs.append(_cx)
            col_ws.append(_cw)
            _cx += _cw

        # ── Row heights ────────────────────────────────────────────────
        avail_h = box.h - header_h - (summ_h if has_summary else 0.0)

        if n_rows > 0:
            if row_h_tok is not None:
                row_h = max(row_min_h, float(row_h_tok))
                if row_h * n_rows > avail_h > 0:
                    row_h = max(row_min_h, avail_h / n_rows)
            else:
                row_h = max(row_min_h, avail_h / n_rows) if avail_h > 0 else row_min_h
        else:
            row_h = row_min_h

        # ── Y anchors ─────────────────────────────────────────────────
        header_y = box.y
        rows_y = header_y + header_h
        summary_y = rows_y + row_h * n_rows
        total_h = header_h + row_h * n_rows + (summ_h if has_summary else 0.0)

        # ── Step 1 — Topic column background ──────────────────────────
        if topic_visible and n_rows > 0:
            box.add({
                "type": "rect",
                "x": box.x, "y": rows_y,
                "w": topic_col_w, "h": row_h * n_rows,
                "fill": topic_col_bg,
                "stroke": "none", "stroke_width": 0, "rx": 0,
            })

        # ── Step 2 — Highlighted comparison column backgrounds ─────────
        if hl_col_bg:
            for ci, col in enumerate(columns):
                if col["highlight"] and n_rows > 0:
                    box.add({
                        "type": "rect",
                        "x": col_xs[ci], "y": rows_y,
                        "w": col_ws[ci], "h": row_h * n_rows,
                        "fill": hl_col_bg,
                        "stroke": "none", "stroke_width": 0, "rx": 0,
                    })

        # ── Step 3 — Row stripes ───────────────────────────────────────
        if stripe_visible:
            for ri in range(n_rows):
                if ri % 2 == 1:
                    box.add({
                        "type": "rect",
                        "x": box.x, "y": rows_y + ri * row_h,
                        "w": box.w, "h": row_h,
                        "fill": stripe_color,
                        "stroke": "none", "stroke_width": 0, "rx": 0,
                    })

        # ── Step 4 — Header row ────────────────────────────────────────
        # Topic column header cell
        if topic_visible:
            box.add({
                "type": "rect",
                "x": box.x, "y": header_y,
                "w": topic_col_w, "h": header_h,
                "fill": topic_col_header_bg,
                "stroke": "none", "stroke_width": 0, "rx": 0,
            })
            if topic_label:
                box.add({
                    "type": "text",
                    "x": box.x + pad_x, "y": header_y,
                    "w": topic_col_w - 2 * pad_x, "h": header_h,
                    "text": topic_label,
                    "font_size": header_size,
                    "font_color": topic_col_header_fg,
                    "font_weight": header_weight,
                    "font_style": header_style,
                    "alignment": topic_align,
                    "vertical_align": "middle",
                    "wrap": False,
                })

        # Comparison column header cells
        for ci, col in enumerate(columns):
            eff_hbg = hl_header_bg if col["highlight"] else header_bg
            eff_hfg = hl_header_fg if col["highlight"] else header_fg
            box.add({
                "type": "rect",
                "x": col_xs[ci], "y": header_y,
                "w": col_ws[ci], "h": header_h,
                "fill": eff_hbg,
                "stroke": "none", "stroke_width": 0, "rx": 0,
            })
            if col["label"]:
                box.add({
                    "type": "text",
                    "x": col_xs[ci] + pad_x, "y": header_y,
                    "w": col_ws[ci] - 2 * pad_x, "h": header_h,
                    "text": col["label"],
                    "font_size": header_size,
                    "font_color": eff_hfg,
                    "font_weight": header_weight,
                    "font_style": header_style,
                    "alignment": header_align,
                    "vertical_align": "middle",
                    "wrap": True,
                    "line_height": header_size * 1.2,
                })

        # ── Step 5 — Data rows ─────────────────────────────────────────
        has_badge = topic_marker in ("number", "icon")

        for ri, row in enumerate(rows):
            ry = rows_y + ri * row_h
            topic = row["topic"]

            # Topic cell
            if topic_visible:
                if has_badge:
                    # Badge is vertically centred in the row
                    by = ry + (row_h - topic_badge_size) / 2
                    bx = box.x + pad_x

                    if topic_marker == "number":
                        num_str = str(
                            topic["number"] if topic["number"] is not None else ri + 1
                        )
                        self._add_badge(
                            box, bx, by, topic_badge_size, topic_badge_shape,
                            topic_badge_color,
                            number_text=num_str,
                            font_size=topic_badge_fs,
                            font_color=topic_badge_fc,
                            icon_font_family=icon_font_family,
                        )
                    else:  # icon
                        icon_name = str(topic["icon"] or "circle")
                        self._add_badge(
                            box, bx, by, topic_badge_size, topic_badge_shape,
                            topic_badge_color,
                            icon_name=icon_name,
                            font_size=topic_badge_fs,
                            font_color=topic_badge_fc,
                            icon_font_family=icon_font_family,
                        )

                    text_x = box.x + pad_x + topic_badge_size + topic_badge_gap
                    text_w = max(1.0, topic_col_w - pad_x - topic_badge_size - topic_badge_gap - pad_x)
                else:
                    text_x = box.x + pad_x
                    text_w = max(1.0, topic_col_w - 2 * pad_x)

                if topic["text"]:
                    box.add({
                        "type": "text",
                        "x": text_x, "y": ry,
                        "w": text_w, "h": row_h,
                        "text": topic["text"],
                        "font_size": topic_size,
                        "font_color": topic_color,
                        "font_weight": topic_weight,
                        "font_style": topic_style,
                        "alignment": topic_align,
                        "vertical_align": "middle",
                        "wrap": True,
                    })

            # Comparison cells
            for ci, cell in enumerate(row["cells"]):
                cx = col_xs[ci]
                cw = col_ws[ci]
                eff_align = cell["alignment"] or cell_align

                # Per-cell background
                eff_cell_bg = cell["bg_color"] or cell_bg
                if eff_cell_bg and eff_cell_bg.lower() not in ("transparent", "none", ""):
                    box.add({
                        "type": "rect",
                        "x": cx, "y": ry, "w": cw, "h": row_h,
                        "fill": eff_cell_bg,
                        "stroke": "none", "stroke_width": 0, "rx": 0,
                    })

                if cell["icon"]:
                    # Icon element — horizontally positioned per alignment token
                    icon_sz = cell_icon_size
                    eff_icon_color = cell["color"] or cell_icon_color
                    if eff_align == "left":
                        icon_x = cx + pad_x
                    elif eff_align == "right":
                        icon_x = cx + cw - pad_x - icon_sz
                    else:  # center
                        icon_x = cx + (cw - icon_sz) / 2
                    icon_y = ry + (row_h - icon_sz) / 2
                    box.add({
                        "type": "icon",
                        "x": icon_x, "y": icon_y,
                        "w": icon_sz, "h": icon_sz,
                        "name": cell["icon"],
                        "font_family": icon_font_family,
                        "font_size": icon_sz,
                        "color": eff_icon_color,
                    })
                elif cell["value"]:
                    eff_color = cell["color"] or cell_color
                    box.add({
                        "type": "text",
                        "x": cx + pad_x, "y": ry,
                        "w": max(1.0, cw - 2 * pad_x), "h": row_h,
                        "text": cell["value"],
                        "font_size": cell_size,
                        "font_color": eff_color,
                        "font_weight": cell_weight,
                        "font_style": cell_style,
                        "alignment": eff_align,
                        "vertical_align": "middle",
                        "wrap": True,
                    })

        # ── Step 6 — Summary row ───────────────────────────────────────
        if has_summary:
            # Full-width background
            box.add({
                "type": "rect",
                "x": box.x, "y": summary_y,
                "w": box.w, "h": summ_h,
                "fill": summ_bg,
                "stroke": "none", "stroke_width": 0, "rx": 0,
            })

            if summary is not None:
                # Topic column in summary
                if topic_visible and summary["topic_text"]:
                    box.add({
                        "type": "text",
                        "x": box.x + pad_x, "y": summary_y,
                        "w": max(1.0, topic_col_w - 2 * pad_x), "h": summ_h,
                        "text": summary["topic_text"],
                        "font_size": summ_size,
                        "font_color": summ_fg,
                        "font_weight": summ_weight,
                        "font_style": summ_style,
                        "alignment": topic_align,
                        "vertical_align": "middle",
                        "wrap": False,
                    })

                # Comparison cells in summary
                for ci, cell in enumerate(summary["cells"]):
                    cx = col_xs[ci]
                    cw = col_ws[ci]
                    eff_align = cell["alignment"] or summ_align
                    use_hl = cell["highlighted"]
                    eff_bg = cell["bg_color"] or (summ_hl_bg if use_hl else "")
                    eff_fg = cell["color"] or (summ_hl_fg if use_hl else summ_fg)

                    # Highlighted / custom background overlay
                    if eff_bg and eff_bg.lower() not in ("transparent", "none", ""):
                        box.add({
                            "type": "rect",
                            "x": cx, "y": summary_y, "w": cw, "h": summ_h,
                            "fill": eff_bg,
                            "stroke": "none", "stroke_width": 0, "rx": 0,
                        })

                    if cell["icon"]:
                        icon_sz = cell_icon_size
                        box.add({
                            "type": "icon",
                            "x": cx + (cw - icon_sz) / 2,
                            "y": summary_y + (summ_h - icon_sz) / 2,
                            "w": icon_sz, "h": icon_sz,
                            "name": cell["icon"],
                            "font_family": icon_font_family,
                            "font_size": icon_sz,
                            "color": eff_fg,
                        })
                    elif cell["value"]:
                        box.add({
                            "type": "text",
                            "x": cx + pad_x, "y": summary_y,
                            "w": max(1.0, cw - 2 * pad_x), "h": summ_h,
                            "text": cell["value"],
                            "font_size": summ_size,
                            "font_color": eff_fg,
                            "font_weight": summ_weight,
                            "font_style": summ_style,
                            "alignment": eff_align,
                            "vertical_align": "middle",
                            "wrap": False,
                        })

        # ── Step 7 — Horizontal separators ────────────────────────────
        if row_sep_visible:
            # Header bottom line
            box.add({
                "type": "line",
                "x1": box.x, "y1": rows_y,
                "x2": box.x + box.w, "y2": rows_y,
                "stroke": row_sep_color, "stroke_width": row_sep_width,
            })
            # Between data rows
            for ri in range(n_rows - 1):
                sep_y = rows_y + (ri + 1) * row_h
                box.add({
                    "type": "line",
                    "x1": box.x, "y1": sep_y,
                    "x2": box.x + box.w, "y2": sep_y,
                    "stroke": row_sep_color, "stroke_width": row_sep_width,
                })
            # Before summary row
            if has_summary and n_rows > 0:
                box.add({
                    "type": "line",
                    "x1": box.x, "y1": summary_y,
                    "x2": box.x + box.w, "y2": summary_y,
                    "stroke": row_sep_color, "stroke_width": row_sep_width,
                })

        # ── Step 8 — Vertical separators ──────────────────────────────
        if col_sep_visible:
            sep_top = box.y
            sep_bot = box.y + total_h
            # After topic column
            if topic_visible:
                sx = box.x + topic_col_w
                box.add({
                    "type": "line",
                    "x1": sx, "y1": sep_top, "x2": sx, "y2": sep_bot,
                    "stroke": col_sep_color, "stroke_width": col_sep_width,
                })
            # Between comparison columns
            for ci in range(n_cols - 1):
                sx = col_xs[ci] + col_ws[ci]
                box.add({
                    "type": "line",
                    "x1": sx, "y1": sep_top, "x2": sx, "y2": sep_bot,
                    "stroke": col_sep_color, "stroke_width": col_sep_width,
                })

        # ── Step 9 — Outer grid border ────────────────────────────────
        if grid_bdr_visible:
            box.add({
                "type": "rect",
                "x": box.x, "y": box.y,
                "w": box.w, "h": total_h,
                "fill": "transparent",
                "stroke": grid_bdr_color,
                "stroke_width": grid_bdr_width,
                "rx": 0,
            })
