"""
PyramidCardRenderer — Renders a stacked-trapezoid hierarchy pyramid
(MHP "Pyramid Chart" pattern, also Maslow / strategic hierarchy).

Layers stack bottom-up by default: the FIRST item in ``layers`` is the
widest base, the LAST is the narrowest apex. Each layer has a label and
optional body text, and may be flagged ``accent: true`` to highlight one
strategic level.

Content schema::

    type: pyramid-card
    content:
      direction: bottom-up   # default; or "top-down" to reverse
      layers:
        - { title: "Foundation",  body: "Operational basics" }
        - { title: "Capability",  body: "Skills & tooling", accent: true }
        - { title: "Strategy",    body: "Direction & vision" }

Tokens (variant prefix ``card-pyramid-``):
    layer-bg-color, layer-accent-bg-color, layer-border-color,
    layer-heading-font-size/color/weight (+ -accent),
    layer-body-font-size/color (+ -accent), layer-gap,
    layer-label-position (left | right | inline),
    label-line-color/width.
"""

from __future__ import annotations

from typing import Any

from scripts.models.deck import CardModel
from scripts.parsing.inline_markdown import text_and_runs
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class PyramidCardRenderer(BaseCardRenderer):
    """Renderer for ``pyramid-card`` type."""

    variant = "card--pyramid"

    def _tok(self, name: str, default: Any = None) -> Any:
        return self._resolve_tok("pyramid", name, default)

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        content = card.content if isinstance(card.content, dict) else {}
        layers = list(content.get("layers") or [])
        if not layers:
            return

        direction = str(content.get("direction") or "bottom-up").lower()

        # ── Token resolution ───────────────────────────────────────────
        gap            = float(self._tok("layer-gap") or 4)
        # Fall back to a medium gray so pyramid layers remain visible even on
        # near-white slide backgrounds (color-surface-sunken is often too light).
        bg             = self._tok("layer-bg-color") or self.resolve("color-border") or "#D8D8D8"
        bg_accent      = self._tok("layer-accent-bg-color") or self.resolve("color-primary") or "#000099"
        border         = self._tok("layer-border-color") or self.resolve("color-border") or "#E0E0E0"
        border_w       = float(self._tok("layer-border-width") or 0)

        head_size      = float(self._tok("layer-heading-font-size") or 14)
        head_color     = self._tok("layer-heading-font-color") or self.resolve("color-text-default") or "#222"
        head_weight    = self._tok("layer-heading-font-weight") or "bold"
        head_color_acc = self._tok("layer-heading-font-color-accent") or "#FFFFFF"

        body_size      = float(self._tok("layer-body-font-size") or 11)
        body_color     = self._tok("layer-body-font-color") or self.resolve("color-text-muted") or "#666"
        body_color_acc = self._tok("layer-body-font-color-accent") or "#FFFFFF"

        label_pos      = str(self._tok("layer-label-position") or "right").lower()
        # "right" → labels to the right of the pyramid (with leader lines)
        # "inline" → label inside each layer (centered)

        line_color     = self._tok("label-line-color") or self.resolve("color-border") or "#CCCCCC"
        line_width     = float(self._tok("label-line-width") or 1)

        # ── Layout: pyramid occupies left half if labels are to the side ──
        if label_pos == "inline":
            pyramid_w = box.w
            pyr_x = box.x
            label_x = None
        else:
            pyramid_w = box.w * 0.42
            pyr_x = box.x
            label_x = box.x + pyramid_w + 24

        n = len(layers)
        layer_h = (box.h - gap * (n - 1)) / n

        # Sort visually: layer index 0 is at the BOTTOM (widest) by default.
        # If direction == "top-down" we reverse so first = top (narrowest).
        if direction == "top-down":
            ordered = list(layers)               # first listed → top
        else:
            ordered = list(reversed(layers))     # first listed → bottom

        # The pyramid as a whole is an isoceles triangle. Each layer is a
        # trapezoid slice. Width of layer k (0 = top, n-1 = bottom) =
        #   pyramid_w * (k + 1) / n
        # Each trapezoid's narrow edge = width of layer above; wide edge = its
        # own width. Implementation: emit trapezoid elements with the right
        # `narrow_pct` so each layer matches the next one above it visually.

        cx = pyr_x + pyramid_w / 2

        for slot_idx, layer in enumerate(ordered):
            # slot_idx 0 = TOP layer in screen space
            top_layer_idx = slot_idx                    # 0..n-1, top→bottom
            # Map back to the source layer for content lookup
            source_layer = layer

            # Width of THIS slice's wide edge (= the bottom of this slice)
            wide_w   = pyramid_w * (top_layer_idx + 1) / n
            # Width of slice ABOVE = top edge of this slice (apex when top_layer_idx == 0)
            narrow_w = pyramid_w * top_layer_idx / n

            sy = box.y + slot_idx * (layer_h + gap)
            sx = cx - wide_w / 2
            narrow_pct = (narrow_w / wide_w) if wide_w > 0 else 0

            accent = bool(source_layer.get("accent"))
            fill = bg_accent if accent else bg

            box.add({
                "type": "trapezoid",
                "orientation": "down",   # narrow at top, wide at bottom
                "x": sx, "y": sy,
                "w": wide_w, "h": layer_h,
                "fill": fill,
                "stroke": border if border_w > 0 else "none",
                "stroke_width": border_w,
                # Style hint consumed by SVG renderer for proper rendering
                "narrow_pct": narrow_pct,
            })

            # ── Label rendering ───────────────────────────────────────
            heading = str(source_layer.get("title", "") or "")
            body_text = str(source_layer.get("body", "") or "")

            if label_pos == "inline":
                # Centered inside the trapezoid
                if heading:
                    box.add({
                        "type": "text",
                        "x": sx, "y": sy + layer_h / 2 - head_size,
                        "w": wide_w, "h": head_size + 4,
                        **text_and_runs(heading),
                        "font_size": head_size,
                        "font_color": head_color_acc if accent else head_color,
                        "font_weight": head_weight,
                        "alignment": "center",
                    })
                if body_text:
                    box.add({
                        "type": "text",
                        "x": sx, "y": sy + layer_h / 2 + 2,
                        "w": wide_w, "h": body_size + 2,
                        **text_and_runs(body_text),
                        "font_size": body_size,
                        "font_color": body_color_acc if accent else body_color,
                        "font_weight": "normal",
                        "alignment": "center",
                    })
            else:
                # Side label: leader line from layer's right edge to the label.
                leader_x1 = cx + wide_w / 2
                leader_x2 = label_x - 8
                leader_y  = sy + layer_h / 2
                box.add({
                    "type": "line",
                    "x1": leader_x1, "y1": leader_y,
                    "x2": leader_x2, "y2": leader_y,
                    "stroke": line_color, "stroke_width": line_width,
                })
                label_w = box.x + box.w - label_x
                cur_y = sy + 4
                if heading:
                    box.add({
                        "type": "text",
                        "x": label_x, "y": cur_y,
                        "w": label_w, "h": head_size + 4,
                        **text_and_runs(heading),
                        "font_size": head_size,
                        "font_color": head_color,
                        "font_weight": head_weight,
                        "alignment": "left",
                    })
                    cur_y += head_size + 4
                if body_text:
                    remaining = max(0, sy + layer_h - cur_y - 2)
                    box.add({
                        "type": "text",
                        "x": label_x, "y": cur_y,
                        "w": label_w, "h": remaining,
                        **text_and_runs(body_text),
                        "font_size": body_size,
                        "font_color": body_color,
                        "font_weight": "normal",
                        "alignment": "left",
                    })
