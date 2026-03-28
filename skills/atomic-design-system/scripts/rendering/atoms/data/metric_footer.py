"""
MetricFooterAtom — two-pair label/value footer row
====================================================
Renders a thin separator line followed by two label/value pairs
(one left-aligned, one right-aligned) inside *footer_h* pixels.
"""
from __future__ import annotations


class MetricFooterAtom:
    """Render a two-pair label/value footer with a top separator line."""

    def render(self, ctx, x: int, y: int, w: int, footer_h: int,
               left_label: str, left_value: str,
               right_label: str, right_value: str,
               text_color: str, sep_color: str,
               props: dict | None = None) -> None:
        """
        Parameters
        ----------
        ctx         : RenderContext
        x, y        : top-left position of the footer zone (pixels)
        w           : total width (pixels)
        footer_h    : height of the footer zone (pixels)
        left_label  : label for the left pair
        left_value  : value for the left pair (can be "")
        right_label : label for the right pair
        right_value : value for the right pair (can be "")
        text_color  : hex color for all text
        sep_color   : hex color for the separator line
        props       : optional card props for shared footer visibility overrides
        """
        if ctx.card_line_enabled(props, "footer", default=True):
            ctx.divider(x, y, w,
                        color=ctx.card_line_color("footer", sep_color))
        cy = y + 4
        th = max(footer_h - 4, 14)
        if left_label:
            txt = f"{left_label}  {left_value}" if left_value else left_label
            ctx.text(x, cy, w // 2, th, txt,
                     size=ctx.font_size("annotation"), color=text_color, align="left", valign="middle")
        if right_label:
            txt = f"{right_label}  {right_value}" if right_value else right_label
            ctx.text(x + w // 2, cy, w // 2, th, txt,
                     size=ctx.font_size("annotation"), color=text_color, align="right", valign="middle")
