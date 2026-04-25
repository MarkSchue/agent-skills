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

The renderer is split across three sibling modules so the steps stay
readable:

* :mod:`._data`     — content normalisation & parsing
* :mod:`._style`    — :class:`CompareStyle` dataclass that resolves all tokens
* :mod:`._geometry` — :class:`CompareGeometry` with column widths / y-anchors

Token naming follows ``--card-compare-{element}-{property}`` and goes through
the standard four-level resolution chain.
"""

from __future__ import annotations

from typing import Any

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox
from scripts.rendering.compare_card._data import (
    parse_columns, parse_rows, parse_summary, parse_topic_cfg,
)
from scripts.rendering.compare_card._geometry import CompareGeometry, compute_geometry
from scripts.rendering.compare_card._style import CompareStyle


class CompareCardRenderer(BaseCardRenderer):
    """Renderer for ``compare-card`` type."""

    variant = "card--compare"

    # ── Body rendering ────────────────────────────────────────────────────

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        content = card.content if isinstance(card.content, dict) else {}

        columns = parse_columns(content)
        n_cols = max(1, len(columns))
        topic_label, tv_raw, tw_raw = parse_topic_cfg(content)
        rows = parse_rows(content, n_cols)
        summary = parse_summary(content, n_cols)

        s = CompareStyle.resolve(
            self,
            topic_visible_raw=tv_raw,
            topic_width_pct_raw=tw_raw,
            has_summary_explicit=summary is not None,
        )
        g = compute_geometry(box, columns, rows, content, s)

        self._draw_topic_bg(box, s, g)
        self._draw_highlighted_col_bgs(box, columns, s, g)
        self._draw_row_stripes(box, s, g)
        self._draw_header_row(box, columns, topic_label, s, g)
        self._draw_data_rows(box, rows, s, g)
        if s.has_summary:
            self._draw_summary_row(box, summary, s, g)
        self._draw_separators(box, s, g)
        self._draw_grid_border(box, s, g)

    # ── Step renderers ────────────────────────────────────────────────────

    def _draw_topic_bg(
        self, box: RenderBox, s: CompareStyle, g: CompareGeometry
    ) -> None:
        if s.topic_visible and g.n_rows > 0:
            box.add({
                "type": "rect",
                "x": box.x, "y": g.rows_y,
                "w": g.topic_col_w, "h": g.row_h * g.n_rows,
                "fill": s.topic_col_bg,
                "stroke": "none", "stroke_width": 0, "rx": 0,
            })

    def _draw_highlighted_col_bgs(
        self, box: RenderBox, columns: list[dict[str, Any]],
        s: CompareStyle, g: CompareGeometry,
    ) -> None:
        if not s.hl_col_bg:
            return
        for ci, col in enumerate(columns):
            if col["highlight"] and g.n_rows > 0:
                box.add({
                    "type": "rect",
                    "x": g.col_xs[ci], "y": g.rows_y,
                    "w": g.col_ws[ci], "h": g.row_h * g.n_rows,
                    "fill": s.hl_col_bg,
                    "stroke": "none", "stroke_width": 0, "rx": 0,
                })

    def _draw_row_stripes(
        self, box: RenderBox, s: CompareStyle, g: CompareGeometry
    ) -> None:
        if not s.stripe_visible:
            return
        for ri in range(g.n_rows):
            if ri % 2 == 1:
                box.add({
                    "type": "rect",
                    "x": box.x, "y": g.rows_y + ri * g.row_h,
                    "w": box.w, "h": g.row_h,
                    "fill": s.stripe_color,
                    "stroke": "none", "stroke_width": 0, "rx": 0,
                })

    def _draw_header_row(
        self, box: RenderBox, columns: list[dict[str, Any]], topic_label: str,
        s: CompareStyle, g: CompareGeometry,
    ) -> None:
        # Topic column header cell
        if s.topic_visible:
            box.add({
                "type": "rect",
                "x": box.x, "y": g.header_y,
                "w": g.topic_col_w, "h": s.header_h,
                "fill": s.topic_col_header_bg,
                "stroke": "none", "stroke_width": 0, "rx": 0,
            })
            if topic_label:
                box.add({
                    "type": "text",
                    "x": box.x + s.pad_x, "y": g.header_y,
                    "w": g.topic_col_w - 2 * s.pad_x, "h": s.header_h,
                    "text": topic_label,
                    "font_size": s.header_size,
                    "font_color": s.topic_col_header_fg,
                    "font_weight": s.header_weight,
                    "font_style": s.header_style,
                    "alignment": s.topic_align,
                    "vertical_align": "middle",
                    "wrap": False,
                })

        # Comparison column headers
        for ci, col in enumerate(columns):
            eff_hbg = s.hl_header_bg if col["highlight"] else s.header_bg
            eff_hfg = s.hl_header_fg if col["highlight"] else s.header_fg
            box.add({
                "type": "rect",
                "x": g.col_xs[ci], "y": g.header_y,
                "w": g.col_ws[ci], "h": s.header_h,
                "fill": eff_hbg,
                "stroke": "none", "stroke_width": 0, "rx": 0,
            })
            if col["label"]:
                box.add({
                    "type": "text",
                    "x": g.col_xs[ci] + s.pad_x, "y": g.header_y,
                    "w": g.col_ws[ci] - 2 * s.pad_x, "h": s.header_h,
                    "text": col["label"],
                    "font_size": s.header_size,
                    "font_color": eff_hfg,
                    "font_weight": s.header_weight,
                    "font_style": s.header_style,
                    "alignment": s.header_align,
                    "vertical_align": "middle",
                    "wrap": True,
                    "line_height": s.header_size * 1.2,
                })

    def _draw_data_rows(
        self, box: RenderBox, rows: list[dict[str, Any]],
        s: CompareStyle, g: CompareGeometry,
    ) -> None:
        has_badge = s.topic_marker in ("number", "icon")

        for ri, row in enumerate(rows):
            ry = g.rows_y + ri * g.row_h

            if s.topic_visible:
                self._draw_topic_cell(box, row["topic"], ri, ry, s, g, has_badge)

            for ci, cell in enumerate(row["cells"]):
                self._draw_data_cell(box, cell, g.col_xs[ci], ry, g.col_ws[ci], g.row_h, s)

    def _draw_topic_cell(
        self, box: RenderBox, topic: dict[str, Any],
        ri: int, ry: float, s: CompareStyle, g: CompareGeometry, has_badge: bool,
    ) -> None:
        if has_badge:
            by = ry + (g.row_h - s.topic_badge_size) / 2
            bx = box.x + s.pad_x
            if s.topic_marker == "number":
                num_str = str(topic["number"] if topic["number"] is not None else ri + 1)
                self._add_badge(box, bx, by, s, number_text=num_str)
            else:  # icon
                self._add_badge(box, bx, by, s, icon_name=str(topic["icon"] or "circle"))
            text_x = box.x + s.pad_x + s.topic_badge_size + s.topic_badge_gap
            text_w = max(1.0, g.topic_col_w - s.pad_x - s.topic_badge_size - s.topic_badge_gap - s.pad_x)
        else:
            text_x = box.x + s.pad_x
            text_w = max(1.0, g.topic_col_w - 2 * s.pad_x)

        if topic["text"]:
            box.add({
                "type": "text",
                "x": text_x, "y": ry,
                "w": text_w, "h": g.row_h,
                "text": topic["text"],
                "font_size": s.topic_size,
                "font_color": s.topic_color,
                "font_weight": s.topic_weight,
                "font_style": s.topic_style,
                "alignment": s.topic_align,
                "vertical_align": "middle",
                "wrap": True,
            })

    def _draw_data_cell(
        self, box: RenderBox, cell: dict[str, Any],
        cx: float, ry: float, cw: float, rh: float, s: CompareStyle,
    ) -> None:
        eff_align = cell["alignment"] or s.cell_align

        eff_cell_bg = cell["bg_color"] or s.cell_bg
        if eff_cell_bg and eff_cell_bg.lower() not in ("transparent", "none", ""):
            box.add({
                "type": "rect",
                "x": cx, "y": ry, "w": cw, "h": rh,
                "fill": eff_cell_bg,
                "stroke": "none", "stroke_width": 0, "rx": 0,
            })

        if cell["icon"]:
            icon_sz = s.cell_icon_size
            eff_icon_color = cell["color"] or s.cell_icon_color
            if eff_align == "left":
                icon_x = cx + s.pad_x
            elif eff_align == "right":
                icon_x = cx + cw - s.pad_x - icon_sz
            else:
                icon_x = cx + (cw - icon_sz) / 2
            box.add({
                "type": "icon",
                "x": icon_x, "y": ry + (rh - icon_sz) / 2,
                "w": icon_sz, "h": icon_sz,
                "name": cell["icon"],
                "font_family": s.icon_font_family,
                "font_size": icon_sz,
                "color": eff_icon_color,
            })
        elif cell["value"]:
            eff_color = cell["color"] or s.cell_color
            box.add({
                "type": "text",
                "x": cx + s.pad_x, "y": ry,
                "w": max(1.0, cw - 2 * s.pad_x), "h": rh,
                "text": cell["value"],
                "font_size": s.cell_size,
                "font_color": eff_color,
                "font_weight": s.cell_weight,
                "font_style": s.cell_style,
                "alignment": eff_align,
                "vertical_align": "middle",
                "wrap": True,
            })

    def _draw_summary_row(
        self, box: RenderBox, summary: dict[str, Any] | None,
        s: CompareStyle, g: CompareGeometry,
    ) -> None:
        # Full-width background
        box.add({
            "type": "rect",
            "x": box.x, "y": g.summary_y,
            "w": box.w, "h": s.summ_h,
            "fill": s.summ_bg,
            "stroke": "none", "stroke_width": 0, "rx": 0,
        })
        if summary is None:
            return

        if s.topic_visible and summary["topic_text"]:
            box.add({
                "type": "text",
                "x": box.x + s.pad_x, "y": g.summary_y,
                "w": max(1.0, g.topic_col_w - 2 * s.pad_x), "h": s.summ_h,
                "text": summary["topic_text"],
                "font_size": s.summ_size,
                "font_color": s.summ_fg,
                "font_weight": s.summ_weight,
                "font_style": s.summ_style,
                "alignment": s.topic_align,
                "vertical_align": "middle",
                "wrap": False,
            })

        for ci, cell in enumerate(summary["cells"]):
            cx, cw = g.col_xs[ci], g.col_ws[ci]
            eff_align = cell["alignment"] or s.summ_align
            use_hl = cell["highlighted"]
            eff_bg = cell["bg_color"] or (s.summ_hl_bg if use_hl else "")
            eff_fg = cell["color"] or (s.summ_hl_fg if use_hl else s.summ_fg)

            if eff_bg and eff_bg.lower() not in ("transparent", "none", ""):
                box.add({
                    "type": "rect",
                    "x": cx, "y": g.summary_y, "w": cw, "h": s.summ_h,
                    "fill": eff_bg,
                    "stroke": "none", "stroke_width": 0, "rx": 0,
                })

            if cell["icon"]:
                icon_sz = s.cell_icon_size
                box.add({
                    "type": "icon",
                    "x": cx + (cw - icon_sz) / 2,
                    "y": g.summary_y + (s.summ_h - icon_sz) / 2,
                    "w": icon_sz, "h": icon_sz,
                    "name": cell["icon"],
                    "font_family": s.icon_font_family,
                    "font_size": icon_sz,
                    "color": eff_fg,
                })
            elif cell["value"]:
                box.add({
                    "type": "text",
                    "x": cx + s.pad_x, "y": g.summary_y,
                    "w": max(1.0, cw - 2 * s.pad_x), "h": s.summ_h,
                    "text": cell["value"],
                    "font_size": s.summ_size,
                    "font_color": eff_fg,
                    "font_weight": s.summ_weight,
                    "font_style": s.summ_style,
                    "alignment": eff_align,
                    "vertical_align": "middle",
                    "wrap": False,
                })

    def _draw_separators(
        self, box: RenderBox, s: CompareStyle, g: CompareGeometry
    ) -> None:
        # Horizontal
        if s.row_sep_visible:
            box.add({
                "type": "line",
                "x1": box.x, "y1": g.rows_y,
                "x2": box.x + box.w, "y2": g.rows_y,
                "stroke": s.row_sep_color, "stroke_width": s.row_sep_width,
            })
            for ri in range(g.n_rows - 1):
                sep_y = g.rows_y + (ri + 1) * g.row_h
                box.add({
                    "type": "line",
                    "x1": box.x, "y1": sep_y,
                    "x2": box.x + box.w, "y2": sep_y,
                    "stroke": s.row_sep_color, "stroke_width": s.row_sep_width,
                })
            if s.has_summary and g.n_rows > 0:
                box.add({
                    "type": "line",
                    "x1": box.x, "y1": g.summary_y,
                    "x2": box.x + box.w, "y2": g.summary_y,
                    "stroke": s.row_sep_color, "stroke_width": s.row_sep_width,
                })

        # Vertical
        if s.col_sep_visible:
            sep_top = box.y
            sep_bot = box.y + g.total_h
            if s.topic_visible:
                sx = box.x + g.topic_col_w
                box.add({
                    "type": "line",
                    "x1": sx, "y1": sep_top, "x2": sx, "y2": sep_bot,
                    "stroke": s.col_sep_color, "stroke_width": s.col_sep_width,
                })
            for ci in range(g.n_cols - 1):
                sx = g.col_xs[ci] + g.col_ws[ci]
                box.add({
                    "type": "line",
                    "x1": sx, "y1": sep_top, "x2": sx, "y2": sep_bot,
                    "stroke": s.col_sep_color, "stroke_width": s.col_sep_width,
                })

    def _draw_grid_border(
        self, box: RenderBox, s: CompareStyle, g: CompareGeometry
    ) -> None:
        if s.grid_bdr_visible:
            box.add({
                "type": "rect",
                "x": box.x, "y": box.y,
                "w": box.w, "h": g.total_h,
                "fill": "transparent",
                "stroke": s.grid_bdr_color,
                "stroke_width": s.grid_bdr_width,
                "rx": 0,
            })

    # ── Badge helper ──────────────────────────────────────────────────────

    def _add_badge(
        self, box: RenderBox, bx: float, by: float, s: CompareStyle,
        *, number_text: str = "", icon_name: str = "",
    ) -> None:
        """Emit badge background shape + number or icon content."""
        size = s.topic_badge_size
        if s.topic_badge_shape == "circle":
            box.add({
                "type": "ellipse",
                "x": bx, "y": by, "w": size, "h": size,
                "fill": s.topic_badge_color,
                "stroke": "none", "stroke_width": 0,
            })
        elif s.topic_badge_shape == "square":
            box.add({
                "type": "rect",
                "x": bx, "y": by, "w": size, "h": size,
                "fill": s.topic_badge_color,
                "stroke": "none", "stroke_width": 0, "rx": 0,
            })
        # "none" → no background

        if number_text:
            box.add({
                "type": "text",
                "x": bx, "y": by, "w": size, "h": size,
                "text": number_text,
                "font_size": s.topic_badge_fs,
                "font_color": s.topic_badge_fc,
                "font_weight": "700",
                "alignment": "center",
                "vertical_align": "middle",
                "wrap": False,
            })
        elif icon_name:
            box.add({
                "type": "icon",
                "x": bx, "y": by, "w": size, "h": size,
                "name": icon_name,
                "font_family": s.icon_font_family,
                "font_size": size * 0.65,
                "color": s.topic_badge_fc,
            })
