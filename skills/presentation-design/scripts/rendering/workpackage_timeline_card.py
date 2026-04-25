"""
WorkpackageTimelineCardRenderer — A horizontal project-phase timeline
with N workpackages above the bar, calendar-week markers along the bar,
and M cross-workpackages spanning the full width below the bar.

Layout (top to bottom):

    ┌────────────────────────────────────────────────────────────────┐
    │ WP1 head      WP2 head     WP3 head    WP4 head    WP5 head    │  ← top row
    │ WP1 body      WP2 body     WP3 body    WP4 body    WP5 body    │
    │                                                                │
    │   3 PT ▼     14 PT ▼     10 PT ▼     112 PT ▼     23 PT ▼ 8 PT │  ← markers
    │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━► KW34 ← gradient bar
    │   KW17        KW20         KW21        KW30        KW32        │  ← KW labels
    │                                                                │
    │ Cross-WP 1 title                                       18 PT   │  ← cross WPs
    │ Cross-WP 1 body                                                │
    │ Cross-WP 2 title                                        7 PT   │
    │ Cross-WP 2 body                                                │
    └────────────────────────────────────────────────────────────────┘

Content schema::

    type: workpackage-timeline-card
    content:
      workpackages:
        - { title: "Setup",                  body: "Setup of development project",                kw: "KW17", pt: 3   }
        - { title: "Functional Specification", body: "Definition of user stories…",               kw: "KW20", pt: 14  }
        - { title: "Technical Specification",  body: "Design and design decisions…",              kw: "KW21", pt: 10  }
        - { title: "Development",            body: "Development in 2 weeks sprints (5 sprints).", kw: "KW30", pt: 112 }
        - { title: "Test",                   body: "User acceptance test, bug fixing…",            kw: "KW32", pt: 23  }
        - { title: "Training & Rollout",     body: "Training of end users…",                       kw: "KW34", pt: 8, end: true }
      cross_workpackages:
        - { title: "Project Management in agile approach",
            body:  "Preparation and conduction of all relevant events in an agile project.",
            pt:    18 }
        - { title: "Technical Lead",
            body:  "Preparation and conduction of all relevant architecture artifacts.",
            pt:    7  }

Tokens (variant prefix ``card-workpackage-timeline-``):
    wp-heading-font-size/color/weight,
    wp-body-font-size/color,
    bar-height, bar-color-start, bar-color-end,
    marker-font-size/color/weight,
    kw-font-size/color/weight,
    end-arrow-size, end-arrow-color, end-kw-font-size/color,
    cross-heading-font-size/color/weight,
    cross-body-font-size/color,
    cross-pt-font-size/color/weight,
    cross-row-gap.
"""

from __future__ import annotations

from typing import Any

from scripts.models.deck import CardModel
from scripts.parsing.inline_markdown import text_and_runs
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _lerp_color(a: str, b: str, t: float) -> str:
    ar, ag, ab = _hex_to_rgb(a)
    br, bg, bb = _hex_to_rgb(b)
    r = int(ar + (br - ar) * t)
    g = int(ag + (bg - ag) * t)
    bl = int(ab + (bb - ab) * t)
    return f"#{r:02X}{g:02X}{bl:02X}"


