"""MissionCard — full-bleed mission/vision statement"""
from __future__ import annotations


class MissionCard:
    """Render a mission/vision card with title, divider, and statement body.

    Follows the same token-driven header/divider/body pattern as all other cards.
    Icon badge uses --color-kpi-icon-bg / --color-kpi-icon-fg tokens.
    All alignment, color, and section-visibility props are respected.
    """

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               body: str = "") -> None:
        # Consistent padding + header height via centralized helpers
        card_pad = ctx.card_pad_px(w, h)
        inner_w  = w - card_pad * 2

        # ── Card frame ─────────────────────────────────────────────────────
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        title     = str(props.get("title", ""))
        statement = (str(props.get("statement", "")) or
                     str(props.get("mission",   "")) or
                     str(body or ""))
        icon_raw  = str(props.get("icon-name", "") or props.get("icon", ""))

        show_header      = bool(title or icon_raw) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)

        # ── Token resolution — identical to ChartCard contract ─────────────
        title_color   = ctx.card_title_color(props, default_token="text-default")
        body_color    = ctx.card_body_color(props, default_token="text-default")
        header_align  = ctx.card_header_align(props, default="left")
        divider_color = ctx.card_line_color("header", ctx.color("line-default"))
        icon_bg       = ctx.icon_bg(props)
        icon_fg       = ctx.icon_fg(props)

        # icon badge + centralized header height so divider aligns with neighbours
        icon_size   = ctx.icon_size(w, h) if icon_raw else 0
        header_h    = ctx.card_header_h(w, h)
        icon_size   = min(icon_size, header_h)  # never overflow header zone onto divider
        icon_radius = ctx.icon_radius(icon_size) if icon_raw else 0
        header_gap  = ctx.card_header_gap(h)

        current_y = y + card_pad

        # ── Header row: title (left) + icon badge (right) — same as ChartCard
        if show_header:
            text_w     = inner_w - (icon_size + header_gap if icon_raw else 0)
            title_size = ctx.card_header_font_size(title, max(40, text_w), h)
            if title:
                ctx.text(x + card_pad, current_y, max(40, text_w), header_h, title,
                         size=title_size, bold=True,
                         color=title_color,
                         align=header_align, valign="middle")

            if icon_raw:
                icon_x = x + w - card_pad - icon_size
                icon_y = current_y + max(0, (header_h - icon_size) // 2)
                ctx.rect(icon_x, icon_y, icon_size, icon_size,
                         fill=icon_bg, stroke=ctx.icon_stroke(props), radius=icon_radius)
                ctx.draw_icon(icon_x, icon_y, icon_size, icon_size, icon_raw, color=icon_fg)

            current_y += header_h + header_gap

        # ── Header divider ─────────────────────────────────────────────────
        if show_header_line:
            line_x, line_w = ctx.card_divider_span("header", x + card_pad, inner_w, props)
            ctx.divider(line_x, current_y, line_w, color=divider_color)
            current_y += max(12, int(h * 0.024))

        # ── Statement body ─────────────────────────────────────────────────
        remaining_h = y + h - current_y - card_pad
        if remaining_h > 0 and statement:
            ctx.text(x + card_pad, current_y, inner_w, remaining_h, statement,
                     size=ctx.font_size("body"),
                     color=body_color,
                     align=header_align, valign="top")
