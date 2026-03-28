"""TimelinePanel — horizontal event timeline"""
from __future__ import annotations


class TimelinePanel:
    """Render a horizontal timeline with status dots and event details."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        events = props.get("events", []) or []
        if not events:
            return
        n      = len(events)
        ev_w   = max(140, (w - 32) // max(n, 1))
        line_y = y + h // 3

        ctx.divider(x + 16, line_y, w - 32,
                    color=ctx.color("border-subtle"))

        for i, ev in enumerate(events):
            if not isinstance(ev, dict):
                continue
            ex     = x + 16 + i * ev_w
            status = str(ev.get("status", "neutral"))
            dot_c, _ = ctx.status_color(status)
            dot_r  = 9

            ctx.ellipse(ex + ev_w // 2 - dot_r, line_y - dot_r,
                        dot_r * 2, dot_r * 2,
                        fill=dot_c, stroke=ctx.color("surface"))

            ctx.text(ex, line_y - 36, ev_w, 24,
                     str(ev.get("date", "")),
                     size=ctx.font_size("annotation"), bold=True,
                     color=ctx.color("primary"), align="center")

            ctx.text(ex, line_y + 14, ev_w, 22,
                     str(ev.get("label", "")),
                     size=ctx.font_size("caption"), bold=True,
                     color=ctx.color("on-surface"), align="center")

            desc = str(ev.get("description", ""))
            if desc:
                ctx.text(ex, line_y + 38, ev_w, 34, desc,
                         size=ctx.font_size("annotation"),
                         color=ctx.color("on-surface-variant"),
                         align="center")
