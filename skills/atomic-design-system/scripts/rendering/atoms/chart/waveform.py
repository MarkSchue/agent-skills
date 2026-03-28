"""
WaveformAtom — amplitude bar waveform
======================================
Renders a series of upward bars whose heights represent normalized 0–1
amplitude values. If *values* is empty a decorative sine-based sample is
auto-generated.
"""
from __future__ import annotations
import math


class WaveformAtom:
    """Render an amplitude bar waveform from a list of 0..1 float values."""

    def render(self, ctx, x: int, y: int, w: int, h: int,
               values: list, fill: str) -> None:
        """
        Parameters
        ----------
        ctx    : RenderContext
        x, y   : top-left position (pixels)
        w, h   : bounding box dimensions (pixels)
        values : list[float 0..1] — normalized amplitude per column
        fill   : hex color for the bars
        """
        if not values:
            n = 20
            values = [
                0.15 + 0.70 * math.sin(math.pi * i / (n - 1)) ** 1.5
                * (0.8 + 0.2 * ((i * 7) % 5) / 4)
                for i in range(n)
            ]
        n      = len(values)
        bw_raw = (w - 2) / max(n, 1)
        bw     = max(3, int(bw_raw * 0.65))
        for i, v in enumerate(values):
            bh = max(4, int(float(v) * (h - 4)))
            bx = x + int(i * bw_raw)
            by = y + h - bh
            ctx.rect(bx, by, bw, bh, fill=fill, radius=2)
