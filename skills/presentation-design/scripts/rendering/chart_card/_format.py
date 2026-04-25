"""Numeric formatting + nice tick step helpers."""

from __future__ import annotations

import math


def fmt_value(v: float, fmt: str) -> str:
    """Format a numeric value; empty fmt → auto integer/decimal."""
    if not fmt:
        return str(int(v)) if (v == int(v) and abs(v) < 1e12) else f"{v:.1f}"
    try:
        if fmt == "%":
            return f"{v:.0f}%"
        return format(v, fmt)
    except Exception:
        return str(v)


def nice_step(span: float, target_ticks: int = 5) -> float:
    """Return a 'nice' round tick step for the given value span."""
    if span <= 0:
        return 1.0
    raw = span / target_ticks
    mag = 10 ** math.floor(math.log10(raw))
    for mult in (1, 2, 2.5, 5, 10):
        step = mag * mult
        if span / step <= target_ticks + 1:
            return step
    return mag * 10
