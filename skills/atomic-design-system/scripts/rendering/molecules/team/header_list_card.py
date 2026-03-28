"""HeaderListCard — avatar header + item grid + CTA footer"""
from __future__ import annotations


class HeaderListCard:
    """Render a card with avatar header, a two-column item grid, and a CTA button."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        PAD = ctx.PAD
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        av_r    = min(22, int(h * 0.06))
        strip_h = max(52, int(h * 0.13))
        av_cx   = x + PAD + av_r
        av_cy   = y + strip_h // 2
        header_name   = str(props.get("header-name",   ""))
        header_detail = str(props.get("header-detail", ""))
        show_header = bool(header_name or header_detail) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)

        txt_x = av_cx + av_r + PAD
        txt_w = w - (txt_x - x) - PAD

        content_top = y + PAD
        if show_header:
            ctx.ellipse(av_cx - av_r, av_cy - av_r,
                        av_r * 2, av_r * 2,
                        fill=ctx.color("primary"),
                        stroke=ctx.color("surface"))

            ctx.text(txt_x, y + strip_h // 2 - 16, txt_w, 20, header_name,
                     size=ctx.font_size("label"), bold=True, color=ctx.color("on-surface"))
            if header_detail:
                ctx.text(txt_x, y + strip_h // 2 + 4, txt_w, 18, header_detail,
                         size=ctx.font_size("annotation"), color=ctx.color("on-surface-variant"))

            content_top = y + strip_h + 8

        if show_header_line:
            ctx.divider(x + PAD, y + strip_h, w - PAD * 2,
                        color=ctx.card_line_color("header", ctx.color("line-default")))

        sec_lbl   = str(props.get("section-label", ""))
        sec_lbl_y = content_top
        if sec_lbl:
            ctx.text(x + PAD, sec_lbl_y, w - PAD * 2, 20, sec_lbl,
                     size=ctx.font_size("caption"), color=ctx.color("on-surface-variant"))

        items     = props.get("items") or []
        gutter    = 10
        pc_y      = sec_lbl_y + (28 if sec_lbl else 4)
        pc_h      = max(80, int(h * 0.22))
        pc_w      = (w - PAD * 2 - gutter) // 2

        for i, appt in enumerate(items[:2]):
            if not isinstance(appt, dict):
                continue
            pcx = x + PAD + i * (pc_w + gutter)
            ctx.rect(pcx, pc_y, pc_w, pc_h,
                     fill=ctx.color("surface"),
                     stroke=ctx.color("border-subtle"),
                     radius=ctx.rad())

            item_label  = str(appt.get("item-label",  ""))
            item_title  = str(appt.get("item-title",  ""))
            item_detail = str(appt.get("item-detail", ""))

            ctx.text(pcx + 10, pc_y + 10, pc_w - 20, 22, item_label,
                     size=ctx.font_size("caption"), bold=True, color=ctx.color("on-surface"))

            pav_y = pc_y + 36
            ctx.rect(pcx + 10, pav_y, 24, 24,
                     fill=ctx.color("surface-variant"), radius=12)

            ctx.text(pcx + 10, pav_y + 28, pc_w - 20, 18, item_title,
                     size=ctx.font_size("annotation"), bold=True, color=ctx.color("on-surface"))
            if item_detail:
                ctx.text(pcx + 10, pav_y + 44, pc_w - 20, 16, item_detail,
                         size=ctx.font_size("annotation"), color=ctx.color("on-surface-variant"))

        footer_bar_h = max(40, int(h * 0.09))
        fb_y         = y + h - footer_bar_h
        cta_label    = str(props.get("cta-label", ""))
        if cta_label:
            cta_w = max(120, len(cta_label) * 9 + 32)
            cta_x = x + w - cta_w - PAD
            for bi in range(2):
                ic_x = x + PAD + bi * 44
                ctx.ellipse(ic_x, fb_y + (footer_bar_h - 36) // 2, 36, 36,
                             fill=ctx.color("surface-variant"),
                             stroke=ctx.color("border-subtle"))
            ctx.badge(cta_x, fb_y + (footer_bar_h - 36) // 2, cta_w, 36,
                      cta_label,
                      fill=ctx.color("primary"),
                      text_color=ctx.color("on-primary"),
                      size=ctx.font_size("caption"), radius=18)
