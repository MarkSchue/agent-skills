"""RoadmapPanel — three swim-lane roadmap"""
from __future__ import annotations


_LANE_FILLS = [
    "primary-container",
    "secondary-container",
    "surface-variant",
]


class RoadmapPanel:
    """Render a multi-lane roadmap panel with coloured item dots."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        lanes = props.get("lanes", []) or []
        if not lanes:
            return
        n      = len(lanes)
        lane_w = (w - 32 - (n - 1) * 16) // max(n, 1)

        for i, lane in enumerate(lanes):
            if not isinstance(lane, dict):
                continue
            lx   = x + 16 + i * (lane_w + 16)
            fill = ctx.color(_LANE_FILLS[i % len(_LANE_FILLS)])

            ctx.rect(lx, y + 8, lane_w, h - 16,
                     fill=fill, stroke=ctx.color("border-subtle"),
                     radius=ctx.rad())

            ctx.text(lx + 12, y + 16, lane_w - 24, 26,
                     str(lane.get("label", "")),
                     size=ctx.font_size("caption"), bold=True, color=ctx.color("on-surface"))

            ctx.divider(lx + 12, y + 48, lane_w - 24,
                        color=ctx.color("border-subtle"))

            iy = y + 58
            for item in (lane.get("items", []) or [])[:9]:
                if not isinstance(item, dict):
                    continue
                status = str(item.get("status", "neutral"))
                dot_c, _ = ctx.status_color(status)
                ctx.ellipse(lx + 12, iy + 3, 10, 10, fill=dot_c)

                ctx.text(lx + 28, iy, lane_w - 40, 20,
                         str(item.get("text", "")),
                         size=ctx.font_size("annotation"), bold=True,
                         color=ctx.color("on-surface"))

                desc = str(item.get("description", ""))
                if desc:
                    ctx.text(lx + 28, iy + 20, lane_w - 40, 18, desc,
                             size=ctx.font_size("annotation"), color=ctx.color("on-surface-variant"))

                iy += 44
                if iy > y + h - 20:
                    break
