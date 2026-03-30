"""TimelineCard — card-framed horizontal or vertical milestone timeline.

Follows the full card contract (ctx.card_pad_px, ctx.card_header_h, etc.)
so it aligns perfectly with neighbouring cards in any grid template.

Horizontal layout (default)
───────────────────────────
  • Optional header (title + divider) at the top of the card.
  • Axis line drawn at a configurable vertical position within the remaining
    content area (default: centred slightly above the midpoint).
  • Above axis: date label (primary color by default).
  • On axis: badge circle (number / text / icon / plain dot).
  • Below axis: event label (bold) + description.
  • Optional result/target at the far right with an arrowhead.

Vertical layout
───────────────
  • Axis line runs vertically at ~20 % of the inner width.
  • Each row: badge on axis · date to the left · label+desc to the right.

Per-card overrides (all optional — priority: prop → CSS token → default)
─────────────────────────────────────────────────────────────────────────
  orientation        : "horizontal" | "vertical"      (default: horizontal)
  dot-radius         : int px — base dot radius        (default: ctx-calculated)
  line-color         : color token or hex              (default: border-subtle)
  date-color         : color token or hex              (default: primary)
  label-color        : color token or hex              (default: on-surface)
  desc-color         : color token or hex              (default: on-surface-variant)
  axis-position      : 0..1 float (horizontal only)   (default: 0.45)
  dot-badge-type     : "none" | "number" | "text" | "icon"  (default: "none")
  dot-badge-color    : fill color for badge circles    (default: primary)
  dot-badge-text-color: text/icon color inside badge   (default: on-primary)
  show-header        : bool                            (cards standard)
  show-header-line   : bool                            (cards standard)
  result             : {label, description, color}     optional target node at end

Per-event fields
────────────────
  date        : string  — date / period shown above axis (horizontal) or left (vertical)
  label       : string  — bold event name shown below axis / right of axis
  description : string  — supporting detail below label
  status      : string  — success | warning | error | neutral | primary
  badge       : string  — custom text/icon override inside the circle (overrides auto number)
"""
from __future__ import annotations


