"""Cartesian (bar / line / combo) chart rendering."""

from __future__ import annotations

import math
from typing import Any

from scripts.rendering.base_card import RenderBox
from scripts.rendering.chart_card._format import fmt_value, nice_step
from scripts.rendering.chart_card._palette import series_color


def draw_cartesian(  # noqa: C901
    renderer, box: RenderBox,
    px: float, py: float, pw: float, ph: float,
    series_raw: list[dict], labels: list[str], mode: str,
    stacked: bool, value_labels: bool,
    y_min_forced, y_max_forced, y_step_forced,
    y_fmt: str,
    axis_color: str, axis_font_size: float, axis_font_color: str,
    grid_color: str, x_visible: bool, y_visible: bool,
    label_font_size: float, label_font_color: str,
    placeholder,
) -> None:
    if not series_raw or not labels:
        placeholder(box, px, py, pw, ph)
        return

    n_labels = len(labels)
    n_series = len(series_raw)

    # Decide which series are bars vs lines (combo mode)
    if mode == "combo":
        bar_idx  = [i for i, s in enumerate(series_raw) if s.get("type", "bar") in ("bar", "")]
        line_idx = [i for i, s in enumerate(series_raw) if s.get("type") == "line"]
        if not bar_idx and not line_idx:
            bar_idx  = list(range(max(0, n_series - 1)))
            line_idx = [n_series - 1] if n_series > 0 else []
    elif mode == "line":
        bar_idx, line_idx = [], list(range(n_series))
    else:  # bar
        bar_idx, line_idx = list(range(n_series)), []

    # ── Y scale ───────────────────────────────────────────────────────
    all_vals: list[float] = []
    for s in series_raw:
        all_vals.extend(float(v) for v in s.get("values", []) if v is not None)

    if stacked and bar_idx:
        col_sums = []
        for li in range(n_labels):
            col_sums.append(sum(
                float(series_raw[si].get("values", [])[li])
                for si in bar_idx
                if li < len(series_raw[si].get("values", []))
                and series_raw[si].get("values", [])[li] is not None
            ))
        y_max_data = max(col_sums) if col_sums else 1.0
    else:
        y_max_data = max(all_vals) if all_vals else 1.0

    y_min_data = min(all_vals) if all_vals else 0.0
    if y_min_data > 0:
        y_min_data = 0.0

    y_min = float(y_min_forced) if y_min_forced is not None else y_min_data
    y_max = float(y_max_forced) if y_max_forced is not None else y_max_data
    if y_max <= y_min:
        y_max = y_min + 1.0

    y_span = y_max - y_min
    step = float(y_step_forced) if y_step_forced is not None else nice_step(y_span)

    def v2y(v: float) -> float:
        return py + ph - max(0.0, min(1.0, (v - y_min) / y_span)) * ph

    # ── Grid lines + y-axis labels ────────────────────────────────────
    t = math.floor(y_min / step) * step
    while t <= y_max + step * 0.01:
        gy = v2y(t)
        if py - 1 <= gy <= py + ph + 1:
            box.add({"type": "line",
                     "x1": px, "y1": gy, "x2": px + pw, "y2": gy,
                     "stroke": grid_color, "stroke_width": 1})
            if y_visible:
                box.add({"type": "text",
                         "x": px - 40, "y": gy - axis_font_size,
                         "w": 36, "h": axis_font_size * 2,
                         "text": fmt_value(t, y_fmt),
                         "font_size": axis_font_size,
                         "font_color": axis_font_color,
                         "alignment": "right",
                         "vertical_align": "middle", "wrap": False})
        t = round(t + step, 10)

    # ── Axis lines ────────────────────────────────────────────────────
    box.add({"type": "line",
             "x1": px, "y1": py, "x2": px, "y2": py + ph,
             "stroke": axis_color, "stroke_width": 1})
    box.add({"type": "line",
             "x1": px, "y1": py + ph, "x2": px + pw, "y2": py + ph,
             "stroke": axis_color, "stroke_width": 1})

    cat_w = pw / n_labels

    # ── Bar series ────────────────────────────────────────────────────
    if bar_idx:
        n_bars = 1 if stacked else len(bar_idx)
        group_pad = cat_w * 0.12
        slot_w    = (cat_w - 2 * group_pad) / n_bars
        bar_w     = slot_w * 0.85

        for li, label in enumerate(labels):
            slot_x = px + li * cat_w

            if stacked:
                y_cursor = py + ph
                for si in bar_idx:
                    vals = series_raw[si].get("values", [])
                    val = float(vals[li]) if li < len(vals) and vals[li] is not None else 0.0
                    if val == 0.0:
                        continue
                    bh = abs((val / y_span) * ph)
                    bx = slot_x + group_pad
                    by = y_cursor - bh
                    color = series_color(renderer, series_raw, si)
                    box.add({"type": "rect",
                             "x": bx, "y": by,
                             "w": cat_w - 2 * group_pad, "h": max(bh, 0.5),
                             "fill": color, "stroke": "none",
                             "stroke_width": 0, "rx": 2})
                    if value_labels and bh > label_font_size + 2:
                        box.add({"type": "text",
                                 "x": bx, "y": by, "w": cat_w - 2 * group_pad, "h": bh,
                                 "text": fmt_value(val, y_fmt),
                                 "font_size": label_font_size,
                                 "font_color": label_font_color,
                                 "alignment": "center", "vertical_align": "middle",
                                 "wrap": False})
                    y_cursor -= bh
            else:
                for rank, si in enumerate(bar_idx):
                    vals = series_raw[si].get("values", [])
                    val = float(vals[li]) if li < len(vals) and vals[li] is not None else 0.0
                    bh = max(0.0, (val - y_min) / y_span * ph)
                    bx = slot_x + group_pad + rank * slot_w
                    by = v2y(max(val, y_min))
                    color = series_color(renderer, series_raw, si)
                    box.add({"type": "rect",
                             "x": bx, "y": by, "w": bar_w, "h": max(bh, 0.5),
                             "fill": color, "stroke": "none",
                             "stroke_width": 0, "rx": 2})
                    if value_labels and bh > label_font_size + 2:
                        box.add({"type": "text",
                                 "x": bx, "y": by - label_font_size - 2,
                                 "w": bar_w, "h": label_font_size + 2,
                                 "text": fmt_value(val, y_fmt),
                                 "font_size": label_font_size,
                                 "font_color": axis_font_color,
                                 "alignment": "center",
                                 "vertical_align": "middle", "wrap": False})

            # x-axis label
            if x_visible:
                box.add({"type": "text",
                         "x": slot_x, "y": py + ph + 3,
                         "w": cat_w, "h": axis_font_size + 4,
                         "text": label,
                         "font_size": axis_font_size,
                         "font_color": axis_font_color,
                         "alignment": "center", "vertical_align": "middle",
                         "wrap": False})

    # ── Line series ───────────────────────────────────────────────────
    if line_idx:
        marker_size = renderer._f("line-marker-size", 5)
        default_lw  = renderer._f("line-width", 2)

        # x-axis labels when there are no bars
        if not bar_idx and x_visible:
            for li, label in enumerate(labels):
                slot_x = px + li * cat_w
                box.add({"type": "text",
                         "x": slot_x, "y": py + ph + 3,
                         "w": cat_w, "h": axis_font_size + 4,
                         "text": label,
                         "font_size": axis_font_size,
                         "font_color": axis_font_color,
                         "alignment": "center", "vertical_align": "middle",
                         "wrap": False})

        for si in line_idx:
            s = series_raw[si]
            vals = s.get("values", [])
            color  = series_color(renderer, series_raw, si)
            dashed = bool(s.get("dashed", False))
            sw     = float(s.get("width", default_lw))
            marker = str(s.get("marker", "circle")).lower()

            points: list[tuple[float, float]] = []
            for li in range(n_labels):
                val = float(vals[li]) if li < len(vals) and vals[li] is not None else 0.0
                cx = px + li * cat_w + cat_w / 2
                cy = v2y(val)
                points.append((cx, cy))

            # Line segments
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                seg: dict[str, Any] = {"type": "line",
                                       "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                                       "stroke": color, "stroke_width": sw}
                if dashed:
                    seg["dashed"] = True
                box.add(seg)

            # Markers
            if marker != "none":
                for (cpx, cpy), raw_val in zip(points, vals[:n_labels]):
                    val_f = float(raw_val) if raw_val is not None else 0.0
                    if marker == "square":
                        box.add({"type": "rect",
                                 "x": cpx - marker_size / 2,
                                 "y": cpy - marker_size / 2,
                                 "w": marker_size, "h": marker_size,
                                 "fill": color, "stroke": "none",
                                 "stroke_width": 0, "rx": 1})
                    else:  # circle
                        box.add({"type": "ellipse",
                                 "x": cpx - marker_size / 2,
                                 "y": cpy - marker_size / 2,
                                 "w": marker_size, "h": marker_size,
                                 "fill": color, "stroke": "none",
                                 "stroke_width": 0})
                    if value_labels:
                        box.add({"type": "text",
                                 "x": cpx - 20,
                                 "y": cpy - label_font_size - 2,
                                 "w": 40, "h": label_font_size + 2,
                                 "text": fmt_value(val_f, y_fmt),
                                 "font_size": label_font_size,
                                 "font_color": color,
                                 "alignment": "center", "wrap": False})
