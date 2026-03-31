"""ChartCard — harmonized chart card with shared header/footer treatment"""
from __future__ import annotations
from rendering.input_utils import parse_numeric, slice_color  # smart input helpers

# Thin aliases used in this module
_slice_val   = parse_numeric
_slice_color = slice_color


class ChartCard:
    """Render a chart card wrapping a bar chart or pie/donut legend."""

    def render(self, ctx, chart_type: str, chart_data: dict,
               x: int, y: int, w: int, h: int) -> None:
        """
        Parameters
        ----------
        ctx        : RenderContext
        chart_type : "bar" | "pie" | "donut"
        chart_data : dict with 'title', 'labels', 'values' / 'slices', 'unit'
        """
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(chart_data, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        card_pad = ctx.card_pad_px(w, h, chart_data)
        title_raw = chart_data.get("title")
        title = str(title_raw or f"chart:{chart_type}")

        icon_raw = str(chart_data.get("icon-name") or chart_data.get("icon") or title or chart_type)

        explicit_header = bool(title_raw or chart_data.get("icon-name") or chart_data.get("icon"))
        show_header = explicit_header and ctx.card_section_enabled(chart_data, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(chart_data, "header", default=True)
        footer_text = str(chart_data.get("source") or chart_data.get("note") or "")
        show_footer = bool(footer_text) and ctx.card_section_enabled(chart_data, "footer", default=True)
        show_footer_line = show_footer and ctx.card_line_enabled(chart_data, "footer", default=True)

        icon_bg = ctx.icon_bg(chart_data)
        icon_fg = ctx.icon_fg(chart_data)
        title_color = ctx.card_title_color(chart_data, default_token="text-on-muted")
        body_color = ctx.card_body_color(chart_data, default_token="text-secondary")
        header_h  = ctx.card_header_h(w, h, chart_data)
        header_gap = ctx.card_header_gap(h, chart_data)
        content_y = y + card_pad

        if show_header:
            icon_size = ctx.icon_size(w, h, chart_data) if icon_raw else 0
            icon_size = min(icon_size, header_h)  # never overflow header zone onto divider
            text_w = w - card_pad * 2 - (icon_size + header_gap if icon_raw else 0)
            title_size = ctx.card_header_font_size(title, max(40, text_w), h, chart_data)

            ctx.text(x + card_pad, content_y, max(40, text_w), header_h, title,
                     size=title_size, bold=True,
                     color=title_color, align=ctx.card_header_align(chart_data, default="left"), valign="middle")

            if icon_raw:
                icon_x = x + w - card_pad - icon_size
                icon_y = content_y + max(0, (header_h - icon_size) // 2)
                icon_radius = ctx.icon_radius(icon_size, chart_data)
                ctx.rect(icon_x, icon_y, icon_size, icon_size,
                         fill=icon_bg, stroke=ctx.icon_stroke(chart_data), radius=icon_radius)
                ctx.draw_icon(icon_x, icon_y, icon_size, icon_size, icon_raw, color=icon_fg)

            content_y += header_h + header_gap

        if show_header_line:
            line_x, line_w = ctx.card_divider_span("header", x + card_pad, w - card_pad * 2, chart_data)
            ctx.divider(line_x, content_y, line_w,
                        color=ctx.card_line_color("header", ctx.color("line-default"), chart_data))
            content_y += max(12, int(h * 0.024))

        footer_h = ctx.card_footer_h(h, chart_data) if show_footer else 0
        footer_gap = ctx.card_footer_gap(h, chart_data) if show_footer else max(ctx.spacing("s"), int(h * 0.014))
        footer_size = ctx.card_footer_font_size(chart_data)
        footer_color = ctx.card_footer_color(chart_data, default_token="text-secondary")
        footer_italic = ctx.card_footer_italic(chart_data)
        footer_y = y + h - card_pad - footer_h
        content_bottom = footer_y
        if show_footer_line:
            divider_y = footer_y - footer_gap
            line_x, line_w = ctx.card_divider_span("footer", x + card_pad, w - card_pad * 2, chart_data)
            ctx.divider(line_x, divider_y, line_w,
                        color=ctx.card_line_color("footer", ctx.color("line-default"), chart_data))
            content_bottom = divider_y - footer_gap
        elif show_footer:
            content_bottom = footer_y - footer_gap

        content_h = max(24, content_bottom - content_y)

        if chart_type == "bar":
            self._bar_chart(ctx, chart_data, x, content_y, w, content_h)
        elif chart_type in ("pie", "donut"):
            chart_data = dict(chart_data)          # don't mutate caller's dict
            chart_data["_chart_type"] = chart_type
            self._pie_legend(ctx, chart_data, x, content_y, w, content_h)

        if show_footer:
            ctx.text(x + card_pad, footer_y, w - card_pad * 2, footer_h, footer_text,
                     size=footer_size, italic=footer_italic,
                     color=footer_color, align="right", valign="middle", inner_margin=0)

    # -- Internal chart renderers ---------------------------------------------

    def _bar_chart(self, ctx, data: dict,
                   x: int, y: int, w: int, h: int) -> None:
        labels         = data.get("labels", []) or []
        values         = data.get("values", []) or []
        unit           = str(data.get("unit", ""))
        # Verbal display option: where to show value annotations.
        # "above"  (default)    — number floats above the bar
        # "inside-bottom"       — number rendered inside bar, near bottom (good for tall bars)
        label_position = str(data.get("label_position", "above")).strip().lower()
        if not labels or not values:
            return

        padding = max(16, int(min(w, h) * 0.06), ctx.spacing("l"))
        n       = len(labels)
        available_w = w - padding * 2
        gutter  = max(10, ctx.spacing("s"), int(w * 0.015))
        bw      = max(12, (available_w - (n - 1) * gutter) // max(n, 1))

        label_h = max(20, int(h * 0.10))
        value_h = max(18, int(h * 0.08))
        canvas_top = y + padding + value_h + 4
        canvas_bottom = y + h - padding - label_h - 4
        chart_h = max(20, canvas_bottom - canvas_top)

        mx_v = max(float(v) for v in values) or 1

        palette = [
            ctx.color("text-highlight"),        # primary accent
            ctx.color("text-secondary"),        # muted contrast
            ctx.color("line-strong"),           # darker neutral
            ctx.color("line-default"),          # subtle divider color
            ctx.color("success"),               # positive accent
            ctx.color("error"),                 # alert accent
        ]

        # Baseline and label lines
        ctx.line(x + padding, canvas_bottom + 2,
                 x + w - padding, canvas_bottom + 2,
                 ctx.color("line-default"))

        for i, (lbl, val) in enumerate(zip(labels, values)):
            ratio = min(1.0, float(val) / mx_v)
            bh = max(8, int(ratio * chart_h))
            bx = x + padding + i * (bw + gutter)
            by = canvas_bottom - bh

            # Bars grow from bottom to top and stay inside inset frame.
            ctx.rect(bx, by, bw, bh,
                     fill=palette[i % len(palette)], radius=ctx.rad("radius-medium"))

            # Value annotation — position depends on label_position option.
            value_size = ctx.fit_text_size(
                f"{val}{unit}",
                bw + 6,
                max_size=min(ctx.font_size("body"), max(ctx.font_size("caption"), int(w * 0.030), int(h * 0.045))),
                min_size=ctx.font_size("annotation"),
                bold=True,
                safety=0.94,
            )
            if label_position == "inside-bottom" and bh > value_size + 8:
                # Render value inside the bar, near the bottom edge.
                ctx.text(bx, by + bh - value_h - 2, bw, value_h,
                         f"{val}{unit}", size=value_size, bold=True,
                         color=ctx.color("text-on-filled"), align="center", valign="bottom")
            else:
                # Default: number floats above the bar.
                ctx.text(bx, by - value_h, bw, value_h,
                         f"{val}{unit}", size=value_size, bold=True,
                         color=ctx.color("text-default"), align="center", valign="bottom")

            # Label below each bar.
            label_size = ctx.fit_text_size(
                str(lbl),
                bw + 8,
                max_size=min(ctx.font_size("body"), max(ctx.font_size("caption"), int(w * 0.025), int(h * 0.045))),
                min_size=ctx.font_size("annotation"),
                safety=0.96,
            )
            ctx.text(bx, canvas_bottom + 6, bw, label_h,
                     str(lbl), size=label_size, color=ctx.color("text-secondary"),
                     align="center", valign="top")

    def _pie_legend(self, ctx, data: dict,
                    x: int, y: int, w: int, h: int) -> None:
        PAD             = ctx.PAD
        slices          = data.get("slices", []) or []
        is_donut        = data.get("_chart_type") == "donut"
        # Verbal configuration — where does the legend go?
        # "right" (default) | "left" | "below" | "above"
        legend_position = str(data.get("legend_position", "right")).strip().lower()

        if not slices:
            return

        # Colour palette — enough contrast across most themes
        palette = [
            ctx.color("text-highlight"),   # brand primary (orange for TKE)
            ctx.color("line-strong"),       # dark neutral
            ctx.color("text-secondary"),    # mid-grey
            ctx.color("border-default"),    # light grey
            ctx.color("success"),           # green
            ctx.color("error"),             # red
        ]

        total = sum(
            _slice_val(sl.get("value", 0)) for sl in slices if isinstance(sl, dict)
        ) or 1
        n_vis = min(len(slices), 6)

        # ------------------------------------------------------------------ #
        #  Compute chart circle centre / radius + legend area                 #
        # ------------------------------------------------------------------ #
        if legend_position in ("below", "above"):
            # Legend is a compact horizontal strip; chart fills the remaining height
            swatch       = max(10, int(h * 0.04))
            item_size    = max(ctx.font_size("caption"),
                               min(ctx.font_size("body"), int(h * 0.06)))
            leg_row_h    = max(swatch + 4, int(h * 0.18))
            chart_area_h = h - leg_row_h - PAD

            if legend_position == "below":
                chart_top = y
                leg_y     = y + chart_area_h + PAD
            else:   # above
                leg_y     = y
                chart_top = y + leg_row_h + PAD
                chart_area_h = h - leg_row_h - PAD

            r       = max(10, min(w // 2 - PAD * 2, chart_area_h // 2 - PAD))
            chart_cx = x + w // 2
            chart_cy = chart_top + chart_area_h // 2

            # Horizontal legend items
            item_w = (w - PAD * 2) // max(n_vis, 1)
            for i, sl in enumerate(slices[:n_vis]):
                if not isinstance(sl, dict):
                    continue
                fill = palette[i % len(palette)]
                ix   = x + PAD + i * item_w
                ctx.rect(ix, leg_y + (leg_row_h - swatch) // 2,
                         swatch, swatch, fill=fill, radius=2)
                ctx.text(ix + swatch + 4, leg_y,
                         item_w - swatch - 4, leg_row_h,
                         f"{sl.get('label', '')} {_slice_val(sl.get('value', 0)):.4g}%",
                         size=item_size, color=ctx.color("text-on-muted"),
                         valign="middle")

        else:   # "right" or "left"
            half_w  = w // 2
            swatch  = max(8, int(h * 0.04))
            row_h   = min(28, max(18, (h - PAD * 2) // max(n_vis, 1)))
            item_size = max(ctx.font_size("caption"),
                            min(ctx.font_size("body"), int(row_h * 0.62)))

            if legend_position == "left":
                leg_col_x = x + PAD
                chart_cx  = x + half_w + half_w // 2
            else:   # right (default)
                leg_col_x = x + half_w + PAD
                chart_cx  = x + half_w // 2

            leg_col_w = half_w - PAD * 2
            r         = max(10, min(half_w // 2 - PAD, h // 2 - PAD))
            chart_cy  = y + h // 2

            # Vertical legend items, vertically centred
            leg_y = y + (h - n_vis * row_h) // 2
            for i, sl in enumerate(slices[:n_vis]):
                if not isinstance(sl, dict):
                    continue
                fill = palette[i % len(palette)]
                ry   = leg_y + i * row_h
                ctx.rect(leg_col_x, ry + (row_h - swatch) // 2,
                         swatch, swatch, fill=fill, radius=2)
                ctx.text(leg_col_x + swatch + 6, ry,
                         leg_col_w - swatch - 6, row_h,
                         f"{sl.get('label', '')}  {_slice_val(sl.get('value', 0)):.4g}%",
                         size=item_size, color=ctx.color("text-on-muted"),
                         valign="middle")

        # ------------------------------------------------------------------ #
        #  Draw coloured wedge sectors                                         #
        # ------------------------------------------------------------------ #
        self._draw_pie_sectors(ctx, slices, palette, total, chart_cx, chart_cy,
                               r, is_donut, bg=ctx.color("bg-card"))

    # -- Sector drawing -------------------------------------------------------

    def _draw_pie_sectors(self, ctx, slices, palette, total,
                          cx, cy, r, is_donut, bg):
        """Draw pie or donut colour segments using ctx.wedge()."""
        hole_r  = int(r * 0.52) if is_donut else 0
        angle   = 0.0
        for i, sl in enumerate(slices):
            if not isinstance(sl, dict):
                continue
            raw_val = sl.get("value", 0)
            val     = _slice_val(raw_val)
            if val <= 0:
                continue
            sweep = val / total * 360
            fill  = _slice_color(raw_val, ctx, palette[i % len(palette)])
            ctx.wedge(cx, cy, r, angle, angle + sweep,
                      fill=fill,
                      hole_r=hole_r)
            angle += sweep

        # For donut: overlay a filled centre circle to punch the visual hole.
        # (PPTX freeform already has the hole baked in; this only matters for
        #  DrawIO where we layer a background disc on top.)
        if is_donut:
            ctx.ellipse(cx - hole_r, cy - hole_r,
                        hole_r * 2, hole_r * 2, fill=bg)
