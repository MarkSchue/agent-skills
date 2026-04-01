"""ContactCard — name, role, and contact details card"""
from __future__ import annotations


class ContactCard:
    """Render a contact card with name, role, and communication links."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        pad = ctx.card_pad_px(w, h, props)
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        name  = str(props.get("name",  ""))
        role  = str(props.get("role",  ""))
        detail = str(props.get("detail", ""))
        email = str(props.get("email", ""))
        url   = str(props.get("url",   ""))
        phone = str(props.get("phone", ""))
        header_align = ctx.card_header_align(props, default="left")
        title_color = ctx.card_title_color(props, default_token="text-on-muted")
        subtitle_color = ctx.card_subtitle_color(props, default_token="text-secondary")
        body_color = ctx.card_body_color(props, default_token="text-secondary")
        show_header = bool(name or role) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)

        title_h = max(28, int(h * 0.09))
        subtitle_h = max(20, int(h * 0.06)) if role else 0
        section_gap = max(ctx.spacing("s"), int(h * 0.016))
        content_y = y + pad
        if show_header:
            ctx.text(x + pad, content_y, w - pad * 2, title_h, name,
                     size=ctx.font_size("heading-sub"), bold=True,
                     color=title_color, align=header_align, valign="middle")
            content_y += title_h
            if role:
                ctx.text(x + pad, content_y, w - pad * 2, subtitle_h, role,
                         size=ctx.font_size("caption"), color=subtitle_color,
                         align=header_align, valign="middle")
                content_y += subtitle_h
            content_y += section_gap

        if show_header_line:
            line_x, line_w = ctx.card_divider_span("header", x + pad, w - pad * 2, props)
            ctx.divider(line_x, content_y, line_w,
                        color=ctx.card_line_color("header", ctx.color("line-default"), props))
            content_y += section_gap

        ry = content_y
        row_sz    = ctx.font_size("caption")
        icon_sz   = max(18, int(row_sz * 1.4))
        row_h     = max(icon_sz, int(row_sz * 1.6))
        icon_gap  = max(6, ctx.spacing("s"))
        text_x    = x + pad + icon_sz + icon_gap
        text_w    = w - pad * 2 - icon_sz - icon_gap
        contact_rows = [
            ("email",   email or detail),
            ("web",     url),
            ("phone",   phone),
        ]
        for icon_name, val in contact_rows:
            if not val:
                continue
            ctx.draw_icon(x + pad, ry + (row_h - icon_sz) // 2,
                          icon_sz, icon_sz, icon_name, color=ctx.color("primary"))
            ctx.text(text_x, ry, text_w, row_h, val,
                     size=row_sz, color=body_color,
                     align="left", valign="middle", inner_margin=0)
            ry += row_h + max(4, ctx.spacing("xs"))
