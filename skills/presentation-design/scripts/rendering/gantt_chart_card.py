"""
GanttChartCardRenderer — Renders a Gantt chart from structured content.

The chart is drawn entirely from primitive elements (rect, text, line) so it
works in both the draw.io and PPTX exporters without any external image.

Supported content YAML keys
----------------------------
title_col_label : str            label above the task-name column (default "Task")
start_date      : str            ISO date "YYYY-MM-DD" or "YYYY-MM"
                  The chart treats this as day 0.  If omitted, day 0 is the
                  earliest task start.
unit            : "days" | "weeks" | "months"   (default "weeks")
condensed       : bool            when true, shrinks labels/rows for small slots
overlays:
  - label    : str               band label shown in the header row (optional)
    start    : int | str         offset from chart start in <unit>, or ISO date
    duration : int               length in <unit>
    color    : str               optional fill hex — overrides the default overlay
                                 fill token so you can colour code types
                                 (e.g. "#FFF3E0" for code-freeze, "#FFF0F0" for UAT)
sections:
  - title: str                   section header (optional — groups tasks visually)
    tasks:
      - id     : str             short unique id  (optional, shown in bar if set)
        label  : str             task name  (required)
        start  : int | str       offset from chart start in <unit>, or "after:<id>"
        duration: int            length in <unit>
        progress: int            0-100  (shaded fill, optional)
        color  : str             override bar fill hex (optional)
        milestone: bool          if true, renders as a diamond instead of bar
        crit   : bool            marks bar as critical (red tint unless color given)

The renderer auto-fits the chart into the available body box.  In condensed mode
(triggered automatically when the box width < card-gantt-condensed-threshold px,
or when `condensed: true` is set explicitly), row height and fonts are scaled down.

Design tokens (`.card--gantt-chart` CSS class)
-----------------------------------------------
See themes/base.css section 13.
"""

from __future__ import annotations

import datetime
import datetime
import math
import re
from typing import Any

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _parse_date_offset(value: str | int | None, unit: str, start_date: datetime.date | None = None) -> float:
    """Convert a start/duration spec to a float offset in the given unit.

    Handles:
    - int / float literals  → returned as-is
    - "N"                   → float(N)
    - "after:<id>"          → returns None (caller resolves after id mapping)
    - "YYYY-MM-DD" / "YYYY-MM" with a configured start_date
    """
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip()
    if s.lower().startswith("after:"):
        return None  # type: ignore[return-value]
    if start_date is not None:
        try:
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
                dt = datetime.date.fromisoformat(s)
                delta = dt - start_date
                if unit == "days":
                    return float(delta.days)
                if unit == "weeks":
                    return delta.days / 7.0
                if unit == "months":
                    months = (dt.year - start_date.year) * 12 + dt.month - start_date.month
                    return months + (dt.day - start_date.day) / 30.0
            if re.fullmatch(r"\d{4}-\d{2}", s):
                year, month = map(int, s.split("-"))
                dt = datetime.date(year, month, 1)
                delta = dt - datetime.date(start_date.year, start_date.month, 1)
                if unit == "days":
                    return float(delta.days)
                if unit == "weeks":
                    return delta.days / 7.0
                if unit == "months":
                    return (dt.year - start_date.year) * 12 + dt.month - start_date.month
        except ValueError:
            pass
    try:
        return float(s)
    except ValueError:
        return 0.0


def _normalise_tasks(sections: list[dict], unit: str, start_date: datetime.date | None) -> list[dict]:
    """Flatten sections into a list of task dicts, resolving 'after:' starts."""
    flat: list[dict] = []
    # First pass: collect all tasks and resolve numeric starts
    id_end: dict[str, float] = {}  # id → end-offset (for 'after:' chains)

    for sec in sections:
        sec_title = sec.get("title", "")
        for raw in sec.get("tasks", []):
            task: dict[str, Any] = {
                "id": str(raw.get("id", "")),
                "label": str(raw.get("label", "")),
                "start_raw": raw.get("start", 0),
                "duration": max(0.0, float(raw.get("duration", 1))),
                "progress": max(0, min(100, int(raw.get("progress", 0)))),
                "color": raw.get("color"),
                "milestone": bool(raw.get("milestone", False)),
                "crit": bool(raw.get("crit", False)),
                "section": sec_title,
            }
            flat.append(task)

    # Second pass: resolve 'after:' starts
    for task in flat:
        raw_start = task["start_raw"]
        parsed = _parse_date_offset(raw_start, unit, start_date)
        if parsed is None:
            ref_id = str(raw_start).split(":", 1)[1].strip()
            task["start"] = id_end.get(ref_id, 0.0)
        else:
            task["start"] = parsed
        end = task["start"] + task["duration"]
        if task["id"]:
            id_end[task["id"]] = end
        del task["start_raw"]

    return flat


