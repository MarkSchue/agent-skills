"""
StepCardRenderer — Diagonal "stair" of 3-5 steps. Each step has an
icon-bearing circle, a heading and an optional body. Steps are arranged
along an ascending diagonal (left-bottom → right-top), evoking progress
or maturity. Inspired by the MHP Slide Library "stair" pattern.

Content schema::

    type: step-card
    content:
      steps:
        - { title: "Assess",   body: "...", icon: "search" }
        - { title: "Design",   body: "...", icon: "palette" }
        - { title: "Build",    body: "...", icon: "build" }
        - { title: "Operate",  body: "...", icon: "rocket_launch" }

Tokens (variant prefix ``card-step-``):
    step-circle-radius, step-circle-stroke-color, step-circle-stroke-width,
    step-circle-fill-color, step-icon-color, step-icon-size,
    step-heading-font-size, step-heading-font-color, step-heading-font-weight,
    step-body-font-size, step-body-font-color,
    step-text-gap, step-row-gap.
"""

from __future__ import annotations

from typing import Any

from scripts.models.deck import CardModel
from scripts.parsing.inline_markdown import text_and_runs
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class StepCardRenderer(BaseCardRenderer):
    """Renderer for ``step-card`` type."""

    variant = "card--step"

    def _tok(self, name: str, default: Any = None) -> Any:
        return self._resolve_tok("step", name, default)

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        content = card.content if isinstance(card.content, dict) else {}
        steps = list(content.get("steps") or [])
        if not steps:
            return
        n = len(steps)

        # ── Token resolution ───────────────────────────────────────────
        c_radius   = float(self._tok("step-circle-radius") or 32)
        c_stroke   = self._tok("step-circle-stroke-color") or self.resolve("color-primary") or "#000099"
        c_stroke_w = float(self._tok("step-circle-stroke-width") or 2.5)
        c_fill     = self._tok("step-circle-fill-color") or "#FFFFFF"
        ic_color   = self._tok("step-icon-color") or self.resolve("color-primary") or "#000099"
        ic_size    = float(self._tok("step-icon-size") or 28)

        head_size  = float(self._tok("step-heading-font-size") or 14)
        head_color = self._tok("step-heading-font-color") or self.resolve("color-text-default") or "#222"
        head_weight= self._tok("step-heading-font-weight") or "bold"

        body_size  = float(self._tok("step-body-font-size") or 11)
        body_color = self._tok("step-body-font-color") or self.resolve("color-text-muted") or "#666"

        text_gap   = float(self._tok("step-text-gap") or 12)
        connector  = str(self._tok("step-connector-visible") or "true").lower() == "true"
        conn_color = self._tok("step-connector-color") or self.resolve("color-border") or "#CCCCCC"
        conn_width = float(self._tok("step-connector-width") or 1.5)
        conn_dash  = str(self._tok("step-connector-dashed") or "true").lower() == "true"

        # ── Geometry ──────────────────────────────────────────────────
        # Distribute step centres along a diagonal from bottom-left to
        # top-right of `box`. Each step gets a horizontal slot of width
        # `slot_w`; the circle sits in its left third, text wraps to the right.
        slot_w = box.w / n
        # vertical rise per step (ascending from bottom to top)
        if n > 1:
            row_gap = (box.h - 2 * c_radius) / (n - 1)
        else:
            row_gap = 0

        # Estimate text block height to size each row
        text_h = head_size + 6 + body_size * 3  # ~3 lines body
        row_h = max(2 * c_radius, text_h)

        # Anchor: first step at bottom-left, last at top-right of box
        for i, step in enumerate(steps):
            # Diagonal placement: x increases linearly, y decreases linearly
            cx_centre = box.x + slot_w * i + c_radius + 8
            # y baseline of the row this step occupies
            row_top = box.y + (n - 1 - i) * row_gap
            cy_centre = row_top + c_radius

            # Circle (ellipse with optional fill, stroke)
            box.add({
                "type": "ellipse",
                "x": cx_centre - c_radius,
                "y": cy_centre - c_radius,
                "w": c_radius * 2,
                "h": c_radius * 2,
                "fill": c_fill,
                "stroke": c_stroke,
                "stroke_width": c_stroke_w,
            })

            # Icon centred in circle (Material Symbols / Phosphor lookup
            # is handled by the icon element type).
            icon_name = step.get("icon")
            if icon_name:
                box.add({
                    "type": "icon",
                    "name": str(icon_name),
                    "x": cx_centre - ic_size / 2,
                    "y": cy_centre - ic_size / 2,
                    "w": ic_size,
                    "h": ic_size,
                    "color": ic_color,
                })

            # Connector line to next step (drawn from this circle's centre-right
            # to next circle's centre-left, with a vertical jog)
            if connector and i < n - 1:
                next_cx = box.x + slot_w * (i + 1) + c_radius + 8
                next_row_top = box.y + (n - 2 - i) * row_gap
                next_cy = next_row_top + c_radius
                # Diagonal segment from this circle's right edge to next circle's left edge
                box.add({
                    "type": "line",
                    "x1": cx_centre + c_radius,
                    "y1": cy_centre,
                    "x2": next_cx - c_radius,
                    "y2": next_cy,
                    "stroke": conn_color,
                    "stroke_width": conn_width,
                    "dashed": conn_dash,
                })

            # Text block to the right of the circle
            tx = cx_centre + c_radius + text_gap
            tw = max(60.0, box.x + box.w - tx - 6)
            ty = cy_centre - (head_size + 6 + body_size * 2) / 2

            heading = str(step.get("title", "") or "")
            if heading:
                box.add({
                    "type": "text",
                    "x": tx, "y": ty, "w": tw, "h": head_size + 4,
                    **text_and_runs(heading),
                    "font_size": head_size,
                    "font_color": head_color,
                    "font_weight": head_weight,
                    "alignment": "left",
                })
                ty += head_size + 4

            body_text = str(step.get("body", "") or "")
            if body_text:
                box.add({
                    "type": "text",
                    "x": tx, "y": ty, "w": tw, "h": body_size * 4,
                    **text_and_runs(body_text),
                    "font_size": body_size,
                    "font_color": body_color,
                    "font_weight": "normal",
                    "alignment": "left",
                })
