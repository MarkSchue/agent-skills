"""
CalendarCardRenderer — A row of N consecutive month grids (Mon-Sun), with
the ability to highlight contiguous date ranges as rounded "pills" in
arbitrary colours, plus an optional legend below the grids.

Content schema::

    type: calendar-card
    content:
      # Either provide an explicit list of months …
      months:
        - "2025-04"
        - "2025-05"
        - "2025-06"
      # … or a start month + count:
      # start: "2025-04"
      # count: 3

      highlights:
        - { start: "2025-04-01", end: "2025-04-04", color: "#E5E54E", label: "Project Phase 1" }
        - { start: "2025-04-07", end: "2025-04-11", color: "#E5E54E", label: "Project Phase 1" }
        - { start: "2025-04-14", end: "2025-05-30", color: "#3344E5", label: "Project Phase 2" }
        - { start: "2025-06-11", end: "2025-06-13", color: "#1FBF7F", label: "Project Phase 3" }

      legend: true   # default: derive from highlights' unique labels
      # legend: [{label: "...", color: "..."}, ...]    # explicit override

Behaviour:

- Week starts Monday (ISO).
- Days outside the current month are still drawn faintly (grey) so the
  grid stays rectangular — this matches the screenshot reference.
- When a highlight range spans multiple weeks, the renderer emits one
  pill per week-row.
- When a highlight range spans multiple months, each affected month's
  cells are highlighted independently.
- Pills sit BEHIND the day numbers; numbers on highlighted days switch
  to ``--card-calendar-highlight-text-color`` (default white).

Tokens (variant prefix ``card-calendar-``):
    month-title-font-size/color/weight,
    weekday-font-size/color/weight,
    day-font-size, day-color, day-out-color, day-highlight-color,
    cell-w, cell-h, cell-gap, month-gap,
    pill-padding-x, pill-radius (px or "auto" → cell-h/2),
    legend-visible, legend-font-size/color, legend-dot-radius, legend-gap.
"""

from __future__ import annotations

import calendar
import datetime as _dt
from typing import Any

from scripts.models.deck import CardModel
from scripts.parsing.inline_markdown import text_and_runs
from scripts.rendering.base_card import BaseCardRenderer, RenderBox

_WEEKDAYS = ("MO", "TU", "WE", "TH", "FR", "SA", "SU")


def _parse_ym(s: str) -> tuple[int, int]:
    """Parse 'YYYY-MM' → (year, month)."""
    parts = str(s).strip().split("-")
    return int(parts[0]), int(parts[1])


def _parse_ymd(s: str) -> _dt.date:
    parts = str(s).strip().split("-")
    return _dt.date(int(parts[0]), int(parts[1]), int(parts[2]))


def _add_months(year: int, month: int, n: int) -> tuple[int, int]:
    idx = (year * 12 + (month - 1)) + n
    return idx // 12, (idx % 12) + 1