class TimelineCard:
    """Render a card-framed timeline with horizontal or vertical orientation."""

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _resolve_color(self, ctx, raw: str, fallback_token: str) -> str:
        raw = (raw or "").strip()
        if not raw:
            return ctx.color(fallback_token)
        if raw.startswith("#"):
            return raw
        return ctx.color(raw)

    def _dot_radius(self, ctx, w: int, h: int, props: dict, has_badge: bool) -> int:
        raw = props.get("dot-radius", "")
        if raw:
            try:
                return max(4, int(raw))
            except (ValueError, TypeError):
                pass
        base = max(7, min(13, int(min(w, h) * 0.012)))
        # Badge circles need more room for text
        return max(16, int(base * 2.2)) if has_badge else base

    def _badge_type(self, props: dict) -> str:
        return str(props.get("dot-badge-type", "none")).strip().lower()

    def _draw_dot(self, ctx, mx, my, dot_r, dot_c, badge_type, badge_text,
                  badge_bg, badge_text_color, props) -> None:
        """Draw a dot or badge circle at (mx, my) centre."""
        if badge_type == "none":
            ctx.ellipse(mx - dot_r, my - dot_r,
                        dot_r * 2, dot_r * 2,
                        fill=dot_c,
                        stroke=ctx.color("surface"))
        else:
            # Filled badge circle
            ctx.ellipse(mx - dot_r, my - dot_r,
                        dot_r * 2, dot_r * 2,
                        fill=badge_bg,
                        stroke=ctx.color("surface"))
            if badge_type == "icon":
                ctx.draw_icon(mx - dot_r, my - dot_r,
                              dot_r * 2, dot_r * 2,
                              badge_text, color=badge_text_color)
            else:
                sz = max(9, min(dot_r, int(dot_r * 0.9)))
                ctx.text(mx - dot_r, my - dot_r,
                         dot_r * 2, dot_r * 2,
                         badge_text,
                         size=sz, bold=True,
                         color=badge_text_color,
                         align="center", valign="middle",
                         inner_margin=0)

    # ── Arrow helpers ─────────────────────────────────────────────────────────

    def _draw_arrowhead_h(self, ctx, tip_x, tip_y, size, color) -> None:
        """Draw a right-pointing filled triangle as arrowhead at (tip_x, tip_y)."""
        try:
            ctx.polygon(
                [(tip_x, tip_y),
                 (tip_x - size, tip_y - size // 2),
                 (tip_x - size, tip_y + size // 2)],
                fill=color, stroke=None,
            )
        except Exception:
            # Fallback if polygon not supported: small rect
            ctx.rect(tip_x - size, tip_y - size // 3,
                     size, size * 2 // 3,
                     fill=color, stroke=None)

    def _draw_arrowhead_v(self, ctx, tip_x, tip_y, size, color) -> None:
        """Draw a downward-pointing filled triangle."""
        try:
            ctx.polygon(
                [(tip_x, tip_y),
                 (tip_x - size // 2, tip_y - size),
                 (tip_x + size // 2, tip_y - size)],
                fill=color, stroke=None,
            )
        except Exception:
            ctx.rect(tip_x - size // 3, tip_y - size,
                     size * 2 // 3, size,
                     fill=color, stroke=None)

    # ── Main render ───────────────────────────────────────────────────────────

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:

        events = props.get("events", []) or []
        if not events:
            return

        orientation  = str(props.get("orientation", "horizontal")).strip().lower()
        badge_type   = self._badge_type(props)
        has_badge    = badge_type != "none"

        # ── Card contract ─────────────────────────────────────────────────
        pad     = ctx.card_pad_px(w, h, props)
        inner_w = w - pad * 2
        title   = str(props.get("title", ""))

        show_header      = bool(title) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)

        # ── Token resolution ──────────────────────────────────────────────
        title_color   = ctx.card_title_color(props, default_token="text-default")
        header_align  = ctx.card_header_align(props, default="left")
        divider_color = ctx.card_line_color("header", ctx.color("line-default"), props)
        bg_color      = ctx.card_bg_color(props, "bg-card")

        line_color        = self._resolve_color(ctx, str(props.get("line-color",  "")), "border-subtle")
        date_color        = self._resolve_color(ctx, str(props.get("date-color",  "")), "primary")
        label_color       = self._resolve_color(ctx, str(props.get("label-color", "")), "on-surface")
        desc_color        = self._resolve_color(ctx, str(props.get("desc-color",  "")), "on-surface-variant")
        badge_bg          = self._resolve_color(ctx, str(props.get("dot-badge-color", "")), "primary")
        badge_text_color  = self._resolve_color(ctx, str(props.get("dot-badge-text-color", "")), "on-primary")
        dot_r             = self._dot_radius(ctx, w, h, props, has_badge)

        GAP_S = ctx.spacing("s")
        GAP_M = ctx.spacing("m")

        # ── Card frame ────────────────────────────────────────────────────
        ctx.rect(x, y, w, h,
                 fill=bg_color,
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        # ── Header ────────────────────────────────────────────────────────
        header_h   = ctx.card_header_h(w, h, props)
        header_gap = ctx.card_header_gap(h, props)
        oy = y + pad

        if show_header:
            title_sz = ctx.card_header_font_size(title, inner_w, h, props)
            ctx.text(x + pad, oy, inner_w, header_h, title,
                     size=title_sz, bold=True,
                     color=title_color,
                     align=header_align, valign="middle")
            oy += header_h + header_gap

        if show_header_line:
            lx, lw = ctx.card_divider_span("header", x + pad, inner_w, props)
            ctx.divider(lx, oy, lw, color=divider_color)
            oy += GAP_M

        # ── Content area ──────────────────────────────────────────────────
        content_y = oy
        content_h = y + h - pad - oy
        content_x = x + pad

        # Result/target node (shared by both orientations)
        result = props.get("result")
        if isinstance(result, str):
            result = {"label": result}

        args = dict(
            ctx=ctx, events=events,
            cx=content_x, cy=content_y, cw=inner_w, ch=content_h,
            dot_r=dot_r, line_color=line_color, date_color=date_color,
            label_color=label_color, desc_color=desc_color,
            GAP_S=GAP_S, GAP_M=GAP_M,
            badge_type=badge_type, badge_bg=badge_bg,
            badge_text_color=badge_text_color,
            result=result, props=props,
        )
        if orientation == "vertical":
            self._render_vertical(**args)
        else:
            self._render_horizontal(**args)

    # ── Horizontal ────────────────────────────────────────────────────────────

    def _render_horizontal(self, ctx, events, cx, cy, cw, ch,
                           dot_r, line_color, date_color,
                           label_color, desc_color,
                           GAP_S, GAP_M,
                           badge_type, badge_bg, badge_text_color,
                           result, props) -> None:
        n = len(events)

        # Reserve space at the right for result/target node
        result_w = 0
        if result:
            result_label = str(result.get("label", ""))
            result_sz    = ctx.font_size("body")
            result_w     = max(60, min(int(cw * 0.18), len(result_label) * result_sz // 2 + GAP_M * 2))

        usable_w = cw - result_w
        ev_w     = usable_w // max(n, 1)

        # axis_pos: fraction of content_h where the axis line sits
        try:
            axis_pos = float(props.get("axis-position", 0.40))
            axis_pos = max(0.20, min(0.70, axis_pos))
        except (TypeError, ValueError):
            axis_pos = 0.40
        line_y = cy + int(ch * axis_pos)

        # Axis line (stops before result zone; arrowhead continues into it)
        arrow_tip_x = cx + usable_w + (result_w // 2 if result else 0)
        line_end_x  = arrow_tip_x - (12 if result else 0)
        ctx.divider(cx, line_y, line_end_x - cx, color=line_color)

        # Arrowhead and result node
        if result:
            arrow_sz  = max(8, dot_r // 2 + 3)
            result_color = self._resolve_color(
                ctx, str(result.get("color", "")), "on-surface")
            self._draw_arrowhead_h(ctx, line_end_x + arrow_sz, line_y,
                                   arrow_sz, line_color)
            result_label = str(result.get("label", ""))
            result_desc  = str(result.get("description", ""))
            result_sz    = ctx.font_size("body")
            rlx          = cx + usable_w + GAP_S
            rlw          = result_w - GAP_S
            label_h      = int(result_sz * 1.4) * max(1, len(result_label) // max(rlw // max(result_sz, 1), 1) + 1)
            label_h      = min(label_h, ch)
            ctx.text(rlx, cy, rlw, ch,
                     result_label,
                     size=result_sz, bold=True,
                     color=result_color,
                     align="left", valign="middle")
            if result_desc:
                ctx.text(rlx, cy + ch // 2, rlw, ch // 2, result_desc,
                         size=ctx.font_size("annotation"),
                         color=self._resolve_color(ctx, "", "on-surface-variant"),
                         align="left", valign="top")

        date_sz  = ctx.font_size("annotation")
        label_sz = ctx.font_size("caption")
        desc_sz  = ctx.font_size("annotation")

        for i, ev in enumerate(events):
            if not isinstance(ev, dict):
                continue
            ex    = cx + i * ev_w
            mid_x = ex + ev_w // 2
            status = str(ev.get("status", "neutral"))
            dot_c, _ = ctx.status_color(status)

            # Resolve badge text
            if badge_type == "number":
                btxt = ev.get("badge") or f"{i + 1:02d}"
            elif badge_type in ("text", "icon"):
                btxt = str(ev.get("badge", ""))
            else:
                btxt = ""

            # Badge / dot on axis
            self._draw_dot(ctx, mid_x, line_y, dot_r, dot_c,
                           badge_type, btxt, badge_bg, badge_text_color, props)

            # Date — above axis
            date_h = max(20, dot_r * 2)
            date_y = line_y - dot_r - GAP_S - date_h
            ctx.text(ex, date_y, ev_w, date_h,
                     str(ev.get("date", "")),
                     size=date_sz, bold=True,
                     color=date_color,
                     align="center", valign="bottom")

            # Event label — below axis
            below_y = line_y + dot_r + GAP_S
            label_h = max(20, int(label_sz * 1.4))
            ctx.text(ex, below_y, ev_w, label_h,
                     str(ev.get("label", "")),
                     size=label_sz, bold=True,
                     color=label_color,
                     align="center", valign="top")

            # Description — below label
            desc_y = below_y + label_h + GAP_S // 2
            remain = (cy + ch) - desc_y
            if remain > 10:
                desc = str(ev.get("description", ""))
                if desc:
                    ctx.text(ex, desc_y, ev_w, remain, desc,
                             size=desc_sz,
                             color=desc_color,
                             align="center", valign="top")

    # ── Vertical ─────────────────────────────────────────────────────────────

    def _render_vertical(self, ctx, events, cx, cy, cw, ch,
                         dot_r, line_color, date_color,
                         label_color, desc_color,
                         GAP_S, GAP_M,
                         badge_type, badge_bg, badge_text_color,
                         result, props) -> None:
        n         = max(len(events), 1)
        axis_x    = cx + max(80, int(cw * 0.22))
        date_w    = axis_x - cx - GAP_S
        content_x = axis_x + dot_r * 2 + GAP_M
        content_w = cx + cw - content_x

        # Reserve bottom space for result node if present
        result_h = 0
        if result:
            result_h = max(40, int(ch * 0.12))

        usable_h = ch - result_h
        row_h    = usable_h // n

        date_sz  = ctx.font_size("annotation")
        label_sz = ctx.font_size("caption")
        desc_sz  = ctx.font_size("annotation")

        # Vertical axis line
        line_end_y = cy + usable_h - (10 if result else 0)
        ctx.rect(axis_x - 1, cy, 2, line_end_y - cy, fill=line_color, stroke=None)

        # Down-arrow + result at bottom
        if result:
            arrow_sz     = max(8, dot_r // 2 + 3)
            result_color = self._resolve_color(
                ctx, str(result.get("color", "")), "on-surface")
            self._draw_arrowhead_v(ctx, axis_x, line_end_y + arrow_sz,
                                   arrow_sz, line_color)
            ctx.text(content_x, line_end_y, content_w, result_h,
                     str(result.get("label", "")),
                     size=label_sz, bold=True,
                     color=result_color,
                     align="left", valign="middle")

        for i, ev in enumerate(events):
            if not isinstance(ev, dict):
                continue
            row_y  = cy + i * row_h
            mid_y  = row_y + row_h // 2
            status = str(ev.get("status", "neutral"))
            dot_c, _ = ctx.status_color(status)

            # Resolve badge text
            if badge_type == "number":
                btxt = ev.get("badge") or f"{i + 1:02d}"
            elif badge_type in ("text", "icon"):
                btxt = str(ev.get("badge", ""))
            else:
                btxt = ""

            # Badge / dot on axis
            self._draw_dot(ctx, axis_x, mid_y, dot_r, dot_c,
                           badge_type, btxt, badge_bg, badge_text_color, props)

            # Date — left of axis
            if date_w > 0:
                dh = max(20, int(date_sz * 1.5))
                ctx.text(cx, mid_y - dh // 2, date_w, dh,
                         str(ev.get("date", "")),
                         size=date_sz, bold=True,
                         color=date_color,
                         align="right", valign="middle")

            # Label — right of axis
            label_h = max(20, int(label_sz * 1.5))
            ctx.text(content_x, row_y + GAP_S, content_w, label_h,
                     str(ev.get("label", "")),
                     size=label_sz, bold=True,
                     color=label_color,
                     align="left", valign="top")

            # Description — below label
            desc_y = row_y + GAP_S + label_h
            desc_h = row_h - GAP_S - label_h - GAP_S
            if desc_h > 8:
                desc = str(ev.get("description", ""))
                if desc:
                    ctx.text(content_x, desc_y, content_w, desc_h, desc,
                             size=desc_sz,
                             color=desc_color,
                             align="left", valign="top")
