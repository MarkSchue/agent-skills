"""DailyHeaderCard — title card with date/time footer"""
from __future__ import annotations


class DailyHeaderCard:
    """Render a full-bleed title card with date and time in the footer."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        PAD = ctx.PAD
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        title    = str(props.get("title", ""))
        date     = str(props.get("date",  ""))
        time_str = str(props.get("time",  ""))
        show_header = bool(title) and ctx.card_section_enabled(props, "header", default=True)
        show_footer = bool(date or time_str) and ctx.card_section_enabled(props, "footer", default=True)
        show_footer_line = show_footer and ctx.card_line_enabled(props, "footer", default=True)

        footer_h = ctx.card_footer_h(h, props) if show_footer else 0
        footer_gap = ctx.card_footer_gap(h, props) if show_footer else 0
        footer_size = ctx.card_footer_font_size(props)
        footer_color = ctx.card_footer_color(props)
        footer_italic = ctx.card_footer_italic(props)

        footer_y = y + h - PAD - footer_h
        title_h  = h - footer_h - PAD * 2 - footer_gap
        title_sz = max(28, min(64, int(h * 0.12)))

        if show_header:
            ctx.text(x + PAD, y + PAD, w - PAD * 2, title_h, title,
                     size=title_sz, bold=True,
                     color=ctx.card_title_color(props, default_token="on-surface"),
                     align="left", valign="top")

        if show_footer_line:
            line_x, line_w = ctx.card_divider_span("footer", x + PAD, w - PAD * 2, props)
            ctx.divider(line_x, footer_y - footer_gap, line_w,
                        color=ctx.card_line_color("footer", ctx.color("line-default"), props))

        if show_footer and date:
            ctx.text(x + PAD, footer_y, w // 2, footer_h, date,
                     size=footer_size, italic=footer_italic,
                     color=footer_color,
                     align="left", valign="middle", inner_margin=0)

        if show_footer and time_str:
            ctx.text(x + w // 2, footer_y, w // 2 - PAD, footer_h,
                     time_str,
                     size=footer_size, italic=footer_italic,
                     color=footer_color,
                     align="right", valign="middle", inner_margin=0)
