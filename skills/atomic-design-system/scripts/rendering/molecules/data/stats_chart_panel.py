"""StatsChartPanel — dark card with stat column and annotated bar chart"""
from __future__ import annotations
from rendering.atoms.data.stat_display import StatDisplayAtom

_stat = StatDisplayAtom()

_STATUS_TOKENS = {"error", "success", "warning", "primary", "secondary",
                  "accent", "neutral"}


class StatsChartPanel:
    """Render a dashboard panel with stats on the left and a bar chart on the right."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        PAD = ctx.card_pad_px(w, h, props)
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        title    = str(props.get("title",    ""))
        subtitle = str(props.get("subtitle", "") or props.get("badge", ""))
        pill     = str(props.get("period",   ""))

        show_header      = bool(title or subtitle or pill) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)

        title_color  = ctx.card_title_color(props, default_token="text-default")
        sub_color    = ctx.color("on-surface-variant")
        div_color    = ctx.card_line_color("header", ctx.color("line-default"), props)
        header_align = ctx.card_header_align(props, default="left")

        # Stats / body alignment — default center
        stat_align = str(props.get("text-align") or props.get("text_align") or "center").strip().lower()
        if stat_align not in ("left", "center", "right"):
            stat_align = "center"

        cy = y + PAD

        # ── Standard card header (same sizing as all other molecules) ─────────
        if show_header:
            inner_w    = w - PAD * 2
            header_h   = ctx.card_header_h(w, h, props)
            header_gap = ctx.card_header_gap(h, props)
            title_sz   = ctx.card_header_font_size(title or subtitle, inner_w, h, props)

            if subtitle:
                # Title on first line, subtitle beneath — split header_h proportionally
                title_zone_h = max(int(header_h * 0.55), int(title_sz * 1.3))
                sub_sz       = max(ctx.font_size("caption"), ctx.font_size("body") - 2)
                sub_zone_h   = max(int(sub_sz * 1.4), header_h - title_zone_h)
                ctx.text(x + PAD, cy, inner_w, title_zone_h,
                         title, size=title_sz, bold=True,
                         color=title_color,
                         align=header_align, valign="middle")
                ctx.text(x + PAD, cy + title_zone_h, inner_w, sub_zone_h,
                         subtitle, size=sub_sz, bold=False,
                         color=sub_color,
                         align=header_align, valign="middle")
                cy += title_zone_h + sub_zone_h + header_gap
            else:
                ctx.text(x + PAD, cy, inner_w, header_h,
                         title or pill, size=title_sz, bold=True,
                         color=title_color,
                         align=header_align, valign="middle")
                cy += header_h + header_gap

            if pill and subtitle:
                pass  # pill already shown as subtitle; skip separate badge

            if show_header_line:
                lx, lw = ctx.card_divider_span("header", x + PAD, inner_w, props)
                ctx.divider(lx, cy, lw, color=div_color)
                cy += 1 + ctx.spacing("s")

        body_y  = cy
        body_h  = max(20, y + h - PAD - body_y)
        left_w  = int(w * 0.38)
        right_x = x + left_w + PAD * 2
        right_w = max(20, w - left_w - PAD * 3)

        # --- Stats column ---------------------------------------------------
        stats   = props.get("stats") or []
        n_stats = max(len(stats), 1)
        row_h   = body_h // n_stats

        for i, stat in enumerate(stats[:4]):
            if not isinstance(stat, dict):
                continue
            sy        = body_y + i * row_h
            label     = str(stat.get("label",           ""))
            stat_val  = str(stat.get("value",           ""))
            stat_unit = str(stat.get("unit",            ""))
            dot_tok   = str(stat.get("dot-color-token", ""))
            dot_offset = 0

            if dot_tok:
                dot_c = (ctx.color(dot_tok)
                         if dot_tok in _STATUS_TOKENS
                         else ctx.color("primary"))
                dot_r = 5
                ctx.rect(x + PAD, sy + row_h // 2 - dot_r,
                         dot_r * 2, dot_r * 2,
                         fill=dot_c, radius=dot_r)
                dot_offset = dot_r * 2 + 6

            lx = x + PAD + dot_offset
            lw = left_w - PAD - dot_offset
            ctx.text(lx, sy, lw, row_h // 2, label,
                     size=ctx.font_size("annotation"), color=ctx.color("text-secondary"),
                     align=stat_align, valign="bottom")
            _stat.render(ctx, lx, sy + row_h // 2 - 4, lw, row_h // 2 + 4,
                         value=stat_val, unit=stat_unit, sublabel="",
                         val_color=ctx.color("on-surface"),
                         unit_color=ctx.color("on-surface-variant"),
                         sub_color=ctx.color("on-surface-variant"),
                         align=stat_align)

        # --- Bar chart column -----------------------------------------------
        labels     = props.get("chart-labels") or props.get("labels") or []
        values     = props.get("chart-values") or props.get("values") or []
        chart_unit = str(props.get("chart-unit") or props.get("unit", ""))
        ref_lines  = props.get("ref-lines") or []
        highlight  = props.get("highlight-bar")
        if highlight is not None:
            highlight = int(highlight)

        if not (labels and values):
            return

        n      = len(labels)
        gutter = max(10, ctx.spacing("s"))
        bw     = max(6, (right_w - PAD - (n - 1) * gutter) // max(n, 1))
        mx_v   = max(float(v) for v in values) or 1
        ch     = body_h - PAD - 20

        for rl_v in ref_lines:
            rl_y = body_y + ch - int(float(rl_v) / mx_v * ch)
            ctx.line(right_x, rl_y, right_x + right_w - PAD, rl_y,
                     ctx.color("line-default"))
            rl_label = (f"{int(rl_v)} hours"
                        if float(rl_v) == int(float(rl_v)) else str(rl_v))
            ctx.text(right_x - 52, rl_y - 8, 50, 16, rl_label,
                     size=ctx.font_size("annotation"), color=ctx.color("text-secondary"),
                     align="right")

        for i, (lbl, val) in enumerate(zip(labels, values)):
            bh_bar   = max(4, int(float(val) / mx_v * ch))
            bx       = right_x + i * (bw + gutter)
            by       = body_y + ch - bh_bar
            bar_fill = (ctx.color("primary")
                        if i == highlight
                        else ctx.color("bg-card-alt"))
            ctx.rect(bx, by, bw, bh_bar, fill=bar_fill, radius=4)

            top_lbl = f"{val}{chart_unit}" if chart_unit else str(val)
            if i == highlight:
                ctx.badge(bx - 2, by - 22, bw + 4, 18, top_lbl,
                          fill=ctx.color("primary"),
                          text_color=ctx.color("on-primary"),
                          size=ctx.font_size("body"), radius=6)
            else:
                ctx.text(bx - 2, by - 20, bw + 4, 18, top_lbl,
                         size=ctx.font_size("body"), color=ctx.color("on-surface-variant"),
                         align="center")

            ctx.text(bx - 4, body_y + ch + 6, bw + 8, 20, str(lbl),
                     size=ctx.font_size("body"), color=ctx.color("on-surface-variant"),
                     align="center")
