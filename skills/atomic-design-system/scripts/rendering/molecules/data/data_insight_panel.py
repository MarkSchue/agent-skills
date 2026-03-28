"""DataInsightPanel — bullet-list insight panel"""
from __future__ import annotations

from rendering.atoms.text.bullet_list import BulletListAtom  # type: ignore[import]


class DataInsightPanel:
    """Render a titled bullet-list insight panel with optional timeframe."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        pad = max(ctx.PAD, ctx.spacing("m"))
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        title     = str(props.get("title",     "Insights"))
        insights  = props.get("insights", []) or []
        timeframe = str(props.get("timeframe", ""))
        header_align = ctx.card_header_align(props, default="left")
        title_color = ctx.card_title_color(props, default_token="text-on-muted")
        body_color = ctx.card_body_color(props, default_token="text-secondary")
        show_header = bool(title) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)
        show_footer = bool(timeframe) and ctx.card_section_enabled(props, "footer", default=True)
        show_footer_line = show_footer and ctx.card_line_enabled(props, "footer", default=True)

        title_h = max(28, int(h * 0.09))
        section_gap = max(ctx.spacing("s"), int(h * 0.016))

        content_top = y + pad
        if show_header:
            ctx.text(x + pad, content_top, w - pad * 2, title_h, title,
                     size=ctx.font_size("heading-sub"), bold=True,
                     color=title_color, align=header_align, valign="middle")
            content_top += title_h + section_gap

        if show_header_line:
            line_x, line_w = ctx.card_divider_span("header", x + pad, w - pad * 2, props)
            ctx.divider(line_x, content_top, line_w,
                        color=ctx.card_line_color("header", ctx.color("line-default")))
            content_top += section_gap

        footer_h = max(20, int(h * 0.07)) if show_footer else 0
        footer_y = y + h - pad - footer_h
        content_bottom = footer_y - section_gap if show_footer else y + h - pad

        if show_footer_line:
            divider_y = footer_y - section_gap
            ctx.divider(x + pad, divider_y, w - pad * 2,
                        color=ctx.card_line_color("footer", ctx.color("line-default")))
            content_bottom = divider_y - section_gap

        if insights:
            BulletListAtom().render(
                ctx,
                x + pad, content_top,
                w - pad * 2, content_bottom - content_top,
                items=insights,
                color=body_color,
            )

        if show_footer:
            ctx.text(x + pad, footer_y, w - pad * 2, footer_h, timeframe,
                     size=ctx.font_size("annotation"), italic=True,
                     color=body_color,
                     align="right", valign="middle")
