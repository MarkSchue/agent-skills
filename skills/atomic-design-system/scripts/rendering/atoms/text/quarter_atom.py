"""
QuarterAtom — numbered/icon quarter cell
==========================================
Renders a single "quarter" section cell consisting of:

  1. **Badge line** — a number (e.g. "01") *or* an icon, rendered in the
     theme accent colour (configurable via ``accent_color``).
  2. **Headline** — bold text, typically 1–2 lines.
  3. **Body text** — normal-weight descriptive paragraph beneath the headline.

All three elements share the same horizontal alignment (``align``), which
defaults to ``"left"`` and can be set to ``"center"`` or ``"right"``.

Colour roles
------------
``accent_color``  — hex color for the badge/number (usually ``primary``)
``title_color``   — hex color for the headline text
``body_color``    — hex color for the body paragraph

Usage::

    from rendering.atoms.text.quarter_atom import QuarterAtom

    QuarterAtom().render(
        ctx, x, y, w, h,
        label="01",
        icon="",
        headline="Headline\\nzwei Zeilen",
        text="Lorem ipsum dolor sit amet …",
        align="left",
        accent_color=ctx.color("primary"),
        title_color=ctx.color("on-surface"),
        body_color=ctx.color("on-surface-variant"),
    )
"""

from __future__ import annotations


class QuarterAtom:
    """Render a single numbered/icon quarter cell."""

    def render(
        self,
        ctx,
        x: int,
        y: int,
        w: int,
        h: int,
        *,
        label: str = "",
        icon: str = "",
        headline: str = "",
        text: str = "",
        align: str = "left",
        accent_color: str = "",
        title_color: str = "",
        body_color: str = "",
    ) -> None:
        """
        Parameters
        ----------
        ctx           : RenderContext (DrawioCtx or PptxCtx)
        x, y          : top-left corner of the cell bounding box
        w, h          : width and height of the cell bounding box
        label         : short badge string, e.g. "01", "02" — shown in accent color
        icon          : Material Icons concept name (overrides ``label`` if both given)
        headline      : headline text; ``\\n`` produces a second line
        text          : body paragraph text
        align         : "left" | "center" | "right" (default "left")
        accent_color  : hex color for the label/icon (default: primary token)
        title_color   : hex color for the headline (default: on-surface token)
        body_color    : hex color for the body text (default: on-surface-variant token)
        """
        accent_color = accent_color or ctx.color("primary")
        title_color  = title_color  or ctx.color("on-surface")
        body_color   = body_color   or ctx.color("on-surface-variant")

        pad = ctx.PAD

        # ── proportional heights ───────────────────────────────────────────────
        badge_h    = max(28, int(h * 0.14))   # "01" / icon row
        headline_h = max(40, int(h * 0.28))   # bold 1–2-line heading
        gap_s      = max(4, ctx.spacing("s"))
        # body gets the remainder
        body_y  = y + pad + badge_h + gap_s + headline_h + gap_s
        body_h  = max(20, (y + h - pad) - body_y)

        badge_sz = max(ctx.font_size("heading-sub"), min(32, badge_h - 4))

        # ── 1. Badge: icon (if given) or label number ──────────────────────────
        if icon:
            icon_s = badge_h
            ctx.draw_icon(x + pad, y + pad, icon_s, icon_s, icon,
                          color=accent_color)
        elif label:
            ctx.text(x + pad, y + pad, w - pad * 2, badge_h, label,
                     size=badge_sz, bold=True, color=accent_color,
                     align=align, valign="middle")

        # ── 2. Headline ────────────────────────────────────────────────────────
        headline_y = y + pad + badge_h + gap_s
        headline_sz = max(ctx.font_size("heading-sub"),
                          min(ctx.font_size("heading"), int(headline_h * 0.44)))
        ctx.text(x + pad, headline_y, w - pad * 2, headline_h, headline,
                 size=headline_sz, bold=True, color=title_color,
                 align=align, valign="top")

        # ── 3. Body text ───────────────────────────────────────────────────────
        if text and body_h > 0:
            body_sz = max(ctx.font_size("caption"),
                          min(ctx.font_size("body"), int(body_h * 0.22)))
            ctx.text(x + pad, body_y, w - pad * 2, body_h, text,
                     size=body_sz, color=body_color,
                     align=align, valign="top")
