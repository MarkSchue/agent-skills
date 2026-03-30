"""GridCard — flexible matrix grid with row-label column, column headers, cell
spanning, and per-cell customisation.

Design anatomy
──────────────
  ┌──────────────────────────────────────────────────────────────────┐
  │  [Optional card title header]                                    │
  │  ┌──────┬──────────────────┬──────────────┬───────────────────┐  │
  │  │      │  Column header   │  Col header  │   Col header      │  │  ← optional column headers
  │  │      │  Subtitle        │  Subtitle    │   Subtitle        │  │
  │  │      │  [badge]         │  [badge]     │   [badge]         │  │
  │  ├──────┼──────────────────┴──────────────┴───────────────────┤  │
  │  │ R1   │  Cell spanning 3 columns (span: 3)                  │  │
  │  ├──────┼──────────────────┬──────────────┬───────────────────┤  │
  │  │ R2   │  Cell text       │  Cell text   │   Cell text       │  │
  │  ├──────┼──────────────────┼──────────────┼───────────────────┤  │
  │  │ R3   │  Tall row        │  with        │   taller content  │  │  ← auto row height
  │  └──────┴──────────────────┴──────────────┴───────────────────┘  │
  └──────────────────────────────────────────────────────────────────┘

Column / row label column
──────────────────────────
  label-col-width       : 0..1 fraction of inner width         default: 0.14
                          Set to 0 to disable the label column entirely
  label-col-fill        : background for row label cells        default: primary
  label-col-text-color  : text color in row labels              default: on-primary
  label-col-align       : text alignment of row labels          default: center

Column headers (each item in ``columns``)
──────────────────────────────────────────
  label         : column header title  (bold)
  subtitle      : small secondary text below the title
  badge         : small filled pill at the bottom of the header cell
  width         : 0..1 fraction of content width (with fractions auto-normalised)
  fill          : per-column header background override
  text-color    : per-column header text override

Row object (each item in ``rows``)
────────────────────────────────────
  label         : row label text (first column)
  label-fill    : per-row label fill override
  label-color   : per-row label text color override
  height        : int>1 = explicit px  |  0<float≤1 = fraction of content h
  cells         : list of cell objects

Cell object
────────────
  text          : main text
  bold          : bool — make text bold                         default: false
  subtitle      : smaller secondary line below text
  badge         : small pill label inside the cell
  badge-fill    : badge background                              default: on-surface
  badge-text-color: badge text                                  default: surface
  span          : int — how many columns this cell covers       default: 1
  fill          : cell background override
  text-color    : cell text color override
  align         : left | center | right                         default: left
  valign        : top | middle | bottom                         default: middle

Card-level props
─────────────────
  title                 : card header title
  columns               : list of column header objects (optional)
  rows                  : list of row objects              (required)
  label-col-width       : see above                              default: 0.14
  label-col-fill        : see above                             default: primary
  label-col-text-color  : see above                             default: on-primary
  label-col-align       : center | left | right                 default: center
  col-header-fill       : column header row background          default: surface-variant
  col-header-text-color : column header text                    default: on-surface
  col-header-height     : explicit px for header row            default: auto
  cell-fill             : default cell background               default: bg-card
  cell-text-color       : default cell text                     default: on-surface
  cell-pad              : inner padding in px                   default: spacing("s")
  border-color          : cell border                           default: border-default
  border-radius         : corner radius for cells               default: 0
  badge-fill            : default badge fill in col-headers/cells default: on-surface
  badge-text-color      : default badge text                    default: surface
"""
from __future__ import annotations
import math


