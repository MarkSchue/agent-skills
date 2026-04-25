"""Geometry calculations for compare-card rendering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from scripts.rendering.base_card import RenderBox
from scripts.rendering.compare_card._style import CompareStyle


@dataclass(slots=True)
class CompareGeometry:
    """All numeric layout values needed to render the comparison grid."""

    n_cols: int
    n_rows: int
    topic_col_w: float
    col_xs: list[float]
    col_ws: list[float]
    row_h: float
    header_y: float
    rows_y: float
    summary_y: float
    total_h: float


def compute_geometry(
    box: RenderBox,
    columns: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    content: dict[str, Any],
    style: CompareStyle,
) -> CompareGeometry:
    """Compute column widths, row heights and y-anchors for the grid."""
    n_cols = max(1, len(columns))
    n_rows = len(rows)

    topic_col_w = box.w * style.topic_col_pct if style.topic_visible else 0.0
    compare_total_w = box.w - topic_col_w

    raw_col_widths = content.get("col_widths")
    if raw_col_widths and len(raw_col_widths) >= n_cols:
        total_w = sum(float(w) for w in raw_col_widths[:n_cols]) or 1.0
        col_fracs = [float(w) / total_w for w in raw_col_widths[:n_cols]]
    else:
        col_fracs = [1.0 / n_cols] * n_cols

    col_xs: list[float] = []
    col_ws: list[float] = []
    cx = box.x + topic_col_w
    for frac in col_fracs:
        cw = compare_total_w * frac
        col_xs.append(cx)
        col_ws.append(cw)
        cx += cw

    avail_h = box.h - style.header_h - (style.summ_h if style.has_summary else 0.0)
    if n_rows > 0:
        if style.row_h_tok is not None:
            row_h = max(style.row_min_h, float(style.row_h_tok))
            if row_h * n_rows > avail_h > 0:
                row_h = max(style.row_min_h, avail_h / n_rows)
        else:
            row_h = max(style.row_min_h, avail_h / n_rows) if avail_h > 0 else style.row_min_h
    else:
        row_h = style.row_min_h

    header_y = box.y
    rows_y = header_y + style.header_h
    summary_y = rows_y + row_h * n_rows
    total_h = style.header_h + row_h * n_rows + (style.summ_h if style.has_summary else 0.0)

    return CompareGeometry(
        n_cols=n_cols, n_rows=n_rows,
        topic_col_w=topic_col_w,
        col_xs=col_xs, col_ws=col_ws,
        row_h=row_h,
        header_y=header_y, rows_y=rows_y,
        summary_y=summary_y, total_h=total_h,
    )
