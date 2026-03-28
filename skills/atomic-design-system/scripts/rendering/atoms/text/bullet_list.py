"""BulletListAtom — auto-sizing bullet list atom.

Renders a list of text items that scale dynamically to fill the
available bounding-box height.  Font size is clamped between the
``caption`` and ``body`` design tokens so it never becomes unreadably
tiny or awkwardly large.

Usage::

    from rendering.atoms.text.bullet_list import BulletListAtom

    BulletListAtom().render(
        ctx, x, y, w, h, items=["Item A", "Item B"], color=ctx.color("text-secondary")
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
        bullet: str = "•",
    ) -> None:
        """
        Parameters
        ----------
        ctx     : render context (DrawioCtx or PptxCtx)
        x, y    : top-left of the bounding box
        w, h    : width and height of the bounding box
        items   : list of strings to render as bullet points
        color   : text colour token resolved to a hex/colour string
        size    : explicit font size in pt; ``None`` = auto-fit to height
        bullet  : bullet character prepended to each item (default ``•``)
        """
        n = max(len(items), 1)

        # Distribute available height evenly among items; guarantee a minimum.
        item_h = max(22, h // n)

        if size is None:
            # Target ~58 % of item height, clamped between caption and body.
            clamped = int(item_h * 0.58)
            size = max(ctx.font_size("caption"),
                       min(ctx.font_size("body"), clamped))

        iy = y
        for item in items:
            text = (f"{bullet} {item}"
                    if not str(item).startswith(bullet)
                    else str(item))
            # Stop if rendering this item would overflow the box.
            if iy + item_h > y + h + 2:
                break
            ctx.text(x, iy, w, item_h, text,
                     size=size, color=color, valign="middle")
            iy += item_h
