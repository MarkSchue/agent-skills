"""
TimelineCardRenderer — Renders a timeline with milestone markers.

Supports horizontal and vertical orientations. Each milestone (called a
"milestone" for clarity) has a marker on the spine (text, number, date, or
icon), an optional icon beside the heading, a heading, and body text.
An optional arrowhead at the spine end and a terminal goal block complete
the design.

content:
  orientation  : horizontal | vertical          (default: horizontal)
  alternate    : bool                           Alternate entries above/below in
                                                horizontal mode (default: true)
  arrow        : bool                           Show arrowhead (default: true)
  milestones:
    - marker   : str        Text or icon ligature in the spine dot
                            (e.g. "Q1", "CW12", "1", or "rocket_launch")
      heading  : str        Entry title (bold)
      body     : str        Description text
      icon:
        name   : str        Material icon ligature beside heading
        color  : "#hex"     Icon color override
      accent   : bool       Highlight this milestone with accent color
  goal:                     Optional terminal destination block
    heading    : str
    body       : str
    icon:
      name     : str
      color    : "#hex"
  caption      : str        Attribution line at bottom

Design tokens: .card--timeline in themes/base.css (section 15).
"""

from __future__ import annotations

import math
from typing import Any

from scripts.models.deck import CardModel
from scripts.rendering._utils import _is_icon_ligature
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


# ── Helpers ────────────────────────────────────────────────────────────────

def _is_icon_ligature(text: str) -> bool:
    """Return True when *text* looks like a Material icon ligature (lowercase + underscores only)."""
    return bool(text and text.replace("_", "").isalpha() and text == text.lower())


def _estimate_lines(text: str, max_chars: int) -> int:
    """Estimate how many wrapped lines *text* will occupy at *max_chars* per line."""
    if not text or max_chars <= 0:
        return 0
    words = text.split()
    lines, current = 1, 0
    for word in words:
        if current == 0:
            current = len(word)
        elif current + 1 + len(word) <= max_chars:
            current += 1 + len(word)
        else:
            lines += 1
            current = len(word)
    return lines


def _normalize_icon(raw: Any) -> dict:
    if isinstance(raw, dict):
        return {
            "name": str(raw.get("name", "")),
            "color": str(raw.get("color", "")),
        }
    return {"name": str(raw) if raw else "", "color": ""}


def _normalize_milestone(entry: Any) -> dict:
    if not isinstance(entry, dict):
        return {"marker": str(entry), "heading": "", "body": "", "icon": {"name": "", "color": ""}, "accent": False}
    return {
        "marker":  str(entry.get("marker", "")),
        "heading": str(entry.get("heading", "")),
        "body":    str(entry.get("body", "")),
        "icon":    _normalize_icon(entry.get("icon")),
        "accent":  bool(entry.get("accent", False)),
    }


# ── Renderer ────────────────────────────────────────────────────────────────

