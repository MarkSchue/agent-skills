"""TableSummaryCard — summary companion for data tables.

Shows the most important KPIs from a table alongside contextual annotations
(assumptions, remarks, notes, warnings).  Can sit to the **left** of a table
(vertical stack) or **below** it (horizontal KPI strip + annotation rows).
When placed below / in table-companion mode the card visually "attaches" to
the table with a top accent stripe and a subtly highlighted background.

Design anatomy — layout: stacked  (default)
────────────────────────────────────────────
  ┌────────────────────────────────────────────────────────────┐
  │  ████ accent stripe  (table-mode only)                     │
  │  [Optional card title]                                     │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │  ← KPI strip
  │  │  LABEL   │  │  LABEL   │  │  LABEL   │
  │  │  87 %    │  │  12.4 M  │  │  +3 d    │
  │  └──────────┘  └──────────┴──────────────┘
  │  ─────────────────────────────────────────────────────────
  │  [Assumption] Lorem ipsum dolor sit amet consetetur         │  ← info rows
  │  [Remark]     Lorem ipsum dolor sit amet consetetur         │
  │  [Note]       Lorem ipsum dolor sit amet                    │
  └────────────────────────────────────────────────────────────┘

Design anatomy — layout: side-by-side
──────────────────────────────────────
  ┌──────────────────────────────────────────────────────────────┐
  │  ████ accent stripe  (table-mode only)                       │
  │  ┌──────────┐  │  [Assumption] Lorem ipsum dolor sit amet    │
  │  │ VALUE    │  │  [Remark]     Lorem ipsum dolor sit amet    │
  │  ├──────────┤  │  [Note]       Lorem ipsum dolor sit amet    │
  │  │ VALUE    │  │                                             │
  │  └──────────┘  │                                             │
  └──────────────────────────────────────────────────────────────┘

KPI item fields
────────────────
  label       : string     — metric name (small, above value)
  value       : string     — main metric  (large, highlighted)
  value-unit  : string     — unit suffix appended to value  (e.g. "%", "M €")
  trend       : up|down|neutral — arrow indicator
  color       : color      — per-KPI value color override  default: text-highlight
  sublabel    : string     — tiny text below value (e.g. "YTD" or a reference)

Info item fields
─────────────────
  type        : assumption|remark|note|warning|info|custom  — semantic badge
  label       : string     — badge text (auto from type if omitted)
  text        : string     — body text
  color       : color      — per-item badge fill override

Card-level props
─────────────────
  title               : card header title
  kpis                : list of KPI objects
  info                : list of annotation / info objects
  layout              : stacked | side-by-side           default: stacked
  kpi-col-frac        : 0..1 fraction of width for KPI zone in side-by-side  default: 0.40
  kpi-value-color     : global KPI value color           default: text-highlight
  kpi-value-size      : explicit px for KPI values       default: auto
  kpi-label-color     : KPI label text                   default: on-surface-variant
  kpi-fill            : background for each KPI chip     default: transparent (bg-card)
  kpi-border          : bool — border around KPI chips   default: false
  kpi-divider         : bool — vertical dividers between KPIs   default: false
  info-label-color    : text color inside type badges    default: surface
  info-text-color     : annotation body text             default: on-surface-variant
  info-text-size      : font-size for annotation text    default: body
  table-mode          : bool — companion styling          default: false
  accent-color        : top stripe and badge accent      default: primary
  accent-stripe-h     : px height of top accent stripe   default: 4
  placement           : left|below — semantic alias for layout hint  (read-only)
"""
from __future__ import annotations


# ── Semantic badge labels and colors ─────────────────────────────────────────
_INFO_TYPE_LABELS: dict[str, str] = {
    "assumption": "Assumption",
    "remark":     "Remark",
    "note":       "Note",
    "warning":    "Warning",
    "info":       "Info",
}

_INFO_TYPE_TOKENS: dict[str, tuple[str, str]] = {
    # (badge-fill-token, badge-text-token)
    "assumption": ("on-surface-variant", "surface"),
    "remark":     ("primary",            "on-primary"),
    "note":       ("secondary",          "on-secondary"),
    "warning":    ("warning",            "on-warning"),
    "info":       ("secondary",          "on-secondary"),
    "custom":     ("on-surface-variant", "surface"),
}


