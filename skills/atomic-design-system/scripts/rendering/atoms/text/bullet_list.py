"""BulletListAtom — auto-sizing bullet list atom.

Renders a list of text items that scale dynamically to fill the
available bounding-box height.  Font size is clamped between the
``caption`` and ``heading-sub`` design tokens so it never becomes
unreadably tiny or awkwardly large.

Usage::

    from rendering.atoms.text.bullet_list import BulletListAtom

    BulletListAtom().render(
        ctx, x, y, w, h, items=["Item A", "Item B"],
        color=ctx.color("text-secondary"),
        bullet_color=ctx.color("primary"),
        align="left",
    )
"""

from __future__ import annotations


class BulletListAtom:
    """Render a bullet list that fills the available height proportionally."""

    def render(
        self,
        ctx,
        x: int,
        y: int,
        w: int,
        h: int,
        items: list,
        color: str,
        *,
        size: int | None = None,
        bullet: str = "▪",
        bullet_color: str | None = None,
        align: str = "left",
        show_bullets: bool = True,
    ) -> None:
        """
        Parameters
        ----------
        ctx          : render context (DrawioCtx or PptxCtx)
        x, y         : top-left of the bounding box
        w, h         : width and height of the bounding box
        items        : list of strings to render as bullet points
        color        : body text colour
        size         : explicit font size in pt; ``None`` = auto-fit to height
        bullet       : bullet character (default ▪ — filled square, more visually distinct)
        bullet_color : colour for the bullet glyph; defaults to ``color`` when None
        align        : horizontal alignment of body text (``left`` / ``center`` / ``right``)
        """
        n = max(len(items), 1)
        _bullet_color = bullet_color if bullet_color else color

        # Distribute available height evenly; guarantee a minimum.
        item_h = max(24, h // n)

        if size is None:
            # Target ~65 % of item height, clamped between body and heading-sub.
            clamped = int(item_h * 0.65)
            size = max(ctx.font_size("body"),
                       min(ctx.font_size("heading-sub"), clamped))

        # Bullet glyph width: proportional to font size
        bullet_sz  = max(size - 2, ctx.font_size("body"))
        bullet_w   = max(16, int(bullet_sz * 1.1)) if show_bullets else 0
        bullet_gap = max(4, int(bullet_sz * 0.3))  if show_bullets else 0
        text_x     = x + bullet_w + bullet_gap
        text_w     = max(20, w - bullet_w - bullet_gap)

        # When centered we embed the bullet inside the same text block
        # (separate coloured rendering works best for left/right layouts).
        use_split = show_bullets and (align == "left" or align == "right") and bool(bullet)

        iy = y
        for item in items:
            if iy + item_h > y + h + 2:
                break

            if use_split:
                # Bullet column (always left-anchored for left; mirrored for right)
                bx = x if align == "left" else x + w - bullet_w
                ctx.text(bx, iy, bullet_w, item_h, bullet,
                         size=bullet_sz, bold=True,
                         color=_bullet_color,
                         align="center", valign="middle", inner_margin=0)
                tx = x + bullet_w + bullet_gap if align == "left" else x
                tw = max(20, w - bullet_w - bullet_gap)
                ctx.text(tx, iy, tw, item_h, str(item),
                         size=size, color=color,
                         align=align, valign="middle", inner_margin=0)
            else:
                # Center or no-bullet: single text block, embed bullet only when shown
                if show_bullets and bullet:
                    text = (f"{bullet}\u2009{item}"
                            if not str(item).startswith(bullet)
                            else str(item))
                else:
                    text = str(item)
                ctx.text(x, iy, w, item_h, text,
                         size=size, color=color,
                         align=align, valign="middle", inner_margin=0)

            iy += item_h
