"""KpiCard — key performance indicator card"""
from __future__ import annotations
from rendering.input_utils import resolve_trend  # smart input interpretation




class KpiCard:
    """Render a KPI card with large value, trend arrow, and comparison note."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

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
        header_text_color = ctx.card_title_color(props, default_token="text-on-muted")
        body_text_color = ctx.card_body_color(props, default_token="text-on-muted")

        pad      = ctx.card_pad_px(w, h, props)
        inner_w  = w - pad * 2
        header_gap = ctx.card_header_gap(h, props)
        icon_size = ctx.icon_size(w, h, props) if icon_raw else 0
        header_h  = ctx.card_header_h(w, h, props)
        icon_size = min(icon_size, header_h)  # never overflow header zone onto divider
        label_size = ctx.card_header_font_size("", inner_w, h, props)
        unit_size = max(ctx.font_size("caption"), min(ctx.font_size("body"), int(h * 0.026)))
        compact_value = "".join(c for c in value if not c.isspace())
        char_count = max(1, len(compact_value))
        value_cap = 132 if char_count <= 3 else 116 if char_count <= 6 else 104
        value_size = ctx.fit_text_size(
            value,
            inner_w,
            max_size=max(ctx.font_size("heading-display"), min(value_cap, int(h * 0.20))),
            min_size=max(28, ctx.font_size("heading-sub")),
            bold=True,
            safety=0.90,
        )
        trend_size = max(ctx.font_size("label"), min(26, int(h * 0.052)))
        footer_size = max(ctx.font_size("label"), min(20, int(h * 0.032)))
        unit_h = max(18, int(unit_size * 1.45)) if unit else 0
        trend_h = max(28, int(trend_size * 1.45))
        comp_h = max(20, int(footer_size * 1.55)) if comp else 0
        value_h_target = max(80, int(value_size * 1.22))

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
                     align="left", valign="middle")
            content_y += unit_h + max(4, int(h * 0.01))

        stack_gap = max(8, int(h * 0.018))
        minor_gap = max(6, int(h * 0.014))
        footer_y = y + h - pad - comp_h if comp else y + h - pad
        footer_line_y = footer_y - minor_gap if (comp and show_footer_line) else footer_y
        content_bottom = footer_line_y - minor_gap if comp and show_footer_line else footer_y - minor_gap if comp else y + h - pad
        content_bottom = max(content_y, content_bottom)
        available_stack_h = max(60, content_bottom - content_y - stack_gap - trend_h)
        value_h = max(52, min(value_h_target, available_stack_h))
        if value_h < value_h_target:
            value_size = min(value_size, max(28, int(value_h / 1.22)))
        total_stack_h = value_h + stack_gap + trend_h
        stack_start_y = content_y + max(0, (content_bottom - content_y - total_stack_h) // 2)
        trend_y = stack_start_y + value_h + stack_gap

        ctx.text(x + pad, stack_start_y, inner_w, value_h, value,
                 size=value_size, bold=True, color=ctx.color("text-highlight"),
                 align="left", valign="middle")

        icon_name = ("arrow_upward"   if trend == "up"   else
                     "arrow_downward" if trend == "down" else
                     "remove")
        tc = (ctx.color("success") if trend == "up" else
              ctx.color("error")   if trend == "down" else
              ctx.color("text-secondary"))
        ctx.draw_icon(x + pad, trend_y, trend_h, trend_h, icon_name, color=tc)
        if delta:
            ctx.text(x + pad + trend_h + 8, trend_y,
                     max(10, inner_w - trend_h - 8), trend_h,
                     delta, size=trend_size, bold=True, color=tc,
                     align="left", valign="middle")

        if comp:
            if show_footer_line:
                line_x, line_w = ctx.card_divider_span("footer", x + pad, inner_w, props)
                ctx.divider(line_x, footer_line_y, line_w, color=footer_line_color)
            ctx.text(x + pad, footer_y, inner_w, comp_h, comp,
                     size=footer_size, italic=True,
                     color=body_text_color,
                     align="left", valign="middle")
