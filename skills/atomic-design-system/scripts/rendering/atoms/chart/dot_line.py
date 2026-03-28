"""
DotLineAtom — lollipop / dumbbell chart
=========================================
Renders vertical sticks with dot markers at both the top (scaled value)
and the baseline.  Values are auto-normalized so any numeric range works.
"""
from __future__ import annotations


class DotLineAtom:
    """Render a lollipop / dumbbell chart from a list of numeric values."""

    def render(self, ctx, x: int, y: int, w: int, h: int,
               values: list, dot_color: str, line_color: str) -> None:
        """
        Parameters
        ----------
        ctx        : RenderContext
        x, y       : top-left position (pixels)
        w, h       : bounding box dimensions (pixels)
        values     : list[number] — raw data values (auto-normalized)
        dot_color  : hex color for the circle markers
        line_color : hex color for the vertical sticks
        """
        if not values:
            values = [0.5, 0.7, 0.4, 0.8, 0.6, 0.9, 0.5]
        mn, mx = (min(float(v) for v in values),
                  max(float(v) for v in values))
        span   = (mx - mn) or 1
        norm   = [(float(v) - mn) / span for v in values]
        n      = len(norm)
        step   = w / max(n, 1)
        dot_r  = max(5, int(h * 0.05))
        for i, nv in enumerate(norm):
            cx       = x + int(i * step + step / 2)
            top_y    = y + h - int(nv * (h - dot_r * 2)) - dot_r
            bottom_y = y + h - dot_r
            ctx.line(cx, top_y + dot_r, cx, bottom_y - dot_r, line_color)
            for dy in (top_y, bottom_y):
                ctx.ellipse(cx - dot_r, dy - dot_r,
                             dot_r * 2, dot_r * 2, dot_color)
