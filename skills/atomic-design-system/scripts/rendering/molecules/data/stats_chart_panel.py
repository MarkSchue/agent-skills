"""StatsChartPanel — dark card with stat column and annotated bar chart"""
from __future__ import annotations
from rendering.atoms.data.icon_title_header import IconTitleHeaderAtom
from rendering.atoms.data.stat_display       import StatDisplayAtom

_header = IconTitleHeaderAtom()
_stat   = StatDisplayAtom()

_STATUS_TOKENS = {"error", "success", "warning", "primary", "secondary",
                  "accent", "neutral"}


class StatsChartPanel:
    """Render a dashboard panel with stats on the left and a bar chart on the right."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        PAD = ctx.PAD
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        header_h = max(60, int(h * 0.22))
        body_y   = y + header_h + PAD
        body_h   = h - header_h - PAD * 2
        left_w   = int(w * 0.35)
        right_x  = x + left_w + PAD * 3
        right_w  = w - left_w - PAD * 4

        title    = str(props.get("title",    ""))
        subtitle = str(props.get("subtitle", ""))
        pill     = str(props.get("period",   ""))
        show_header = bool(title or subtitle or pill) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)

        if show_header:
            icon_raw = str(props.get("icon-name", "") or props.get("icon", ""))
            _header.render(ctx, x, y, w, header_h,
                           icon_bg=ctx.icon_bg(props),
                           title=title,
                           subtitle=subtitle,
                           pill=pill,
                           pill_bg=ctx.color("surface-variant"),
                           pill_color=ctx.color("on-surface"),
                           title_color=ctx.card_title_color(props, default_token="on-surface"),
                           sub_color=ctx.color("on-surface-variant"),
                           icon_name=icon_raw)

        if show_header_line:
            ctx.divider(x + PAD, y + header_h, w - PAD * 2,
                        color=ctx.card_line_color("header", ctx.color("line-default"), props))

        # --- Stats column ---------------------------------------------------
        stats   = props.get("stats") or []
        n_stats = max(len(stats), 1)
        row_h   = body_h // n_stats

        for i, stat in enumerate(stats[:3]):
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
                     align="left", valign="bottom")
            _stat.render(ctx, lx, sy + row_h // 2 - 4, lw, row_h // 2 + 4,
                         value=stat_val, unit=stat_unit, sublabel="",
                         val_color=ctx.color("on-surface"),
                         unit_color=ctx.color("on-surface-variant"),
                         sub_color=ctx.color("on-surface-variant"),
                         align="left")

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
