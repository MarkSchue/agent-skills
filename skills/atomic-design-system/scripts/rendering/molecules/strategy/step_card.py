"""StepCard — numbered step layout with up to 5 equal columns.

Design anatomy (per column)
────────────────────────────
  ┌──────────────────────────────────────────────────────────┐
  │  [opt header / title]                                    │
  │  01          02          03          …                   │  ← large number
  │  ────        ────        ────                            │  ← accent line (colored)
  │  Headline    Headline    Headline                        │  ← bold headline
  │  two lines   two lines   two lines                       │
  ├──────────────────────────────────────────────────────────┤  ← full-width divider
  │  Body text   Body text   Body text                       │
  │  wraps…      wraps…      wraps…                          │
  └──────────────────────────────────────────────────────────┘

Per-card overrides (all optional)
───────────────────────────────────
  number-type        : "number" (auto 01,02…) | "text" (reads step.number)
                       | "icon" (reads step.icon) | "none"        default: number
  active-step        : 1-based index — highlights that column with active-color  default: 0 (none)
  active-color       : color token/hex for the active step               default: primary
  default-color      : color token/hex for steps without a status        default: on-surface-variant
  done-color         : color token/hex for status=done                   default: success
  muted-color        : color token/hex for status=muted                  default: border-subtle
  number-size        : explicit font-size in px for the big number       default: auto
  show-accent-line   : bool — draw the colored bar under the number      default: true
  accent-line-width  : 0..1 fraction of col width                        default: 0.35
  accent-line-height : px                                                 default: 3
  divider-position   : 0..1 fraction of content height for the divider   default: 0.52
  headline-color     : global override for all headline texts            default: on-surface
  body-color         : global override for all body texts                default: on-surface-variant

Per-step fields (inside each item of ``steps``)
─────────────────────────────────────────────────
  headline    : bold step title (required)
  body        : supporting text shown below the divider
  number      : custom label when number-type=text  (fallback: auto index)
  icon        : icon description when number-type=icon
  badge       : alias for number/icon (convenience)
  status      : "active" | "done" | "muted" | "default"
  color       : per-step explicit color override (overrides status)
"""
from __future__ import annotations


