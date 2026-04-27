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
        project_root: Optional path for logo resolution.
    """

    def __init__(self, theme, *, rows: int = 1, cols: int = 1, project_root=None) -> None:
        super().__init__(theme, project_root=project_root)
        self.rows = rows
        self.cols = cols

    def compute_card_slots(
        self,
        chrome: SlideChrome,
        overrides: dict[str, Any] | None,
    ) -> list[RenderBox]:
        """Divide the body area into an R×C grid of card slots.

        When *overrides* contains a ``col_widths`` list of length >= ``self.cols``,
        columns are sized proportionally to those weights rather than equally.
        Example: ``col_widths: [2, 1]`` gives a 2/3 + 1/3 split on a 1×2 grid.
        """
        gap = float(self._resolve("canvas-card-gap", overrides) or 12)

        total_gap_x = gap * (self.cols - 1)
        total_gap_y = gap * (self.rows - 1)

        body_w_for_cols = chrome.body_w - total_gap_x

        # Proportional column widths — read from per-slide override if present
        col_widths_raw = overrides.get("col_widths") if overrides else None
        if (
            col_widths_raw
            and isinstance(col_widths_raw, list)
            and len(col_widths_raw) >= self.cols
        ):
            total_parts = sum(float(w) for w in col_widths_raw[: self.cols]) or 1.0
            slot_ws = [
                body_w_for_cols * float(w) / total_parts
                for w in col_widths_raw[: self.cols]
            ]
        else:
            equal_w = body_w_for_cols / self.cols
            slot_ws = [equal_w] * self.cols

        body_h_for_rows = chrome.body_h - total_gap_y
        row_heights_raw = overrides.get("row_heights") if overrides else None
        if (
            row_heights_raw
            and isinstance(row_heights_raw, list)
            and len(row_heights_raw) >= self.rows
        ):
            total_parts = sum(float(h) for h in row_heights_raw[: self.rows]) or 1.0
            slot_hs = [
                body_h_for_rows * float(h) / total_parts
                for h in row_heights_raw[: self.rows]
            ]
        else:
            equal_h = body_h_for_rows / self.rows
            slot_hs = [equal_h] * self.rows

        slots: list[RenderBox] = []
        y_cursor = chrome.body_y
        for r in range(self.rows):
            x_cursor = chrome.body_x
            for c in range(self.cols):
                slots.append(RenderBox(x_cursor, y_cursor, slot_ws[c], slot_hs[r]))
                x_cursor += slot_ws[c] + gap
            y_cursor += slot_hs[r] + gap

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


def create_grid_renderer(layout_id: str, theme, project_root=None) -> GridLayoutRenderer:
    """Create a ``GridLayoutRenderer`` for the given *layout_id*.

    Args:
        layout_id: One of ``grid-1x1`` through ``grid-3x4``.
        theme: The loaded ``ThemeTokens``.
        project_root: Optional path for logo resolution.

    Raises:
        ValueError: If *layout_id* is not a recognized grid layout.
    """
    spec = _GRID_SPECS.get(layout_id)
    if spec is None:
        raise ValueError(f"Unknown grid layout: {layout_id}")
    rows, cols = spec
    return GridLayoutRenderer(theme, rows=rows, cols=cols, project_root=project_root)
