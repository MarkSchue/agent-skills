"""DailyHeaderCard — dark title card with date/time footer"""
from __future__ import annotations


class DailyHeaderCard:
    """Render a dark full-bleed title card with date and time in the footer."""

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

        footer_h = max(24, int(h * 0.10)) if show_footer else 0
        footer_gap = max(ctx.spacing("s"), int(h * 0.016)) if show_footer else 0
        footer_y = y + h - PAD - footer_h
        title_h  = h - footer_h - PAD * 2 - footer_gap
        title_sz = max(28, min(64, int(h * 0.12)))

        if show_header:
            ctx.text(x + PAD, y + PAD, w - PAD * 2, title_h, title,
                     size=title_sz, bold=True,
                     color=ctx.color("surface"),
                     align="left", valign="top")

        if show_footer_line:
            ctx.divider(x + PAD, footer_y - footer_gap, w - PAD * 2,
                        color=ctx.card_line_color("footer", ctx.color("line-default")))

        if show_footer and date:
            ctx.text(x + PAD, footer_y, w // 2, footer_h, date,
                     size=ctx.font_size("annotation"), color=ctx.color("on-surface-variant"),
                     align="left", valign="middle")

        if show_footer and time_str:
            ctx.text(x + w // 2, footer_y, w // 2 - PAD, footer_h,
                     time_str,
                     size=ctx.font_size("annotation"), color=ctx.color("on-surface-variant"),
                     align="right", valign="middle")
