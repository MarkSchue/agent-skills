"""RoleCard — job role with primary header strip and bullet responsibilities"""
from __future__ import annotations


class RoleCard:
    """Render a role card with a coloured header strip and responsibility bullets."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        title   = str(props.get("title",   ""))
        level   = str(props.get("level",   ""))
        reports = str(props.get("reports-to", ""))
        resps   = props.get("responsibilities", []) or []

        # Header strip (rounded top, square bottom)
        ctx.rect(x, y, w, 54,
                 fill=ctx.color("primary"), radius=ctx.rad())
        ctx.rect(x, y + 30, w, 24,
                 fill=ctx.color("primary"))

        ctx.text(x + 16, y + 14, w - 72, 26, title,
                 size=ctx.font_size("label"), bold=True, color=ctx.color("on-primary"))

        if level:
            ctx.badge(x + w - 58, y + 15, 42, 22, level,
                      fill=ctx.color("on-primary"),
                      text_color=ctx.color("primary"),
                      size=ctx.font_size("annotation"))

        ry = y + 62
        if reports:
            ctx.text(x + 16, ry, w - 32, 20,
                     f"Reports to: {reports}",
                     size=ctx.font_size("annotation"), italic=True,
                     color=ctx.color("on-surface-variant"))
            ry += 28

        for resp in (resps or [])[:6]:
            ctx.text(x + 16, ry, 14, 18, "•",
                     size=ctx.font_size("label"), color=ctx.color("primary"), align="center")
            ctx.text(x + 34, ry, w - 50, 20, str(resp),
                     size=ctx.font_size("caption"), color=ctx.color("on-surface-variant"))
            ry += 26
            if ry > y + h - 10:
                break
