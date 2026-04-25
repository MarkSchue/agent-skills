"""
GaugeCardRenderer — A row of 2-5 donut gauges, each showing a percentage
with a heading and optional body text. Inspired by KPI / dashboard slides
in the MHP Slide Library.

Content schema::

    type: gauge-card
    content:
      gauges:
        - { value: 76, heading: "Adoption", body: "of teams onboarded", icon: "groups" }
        - { value: 92, heading: "Quality",  body: "release pass rate" }
        - { value: 41, heading: "Cost",     body: "vs. baseline", color: "#E5546A" }

Tokens (variant prefix ``card-gauge-``):
    ring-radius (px max), ring-thickness (fraction 0..1 of ring radius),
    ring-bg-color, ring-fg-color (default = primary; per-gauge `color` overrides),
    value-font-size/color/weight, value-suffix (default "%"),
    heading-font-size/color/weight,
    body-font-size/color,
    gauge-gap (px between gauges).

Geometry: each gauge takes an equal horizontal slot. Inside its slot:
    - donut ring centred horizontally, near the top
    - % value centred inside the ring
    - heading below the ring (bold, primary)
    - body below the heading (muted)
"""

from __future__ import annotations

from typing import Any

from scripts.models.deck import CardModel
from scripts.parsing.inline_markdown import text_and_runs
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class GaugeCardRenderer(BaseCardRenderer):
    """Renderer for ``gauge-card`` type."""

    variant = "card--gauge"

    def _tok(self, name: str, default: Any = None) -> Any:
        return self._resolve_tok("gauge", name, default)

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        content = card.content if isinstance(card.content, dict) else {}
        gauges = list(content.get("gauges") or [])
        if not gauges:
            return
        n = len(gauges)

        # ── Tokens ────────────────────────────────────────────────────
        max_radius   = float(self._tok("ring-radius") or 64)
        thickness    = float(self._tok("ring-thickness") or 0.22)
        bg_color     = self._tok("ring-bg-color") or self.resolve("color-surface-sunken") or "#EEEEEE"
        fg_color_def = self._tok("ring-fg-color") or self.resolve("color-primary") or "#000099"

        val_size_tok = self._tok("value-font-size")  # may be None → derived from radius
        val_color    = self._tok("value-font-color") or self.resolve("color-primary") or "#000099"
        val_weight   = self._tok("value-font-weight") or "bold"
        val_suffix   = str(self._tok("value-suffix") or "%")

        head_size    = float(self._tok("heading-font-size") or 14)
        head_color   = self._tok("heading-font-color") or self.resolve("color-text-default") or "#222"
        head_weight  = self._tok("heading-font-weight") or "bold"

        body_size    = float(self._tok("body-font-size") or 11)
        body_color   = self._tok("body-font-color") or self.resolve("color-text-muted") or "#666"

        gap          = float(self._tok("gauge-gap") or 16)

        # ── Geometry ──────────────────────────────────────────────────
        slot_w = (box.w - gap * (n - 1)) / n
        # Pick radius that fits both horizontally and vertically (leaving
        # room for heading + body below). Reserve 80px for text below ring.
        text_block_h = head_size + body_size * 3 + 16
        radius = min(max_radius, slot_w / 2 - 8, (box.h - text_block_h) / 2 - 8)
        radius = max(28.0, radius)
        outer_r = radius
        inner_r = radius * (1 - max(0.05, min(0.6, thickness)))

        val_size = float(val_size_tok or radius * 0.55)

        for i, g in enumerate(gauges):
            try:
                value = float(g.get("value", 0))
            except (TypeError, ValueError):
                value = 0
            value = max(0.0, min(100.0, value))
            fg_color = g.get("color") or fg_color_def

            slot_x = box.x + i * (slot_w + gap)
            cx = slot_x + slot_w / 2
            cy = box.y + outer_r + 4

            # Background full ring (0° → 360°). SVG can't draw a full circle as
            # one arc, so we cap at 359.99° in the renderer; the small gap is
            # imperceptible. Use a single full annulus via two arc segments.
            box.add({
                "type": "arc",
                "cx": cx, "cy": cy,
                "outer_radius": outer_r,
                "inner_radius": inner_r,
                "start_angle": -90.0,
                "end_angle":   269.99,
                "fill": bg_color,
                "stroke": "none",
                "stroke_width": 0,
            })

            # Foreground arc (0° at top, sweeping CW by value%)
            if value > 0:
                sweep = (value / 100.0) * 360.0
                box.add({
                    "type": "arc",
                    "cx": cx, "cy": cy,
                    "outer_radius": outer_r,
                    "inner_radius": inner_r,
                    "start_angle": -90.0,
                    "end_angle":   -90.0 + sweep,
                    "fill": fg_color,
                    "stroke": "none",
                    "stroke_width": 0,
                })

            # Center mask ellipse — creates the donut hole in PPTX (blockArc adj3
            # does not reliably hollow out the shape; an overlaid white ellipse does).
            # In drawio the arc already renders as a donut; the white ellipse is harmless.
            slide_bg = self.resolve("color-background") or "#FFFFFF"
            box.add({
                "type": "ellipse",
                "x": cx - inner_r,
                "y": cy - inner_r,
                "w": inner_r * 2,
                "h": inner_r * 2,
                "fill": slide_bg,
                "stroke": "none",
                "stroke_width": 0,
            })

            # Value label centred in the ring
            label = f"{int(round(value))}{val_suffix}"
            box.add({
                "type": "text",
                "x": cx - outer_r,
                "y": cy - val_size / 2 - 2,
                "w": outer_r * 2,
                "h": val_size + 6,
                **text_and_runs(label),
                "font_size": val_size,
                "font_color": val_color,
                "font_weight": val_weight,
                "alignment": "center",
                "vertical_align": "middle",
            })

            # Heading + body below the ring
            ty = cy + outer_r + 10
            heading = str(g.get("heading", "") or "")
            if heading:
                box.add({
                    "type": "text",
                    "x": slot_x, "y": ty, "w": slot_w, "h": head_size + 4,
                    **text_and_runs(heading),
                    "font_size": head_size,
                    "font_color": head_color,
                    "font_weight": head_weight,
                    "alignment": "center",
                })
                ty += head_size + 4

            body_text = str(g.get("body", "") or "")
            if body_text:
                box.add({
                    "type": "text",
                    "x": slot_x, "y": ty, "w": slot_w,
                    "h": max(0.0, box.y + box.h - ty),
                    **text_and_runs(body_text),
                    "font_size": body_size,
                    "font_color": body_color,
                    "font_weight": "normal",
                    "alignment": "center",
                })
