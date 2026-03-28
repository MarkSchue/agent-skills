"""TeamGridPanel — grid of mini member cards"""
from __future__ import annotations


class TeamGridPanel:
    """Render a grid of compact team member cards with avatar, name, and title."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        members = props.get("members", []) or []
        cols    = int(props.get("columns", 3))
        title   = str(props.get("title",   ""))

        if title:
            ctx.text(x, y, w, 28, title,
                     size=ctx.font_size("label"), bold=True, color=ctx.color("on-surface"))
            y += 36

        card_w = (w - (cols - 1) * 12) // cols
        card_h = 108

        for i, member in enumerate(members):
            if not isinstance(member, dict):
                continue
            col = i % cols
            row = i // cols
            cx  = x + col * (card_w + 12)
            cy  = y + row * (card_h + 12)

            ctx.rect(cx, cy, card_w, card_h,
                     fill=ctx.card_bg_color(props, "bg-card"),
                     stroke=ctx.color("border-default"),
                     radius=ctx.rad())

            av_r = 20
            ctx.ellipse(cx + card_w // 2 - av_r, cy + 10,
                        av_r * 2, av_r * 2,
                        fill=ctx.color("primary"))

            ctx.text(cx + 4, cy + 52, card_w - 8, 22,
                     str(member.get("name", "")),
                     size=ctx.font_size("caption"), bold=True,
                     color=ctx.color("on-surface-variant"), align="center")

            ctx.text(cx + 4, cy + 72, card_w - 8, 18,
                     str(member.get("title", "")),
                     size=ctx.font_size("annotation"),
                     color=ctx.color("on-surface-variant"), align="center")
