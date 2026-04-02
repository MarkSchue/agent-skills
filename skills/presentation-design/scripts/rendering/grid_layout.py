"""
GridLayoutRenderer — Configurable R×C grid layout for card placement.

Supports all grid variants from 1×1 to 3×4 through row/column parameters.
"""

from __future__ import annotations

from typing import Any

from scripts.rendering.base_layout import BaseLayoutRenderer, RenderBox, SlideChrome


class GridLayoutRenderer(BaseLayoutRenderer):
    """Configurable grid layout renderer.

    Args:
        theme: The loaded ``ThemeTokens``.
        rows: Number of grid rows (1–3).
        cols: Number of grid columns (1–4).
    """

    def __init__(self, theme, *, rows: int = 1, cols: int = 1) -> None:
        super().__init__(theme)
        self.rows = rows
        self.cols = cols

    def compute_card_slots(
        self,
        chrome: SlideChrome,
        overrides: dict[str, Any] | None,
    ) -> list[RenderBox]:
        """Divide the body area into an R×C grid of equal-sized card slots."""
        gap = float(self._resolve("canvas-card-gap", overrides) or 12)

        total_gap_x = gap * (self.cols - 1)
        total_gap_y = gap * (self.rows - 1)

        slot_w = (chrome.body_w - total_gap_x) / self.cols
        slot_h = (chrome.body_h - total_gap_y) / self.rows

        slots: list[RenderBox] = []
        for r in range(self.rows):
            for c in range(self.cols):
                x = chrome.body_x + c * (slot_w + gap)
                y = chrome.body_y + r * (slot_h + gap)
                slots.append(RenderBox(x, y, slot_w, slot_h))

        return slots


# ── Factory helper ───────────────────────────────────────────────────────────

# Map layout IDs to (rows, cols) tuples
_GRID_SPECS: dict[str, tuple[int, int]] = {
    "grid-1x1": (1, 1),
    "grid-1x2": (1, 2),
    "grid-1x3": (1, 3),
    "grid-1x4": (1, 4),
    "grid-2x1": (2, 1),
    "grid-2x2": (2, 2),
    "grid-2x3": (2, 3),
    "grid-2x4": (2, 4),
    "grid-3x1": (3, 1),
    "grid-3x2": (3, 2),
    "grid-3x3": (3, 3),
    "grid-3x4": (3, 4),
}


def create_grid_renderer(layout_id: str, theme) -> GridLayoutRenderer:
    """Create a ``GridLayoutRenderer`` for the given *layout_id*.

    Args:
        layout_id: One of ``grid-1x1`` through ``grid-3x4``.
        theme: The loaded ``ThemeTokens``.

    Raises:
        ValueError: If *layout_id* is not a recognized grid layout.
    """
    spec = _GRID_SPECS.get(layout_id)
    if spec is None:
        raise ValueError(f"Unknown grid layout: {layout_id}")
    rows, cols = spec
    return GridLayoutRenderer(theme, rows=rows, cols=cols)
