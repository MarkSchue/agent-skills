"""DailyHeaderCard — title card with subtitle, stat pairs, and optional date/time footer"""
from __future__ import annotations


class DailyHeaderCard:
    """Render a header card with title, optional subtitle, optional left/right stat pairs,
    and an optional date/time footer.

    Deck props (all optional beyond title):
        title         : main headline (large, bold)
        subtitle      : secondary description line below title
        left_label / left-label   : label for left stat column
        left_value / left-value   : value for left stat column
        right_label / right-label : label for right stat column
        right_value / right-value : value for right stat column
        date          : date string shown in footer left
        time          : time string shown in footer right

    Customization:
        text-align    : "left" (default) | "center" | "right"
        stat-color    : token for stat values (default: "primary")
    """

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        pad = ctx.card_pad_px(w, h, props)
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        # ── Props ─────────────────────────────────────────────────────────
        title    = str(props.get("title",    ""))
        subtitle = str(props.get("subtitle", "")).strip()
        date     = str(props.get("date",  ""))
        time_str = str(props.get("time",  ""))

        # left/right stat pair — accept both underscore and hyphen
        left_label  = str(props.get("left_label",  props.get("left-label",  ""))).strip()
        left_value  = str(props.get("left_value",  props.get("left-value",  ""))).strip()
        right_label = str(props.get("right_label", props.get("right-label", ""))).strip()
        right_value = str(props.get("right_value", props.get("right-value", ""))).strip()
        has_stats   = bool(left_value or right_value)

        text_align = str(props.get("text-align", props.get("text_align", "left"))).strip()
        stat_color_token = str(props.get("stat-color", props.get("stat_color", "primary"))).strip()

        title_color    = ctx.card_title_color(props, default_token="text-default")
        subtitle_color = ctx.card_subtitle_color(props, default_token="text-secondary")
        stat_color     = ctx.color(stat_color_token)
        label_color    = ctx.card_body_color(props, default_token="text-secondary")
        divider_color  = ctx.card_line_color("title", ctx.color("line-default"), props)

        GAP_S = ctx.spacing("s")
        GAP_M = max(10, int(h * 0.022))

        show_header      = bool(title) and ctx.card_section_enabled(props, "title", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "title", default=True)
        show_footer      = bool(date or time_str) and ctx.card_section_enabled(props, "footer", default=True)
        show_footer_line = show_footer and ctx.card_line_enabled(props, "footer", default=True)

        inner_w = w - pad * 2

        # ── Footer geometry (reserve from bottom up) ──────────────────────
        footer_h    = ctx.card_footer_h(h, props) if show_footer else 0
        footer_gap  = ctx.card_footer_gap(h, props) if show_footer else 0
        footer_size = ctx.card_footer_font_size(props)
        footer_color = ctx.card_footer_color(props)
        footer_italic = ctx.card_footer_italic(props)
        footer_y    = y + h - pad - footer_h

        # ── Stats row geometry (reserve above footer) ─────────────────────
        stats_h   = 0
        stats_gap = 0
        if has_stats:
            stats_h   = max(40, int(h * 0.18))
            stats_gap = GAP_M

        # ── Header section ────────────────────────────────────────────────
        header_h   = ctx.card_title_h(w, h, props)
        header_gap = ctx.card_title_gap(h, props)
        oy = y + pad

        if show_header:
            title_sz = ctx.card_title_font_size(title, inner_w, h, props)
            ctx.text(x + pad, oy, inner_w, header_h, title,
                     size=title_sz, bold=True,
                     color=title_color,
                     align=text_align, valign="middle", inner_margin=0)
            oy += header_h + header_gap

        if show_header_line:
            lx, lw = ctx.card_divider_span("title", x + pad, inner_w, props)
            ctx.divider(lx, oy, lw, color=divider_color)
            oy += GAP_M

        # ── Subtitle ──────────────────────────────────────────────────────
        if subtitle:
            content_bottom = y + h - pad - footer_h - (footer_gap if show_footer else 0) \
                             - stats_h - (stats_gap if has_stats else 0)
            sub_avail = max(0, content_bottom - oy)
            sub_sz = ctx.fit_text_size(
                subtitle, inner_w,
                max_size=ctx.font_size("body"),
                min_size=ctx.font_size("caption"),
                bold=False, safety=0.90,
            )
            avg_chars = max(1, int(inner_w / max(1, sub_sz * 0.55)))
            n_lines   = max(1, -(-len(subtitle) // avg_chars))
            sub_h     = min(sub_avail, n_lines * int(sub_sz * 1.5) + GAP_S)
            ctx.text(x + pad, oy, inner_w, sub_h, subtitle,
                     size=sub_sz, bold=False,
                     color=subtitle_color,
                     align=text_align, valign="top", inner_margin=0)
            oy += sub_h + GAP_S

        # ── Stat pair row ─────────────────────────────────────────────────
        if has_stats:
            stat_y   = y + h - pad - footer_h - (footer_gap if show_footer else 0) - stats_h
            col_w    = inner_w // 2
            val_sz   = ctx.fit_text_size(
                max(left_value, right_value, key=len) or "—",
                col_w - GAP_S,
                max_size=ctx.font_size("heading-sub"),
                min_size=ctx.font_size("body"),
                bold=True, safety=0.88,
            )
            lbl_sz   = max(ctx.font_size("annotation"),
                           min(ctx.font_size("caption"), int(val_sz * 0.65)))
            val_h    = max(24, int(val_sz * 1.4))
            lbl_h    = max(16, int(lbl_sz * 1.4))
            pair_h   = val_h + GAP_S + lbl_h
            pair_y   = stat_y + max(0, (stats_h - pair_h) // 2)

            # Divider above stats
            ctx.divider(x + pad, stat_y, inner_w, color=divider_color)

            for col_i, (lbl, val) in enumerate([(left_label, left_value),
                                                 (right_label, right_value)]):
                cx = x + pad + col_i * col_w
                cw = col_w - GAP_S
                if val:
                    ctx.text(cx, pair_y, cw, val_h, val,
                             size=val_sz, bold=True,
                             color=stat_color,
                             align=text_align, valign="middle", inner_margin=0)
                if lbl:
                    ctx.text(cx, pair_y + val_h + GAP_S, cw, lbl_h, lbl,
                             size=lbl_sz, bold=False,
                             color=label_color,
                             align=text_align, valign="middle", inner_margin=0)

        # ── Date/time footer ──────────────────────────────────────────────
        if show_footer_line:
            lx, lw = ctx.card_divider_span("footer", x + pad, inner_w, props)
            ctx.divider(lx, footer_y - footer_gap, lw,
                        color=ctx.card_line_color("footer", ctx.color("line-default"), props))

        if show_footer and date:
            ctx.text(x + pad, footer_y, inner_w // 2, footer_h, date,
                     size=footer_size, italic=footer_italic,
                     color=footer_color,
                     align="left", valign="middle", inner_margin=0)

        if show_footer and time_str:
            ctx.text(x + w // 2, footer_y, inner_w // 2, footer_h, time_str,
                     size=footer_size, italic=footer_italic,
                     color=footer_color,
                     align="right", valign="middle", inner_margin=0)
