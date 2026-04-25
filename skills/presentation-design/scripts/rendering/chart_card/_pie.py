"""Pie / donut chart rendering using vertical column scan for pixel-accurate sectors."""

from __future__ import annotations

import math

from scripts.rendering.base_card import RenderBox
from scripts.rendering.chart_card._palette import resolve_palette, series_color


def draw_pie(  # noqa: C901
    renderer, box: RenderBox,
    px: float, py: float, pw: float, ph: float,
    series_raw: list[dict], labels: list[str],
    inner_radius: float,
    value_labels: bool, label_font_size: float, label_font_color: str,
    placeholder,
) -> None:
    if not (series_raw and labels):
        placeholder(box, px, py, pw, ph)
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
        placeholder(box, px, py, pw, ph)
        return

    # Geometry
    cx = px + pw / 2
    cy = py + ph / 2
    r  = min(pw, ph) / 2 * 0.88
    inner_r = r * max(0.0, min(0.9, inner_radius))

    # Sector colours (one per label)
    if len(series_raw) == 1:
        pal = resolve_palette(renderer)
        explicit = series_raw[0].get("colors") or []
        sector_colors = []
        for li in range(n):
            if li < len(explicit) and explicit[li]:
                sector_colors.append(str(explicit[li]))
            else:
                sector_colors.append(pal[li % len(pal)])
    else:
        sector_colors = [series_color(renderer, series_raw, li % len(series_raw))
                         for li in range(n)]

    # Sector angle ranges (starting at -π/2 = top, clockwise)
    START = -math.pi / 2
    sectors: list[tuple[float, float, str]] = []
    angle = START
    for li, val in enumerate(values):
        if val <= 0:
            continue
        sweep = 2 * math.pi * val / grand_total
        sectors.append((angle, angle + sweep, sector_colors[li]))
        angle += sweep

    # Column-scan rendering — accurate and clean
    col_w = max(1.5, r / 60)

    xi = cx - r
    while xi < cx + r:
        dx = xi + col_w / 2 - cx
        chord_sq = r * r - dx * dx
        if chord_sq <= 0:
            xi += col_w
            continue
        chord = math.sqrt(chord_sq)

        inner_chord_sq = inner_r * inner_r - dx * dx if inner_r > 0 else -1.0
        inner_chord = math.sqrt(inner_chord_sq) if inner_chord_sq > 0 else 0.0

        for a1, a2, color in sectors:
            def _norm(a: float) -> float:
                while a < START:
                    a += 2 * math.pi
                while a >= START + 2 * math.pi:
                    a -= 2 * math.pi
                return a

            a_top    = _norm(math.atan2(-chord, dx))
            a_bottom = _norm(math.atan2(+chord, dx))

            def _y_for_angle(a_target: float) -> float:
                if abs(dx) < 1e-9:
                    return -chord if a_target <= _norm(0.0) else +chord
                return math.tan(a_target) * dx

            def _clip_to_chord(y: float) -> float:
                return max(-chord, min(chord, y))

            def _emit_rect(y_lo: float, y_hi: float) -> None:
                if y_hi - y_lo < 0.1:
                    return
                box.add({"type": "rect",
                         "x": xi, "y": cy + y_lo,
                         "w": col_w, "h": y_hi - y_lo,
                         "fill": color, "stroke": color,
                         "stroke_width": 0.5, "rx": 0})

            def _draw_strip(y_lo: float, y_hi: float) -> None:
                y_lo = _clip_to_chord(y_lo)
                y_hi = _clip_to_chord(y_hi)
                if inner_chord > 0:
                    if y_hi < -inner_chord or y_lo > inner_chord:
                        return
                    if y_lo < -inner_chord:
                        _emit_rect(y_lo, -inner_chord)
                    if y_hi > inner_chord:
                        _emit_rect(inner_chord, y_hi)
                    return
                _emit_rect(y_lo, y_hi)

            if a_top <= a_bottom:
                lo = max(a1, a_top)
                hi = min(a2, a_bottom)
                if lo < hi:
                    _draw_strip(_y_for_angle(lo), _y_for_angle(hi))
            else:
                lo1 = max(a1, a_top);  hi1 = min(a2, START + 2 * math.pi)
                lo2 = max(a1, START);  hi2 = min(a2, a_bottom)
                if lo1 < hi1:
                    _draw_strip(_y_for_angle(lo1), chord)
                if lo2 < hi2:
                    _draw_strip(-chord, _y_for_angle(hi2))

        xi += col_w

    # Donut "punch-out" circle
    if inner_r > 0:
        bg_color = renderer._tok("bg-color")
        box.add({"type": "ellipse",
                 "x": cx - inner_r, "y": cy - inner_r,
                 "w": inner_r * 2, "h": inner_r * 2,
                 "fill": bg_color, "stroke": bg_color, "stroke_width": 1})

    # Value labels on sectors
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
