"""UserStoryCard — structured field-grid card for user stories / feature cards.

Renders a set of labelled fields arranged in N columns (default: 2).
Each field has a bold label at the top of its cell and optional value text
below — matching the standard SAFe / agile user-story template layout.

The card header shows the story ID (as a distinct badge/chip) plus an
optional story title/summary.

Design anatomy
──────────────
  ┌──────────────────────────────────────────────────────────────────┐
  │ [US-042]  Title / Summary of the user story                      │  ← header
  │ ──────────────────────────────────────────────────────────────── │
  │ ┌────────────────────────────────┬─────────────────────────────┐ │
  │ │ Description:                   │ Benefit hypothesis:         │ │  ← tall field
  │ │ As a [user], I want to …       │                             │ │
  │ ├────────────────────────────────┼─────────────────────────────┤ │
  │ │ Nonfunctional requirements:    │ Acceptance criteria:        │ │  ← tall field
  │ │                                │                             │ │
  │ ├────────────────────────────────┼─────────────────────────────┤ │
  │ │ User business value:           │ Cost of delay:              │ │  ← compact rows
  │ ├────────────────────────────────┼─────────────────────────────┤ │
  │ │ Time criticality:              │ Job size:                   │ │
  │ ├────────────────────────────────┼─────────────────────────────┤ │
  │ │ Risk reduction / RROE value:   │ WSJF:                       │ │
  │ ├────────────────────────────────┴─────────────────────────────┤ │
  │ │ Notes:                                                        │ │  ← full-span
  │ └───────────────────────────────────────────────────────────────┘ │
  └──────────────────────────────────────────────────────────────────┘

Per-card props
──────────────
  id                  : string — story ID shown as badge in header      (e.g. "US-042")
  id-fill             : color — ID badge background                      default: primary
  id-text-color       : color — ID badge text                            default: on-primary
  title               : string — story summary/title next to the ID
  status              : string — optional status badge text               (e.g. "In Review")
  status-fill         : color — status badge background                   default: secondary
  n-cols              : int   — number of field columns (1–4)             default: 2
  fields              : list  — field objects  (required)
  placeholder-color   : color — text color when a field has no value     default: on-surface-variant/40
  label-color         : color — field label text color                    default: on-surface
  label-size          : int   — explicit px for field labels              default: auto
  value-color         : color — field value text color                    default: on-surface-variant
  value-size          : int   — explicit px for field values              default: auto
  cell-fill           : color — default cell background                   default: bg-card
  border-color        : color — grid line color                           default: border-default
  cell-pad            : int   — cell inner padding in px                  default: spacing("s")

Field object
────────────
  label           : bold heading at the top of the cell
  value           : content text below the label
  placeholder     : grey fallback text when value is absent
  span            : int — columns this field spans                        default: 1
  height          : float 0..1 = fraction of content-h  | int >1 = px    default: auto (equal)
  fill            : cell background override
  label-color     : per-field label color override
  value-color     : per-field value color override
  bold-value      : bool — bold weight for value text                     default: false
  align           : left | center | right                                 default: left
"""
from __future__ import annotations


