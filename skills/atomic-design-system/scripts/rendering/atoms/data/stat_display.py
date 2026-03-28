"""
StatDisplayAtom — big-number stat display
==========================================
Renders a large numeric value with a small unit label and an optional
sub-label beneath. The block is vertically centered in the bounding box.
"""
from __future__ import annotations


class StatDisplayAtom:
    """Render a big-number stat: value (large) + unit (small) + optional sublabel."""

    def render(self, ctx, x: int, y: int, w: int, h: int,
               value: str, unit: str, sublabel: str,
               val_color: str, unit_color: str, sub_color: str,
               align: str = "left") -> None:
        """
        Parameters
        ----------
        ctx        : RenderContext
        x, y       : top-left position (pixels)
        w, h       : bounding box dimensions (pixels)
        value      : the large numeric/text string to display
        unit       : small unit label (e.g. "users", "%")
        sublabel   : optional caption line beneath the value
        val_color  : hex color for the main value
        unit_color : hex color for the unit
        sub_color  : hex color for the sublabel
        align      : "left" | "center" | "right"
        """
        val_sz  = ctx.fit_text_size(
            value,
            w,
            max_size=max(36, min(96, int(h * 0.22))),
            min_size=max(24, ctx.font_size("heading-sub")),
            bold=True,
            safety=0.90,
        )
        unit_sz = max(14, int(h * 0.07))
        sub_sz  = 11
        val_h   = int(val_sz * 1.2)
        total_h = val_h + (sub_sz + 6 if sublabel else 0)
        start_y = y + max(0, (h - total_h) // 2)

        ctx.text(x, start_y, w, val_h, value,
                 size=val_sz, bold=True, color=val_color,
                 align=align, valign="middle")

        if unit:
            u_w = max(40, int(len(unit) * unit_sz * 0.7))
            ux  = (x + w - u_w) if align == "right" else x
            ctx.text(ux, start_y, u_w, unit_sz + 4, unit,
                     size=unit_sz, color=unit_color,
                     align="right" if align == "right" else "left",
                     valign="top")

        if sublabel:
            ctx.text(x, start_y + val_h + 2, w, sub_sz + 4, sublabel,
                     size=sub_sz, color=sub_color,
                     align=align, valign="top")
