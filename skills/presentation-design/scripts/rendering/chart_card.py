"""
ChartCardRenderer — Renders chart-card entirely from primitives (rect/line/ellipse/text).

No image dependency.  Supports four chart types selectable via ``content.chart_type``:

  bar     Vertical grouped or stacked bar chart
  line    Line chart with optional point markers
  pie     Pie or donut chart
  combo   Bars for primary series + line overlay for secondary series

Anatomy of a chart-card content block
--------------------------------------
content:
  chart_type   : bar | line | pie | combo         (default: bar)
  labels       : [str, ...]                       Category axis labels
  stacked      : bool                             Stacked bars (default: false)
  value_labels : bool                             Show data labels (default: false)
  inner_radius : float  0.0-0.9                   Donut hole for pie (0 = full pie)
  caption      : str                              Attribution line at bottom
  series:
    - name    : str                               Legend label
      values  : [float, ...]                      One value per label
      color   : "#RRGGBB"                         Override palette color
      type    : bar | line                        For combo only
      marker  : circle | square | none            Line marker shape (default: circle)
      dashed  : bool                              Dashed line stroke (default: false)
      width   : int                               Line stroke width px (default: token)
  x_axis:
    title      : str
    visible    : bool                             default: true
  y_axis:
    title      : str
    visible    : bool                             default: true
    min        : float                            Override auto-min
    max        : float                            Override auto-max
    step       : float                            Tick step (auto if omitted)
    format     : ",.0f" | "%" | ".1f" | …        Python format string for tick labels
  legend:
    visible    : bool                             default: true
    position   : bottom | right | top | none      default: token --card-chart-legend-position

Design tokens (CSS class .card--chart) — see themes/base.css section 7.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox

# ── Default series colour palette ─────────────────────────────────────────
_DEFAULT_PALETTE = [
    "#3B82F6",  # blue
    "#EF4444",  # red
    "#10B981",  # green
    "#F59E0B",  # amber
    "#8B5CF6",  # violet
    "#EC4899",  # pink
    "#06B6D4",  # cyan
    "#F97316",  # orange
]


# ── Helpers ────────────────────────────────────────────────────────────────

def _fmt_value(v: float, fmt: str) -> str:
    """Format a numeric value; empty fmt → auto integer/decimal."""
    if not fmt:
        return str(int(v)) if (v == int(v) and abs(v) < 1e12) else f"{v:.1f}"
    try:
        if fmt == "%":
            return f"{v:.0f}%"
        return format(v, fmt)
    except Exception:
        return str(v)


def _nice_step(span: float, target_ticks: int = 5) -> float:
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


# ── Renderer ───────────────────────────────────────────────────────────────

class ChartCardRenderer(BaseCardRenderer):
    """Renderer for ``chart-card`` type — native primitive-based charts."""

    variant = "card--chart"

    def __init__(self, theme, *, project_root: str | Path | None = None) -> None:
        super().__init__(theme)
        self.project_root = Path(project_root) if project_root else None

    # ── Token helpers ────────────────────────────────────────────────────

    def _tok(self, name: str, default: Any = None) -> Any:
        return self._resolve_tok("chart", name, default)

    def _f(self, name: str, default: float) -> float:
        return float(self._tok(name, default))

    def _palette(self) -> list[str]:
        # Try individual palette-N tokens first (1..8)
        slots = []
        for i in range(1, 9):
            c = self._tok(f"palette-{i}", "")
            if c:
                slots.append(str(c).strip())
        return slots if slots else _DEFAULT_PALETTE

    def _series_color(self, series: list[dict], idx: int) -> str:
        explicit = series[idx].get("color") if idx < len(series) else None
        if explicit:
            return str(explicit)
        pal = self._palette()
        return pal[idx % len(pal)]

    # ── Main entry point ──────────────────────────────────────────────────

    def render_body(self, card: CardModel, box: RenderBox) -> None:  # noqa: C901
        content = card.content if isinstance(card.content, dict) else {}

        # ── Image path shortcut ────────────────────────────────────────
        image_path = content.get("image", "")
        if image_path:
            self._render_image_fallback(card, box, content, image_path)
            return

        # ── Shared token resolution ────────────────────────────────────
        axis_color       = self._tok("axis-color")
        axis_font_size   = self._f("axis-font-size",          9)
        axis_font_color  = self._tok("axis-font-color",       axis_color)
        grid_color       = self._tok("grid-color")
        legend_font_size = self._f("legend-font-size",        10)
        legend_pos_tok   = self._tok("legend-position",       "bottom")
        caption_font_sz  = self._f("caption-font-size",       10)
        caption_color    = self._tok("caption-font-color")
        caption_align    = self._tok("caption-alignment",     "center")
        label_font_size  = self._f("label-font-size",         9)
        label_font_color = self._tok("label-font-color")
        title_font_size  = self._f("axis-title-font-size",    10)
        title_font_color = self._tok("axis-title-font-color", axis_color)

        # ── Content fields ─────────────────────────────────────────────
        chart_type   = str(content.get("chart_type", "bar")).lower()
        series_raw   = content.get("series", [])
        if not isinstance(series_raw, list):
            series_raw = []
        labels       = [str(l) for l in content.get("labels", [])]
        stacked      = bool(content.get("stacked", False))
        value_labels = bool(content.get("value_labels", False))
        inner_radius = float(content.get("inner_radius", 0.0))
        caption      = str(content.get("caption", ""))

        # ── Axis config ────────────────────────────────────────────────
        x_axis_cfg  = content.get("x_axis", {}) or {}
        y_axis_cfg  = content.get("y_axis", {}) or {}
        x_visible   = bool(x_axis_cfg.get("visible", True))
        y_visible   = bool(y_axis_cfg.get("visible", True))
        x_title     = str(x_axis_cfg.get("title", ""))
        y_title     = str(y_axis_cfg.get("title", ""))
        y_min_forced = y_axis_cfg.get("min")
        y_max_forced = y_axis_cfg.get("max")
        y_step_forced = y_axis_cfg.get("step")
        y_fmt        = str(y_axis_cfg.get("format", ""))

        # ── Legend config ──────────────────────────────────────────────
        legend_cfg  = content.get("legend", {}) or {}
        legend_vis  = bool(legend_cfg.get("visible", True))
        leg_pos_raw = legend_cfg.get("position")
        legend_pos  = str(leg_pos_raw).lower() if leg_pos_raw else legend_pos_tok
        if legend_pos == "none":
            legend_vis = False

        # ── Space reservations ─────────────────────────────────────────
        cap_h = (caption_font_sz + 6) if caption else 0

        swatch = int(legend_font_size) + 4
        leg_item_h = swatch + 4
        leg_h = leg_w = 0.0
        if legend_vis and series_raw:
            if legend_pos in ("bottom", "top"):
                rows = math.ceil(len(series_raw) / max(1, int(box.w / 120)))
                leg_h = rows * leg_item_h + 6
            elif legend_pos == "right":
                leg_w = 100.0

        x_title_h = (title_font_size + 6) if x_title else 0
        y_title_w = (title_font_size + 6) if y_title else 0

        # ── Plot area geometry ─────────────────────────────────────────
        pad_left   = 42 + y_title_w
        pad_right  = 8 + leg_w
        pad_top    = (leg_h + 4) if legend_pos == "top" else 8
        pad_bottom = 22 + x_title_h

        plot_x = box.x + pad_left
        plot_y = box.y + pad_top
        plot_w = max(20.0, box.w - pad_left - pad_right)
        plot_h = max(20.0, box.h - pad_top - pad_bottom - cap_h
                     - (leg_h if legend_pos == "bottom" else 0))

        # ── Dispatch chart type ────────────────────────────────────────
        if chart_type == "pie":
            # For pie, use the full body without axis margins
            self._draw_pie(box, plot_x, plot_y, plot_w, plot_h,
                           series_raw, labels, inner_radius,
                           value_labels, label_font_size, label_font_color)
        else:
            self._draw_cartesian(box, plot_x, plot_y, plot_w, plot_h,
                                 series_raw, labels, chart_type,
                                 stacked, value_labels,
                                 y_min_forced, y_max_forced, y_step_forced, y_fmt,
                                 axis_color, axis_font_size, axis_font_color,
                                 grid_color, x_visible, y_visible,
                                 label_font_size, label_font_color)

        # ── Axis titles ────────────────────────────────────────────────
        if x_title:
            box.add({"type": "text",
                     "x": plot_x, "y": plot_y + plot_h + 14,
                     "w": plot_w, "h": title_font_size + 4,
                     "text": x_title, "font_size": title_font_size,
                     "font_color": title_font_color, "alignment": "center",
                     "vertical_align": "middle", "wrap": False})
        if y_title:
            box.add({"type": "text",
                     "x": box.x, "y": plot_y, "w": title_font_size + 4, "h": plot_h,
                     "text": y_title, "font_size": title_font_size,
                     "font_color": title_font_color, "alignment": "center",
                     "vertical_align": "middle", "wrap": False})

        # ── Legend ─────────────────────────────────────────────────────
        if legend_vis and series_raw:
            self._draw_legend(box, plot_x, plot_y, plot_w, plot_h,
                              series_raw, legend_pos, leg_h, leg_w,
                              legend_font_size, swatch)

        # ── Caption ────────────────────────────────────────────────────
        if caption:
            cap_y = box.y + box.h - cap_h
            box.add({"type": "text",
                     "x": box.x, "y": cap_y, "w": box.w, "h": cap_h,
                     "text": caption, "font_size": caption_font_sz,
                     "font_color": caption_color,
                     "alignment": caption_align, "wrap": False})

    # ── Cartesian engine (bar / line / combo) ─────────────────────────────

    def _draw_cartesian(  # noqa: C901
        self, box: RenderBox,
        px: float, py: float, pw: float, ph: float,
        series_raw: list[dict], labels: list[str], mode: str,
        stacked: bool, value_labels: bool,
        y_min_forced, y_max_forced, y_step_forced,
        y_fmt: str,
        axis_color: str, axis_font_size: float, axis_font_color: str,
        grid_color: str, x_visible: bool, y_visible: bool,
        label_font_size: float, label_font_color: str,
    ) -> None:
        if not series_raw or not labels:
            self._draw_placeholder(box, px, py, pw, ph)
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
            bar_idx  = []
            line_idx = list(range(n_series))
        else:  # bar
            bar_idx  = list(range(n_series))
            line_idx = []

        # ── Y scale ───────────────────────────────────────────────────
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
        step = float(y_step_forced) if y_step_forced is not None else _nice_step(y_span)

        def v2y(v: float) -> float:
            return py + ph - max(0.0, min(1.0, (v - y_min) / y_span)) * ph

        # ── Grid lines + y-axis labels ─────────────────────────────────
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
                             "text": _fmt_value(t, y_fmt),
                             "font_size": axis_font_size,
                             "font_color": axis_font_color,
                             "alignment": "right",
                             "vertical_align": "middle", "wrap": False})
            t = round(t + step, 10)

        # ── Axis lines ─────────────────────────────────────────────────
        box.add({"type": "line",
                 "x1": px, "y1": py, "x2": px, "y2": py + ph,
                 "stroke": axis_color, "stroke_width": 1})
        box.add({"type": "line",
                 "x1": px, "y1": py + ph, "x2": px + pw, "y2": py + ph,
                 "stroke": axis_color, "stroke_width": 1})

        cat_w = pw / n_labels

        # ── Bar series ─────────────────────────────────────────────────
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
                        color = self._series_color(series_raw, si)
                        box.add({"type": "rect",
                                 "x": bx, "y": by,
                                 "w": cat_w - 2 * group_pad, "h": max(bh, 0.5),
                                 "fill": color, "stroke": "none",
                                 "stroke_width": 0, "rx": 2})
                        if value_labels and bh > label_font_size + 2:
                            box.add({"type": "text",
                                     "x": bx, "y": by, "w": cat_w - 2 * group_pad, "h": bh,
                                     "text": _fmt_value(val, y_fmt),
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
                        color = self._series_color(series_raw, si)
                        box.add({"type": "rect",
                                 "x": bx, "y": by, "w": bar_w, "h": max(bh, 0.5),
                                 "fill": color, "stroke": "none",
                                 "stroke_width": 0, "rx": 2})
                        if value_labels and bh > label_font_size + 2:
                            box.add({"type": "text",
                                     "x": bx, "y": by - label_font_size - 2,
                                     "w": bar_w, "h": label_font_size + 2,
                                     "text": _fmt_value(val, y_fmt),
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

        # ── Line series ────────────────────────────────────────────────
        if line_idx:
            marker_size = self._f("line-marker-size", 5)
            default_lw  = self._f("line-width", 2)

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
                color  = self._series_color(series_raw, si)
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
                                     "text": _fmt_value(val_f, y_fmt),
                                     "font_size": label_font_size,
                                     "font_color": color,
                                     "alignment": "center", "wrap": False})

    # ── Pie / donut chart ─────────────────────────────────────────────────

    def _draw_pie(  # noqa: C901
        self, box: RenderBox,
        px: float, py: float, pw: float, ph: float,
        series_raw: list[dict], labels: list[str],
        inner_radius: float,
        value_labels: bool, label_font_size: float, label_font_color: str,
    ) -> None:
        """Draw pie chart using vertical column scan for pixel-accurate sectors."""
        if not (series_raw and labels):
            self._draw_placeholder(box, px, py, pw, ph)
            return

        n = len(labels)

        # Aggregate label values across series (single series = typical pie)
        values: list[float] = []
        if len(series_raw) == 1:
            for li in range(n):
                raw = series_raw[0].get("values", [])
                values.append(max(0.0, float(raw[li]) if li < len(raw) else 0.0))
        else:
            for li in range(n):
                total = 0.0
                for s in series_raw:
                    raw = s.get("values", [])
                    total += max(0.0, float(raw[li]) if li < len(raw) else 0.0)
                values.append(total)

        grand_total = sum(values)
        if grand_total == 0:
            self._draw_placeholder(box, px, py, pw, ph)
            return

        # Geometry
        cx = px + pw / 2
        cy = py + ph / 2
        r  = min(pw, ph) / 2 * 0.88
        inner_r = r * max(0.0, min(0.9, inner_radius))

        # Build sector colour array (one per label)
        if len(series_raw) == 1:
            pal = self._palette()
            explicit = series_raw[0].get("colors") or []  # optional list of per-label colours
            sector_colors = []
            for li in range(n):
                if li < len(explicit) and explicit[li]:
                    sector_colors.append(str(explicit[li]))
                else:
                    sector_colors.append(pal[li % len(pal)])
        else:
            sector_colors = [self._series_color(series_raw, li % len(series_raw))
                             for li in range(n)]

        # Build sector angle ranges (starting at -π/2 = top, clockwise)
        START = -math.pi / 2
        sectors: list[tuple[float, float, str]] = []  # (a1, a2, color)
        angle = START
        for li, val in enumerate(values):
            if val <= 0:
                continue
            sweep = 2 * math.pi * val / grand_total
            sectors.append((angle, angle + sweep, sector_colors[li]))
            angle += sweep

        # Column-scan rendering — accurate and clean
        bg_color = self._tok("bg-color")
        col_w = max(1.5, r / 60)  # ~60 columns per radius → smooth appearance

        xi = cx - r
        while xi < cx + r:
            dx = xi + col_w / 2 - cx  # centre of column relative to circle centre
            chord_sq = r * r - dx * dx
            if chord_sq <= 0:
                xi += col_w
                continue
            chord = math.sqrt(chord_sq)

            # Inner chord for donut
            inner_chord_sq = inner_r * inner_r - dx * dx if inner_r > 0 else -1.0
            inner_chord = math.sqrt(inner_chord_sq) if inner_chord_sq > 0 else 0.0

            # ── For each sector, find the y range within this column ────
            for a1, a2, color in sectors:
                # Determine y range where atan2(dy, dx) is in [a1, a2]
                # atan2(dy, dx) is monotone in dy for fixed dx.
                # Going from dy = -chord (top) to dy = +chord (bottom):
                #   angle_at_top    = atan2(-chord, dx) — may be in any quadrant
                #   angle_at_bottom = atan2(+chord, dx)
                #
                # Since a1, a2 are in [START, START+2π] and atan2 returns [-π, π],
                # we must normalise consistently.

                def _norm(a: float) -> float:
                    """Shift angle into [START, START + 2π)."""
                    while a < START:
                        a += 2 * math.pi
                    while a >= START + 2 * math.pi:
                        a -= 2 * math.pi
                    return a

                a_top    = _norm(math.atan2(-chord, dx))
                a_bottom = _norm(math.atan2(+chord, dx))

                # The column angle increases from top (most negative y) to bottom.
                # However, for dx < 0 the wrap at ±π makes it non-monotone in plain
                # atan2 — _norm fixes this by projecting everything to [START, START+2π].

                # Monotone check: if top > bottom after _norm, the column spans the
                # wrap boundary; we split into two sub-strips.
                def _y_for_angle(a_target: float) -> float:
                    """Inverse of atan2(dy, dx): dy = tan(a_target) * dx."""
                    if abs(dx) < 1e-9:
                        # Vertical axis: top is a=-π/2, bottom is a=+π/2 (normalised)
                        return -chord if a_target <= _norm(0.0) else +chord
                    return math.tan(a_target) * dx

                def _clip_to_chord(y: float) -> float:
                    return max(-chord, min(chord, y))

                def _draw_strip(y_lo: float, y_hi: float) -> None:
                    """Emit a rect for the portion [y_lo, y_hi] in this column."""
                    y_lo = _clip_to_chord(y_lo)
                    y_hi = _clip_to_chord(y_hi)
                    if inner_chord > 0:
                        # Remove inner circle band
                        if y_hi < -inner_chord or y_lo > inner_chord:
                            pass  # fully outside inner circle
                        else:
                            # Split: above and below inner band
                            if y_lo < -inner_chord:
                                _emit_rect(y_lo, -inner_chord)
                            if y_hi > inner_chord:
                                _emit_rect(inner_chord, y_hi)
                            return
                    _emit_rect(y_lo, y_hi)

                def _emit_rect(y_lo: float, y_hi: float) -> None:
                    if y_hi - y_lo < 0.1:
                        return
                    box.add({"type": "rect",
                             "x": xi, "y": cy + y_lo,
                             "w": col_w, "h": y_hi - y_lo,
                             "fill": color, "stroke": color,
                             "stroke_width": 0.5, "rx": 0})

                if a_top <= a_bottom:
                    # Normal case: sector range intersected with [a_top, a_bottom]
                    lo = max(a1, a_top)
                    hi = min(a2, a_bottom)
                    if lo < hi:
                        _draw_strip(_y_for_angle(lo), _y_for_angle(hi))
                else:
                    # Wrap: column spans [a_top, START+2π] ∪ [START, a_bottom]
                    # Intersect with sector [a1, a2]
                    lo1 = max(a1, a_top);  hi1 = min(a2, START + 2 * math.pi)
                    lo2 = max(a1, START);  hi2 = min(a2, a_bottom)
                    if lo1 < hi1:
                        _draw_strip(_y_for_angle(lo1), chord)
                    if lo2 < hi2:
                        _draw_strip(-chord, _y_for_angle(hi2))

            xi += col_w

        # ── Donut "punch-out" circle ───────────────────────────────────
        if inner_r > 0:
            box.add({"type": "ellipse",
                     "x": cx - inner_r, "y": cy - inner_r,
                     "w": inner_r * 2, "h": inner_r * 2,
                     "fill": bg_color, "stroke": bg_color, "stroke_width": 1})

        # ── Value labels on sectors ────────────────────────────────────
        if value_labels:
            angle = START
            for li, val in enumerate(values):
                if val <= 0:
                    continue
                sweep = 2 * math.pi * val / grand_total
                mid_a = angle + sweep / 2
                label_r = (r + inner_r) / 2 if inner_r > 0 else r * 0.65
                lx = cx + label_r * math.cos(mid_a) - 20
                ly = cy + label_r * math.sin(mid_a) - label_font_size / 2
                box.add({"type": "text",
                         "x": lx, "y": ly, "w": 40, "h": label_font_size + 2,
                         "text": f"{val / grand_total * 100:.0f}%",
                         "font_size": label_font_size,
                         "font_color": label_font_color,
                         "alignment": "center", "wrap": False})
                angle += sweep

    # ── Legend ─────────────────────────────────────────────────────────────

    def _draw_legend(
        self, box: RenderBox,
        px: float, py: float, pw: float, ph: float,
        series_raw: list[dict], position: str,
        leg_h: float, leg_w: float,
        font_size: float, swatch: float,
    ) -> None:
        leg_font_color = self._tok("legend-font-color")
        item_w = 115.0

        if position in ("bottom", "top"):
            leg_y = (box.y + box.h - leg_h + 2) if position == "bottom" else (box.y + 2)
            items_per_row = max(1, int(pw / item_w))
            for i, s in enumerate(series_raw):
                row = i // items_per_row
                col = i % items_per_row
                ix = px + col * item_w
                iy = leg_y + row * (swatch + 4)
                color = self._series_color(series_raw, i)
                box.add({"type": "rect",
                         "x": ix, "y": iy, "w": swatch, "h": swatch,
                         "fill": color, "stroke": "none", "stroke_width": 0, "rx": 2})
                box.add({"type": "text",
                         "x": ix + swatch + 3, "y": iy,
                         "w": item_w - swatch - 6, "h": swatch,
                         "text": str(s.get("name", f"Series {i + 1}")),
                         "font_size": font_size, "font_color": leg_font_color,
                         "alignment": "left", "vertical_align": "middle",
                         "wrap": False})
        elif position == "right":
            leg_x = px + pw + 6
            for i, s in enumerate(series_raw):
                iy = py + i * (swatch + 4)
                if iy + swatch > py + ph:
                    break
                color = self._series_color(series_raw, i)
                box.add({"type": "rect",
                         "x": leg_x, "y": iy, "w": swatch, "h": swatch,
                         "fill": color, "stroke": "none", "stroke_width": 0, "rx": 2})
                box.add({"type": "text",
                         "x": leg_x + swatch + 3, "y": iy,
                         "w": leg_w - swatch - 6, "h": swatch,
                         "text": str(s.get("name", f"Series {i + 1}")),
                         "font_size": font_size, "font_color": leg_font_color,
                         "alignment": "left", "vertical_align": "middle",
                         "wrap": False})

    # ── Image-based rendering (when content supplies an image path) ───────────

    def _render_image_fallback(
        self, card: CardModel, box: RenderBox, content: dict, image_path: str
    ) -> None:
        """Render a plain image + optional caption when chart content supplies an image path."""
        import logging
        logger = logging.getLogger(__name__)
        if self.project_root:
            full = self.project_root / "assets" / image_path
            if not full.exists():
                logger.warning("Chart asset not found: %s (expected at %s)", image_path, full)

        caption = str(content.get("caption", ""))
        caption_h = 20 if caption else 0
        img_h = box.h - caption_h

        box.add({"type": "image",
                 "x": box.x, "y": box.y, "w": box.w, "h": img_h,
                 "src": image_path, "alt": str(content.get("alt", "")),
                 "fit": self._tok("image-fit", "contain"),
                 "border_radius": self._tok("image-border-radius", 4)})

        if caption:
            box.add({"type": "text",
                     "x": box.x, "y": box.y + img_h + 4, "w": box.w,
                     "text": caption,
                     "font_size": self._f("caption-font-size", 11),
                     "font_color": self._tok("caption-font-color"),
                     "alignment": self._tok("caption-alignment", "center")})

    # ── Placeholder ─────────────────────────────────────────────────────────

    def _draw_placeholder(
        self, box: RenderBox, px: float, py: float, pw: float, ph: float
    ) -> None:
        border = self._tok("grid-color")
        box.add({"type": "rect",
                 "x": px, "y": py, "w": pw, "h": ph,
                 "fill": "#F9FAFB", "stroke": border, "stroke_width": 1, "rx": 4})
        box.add({"type": "text",
                 "x": px, "y": py + ph * 0.4, "w": pw,
                 "text": "[No chart data]",
                 "font_size": 11, "font_color": "#AAAAAA", "alignment": "center"})
