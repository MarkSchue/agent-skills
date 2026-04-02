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
        # job-title is canonical; role kept as backward-compat alias
        role  = str(props.get("job-title") or props.get("role") or "")
        detail = str(props.get("detail", ""))
        email = str(props.get("email", ""))
        url   = str(props.get("url",   ""))
        phone = str(props.get("phone", ""))
        header_align = ctx.card_title_align(props, default="left")
        title_color = ctx.card_title_color(props, default_token="text-on-muted")
        subtitle_color = ctx.card_subtitle_color(props, default_token="text-secondary")
        body_color = ctx.card_body_color(props, default_token="text-secondary")
        show_header = bool(name or role) and ctx.card_section_enabled(props, "title", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "title", default=True)

        title_h     = ctx.card_title_h(w, h, props)
        title_size  = ctx.card_title_font_size(name or role, w - pad * 2, h, props)
        sub_sz      = max(ctx.font_size("annotation"), ctx.font_size("caption"))
        subtitle_h  = max(int(title_h * 0.70), int(sub_sz * 1.4)) if role else 0
        section_gap = max(ctx.spacing("s"), ctx.card_title_gap(h, props))
        content_y = y + pad
        if show_header:
            ctx.text(x + pad, content_y, w - pad * 2, title_h, name,
                     size=title_size, bold=True,
                     color=title_color, align=header_align, valign="middle")
            content_y += title_h
            if role:
                ctx.text(x + pad, content_y, w - pad * 2, subtitle_h, role,
                         size=sub_sz, color=subtitle_color,
                         align=header_align, valign="middle")
                content_y += subtitle_h
            content_y += section_gap

        if show_header_line:
            line_x, line_w = ctx.card_divider_span("title", x + pad, w - pad * 2, props)
            ctx.divider(line_x, content_y, line_w,
                        color=ctx.card_line_color("title", ctx.color("line-default"), props))
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
