"""QuoteCard — large pull-quote with attribution"""
from __future__ import annotations


class QuoteCard:
    """Render a large pull-quote card with an opening mark and attribution."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        PAD = ctx.PAD
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        quote       = str(props.get("quote", ""))
        attribution = str(props.get("attribution", ""))
        attr_h      = 36 if attribution else 0
        q_mark_sz   = min(48, max(32, int(h * 0.07)))
        q_mark_h    = q_mark_sz + 4
        q_body_sz   = min(20, max(13, int(h * 0.022)))
        q_body_h    = h - PAD - q_mark_h - PAD // 2 - attr_h - PAD

        ctx.text(x + PAD, y + PAD, q_mark_h, q_mark_h, "\u201C",
                 size=q_mark_sz, bold=True,
                 color=ctx.color("primary"),
                 align="left", valign="top")

        qy = y + PAD + q_mark_h + PAD // 2
        ctx.text(x + PAD, qy, w - PAD * 2, max(40, q_body_h), quote,
                 size=q_body_sz,
                 color=ctx.color("on-primary-container"),
                 align="left", valign="top")

        if attribution:
            ctx.text(x + PAD, y + h - PAD - attr_h, w - PAD * 2, attr_h,
                     f"\u2014 {attribution}",
                     size=ctx.font_size("caption"), bold=True, italic=True,
                     color=ctx.color("on-primary-container"),
                     align="right")
