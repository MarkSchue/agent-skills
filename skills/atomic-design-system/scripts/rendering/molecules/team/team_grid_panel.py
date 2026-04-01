"""TeamGridPanel — grid of mini member cards"""
from __future__ import annotations


class TeamGridPanel:
    """Render a grid of compact team member cards with avatar, name, and title."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        members = props.get("members", []) or []
        cols    = int(props.get("columns", 3))
        title   = str(props.get("title",   ""))

        gutter  = max(8, int(min(w, h) * 0.012))
        n_rows  = max(1, -(-len(members) // max(cols, 1)))  # ceiling div
        title_h = 0
        if title:
            title_h = max(24, int(h * 0.07))
            ctx.text(x, y, w, title_h, title,
                     size=ctx.font_size("label"), bold=True,
                     color=ctx.color("on-surface"), align="left", valign="middle")
            y += title_h + gutter

        card_w = (w - (cols - 1) * gutter) // cols
        avail_h = h - title_h - (gutter if title else 0)
        card_h  = max(80, (avail_h - (n_rows - 1) * gutter) // max(n_rows, 1))

        for i, member in enumerate(members):
            if not isinstance(member, dict):
                continue
            col = i % cols
            row = i // cols
            cx  = x + col * (card_w + gutter)
            cy  = y + row * (card_h + gutter)

            ctx.rect(cx, cy, card_w, card_h,
                     fill=ctx.card_bg_color(props, "bg-card"),
                     stroke=ctx.color("border-default"),
                     radius=ctx.rad())

            av_r = min(int(card_h * 0.22), int(card_w * 0.28), 28)
            av_top = cy + max(6, int(card_h * 0.08))
            ctx.ellipse(cx + card_w // 2 - av_r, av_top,
                        av_r * 2, av_r * 2,
                        fill=ctx.color("primary"))

            text_y    = av_top + av_r * 2 + max(4, int(card_h * 0.06))
            name_h    = max(16, int(card_h * 0.20))
            role_h    = max(14, int(card_h * 0.16))
            text_pad  = max(4, int(card_w * 0.04))

            ctx.text(cx + text_pad, text_y, card_w - text_pad * 2, name_h,
                     str(member.get("name", "")),
                     size=ctx.font_size("caption"), bold=True,
                     color=ctx.color("on-surface-variant"),
                     align="center", valign="middle", inner_margin=0)

            ctx.text(cx + text_pad, text_y + name_h, card_w - text_pad * 2, role_h,
                     str(member.get("title", "")),
                     size=ctx.font_size("annotation"),
                     color=ctx.color("on-surface-variant"),
                     align="center", valign="middle", inner_margin=0)
