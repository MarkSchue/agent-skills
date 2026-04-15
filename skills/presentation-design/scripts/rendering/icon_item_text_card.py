"""
IconItemTextCardRenderer — Renders icon_item_text cards with 1–5 item rows.

Each item includes an optional icon/label on the left or right, plus a heading
and body text. The card inherits all standard card chrome, header, footer, and
icon features from BaseCardRenderer.
"""

from __future__ import annotations

from scripts.models.deck import CardModel
from scripts.parsing.inline_markdown import text_and_runs, strip_inline
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class IconItemTextCardRenderer(BaseCardRenderer):
    """Renderer for ``icon_item_text`` type."""

    variant = "card--icon-item-text"

    @staticmethod
    def _normalize_block(entry: object) -> dict[str, object]:
        if isinstance(entry, dict):
            icon = entry.get("icon", {})
            if isinstance(icon, dict):
                icon_dict = {
                    "name": icon.get("name", ""),
                    "text": icon.get("text", ""),
                    "position": icon.get("position", "left"),
                    "color": icon.get("color", ""),
                    "size": icon.get("size", ""),
                    "font_family": icon.get("font_family", ""),
                    "visible": icon.get("visible", True),
                }
            else:
                icon_dict = {
                    "name": "",
                    "text": str(icon) if icon is not None else "",
                    "position": entry.get("icon_position", "left"),
                    "color": "",
                    "size": "",
                    "font_family": "",
                    "visible": bool(icon),
                }
            return {
                "heading": str(entry.get("heading", "")),
                "body": str(entry.get("body", "")),
                "icon": icon_dict,
                "icon_position": str(entry.get("icon_position", icon_dict["position"])) or "left",
            }
        return {
            "heading": "",
            "body": str(entry),
            "icon": {
                "name": "",
                "text": str(entry),
                "position": "left",
                "color": "",
                "size": "",
                "font_family": "",
                "visible": False,
            },
            "icon_position": "left",
        }

    @staticmethod
    def _is_icon_ligature(text: str) -> bool:
        return bool(text and text.islower() and " " not in text)

    @staticmethod
    def _estimate_line_count(text: str, max_chars: int) -> int:
        if max_chars <= 0:
            return max(1, len(text))
        words = text.split()
        if not words:
            return 1
        line_count = 1
        current_len = 0
        for word in words:
            if current_len == 0:
                current_len = len(word)
            elif current_len + 1 + len(word) <= max_chars:
                current_len += 1 + len(word)
            else:
                line_count += 1
                current_len = len(word)
        return line_count

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        content = card.content if isinstance(card.content, dict) else {}
        raw_blocks = content.get("blocks", [])

        if not raw_blocks:
            return

        blocks = [self._normalize_block(entry) for entry in raw_blocks]
        n = max(1, min(5, len(blocks)))
        blocks = blocks[:n]

        # Heading style
        h_size = float(self._resolve_tok("icon-item-text", "heading-font-size",  14))
        h_color = self._resolve_tok("icon-item-text", "heading-font-color")
        h_weight = str(self._resolve_tok("icon-item-text", "heading-font-weight", "700"))
        h_style = self._resolve_tok("icon-item-text", "heading-font-style",        "normal")
        h_align = self._resolve_tok("icon-item-text", "heading-alignment",         "left")

        # Body style
        b_size = float(self._resolve_tok("icon-item-text", "body-font-size",      12))
        b_color = self._resolve_tok("icon-item-text", "body-font-color")
        b_weight = str(self._resolve_tok("icon-item-text", "body-font-weight",    "400"))
        b_style = self._resolve_tok("icon-item-text", "body-font-style",           "normal")
        b_align = self._resolve_tok("icon-item-text", "body-alignment",            "left")

        # Icon style — resolved from --card-item-icon-* base tokens.
        # Override at class level in CSS (.card--icon-item-text { --card-item-icon-color: ...; })
        # or at instance level via style_overrides: card_item_icon_color: ...
        icon_size = float(self.resolve("card-item-icon-size") or 20)
        icon_gap = float(self.resolve("card-item-icon-gap") or 8)
        icon_color = self.resolve("card-item-icon-color")
        icon_font_family = self.resolve("icon-font-family") or "Material Symbols Outlined"
        icon_weight = str(self.resolve("card-item-icon-font-weight") or "700")

        # Divider style
        div_visible_raw = self.resolve("card-divider-visible")
        div_visible = div_visible_raw in (True, "true", "True")
        div_color = self.resolve("card-divider-color")
        div_width = float(self.resolve("card-divider-width") or 1)
        div_length_pct = float(self._resolve_tok("icon-item-text", "divider-length-pct", 100)) / 100
        div_alignment = self._resolve_tok("icon-item-text", "divider-alignment", "left")

        # Vertical spacing — falls back to --card-gap-* base tokens
        gap_top = float(self._resolve_tok("icon-item-text", "gap-top", 0))
        gap_bottom = float(self._resolve_tok("icon-item-text", "gap-bottom", 0))
        gap_between = float(self._resolve_tok("icon-item-text", "gap-between", 8))
        heading_gap = float(self._resolve_tok("icon-item-text", "heading-gap", 8))
        vertical_align = self._resolve_tok("icon-item-text", "block-vertical-alignment", "top")

        avail_h = box.h - gap_top - gap_bottom
        slot_h = avail_h / n
        block_pad = gap_between / 2  # minimum space from slot boundary (divider) to content

        for i, block in enumerate(blocks):
            slot_start = box.y + gap_top + i * slot_h
            slot_end = slot_start + slot_h

            icon_data = block["icon"]
            icon_position = block["icon_position"] if block["icon_position"] in ("left", "right") else "left"
            has_icon = bool(icon_data.get("visible") and (icon_data.get("name") or icon_data.get("text")))

            if has_icon:
                text_x = box.x + icon_size + icon_gap if icon_position == "left" else box.x
                icon_x = box.x if icon_position == "left" else box.x + box.w - icon_size
                text_w = box.w - icon_size - icon_gap
            else:
                text_x = box.x
                icon_x = box.x
                text_w = box.w

            heading_text = block["heading"]
            body_text = block["body"]

            heading_line_height = h_size * float(self._resolve_tok("icon-item-text", "heading-line-height", 1.3))
            body_line_height = b_size * float(self._resolve_tok("icon-item-text", "body-line-height", 1.3))
            heading_chars = max(1, int(text_w / (h_size * 0.48)))
            body_chars = max(1, int(text_w / (b_size * 0.48)))

            heading_h = 0
            heading_text_h = 0
            if heading_text:
                heading_lines = self._estimate_line_count(strip_inline(heading_text), heading_chars)
                heading_text_h = heading_lines * heading_line_height
                heading_h = heading_text_h

            body_h = 0
            if body_text:
                body_lines = self._estimate_line_count(strip_inline(body_text), body_chars)
                body_h = max(b_size, body_lines * body_line_height)

            content_height = heading_text_h + (heading_gap if heading_text and body_text else 0) + body_h

            if vertical_align == "middle":
                # Step 4: pure centre — gap above == gap below, overflow is symmetric
                margin = max(0, (slot_h - content_height) / 2)
                content_top = slot_start + margin
            elif vertical_align == "bottom":
                content_top = slot_end - block_pad - content_height
            else:  # top
                content_top = slot_start + block_pad
            current_y = content_top

            if heading_text:
                box.add(
                    {
                        "type": "text",
                        "x": text_x,
                        "y": current_y,
                        "w": text_w,
                        "h": heading_text_h,
                        **text_and_runs(heading_text),
                        "font_size": h_size,
                        "line_height": heading_line_height,
                        "font_color": h_color,
                        "font_weight": h_weight,
                        "font_style": h_style,
                        "alignment": h_align,
                        "vertical_align": "bottom",
                        "wrap": True,
                    }
                )
                current_y += heading_text_h
                if body_text:
                    current_y += heading_gap

            if body_text:
                box.add(
                    {
                        "type": "text",
                        "x": text_x,
                        "y": current_y,
                        "w": text_w,
                        "h": body_h,
                        **text_and_runs(body_text),
                        "font_size": b_size,
                        "line_height": body_line_height,
                        "font_color": b_color,
                        "font_weight": b_weight,
                        "font_style": b_style,
                        "alignment": b_align,
                        "wrap": True,
                    }
                )

            if has_icon:
                # Align icon vertically with the heading line (top-aligned, or centred for tall headings)
                icon_y = content_top + max(0.0, (heading_text_h - icon_size) / 2.0)
                icon_name = str(icon_data.get("name") or "").strip()
                icon_text = str(icon_data.get("text") or "").strip()

                if icon_name:
                    box.add(
                        {
                            "type": "icon",
                            "x": icon_x,
                            "y": icon_y,
                            "w": icon_size,
                            "h": icon_size,
                            "name": icon_name,
                            "font_family": icon_data.get("font_family") or icon_font_family,
                            "font_size": icon_size,
                            "color": icon_data.get("color") or icon_color,
                        }
                    )
                elif icon_text:
                    box.add(
                        {
                            "type": "text",
                            "x": icon_x,
                            "y": icon_y,
                            "w": icon_size,
                            "h": icon_size,
                            "text": icon_text,
                            "font_size": icon_size,
                            "font_color": icon_data.get("color") or icon_color,
                            "font_weight": icon_weight,
                            "alignment": "center",
                            "wrap": False,
                            "vertical_align": "middle",
                        }
                    )

            if div_visible and i < n - 1:
                div_y = slot_end
                x1, x2 = self._divider_x(box.x, box.w, box.w * div_length_pct, div_alignment)
                box.add(
                    {
                        "type": "line",
                        "x1": x1,
                        "y1": div_y,
                        "x2": x2,
                        "y2": div_y,
                        "stroke": div_color,
                        "stroke_width": div_width,
                    }
                )

    @staticmethod
    def _divider_x(box_x: float, box_w: float, length_px: float, alignment: str) -> tuple[float, float]:
        if alignment == "center":
            cx = box_x + box_w / 2
            return cx - length_px / 2, cx + length_px / 2
        if alignment == "right":
            return box_x + box_w - length_px, box_x + box_w
        return box_x, box_x + length_px
