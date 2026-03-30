"""TableCard — card-framed data table with optional header, alternating rows,
and optional total/summary row.

Uses the platform-native table primitive (PPTX: python-pptx add_table;
draw.io: mxTable/swimlane parent-child cells) so the result integrates
with the host application's own table tools (resizable columns, editable
cells, etc.).

Per-card overrides (all optional)
───────────────────────────────────
  title              : string  — card header title
  subtitle           : string  — card header subtitle (small, below title)
  columns            : list[{label, width, align}] — column definitions
  rows               : list[list|dict]             — data rows
  total              : list  — a single total/summary row
  has-header         : bool  — show column labels as styled header row  (default: true when columns have labels)
  alt-rows           : bool  — alternate row fill color                  (default: true)
  header-fill        : color — header row background                     (default: primary)
  header-text-color  : color — header row text                           (default: on-primary)
  row-fill           : color — even data row background                  (default: surface)
  alt-fill           : color — odd data row background                   (default: surface-variant)
  total-fill         : color — total row background                      (default: surface-variant)
  total-text-color   : color — total row text                            (default: on-surface)
  border-color       : color — cell border / grid lines                  (default: border-subtle)
  text-size          : int   — table body font size in pt                (default: ctx body)
  bold-header        : bool  — bold text in header row                   (default: true)
  bold-total         : bool  — bold text in total row                    (default: true)

Column definition fields
────────────────────────
  label   : string  — column header text
  width   : float   — relative width fraction (e.g. 0.3); auto-normalised across columns
  align   : string  — left | center | right                              (default: left)

Rows as lists
─────────────
  rows:
    - ["Value A", "12", "€ 9,600"]
    - ["Value B", "8",  "€ 6,400"]

Rows as dicts (key = column label)
───────────────────────────────────
  rows:
    - Component: "Frontend"
      Days: "15"
      Cost: "€ 12,000"
"""
from __future__ import annotations


