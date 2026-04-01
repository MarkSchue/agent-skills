"""DataInsightPanel — bullet-list insight panel"""
from __future__ import annotations

from rendering.atoms.text.bullet_list import BulletListAtom  # type: ignore[import]


class DataInsightPanel:
    """Render a titled bullet-list insight panel with optional timeframe."""

    @staticmethod
    def _normalize_insights(insights_raw) -> list[str]:
        """Normalize insight items to plain text strings."""
        items: list[str] = []
        if not isinstance(insights_raw, list):
            return items
        for item in insights_raw:
            if isinstance(item, dict):
                text = str(item.get("text", "") or item.get("body", "") or item.get("value", "")).strip()
            else:
                text = str(item).strip()
            if text:
                items.append(text)
        return items

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        pad = ctx.card_pad_px(w, h, props)
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        title     = str(props.get("title",     "Insights"))
        insights  = self._normalize_insights(props.get("insights", []) or [])
        timeframe = str(props.get("timeframe", ""))

        # Alignment — applies to header, bullets, and footer
        text_align   = str(props.get("text-align") or props.get("text_align") or "left").strip().lower()
        if text_align not in ("left", "center", "right"):
            text_align = "left"
        header_align = ctx.card_header_align(props, default=text_align)

        title_color  = ctx.card_title_color(props, default_token="text-default")
        body_color   = ctx.card_body_color(props, default_token="text-secondary")
        bullet_color = ctx.color("primary")
        show_header = bool(title) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)
        show_footer = bool(timeframe) and ctx.card_section_enabled(props, "footer", default=True)
        show_footer_line = show_footer and ctx.card_line_enabled(props, "footer", default=True)

        title_h = ctx.card_header_h(w, h, props)
        section_gap = ctx.card_header_gap(h, props)

        content_top = y + pad
        if show_header:
            title_sz = ctx.card_header_font_size(title, w - pad * 2, h, props)
            ctx.text(x + pad, content_top, w - pad * 2, title_h, title,
                     size=title_sz, bold=True,
                     color=title_color, align=header_align, valign="middle")
            content_top += title_h + section_gap

        if show_header_line:
            line_x, line_w = ctx.card_divider_span("header", x + pad, w - pad * 2, props)
            ctx.divider(line_x, content_top, line_w,
                        color=ctx.card_line_color("header", ctx.color("line-default"), props))
            content_top += section_gap

        footer_h      = ctx.card_footer_h(h, props) if show_footer else 0
        footer_gap    = ctx.card_footer_gap(h, props) if show_footer else section_gap
        footer_size   = ctx.card_footer_font_size(props)
        footer_color  = ctx.card_footer_color(props, default_token="text-secondary")
        footer_italic = ctx.card_footer_italic(props)
        footer_y      = y + h - pad - footer_h
        content_bottom = footer_y - footer_gap if show_footer else y + h - pad

        if show_footer_line:
            divider_y = footer_y - footer_gap
            line_x, line_w = ctx.card_divider_span("footer", x + pad, w - pad * 2, props)
            ctx.divider(line_x, divider_y, line_w,
                        color=ctx.card_line_color("footer", ctx.color("line-default"), props))
            content_bottom = divider_y - footer_gap

        if insights:
            # show-bullets prop (default false for data-insight panels — clean prose look)
            raw_sb = props.get("show-bullets", props.get("show_bullets", False))
            show_bullets = str(raw_sb).lower() not in ("false", "no", "0") if isinstance(raw_sb, str) else bool(raw_sb)
            BulletListAtom().render(
                ctx,
                x + pad, content_top,
                w - pad * 2, content_bottom - content_top,
                items=insights,
                color=body_color,
                bullet_color=bullet_color,
                align=text_align,
                show_bullets=show_bullets,
            )

        if show_footer:
            ctx.text(x + pad, footer_y, w - pad * 2, footer_h, timeframe,
                     size=footer_size, italic=footer_italic,
                     color=footer_color,
                     align=text_align if text_align != "left" else "right",
                     valign="middle", inner_margin=0)
