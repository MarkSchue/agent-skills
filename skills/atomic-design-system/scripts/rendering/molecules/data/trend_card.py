"""TrendCard — trend metric with sparkline bars"""
from __future__ import annotations
from rendering.input_utils import resolve_trend  # smart trend interpretation


class TrendCard:
    """Render a trend card with large value, delta, and optional sparkline."""

    @staticmethod
    def _trend_glyph(trend: str) -> str:
        return "↑" if trend == "up" else ("↓" if trend == "down" else "→")

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        label_text = str(props.get("label") or "")
        title_text = str(label_text or props.get("title") or props.get("unit") or "")
        unit       = str(props.get("unit",   ""))
        value      = str(props.get("value",  "—"))
        change     = str(props.get("change", ""))
        trend      = resolve_trend(props.get("trend", "neutral"))
        sparkline  = props.get("sparkline", [])
        if isinstance(sparkline, str):
            sparkline = [v.strip() for v in sparkline.split(",") if v.strip()]
        has_spark = bool(sparkline and isinstance(sparkline, list)
                         and len(sparkline) > 1)

        card_pad = ctx.card_pad_px(w, h, props)

        # ── Card header (matches ChartCard pattern) ──────────────────────────
        show_header      = bool(title_text) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)
        title_color      = ctx.card_title_color(props, default_token="text-default")
        body_color       = ctx.card_body_color(props, default_token="text-secondary")

        # Centralized header helpers — consistent with all other card molecules.
        header_h   = ctx.card_header_h(w, h, props)
        header_gap = ctx.card_header_gap(h, props)
        content_y  = y + card_pad

        if show_header:
            title_size = ctx.card_header_font_size(title_text, w - card_pad * 2, h, props)
            ctx.text(x + card_pad, content_y, w - card_pad * 2, header_h,
                     title_text,
                     size=title_size, bold=True,
                     color=title_color,
                     align=ctx.card_header_align(props, default="left"),
                     valign="middle", inner_margin=0)
            content_y += header_h + header_gap

        if show_header_line:
            line_x, line_w = ctx.card_divider_span("header", x + card_pad,
                                                    w - card_pad * 2, props)
            ctx.divider(line_x, content_y,
                        line_w, color=ctx.card_line_color("header",
                                                          ctx.color("line-default"), props))
            content_y += max(12, int(h * 0.024))

        # ── Remaining content geometry ────────────────────────────────────────
        remaining_h = (y + h) - content_y - card_pad
        if remaining_h <= 24:
            return

        delta_text = f"{self._trend_glyph(trend)} {change}".strip() if change else self._trend_glyph(trend)
        delta_size = ctx.font_size("body")
        delta_h = max(22, int(delta_size * 1.4))
        spark_gap = max(8, int(remaining_h * 0.04)) if has_spark else 0
        spark_target_h = max(28, int(remaining_h * 0.22)) if has_spark else 0
        value_zone_h = max(40, remaining_h - delta_h - spark_gap - spark_target_h)

        val_sz = ctx.fit_text_size(
            value,
            w - card_pad * 2,
            max_size=max(ctx.font_size("heading-sub"), min(ctx.font_size("heading-display"), int(value_zone_h * 0.70))),
            min_size=max(24, ctx.font_size("heading-sub")),
            bold=True,
            safety=0.90,
        )
        val_h = max(int(val_sz * 1.45), min(value_zone_h, int(val_sz * 2.5)))

        vy           = content_y
        ty           = vy + val_h + max(6, int(remaining_h * 0.02))
        delta_bottom = ty + delta_h + spark_gap

        ctx.text(x + card_pad, vy, w - card_pad * 2, val_h, value,
                 size=val_sz, bold=True, color=ctx.color("text-highlight"),
                 align="left", valign="middle", inner_margin=0)

        tc = (ctx.color("success") if trend == "up" else
              ctx.color("error")   if trend == "down" else
              body_color)
        ctx.text(x + card_pad, ty,
                 w - card_pad * 2, delta_h,
                 delta_text, size=delta_size, bold=True, color=tc,
                 align="left", valign="middle", inner_margin=0)

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