class TimelineCardRenderer(BaseCardRenderer):
    """Renderer for ``timeline-card`` type — primitive spine/milestone charts."""

    variant = "card--timeline"

    # ── Main entry ─────────────────────────────────────────────────────────

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        """Render the timeline in horizontal or vertical orientation."""
        content = card.content if isinstance(card.content, dict) else {}

        orientation = str(content.get("orientation", self._tok("orientation", "horizontal"))).lower()
        alternate   = _truthy(content.get("alternate", self._tok("alternate", True)))
        arrow       = _truthy(content.get("arrow",     self._tok("arrow",     True)))
        caption     = str(content.get("caption", ""))

        raw_milestones = content.get("milestones", [])
        milestones = [_normalize_milestone(m) for m in (raw_milestones or [])]

        goal_raw = content.get("goal")
        goal: dict | None = None
        if isinstance(goal_raw, dict) and goal_raw:
            goal = {
                "marker":  str(goal_raw.get("marker", "")),
                "heading": str(goal_raw.get("heading", "")),
                "body":    str(goal_raw.get("body", "")),
                "icon":    _normalize_icon(goal_raw.get("icon")),
                "accent":  True,
            }

        # Caption space
        cap_h = self._f("caption-font-size", 10) + 6 if caption else 0

        body_box = RenderBox(box.x, box.y, box.w, box.h - cap_h)

        if orientation == "vertical":
            self._render_vertical(body_box, milestones, goal, arrow)
        else:
            self._render_horizontal(body_box, milestones, goal, arrow, alternate)

        if caption:
            cap_y = box.y + box.h - cap_h
            box.add({"type": "text",
                     "x": box.x, "y": cap_y, "w": box.w, "h": cap_h,
                     "text": caption,
                     "font_size": self._f("caption-font-size", 10),
                     "font_color": self._tok("caption-font-color"),
                     "alignment": self._tok("caption-alignment", "center"),
                     "wrap": False})

        for el in body_box.elements:
            box.add(el)

    # ── Horizontal renderer ────────────────────────────────────────────────

    def _render_horizontal(  # noqa: C901
        self,
        box: RenderBox,
        milestones: list[dict],
        goal: dict | None,
        arrow: bool,
        alternate: bool,
    ) -> None:
        if not milestones and not goal:
            return

        # ── Token resolution ───────────────────────────────────────────
        spine_color  = self._tok("spine-color")
        spine_width  = self._f("spine-width", 2)
        marker_size  = self._f("marker-size", 28)
        marker_fill  = self._tok("marker-fill")
        marker_stroke = self._tok("marker-stroke")
        marker_fsz   = self._f("marker-font-size", 8)
        marker_fcol  = self._tok("marker-font-color")
        goal_fill    = self._tok("goal-marker-fill")
        accent_fill  = self._tok("accent-marker-fill")

        h_size  = self._f("heading-font-size", 12)
        h_color = self._tok("heading-font-color")
        h_weight = self._tok("heading-font-weight", "700")
        h_style  = self._tok("heading-font-style",  "normal")

        b_size  = self._f("body-font-size", 10)
        b_color = self._tok("body-font-color")
        b_weight = self._tok("body-font-weight", "400")
        b_style  = self._tok("body-font-style",  "normal")

        icon_size = self._f("item-icon-size", 14)
        icon_gap  = self._f("item-icon-gap",  4)
        icon_color = self._tok("item-icon-color")
        icon_ff    = self.resolve("icon-font-family") or "Material Symbols Outlined"
        icon_fw    = self._tok("item-icon-font-weight", "700")

        connector_len = self._f("connector-length", 10)
        arrow_size    = self._f("arrow-size", 10)

        # ── Geometry ───────────────────────────────────────────────────
        # Build combined item list (milestones + optional goal)
        items: list[dict] = list(milestones)
        if goal:
            items.append(goal)
        n = len(items)
        if n == 0:
            return

        # Reserve side padding so first/last markers are not clipped
        pad_x = marker_size / 2 + 4
        arrow_reserve = (arrow_size + 6) if arrow else 0
        usable_w = box.w - 2 * pad_x - arrow_reserve
        slot_w = usable_w / n

        # Spine y: with alternate the spine sits at mid-height
        # without alternate (all below) spine sits at ~30% from top
        if alternate:
            spine_y = box.y + box.h * 0.45
        else:
            spine_y = box.y + box.h * 0.28

        above_h = spine_y - box.y - marker_size / 2 - connector_len
        below_h = box.y + box.h - spine_y - marker_size / 2 - connector_len

        spine_x1 = box.x + pad_x
        spine_x2 = box.x + box.w - pad_x - arrow_reserve + (arrow_reserve if not arrow else 0)

        # Spine line
        box.add({"type": "line",
                 "x1": spine_x1, "y1": spine_y,
                 "x2": spine_x2 - (arrow_size if arrow else 0) + (0 if goal else 0),
                 "y2": spine_y,
                 "stroke": spine_color, "stroke_width": spine_width})

        # Arrow
        if arrow:
            tip_x = spine_x2
            ah = arrow_size * 0.55
            box.add({"type": "line",
                     "x1": tip_x - arrow_size, "y1": spine_y - ah,
                     "x2": tip_x, "y2": spine_y,
                     "stroke": spine_color, "stroke_width": spine_width})
            box.add({"type": "line",
                     "x1": tip_x - arrow_size, "y1": spine_y + ah,
                     "x2": tip_x, "y2": spine_y,
                     "stroke": spine_color, "stroke_width": spine_width})

        # Milestones
        for i, item in enumerate(items):
            is_goal = item.get("accent", False)
            mx = box.x + pad_x + (i + 0.5) * slot_w

            # Which side: below by default; above for odd items when alternating
            above = alternate and (i % 2 == 1)
            fill = goal_fill if is_goal else (accent_fill if item.get("accent") else marker_fill)

            # Marker circle
            self._draw_marker(box, mx, spine_y, item["marker"],
                               marker_size, fill, marker_stroke,
                               marker_fsz, marker_fcol, icon_ff, icon_fw)

            # Connector tick
            tick_y1 = spine_y - marker_size / 2 if above else spine_y + marker_size / 2
            tick_y2 = tick_y1 - connector_len if above else tick_y1 + connector_len
            box.add({"type": "line",
                     "x1": mx, "y1": tick_y1, "x2": mx, "y2": tick_y2,
                     "stroke": spine_color, "stroke_width": 1})

            # Content block
            cw = min(slot_w - 4, 120)
            cx_left = mx - cw / 2
            if above:
                content_bot = tick_y1 - connector_len
                self._draw_entry_above(box, cx_left, content_bot, cw, above_h,
                                       item, is_goal,
                                       h_size, h_color, h_weight, h_style,
                                       b_size, b_color, b_weight, b_style,
                                       icon_size, icon_gap, icon_color, icon_ff, icon_fw)
            else:
                content_top = tick_y1 + connector_len
                self._draw_entry_below(box, cx_left, content_top, cw, below_h,
                                       item, is_goal,
                                       h_size, h_color, h_weight, h_style,
                                       b_size, b_color, b_weight, b_style,
                                       icon_size, icon_gap, icon_color, icon_ff, icon_fw)

    # ── Vertical renderer ─────────────────────────────────────────────────

    def _render_vertical(  # noqa: C901
        self,
        box: RenderBox,
        milestones: list[dict],
        goal: dict | None,
        arrow: bool,
    ) -> None:
        if not milestones and not goal:
            return

        # ── Token resolution ───────────────────────────────────────────
        spine_color  = self._tok("spine-color")
        spine_width  = self._f("spine-width", 2)
        marker_size  = self._f("marker-size", 28)
        marker_fill  = self._tok("marker-fill")
        marker_stroke = self._tok("marker-stroke")
        marker_fsz   = self._f("marker-font-size", 8)
        marker_fcol  = self._tok("marker-font-color")
        goal_fill    = self._tok("goal-marker-fill")
        accent_fill  = self._tok("accent-marker-fill")

        h_size  = self._f("heading-font-size", 12)
        h_color = self._tok("heading-font-color")
        h_weight = self._tok("heading-font-weight", "700")
        h_style  = self._tok("heading-font-style",  "normal")

        b_size  = self._f("body-font-size", 10)
        b_color = self._tok("body-font-color")
        b_weight = self._tok("body-font-weight", "400")
        b_style  = self._tok("body-font-style",  "normal")

        icon_size = self._f("item-icon-size", 14)
        icon_gap  = self._f("item-icon-gap",  4)
        icon_color = self._tok("item-icon-color")
        icon_ff    = self.resolve("icon-font-family") or "Material Symbols Outlined"
        icon_fw    = self._tok("item-icon-font-weight", "700")

        connector_len = self._f("connector-length", 10)
        arrow_size    = self._f("arrow-size", 10)

        # ── Geometry ───────────────────────────────────────────────────
        items: list[dict] = list(milestones)
        if goal:
            items.append(goal)
        n = len(items)
        if n == 0:
            return

        pad_y = marker_size / 2 + 4
        arrow_reserve = (arrow_size + 8) if arrow else 0
        usable_h = box.h - 2 * pad_y - arrow_reserve

        # Spine x: left column
        spine_x = box.x + marker_size / 2 + 4
        content_x = spine_x + marker_size / 2 + connector_len + 6
        content_w = box.x + box.w - content_x - 4

        spine_y1 = box.y + pad_y
        spine_y2 = box.y + box.h - pad_y - arrow_reserve

        # Spine line
        box.add({"type": "line",
                 "x1": spine_x, "y1": spine_y1,
                 "x2": spine_x, "y2": spine_y2,
                 "stroke": spine_color, "stroke_width": spine_width})

        # Arrow
        if arrow:
            tip_y = spine_y2 + arrow_reserve
            aw = arrow_size * 0.55
            box.add({"type": "line",
                     "x1": spine_x - aw, "y1": tip_y - arrow_size,
                     "x2": spine_x, "y2": tip_y,
                     "stroke": spine_color, "stroke_width": spine_width})
            box.add({"type": "line",
                     "x1": spine_x + aw, "y1": tip_y - arrow_size,
                     "x2": spine_x, "y2": tip_y,
                     "stroke": spine_color, "stroke_width": spine_width})

        # Slot height per item
        slot_h = usable_h / n

        # One item height for content
        # Estimate heading + body height per slot
        for i, item in enumerate(items):
            is_goal = item.get("accent", False)
            my = box.y + pad_y + (i + 0.5) * slot_h

            fill = goal_fill if is_goal else (accent_fill if item.get("accent") else marker_fill)

            # Marker circle
            self._draw_marker(box, spine_x, my, item["marker"],
                               marker_size, fill, marker_stroke,
                               marker_fsz, marker_fcol, icon_ff, icon_fw)

            # Horizontal connector
            tick_x1 = spine_x + marker_size / 2
            tick_x2 = tick_x1 + connector_len
            box.add({"type": "line",
                     "x1": tick_x1, "y1": my, "x2": tick_x2, "y2": my,
                     "stroke": spine_color, "stroke_width": 1})

            # Content block: centered vertically on my
            avail_entry_h = slot_h - 6
            has_icon = bool(item["icon"].get("name"))
            has_heading = bool(item["heading"])
            has_body = bool(item["body"])

            heading_lh = h_size * 1.25
            body_lh    = b_size * 1.30
            body_chars  = max(1, int(content_w / (b_size * 0.48)))
            body_lines  = _estimate_lines(item["body"], body_chars) if has_body else 0
            heading_h   = heading_lh if has_heading else 0
            body_h      = body_lines * body_lh if has_body else 0
            total_h     = heading_h + (4 if has_heading and has_body else 0) + body_h
            content_y   = my - total_h / 2

            entry_icon_color = item["icon"].get("color") or (
                goal_fill if is_goal else icon_color
            )

            if has_heading:
                icon_name = item["icon"].get("name", "")
                if has_icon:
                    box.add({"type": "icon",
                             "name": icon_name,
                             "x": content_x, "y": content_y,
                             "w": icon_size, "h": icon_size,
                             "color": entry_icon_color,
                             "font_family": icon_ff,
                             "font_weight": icon_fw})
                    hx = content_x + icon_size + icon_gap
                    hw = content_w - icon_size - icon_gap
                else:
                    hx = content_x
                    hw = content_w
                box.add({"type": "text",
                         "x": hx, "y": content_y,
                         "w": hw, "h": heading_lh,
                         "text": item["heading"],
                         "font_size": h_size,
                         "font_color": goal_fill if is_goal else h_color,
                         "font_weight": h_weight,
                         "font_style": h_style,
                         "alignment": "left",
                         "vertical_align": "middle",
                         "wrap": False})

            if has_body:
                by = content_y + heading_h + (4 if has_heading else 0)
                bx = content_x + icon_size + icon_gap if has_icon else content_x
                bw = content_w - icon_size - icon_gap if has_icon else content_w
                box.add({"type": "text",
                         "x": bx, "y": by, "w": bw,
                         "h": min(body_h, avail_entry_h - heading_h - 4),
                         "text": item["body"],
                         "font_size": b_size,
                         "font_color": b_color,
                         "font_weight": b_weight,
                         "font_style": b_style,
                         "alignment": "left",
                         "vertical_align": "top",
                         "wrap": True})

    # ── Marker circle drawing ──────────────────────────────────────────────

    def _draw_marker(
        self, box: RenderBox,
        cx: float, cy: float,
        marker_text: str,
        size: float, fill: str, stroke: str,
        font_size: float, font_color: str,
        icon_ff: str, icon_fw: str,
    ) -> None:
        r = size / 2
        box.add({"type": "ellipse",
                 "x": cx - r, "y": cy - r, "w": size, "h": size,
                 "fill": fill, "stroke": stroke, "stroke_width": 1.5})

        if marker_text:
            if _is_icon_ligature(marker_text):
                box.add({"type": "icon",
                         "name": marker_text,
                         "x": cx - r, "y": cy - r, "w": size, "h": size,
                         "color": font_color,
                         "font_family": icon_ff,
                         "font_weight": icon_fw})
            else:
                # Scale font size to fit longer text
                fsz = font_size if len(marker_text) <= 4 else max(6.0, font_size * 0.8)
                box.add({"type": "text",
                         "x": cx - r, "y": cy - r, "w": size, "h": size,
                         "text": marker_text,
                         "font_size": fsz,
                         "font_color": font_color,
                         "font_weight": "700",
                         "alignment": "center",
                         "vertical_align": "middle",
                         "wrap": False})

    # ── Content block helpers ──────────────────────────────────────────────

    def _draw_entry_below(
        self, box: RenderBox,
        cx: float, top: float, cw: float, avail_h: float,
        item: dict, is_goal: bool,
        h_size: float, h_color: str, h_weight: str, h_style: str,
        b_size: float, b_color: str, b_weight: str, b_style: str,
        icon_size: float, icon_gap: float, icon_color: str,
        icon_ff: str, icon_fw: str,
    ) -> None:
        self._draw_entry_content(box, cx, top, cw, avail_h, item, is_goal, "below",
                                 h_size, h_color, h_weight, h_style,
                                 b_size, b_color, b_weight, b_style,
                                 icon_size, icon_gap, icon_color, icon_ff, icon_fw)

    def _draw_entry_above(
        self, box: RenderBox,
        cx: float, bottom: float, cw: float, avail_h: float,
        item: dict, is_goal: bool,
        h_size: float, h_color: str, h_weight: str, h_style: str,
        b_size: float, b_color: str, b_weight: str, b_style: str,
        icon_size: float, icon_gap: float, icon_color: str,
        icon_ff: str, icon_fw: str,
    ) -> None:
        # For above-spine entries, anchor from the bottom of the available area
        has_icon    = bool(item["icon"].get("name"))
        has_heading = bool(item["heading"])
        has_body    = bool(item["body"])
        heading_lh  = h_size * 1.25
        body_lh     = b_size * 1.30
        body_chars  = max(1, int(cw / (b_size * 0.48)))
        body_lines  = _estimate_lines(item["body"], body_chars) if has_body else 0
        total_h     = (heading_lh if has_heading else 0) + (4 if has_heading and has_body else 0) + body_lines * body_lh
        top = bottom - total_h
        self._draw_entry_content(box, cx, top, cw, avail_h, item, is_goal, "above",
                                 h_size, h_color, h_weight, h_style,
                                 b_size, b_color, b_weight, b_style,
                                 icon_size, icon_gap, icon_color, icon_ff, icon_fw)

    def _draw_entry_content(  # noqa: C901
        self, box: RenderBox,
        cx: float, top: float, cw: float, avail_h: float,
        item: dict, is_goal: bool, side: str,
        h_size: float, h_color: str, h_weight: str, h_style: str,
        b_size: float, b_color: str, b_weight: str, b_style: str,
        icon_size: float, icon_gap: float, icon_color: str,
        icon_ff: str, icon_fw: str,
    ) -> None:
        goal_fill = self._tok("goal-marker-fill")
        has_icon    = bool(item["icon"].get("name"))
        has_heading = bool(item["heading"])
        has_body    = bool(item["body"])
        heading_lh  = h_size * 1.25
        body_lh     = b_size * 1.30

        entry_icon_color = item["icon"].get("color") or (goal_fill if is_goal else icon_color)

        y_cursor = top
        if has_heading:
            ix = cx
            iw = cw
            if has_icon:
                box.add({"type": "icon",
                         "name": item["icon"]["name"],
                         "x": cx, "y": y_cursor,
                         "w": icon_size, "h": heading_lh,
                         "color": entry_icon_color,
                         "font_family": icon_ff,
                         "font_weight": icon_fw})
                ix = cx + icon_size + icon_gap
                iw = cw - icon_size - icon_gap
            box.add({"type": "text",
                     "x": ix, "y": y_cursor, "w": iw, "h": heading_lh,
                     "text": item["heading"],
                     "font_size": h_size,
                     "font_color": goal_fill if is_goal else h_color,
                     "font_weight": h_weight,
                     "font_style": h_style,
                     "alignment": "center",
                     "vertical_align": "middle",
                     "wrap": False})
            y_cursor += heading_lh + 2

        if has_body:
            body_chars  = max(1, int(cw / (b_size * 0.48)))
            body_lines  = _estimate_lines(item["body"], body_chars)
            body_h      = body_lines * body_lh
            bx = cx + icon_size + icon_gap if has_icon and not has_heading else cx
            bw = cw - icon_size - icon_gap if has_icon and not has_heading else cw
            remaining = top + avail_h - y_cursor
            box.add({"type": "text",
                     "x": bx, "y": y_cursor, "w": bw, "h": min(body_h, max(0, remaining)),
                     "text": item["body"],
                     "font_size": b_size,
                     "font_color": b_color,
                     "font_weight": b_weight,
                     "font_style": b_style,
                     "alignment": "center",
                     "vertical_align": "top",
                     "wrap": True})


# ── Utility ───────────────────────────────────────────────────────────────

def _truthy(v: Any) -> bool:
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.lower() in ("true", "1", "yes")
    return bool(v)
