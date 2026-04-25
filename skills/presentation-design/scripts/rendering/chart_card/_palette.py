"""Default chart-series colour palette + per-series colour resolution."""

from __future__ import annotations

DEFAULT_PALETTE = [
    "#3B82F6",  # blue
    "#EF4444",  # red
    "#10B981",  # green
    "#F59E0B",  # amber
    "#8B5CF6",  # violet
    "#EC4899",  # pink
    "#06B6D4",  # cyan
    "#F97316",  # orange
]


def resolve_palette(renderer) -> list[str]:
    """Return the active palette: per-slot tokens (palette-1..8) override default."""
    slots: list[str] = []
    for i in range(1, 9):
        c = renderer._tok(f"palette-{i}", "")
        if c:
            slots.append(str(c).strip())
    return slots if slots else DEFAULT_PALETTE


def series_color(renderer, series: list[dict], idx: int) -> str:
    """Return the colour for series *idx* — explicit ``color`` wins over palette."""
    explicit = series[idx].get("color") if idx < len(series) else None
    if explicit:
        return str(explicit)
    pal = resolve_palette(renderer)
    return pal[idx % len(pal)]