class GridCard:
    """Render a customisable matrix grid with optional row labels, column
    headers, and per-cell content spanning."""

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _rc(self, ctx, raw: str, fallback: str) -> str:
        raw = (raw or "").strip()
        if not raw:
            return ctx.color(fallback)
        return raw if raw.startswith("#") else ctx.color(raw)

    def _int_prop(self, props: dict, key: str, default: int) -> int:
        v = props.get(key, "")
        try:
            return max(0, int(v))
        except (ValueError, TypeError):
            return default

    def _float_prop(self, props: dict, key: str, default: float) -> float:
        v = props.get(key, "")
        try:
            return float(v)
        except (ValueError, TypeError):
            return default

    def _col_widths(self, columns: list, total_w: int) -> list[int]:
        """Compute pixel widths for each content column."""
        n = len(columns)
        if n == 0:
            return []
        fracs = []
        for col in columns:
            w_raw = col.get("width", "")
            try:
                fracs.append(max(0.0, float(w_raw)))
            except (ValueError, TypeError):
                fracs.append(0.0)
        total_frac = sum(fracs)
        if total_frac <= 0:
            # equal division
            fracs = [1.0 / n] * n
        else:
            fracs = [f / total_frac for f in fracs]
        widths = [max(8, int(total_w * f)) for f in fracs]
        # Adjust last column to consume rounding remainder
        widths[-1] = max(8, total_w - sum(widths[:-1]))
        return widths

    def _row_heights(self, rows: list, total_h: int, n_rows: int) -> list[int]:
        """Compute pixel height for each row, respecting explicit heights."""
        if n_rows == 0:
            return []
        heights: list[int | None] = []
        used = 0
        auto_count = 0
        for row in rows:
            if not isinstance(row, dict):
                row = {}
            h_raw = row.get("height", "")
            if h_raw == "" or h_raw is None:
                heights.append(None)
                auto_count += 1
            else:
                try:
                    v = float(h_raw)
                    if v > 1:  # treat as px
                        px = max(10, int(v))
                    else:      # treat as fraction
                        px = max(10, int(total_h * v))
                    heights.append(px)
                    used += px
                except (ValueError, TypeError):
                    heights.append(None)
                    auto_count += 1
        auto_h = max(10, (total_h - used) // max(1, auto_count))
        return [h if h is not None else auto_h for h in heights]

    def _cell_span_width(self, col_idx: int, span: int,
                         col_xs: list[int], total_content_x: int,
                         total_content_w: int) -> int:
        """Width in px for a cell starting at col_idx spanning `span` columns."""
        n = len(col_xs)
        end_idx = min(col_idx + span, n)
        if end_idx < n:
            return col_xs[end_idx] - col_xs[col_idx]
        else:
            return (total_content_x + total_content_w) - col_xs[col_idx]

    def _draw_cell(self, ctx,
                   cx: int, cy: int, cw: int, ch: int,
                   cell: dict,
                   fill: str, text_color: str, border_color: str,
                   cell_pad: int, border_radius: int,
                   default_align: str = "left",
                   default_valign: str = "middle",
                   badge_fill: str = "", badge_text_color: str = "") -> None:
        """Draw a single cell: background, optional badge, text + subtitle."""

        # Cell background + border
        c_fill      = self._rc(ctx, str(cell.get("fill", "")),       "") or fill
        c_tc        = self._rc(ctx, str(cell.get("text-color", "")), "") or text_color
        c_align     = str(cell.get("align",  default_align)).strip().lower()
        c_valign    = str(cell.get("valign", default_valign)).strip().lower()
        if c_align  not in ("left", "center", "right"):  c_align  = default_align
        if c_valign not in ("top",  "middle",  "bottom"): c_valign = default_valign

        ctx.rect(cx, cy, cw, ch, fill=c_fill, stroke=border_color, radius=border_radius)

        text_str    = str(cell.get("text",     "")).strip()
        is_bold     = str(cell.get("bold",     "false")).lower() not in ("false", "no", "0")
        subtitle    = str(cell.get("subtitle", "")).strip()
        badge_str   = str(cell.get("badge",    "")).strip()
        b_fill      = self._rc(ctx, str(cell.get("badge-fill",       "")), "") or badge_fill
        b_tc        = self._rc(ctx, str(cell.get("badge-text-color", "")), "") or badge_text_color

        inner_x = cx + cell_pad
        inner_w = max(4, cw - cell_pad * 2)
        inner_h = max(4, ch - cell_pad * 2)

        text_sz     = max(9,  min(16, int(inner_h * 0.28)))
        subtitle_sz = max(8,  min(12, int(inner_h * 0.18)))
        badge_sz    = max(8,  min(11, int(inner_h * 0.16)))
        badge_h     = badge_sz + 6

        # Compute occupied heights for vertical layout
        has_subtitle = bool(subtitle)
        has_badge    = bool(badge_str)

        text_line_h  = int(text_sz * 1.4)
        sub_line_h   = (int(subtitle_sz * 1.4) + 2) if has_subtitle else 0
        badge_zone_h = (badge_h + 4) if has_badge else 0
        stack_h      = text_line_h + sub_line_h + badge_zone_h

        # Vertical centering
        if c_valign == "middle":
            ty = cy + cell_pad + max(0, (inner_h - stack_h) // 2)
        elif c_valign == "bottom":
            ty = cy + ch - cell_pad - stack_h
        else:
            ty = cy + cell_pad

        if text_str:
            ctx.text(inner_x, ty, inner_w, text_line_h,
                     text_str, size=text_sz, bold=is_bold,
                     color=c_tc, align=c_align, valign="top", inner_margin=0)
        ty += text_line_h

        if has_subtitle:
            ctx.text(inner_x, ty, inner_w, sub_line_h,
                     subtitle, size=subtitle_sz, bold=False,
                     color=c_tc, align=c_align, valign="top", inner_margin=0)
            ty += sub_line_h

        if has_badge and b_fill:
            badge_w = min(inner_w, max(30, int(inner_w * 0.7)))
            bx = inner_x
            if c_align == "center":
                bx = cx + (cw - badge_w) // 2
            elif c_align == "right":
                bx = cx + cw - cell_pad - badge_w
            ctx.badge(bx, ty + 2, badge_w, badge_h,
                      badge_str, fill=b_fill,
                      text_color=b_tc or ctx.color("surface"),
                      size=badge_sz,
                      radius=max(3, badge_h // 3))

    # ── Main render ───────────────────────────────────────────────────────────

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:

        rows_raw = list(props.get("rows") or [])
        if not rows_raw:
            return

        columns_raw = list(props.get("columns") or [])

        # ── Card contract ─────────────────────────────────────────────────
        pad     = ctx.card_pad_px(w, h, props)
        inner_w = w - pad * 2
        title   = str(props.get("title", ""))

        show_header      = bool(title) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)
        title_color      = ctx.card_title_color(props, default_token="text-default")
        header_align     = ctx.card_header_align(props, default="left")
        hdr_div_c        = ctx.card_line_color("header", ctx.color("line-default"), props)
        bg_color         = ctx.card_bg_color(props, "bg-card")

        ctx.rect(x, y, w, h,
                 fill=bg_color,
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        GAP_S = ctx.spacing("s")   # 8 px

        cy = y + pad

        if show_header:
            hh   = ctx.card_header_h(w, h, props)
            hgap = ctx.card_header_gap(h, props)
            tsz  = ctx.card_header_font_size(title, inner_w, h, props)
            ctx.text(x + pad, cy, inner_w, hh,
                     title, size=tsz, bold=True,
                     color=title_color, align=header_align, valign="middle")
            cy += hh + hgap
            if show_header_line:
                lx, lw = ctx.card_divider_span("header", x + pad, inner_w, props)
                ctx.divider(lx, cy, lw, color=hdr_div_c)
                cy += 1 + GAP_S

        # ── Content bounds ────────────────────────────────────────────────
        content_top    = cy
        content_bottom = y + h - pad
        content_h      = max(20, content_bottom - content_top)

        # ── Column layout ─────────────────────────────────────────────────
        label_col_frac = self._float_prop(props, "label-col-width", 0.14)
        label_col_frac = max(0.0, min(0.50, label_col_frac))
        has_label_col  = label_col_frac > 0.0

        label_col_w  = int(inner_w * label_col_frac) if has_label_col else 0
        content_zone_w = inner_w - label_col_w

        lbl_fill      = self._rc(ctx, str(props.get("label-col-fill",       "")), "primary")
        lbl_tc        = self._rc(ctx, str(props.get("label-col-text-color", "")), "on-primary")
        lbl_align     = str(props.get("label-col-align", "center")).strip().lower()
        if lbl_align not in ("left", "center", "right"):
            lbl_align = "center"

        # Content column widths  
        n_content_cols = max(1, len(columns_raw)) if columns_raw else 1
        # If no column definitions but cells exist, infer from max cells in any row
        if not columns_raw:
            for row in rows_raw:
                if isinstance(row, dict):
                    cells = row.get("cells", [])
                    count = sum(int((c.get("span", 1) if isinstance(c, dict) else 1)) for c in cells)
                    n_content_cols = max(n_content_cols, count)
            columns_raw = [{}] * n_content_cols

        n_content_cols = len(columns_raw)
        col_widths     = self._col_widths(columns_raw, content_zone_w)

        # Pre-compute cumulative X positions for each column (relative to content zone start)
        content_x  = x + pad + label_col_w
        col_xs: list[int] = []
        cx_acc = content_x
        for cw_i in col_widths:
            col_xs.append(cx_acc)
            cx_acc += cw_i

        # ── Cell styling defaults ─────────────────────────────────────────
        col_hdr_fill   = self._rc(ctx, str(props.get("col-header-fill",       "")), "surface-variant")
        col_hdr_tc     = self._rc(ctx, str(props.get("col-header-text-color", "")), "on-surface")
        cell_fill      = self._rc(ctx, str(props.get("cell-fill",             "")), "bg-card")
        cell_tc        = self._rc(ctx, str(props.get("cell-text-color",       "")), "on-surface")
        border_color   = self._rc(ctx, str(props.get("border-color",          "")), "border-default")
        border_radius  = self._int_prop(props, "border-radius", 0)
        cell_pad       = self._int_prop(props, "cell-pad", GAP_S)
        badge_fill     = self._rc(ctx, str(props.get("badge-fill",            "")), "on-surface")
        badge_tc       = self._rc(ctx, str(props.get("badge-text-color",      "")), "surface")

        # ── Column header row ─────────────────────────────────────────────
        has_col_header = any(
            (isinstance(col, dict) and (col.get("label") or col.get("subtitle") or col.get("badge")))
            for col in columns_raw
        )
        if has_col_header:
            raw_chh       = props.get("col-header-height", "")
            auto_chh      = max(40, int(content_h * 0.20))
            try:
                col_hdr_h = max(20, int(raw_chh)) if str(raw_chh).strip() else auto_chh
            except (ValueError, TypeError):
                col_hdr_h = auto_chh
        else:
            col_hdr_h = 0

        # ── Row heights (data rows only) ──────────────────────────────────
        data_h         = content_h - col_hdr_h
        row_heights    = self._row_heights(rows_raw, data_h, len(rows_raw))

        # ── Draw column headers ───────────────────────────────────────────
        if has_col_header:
            # Corner cell (above label column)
            if has_label_col:
                ctx.rect(x + pad, content_top, label_col_w, col_hdr_h,
                         fill=lbl_fill, stroke=border_color, radius=border_radius)

            for ci, col in enumerate(columns_raw):
                if not isinstance(col, dict):
                    col = {}
                hdr_fill = self._rc(ctx, str(col.get("fill", "")), "") or col_hdr_fill
                hdr_tc   = self._rc(ctx, str(col.get("text-color", "")), "") or col_hdr_tc
                self._draw_cell(ctx,
                                col_xs[ci], content_top,
                                col_widths[ci], col_hdr_h,
                                col, fill=hdr_fill, text_color=hdr_tc,
                                border_color=border_color,
                                cell_pad=cell_pad, border_radius=border_radius,
                                default_align="center", default_valign="middle",
                                badge_fill=badge_fill, badge_text_color=badge_tc)

        # ── Draw data rows ────────────────────────────────────────────────
        ry = content_top + col_hdr_h

        for ri, row in enumerate(rows_raw):
            if not isinstance(row, dict):
                row = {"cells": [{"text": str(row)}]}

            rh = row_heights[ri]

            # Row label cell
            if has_label_col:
                label_text  = str(row.get("label", "")).strip()
                row_lbl_fill = self._rc(ctx, str(row.get("label-fill",  "")), "") or lbl_fill
                row_lbl_tc   = self._rc(ctx, str(row.get("label-color", "")), "") or lbl_tc
                ctx.rect(x + pad, ry, label_col_w, rh,
                         fill=row_lbl_fill, stroke=border_color, radius=border_radius)
                if label_text:
                    txt_sz = max(9, min(16, int(rh * 0.22)))
                    ctx.text(x + pad + cell_pad, ry,
                             label_col_w - cell_pad * 2, rh,
                             label_text,
                             size=txt_sz, bold=True,
                             color=row_lbl_tc,
                             align=lbl_align, valign="middle",
                             inner_margin=0)

            # Data cells — walk left to right, track current column index
            cells       = list(row.get("cells") or [])
            col_cursor  = 0

            for cell in cells:
                if col_cursor >= n_content_cols:
                    break
                if not isinstance(cell, dict):
                    cell = {"text": str(cell)}

                span    = max(1, min(int(cell.get("span", 1) or 1),
                                     n_content_cols - col_cursor))
                cw_span = self._cell_span_width(col_cursor, span,
                                                col_xs, content_x, content_zone_w)
                self._draw_cell(ctx,
                                col_xs[col_cursor], ry,
                                cw_span, rh,
                                cell,
                                fill=cell_fill, text_color=cell_tc,
                                border_color=border_color,
                                cell_pad=cell_pad, border_radius=border_radius,
                                default_align="left", default_valign="middle",
                                badge_fill=badge_fill, badge_text_color=badge_tc)
                col_cursor += span

            # Fill any remaining columns with empty cells to complete grid borders
            while col_cursor < n_content_cols:
                ctx.rect(col_xs[col_cursor], ry,
                         col_widths[col_cursor], rh,
                         fill=cell_fill, stroke=border_color, radius=border_radius)
                col_cursor += 1

            ry += rh
