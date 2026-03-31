"""RoleCard — job role with primary header strip and bullet responsibilities"""
from __future__ import annotations

from rendering.atoms.text.bullet_list import BulletListAtom


class RoleCard:
    """Render a role card with a coloured header strip and responsibility bullets."""

    @staticmethod
    def _normalize_items(items_raw) -> list[str]:
        items: list[str] = []
        if not isinstance(items_raw, list):
            return items
        for item in items_raw:
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

        title   = str(props.get("title",   ""))
        level   = str(props.get("level",   ""))
        reports = str(props.get("reports-to", ""))
        resps   = self._normalize_items(props.get("responsibilities", []) or [])

        inner_w = w - pad * 2
        title_color = ctx.card_title_color(props, default_token="text-default")
        subtitle_color = ctx.card_subtitle_color(props, default_token="text-secondary")
        body_color = ctx.card_body_color(props, default_token="text-secondary")
        show_header = bool(title or level) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)

        header_h = ctx.card_header_h(w, h, props)
        header_gap = ctx.card_header_gap(h, props)
        header_y = y + pad
        content_y = header_y

        level_gap = ctx.spacing("s")
        level_text_size = ctx.fit_text_size(
            level,
            max(40, int(inner_w * 0.34)),
            max_size=ctx.font_size("caption"),
            min_size=ctx.font_size("annotation"),
            bold=True,
            safety=0.92,
        ) if level else ctx.font_size("annotation")
        level_badge_w = 0
        if level:
            level_badge_w = max(44, min(int(inner_w * 0.38), int(ctx.estimate_text_width(level, level_text_size, bold=True)) + ctx.spacing("m")))
        title_w = max(40, inner_w - level_badge_w - (level_gap if level_badge_w else 0))

        if show_header:
            title_size = ctx.card_header_font_size(title, title_w, h, props)
            if title:
                ctx.text(x + pad, header_y, title_w, header_h, title,
                         size=title_size, bold=True,
                         color=title_color,
                         align=ctx.card_header_align(props, default="left"), valign="middle",
                         inner_margin=0)

            if level:
                badge_h = max(20, min(header_h, int(level_text_size * 1.7)))
                badge_y = header_y + max(0, (header_h - badge_h) // 2)
                badge_x = x + w - pad - level_badge_w
                ctx.badge(badge_x, badge_y, level_badge_w, badge_h, level,
                          fill=ctx.color("primary-container"),
                          text_color=ctx.color("on-primary-container"),
                          size=level_text_size, radius=ctx.rad())

            content_y = header_y + header_h + header_gap

        if show_header_line:
            line_x, line_w = ctx.card_divider_span("header", x + pad, inner_w, props)
            ctx.divider(line_x, content_y, line_w,
                        color=ctx.card_line_color("header", ctx.color("line-default"), props))
            content_y += max(ctx.spacing("s"), int(h * 0.02))

        reports_h = 0
        if reports:
            reports_size = ctx.fit_text_size(
                f"Reports to: {reports}",
                inner_w,
                max_size=ctx.card_footer_font_size(props),
                min_size=ctx.font_size("annotation"),
                bold=False,
                safety=0.94,
            )
            reports_h = max(18, int(reports_size * 1.55))
            ctx.text(x + pad, content_y, inner_w, reports_h,
                     f"Reports to: {reports}",
                     size=reports_size, italic=ctx.card_footer_italic(props),
                     color=subtitle_color,
                     align="left", valign="middle", inner_margin=0)
            content_y += reports_h + max(ctx.spacing("s"), int(h * 0.018))

        content_bottom = y + h - pad
        list_h = max(0, content_bottom - content_y)
        if resps and list_h > 16:
            item_count = max(1, len(resps))
            target_item_h = max(22, list_h // item_count)
            bullet_size = max(
                ctx.font_size("annotation"),
                min(ctx.font_size("body"), int(target_item_h * 0.56))
            )
            BulletListAtom().render(
                ctx,
                x + pad,
                content_y,
                inner_w,
                list_h,
                items=resps,
                color=body_color,
                size=bullet_size,
            )
