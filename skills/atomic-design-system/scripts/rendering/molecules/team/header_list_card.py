"""HeaderListCard — avatar header + item grid + CTA footer"""
from __future__ import annotations


class HeaderListCard:
    """Render a card with avatar header, a two-column item grid, and a CTA button."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        pad = ctx.card_pad_px(w, h, props)
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        av_r    = min(22, int(h * 0.06))
        strip_h = max(52, int(h * 0.13))
        av_cx   = x + pad + av_r
        av_cy   = y + strip_h // 2
        header_name   = str(props.get("header-name",   ""))
        header_detail = str(props.get("header-detail", ""))
        show_header = bool(header_name or header_detail) and ctx.card_section_enabled(props, "title", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "title", default=True)

        txt_x = av_cx + av_r + pad
        txt_w = w - (txt_x - x) - pad

        content_top = y + pad
        if show_header:
            ctx.ellipse(av_cx - av_r, av_cy - av_r,
                        av_r * 2, av_r * 2,
                        fill=ctx.avatar_bg(props),
                        stroke=ctx.color("surface"))

            name_sz   = ctx.font_size("label")
            detail_sz = ctx.font_size("annotation")
            row_h_n   = max(18, int(name_sz * 1.4))
            row_h_d   = max(14, int(detail_sz * 1.4))
            mid = y + strip_h // 2
            ctx.text(txt_x, mid - row_h_n, txt_w, row_h_n, header_name,
                     size=name_sz, bold=True, color=ctx.color("on-surface"),
                     align="left", valign="middle", inner_margin=0)
            if header_detail:
                ctx.text(txt_x, mid, txt_w, row_h_d, header_detail,
                         size=detail_sz, color=ctx.color("on-surface-variant"),
                         align="left", valign="middle", inner_margin=0)

            content_top = y + strip_h + ctx.spacing("s")

        if show_header_line:
            ctx.divider(x + pad, y + strip_h, w - pad * 2,
                        color=ctx.card_line_color("title", ctx.color("line-default"), props))

        sec_lbl   = str(props.get("section-label", ""))
        sec_lbl_y = content_top
        sec_sz    = ctx.font_size("caption")
        sec_lbl_h = max(18, int(sec_sz * 1.5))
        if sec_lbl:
            ctx.text(x + pad, sec_lbl_y, w - pad * 2, sec_lbl_h, sec_lbl,
                     size=sec_sz, color=ctx.color("on-surface-variant"),
                     align="left", valign="middle", inner_margin=0)

        items     = props.get("items") or []
        gutter    = max(8, int(w * 0.012))
        pc_y      = sec_lbl_y + (sec_lbl_h + ctx.spacing("xs") if sec_lbl else ctx.spacing("xs"))
        pc_w      = (w - pad * 2 - gutter) // 2

        # Responsive inner item-card geometry
        IPAD    = max(8, int(pc_w * 0.06))
        lbl_sz  = ctx.font_size("caption")
        ann_sz  = ctx.font_size("annotation")
        lbl_h   = max(18, int(lbl_sz * 1.4))
        sq_sz   = max(12, int(lbl_sz * 0.9))
        sq_gap  = max(4, ctx.spacing("xs"))
        txt_gap = max(4, ctx.spacing("xs"))
        ttl_h   = max(16, int(ann_sz * 1.4))
        det_h   = max(28, int(ann_sz * 2.6))
        det_gap = max(2, ctx.spacing("xs") // 2)
        pc_h    = IPAD + lbl_h + sq_gap + sq_sz + txt_gap + ttl_h + det_gap + det_h + IPAD
        pc_h    = max(pc_h, int(h * 0.30))

        for i, appt in enumerate(items[:2]):
            if not isinstance(appt, dict):
                continue
            pcx = x + PAD + i * (pc_w + gutter)
            ctx.rect(pcx, pc_y, pc_w, pc_h,
                     fill=ctx.color("surface"),
                     stroke=ctx.color("border-subtle"),
                     radius=ctx.rad())

            item_label  = str(appt.get("item-label",  "") or appt.get("label", ""))
            # job-title is canonical; item-title kept as backward-compat alias
            item_title  = str(appt.get("job-title") or appt.get("item-title") or appt.get("headline") or "")
            # body is canonical; item-detail kept as backward-compat alias
            item_detail = str(appt.get("body") or appt.get("item-detail") or "")

            # row 1 — label
            ctx.text(pcx + IPAD, pc_y + IPAD, pc_w - IPAD * 2, lbl_h, item_label,
                     size=lbl_sz, bold=True, color=ctx.color("on-surface"),
                     align="left", valign="middle", inner_margin=0)

            # row 2 — bullet square
            sq_y = pc_y + IPAD + lbl_h + sq_gap
            ctx.rect(pcx + IPAD, sq_y, sq_sz, sq_sz,
                     fill=ctx.color("surface-variant"), radius=max(2, sq_sz // 4))

            # row 3 — title directly beneath bullet
            ttl_y = sq_y + sq_sz + txt_gap
            ctx.text(pcx + IPAD, ttl_y, pc_w - IPAD * 2, ttl_h, item_title,
                     size=ann_sz, bold=True, color=ctx.color("on-surface"),
                     align="left", valign="middle", inner_margin=0)

            # row 4 — detail beneath title
            if item_detail:
                det_y = ttl_y + ttl_h + det_gap
                ctx.text(pcx + IPAD, det_y, pc_w - IPAD * 2, det_h, item_detail,
                         size=ann_sz, color=ctx.color("on-surface-variant"),
                         align="left", valign="top", inner_margin=0)

        footer_bar_h = max(40, int(h * 0.09))
        fb_y         = y + h - footer_bar_h
        cta_label    = str(props.get("cta-label", ""))
        if cta_label:
            cta_btn_h = max(28, int(footer_bar_h * 0.75))
            cta_w = max(100, int(ctx.estimate_text_width(cta_label, ctx.font_size("caption"), bold=False)) + pad * 2)
            cta_x = x + w - cta_w - pad
            ctx.badge(cta_x, fb_y + (footer_bar_h - cta_btn_h) // 2, cta_w, cta_btn_h,
                      cta_label,
                      fill=ctx.color("primary"),
                      text_color=ctx.color("on-primary"),
                      size=ctx.font_size("caption"), radius=ctx.rad())
