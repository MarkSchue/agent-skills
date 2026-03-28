"""LocationCard — site info with icon rows"""
from __future__ import annotations


class LocationCard:
    """Render a location/office info card with icon-prefixed rows."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        rows = [
            ("location",  props.get("site-name", "")),
            ("building",  props.get("address",   "")),
            ("people",    props.get("headcount", "")),
            ("timezone",  props.get("timezone",  "")),
        ]

        ry = y + 20
        for icon_name, val in rows:
            if not str(val).strip():
                continue
            ctx.draw_icon(x + 16, ry, 28, 24, icon_name, color=ctx.color("primary"))
            ctx.text(x + 48, ry, w - 64, 24, str(val),
                     size=ctx.font_size("caption"), color=ctx.color("on-surface-variant"))
            ry += 32
            if ry > y + h - 10:
                break
