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
        reports = str(props.get("reports-to", props.get("reports_to", "")))
        resps   = self._normalize_items(props.get("responsibilities", []) or [])

        # Customization props
        text_align   = str(props.get("text-align",   props.get("text_align",   "left")))
        bullet_color_key = props.get("bullet-color",  props.get("bullet_color", None))
        bullet_color = ctx.color(bullet_color_key) if bullet_color_key else ctx.color("primary")
        show_reports = str(props.get("show-reports",  props.get("show_reports", "true"))).lower() not in ("false", "no", "0")

        inner_w       = w - pad * 2
        title_color   = ctx.card_title_color(props, default_token="text-default")
        subtitle_color = ctx.card_subtitle_color(props, default_token="text-secondary")
        body_color    = ctx.card_body_color(props, default_token="text-secondary")

        show_header      = bool(title or level) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)

        header_h   = ctx.card_header_h(w, h, props)
        header_gap = ctx.card_header_gap(h, props)
        content_y  = y + pad

        # ── Header: title row + level badge on its own row ───────────────────
        if show_header:
            # Title row
            title_size = ctx.card_header_font_size(title, inner_w, h, props)
            if title:
                ctx.text(x + pad, content_y, inner_w, header_h, title,
                         size=title_size, bold=True,
                         color=title_color,
                         align=ctx.card_header_align(props, default="left"),
                         valign="middle", inner_margin=0)
            content_y += header_h

            # Level badge — full-width row, left-aligned, so it never overflows
            if level:
                level_text_size = ctx.fit_text_size(
                    level,
                    inner_w,
                    max_size=ctx.font_size("caption"),
                    min_size=ctx.font_size("annotation"),
                    bold=True,
                    safety=0.90,
                )
                badge_h = max(20, int(level_text_size * 1.8))
                badge_gap = max(4, int(h * 0.010))
                content_y += badge_gap
                # Badge width fits the text, capped at inner_w
                badge_w = min(inner_w,
                              max(48, int(ctx.estimate_text_width(level, level_text_size, bold=True))
                                  + ctx.spacing("m") * 2))
                ctx.badge(x + pad, content_y, badge_w, badge_h, level,
                          fill=ctx.color("primary-container"),
                          text_color=ctx.color("on-primary-container"),
                          size=level_text_size, radius=ctx.rad())
                content_y += badge_h

            content_y += header_gap

        if show_header_line:
            line_x, line_w = ctx.card_divider_span("header", x + pad, inner_w, props)
            ctx.divider(line_x, content_y, line_w,
                        color=ctx.card_line_color("header", ctx.color("line-default"), props))
            content_y += max(ctx.spacing("s"), int(h * 0.02))

        # ── Reports-to row (optional) ────────────────────────────────────────
        if reports and show_reports:
            reports_label = f"Reports to: {reports}"
            reports_size  = ctx.fit_text_size(
                reports_label,
                inner_w,
                max_size=ctx.card_footer_font_size(props),
                min_size=ctx.font_size("annotation"),
                bold=False,
                safety=0.94,
            )
            reports_h = max(18, int(reports_size * 1.55))
            ctx.text(x + pad, content_y, inner_w, reports_h,
                     reports_label,
                     size=reports_size, italic=ctx.card_footer_italic(props),
                     color=subtitle_color,
                     align=text_align, valign="middle", inner_margin=0)
            content_y += reports_h + max(ctx.spacing("s"), int(h * 0.018))

        # ── Responsibility bullets ────────────────────────────────────────────
        content_bottom = y + h - pad
        list_h = max(0, content_bottom - content_y)
        if resps and list_h > 16:
            item_count    = max(1, len(resps))
            target_item_h = max(24, list_h // item_count)
            # Responsive ceiling: heading-sub keeps bullets large enough to fill space
            bullet_size = max(
                ctx.font_size("body"),
                min(ctx.font_size("heading-sub"), int(target_item_h * 0.65))
            )
            BulletListAtom().render(
                ctx,
                x + pad,
                content_y,
                inner_w,
                list_h,
                items=resps,
                color=body_color,
                bullet_color=bullet_color,
                align=text_align,
                size=bullet_size,
            )