class CalendarCardRenderer(BaseCardRenderer):
    """Renderer for ``calendar-card`` type."""

    variant = "card--calendar"

    def _tok(self, name: str, default: Any = None) -> Any:
        return self._resolve_tok("calendar", name, default)

    # ── helpers ──────────────────────────────────────────────────────
    def _months(self, content: dict) -> list[tuple[int, int]]:
        if content.get("months"):
            out = []
            for m in content["months"]:
                if isinstance(m, str):
                    out.append(_parse_ym(m))
                elif isinstance(m, dict) and "year" in m and "month" in m:
                    out.append((int(m["year"]), int(m["month"])))
            return out
        start = content.get("start")
        count = int(content.get("count", 1) or 1)
        if start:
            y, mo = _parse_ym(start)
            return [_add_months(y, mo, i) for i in range(count)]
        # Default: current month
        today = _dt.date.today()
        return [(today.year, today.month)]

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        content = card.content if isinstance(card.content, dict) else {}
        months = self._months(content)
        if not months:
            return
        highlights_raw = list(content.get("highlights") or [])
        # Normalise highlight ranges
        highlights: list[dict] = []
        for h in highlights_raw:
            try:
                s = _parse_ymd(h["start"])
                e = _parse_ymd(h.get("end") or h["start"])
            except (KeyError, ValueError, TypeError):
                continue
            if e < s:
                s, e = e, s
            highlights.append({
                "start": s, "end": e,
                "color": h.get("color"),
                "label": h.get("label", ""),
            })

        # ── Tokens ────────────────────────────────────────────────────
        primary       = self.resolve("color-primary") or "#000099"

        title_size    = float(self._tok("month-title-font-size") or 14)
        title_color   = self._tok("month-title-font-color") or primary
        title_weight  = self._tok("month-title-font-weight") or "bold"

        wd_size       = float(self._tok("weekday-font-size") or 10)
        wd_color      = self._tok("weekday-font-color") or self.resolve("color-text-muted") or "#9AA1D6"
        wd_weight     = self._tok("weekday-font-weight") or "normal"

        day_size      = float(self._tok("day-font-size") or 11)
        day_color     = self._tok("day-color") or self.resolve("color-text-default") or "#222"
        day_out_color = self._tok("day-out-color") or self.resolve("color-text-muted") or "#CCCCCC"
        day_hl_color  = self._tok("day-highlight-color") or "#FFFFFF"

        cell_w_t      = self._tok("cell-w")
        cell_h_t      = self._tok("cell-h")
        cell_gap      = float(self._tok("cell-gap") or 2)
        month_gap     = float(self._tok("month-gap") or 24)

        pill_pad_x    = float(self._tok("pill-padding-x") or 4)
        pill_r_t      = self._tok("pill-radius")  # "auto" or px

        legend_vis_raw= content.get("legend", True)
        legend_visible= bool(legend_vis_raw) if not isinstance(legend_vis_raw, list) else True
        legend_size   = float(self._tok("legend-font-size") or 11)
        legend_color  = self._tok("legend-font-color") or self.resolve("color-text-default") or "#222"
        legend_dot_r  = float(self._tok("legend-dot-radius") or 7)
        legend_gap    = float(self._tok("legend-gap") or 24)
        legend_h      = max(legend_dot_r * 2 + 4, legend_size + 4) if legend_visible else 0

        # ── Geometry ──────────────────────────────────────────────────
        n_months = len(months)
        # Width per month grid (7 day columns + 6 gaps)
        avail_w = box.w - month_gap * (n_months - 1)
        month_w = avail_w / n_months

        # Cell sizing
        if cell_w_t:
            cell_w = float(cell_w_t)
        else:
            cell_w = (month_w - cell_gap * 6) / 7
        # Body height for the calendar grids (above legend)
        body_h = box.h - legend_h - (8 if legend_visible else 0)
        # Each month: 1 title row + 1 weekday row + up to 6 day rows
        title_row_h = title_size + 6
        wd_row_h    = wd_size + 6
        rows_for_days = 6
        if cell_h_t:
            cell_h = float(cell_h_t)
        else:
            cell_h = (body_h - title_row_h - wd_row_h - cell_gap * (rows_for_days - 1)) / rows_for_days
        cell_h = max(16.0, cell_h)

        try:
            pill_r = float(pill_r_t) if pill_r_t and str(pill_r_t).lower() != "auto" else cell_h / 2
        except (TypeError, ValueError):
            pill_r = cell_h / 2

        # ── Render each month ─────────────────────────────────────────
        for mi, (yr, mo) in enumerate(months):
            mx = box.x + mi * (month_w + month_gap)
            my = box.y

            # Month title
            month_label = f"{calendar.month_name[mo].upper()} {yr}"
            box.add({
                "type": "text",
                "x": mx, "y": my, "w": month_w, "h": title_row_h,
                **text_and_runs(month_label),
                "font_size": title_size,
                "font_color": title_color,
                "font_weight": title_weight,
                "alignment": "center",
            })

            # Weekday header
            wy = my + title_row_h
            for ci, name in enumerate(_WEEKDAYS):
                cx = mx + ci * (cell_w + cell_gap)
                box.add({
                    "type": "text",
                    "x": cx, "y": wy,
                    "w": cell_w, "h": wd_row_h,
                    **text_and_runs(name),
                    "font_size": wd_size,
                    "font_color": wd_color,
                    "font_weight": wd_weight,
                    "alignment": "center",
                })

            # Day grid origin
            grid_y = wy + wd_row_h
            cal = calendar.Calendar(firstweekday=0)  # Monday=0
            weeks = cal.monthdatescalendar(yr, mo)  # list of weeks; each = 7 dates

            # ── Pass 1: emit highlight pills (drawn UNDER day numbers) ──
            for h in highlights:
                color = h["color"] or primary
                for ri, week in enumerate(weeks):
                    # Indices in this week whose date belongs to *this month*
                    # AND falls within the highlight range.
                    in_run = [
                        i for i, d in enumerate(week)
                        if d.month == mo and h["start"] <= d <= h["end"]
                    ]
                    if not in_run:
                        continue
                    # Group into contiguous index runs (handles a holiday
                    # gap inside the same week, although typically all are contiguous).
                    runs: list[tuple[int, int]] = []
                    start = prev = in_run[0]
                    for idx in in_run[1:]:
                        if idx == prev + 1:
                            prev = idx
                        else:
                            runs.append((start, prev))
                            start = prev = idx
                    runs.append((start, prev))
                    for c_start, c_end in runs:
                        px = mx + c_start * (cell_w + cell_gap) + pill_pad_x
                        pw = (
                            (c_end - c_start + 1) * cell_w
                            + (c_end - c_start) * cell_gap
                            - pill_pad_x * 2
                        )
                        py = grid_y + ri * (cell_h + cell_gap)
                        box.add({
                            "type": "rect",
                            "x": px, "y": py,
                            "w": max(pw, cell_w * 0.5),
                            "h": cell_h,
                            "fill": color,
                            "stroke": "none",
                            "stroke_width": 0,
                            "rx": pill_r,
                        })

            # ── Pass 2: emit day numbers ──────────────────────────────
            # Build a fast lookup: which dates are highlighted
            hl_dates: dict[_dt.date, str] = {}
            for h in highlights:
                d = h["start"]
                while d <= h["end"]:
                    hl_dates[d] = h["color"] or primary
                    d += _dt.timedelta(days=1)

            for ri, week in enumerate(weeks):
                for ci, d in enumerate(week):
                    cx = mx + ci * (cell_w + cell_gap)
                    cy = grid_y + ri * (cell_h + cell_gap)
                    in_month = (d.month == mo)
                    is_hl = in_month and (d in hl_dates)
                    color = day_hl_color if is_hl else (day_color if in_month else day_out_color)
                    box.add({
                        "type": "text",
                        "x": cx, "y": cy,
                        "w": cell_w, "h": cell_h,
                        **text_and_runs(str(d.day)),
                        "font_size": day_size,
                        "font_color": color,
                        "font_weight": "normal",
                        "alignment": "center",
                        "vertical_align": "middle",
                    })

        # ── Legend ────────────────────────────────────────────────────
        if not legend_visible:
            return

        # Either explicit list or derived from unique highlight labels (in order).
        legend_items: list[dict] = []
        if isinstance(legend_vis_raw, list):
            for item in legend_vis_raw:
                if isinstance(item, dict) and item.get("label"):
                    legend_items.append({
                        "label": str(item["label"]),
                        "color": item.get("color") or primary,
                    })
        else:
            seen: set[str] = set()
            for h in highlights:
                lbl = (h.get("label") or "").strip()
                if not lbl or lbl in seen:
                    continue
                seen.add(lbl)
                legend_items.append({"label": lbl, "color": h["color"] or primary})

        if not legend_items:
            return

        # Stack legend items vertically in the bottom-left of the body box,
        # below the calendar grids. Each item: dot + label.
        ly = box.y + box.h - legend_h * len(legend_items)
        if ly < box.y + body_h + 4:
            ly = box.y + body_h + 8
        for i, item in enumerate(legend_items):
            row_y = ly + i * legend_h
            # Dot
            dot_x = box.x + 4
            box.add({
                "type": "ellipse",
                "x": dot_x,
                "y": row_y + (legend_h - legend_dot_r * 2) / 2,
                "w": legend_dot_r * 2,
                "h": legend_dot_r * 2,
                "fill": item["color"],
                "stroke": "none",
                "stroke_width": 0,
            })
            # Label
            box.add({
                "type": "text",
                "x": dot_x + legend_dot_r * 2 + 8,
                "y": row_y,
                "w": box.w - (dot_x + legend_dot_r * 2 + 8 - box.x),
                "h": legend_h,
                **text_and_runs(item["label"]),
                "font_size": legend_size,
                "font_color": legend_color,
                "font_weight": "normal",
                "alignment": "left",
                "vertical_align": "middle",
            })
