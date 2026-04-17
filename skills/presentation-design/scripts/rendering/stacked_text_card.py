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
from scripts.parsing.inline_markdown import text_and_runs, strip_inline
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
        """Render equal-height block slots with heading, body, dividers, and optional key takeaway."""
        content = card.content if isinstance(card.content, dict) else {}
        raw_blocks = content.get("blocks", [])
        kt_text = content.get("key_takeaway", "") or ""

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
                        "bullets": list(entry.get("bullets") or []),
                    }
                )
            else:
                blocks.append({"heading": "", "body": str(entry), "bullets": []})

        n = max(2, min(4, len(blocks)))  # clamp to 2–4
        blocks = blocks[:n]

        # ── Token resolution ──────────────────────────────────────────────

        # Heading (h2-style)
        h_size   = float(self._resolve_tok("stacked-text", "heading-font-size",   14))
        h_color  = self._resolve_tok("stacked-text", "heading-font-color")
        h_weight = str(self._resolve_tok("stacked-text", "heading-font-weight",    "700"))
        h_style  = self._resolve_tok("stacked-text", "heading-font-style",         "normal")
        h_align  = self._resolve_tok("stacked-text", "heading-alignment",          "left")

        # Body (text-body style)
        b_size   = float(self._resolve_tok("stacked-text", "body-font-size",       12))
        b_color  = self._resolve_tok("stacked-text", "body-font-color")
        b_weight = str(self._resolve_tok("stacked-text", "body-font-weight",       "400"))
        b_style  = self._resolve_tok("stacked-text", "body-font-style",            "normal")
        b_align  = self._resolve_tok("stacked-text", "body-alignment",             "left")

        # Divider between blocks
        div_visible_raw = self.resolve("card-divider-visible")
        div_visible    = div_visible_raw in (True, "true", "True")
        div_color      = self.resolve("card-divider-color")
        _div_width_raw = self.resolve("card-divider-width")
        div_width      = float(_div_width_raw if _div_width_raw is not None and _div_width_raw != "" else 1)
        if div_width == 0:
            div_visible = False
        div_length_pct = float(self._resolve_tok("stacked-text", "divider-length-pct", 50)) / 100
        div_alignment  = self._resolve_tok("stacked-text", "divider-alignment", "left")

        # Vertical gaps — falls back to --card-gap-* base tokens
        gap_top       = float(self._resolve_tok("stacked-text", "gap-top",       0))
        gap_bottom    = float(self._resolve_tok("stacked-text", "gap-bottom",    0))
        gap_between   = float(self._resolve_tok("stacked-text", "gap-between",   8))
        heading_gap   = float(self._resolve_tok("stacked-text", "heading-gap",   8))
        vertical_align = self._resolve_tok("stacked-text", "block-vertical-alignment", "top")

        # Key takeaway
        kt_size       = float(self._resolve_tok("stacked-text", "key-takeaway-font-size",   b_size))
        kt_color      = self._resolve_tok("stacked-text", "key-takeaway-font-color")         or h_color
        kt_weight     = str(self._resolve_tok("stacked-text", "key-takeaway-font-weight",   "700"))
        kt_style      = self._resolve_tok("stacked-text", "key-takeaway-font-style",         "normal")
        kt_align      = self._resolve_tok("stacked-text", "key-takeaway-alignment")          or b_align
        kt_margin_top = float(self._resolve_tok("stacked-text", "key-takeaway-margin-top",  8))
        kt_lh_ratio  = float(self._resolve_tok("stacked-text", "body-line-height",          1.5))

        # Reserve vertical space for key takeaway — use 2 lines × line-height so
        # renderers that clip at the cell boundary (e.g. draw.io) don't cut off
        # the second line of a wrapped key-takeaway.  Use at least 1.5× so there
        # is a small rendering buffer even when the theme sets a tighter value.
        kt_height = (kt_size * 2 * max(kt_lh_ratio, 1.5) + kt_margin_top) if kt_text else 0

        # ── Geometry ──────────────────────────────────────────────────────

        avail_h = box.h - gap_top - gap_bottom - kt_height
        slot_h = avail_h / n
        block_pad = gap_between / 2  # minimum space from slot boundary (divider) to content
        div_length = box.w * div_length_pct

        # ── Render each block in its equal-height slot ────────────────────

        for i, block in enumerate(blocks):
            slot_start = box.y + gap_top + i * slot_h
            slot_end = slot_start + slot_h

            heading_text = block["heading"]
            body_text    = block["body"]

            heading_line_height = h_size * float(self._resolve_tok("stacked-text", "heading-line-height", 1.25))
            body_line_height = b_size * float(self._resolve_tok("stacked-text", "body-line-height", 1.25))
            heading_chars = max(1, int(box.w / (h_size * 0.6)))
            body_chars = max(1, int(box.w / (b_size * 0.6)))

            heading_h = 0
            heading_text_h = 0
            if heading_text:
                heading_lines = max(1, len(strip_inline(heading_text)) // heading_chars + 1)
                heading_text_h = heading_lines * heading_line_height
                heading_h = heading_text_h

            bullets = block.get("bullets") or []
            body_h = 0
            if bullets:
                body_h = self._bullet_list_height(bullets, b_size, body_line_height, box.w)
            elif body_text:
                body_lines = max(1, len(strip_inline(body_text)) // body_chars + 1)
                body_h = max(b_size, body_lines * body_line_height)

            has_body = bool(bullets or body_text)
            content_height = heading_text_h + (heading_gap if heading_text and has_body else 0) + body_h

            if vertical_align == "middle":
                # Step 4: pure centre — gap above == gap below, overflow is symmetric
                margin = (slot_h - content_height) / 2
                current_y = slot_start + margin
            elif vertical_align == "bottom":
                current_y = slot_end - block_pad - content_height
            else:  # top
                current_y = slot_start + block_pad

            if heading_text:
                box.add(
                    {
                        "type":        "text",
                        "x":           box.x,
                        "y":           current_y,
                        "w":           box.w,
                        "h":           heading_text_h,
                        **text_and_runs(heading_text),
                        "font_size":   h_size,
                        "line_height": heading_line_height,
                        "font_color":  h_color,
                        "font_weight": h_weight,
                        "font_style":  h_style,
                        "alignment":   h_align,
                        "vertical_align": "bottom",
                        "wrap":        True,
                    }
                )
                current_y += heading_text_h
                if has_body:
                    current_y += heading_gap

            if bullets:
                self._emit_bullet_list(
                    box, bullets, box.x, current_y, box.w, body_h,
                    b_size, b_color, b_weight, b_align, body_line_height,
                )
            elif body_text:
                box.add(
                    {
                        "type":        "text",
                        "x":           box.x,
                        "y":           current_y,
                        "w":           box.w,
                        "h":           body_h,
                        **text_and_runs(body_text),
                        "font_size":   b_size,
                        "line_height": body_line_height,
                        "font_color":  b_color,
                        "font_weight": b_weight,
                        "font_style":  b_style,
                        "alignment":   b_align,
                        "wrap":        True,
                    }
                )

            # Divider between blocks (drawn at the slot boundary, not after last)
            if div_visible and i < n - 1:
                div_y = slot_end  # fixed slot boundary — consistent across cards
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

        # ── Key takeaway (optional, below all blocks) ──────────────────────
        if kt_text:
            kt_y = box.y + gap_top + avail_h + kt_margin_top
            box.add(
                {
                    "type":        "text",
                    "x":           box.x,
                    "y":           kt_y,
                    "w":           box.w,
                    "h":           kt_height - kt_margin_top,
                    "text":        ">> " + kt_text,
                    "font_size":   kt_size,
                    "font_color":  kt_color,
                    "font_weight": kt_weight,
                    "font_style":  kt_style,
                    "alignment":   kt_align,
                    "line_height": kt_size * kt_lh_ratio,
                    "wrap":        True,
                }
            )
