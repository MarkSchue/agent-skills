"""
ProcessFlowCardRenderer — Renders a horizontal process flow with N
right-pointing chevron/arrow steps (MHP "Process chart" pattern).

Each step shows an index number, a heading and an optional body. Steps
are connected visually as chevrons that point to the next step. The
optional final step can be flagged as ``accent: true`` to highlight the
end state (e.g. a goal).

Content schema::

    type: process-flow-card
    content:
      steps:
        - { title: "Discover", body: "Frame the problem." }
        - { title: "Design",   body: "Architect options." }
        - { title: "Deliver",  body: "Ship & measure.", accent: true }

Tokens (variant prefix ``card-process-flow-``):
    step-bg-color, step-accent-bg-color, step-border-color,
    step-heading-font-size/color/weight (+ -accent variants),
    step-body-font-size/color (+ -accent variants),
    step-number-font-size/color/weight (+ -accent variants),
    step-number-visible, chevron-tip-pct, step-gap.
"""

from __future__ import annotations

from typing import Any

from scripts.models.deck import CardModel
from scripts.parsing.inline_markdown import text_and_runs
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class ProcessFlowCardRenderer(BaseCardRenderer):
    """Renderer for ``process-flow-card`` type."""

    variant = "card--process-flow"

    def _tok(self, name: str, default: Any = None) -> Any:
        return self._resolve_tok("process-flow", name, default)

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        content = card.content if isinstance(card.content, dict) else {}
        steps = list(content.get("steps") or [])
        if not steps:
            return

        # ── Token resolution ───────────────────────────────────────────
        gap            = float(self._tok("step-gap") or 8)
        chev_pct       = float(self._tok("chevron-tip-pct") or 0.18)
        # Tip width as percent of step width.

        bg             = self._tok("step-bg-color") or self.resolve("color-surface-sunken") or "#F5F5F7"
        bg_accent      = self._tok("step-accent-bg-color") or self.resolve("color-primary") or "#000099"
        border         = self._tok("step-border-color") or self.resolve("color-border") or "#E0E0E0"
        border_w       = float(self._tok("step-border-width") or 0)

        head_size      = float(self._tok("step-heading-font-size") or 14)
        head_color     = self._tok("step-heading-font-color") or self.resolve("color-primary") or "#000099"
        head_weight    = self._tok("step-heading-font-weight") or "bold"
        head_color_acc = self._tok("step-heading-font-color-accent") or "#FFFFFF"

        body_size      = float(self._tok("step-body-font-size") or 11)
        body_color     = self._tok("step-body-font-color") or self.resolve("color-text-default") or "#222"
        body_color_acc = self._tok("step-body-font-color-accent") or "#FFFFFF"

        num_visible    = str(self._tok("step-number-visible") or "true").lower() == "true"
        num_size       = float(self._tok("step-number-font-size") or 28)
        num_color      = self._tok("step-number-font-color") or self.resolve("color-text-muted") or "#999"
        num_weight     = self._tok("step-number-font-weight") or "bold"
        num_color_acc  = self._tok("step-number-font-color-accent") or "#FFFFFF"

        pad_x          = float(self._tok("step-padding-x") or 16)
        pad_y          = float(self._tok("step-padding-y") or 12)

        n = len(steps)
        # Each chevron has a triangular tip on the right, width tip_w, that
        # extends BEYOND the rect width. We lay out the rectangles edge-to-edge
        # (with `gap` between them) and let chevron tips overlap the next step's
        # tail notch — so visually they look connected.
        tip_w = box.h * chev_pct
        total_w = box.w
        step_w = (total_w - tip_w - gap * (n - 1)) / n
        if step_w <= 10:
            step_w = max(40.0, total_w / n)

        for i, step in enumerate(steps):
            sx = box.x + i * (step_w + gap)
            sy = box.y
            sh = box.h
            accent = bool(step.get("accent"))
            fill = bg_accent if accent else bg

            # Emit a native chevron element. The exporter uses MSO_SHAPE.CHEVRON
            # (PPTX) and ``shape=step`` (drawio). The chevron's tip is included
            # within w; we extended the layout above to leave room for tip_w.
            box.add({
                "type": "chevron",
                "x": sx, "y": sy,
                "w": step_w + tip_w, "h": sh,
                "fill": fill,
                "stroke": border if border_w > 0 else "none",
                "stroke_width": border_w,
            })

            # Inner text region (avoid the right tip, and leave a tail offset
            # for steps after the first since their left edge has a notch).
            tail = 0 if i == 0 else tip_w
            tx = sx + tail + pad_x
            ty = sy + pad_y
            tw = step_w - tail - pad_x  # leave room for tip taper
            th = sh - pad_y * 2
            cur_y = ty

            # Step number (large, optional)
            if num_visible:
                box.add({
                    "type": "text",
                    "x": tx, "y": cur_y, "w": tw, "h": num_size + 4,
                    **text_and_runs(f"{i + 1:02d}"),
                    "font_size": num_size,
                    "font_color": num_color_acc if accent else num_color,
                    "font_weight": num_weight,
                    "alignment": "left",
                })
                cur_y += num_size + 6

            # Heading
            heading = str(step.get("title", "") or "")
            if heading:
                box.add({
                    "type": "text",
                    "x": tx, "y": cur_y, "w": tw, "h": head_size + 4,
                    **text_and_runs(heading),
                    "font_size": head_size,
                    "font_color": head_color_acc if accent else head_color,
                    "font_weight": head_weight,
                    "alignment": "left",
                })
                cur_y += head_size + 6

            # Body
            body_text = str(step.get("body", "") or "")
            if body_text:
                remaining = max(0, ty + th - cur_y)
                box.add({
                    "type": "text",
                    "x": tx, "y": cur_y, "w": tw, "h": remaining,
                    **text_and_runs(body_text),
                    "font_size": body_size,
                    "font_color": body_color_acc if accent else body_color,
                    "font_weight": "normal",
                    "alignment": "left",
                })
