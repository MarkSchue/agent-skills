"""LocationCard — site info with icon rows"""
from __future__ import annotations


class LocationCard:
    """Render a location/office info card with optional title header and icon-prefixed rows."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        pad     = ctx.card_pad_px(w, h, props)
        inner_w = w - pad * 2
        title   = str(props.get("title", "") or props.get("name", "") or "").strip()

        show_header      = bool(title) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)
        title_color  = ctx.card_title_color(props, default_token="text-default")
        header_align = ctx.card_header_align(props, default="left")
        div_color    = ctx.card_line_color("header", ctx.color("line-default"), props)

        cy = y + pad

        # ── Optional title header ─────────────────────────────────────────
        if show_header:
            header_h   = ctx.card_header_h(w, h, props)
            header_gap = ctx.card_header_gap(h, props)
            title_size = ctx.card_header_font_size(title, inner_w, h, props)
            ctx.text(x + pad, cy, inner_w, header_h,
                     title, size=title_size, bold=True,
                     color=title_color, align=header_align, valign="middle")
            cy += header_h + header_gap
            if show_header_line:
                lx, lw = ctx.card_divider_span("header", x + pad, inner_w, props)
                ctx.divider(lx, cy, lw, color=div_color)
                cy += 1 + ctx.spacing("m")

        # ── Content rows ──────────────────────────────────────────────────
        rows = [
            ("location", props.get("site-name", "")  or props.get("city",     "")),
            ("building", props.get("address",   "")),
            ("people",   props.get("headcount", "")),
            ("timezone", props.get("timezone",  "")),
            ("contact",  props.get("contact",   "")),
        ]
        active_rows = [(icon, str(val).strip()) for icon, val in rows if str(val).strip()]
        if not active_rows:
            return

        # Responsive sizing: distribute remaining height evenly across rows
        content_bottom = y + h - pad
        available_h    = max(32, content_bottom - cy)
        n_rows         = len(active_rows)
        row_h          = max(28, available_h // n_rows)

        # Icon size: ~60 % of row height, capped
        icon_sz  = max(16, min(row_h - 4, int(row_h * 0.60)))
        # Text size: responsive to row height so fewer rows → larger text.
        # Floor is body (16), ceiling is heading-sub (24), scales at 45% of row height.
        text_sz  = max(ctx.font_size("body"), min(ctx.font_size("heading-sub"), int(row_h * 0.45)))
        icon_gap = ctx.spacing("s")
        text_x   = x + pad + icon_sz + icon_gap
        text_w   = max(24, inner_w - icon_sz - icon_gap)

        for icon_name, val in active_rows:
            icon_y = cy + max(0, (row_h - icon_sz) // 2)
            ctx.draw_icon(x + pad, icon_y, icon_sz, icon_sz,
                          icon_name, color=ctx.color("primary"))
            ctx.text(text_x, cy, text_w, row_h, val,
                     size=text_sz, color=ctx.color("on-surface-variant"),
                     valign="middle")
            cy += row_h
            if cy >= content_bottom:
                break
