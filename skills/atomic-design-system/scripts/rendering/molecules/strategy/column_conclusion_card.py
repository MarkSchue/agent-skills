"""ColumnConclusionCard — 2–5 equal columns with optional icon, metric, headline,
body text, and a full-width conclusion zone below a decorated divider.

Design anatomy
──────────────
  ┌──────────────────────────────────────────────────────────────────┐
  │  [Optional title header]                                         │
  │                                                                  │
  │   ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
  │   │  [icon]  │  │  [icon]  │  │  [icon]  │   ← optional         │
  │   │  00 %    │  │  00 %    │  │  00 %    │   ← optional metric  │
  │   │  Bold    │  │  Bold    │  │  Bold    │   ← headline         │
  │   │  Headline│  │  Headline│  │  Headline│                      │
  │   │  Body    │  │  Body    │  │  Body    │   ← body text        │
  │   │  text…   │  │  text…   │  │  text…   │                      │
  │   └──────────┘  └──────────┘  └──────────┘                      │
  │  ─────────────────────[∨]─────────────────────  ← divider+chev. │
  │       Lorem ipsum dolor sit amet — conclusion text               │
  └──────────────────────────────────────────────────────────────────┘

Per-card overrides (all optional)
───────────────────────────────────
  title              : card header title
  columns            : list of 2–5 column objects (see below)
  text-align         : center | left | right — all column content   default: center
  value-color        : global metric/value color token              default: primary
  value-size         : explicit font size (px) for all metrics      default: auto
  icon-size          : explicit icon size (px)                      default: auto
  icon-color         : global icon color                            default: on-surface-variant
  conclusion         : full-width bold text below divider           default: ""
  conclusion-color   : color for conclusion text                    default: on-surface
  conclusion-size    : font size (px) for conclusion box             default: auto
  conclusion-bold    : bool — bold conclusion text                  default: true
  conclusion-align   : left | center | right for conclusion         default: center
  show-divider       : bool — full-width line above conclusion       default: true
  show-chevron       : bool — chevron on the divider                default: true (if conclusion)
  chevron-color      : color for chevron                            default: on-surface-variant
  column-gap         : gap between columns in px                    default: auto

Per-column fields
─────────────────
  icon        : string  — icon description / emoji (optional)
  value       : string  — large metric or number (e.g. "87", "12.4 M")
  value-unit  : string  — appended to value (e.g. "%", "€")
  headline    : string  — bold text (required for useful output)
  body        : string  — supporting text
  color       : color   — per-column override for value + icon accent
"""
from __future__ import annotations
import math


