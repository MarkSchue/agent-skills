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
        """Draw a downward-pointing filled V chevron centred at (cx, cy)."""
        t = max(3, sz // 4)   # arm thickness
        try:
            # 6-point polygon: outer V, inner V (clockwise)
            pts = [
                (cx - sz,     cy - sz // 2),       # A outer top-left
                (cx,          cy + sz // 2),        # B outer bottom
                (cx + sz,     cy - sz // 2),        # C outer top-right
                (cx + sz - t, cy - sz // 2),        # D inner top-right
                (cx,          cy + sz // 2 - t),    # E inner bottom
                (cx - sz + t, cy - sz // 2),        # F inner top-left
            ]
            ctx.polygon(pts, fill=color, stroke=None)
        except Exception:
            # Fallback: text character
            ctx.text(cx - sz, cy - sz, sz * 2, sz * 2, "∨",
                     size=max(10, sz), bold=True, color=color,
                     align="center", valign="middle", inner_margin=0)

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

        show_header      = bool(title) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)

        title_color   = ctx.card_title_color(props, default_token="text-default")
        header_align  = ctx.card_header_align(props, default="left")
        div_color     = ctx.card_line_color("header", ctx.color("line-default"), props)
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
            header_h   = ctx.card_header_h(w, h, props)
            header_gap = ctx.card_header_gap(h, props)
            title_size = ctx.card_header_font_size(title, inner_w, h, props)
            ctx.text(x + pad, cy, inner_w, header_h,
                     title, size=title_size, bold=True,
                     color=title_color, align=header_align, valign="middle")
            cy += header_h + header_gap
            if show_header_line:
                lx, lw = ctx.card_divider_span("header", x + pad, inner_w, props)
                ctx.divider(lx, cy, lw, color=div_color)
                cy += 1 + GAP_S

        # ── Content area bounds ───────────────────────────────────────────
        content_top    = cy
        content_bottom = y + h - pad
        content_h      = max(20, content_bottom - content_top)

        # ── Conclusion zone allocation ────────────────────────────────────
        conclusion     = str(props.get("conclusion", "")).strip()
        show_conc_div  = str(props.get("show-divider", "true")).lower() != "false"
        show_chevron   = (str(props.get("show-chevron", "true")).lower() != "false"
                          and bool(conclusion))

        conc_zone_h = 0
        if conclusion:
            conc_sz    = ctx.font_size("body")
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
        body_sz     = ctx.font_size("body")

        # Auto value size: prominent, scales with column dimensions
        auto_val_sz = max(22, min(52, int(min(col_w * 0.32, col_zone_h * 0.28))))

        # Auto icon size
        auto_icon_sz = ctx.icon_size(col_w, col_zone_h, props)

        for i, col in enumerate(cols_raw):
            if not isinstance(col, dict):
                col = {"headline": str(col)}

            sx = x + pad + i * (col_w + col_gap)

            icon_str    = str(col.get("icon", "")).strip()
            value_str   = str(col.get("value", "")).strip()
            value_unit  = str(col.get("value-unit", "")).strip()
            headline    = str(col.get("headline", "")).strip()
            body_text   = str(col.get("body", "")).strip()

            # Per-column color override
            col_color_raw = str(col.get("color", "")).strip()
            col_val_color  = (self._rc(ctx, col_color_raw, "primary")
                              if col_color_raw else global_val_color)
            col_icon_color = (self._rc(ctx, col_color_raw, "on-surface-variant")
                              if col_color_raw else global_icon_color)

            icon_sz  = global_icon_sz or auto_icon_sz
            val_sz   = global_val_sz  or auto_val_sz

            # ── Vertical stack within column ──────────────────────────────
            # Determine which zones are active and sizes
            has_icon  = bool(icon_str)
            has_value = bool(value_str)

            icon_zone_h   = (icon_sz + GAP_S)  if has_icon  else 0
            value_zone_h  = (int(val_sz * 1.35) + GAP_XS) if has_value else 0
            headline_zone_h = (int(headline_sz * 1.5) * max(1, len(headline) // max(1, col_w // max(1, headline_sz)) + 1))
            headline_zone_h = min(headline_zone_h, int(col_zone_h * 0.35))
            headline_zone_h = max(int(headline_sz * 1.5), headline_zone_h) if headline else 0
            body_zone_h   = (max(20, col_zone_h - icon_zone_h - value_zone_h - headline_zone_h - GAP_S * 2)
                             if body_text else 0)

            total_h = icon_zone_h + value_zone_h + headline_zone_h + body_zone_h
            # Centre the stack vertically in col_zone_h
            start_y = content_top + max(0, (col_zone_h - total_h) // 2)
            iy      = start_y

            # Icon
            if has_icon:
                ctx.draw_icon(sx, iy, col_w, icon_sz, icon_str, color=col_icon_color)
                iy += icon_sz + GAP_S

            # Metric value + unit
            if has_value:
                display = f"{value_str} {value_unit}".strip() if value_unit else value_str
                ctx.text(sx, iy, col_w, int(val_sz * 1.35),
                         display,
                         size=val_sz, bold=True,
                         color=col_val_color,
                         align=text_align, valign="middle",
                         inner_margin=0)
                iy += int(val_sz * 1.35) + GAP_XS

            # Headline
            if headline:
                ctx.text(sx, iy, col_w, headline_zone_h,
                         headline,
                         size=headline_sz, bold=True,
                         color=ctx.color("on-surface"),
                         align=text_align, valign="top",
                         inner_margin=0)
                iy += headline_zone_h + GAP_XS

            # Body
            if body_text and body_zone_h > 8:
                ctx.text(sx, iy, col_w, body_zone_h,
                         body_text,
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
            conc_sz = ctx.font_size("body")
            if raw_csz:
                try:
                    conc_sz = max(8, int(raw_csz))
                except (ValueError, TypeError):
                    pass

            div_y = col_zone_bottom
            chev_sz = max(6, GAP_M // 2 + 2)   # half-width of chevron arms

            # Full-width divider
            if show_conc_div:
                conc_div_color = self._rc(ctx, str(props.get("divider-color", "")), "border-subtle")
                ctx.divider(x + pad, div_y, inner_w, color=conc_div_color)

            # Chevron centred on divider
            if show_chevron:
                chev_cx = x + pad + inner_w // 2
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
