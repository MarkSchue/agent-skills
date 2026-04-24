"""
QuadrantCardRenderer — Renders a 2×2 matrix card (SWOT, BCG matrix,
prioritisation grid, Eisenhower box, etc.).

Four labelled quadrants in a 2×2 grid with optional axis labels along the
top edge (low → high) and left edge (low → high). Each quadrant has a
heading, an optional accent fill and either a body string or a list of
bullet items.

Content schema::

    type: quadrant-card
    content:
      x_axis: { low: "Short Term",  high: "Long Term"  }   # optional
      y_axis: { low: "Low Impact",  high: "High Impact" }  # optional
      quadrants:
        - { title: "Quick Wins",  items: ["...", "..."], accent: true }
        - { title: "Major Bets",  items: ["..."] }
        - { title: "Fill-ins",    body: "..." }
        - { title: "Reconsider",  body: "..." }

Quadrant order is row-major top-left → top-right → bottom-left → bottom-right.
"""

from __future__ import annotations

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class QuadrantCardRenderer(BaseCardRenderer):
    """Renderer for ``quadrant-card`` type."""

    variant = "card--quadrant"

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        content = card.content if isinstance(card.content, dict) else {}
        quads = list(content.get("quadrants") or [])
        # Normalise to exactly 4 entries
        while len(quads) < 4:
            quads.append({})
        quads = quads[:4]

        x_axis = content.get("x_axis") or {}
        y_axis = content.get("y_axis") or {}

        # ── Token resolution ───────────────────────────────────────────
        gap            = float(self._tok("tile-gap") or 12)
        tile_bg        = self._tok("tile-bg-color") or self.resolve("color-surface-sunken") or "#F5F5F7"
        tile_accent    = self._tok("tile-accent-bg-color") or self.resolve("color-primary") or "#000099"
        tile_border    = self._tok("tile-border-color") or self.resolve("color-border") or "#E0E0E0"
        tile_border_w  = float(self._tok("tile-border-width") or 0)

        head_size      = float(self._tok("quadrant-heading-font-size") or 14)
        head_color     = self._tok("quadrant-heading-font-color") or self.resolve("color-primary") or "#000099"
        head_weight    = self._tok("quadrant-heading-font-weight") or "bold"
        head_color_acc = self._tok("quadrant-heading-font-color-accent") or "#FFFFFF"

        body_size      = float(self._tok("quadrant-body-font-size") or 11)
        body_color     = self._tok("quadrant-body-font-color") or self.resolve("color-text-default") or "#222"
        body_color_acc = self._tok("quadrant-body-font-color-accent") or "#FFFFFF"

        bullet_char    = self._tok("bullet-char") or "•"
        # Unescape CSS-style unicode escapes (e.g. "\2022" → "•") that may
        # arrive from theme tokens written as `--card-quadrant-bullet-char: "\2022";`
        if bullet_char and bullet_char.startswith("\\"):
            try:
                bullet_char = chr(int(bullet_char.lstrip("\\").strip(), 16))
            except (ValueError, TypeError):
                bullet_char = "•"
        bullet_gap     = float(self._tok("bullet-gap") or 6)

        axis_size      = float(self._tok("axis-label-font-size") or 10)
        axis_color     = self._tok("axis-label-font-color") or self.resolve("color-text-muted") or "#666"
        axis_weight    = self._tok("axis-label-font-weight") or "normal"
        axis_visible   = str(self._tok("axis-visible") or "true").lower() == "true"
        axis_pad       = float(self._tok("axis-pad") or 16)

        has_x = axis_visible and (x_axis.get("low") or x_axis.get("high"))
        has_y = axis_visible and (y_axis.get("low") or y_axis.get("high"))

        # Reserve space for axis labels
        top_pad   = axis_size + 6 if has_x else 0
        left_pad  = axis_size + axis_pad if has_y else 0

        grid_x = box.x + left_pad
        grid_y = box.y + top_pad
        grid_w = box.w - left_pad
        grid_h = box.h - top_pad

        # ── Axis labels ────────────────────────────────────────────────
        if has_x:
            half_w = grid_w / 2
            box.add({
                "type": "text",
                "x": grid_x, "y": box.y, "w": half_w, "h": axis_size + 4,
                "text": str(x_axis.get("low", "")),
                "font_size": axis_size,
                "font_color": axis_color,
                "font_weight": axis_weight,
                "alignment": "left",
                "wrap": False,
            })
            box.add({
                "type": "text",
                "x": grid_x + half_w, "y": box.y,
                "w": half_w, "h": axis_size + 4,
                "text": str(x_axis.get("high", "")),
                "font_size": axis_size,
                "font_color": axis_color,
                "font_weight": axis_weight,
                "alignment": "right",
                "wrap": False,
            })

        if has_y:
            half_h = grid_h / 2
            # "high" sits at top of the y-axis, "low" at bottom (chart convention)
            box.add({
                "type": "text",
                "x": box.x, "y": grid_y, "w": left_pad - 4, "h": axis_size + 4,
                "text": str(y_axis.get("high", "")),
                "font_size": axis_size,
                "font_color": axis_color,
                "font_weight": axis_weight,
                "alignment": "right",
                "wrap": False,
            })
            box.add({
                "type": "text",
                "x": box.x, "y": grid_y + grid_h - axis_size - 4,
                "w": left_pad - 4, "h": axis_size + 4,
                "text": str(y_axis.get("low", "")),
                "font_size": axis_size,
                "font_color": axis_color,
                "font_weight": axis_weight,
                "alignment": "right",
                "wrap": False,
            })

        # ── 2×2 tile geometry ──────────────────────────────────────────
        tile_w = (grid_w - gap) / 2
        tile_h = (grid_h - gap) / 2

        for idx, q in enumerate(quads):
            row = idx // 2
            col = idx % 2
            tx = grid_x + col * (tile_w + gap)
            ty = grid_y + row * (tile_h + gap)

            is_accent = bool(q.get("accent"))
            fill = tile_accent if is_accent else tile_bg
            stroke = "none" if (tile_border_w == 0 or is_accent) else tile_border

            box.add({
                "type": "rect",
                "x": tx, "y": ty, "w": tile_w, "h": tile_h,
                "fill": fill, "stroke": stroke,
                "stroke_width": tile_border_w,
            })

            inner_pad = 12.0
            ix = tx + inner_pad
            iy = ty + inner_pad
            iw = tile_w - 2 * inner_pad

            head_text = str(q.get("title", "") or "")
            if head_text:
                box.add({
                    "type": "text",
                    "x": ix, "y": iy, "w": iw, "h": head_size + 4,
                    "text": head_text,
                    "font_size": head_size,
                    "font_color": head_color_acc if is_accent else head_color,
                    "font_weight": head_weight,
                    "alignment": "left",
                    "wrap": False,
                })
                iy += head_size + 8

            items = q.get("items")
            body  = q.get("body")
            body_col = body_color_acc if is_accent else body_color

            line_h = body_size * 1.45
            avail_h = ty + tile_h - inner_pad - iy

            if isinstance(items, list) and items:
                for item in items:
                    if avail_h < line_h:
                        break
                    text = f"{bullet_char} {item}"
                    box.add({
                        "type": "text",
                        "x": ix, "y": iy, "w": iw, "h": line_h,
                        "text": text,
                        "font_size": body_size,
                        "font_color": body_col,
                        "alignment": "left",
                        "wrap": True,
                    })
                    iy += line_h + bullet_gap
                    avail_h -= line_h + bullet_gap
            elif body:
                box.add({
                    "type": "text",
                    "x": ix, "y": iy, "w": iw, "h": max(0, avail_h),
                    "text": str(body),
                    "font_size": body_size,
                    "font_color": body_col,
                    "alignment": "left",
                    "vertical_align": "top",
                    "wrap": True,
                })
