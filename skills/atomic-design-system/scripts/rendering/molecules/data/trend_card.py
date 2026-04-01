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

        text_align = str(props.get("text-align", props.get("text_align", "left"))).strip().lower()
        if text_align not in ("left", "center", "right"):
            text_align = "left"

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
                 align=text_align, valign="middle", inner_margin=0)

        tc = (ctx.color("success") if trend == "up" else
              ctx.color("error")   if trend == "down" else
              body_color)
        ctx.text(x + card_pad, ty,
                 w - card_pad * 2, delta_h,
                 delta_text, size=delta_size, bold=True, color=tc,
                 align=text_align, valign="middle", inner_margin=0)

        if has_spark:
            vals = [float(v) for v in sparkline]
            mn, mx_v = min(vals), max(vals)
            span = mx_v - mn or 1

            # Optional: x-axis labels (e.g. years) shown below bars
            x_labels_raw = props.get("x-labels", props.get("x_labels", []))
            if isinstance(x_labels_raw, str):
                x_labels_raw = [v.strip() for v in x_labels_raw.split(",") if v.strip()]
            x_labels_list = list(x_labels_raw)

            # Optional: numeric labels on/inside bars
            show_bar_labels = str(props.get("show-bar-labels",
                                            props.get("show_bar_labels", "false")
                                            )).lower() in ("true", "yes", "1")
            bar_label_pos = str(props.get("bar-label-position",
                                          props.get("bar_label_position", "top")
                                          )).lower()   # "top" | "inside"

            caption_sz = ctx.font_size("caption")

            # Reserve vertical space for optional rows
            x_label_h   = max(16, int(caption_sz * 1.5)) if x_labels_list else 0
            # For "top" labels, reserve headroom above bars
            bar_label_h = max(14, int(caption_sz * 1.3)) if (show_bar_labels and bar_label_pos == "top") else 0

            # Both DrawIO arcSize and PPTX adj are PERCENTAGE-based, not pixel.
            # Actual arc radius in our coordinate space:
            #   actual_px = token_val * min(card_w, card_h) / 200
            # so we must use that (not just the raw token) as the safe inset.
            corner_r  = ctx.rad() * min(w, h) // 200 + 2   # +2 anti-alias
            h_pad     = max(card_pad, corner_r)

            # Zone boundaries
            spy         = delta_bottom
            zone_bottom = y + h - h_pad          # absolute bottom of spark zone
            bar_bottom  = zone_bottom - x_label_h   # bottom edge of bars
            bar_top     = spy + bar_label_h          # top edge of bars (headroom for top labels)

            spark_h = max(0, bar_bottom - bar_top)
            if spark_h < 10:
                return
            spark_w = w - h_pad * 2
            n       = len(vals)
            gutter  = max(2, int(w * 0.008))
            bw      = max(4, (spark_w - (n - 1) * gutter) // max(n, 1))

            for i, v in enumerate(vals):
                bh = max(3, int((v - mn) / span * (spark_h - 2)))
                bx = x + h_pad + i * (bw + gutter)
                by = bar_bottom - bh
                ctx.rect(bx, by, max(bw - 1, 2), bh,
                         fill=ctx.color("text-highlight"))

                # ── Bar value label ─────────────────────────────────────────
                if show_bar_labels:
                    raw_val = sparkline[i] if i < len(sparkline) else v
                    try:
                        fv = float(raw_val)
                        lbl_str = str(int(fv)) if fv == int(fv) else str(fv)
                    except (ValueError, TypeError):
                        lbl_str = str(raw_val)

                    lbl_sz = max(8, min(caption_sz, int(bw * 0.55)))
                    lbl_h  = max(12, int(lbl_sz * 1.3))

                    if bar_label_pos == "inside" and bh >= lbl_h + 4:
                        lbl_y     = by + 2
                        lbl_color = ctx.color("bg-card")   # contrast on bar fill
                    else:
                        # "top" — render above the bar inside the headroom
                        lbl_y     = by - lbl_h - 1
                        lbl_color = ctx.color("text-highlight")

                    ctx.text(bx, lbl_y, max(bw - 1, 2), lbl_h,
                             lbl_str, size=lbl_sz, bold=False,
                             color=lbl_color,
                             align="center", valign="middle", inner_margin=0)

            # ── X-axis legend ───────────────────────────────────────────────
            if x_labels_list and x_label_h > 0:
                lbl_sz = max(8, min(caption_sz, int(bw * 0.65)))
                for i, lbl in enumerate(x_labels_list):
                    if i >= n:
                        break
                    bx = x + h_pad + i * (bw + gutter)
                    ctx.text(bx, bar_bottom + 2, max(bw - 1, 2), x_label_h - 2,
                             str(lbl), size=lbl_sz,
                             color=body_color,
                             align="center", valign="middle", inner_margin=0)