class StepCard:
    """Render a numbered step layout with 1–5 equal columns."""

    def layout_requirements(self, ds, props: dict, body: str = "") -> dict:
        """Return a conservative minimum width/height for safe layout planning."""
        steps = list(props.get("steps") or [])[:5]
        count = max(1, len(steps))
        title = str(props.get("title", "")).strip()
        col_min_w = max(ds.font_size("body") * 9, ds.font_size("heading-sub") * 6)
        min_width = col_min_w * count + ds.spacing("m") * max(0, count - 1) + ds.spacing("l") * 2
        min_height = max(ds.font_size("body") * 16, ds.font_size("heading-sub") * 10)
        if title:
            min_height += ds.font_size("heading-sub") * 2
        return {"min_width": int(min_width), "min_height": int(min_height)}

    # ── Color helpers ─────────────────────────────────────────────────────────

    def _resolve_color(self, ctx, raw: str, fallback: str) -> str:
        raw = (raw or "").strip()
        if not raw:
            return ctx.color(fallback)
        return raw if raw.startswith("#") else ctx.color(raw)

    def _step_color(self, ctx, step: dict, idx: int, props: dict,
                    active_step: int) -> str:
        """Resolve the accent color for a single step."""
        # 1. Explicit per-step color wins
        if "color" in step:
            return self._resolve_color(ctx, str(step["color"]), "on-surface-variant")
        # 2. Per-step status
        status = str(step.get("status", "")).strip().lower()
        if status == "active":
            return self._resolve_color(ctx, str(props.get("active-color", "")), "primary")
        if status == "done":
            return self._resolve_color(ctx, str(props.get("done-color", "")), "success")
        if status == "muted":
            return self._resolve_color(ctx, str(props.get("muted-color", "")), "border-subtle")
        # 3. active-step index match (1-based)
        if active_step > 0 and idx == active_step - 1:
            return self._resolve_color(ctx, str(props.get("active-color", "")), "primary")
        # 4. Default
        return self._resolve_color(ctx, str(props.get("default-color", "")), "on-surface-variant")

    # ── Main render ───────────────────────────────────────────────────────────

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:

        steps = list(props.get("steps") or [])[:5]
        if not steps:
            return

        n           = len(steps)
        number_type = str(props.get("number-type", "number")).strip().lower()
        active_step = int(props.get("active-step", 0) or 0)

        # ── Card contract ─────────────────────────────────────────────────
        pad     = ctx.card_pad_px(w, h, props)
        inner_w = w - pad * 2
        title   = str(props.get("title", ""))

        show_header      = bool(title) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)

        title_color   = ctx.card_title_color(props, default_token="text-default")
        header_align  = ctx.card_header_align(props, default="left")
        divider_color = ctx.card_line_color("header", ctx.color("line-default"), props)
        bg_color      = ctx.card_bg_color(props, "bg-card")

        # ── Card frame ────────────────────────────────────────────────────
        ctx.rect(x, y, w, h,
                 fill=bg_color,
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        # ── Optional header ───────────────────────────────────────────────
        GAP_XS = ctx.spacing("xs")   # 4 px
        GAP_S  = ctx.spacing("s")    # 8 px
        GAP_M  = ctx.spacing("m")    # 16 px

        cy = y + pad

        if show_header:
            header_h   = ctx.card_header_h(w, h, props)
            header_gap = ctx.card_header_gap(h, props)
            title_size = ctx.card_header_font_size(title, inner_w, h, props)
            ctx.text(x + pad, cy, inner_w, header_h,
                     title,
                     size=title_size, bold=True,
                     color=title_color,
                     align=header_align, valign="middle")
            cy += header_h + header_gap
            if show_header_line:
                ctx.rect(x + pad, cy, inner_w, 1, fill=divider_color, stroke=None)
                cy += 1 + header_gap

        # ── Content area ──────────────────────────────────────────────────
        content_bottom = y + h - pad
        content_h      = content_bottom - cy
        cx             = x + pad

        # Column layout: equal widths with inter-column gap
        col_gap = max(GAP_S, min(GAP_M, int(inner_w * 0.025)))
        col_w   = max(20, (inner_w - col_gap * (n - 1)) // n)

        # Divider splits header-zone (number + accent + headline) from body
        divider_pos  = float(props.get("divider-position", 0.52))
        divider_pos  = max(0.25, min(0.80, divider_pos))
        divider_y    = cy + int(content_h * divider_pos)
        header_zone_h = divider_y - cy

        # --- Number font size ---
        raw_num_sz = props.get("number-size", "")
        if raw_num_sz:
            try:
                num_font_sz = max(10, int(raw_num_sz))
            except (ValueError, TypeError):
                num_font_sz = 0
        else:
            num_font_sz = 0
        if not num_font_sz:
            # scale with column width and header zone; land in ~20–52 px range
            num_font_sz = max(20, min(52, int(min(col_w * 0.36, header_zone_h * 0.42))))

        # --- Headline and body font sizes ---
        headline_font_sz = max(10, min(20, int(col_w * 0.095 + 4)))
        body_font_sz     = ctx.font_size("body")

        # --- Accent line config ---
        show_accent       = str(props.get("show-accent-line", "true")).lower() != "false"
        accent_line_frac  = float(props.get("accent-line-width", 0.35))
        accent_line_thick = int(props.get("accent-line-height", 3))

        # --- Headline / body color globals ---
        _headline_global = str(props.get("headline-color", "")).strip()
        _body_global     = str(props.get("body-color", "")).strip()

        # ── Draw each step column ─────────────────────────────────────────
        for i, step in enumerate(steps):
            sx         = cx + i * (col_w + col_gap)
            step_color = self._step_color(ctx, step, i, props, active_step)

            # -- Badge text (number / text / icon / none) --
            if number_type == "number":
                badge_text = f"{i + 1:02d}"
            elif number_type in ("text", "badge"):
                badge_text = str(step.get("number", step.get("badge", str(i + 1))))
            elif number_type == "icon":
                badge_text = str(step.get("icon", step.get("badge", "")))
            else:
                badge_text = ""

            # ─── Number / icon ────────────────────────────────────────────
            # Allocate ~40 % of header zone for the number block
            num_zone_h = max(num_font_sz + 4, int(header_zone_h * 0.40))

            if number_type == "icon" and badge_text:
                icon_sz = min(num_font_sz, num_zone_h)
                ctx.draw_icon(sx, cy + (num_zone_h - icon_sz) // 2,
                              icon_sz, icon_sz,
                              badge_text, color=step_color)
            elif badge_text:
                ctx.text(sx, cy, col_w, num_zone_h,
                         badge_text,
                         size=num_font_sz, bold=False,
                         color=step_color,
                         align="left", valign="bottom",
                         inner_margin=0)

            # ─── Accent line ──────────────────────────────────────────────
            accent_y = cy + num_zone_h + GAP_XS
            if show_accent:
                accent_w = max(10, int(col_w * accent_line_frac))
                ctx.rect(sx, accent_y, accent_w, accent_line_thick,
                         fill=step_color, stroke=None)

            # ─── Headline ─────────────────────────────────────────────────
            headline_y = accent_y + (accent_line_thick if show_accent else 0) + GAP_S
            headline_h = max(10, divider_y - headline_y - GAP_XS)
            headline   = str(step.get("headline", step.get("label", "")))

            if _headline_global:
                hc = self._resolve_color(ctx, _headline_global, "on-surface")
            else:
                hc = ctx.color("on-surface")

            if headline:
                ctx.text(sx, headline_y, col_w, headline_h,
                         headline,
                         size=headline_font_sz, bold=True,
                         color=hc,
                         align="left", valign="top",
                         inner_margin=0)

        # ── Full-width divider ────────────────────────────────────────────
        divider_fill = self._resolve_color(
            ctx,
            str(props.get("divider-color", "")),
            "border-subtle",
        )
        ctx.rect(cx, divider_y, inner_w, 1, fill=divider_fill, stroke=None)

        # ── Body text ─────────────────────────────────────────────────────
        body_y    = divider_y + 1 + GAP_S
        body_zone = max(10, content_bottom - body_y)

        for i, step in enumerate(steps):
            sx        = cx + i * (col_w + col_gap)
            body_text = str(step.get("body", step.get("description", "")))
            if not body_text:
                continue

            bc = (self._resolve_color(ctx, _body_global, "on-surface-variant")
                  if _body_global else ctx.color("on-surface-variant"))

            ctx.text(sx, body_y, col_w, body_zone,
                     body_text,
                     size=body_font_sz, bold=False,
                     color=bc,
                     align="left", valign="top",
                     inner_margin=0)