class TableSummaryCard:
    """Render a KPI + annotation summary companion card for data tables."""

    # ── Internal helpers ──────────────────────────────────────────────────────

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
        if raw in ("true", "yes", "1"):
            return True
        if raw in ("false", "no", "0"):
            return False
        return default

    def _info_badge_colors(self, ctx, item: dict,
                           global_label_color: str) -> tuple[str, str]:
        """Return (fill, text) for an info badge."""
        item_type  = str(item.get("type", "custom")).strip().lower()
        tokens     = _INFO_TYPE_TOKENS.get(item_type, _INFO_TYPE_TOKENS["custom"])
        fill_raw   = str(item.get("color", "")).strip()
        fill  = self._rc(ctx, fill_raw, tokens[0]) if fill_raw else ctx.color(tokens[0])
        text  = global_label_color or ctx.color(tokens[1])
        return fill, text

    def _info_badge_label(self, item: dict) -> str:
        custom = str(item.get("label", "")).strip()
        if custom:
            return custom
        item_type = str(item.get("type", "")).strip().lower()
        return _INFO_TYPE_LABELS.get(item_type, "Note")

    # ── Drawing sub-sections ──────────────────────────────────────────────────

    def _draw_kpi_strip(self, ctx, props: dict,
                        sx: int, sy: int, sw: int, sh: int,
                        kpis: list,
                        kpi_value_color: str,
                        kpi_label_color: str,
                        kpi_fill: str,
                        show_kpi_border: bool,
                        show_kpi_dividers: bool,
                        border_color: str,
                        cell_pad: int) -> None:
        """Draw the horizontal KPI chip strip in the given bounding box."""
        n = max(1, len(kpis))
        GAP = ctx.spacing("s")
        chip_gap = GAP
        chip_w   = max(20, (sw - chip_gap * (n - 1)) // n)

        # Global explicit value size
        raw_vsz = props.get("kpi-value-size", "")
        global_vsz = 0
        try:
            global_vsz = max(10, int(raw_vsz)) if str(raw_vsz).strip() else 0
        except (ValueError, TypeError):
            pass

        label_sz  = max(8,  min(12, int(sh * 0.19)))
        auto_vsz  = max(18, min(44, int(sh * 0.42)))
        sub_sz    = max(7,  min(10, int(sh * 0.14)))
        vsz       = global_vsz or auto_vsz
        trend_sz  = max(8,  min(14, int(sh * 0.18)))

        label_h   = int(label_sz * 1.5)
        value_h   = int(vsz * 1.35)
        sub_h     = int(sub_sz * 1.4)
        trend_h   = int(trend_sz * 1.4)

        for i, kpi in enumerate(kpis):
            if not isinstance(kpi, dict):
                kpi = {"value": str(kpi)}

            cx = sx + i * (chip_w + chip_gap)

            # Chip background & border
            if kpi_fill and kpi_fill != ctx.color("bg-card"):
                ctx.rect(cx, sy, chip_w, sh,
                         fill=kpi_fill,
                         stroke=border_color if show_kpi_border else None,
                         radius=ctx.rad("radius-small") if hasattr(ctx, "rad") else 4)
            elif show_kpi_border:
                ctx.rect(cx, sy, chip_w, sh,
                         fill=kpi_fill or ctx.color("bg-card"),
                         stroke=border_color,
                         radius=ctx.rad("radius-small") if hasattr(ctx, "rad") else 4)

            # Vertical divider between KPIs (not after last)
            if show_kpi_dividers and i > 0:
                ctx.rect(cx - 1, sy + cell_pad, 1, sh - cell_pad * 2,
                         fill=border_color, stroke=None)

            # Compute content stack (label? → value → sublabel? + trend?)
            kpi_label    = str(kpi.get("label", "")).strip()
            raw_value    = str(kpi.get("value", "—")).strip()
            unit         = str(kpi.get("value-unit", "")).strip()
            sublabel     = str(kpi.get("sublabel", "")).strip()
            trend_str    = str(kpi.get("trend", "")).strip().lower()

            show_lbl     = bool(kpi_label)
            show_sub     = bool(sublabel)
            has_trend    = trend_str in ("up", "down", "neutral")

            stack_h = (label_h if show_lbl else 0) + value_h + (sub_h if show_sub else 0)
            iy = sy + max(cell_pad, (sh - stack_h) // 2)

            # Label
            if show_lbl:
                ctx.text(cx + cell_pad, iy, chip_w - cell_pad * 2, label_h,
                         kpi_label, size=label_sz, bold=False,
                         color=kpi_label_color, align="left", valign="middle",
                         inner_margin=0)
                iy += label_h

            # Value + unit
            per_col_raw   = str(kpi.get("color", "")).strip()
            val_color     = (self._rc(ctx, per_col_raw, "text-highlight")
                             if per_col_raw else kpi_value_color)
            display_value = f"{raw_value} {unit}".strip() if unit else raw_value

            # Trend arrow prefix
            if has_trend:
                arrow = "↑ " if trend_str == "up" else ("↓ " if trend_str == "down" else "→ ")
                display_value = arrow + display_value

            ctx.text(cx + cell_pad, iy, chip_w - cell_pad * 2, value_h,
                     display_value,
                     size=vsz, bold=True,
                     color=val_color,
                     align="left", valign="middle", inner_margin=0)
            iy += value_h

            # Sub-label
            if show_sub:
                ctx.text(cx + cell_pad, iy, chip_w - cell_pad * 2, sub_h,
                         sublabel, size=sub_sz, bold=False,
                         color=kpi_label_color, align="left", valign="middle",
                         inner_margin=0)

    def _draw_info_rows(self, ctx, props: dict,
                        sx: int, sy: int, sw: int, sh: int,
                        info_items: list,
                        info_text_color: str,
                        info_label_color: str,
                        info_text_sz: int,
                        cell_pad: int) -> None:
        """Draw stacked annotation rows."""
        n = max(1, len(info_items))
        GAP_XS = ctx.spacing("xs")
        GAP_S  = ctx.spacing("s")

        # Row height: equal distribution
        row_h = max(16, sh // n)

        badge_sz   = max(7,  min(11, int(row_h * 0.40)))
        badge_h    = badge_sz + 6
        badge_w_min = 70
        # Measure a reasonable badge width
        badge_w    = max(badge_w_min, int(sw * 0.14))
        text_x     = sx + badge_w + GAP_S
        text_w     = max(20, sw - badge_w - GAP_S)

        iy = sy
        for item in info_items:
            if not isinstance(item, dict):
                item = {"type": "note", "text": str(item)}

            badge_label = self._info_badge_label(item)
            b_fill, b_tc = self._info_badge_colors(ctx, item, info_label_color)
            body_text   = str(item.get("text", "")).strip()

            # Vertically centre both badge and text in the row
            by = iy + max(0, (row_h - badge_h) // 2)
            ctx.badge(sx, by, badge_w, badge_h,
                      badge_label, fill=b_fill,
                      text_color=b_tc, size=badge_sz,
                      radius=max(3, badge_h // 3))

            if body_text:
                ctx.text(text_x, iy, text_w, row_h,
                         body_text, size=info_text_sz, bold=False,
                         color=info_text_color,
                         align="left", valign="middle", inner_margin=0)

            iy += row_h

    # ── Main render ───────────────────────────────────────────────────────────

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:

        kpis       = list(props.get("kpis")  or [])
        info_items = list(props.get("info")  or [])

        if not kpis and not info_items:
            return

        # ── Card contract ─────────────────────────────────────────────────
        pad     = ctx.card_pad_px(w, h, props)
        inner_w = w - pad * 2
        title   = str(props.get("title", ""))

        show_header      = bool(title) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)
        title_color      = ctx.card_title_color(props, default_token="text-default")
        header_align     = ctx.card_header_align(props, default="left")
        hdr_div_c        = ctx.card_line_color("header", ctx.color("line-default"), props)

        # ── Table-companion mode ──────────────────────────────────────────
        table_mode = self._bool_prop(props, "table-mode", False)
        accent_color_raw = str(props.get("accent-color", "")).strip()
        accent_color     = self._rc(ctx, accent_color_raw, "primary")
        accent_stripe_h  = self._int_prop(props, "accent-stripe-h", 4)
        if accent_stripe_h < 2:
            accent_stripe_h = 0

        bg_token  = "primary-container" if table_mode else "bg-card"
        bg_color  = ctx.card_bg_color(props, bg_token)

        # Card frame — in table-mode suppress top border-radius to "dock" to table
        if table_mode:
            r = ctx.rad()
            # Draw the card body with full radius, then overdraw top-corners with square rect
            ctx.rect(x, y, w, h,
                     fill=bg_color,
                     stroke=ctx.color("border-default"),
                     radius=r)
            # Mask top two corners square: thin rect strip
            if r > 0:
                ctx.rect(x, y, w, r + 1, fill=bg_color, stroke=None, radius=0)
            # Top accent stripe
            if accent_stripe_h > 0:
                ctx.rect(x, y, w, accent_stripe_h,
                         fill=accent_color, stroke=None, radius=0)
        else:
            ctx.rect(x, y, w, h,
                     fill=bg_color,
                     stroke=ctx.color("border-default"),
                     radius=ctx.rad())

        GAP_S  = ctx.spacing("s")
        GAP_M  = ctx.spacing("m")
        GAP_XS = ctx.spacing("xs")

        cy = y + pad
        # Shift below stripe if table-mode
        if table_mode and accent_stripe_h > 0:
            cy = max(cy, y + accent_stripe_h + GAP_XS)

        # ── Optional title header ─────────────────────────────────────────
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

        has_kpis  = bool(kpis)
        has_info  = bool(info_items)

        # ── Global styling ────────────────────────────────────────────────
        kpi_value_color = self._rc(ctx, str(props.get("kpi-value-color", "")), "text-highlight")
        kpi_label_color = self._rc(ctx, str(props.get("kpi-label-color", "")), "on-surface-variant")
        kpi_fill_raw    = str(props.get("kpi-fill", "")).strip()
        kpi_fill        = self._rc(ctx, kpi_fill_raw, "bg-card") if kpi_fill_raw else ctx.color("bg-card")
        show_kpi_border   = self._bool_prop(props, "kpi-border",   False)
        show_kpi_dividers = self._bool_prop(props, "kpi-divider",  False)
        border_color      = self._rc(ctx, str(props.get("border-color", "")), "border-subtle")

        info_text_color = self._rc(ctx, str(props.get("info-text-color", "")), "on-surface-variant")
        info_label_c    = self._rc(ctx, str(props.get("info-label-color", "")), "surface")

        info_text_sz_raw = props.get("info-text-size", "")
        try:
            info_text_sz = max(8, int(info_text_sz_raw)) if str(info_text_sz_raw).strip() else ctx.font_size("body")
        except (ValueError, TypeError):
            info_text_sz = ctx.font_size("body")

        cell_pad = GAP_S

        # ── Layout ────────────────────────────────────────────────────────
        layout = str(props.get("layout", "stacked")).strip().lower()
        if layout not in ("stacked", "side-by-side"):
            layout = "stacked"

        if layout == "side-by-side" and has_kpis and has_info:
            kpi_frac  = float(props.get("kpi-col-frac", 0.40) or 0.40)
            kpi_frac  = max(0.20, min(0.70, kpi_frac))
            kpi_zone_w = max(40, int(inner_w * kpi_frac))
            sep_w      = 1
            sep_gap    = GAP_S
            info_zone_x = x + pad + kpi_zone_w + sep_w + sep_gap
            info_zone_w = max(20, inner_w - kpi_zone_w - sep_w - sep_gap)

            # KPI chips — vertical stack in their zone
            n_kpis   = len(kpis)
            chip_h   = max(30, content_h // max(1, n_kpis) - cell_pad)
            kpi_y    = content_top
            for i, kpi in enumerate(kpis):
                self._draw_kpi_strip(ctx, props,
                                     x + pad, kpi_y, kpi_zone_w, chip_h,
                                     [kpi],
                                     kpi_value_color, kpi_label_color, kpi_fill,
                                     show_kpi_border, False,
                                     border_color, cell_pad)
                kpi_y += chip_h + cell_pad

            # Separator line
            ctx.rect(x + pad + kpi_zone_w, content_top,
                     sep_w, content_h,
                     fill=border_color, stroke=None)

            # Info rows
            self._draw_info_rows(ctx, props,
                                 info_zone_x, content_top,
                                 info_zone_w, content_h,
                                 info_items, info_text_color, info_label_c,
                                 info_text_sz, cell_pad)

        else:  # stacked (default)
            kpi_zone_h  = 0
            info_zone_h = 0
            mid_div_h   = 0

            if has_kpis and has_info:
                # KPI strip gets ~38% of content height, rest for info
                kpi_zone_h  = max(40, int(content_h * 0.38))
                mid_div_h   = 1 + GAP_XS * 2
                info_zone_h = max(20, content_h - kpi_zone_h - mid_div_h)
            elif has_kpis:
                kpi_zone_h  = content_h
            else:
                info_zone_h = content_h

            if has_kpis:
                self._draw_kpi_strip(ctx, props,
                                     x + pad, content_top, inner_w, kpi_zone_h,
                                     kpis,
                                     kpi_value_color, kpi_label_color, kpi_fill,
                                     show_kpi_border, show_kpi_dividers,
                                     border_color, cell_pad)

            if has_kpis and has_info:
                div_y = content_top + kpi_zone_h + GAP_XS
                lx, lw = ctx.card_divider_span("header", x + pad, inner_w, props)
                ctx.divider(lx, div_y, lw,
                            color=accent_color if table_mode else hdr_div_c)

            if has_info:
                info_y = (content_top + kpi_zone_h + mid_div_h) if has_kpis else content_top
                self._draw_info_rows(ctx, props,
                                     x + pad, info_y,
                                     inner_w, info_zone_h,
                                     info_items, info_text_color, info_label_c,
                                     info_text_sz, cell_pad)