class UserStoryCard:
    """Render a structured user-story card with a field grid."""

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

    def _bool_prop(self, props: dict, key: str, default: bool) -> bool:
        raw = str(props.get(key, "")).lower()
        if raw in ("true", "yes", "1"):  return True
        if raw in ("false", "no", "0"): return False
        return default

    # ── Field grid layout helpers ─────────────────────────────────────────────

    def _group_into_rows(self, fields: list, n_cols: int) -> list[list[tuple]]:
        """Group field dicts into rows based on `span`, yielding
        list of rows, each row = list of (field_dict, col_start, span_cols)."""
        rows: list[list[tuple]] = []
        row: list[tuple] = []
        col_cursor = 0

        for field in fields:
            if not isinstance(field, dict):
                field = {"label": str(field)}
            span = max(1, min(int(field.get("span", 1) or 1), n_cols))

            # Would overrun current row? → flush
            if col_cursor + span > n_cols and col_cursor > 0:
                rows.append(row)
                row        = []
                col_cursor = 0

            row.append((field, col_cursor, span))
            col_cursor += span

            # Full row? → flush
            if col_cursor >= n_cols:
                rows.append(row)
                row        = []
                col_cursor = 0

        if row:
            rows.append(row)

        return rows

    def _resolve_row_heights(self, rows: list, content_h: int) -> list[int]:
        """Compute px height per row respecting explicit height hints."""
        n = len(rows)
        if n == 0:
            return []
        heights: list[int | None] = []
        used = 0
        auto_count = 0

        for row in rows:
            # Take max explicit height from any field in the row
            max_h: int | None = None
            for (field, _, _) in row:
                raw = field.get("height", "")
                if raw == "" or raw is None:
                    continue
                try:
                    v = float(raw)
                    px = max(10, int(content_h * v)) if v <= 1.0 else max(10, int(v))
                    max_h = max(max_h, px) if max_h is not None else px
                except (ValueError, TypeError):
                    pass
            if max_h is None:
                heights.append(None)
                auto_count += 1
            else:
                heights.append(max_h)
                used += max_h

        auto_h = max(16, (content_h - used) // max(1, auto_count))
        return [h if h is not None else auto_h for h in heights]

    # ── Cell rendering ────────────────────────────────────────────────────────

    def _draw_field_cell(self, ctx,
                         cx: int, cy: int, cw: int, ch: int,
                         field: dict,
                         cell_fill: str, border_color: str, cell_pad: int,
                         global_label_color: str, global_value_color: str,
                         global_label_sz: int, global_value_sz: int,
                         placeholder_color: str) -> None:

        fill = self._rc(ctx, str(field.get("fill", "")), "") or cell_fill
        ctx.rect(cx, cy, cw, ch, fill=fill, stroke=border_color, radius=0)

        label_text  = str(field.get("label",       "")).strip()
        value_text  = str(field.get("value",       "")).strip()
        placeholder = str(field.get("placeholder", "")).strip()
        bold_value  = str(field.get("bold-value",  "false")).lower() not in ("false", "no", "0")
        align       = str(field.get("align",       "left")).strip().lower()
        if align not in ("left", "center", "right"):
            align = "left"

        f_label_color = self._rc(ctx, str(field.get("label-color", "")), "") or global_label_color
        f_value_color = self._rc(ctx, str(field.get("value-color", "")), "") or global_value_color

        inner_x = cx + cell_pad
        inner_w = max(4, cw - cell_pad * 2)
        inner_h = max(4, ch - cell_pad * 2)

        # Font sizes
        lsz = global_label_sz or max(9, min(14, int(inner_h * 0.22)))
        vsz = global_value_sz or max(8, min(13, int(inner_h * 0.18)))

        label_h = int(lsz * 1.55)
        gap     = max(2, int(inner_h * 0.06))
        value_h = max(4, inner_h - label_h - gap)

        iy = cy + cell_pad

        if label_text:
            ctx.text(inner_x, iy, inner_w, label_h,
                     label_text,
                     size=lsz, bold=True,
                     color=f_label_color,
                     align=align, valign="middle",
                     inner_margin=0)
        iy += label_h + gap

        content = value_text or placeholder
        if content:
            c_color = f_value_color if value_text else placeholder_color
            ctx.text(inner_x, iy, inner_w, value_h,
                     content,
                     size=vsz, bold=bold_value,
                     color=c_color,
                     align=align, valign="top",
                     inner_margin=0)

    # ── Main render ───────────────────────────────────────────────────────────

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:

        fields = list(props.get("fields") or [])
        if not fields:
            return

        n_cols = max(1, min(4, self._int_prop(props, "n-cols", 2)))

        # ── Card contract ─────────────────────────────────────────────────
        pad      = ctx.card_pad_px(w, h, props)
        inner_w  = w - pad * 2
        bg_color = ctx.card_bg_color(props, "bg-card")

        ctx.rect(x, y, w, h,
                 fill=bg_color,
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        GAP_XS = ctx.spacing("xs")   # 4
        GAP_S  = ctx.spacing("s")    # 8

        # ── Build header: ID badge + title + optional status badge ────────
        story_id     = str(props.get("id", props.get("story-id", ""))).strip()
        title        = str(props.get("title", "")).strip()
        status_text  = str(props.get("status", "")).strip()

        show_header  = bool(story_id or title)
        show_header  = show_header and ctx.card_section_enabled(props, "header", default=True)
        show_hdr_line = show_header and ctx.card_line_enabled(props, "header", default=True)

        id_fill      = self._rc(ctx, str(props.get("id-fill",       "")), "primary")
        id_tc        = self._rc(ctx, str(props.get("id-text-color",  "")), "on-primary")
        st_fill      = self._rc(ctx, str(props.get("status-fill",    "")), "secondary")
        st_tc        = self._rc(ctx, str(props.get("status-text-color", "")), "on-secondary")
        hdr_div_c    = ctx.card_line_color("header", ctx.color("line-default"), props)

        cy = y + pad

        if show_header:
            header_h   = ctx.card_header_h(w, h, props)
            header_gap = ctx.card_header_gap(h, props)

            id_badge_h = max(20, int(header_h * 0.80))
            id_sz      = max(9,  min(13, int(id_badge_h * 0.52)))
            id_badge_w = max(36, len(story_id) * id_sz + id_sz * 2) if story_id else 0
            id_r       = max(3, id_badge_h // 4)

            st_badge_w = 0
            if status_text:
                st_badge_w = max(40, len(status_text) * 9 + 16)

            # Left: ID badge
            if story_id:
                badge_y = cy + (header_h - id_badge_h) // 2
                ctx.badge(x + pad, badge_y, id_badge_w, id_badge_h,
                          story_id,
                          fill=id_fill, text_color=id_tc,
                          size=id_sz, radius=id_r)

            # Right: status badge
            if status_text:
                st_h    = max(18, int(header_h * 0.65))
                st_sz   = max(8, min(11, int(st_h * 0.52)))
                st_y    = cy + (header_h - st_h) // 2
                ctx.badge(x + w - pad - st_badge_w, st_y, st_badge_w, st_h,
                          status_text,
                          fill=st_fill, text_color=st_tc,
                          size=st_sz, radius=max(3, st_h // 4))

            # Centre: title text (between ID badge and status badge)
            if title:
                title_x = x + pad + (id_badge_w + GAP_S if story_id else 0)
                title_w = max(20, inner_w
                               - (id_badge_w + GAP_S if story_id else 0)
                               - (st_badge_w + GAP_S if status_text else 0))
                title_sz = ctx.card_header_font_size(title, title_w, h, props)
                title_color = ctx.card_title_color(props, default_token="text-default")
                ctx.text(title_x, cy, title_w, header_h,
                         title,
                         size=title_sz, bold=True,
                         color=title_color,
                         align="left", valign="middle")
            elif story_id and not title:
                # ID-only: draw larger with no badge, just prominent text
                pass  # badge already drawn above

            cy += header_h + header_gap
            if show_hdr_line:
                lx, lw = ctx.card_divider_span("header", x + pad, inner_w, props)
                ctx.divider(lx, cy, lw, color=hdr_div_c)
                cy += 1 + GAP_S

        # ── Content bounds ────────────────────────────────────────────────
        content_top    = cy
        content_bottom = y + h - pad
        content_h      = max(20, content_bottom - content_top)

        # ── Styling ───────────────────────────────────────────────────────
        cell_fill    = self._rc(ctx, str(props.get("cell-fill",    "")), "bg-card")
        border_color = self._rc(ctx, str(props.get("border-color", "")), "border-default")
        cell_pad     = self._int_prop(props, "cell-pad", GAP_S)

        global_label_color   = self._rc(ctx, str(props.get("label-color",       "")), "on-surface")
        global_value_color   = self._rc(ctx, str(props.get("value-color",       "")), "on-surface-variant")
        placeholder_color    = self._rc(ctx, str(props.get("placeholder-color", "")), "on-surface-variant")
        global_label_sz      = self._int_prop(props, "label-size", 0)
        global_value_sz      = self._int_prop(props, "value-size", 0)

        # ── Column widths (equal by default) ──────────────────────────────
        col_w = max(10, inner_w // n_cols)
        # Compute actual per-column start X positions
        col_x = [x + pad + i * col_w for i in range(n_cols)]
        # Last column absorbs rounding slack
        last_w = max(10, inner_w - col_w * (n_cols - 1))

        def _cw(col_start: int, span: int) -> int:
            if col_start + span >= n_cols:
                return sum(col_w for _ in range(n_cols - col_start - 1)) + last_w
            return col_w * span

        # ── Group fields into rows ────────────────────────────────────────
        rows = self._group_into_rows(fields, n_cols)
        row_heights = self._resolve_row_heights(rows, content_h)

        # ── Draw grid ─────────────────────────────────────────────────────
        ry = content_top

        for ri, (row, rh) in enumerate(zip(rows, row_heights)):
            for (field, col_start, span) in row:
                cx_cell = col_x[col_start]
                cw_cell = _cw(col_start, span)

                self._draw_field_cell(ctx,
                                      cx_cell, ry, cw_cell, rh,
                                      field,
                                      cell_fill=cell_fill,
                                      border_color=border_color,
                                      cell_pad=cell_pad,
                                      global_label_color=global_label_color,
                                      global_value_color=global_value_color,
                                      global_label_sz=global_label_sz,
                                      global_value_sz=global_value_sz,
                                      placeholder_color=placeholder_color)

            ry += rh