class WorkpackageTimelineCardRenderer(BaseCardRenderer):
    """Renderer for ``workpackage-timeline-card`` type."""

    variant = "card--workpackage-timeline"

    def _tok(self, name: str, default: Any = None) -> Any:
        return self._resolve_tok("workpackage-timeline", name, default)

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        content = card.content if isinstance(card.content, dict) else {}
        wps  = list(content.get("workpackages") or [])
        xwps = list(content.get("cross_workpackages") or content.get("cross-workpackages") or [])
        if not wps:
            return

        # ── Tokens ────────────────────────────────────────────────────
        primary       = self.resolve("color-primary") or "#000099"
        accent        = self.resolve("color-accent")  or "#F58020"

        wp_head_size  = float(self._tok("wp-heading-font-size") or 12)
        wp_head_color = self._tok("wp-heading-font-color") or self.resolve("color-text-default") or "#222"
        wp_head_weight= self._tok("wp-heading-font-weight") or "bold"
        wp_body_size  = float(self._tok("wp-body-font-size") or 10)
        wp_body_color = self._tok("wp-body-font-color") or self.resolve("color-text-muted") or "#555"

        bar_h         = float(self._tok("bar-height") or 6)
        bar_c_start   = self._tok("bar-color-start") or primary
        bar_c_end     = self._tok("bar-color-end")   or accent

        mk_size       = float(self._tok("marker-font-size") or 11)
        mk_color      = self._tok("marker-font-color") or self.resolve("color-text-default") or "#222"
        mk_weight     = self._tok("marker-font-weight") or "bold"

        kw_size       = float(self._tok("kw-font-size") or 11)
        kw_color      = self._tok("kw-font-color") or self.resolve("color-text-default") or "#222"
        kw_weight     = self._tok("kw-font-weight") or "bold"

        end_arrow_sz  = float(self._tok("end-arrow-size") or 10)
        end_arrow_col = self._tok("end-arrow-color") or accent
        end_kw_size   = float(self._tok("end-kw-font-size") or 11)
        end_kw_color  = self._tok("end-kw-font-color") or self.resolve("color-text-default") or "#222"

        x_head_size   = float(self._tok("cross-heading-font-size") or 12)
        x_head_color  = self._tok("cross-heading-font-color") or self.resolve("color-text-default") or "#222"
        x_head_weight = self._tok("cross-heading-font-weight") or "bold"
        x_body_size   = float(self._tok("cross-body-font-size") or 10)
        x_body_color  = self._tok("cross-body-font-color") or self.resolve("color-text-muted") or "#555"
        x_pt_size     = float(self._tok("cross-pt-font-size") or 12)
        x_pt_color    = self._tok("cross-pt-font-color") or self.resolve("color-text-default") or "#222"
        x_pt_weight   = self._tok("cross-pt-font-weight") or "bold"
        x_row_gap     = float(self._tok("cross-row-gap") or 16)

        # ── Geometry ──────────────────────────────────────────────────
        # Reserve a right margin to fit the optional inline end-KW label
        right_inline_w = 60.0
        # Inset the left edge of the bar so the first WP description has
        # room to be right-anchored to its point-in-time (PIT) marker.
        left_inline_w = float(self._tok("first-wp-min-width") or 90.0)
        # Inter-column gap between WP description blocks (px)
        wp_block_gap = float(self._tok("wp-block-gap") or 8.0)
        # Vertical connector line tokens — visible hairline so the eye can
        # follow each WP description down to its point-in-time on the bar.
        connector_color = self._tok("connector-color") or self.resolve("color-text-muted") or "#888"
        connector_width = float(self._tok("connector-width") or 1.0)

        # Top row (workpackage descriptions) — fixed proportional height.
        # Made slightly taller so the card uses more vertical space (the
        # MHP master gives generous room for these descriptions).
        # Allow up to 3 heading lines so titles like "Training & Rollout"
        # don't overflow into the body text row.
        wp_top_h = wp_head_size * 3 + 8 + wp_body_size * 5 + 4

        # Marker row (PT label + diamond)
        mk_h = mk_size + 4 + 8  # text + diamond

        # KW label row
        kw_h = kw_size + 4

        # Cross-WP row (one per cross-WP)
        cross_row_h = x_head_size + 4 + x_body_size + 4

        # Vertical layout — generous breathing room so the timeline
        # uses more of the available card height (MHP-style spacious feel).
        cur_y = box.y
        # Top WP descriptions
        wp_top_y = cur_y
        cur_y += wp_top_h + 24  # extra gap before the marker row

        # Marker row
        mk_row_y = cur_y
        cur_y += mk_h

        # Bar
        bar_y = cur_y
        cur_y += bar_h + 12

        # KW label row
        kw_row_y = cur_y
        cur_y += kw_h + 44

        # Cross-workpackages start right below the KW row (with a gap)
        cross_y = cur_y

        # ── Workpackage column positions ──────────────────────────────
        # Last workpackage may be flagged `end: true` — its marker sits
        # at the very right edge of the bar (no slot column).
        end_wp = wps[-1] if (wps and bool(wps[-1].get("end"))) else None
        layout_wps = wps[:-1] if end_wp else wps[:]

        # Bar geometry — inset on the left to make room for the first
        # WP description block which is right-anchored to its PIT.
        bar_x1 = box.x + left_inline_w
        bar_x2 = box.x + box.w - right_inline_w
        bar_w  = bar_x2 - bar_x1

        # Distribute PITs evenly across the bar (including end-WP at far right)
        if end_wp:
            total_positions = len(layout_wps) + 1
            positions = [
                bar_x1 + (i * bar_w / max(1, total_positions - 1))
                for i in range(total_positions)
            ]
        else:
            positions = (
                [bar_x1 + (i * bar_w / max(1, len(layout_wps) - 1))
                 for i in range(len(layout_wps))]
                if len(layout_wps) > 1
                else [bar_x1 + bar_w / 2]
            )

        # ── 1) Top row: WP titles & bodies ────────────────────────────
        # Each description block is RIGHT-ANCHORED to its PIT so the user
        # can visually follow the text down to the marker on the bar.
        # A thin vertical connector line links the bottom of the block
        # to the diamond marker just above the bar.
        all_positions = positions[:]  # includes end-WP if present
        for i, wp in enumerate(wps):
            pit_x = all_positions[i]
            # Right edge of description block sits AT the PIT
            right_edge = pit_x
            # Left edge: previous PIT + gap, or box.x for the first block
            if i == 0:
                left_edge = box.x
            else:
                left_edge = all_positions[i - 1] + wp_block_gap
            cw = max(20.0, right_edge - left_edge - wp_block_gap)
            cx = right_edge - cw  # right-anchored

            # Title (bold) — right-aligned so the text "lands" on the PIT
            title_text = str(wp.get("title", "") or "")
            if title_text:
                box.add({
                    "type": "text",
                    "x": cx, "y": wp_top_y,
                    "w": cw, "h": wp_head_size * 3 + 6,
                    **text_and_runs(title_text),
                    "font_size": wp_head_size,
                    "font_color": wp_head_color,
                    "font_weight": wp_head_weight,
                    "alignment": "right",
                    "wrap": True,
                })
            # Body — right-aligned
            body_text = str(wp.get("body", "") or "")
            if body_text:
                box.add({
                    "type": "text",
                    "x": cx, "y": wp_top_y + wp_head_size * 3 + 8,
                    "w": cw, "h": wp_body_size * 5,
                    **text_and_runs(body_text),
                    "font_size": wp_body_size,
                    "font_color": wp_body_color,
                    "font_weight": "normal",
                    "alignment": "right",
                    "wrap": True,
                })

            # Thin vertical connector line: bottom of WP block → just
            # above the PT marker text. Stops short of the diamond so
            # marker text remains legible.
            line_top = wp_top_y + wp_top_h + 2
            line_bot = mk_row_y - 2
            if line_bot > line_top:
                box.add({
                    "type": "line",
                    "x1": pit_x, "y1": line_top,
                    "x2": pit_x, "y2": line_bot,
                    "stroke": str(connector_color),
                    "stroke_width": connector_width,
                })

        # ── 2) Gradient bar (approximated with N colour-interpolated slices) ──
        n_slices = 60
        slice_w = bar_w / n_slices
        for i in range(n_slices):
            t = i / max(1, n_slices - 1)
            col = _lerp_color(str(bar_c_start), str(bar_c_end), t)
            box.add({
                "type": "rect",
                "x": bar_x1 + i * slice_w,
                "y": bar_y,
                "w": slice_w + 0.5,  # tiny overlap to avoid hairline gaps
                "h": bar_h,
                "fill": col,
                "stroke": "none",
                "stroke_width": 0,
                "rx": 0,
            })

        # End-arrow (right-pointing triangle as a chevron with very small height,
        # or simulated via a small rect + text). We use an ellipse-marker plus
        # an inline KW label.
        # Solid right-pointing triangle: emit as a chevron with no body width.
        arrow_x = bar_x2
        arrow_y = bar_y + bar_h / 2 - end_arrow_sz / 2
        box.add({
            "type": "chevron",
            "x": arrow_x - end_arrow_sz,
            "y": arrow_y,
            "w": end_arrow_sz * 2,
            "h": end_arrow_sz,
            "fill": end_arrow_col,
            "stroke": "none",
            "stroke_width": 0,
        })
        # Inline KW label to the right of the arrow
        end_kw_label = str((end_wp or {}).get("kw") or "")
        if end_kw_label:
            box.add({
                "type": "text",
                "x": bar_x2 + end_arrow_sz + 4,
                "y": bar_y + bar_h / 2 - end_kw_size / 2,
                "w": right_inline_w,
                "h": end_kw_size + 4,
                **text_and_runs(end_kw_label),
                "font_size": end_kw_size,
                "font_color": end_kw_color,
                "font_weight": kw_weight,
                "alignment": "left",
                "vertical_align": "middle",
            })

        # ── 3) Markers (PT label + diamond) ABOVE the bar ─────────────
        # And KW labels BELOW the bar — for non-end WPs.
        for i, wp in enumerate(layout_wps):
            cx = positions[i]
            pt_val = wp.get("pt")
            if pt_val is not None:
                pt_label = f"{pt_val} PT"
                box.add({
                    "type": "text",
                    "x": cx - 30, "y": mk_row_y,
                    "w": 60, "h": mk_size + 4,
                    **text_and_runs(pt_label),
                    "font_size": mk_size,
                    "font_color": mk_color,
                    "font_weight": mk_weight,
                    "alignment": "center",
                })
            # Diamond/dot marker centred on the bar
            d_size = max(bar_h + 4, 9.0)
            box.add({
                "type": "ellipse",
                "x": cx - d_size / 2,
                "y": bar_y + bar_h / 2 - d_size / 2,
                "w": d_size, "h": d_size,
                "fill": str(self._tok("marker-color") or self.resolve("color-text-default") or "#222"),
                "stroke": "#FFFFFF",
                "stroke_width": 1.5,
            })
            # KW label below the bar
            kw_label = str(wp.get("kw") or "")
            if kw_label:
                box.add({
                    "type": "text",
                    "x": cx - 40, "y": kw_row_y,
                    "w": 80, "h": kw_size + 4,
                    **text_and_runs(kw_label),
                    "font_size": kw_size,
                    "font_color": kw_color,
                    "font_weight": kw_weight,
                    "alignment": "center",
                })

        # End-WP marker (PT label) above the arrow if present
        if end_wp:
            pt_val = end_wp.get("pt")
            if pt_val is not None:
                pt_label = f"{pt_val} PT"
                box.add({
                    "type": "text",
                    "x": bar_x2 - 30, "y": mk_row_y,
                    "w": 60, "h": mk_size + 4,
                    **text_and_runs(pt_label),
                    "font_size": mk_size,
                    "font_color": mk_color,
                    "font_weight": mk_weight,
                    "alignment": "center",
                })
            # dot marker at the bar end centred on the bar
            d_size = max(bar_h + 4, 9.0)
            box.add({
                "type": "ellipse",
                "x": bar_x2 - d_size / 2,
                "y": bar_y + bar_h / 2 - d_size / 2,
                "w": d_size, "h": d_size,
                "fill": str(self._tok("marker-color") or self.resolve("color-text-default") or "#222"),
                "stroke": "#FFFFFF",
                "stroke_width": 1.5,
            })

        # ── 4) Cross-workpackages (full-width rows below the bar) ─────
        for i, xwp in enumerate(xwps):
            ry = cross_y + i * (cross_row_h + x_row_gap)
            title = str(xwp.get("title", "") or "")
            body  = str(xwp.get("body",  "") or "")
            pt_val = xwp.get("pt")
            # Reserve right strip for PT label
            pt_strip_w = 80.0
            text_w = box.w - pt_strip_w - 8
            if title:
                box.add({
                    "type": "text",
                    "x": box.x, "y": ry,
                    "w": text_w, "h": x_head_size + 4,
                    **text_and_runs(title),
                    "font_size": x_head_size,
                    "font_color": x_head_color,
                    "font_weight": x_head_weight,
                    "alignment": "left",
                })
            if body:
                box.add({
                    "type": "text",
                    "x": box.x, "y": ry + x_head_size + 4,
                    "w": text_w, "h": x_body_size + 4,
                    **text_and_runs(body),
                    "font_size": x_body_size,
                    "font_color": x_body_color,
                    "font_weight": "normal",
                    "alignment": "left",
                })
            if pt_val is not None:
                box.add({
                    "type": "text",
                    "x": box.x + box.w - pt_strip_w,
                    "y": ry + (cross_row_h - x_pt_size) / 2,
                    "w": pt_strip_w,
                    "h": x_pt_size + 4,
                    **text_and_runs(f"{pt_val} PT"),
                    "font_size": x_pt_size,
                    "font_color": x_pt_color,
                    "font_weight": x_pt_weight,
                    "alignment": "right",
                })
