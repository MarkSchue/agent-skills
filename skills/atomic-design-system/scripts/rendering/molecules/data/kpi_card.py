"""KpiCard — key performance indicator card"""
from __future__ import annotations
from rendering.input_utils import resolve_trend  # smart input interpretation




class KpiCard:
    """Render a KPI card with large value, trend arrow, and comparison note."""

    @staticmethod
    def _trend_glyph(trend: str) -> str:
        return "↑" if trend == "up" else ("↓" if trend == "down" else "→")

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        text_align = str(props.get("text-align", props.get("text_align", "left"))).strip().lower()
        if text_align not in ("left", "center", "right"):
            text_align = "left"

        label = str(props.get("label") or props.get("title") or "")
        unit  = str(props.get("unit",  ""))
        value = str(props.get("value", "—"))
        trend = resolve_trend(props.get("trend", "neutral"))
        icon_raw = str(props.get("icon-name", "") or props.get("icon", "") or label)
        # support both delta/change and comparison/reference
        delta = str(props.get("delta",  "") or props.get("change", ""))
        comp  = str(props.get("comparison", "") or props.get("reference", ""))

        has_header = bool(label or icon_raw)
        show_header = has_header and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)
        show_footer = bool(comp) and ctx.card_section_enabled(props, "footer", default=True)
        show_footer_line = show_footer and ctx.card_line_enabled(props, "footer", default=True)
        if not show_footer:
            comp = ""

        header_line_color = ctx.card_line_color("header", ctx.color("line-default"), props)
        footer_line_color = ctx.card_line_color("footer", ctx.color("line-default"), props)
        icon_bg = ctx.icon_bg(props)
        icon_fg = ctx.icon_fg(props)
        header_text_color = ctx.card_title_color(props, default_token="text-default")
        body_text_color = ctx.card_body_color(props, default_token="text-secondary")

        pad      = ctx.card_pad_px(w, h, props)
        inner_w  = w - pad * 2
        header_gap = ctx.card_header_gap(h, props)
        icon_size = ctx.icon_size(w, h, props) if icon_raw else 0
        header_h  = ctx.card_header_h(w, h, props)
        icon_size = min(icon_size, header_h)  # never overflow header zone onto divider
        label_size = ctx.card_header_font_size(label or icon_raw, inner_w, h, props)
        unit_size = ctx.font_size("body")
        compact_value = "".join(c for c in value if not c.isspace())
        char_count = max(1, len(compact_value))
        value_cap = 108 if char_count <= 8 else 88 if char_count <= 16 else 72
        trend_size = ctx.font_size("body")
        footer_size = ctx.card_footer_font_size(props)
        footer_color = ctx.card_footer_color(props, default_token="text-secondary")
        footer_italic = ctx.card_footer_italic(props)
        unit_h = max(18, int(unit_size * 1.45)) if unit else 0
        trend_h = max(28, int(trend_size * 1.45))
        comp_h = ctx.card_footer_h(h, props) if comp else 0

        header_y = y + pad
        content_y = header_y
        if show_header:
            text_w = inner_w - (icon_size + header_gap if icon_raw else 0)
            if label:
                ctx.text(x + pad, header_y, max(40, text_w), header_h, label,
                         size=label_size, bold=True,
                         color=header_text_color,
                         align=ctx.card_header_align(props, default="left"), valign="middle")

            if icon_raw:
                icon_x = x + w - pad - icon_size
                icon_y = header_y + max(0, (header_h - icon_size) // 2)
                icon_radius = ctx.icon_radius(icon_size, props)
                ctx.rect(icon_x, icon_y, icon_size, icon_size,
                         fill=icon_bg, stroke=ctx.icon_stroke(props), radius=icon_radius)
                ctx.draw_icon(icon_x, icon_y, icon_size, icon_size, icon_raw, color=icon_fg)

            content_y = header_y + header_h + header_gap

        if show_header_line:
            line_x, line_w = ctx.card_divider_span("header", x + pad, inner_w, props)
            ctx.divider(line_x, content_y, line_w, color=header_line_color)
            content_y += max(12, int(h * 0.026))

        if unit:
            ctx.text(x + pad, content_y, inner_w, unit_h, unit.upper(),
                     size=unit_size, bold=True,
                     color=body_text_color,
                     align=text_align, valign="middle")
            content_y += unit_h + max(4, int(h * 0.01))

        stack_gap = max(8, int(h * 0.018))
        minor_gap = max(6, int(h * 0.014))
        footer_y = y + h - pad - comp_h if comp else y + h - pad
        footer_line_y = footer_y - minor_gap if (comp and show_footer_line) else footer_y
        content_bottom = footer_line_y - minor_gap if comp and show_footer_line else footer_y - minor_gap if comp else y + h - pad
        content_bottom = max(content_y, content_bottom)
        available_stack_h = max(60, content_bottom - content_y)
        delta_text = f"{self._trend_glyph(trend)} {delta}".strip() if delta else self._trend_glyph(trend)
        delta_w = ctx.estimate_text_width(delta_text, trend_size, bold=True)
        delta_box_w = min(inner_w, max(trend_h + 12, int(delta_w + 10)))
        delta_box_h = trend_h
        value_h_max = max(48, available_stack_h - delta_box_h - stack_gap)
        value_size = ctx.fit_text_size(
            value,
            inner_w,
            max_size=max(ctx.font_size("heading-sub"), min(value_cap, int(value_h_max * 0.72))),
            min_size=max(ctx.font_size("body"), ctx.font_size("heading-sub") - 2),
            bold=True,
            safety=0.90,
        )
        # Cap value_h strictly to value_h_max so the value text box never
        # overflows into the delta/trend row below it.
        value_h = min(value_h_max, int(value_size * 1.45))
        total_stack_h = value_h + stack_gap + trend_h
        stack_start_y = content_y + max(0, (content_bottom - content_y - total_stack_h) // 2)
        trend_y = stack_start_y + value_h + stack_gap

        ctx.text(x + pad, stack_start_y, inner_w, value_h, value,
                 size=value_size, bold=True, color=ctx.color("text-highlight"),
                 align=text_align, valign="middle", inner_margin=0)

        tc = (ctx.color("success") if trend == "up" else
              ctx.color("error")   if trend == "down" else
              ctx.color("text-secondary"))
        ctx.text(x + pad, trend_y,
                 min(delta_box_w, inner_w) if text_align == "left" else inner_w, trend_h,
                 delta_text,
                 size=trend_size, bold=True, color=tc,
                 align=text_align, valign="middle", inner_margin=0)

        if comp:
            if show_footer_line:
                line_x, line_w = ctx.card_divider_span("footer", x + pad, inner_w, props)
                ctx.divider(line_x, footer_line_y, line_w, color=footer_line_color)
            ctx.text(x + pad, footer_y, inner_w, comp_h, comp,
                     size=footer_size, italic=footer_italic,
                     color=footer_color,
                     align=text_align, valign="middle", inner_margin=0)
