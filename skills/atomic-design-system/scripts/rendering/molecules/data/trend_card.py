"""TrendCard — trend metric with sparkline bars"""
from __future__ import annotations
from rendering.input_utils import resolve_trend  # smart trend interpretation


class TrendCard:
    """Render a trend card with large value, delta, and optional sparkline."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        # Card title: explicit 'unit' field is the metric label and takes
        # priority; fall back to the ## section heading injected as 'title'.
        title_text = str(props.get("unit") or props.get("title") or "")
        unit       = str(props.get("unit",   ""))
        value      = str(props.get("value",  "—"))
        change     = str(props.get("change", ""))
        trend      = resolve_trend(props.get("trend", "neutral"))
        sparkline  = props.get("sparkline", [])
        if isinstance(sparkline, str):
            sparkline = [v.strip() for v in sparkline.split(",") if v.strip()]
        has_spark = bool(sparkline and isinstance(sparkline, list)
                         and len(sparkline) > 1)

        card_pad = max(ctx.PAD, int(min(w, h) * 0.055))

        # ── Card header (matches ChartCard pattern) ──────────────────────────
        show_header      = bool(title_text) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)
        title_color      = ctx.card_title_color(props, default_token="text-on-muted")

        # Match ChartCard's header_h formula (no icon branch) so divider lines
        # sit at the same Y as neighbouring chart-card columns in grid-3.
        header_h   = max(34, int(h * 0.12))
        header_gap = max(8, int(h * 0.018))
        content_y  = y + card_pad

        if show_header:
            title_size = ctx.fit_text_size(
                title_text,
                w - card_pad * 2,
                max_size=max(ctx.font_size("body"), min(22, int(h * 0.034))),
                min_size=ctx.font_size("label"),
                bold=True,
                safety=0.92,
            )
            ctx.text(x + card_pad, content_y, w - card_pad * 2, header_h,
                     title_text,
                     size=title_size, bold=True,
                     color=title_color,
                     align=ctx.card_header_align(props, default="left"),
                     valign="middle")
            content_y += header_h + header_gap

        if show_header_line:
            line_x, line_w = ctx.card_divider_span("header", x + card_pad,
                                                    w - card_pad * 2, props)
            ctx.divider(line_x, content_y,
                        line_w, color=ctx.card_line_color("header",
                                                          ctx.color("line-default")))
            content_y += max(12, int(h * 0.024))

        # ── Remaining content geometry ────────────────────────────────────────
        remaining_h = (y + h) - content_y - card_pad

        val_sz = ctx.fit_text_size(
            value,
            w - card_pad * 2,
            max_size=max(36, min(120, int(remaining_h * 0.40))),
            min_size=max(24, ctx.font_size("heading-sub")),
            bold=True,
            safety=0.90,
        )
        val_h      = max(52, int(remaining_h * 0.38))
        delta_size = max(ctx.font_size("caption"),  min(ctx.font_size("heading"), int(remaining_h * 0.10)))
        delta_h    = max(24, int(remaining_h * 0.14))

        vy           = content_y
        ty           = vy + val_h + 4
        delta_bottom = ty + delta_h + max(6, int(remaining_h * 0.02))

        ctx.text(x + card_pad, vy, w - card_pad * 2, val_h, value,
                 size=val_sz, bold=True, color=ctx.color("text-highlight"))

        icon_name = ("arrow_upward"   if trend == "up"   else
                     "arrow_downward" if trend == "down" else
                     "remove")
        tc = (ctx.color("success") if trend == "up" else
              ctx.color("error")   if trend == "down" else
              ctx.color("text-secondary"))
        ctx.draw_icon(x + card_pad, ty, delta_h, delta_h, icon_name, color=tc)
        if change:
            ctx.text(x + card_pad + delta_h + 8, ty,
                     max(10, w - card_pad * 2 - delta_h - 12), delta_h,
                     change, size=delta_size, bold=True, color=tc,
                     align="left", valign="middle")

        if has_spark:
            vals = [float(v) for v in sparkline]
            mn, mx_v = min(vals), max(vals)
            span = mx_v - mn or 1

            # Both DrawIO arcSize and PPTX adj are PERCENTAGE-based, not pixel.
            # Actual arc radius in our coordinate space:
            #   actual_px = token_val * min(card_w, card_h) / 200
            # so we must use that (not just the raw token) as the safe inset.
            corner_r  = ctx.rad() * min(w, h) // 200 + 2   # +2 anti-alias
            h_pad     = max(card_pad, corner_r)

            # Sparkline fills ALL remaining space below the delta row.
            spy          = delta_bottom
            spark_bottom = y + h - h_pad    # bottom pulled in by true corner clearance
            spark_h      = max(0, spark_bottom - spy)
            if spark_h < 10:
                return
            spark_w = w - h_pad * 2
            n       = len(vals)
            gutter  = max(2, int(w * 0.008))
            bw      = max(4, (spark_w - (n - 1) * gutter) // max(n, 1))
            for i, v in enumerate(vals):
                bh = max(3, int((v - mn) / span * (spark_h - 2)))
                bx = x + h_pad + i * (bw + gutter)
                by = spark_bottom - bh
                ctx.rect(bx, by, max(bw - 1, 2), bh,
                         fill=ctx.color("text-highlight"))
