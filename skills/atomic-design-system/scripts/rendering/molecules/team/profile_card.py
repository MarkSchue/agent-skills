"""ProfileCard — circle avatar + name, title, department, bio, email"""
from __future__ import annotations


class ProfileCard:
    """Render a centred profile card with avatar circle and contact info."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        pad = ctx.card_pad_px(w, h, props)
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        name       = str(props.get("name",       ""))
        title_text = str(props.get("title",      ""))
        dept       = str(props.get("department", ""))
        bio        = str(props.get("bio",        ""))
        email      = str(props.get("email",      ""))

        inner_w = w - pad * 2
        av_r    = min(int(h * 0.13), int(w * 0.22), 52)
        av_d    = av_r * 2
        gap     = max(ctx.spacing("xs"), int(h * 0.016))

        # Responsive row heights
        name_h  = max(22, int(h * 0.08))
        title_h = max(18, int(h * 0.06))
        dept_h  = max(20, int(h * 0.06)) if dept  else 0
        bio_h   = max(36, int(h * 0.14)) if bio   else 0
        email_h = max(16, int(h * 0.05)) if email else 0

        block_h = (av_d + gap + name_h + gap // 2 + title_h
                   + (gap + dept_h  if dept  else 0)
                   + (gap + bio_h   if bio   else 0)
                   + (gap + email_h if email else 0))
        start_y = y + max(pad, (h - block_h) // 2)

        # Avatar — shape follows design-system language:
        # expressive (radius-large >= 20, e.g. Material) → circular
        # geometric  (radius-large <  20, e.g. Carbon)   → rounded-square photo frame
        _av_r = ctx.rad("radius-large")
        if _av_r >= 20:
            ctx.ellipse(x + w // 2 - av_r, start_y, av_d, av_d,
                        fill=ctx.color("primary"),
                        stroke=ctx.color("surface"))
        else:
            ctx.rect(x + w // 2 - av_r, start_y, av_d, av_d,
                     fill=ctx.color("primary"),
                     stroke=ctx.color("surface"), radius=_av_r)

        ty = start_y + av_d + gap
        ctx.text(x + pad, ty, inner_w, name_h, name,
                 size=ctx.font_size("label"), bold=True,
                 color=ctx.color("text-default"), align="center", valign="middle")

        ty += name_h + gap // 2
        ctx.text(x + pad, ty, inner_w, title_h, title_text,
                 size=ctx.font_size("caption"), color=ctx.color("text-secondary"),
                 align="center", valign="middle")

        ty += title_h + gap
        if dept:
            badge_w = min(inner_w, max(80, len(dept) * 9 + 24))
            bx = x + (w - badge_w) // 2
            ctx.badge(bx, ty, badge_w, dept_h, dept,
                      fill=ctx.color("secondary"),
                      text_color=ctx.color("on-secondary"),
                      size=ctx.font_size("annotation"), radius=ctx.rad())
            ty += dept_h + gap

        if bio:
            ctx.text(x + pad, ty, inner_w, bio_h, bio,
                     size=ctx.font_size("annotation"),
                     color=ctx.color("text-secondary"), align="center", valign="top")
            ty += bio_h + gap

        if email:
            ctx.text(x + pad, ty, inner_w, email_h, email,
                     size=ctx.font_size("annotation"), italic=True,
                     color=ctx.color("text-secondary"), align="center", valign="middle")
