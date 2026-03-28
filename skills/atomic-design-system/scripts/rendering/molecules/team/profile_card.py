"""ProfileCard — circle avatar + name, title, department, bio, email"""
from __future__ import annotations


class ProfileCard:
    """Render a centred profile card with avatar circle and contact info."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        PAD = ctx.PAD
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        name       = str(props.get("name",       ""))
        title_text = str(props.get("title",      ""))
        dept       = str(props.get("department", ""))
        bio        = str(props.get("bio",        ""))
        email      = str(props.get("email",      ""))

        av_r    = min(int(h * 0.13), int(w * 0.22), 52)
        av_d    = av_r * 2
        name_h  = 30
        title_h = 24
        dept_h  = 26 if dept  else 0
        bio_h   = 56 if bio   else 0
        email_h = 20 if email else 0
        gap     = 8
        block_h = (av_d + gap + name_h + gap // 2 + title_h
                   + (gap + dept_h  if dept  else 0)
                   + (gap + bio_h   if bio   else 0)
                   + (gap + email_h if email else 0))
        start_y = y + max(PAD, (h - block_h) // 2)

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
        ctx.text(x + PAD, ty, w - PAD * 2, name_h, name,
                 size=ctx.font_size("label"), bold=True,
                 color=ctx.color("text-default"), align="center")

        ty += name_h + gap // 2
        ctx.text(x + PAD, ty, w - PAD * 2, title_h, title_text,
                 size=ctx.font_size("caption"), color=ctx.color("text-secondary"), align="center")

        ty += title_h + gap
        if dept:
            badge_w = min(w - PAD * 2, max(80, len(dept) * 9 + 24))
            bx = x + (w - badge_w) // 2
            ctx.badge(bx, ty, badge_w, dept_h, dept,
                      fill=ctx.color("secondary"),
                      text_color=ctx.color("on-secondary"),
                      size=ctx.font_size("annotation"), radius=ctx.rad())
            ty += dept_h + gap

        if bio:
            ctx.text(x + PAD, ty, w - PAD * 2, bio_h, bio,
                     size=ctx.font_size("annotation"),
                     color=ctx.color("text-secondary"), align="center")
            ty += bio_h + gap

        if email:
            ctx.text(x + PAD, ty, w - PAD * 2, email_h, email,
                     size=ctx.font_size("annotation"), italic=True,
                     color=ctx.color("text-secondary"), align="center")
