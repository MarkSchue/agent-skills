"""
StackedTextCardRenderer — Renders stacked-text-card with 2–4 equal-height
content blocks, each composed of an h2-style heading and a body text section.

Layout principle (requirement-critical):
  The body area is divided into *n* equal slots, where *n* is the number of
  blocks (2–4).  Slot boundaries are therefore at fixed proportional positions
  regardless of text content.  Two stacked-text cards with the same block count
  placed on the same slide will always show their divider lines at the same
  vertical position — even when one card has much shorter text than the other.

    slot_h  = (available_height - gap_top - gap_bottom) / n
    divider_y[k] = box.y + gap_top + (k+1) * slot_h   (k = 0 … n−2)

All visual properties are controlled through ``--card-stacked-text-*`` tokens on
the ``.card--stacked-text`` variant class, overridable per instance via the
``style_overrides`` YAML key (same override chain as all other card types).
"""

from __future__ import annotations

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class StackedTextCardRenderer(BaseCardRenderer):
    """Renderer for ``stacked-text-card`` type.

    Blocks are always equal-height so divider lines align across cards with
    the same block count on the same slide.
    """

    variant = "card--stacked-text"

    # ── helper: pick divider x1/x2 based on alignment + length ──────────

    @staticmethod
    def _divider_x(box_x: float, box_w: float, length_px: float, alignment: str):
        if alignment == "center":
            cx = box_x + box_w / 2
            return cx - length_px / 2, cx + length_px / 2
        if alignment == "right":
            return box_x + box_w - length_px, box_x + box_w
        # default: left
        return box_x, box_x + length_px

    # ── render_body ───────────────────────────────────────────────────────

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        """Render equal-height block slots with heading, body, and dividers."""
        content = card.content if isinstance(card.content, dict) else {}
        raw_blocks = content.get("blocks", [])

        if not raw_blocks:
            return

        # Normalise: blocks may be plain strings or dicts
        blocks: list[dict] = []
        for entry in raw_blocks:
            if isinstance(entry, dict):
                blocks.append(
                    {
                        "heading": str(entry.get("heading", "")),
                        "body":    str(entry.get("body", "")),
                    }
                )
            else:
                blocks.append({"heading": "", "body": str(entry)})

        n = max(2, min(4, len(blocks)))  # clamp to 2–4
        blocks = blocks[:n]

        # ── Token resolution ──────────────────────────────────────────────

        # Heading (h2-style)
        h_size   = float(self.resolve("card-stacked-text-heading-font-size")   or 14)
        h_color  = self.resolve("card-stacked-text-heading-font-color")         or self.resolve("card-title-font-color") or "#1A1A1A"
        h_weight = str(self.resolve("card-stacked-text-heading-font-weight")    or "700")
        h_style  = self.resolve("card-stacked-text-heading-font-style")         or "normal"
        h_align  = self.resolve("card-stacked-text-heading-alignment")          or "left"

        # Body (text-body style)
        b_size   = float(self.resolve("card-stacked-text-body-font-size")       or 12)
        b_color  = self.resolve("card-stacked-text-body-font-color")            or self.resolve("text-body-font-color") or "#333333"
        b_weight = str(self.resolve("card-stacked-text-body-font-weight")       or "400")
        b_style  = self.resolve("card-stacked-text-body-font-style")            or "normal"
        b_align  = self.resolve("card-stacked-text-body-alignment")             or "left"

        # Divider between blocks
        div_visible_raw = self.resolve("card-stacked-text-divider-visible")
        div_visible    = div_visible_raw in (True, "true", "True")
        div_color      = self.resolve("card-stacked-text-divider-color")        or self.resolve("card-title-line-color") or "#003087"
        div_width      = float(self.resolve("card-stacked-text-divider-width")  or 1)
        div_length_pct = float(self.resolve("card-stacked-text-divider-length-pct") or 50) / 100
        div_alignment  = self.resolve("card-stacked-text-divider-alignment")    or "left"

        # Vertical gaps
        gap_top       = float(self.resolve("card-stacked-text-gap-top")         or 0)
        gap_bottom    = float(self.resolve("card-stacked-text-gap-bottom")      or 0)
        gap_between   = float(self.resolve("card-stacked-text-gap-between")     or 8)
        heading_gap   = float(self.resolve("card-stacked-text-heading-gap")     or 4)

        # ── Geometry ──────────────────────────────────────────────────────

        avail_h = box.h - gap_top - gap_bottom
        slot_h  = avail_h / n
        div_length = box.w * div_length_pct

        # ── Render each block in its equal-height slot ────────────────────

        for i, block in enumerate(blocks):
            slot_y = box.y + gap_top + i * slot_h

            # Text area within the slot: leave gap_between/2 at top (except
            # first block) and gap_between/2 at bottom (except last block).
            text_y_start = slot_y + (gap_between / 2 if i > 0 else 0)

            heading_text = block["heading"]
            body_text    = block["body"]

            current_y = text_y_start

            # Heading
            if heading_text:
                heading_h = h_size + heading_gap
                box.add(
                    {
                        "type":        "text",
                        "x":           box.x,
                        "y":           current_y,
                        "w":           box.w,
                        "h":           heading_h,
                        "text":        heading_text,
                        "font_size":   h_size,
                        "font_color":  h_color,
                        "font_weight": h_weight,
                        "font_style":  h_style,
                        "alignment":   h_align,
                        "wrap":        True,
                    }
                )
                current_y += heading_h

            # Body text
            if body_text:
                # Available height: from current_y to slot bottom minus gap_between/2
                body_end_y = slot_y + slot_h - (gap_between / 2 if i < n - 1 else 0)
                body_h     = max(b_size, body_end_y - current_y)
                box.add(
                    {
                        "type":        "text",
                        "x":           box.x,
                        "y":           current_y,
                        "w":           box.w,
                        "h":           body_h,
                        "text":        body_text,
                        "font_size":   b_size,
                        "font_color":  b_color,
                        "font_weight": b_weight,
                        "font_style":  b_style,
                        "alignment":   b_align,
                        "wrap":        True,
                    }
                )

            # Divider between blocks (drawn at the slot boundary, not after last)
            if div_visible and i < n - 1:
                div_y = slot_y + slot_h  # fixed slot boundary — consistent across cards
                x1, x2 = self._divider_x(box.x, box.w, div_length, div_alignment)
                box.add(
                    {
                        "type":         "line",
                        "x1":           x1,
                        "y1":           div_y,
                        "x2":           x2,
                        "y2":           div_y,
                        "stroke":       div_color,
                        "stroke_width": div_width,
                    }
                )
