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
        ic_font    = str(self.resolve("icon-font-family") or "Material Symbols Outlined")

        head_size  = float(self._tok("step-heading-font-size") or 14)
        head_color = self._tok("step-heading-font-color") or self.resolve("color-text-default") or "#222"
        head_weight= self._tok("step-heading-font-weight") or "bold"

        body_size  = float(self._tok("step-body-font-size") or 11)
        body_color = self._tok("step-body-font-color") or self.resolve("color-text-muted") or "#666"

        text_gap   = float(self._tok("step-text-gap") or 8)
        # Connector lines are off by default — text blocks below the circles
        # provide enough visual rhythm without extra lines.
        connector  = str(self._tok("step-connector-visible") or "false").lower() == "true"
        conn_color = self._tok("step-connector-color") or self.resolve("color-border") or "#CCCCCC"
        conn_width = float(self._tok("step-connector-width") or 1.5)
        conn_dash  = str(self._tok("step-connector-dashed") or "true").lower() == "true"

        # ── Geometry ──────────────────────────────────────────────────
        # Reserve vertical space at the bottom for the text block of the
        # lowest (leftmost) step. Circles are placed on the diagonal within
        # the upper portion; all steps then have room for text below them.
        slot_w = box.w / n
        slot_margin = 8.0  # horizontal padding inside each slot

        # How much height to keep clear for text beneath the lowest circle.
        text_reserve = head_size + 4 + body_size * 4 + text_gap + 8

        # Height available for the circle diagonal (must be at least 2*radius).
        diag_h = max(box.h - text_reserve, 2 * c_radius + 4)

        if n > 1:
            row_gap = (diag_h - 2 * c_radius) / (n - 1)
        else:
            row_gap = 0

        for i, step in enumerate(steps):
            slot_x = box.x + slot_w * i

            # Circle centre: left-aligned within slot (matching text indent),
            # diagonally placed within the reserved diagonal area.
            cx_centre = slot_x + slot_margin + c_radius
            cy_centre = box.y + c_radius + (n - 1 - i) * row_gap

            # Circle
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

            # Icon centred in circle
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
                    "font_family": ic_font,
                })

            # Optional connector line to next step
            if connector and i < n - 1:
                next_cx = box.x + slot_w * (i + 1) + slot_w / 2
                next_cy = box.y + c_radius + (n - 2 - i) * row_gap
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

            # ── Text block BELOW the circle ────────────────────────────
            # Uses the full slot width so body text wraps in a proper block
            # rather than a single long line beside the circle.
            tx = slot_x + slot_margin
            tw = slot_w - 2 * slot_margin
            ty = cy_centre + c_radius + text_gap

            # Available height from below the circle to the bottom of the box
            available_h = box.y + box.h - ty

            if available_h <= head_size:
                # No space for text (can happen for the lowest/leftmost step
                # when the circle sits near the bottom edge)
                continue

            heading = str(step.get("title", "") or "")
            if heading:
                h_height = min(head_size + 4, available_h)
                box.add({
                    "type": "text",
                    "x": tx, "y": ty, "w": tw, "h": h_height,
                    **text_and_runs(heading),
                    "font_size": head_size,
                    "font_color": head_color,
                    "font_weight": head_weight,
                    "alignment": "left",
                    "wrap": True,
                })
                ty += h_height + 4
                available_h -= h_height + 4

            body_text = str(step.get("body", "") or "")
            if body_text and available_h > body_size:
                box.add({
                    "type": "text",
                    "x": tx, "y": ty, "w": tw,
                    "h": max(body_size * 2, available_h),
                    **text_and_runs(body_text),
                    "font_size": body_size,
                    "font_color": body_color,
                    "font_weight": "normal",
                    "alignment": "left",
                    "wrap": True,
                })