class ColumnConclusionCard:
    """Render a column-conclusion card with 2–5 columns and optional conclusion row."""

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _rc(self, ctx, raw, fallback: str) -> str:
        raw = (raw or "").strip()
        if not raw:
            return ctx.color(fallback)
        return raw if raw.startswith("#") else ctx.color(raw)

    def _draw_chevron(self, ctx, cx: int, cy: int, sz: int, color: str) -> None:
        """Draw a downward-pointing chevron centred at (cx, cy) using the
        icon system so it renders identically in PPTX and draw.io."""
        icon_w = sz * 2
        icon_h = sz * 2
        icon_x = cx - sz
        icon_y = cy - sz
        ctx.draw_icon(icon_x, icon_y, icon_w, icon_h, "arrow_downward", color=color)

    # ── Main render ───────────────────────────────────────────────────────────

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:

        cols_raw = list(props.get("columns") or [])[:5]
        if not cols_raw:
            return
        n = max(2, len(cols_raw))

        # ── Card contract ─────────────────────────────────────────────────
        pad        = ctx.card_pad_px(w, h, props)
        inner_w    = w - pad * 2
        title      = str(props.get("title", ""))

        show_header      = bool(title) and ctx.card_section_enabled(props, "title", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "title", default=True)

        title_color   = ctx.card_title_color(props, default_token="text-default")
        header_align  = ctx.card_title_align(props, default="left")
        div_color     = ctx.card_line_color("title", ctx.color("line-default"), props)
        bg_color      = ctx.card_bg_color(props, "bg-card")

        # ── Card frame ────────────────────────────────────────────────────
        ctx.rect(x, y, w, h,
                 fill=bg_color,
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        GAP_XS = ctx.spacing("xs")
        GAP_S  = ctx.spacing("s")
        GAP_M  = ctx.spacing("m")

        cy = y + pad

        # ── Optional title header ─────────────────────────────────────────
        if show_header:
            header_h   = ctx.card_title_h(w, h, props)
            header_gap = ctx.card_title_gap(h, props)
            title_size = ctx.card_title_font_size(title, inner_w, h, props)
            ctx.text(x + pad, cy, inner_w, header_h,
                     title, size=title_size, bold=True,
                     color=title_color, align=header_align, valign="middle")
            cy += header_h + header_gap
            if show_header_line:
                lx, lw = ctx.card_divider_span("title", x + pad, inner_w, props)
                ctx.divider(lx, cy, lw, color=div_color)
                cy += 1 + GAP_S

        # ── Content area bounds ───────────────────────────────────────────
        content_top    = cy
        content_bottom = y + h - pad
        content_h      = max(20, content_bottom - content_top)

        # ── Conclusion zone allocation ────────────────────────────────────
        # takeaway is canonical; conclusion is kept as backward-compat alias
        conclusion     = str(props.get("takeaway") or props.get("conclusion") or "").strip()
        show_conc_div  = str(props.get("show-divider", "true")).lower() != "false"
        show_chevron   = (str(props.get("show-chevron", "true")).lower() != "false"
                          and bool(conclusion))

        conc_zone_h = 0
        if conclusion:
            conc_sz    = ctx.slide_font_size("body", props)
            raw_csz    = props.get("conclusion-size", "")
            if raw_csz:
                try:
                    conc_sz = max(8, int(raw_csz))
                except (ValueError, TypeError):
                    pass
            # allocate: divider+chevron row + text lines
            chevron_row_h = GAP_M + (GAP_M if show_chevron else 0)
            text_lines    = max(1, len(conclusion) // max(1, inner_w // max(1, conc_sz)) + 1)
            text_lines    = min(text_lines, 3)
            conc_text_h   = int(conc_sz * 1.5) * text_lines
            conc_zone_h   = chevron_row_h + conc_text_h + GAP_S

        col_zone_bottom = content_bottom - conc_zone_h
        col_zone_h      = max(20, col_zone_bottom - content_top)

        # ── Column layout ─────────────────────────────────────────────────
        raw_gap  = props.get("column-gap", "")
        col_gap  = GAP_M
        if raw_gap:
            try:
                col_gap = max(0, int(raw_gap))
            except (ValueError, TypeError):
                pass
        col_w    = max(20, (inner_w - col_gap * (n - 1)) // n)

        # Global props
        text_align   = str(props.get("text-align", "center")).strip().lower()
        if text_align not in ("left", "center", "right"):
            text_align = "center"

        # Vertical alignment for the column content stack.
        # Controls both where the stack is anchored (top/middle/bottom) and
        # the valign used inside each text box.
        col_valign = str(props.get("col-valign") or props.get("col_valign") or "middle").strip().lower()
        if col_valign not in ("top", "middle", "bottom"):
            col_valign = "middle"

        raw_val_sz   = props.get("value-size", "")
        global_val_sz = 0
        if raw_val_sz:
            try:
                global_val_sz = max(10, int(raw_val_sz))
            except (ValueError, TypeError):
                pass

        raw_icon_sz  = props.get("icon-size", "")
        global_icon_sz = 0
        if raw_icon_sz:
            try:
                global_icon_sz = max(12, int(raw_icon_sz))
            except (ValueError, TypeError):
                pass

        global_val_color  = self._rc(ctx, str(props.get("value-color",  "")), "primary")
        global_icon_color = self._rc(ctx, str(props.get("icon-color",   "")), "on-surface-variant")

        headline_sz = max(10, min(22, int(col_w * 0.10 + 4)))
        body_sz     = ctx.slide_font_size("body", props)

        # Auto value size: number only — unit is rendered as a separate smaller label below
        auto_val_sz = max(16, min(28, int(min(col_w * 0.24, col_zone_h * 0.18))))

        # Auto icon size
        auto_icon_sz = ctx.icon_size(col_w, col_zone_h, props)

        # ── Pass 1: collect per-column data + zone heights ─────────────────
        col_data = []
        for col in cols_raw:
            if not isinstance(col, dict):
                col = {"headline": str(col)}

            icon_str   = str(col.get("icon", "")).strip()
            value_str  = str(col.get("value", "")).strip()
            value_unit = str(col.get("value-unit", "")).strip()
            headline   = str(col.get("headline", "")).strip()
            body_text  = str(col.get("body", "")).strip()

            col_color_raw  = str(col.get("color", "")).strip()
            col_val_color  = (self._rc(ctx, col_color_raw, "primary")
                              if col_color_raw else global_val_color)
            col_icon_color = (self._rc(ctx, col_color_raw, "on-surface-variant")
                              if col_color_raw else global_icon_color)

            icon_sz = global_icon_sz or auto_icon_sz
            val_sz  = global_val_sz  or auto_val_sz
            unit_sz = max(10, int(val_sz * 0.55))

            has_icon  = bool(icon_str)
            has_value = bool(value_str)
            has_unit  = has_value and bool(value_unit)

            icon_zone_h  = (icon_sz + GAP_S)              if has_icon  else 0
            value_zone_h = (int(val_sz  * 1.35) + GAP_XS) if has_value else 0
            unit_zone_h  = (int(unit_sz * 1.30) + GAP_XS) if has_unit  else 0
            hl_raw_h     = (int(headline_sz * 1.5)
                            * max(1, len(headline) // max(1, col_w // max(1, headline_sz)) + 1))
            hl_raw_h     = min(hl_raw_h, int(col_zone_h * 0.35))
            headline_zone_h = max(int(headline_sz * 1.5), hl_raw_h) if headline else 0

            col_data.append(dict(
                icon_str=icon_str, value_str=value_str, value_unit=value_unit,
                headline=headline, body_text=body_text,
                col_val_color=col_val_color, col_icon_color=col_icon_color,
                icon_sz=icon_sz, val_sz=val_sz, unit_sz=unit_sz,
                has_icon=has_icon, has_value=has_value, has_unit=has_unit,
                icon_zone_h=icon_zone_h, value_zone_h=value_zone_h,
                unit_zone_h=unit_zone_h, headline_zone_h=headline_zone_h,
            ))

        # ── Zone maxima → every column shares the same vertical grid ───────
        max_icon_h      = max(d["icon_zone_h"]     for d in col_data)
        max_value_h     = max(d["value_zone_h"]    for d in col_data)
        max_unit_h      = max(d["unit_zone_h"]     for d in col_data)
        max_headline_h  = max(d["headline_zone_h"] for d in col_data)
        fixed_used      = max_icon_h + max_value_h + max_unit_h + max_headline_h
        body_zone_h     = max(0, col_zone_h - fixed_used - GAP_S * 2)
        total_aligned_h = fixed_used + (body_zone_h if any(d["body_text"] for d in col_data) else 0)

        # Anchor the whole aligned block once (shared by all columns)
        if col_valign == "top":
            stack_start_y = content_top
        elif col_valign == "bottom":
            stack_start_y = content_top + max(0, col_zone_h - total_aligned_h)
        else:
            stack_start_y = content_top + max(0, (col_zone_h - total_aligned_h) // 2)

        # ── Pass 2: render columns using shared zone heights ───────────────
        for i, d in enumerate(col_data):
            sx = x + pad + i * (col_w + col_gap)
            iy = stack_start_y

            # Icon zone (shared height — blank space if this column has no icon)
            if d["has_icon"]:
                ctx.draw_icon(sx, iy, col_w, d["icon_sz"], d["icon_str"],
                              color=d["col_icon_color"])
            iy += max_icon_h

            # Value zone
            if d["has_value"]:
                ctx.text(sx, iy, col_w, d["value_zone_h"],
                         d["value_str"],
                         size=d["val_sz"], bold=True,
                         color=d["col_val_color"],
                         align=text_align, valign="middle", inner_margin=0)
            iy += max_value_h

            # Unit zone
            if d["has_unit"]:
                ctx.text(sx, iy, col_w, d["unit_zone_h"],
                         d["value_unit"],
                         size=d["unit_sz"], bold=False,
                         color=d["col_val_color"],
                         align=text_align, valign="middle", inner_margin=0)
            iy += max_unit_h

            # Headline zone — all headlines start at identical iy
            if d["headline"]:
                ctx.text(sx, iy, col_w, max_headline_h,
                         d["headline"],
                         size=headline_sz, bold=True,
                         color=ctx.color("on-surface"),
                         align=text_align, valign="top",
                         inner_margin=0)
            iy += max_headline_h

            # Body zone — all bodies start at identical iy
            if d["body_text"] and body_zone_h > 8:
                ctx.text(sx, iy, col_w, body_zone_h,
                         d["body_text"],
                         size=body_sz, bold=False,
                         color=ctx.color("on-surface-variant"),
                         align=text_align, valign="top",
                         inner_margin=0)

        # ── Conclusion zone ───────────────────────────────────────────────
        if conclusion:
            conc_color  = self._rc(ctx, str(props.get("conclusion-color", "")), "on-surface")
            chev_color  = self._rc(ctx, str(props.get("chevron-color",   "")), "on-surface-variant")
            conc_bold   = str(props.get("conclusion-bold",  "true")).lower() not in ("false", "no", "0")
            conc_align  = str(props.get("conclusion-align", "center")).strip().lower()
            if conc_align not in ("left", "center", "right"):
                conc_align = "center"

            raw_csz = props.get("conclusion-size", "")
            conc_sz = ctx.slide_font_size("body", props)
            if raw_csz:
                try:
                    conc_sz = max(8, int(raw_csz))
                except (ValueError, TypeError):
                    pass

            div_y = col_zone_bottom
            chev_sz = max(14, GAP_M)   # half-width of chevron arms — prominent but proportional

            chev_cx = x + pad + inner_w // 2
            # Gap around the arrow so the divider line is cleanly split
            chev_gap = chev_sz * 3

            # Split divider: left segment + right segment with arrow gap in between
            if show_conc_div:
                conc_div_color = self._rc(ctx, str(props.get("divider-color", "")), "border-subtle")
                left_w  = chev_cx - (x + pad) - chev_gap // 2
                right_x = chev_cx + chev_gap // 2
                right_w = (x + pad + inner_w) - right_x
                if left_w > 4:
                    ctx.divider(x + pad, div_y, left_w, color=conc_div_color)
                if right_w > 4:
                    ctx.divider(right_x, div_y, right_w, color=conc_div_color)

            # Chevron centred in the gap
            if show_chevron:
                self._draw_chevron(ctx, chev_cx, div_y, chev_sz, chev_color)

            # Conclusion text
            conc_text_y = div_y + (chev_sz + GAP_S if show_chevron else GAP_S)
            conc_text_h = max(20, content_bottom - conc_text_y)
            ctx.text(x + pad, conc_text_y, inner_w, conc_text_h,
                     conclusion,
                     size=conc_sz, bold=conc_bold,
                     color=conc_color,
                     align=conc_align, valign="middle",
                     inner_margin=0)