class TableCard:
    """Render a card-framed data table using ctx.native_table()."""

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _resolve_color(self, ctx, raw: str, fallback: str) -> str:
        raw = (raw or "").strip()
        if not raw:
            return ctx.color(fallback)
        return raw if raw.startswith("#") else ctx.color(raw)

    def _parse_columns(self, raw_columns, data_rows: list) -> list[dict]:
        """Normalize column definitions. Auto-generate from data if absent."""
        if raw_columns:
            out = []
            for col in raw_columns:
                if isinstance(col, dict):
                    out.append({
                        "label":      str(col.get("label", col.get("name", ""))),
                        "width_frac": float(col.get("width", col.get("width_frac", 1.0))),
                        "align":      str(col.get("align", "left")).strip().lower(),
                    })
                elif isinstance(col, str):
                    out.append({"label": col, "width_frac": 1.0, "align": "left"})
            return out if out else [{"label": "", "width_frac": 1.0, "align": "left"}]
        # Auto-generate from first row width
        if data_rows and isinstance(data_rows[0], (list, tuple)):
            n = len(data_rows[0])
            return [{"label": "", "width_frac": 1.0, "align": "left"}] * n
        return [{"label": "", "width_frac": 1.0, "align": "left"}]

    def _parse_rows(self, raw_rows, columns: list[dict]) -> list[list[str]]:
        """Normalize rows to list[list[str]]. Handles lists and dicts."""
        if not raw_rows:
            return []
        out = []
        col_labels = [c["label"] for c in columns]
        for row in raw_rows:
            if isinstance(row, (list, tuple)):
                out.append([str(v) for v in row])
            elif isinstance(row, dict):
                # Map by column label; fall back to positional order
                if any(lbl in row for lbl in col_labels):
                    out.append([str(row.get(lbl, "")) for lbl in col_labels])
                else:
                    out.append([str(v) for v in row.values()])
            else:
                out.append([str(row)])
        return out

    # ── Main render ───────────────────────────────────────────────────────────

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:

        # ── Card contract ─────────────────────────────────────────────────
        pad     = ctx.card_pad_px(w, h, props)
        inner_w = w - pad * 2
        title   = str(props.get("title", ""))
        subtitle = str(props.get("subtitle", ""))

        show_header      = bool(title or subtitle) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)

        title_color   = ctx.card_title_color(props, default_token="text-default")
        header_align  = ctx.card_header_align(props, default="left")
        divider_color = ctx.card_line_color("header", ctx.color("line-default"), props)
        bg_color      = ctx.card_bg_color(props, "bg-card")

        # ── Card frame ────────────────────────────────────────────────────
        ctx.rect(x, y, w, h,
                 fill=bg_color,
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        GAP_S  = ctx.spacing("s")
        GAP_XS = ctx.spacing("xs")

        cy = y + pad

        # ── Header ────────────────────────────────────────────────────────
        if show_header:
            header_h   = ctx.card_header_h(w, h, props)
            header_gap = ctx.card_header_gap(h, props)
            title_size = ctx.card_header_font_size(title, inner_w, h, props)
            ctx.text(x + pad, cy, inner_w, header_h,
                     title,
                     size=title_size, bold=True,
                     color=title_color,
                     align=header_align, valign="middle")
            cy += header_h + header_gap

            if subtitle:
                sub_sz = ctx.font_size("caption")
                sub_h  = max(16, int(sub_sz * 1.5))
                ctx.text(x + pad, cy, inner_w, sub_h,
                         subtitle,
                         size=sub_sz, bold=False,
                         color=ctx.card_subtitle_color(props),
                         align=header_align, valign="top")
                cy += sub_h + GAP_XS

            if show_header_line:
                lx, lw = ctx.card_divider_span("header", x + pad, inner_w, props)
                ctx.divider(lx, cy, lw, color=divider_color)
                cy += 1 + GAP_S

        # ── Parse table data ──────────────────────────────────────────────
        raw_columns = props.get("columns") or []
        raw_rows    = props.get("rows") or []
        raw_total   = props.get("total")

        # Normalize total to a single extra row
        if raw_total is not None:
            if isinstance(raw_total, (list, tuple)):
                # Could be [[...]] or [...]
                if raw_total and isinstance(raw_total[0], (list, tuple)):
                    total_rows = [list(raw_total[0])]
                else:
                    total_rows = [list(raw_total)]
            elif isinstance(raw_total, dict):
                total_rows = [list(raw_total.values())]
            else:
                total_rows = [[str(raw_total)]]
        else:
            total_rows = []

        data_rows_all = list(raw_rows) + total_rows
        has_total     = bool(total_rows)

        columns   = self._parse_columns(raw_columns, data_rows_all)
        data_rows = self._parse_rows(data_rows_all, columns)

        # Decide whether to render a header row
        any_label  = any(c["label"] for c in columns)
        has_header = bool(props.get("has-header",
                                    "true" if any_label else "false") in
                          (True, "true", "yes", "1", 1)) if any_label else False

        if not data_rows and not has_header:
            return

        # ── Table color props ─────────────────────────────────────────────
        alt_rows = str(props.get("alt-rows", "true")).lower() not in ("false", "no", "0")

        header_fill       = self._resolve_color(ctx, str(props.get("header-fill", "")),       "primary")
        header_text_color = self._resolve_color(ctx, str(props.get("header-text-color", "")), "on-primary")
        row_fill          = self._resolve_color(ctx, str(props.get("row-fill", "")),           "surface")
        alt_fill_c        = (self._resolve_color(ctx, str(props.get("alt-fill", "")), "surface-variant")
                             if alt_rows else row_fill)
        total_fill        = self._resolve_color(ctx, str(props.get("total-fill", "")),         "surface-variant")
        total_text_color  = self._resolve_color(ctx, str(props.get("total-text-color", "")),   "on-surface")
        border_color      = self._resolve_color(ctx, str(props.get("border-color", "")),       "border-subtle")
        bold_header       = str(props.get("bold-header", "true")).lower() not in ("false", "no", "0")
        bold_total        = str(props.get("bold-total",  "true")).lower() not in ("false", "no", "0")

        raw_sz   = props.get("text-size", "")
        text_sz  = None
        if raw_sz:
            try:
                text_sz = max(8, int(raw_sz))
            except (ValueError, TypeError):
                pass

        # ── Table area ────────────────────────────────────────────────────
        table_x = x + pad
        table_y = cy
        table_w = inner_w
        table_h = max(20, y + h - pad - cy)

        ctx.native_table(
            table_x, table_y, table_w, table_h,
            columns       = columns,
            data_rows     = data_rows,
            has_header    = has_header,
            has_total     = has_total,
            header_fill       = header_fill,
            header_text_color = header_text_color,
            row_fill          = row_fill,
            alt_fill          = alt_fill_c,
            total_fill        = total_fill,
            total_text_color  = total_text_color,
            border_color      = border_color,
            text_size         = text_sz,
            bold_header       = bold_header,
            bold_total        = bold_total,
        )