# ─────────────────────────────────────────────────────────────────────────────
# Renderer
# ─────────────────────────────────────────────────────────────────────────────

class GanttChartCardRenderer(BaseCardRenderer):
    """Renderer for ``gantt-chart-card`` type."""

    variant = "card--gantt-chart"

    def _tok(self, name: str, default=None):
        """Override: resolves ``card-gantt-{name}`` (prefix differs from variant ``card--gantt-chart``)."""
        return self._resolve_tok("gantt", name, default)

    def render_body(self, card: CardModel, box: RenderBox) -> None:  # noqa: C901
        """Render a Gantt chart with a fixed label column, time-axis grid, and task bars."""
        content = card.content if isinstance(card.content, dict) else {}

        # ── Resolve tokens ────────────────────────────────────────────────
        label_col_pct   = self._f("label-col-pct",    28)
        row_h           = self._f("row-height",        22)
        section_h       = self._f("section-height",    18)
        header_h        = self._f("header-height",     20)
        bar_radius      = self._f("bar-radius",        3)
        bar_color       = self._tok("bar-color")
        bar_crit_color  = self._tok("bar-crit-color")
        bar_done_opacity = self._f("bar-done-opacity", 0.45)
        grid_color      = self._tok("grid-color")
        section_fill    = self._tok("section-fill")
        section_color   = self._tok("section-font-color")
        section_size    = self._f("section-font-size",  10)
        label_size      = self._f("label-font-size",    10)
        label_color     = self._tok("label-font-color")
        tick_size       = self._f("tick-font-size",     9)
        tick_color      = self._tok("tick-font-color")
        bar_text_size   = self._f("bar-text-font-size", 8)
        bar_text_color  = self._tok("bar-text-font-color")
        milestone_color = self._tok("milestone-color")
        progress_color  = self._tok("progress-color")
        overlay_fill    = self._tok("overlay-fill")
        overlay_label_color = self._tok("overlay-label-color")
        overlay_label_size = self._f("overlay-label-font-size", 8)
        overlay_opacity = int(float(self._tok("overlay-opacity") or 40))
        condensed_threshold = self._f("condensed-threshold",   320)

        # ── Content parsing ───────────────────────────────────────────────
        unit      = str(content.get("unit", "weeks")).lower()
        condensed = bool(content.get("condensed", False))
        title_col_label = str(content.get("title_col_label", "Task"))

        raw_sections = content.get("sections", [])
        if not isinstance(raw_sections, list):
            raw_sections = []

        # Optional date origin for ISO date parsing
        raw_start_date = content.get("start_date")
        start_date = None
        if isinstance(raw_start_date, str):
            try:
                if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw_start_date):
                    start_date = datetime.date.fromisoformat(raw_start_date)
                elif re.fullmatch(r"\d{4}-\d{2}", raw_start_date):
                    year, month = map(int, raw_start_date.split("-"))
                    start_date = datetime.date(year, month, 1)
            except ValueError:
                start_date = None

        # Overlays: named background spans (holidays, code-freeze, UAT, sprints, …).
        raw_overlays = content.get("overlays", [])
        if not isinstance(raw_overlays, list):
            raw_overlays = []

        # Flatten to tasks
        tasks = _normalise_tasks(raw_sections, unit, start_date)

        # ── Auto-condensed ────────────────────────────────────────────────
        if box.w < condensed_threshold:
            condensed = True
        if condensed:
            row_h       = max(14, row_h * 0.65)
            section_h   = max(12, section_h * 0.65)
            header_h    = max(14, header_h * 0.75)
            label_size  = max(7, label_size * 0.8)
            tick_size   = max(6, tick_size * 0.8)
            bar_text_size = max(6, bar_text_size * 0.8)
            section_size = max(7, section_size * 0.8)

        # ── Chart bounds ──────────────────────────────────────────────────
        label_col_w = box.w * label_col_pct / 100.0
        chart_x     = box.x + label_col_w
        chart_w     = box.w - label_col_w

        if not tasks:
            # Empty placeholder
            box.add({
                "type": "rect",
                "x": box.x, "y": box.y, "w": box.w, "h": box.h,
                "fill": "#F9FAFB", "stroke": grid_color,
                "stroke_width": 1, "rx": 4,
            })
            box.add({
                "type": "text",
                "x": box.x, "y": box.y + box.h * 0.4, "w": box.w,
                "text": "[No Gantt tasks defined]",
                "font_size": label_size, "font_color": "#AAAAAA",
                "alignment": "center",
            })
            return

        # ── Overlays ───────────────────────────────────────────────────────────
        def _normalise_overlays(raw_overlays: list[dict], unit: str, start_date: datetime.date | None) -> list[dict]:
            entries: list[dict] = []
            for raw in raw_overlays:
                start = _parse_date_offset(raw.get("start", 0), unit, start_date)
                duration = max(0.0, float(raw.get("duration", 1)))
                entries.append({
                    "start": start,
                    "duration": duration,
                    "label": str(raw.get("label", "")),
                    "color": raw.get("color"),  # per-overlay fill override
                })
            return entries

        overlays = _normalise_overlays(raw_overlays, unit, start_date)

        # ── Time range ────────────────────────────────────────────────────
        t_min = min([t["start"] for t in tasks] + [o["start"] for o in overlays] or [0.0])
        t_max = max([t["start"] + t["duration"] for t in tasks] + [o["start"] + o["duration"] for o in overlays] or [1.0])
        if t_max <= t_min:
            t_max = t_min + 1
        t_span = t_max - t_min

        # Tick count: aim for 5-10 ticks that produce round numbers
        raw_ticks = t_span
        nice_intervals = [1, 2, 4, 5, 10, 12, 13, 26, 52]
        tick_interval = 1
        for ni in nice_intervals:
            if raw_ticks / ni <= 10:
                tick_interval = ni
                break

        def t2x(t: float) -> float:
            return chart_x + (t - t_min) / t_span * chart_w

        # ── Compute row layout ────────────────────────────────────────────
        # Build a vertical layout: header row, then for each section optionally
        # a section header, then task rows.
        layout: list[dict] = []  # {kind:"header"|"section"|"task", data:…, y:float, h:float}
        y_cur = box.y + header_h  # start below tick header
        prev_section: str | None = None

        for task in tasks:
            sec = task["section"]
            if sec and sec != prev_section:
                layout.append({"kind": "section", "title": sec, "y": y_cur, "h": section_h})
                y_cur += section_h
                prev_section = sec
            layout.append({"kind": "task", "task": task, "y": y_cur, "h": row_h})
            y_cur += row_h

        total_content_h = y_cur - box.y
        # Scale down if content overflows
        if total_content_h > box.h and box.h > 0:
            scale = box.h / total_content_h
            header_h      *= scale
            y_cur = box.y + header_h
            for entry in layout:
                entry["h"] *= scale
                entry["y"]  = y_cur
                y_cur += entry["h"]

        # ── Draw background & label column separator ──────────────────────
        box.add({
            "type": "rect",
            "x": box.x, "y": box.y, "w": box.w, "h": box.h,
            "fill": "#FFFFFF", "stroke": grid_color,
            "stroke_width": 1, "rx": 0,
        })

        # Vertical separator after label column
        box.add({
            "type": "line",
            "x1": chart_x, "y1": box.y,
            "x2": chart_x, "y2": box.y + box.h,
            "stroke": grid_color, "stroke_width": 1,
        })

        # ── Draw tick grid lines & tick labels ────────────────────────────
        t = math.ceil(t_min / tick_interval) * tick_interval
        header_y = box.y
        while t <= t_max:
            gx = t2x(t)
            if chart_x <= gx <= chart_x + chart_w:
                # Vertical grid line
                box.add({
                    "type": "line",
                    "x1": gx, "y1": box.y + header_h,
                    "x2": gx, "y2": box.y + box.h,
                    "stroke": grid_color, "stroke_width": 1,
                })
                # Tick label (centred between this and next tick)
                next_gx = t2x(t + tick_interval)
                lbl = f"{int(t)}"
                box.add({
                    "type": "text",
                    "x": gx, "y": header_y,
                    "w": max(1.0, next_gx - gx),
                    "h": header_h,
                    "text": lbl,
                    "font_size": tick_size,
                    "font_color": tick_color,
                    "alignment": "center",
                    "vertical_align": "middle",
                    "wrap": False,
                })
            t += tick_interval

        # Header label for label column
        box.add({
            "type": "text",
            "x": box.x + 2, "y": header_y,
            "w": label_col_w - 4,
            "h": header_h,
            "text": title_col_label,
            "font_size": tick_size,
            "font_color": tick_color,
            "alignment": "left",
            "vertical_align": "middle",
            "wrap": False,
        })

        # ── Draw section headers & task rows ──────────────────────────────
        for entry in layout:
            ey = entry["y"]
            eh = entry["h"]

            if entry["kind"] == "section":
                # Section header band
                box.add({
                    "type": "rect",
                    "x": box.x, "y": ey, "w": box.w, "h": eh,
                    "fill": section_fill, "stroke": "none",
                    "stroke_width": 0, "rx": 0,
                })
                box.add({
                    "type": "text",
                    "x": box.x + 4, "y": ey,
                    "w": box.w - 8, "h": eh,
                    "text": entry["title"],
                    "font_size": section_size,
                    "font_color": section_color,
                    "font_weight": "700",
                    "alignment": "left",
                    "vertical_align": "middle",
                    "wrap": False,
                })

            elif entry["kind"] == "task":
                task = entry["task"]
                # Horizontal separator
                box.add({
                    "type": "line",
                    "x1": box.x, "y1": ey + eh,
                    "x2": box.x + box.w, "y2": ey + eh,
                    "stroke": grid_color, "stroke_width": 1,
                })

                # Label column text
                box.add({
                    "type": "text",
                    "x": box.x + 2, "y": ey,
                    "w": label_col_w - 6,
                    "h": eh,
                    "text": task["label"],
                    "font_size": label_size,
                    "font_color": label_color,
                    "alignment": "left",
                    "vertical_align": "middle",
                    "wrap": False,
                })

                # ── Milestone ─────────────────────────────────────────────
                if task["milestone"]:
                    dia_size = min(eh * 0.7, 12.0)
                    mx = t2x(task["start"] + task["duration"] / 2)
                    my = ey + eh / 2 - dia_size / 2
                    # Draw as a rotated square (approximated as a small square)
                    box.add({
                        "type": "rect",
                        "x": mx - dia_size / 2, "y": my,
                        "w": dia_size, "h": dia_size,
                        "fill": task["color"] or milestone_color,
                        "stroke": "none", "stroke_width": 0,
                        "rx": 2,
                    })
                    continue

                # ── Bar ───────────────────────────────────────────────────
                bx = t2x(task["start"])
                bw = max(2.0, t2x(task["start"] + task["duration"]) - bx)
                bar_pad = max(2.0, eh * 0.18)
                by = ey + bar_pad
                bh = max(4.0, eh - 2 * bar_pad)

                fill = task["color"] or (bar_crit_color if task["crit"] else bar_color)

                # Full bar
                box.add({
                    "type": "rect",
                    "x": bx, "y": by, "w": bw, "h": bh,
                    "fill": fill, "stroke": "none",
                    "stroke_width": 0, "rx": bar_radius,
                })

                # Progress overlay (darker/different tint)
                if task["progress"] > 0:
                    prog_w = bw * task["progress"] / 100.0
                    box.add({
                        "type": "rect",
                        "x": bx, "y": by, "w": prog_w, "h": bh,
                        "fill": progress_color, "stroke": "none",
                        "stroke_width": 0, "rx": bar_radius,
                    })

                # Bar label (task id or label if id absent, clipped to bar)
                bar_label = task["id"] if task["id"] else task["label"]
                if bw > bar_text_size * 2 and not condensed:
                    box.add({
                        "type": "text",
                        "x": bx + 3, "y": by,
                        "w": max(1.0, bw - 6), "h": bh,
                        "text": bar_label,
                        "font_size": bar_text_size,
                        "font_color": bar_text_color,
                        "alignment": "left",
                        "vertical_align": "middle",
                        "wrap": False,
                    })

        # ── Overlay spans — drawn last so they sit on top in z-order ─────
        # Semi-transparent so bars beneath remain visible.
        for overlay in overlays:
            os_ = max(0.0, overlay["start"])
            oe = max(os_ + overlay["duration"], os_ + 0.5)
            ox = t2x(os_)
            ow = max(2.0, t2x(oe) - ox)
            fill_color = overlay["color"] or overlay_fill
            box.add({
                "type": "rect",
                "x": ox, "y": box.y + header_h,
                "w": ow, "h": box.h - header_h,
                "fill": fill_color, "stroke": "none",
                "stroke_width": 0, "rx": 0,
                "opacity": overlay_opacity,
            })
            if overlay["label"] and ow > overlay_label_size * 2:
                box.add({
                    "type": "text",
                    "x": ox + 2, "y": box.y,
                    "w": max(1.0, ow - 4), "h": header_h,
                    "text": overlay["label"],
                    "font_size": overlay_label_size,
                    "font_color": overlay_label_color,
                    "alignment": "left",
                    "vertical_align": "middle",
                    "wrap": False,
                })
