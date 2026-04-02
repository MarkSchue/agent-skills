"""LocationCard — site info with icon rows"""
from __future__ import annotations


class LocationCard:
    """Render a location/office info card with optional title header and icon-prefixed rows."""

    def preferred_font_sizes(self, ctx, props: dict, w: int, h: int) -> dict:
        """Return the natural content-row text size for the template pre-pass."""
        pad = ctx.card_pad_px(w, h, props)
        title = str(props.get("title", "") or props.get("name", "") or "").strip()
        header_h = ctx.card_title_h(w, h, props) if title else 0
        header_gap = ctx.card_title_gap(h, props) if title else 0
        rows = [v for _, v in [
            ("location", props.get("site-name", "") or props.get("city", "")),
            ("building", props.get("address", "")),
            ("people",   props.get("headcount", "")),
            ("timezone", props.get("timezone", "")),
            ("contact",  props.get("contact", "")),
        ] if str(v).strip()]
        n_rows = max(1, len(rows))
        available_h = max(32, h - pad * 2 - header_h - header_gap)
        row_h = max(28, available_h // n_rows)
        text_sz = max(ctx.font_size("body"), min(ctx.font_size("heading-sub"), int(row_h * 0.45)))
        return {"body": text_sz}

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        pad     = ctx.card_pad_px(w, h, props)
        inner_w = w - pad * 2
        title   = str(props.get("title", "") or props.get("name", "") or "").strip()

        show_header      = bool(title) and ctx.card_section_enabled(props, "title", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "title", default=True)
        title_color  = ctx.card_title_color(props, default_token="text-default")
        header_align = ctx.card_title_align(props, default="left")
        div_color    = ctx.card_line_color("title", ctx.color("line-default"), props)

        cy = y + pad

        # ── Optional title header ─────────────────────────────────────────
        if show_header:
            header_h   = ctx.card_title_h(w, h, props)
            header_gap = ctx.card_title_gap(h, props)
            title_size = ctx.card_title_font_size(title, inner_w, h, props)
            ctx.text(x + pad, cy, inner_w, header_h,
                     title, size=title_size, bold=True,
                     color=title_color, align=header_align, valign="middle")
            cy += header_h + header_gap
            if show_header_line:
                lx, lw = ctx.card_divider_span("title", x + pad, inner_w, props)
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
        # Text size: harmonized with slide via slide_font_size; falls back to responsive
        # formula when no slide pre-pass has been run.
        text_sz  = ctx.slide_font_size("body", props)
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
