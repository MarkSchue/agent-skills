"""QuoteCard — large pull-quote with attribution"""
from __future__ import annotations
import math


class QuoteCard:
    """Render a large pull-quote card with an opening mark and attribution."""

    def layout_requirements(self, ds, props: dict, body: str = "") -> dict:
        """Return a conservative minimum width/height for safe layout planning."""
        quote = str(props.get("quote", "") or body)
        title = str(props.get("title", "") or "")
        name = str(props.get("name", "") or "")
        density = max(len(quote), len(title) + len(name))
        min_width = ds.font_size("body") * 24 + min(160, density // 3)
        min_height = ds.font_size("body") * 12 + (ds.font_size("caption") * 3 if (title or name) else 0)
        return {"min_width": int(max(420, min_width)), "min_height": int(max(220, min_height))}

    def _wrap_lines(self, ctx, text: str, width: int, size: int,
                    bold: bool = False) -> int:
        """Estimate wrapped lines for quote and attribution layout."""
        usable_w = max(1, int(width))
        total = 0
        for raw_line in str(text or "").splitlines() or [""]:
            line = raw_line.strip() or " "
            est_w = ctx.estimate_text_width(line, size, bold=bold)
            total += max(1, int(math.ceil(est_w / max(1.0, usable_w * 0.94))))
        return max(1, total)

    def _fit_block_size(self, ctx, text: str, width: int, height: int,
                        max_size: int, min_size: int,
                        bold: bool = False, leading: float = 1.3) -> int:
        """Reduce text size until it fits within both width and height."""
        floor = max(1, min_size)
        size = max(floor, max_size)
        while size > floor:
            lines = self._wrap_lines(ctx, text, width, size, bold=bold)
            need_h = max(int(size * leading), int(lines * size * leading))
            widest_ok = ctx.fit_text_size(text or " ", width,
                                          max_size=size,
                                          min_size=floor,
                                          bold=bold) >= size
            if need_h <= max(1, height) and widest_ok:
                break
            size -= 1
        return max(floor, size)

    def preferred_font_sizes(self, ctx, props: dict, w: int, h: int) -> dict:
        """Return the natural quote body size for the template pre-pass averaging."""
        return {"body": ctx.slide_font_size("body", props)}

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        PAD = ctx.card_pad_px(w, h, props)
        GAP_S = ctx.spacing("s")
        GAP_M = ctx.spacing("m")
        GAP_XS = ctx.spacing("xs")
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        # body: is the canonical alias; quote: kept for backward compatibility
        quote       = str(props.get("body", "") or props.get("quote", ""))
        # Card header — consistent with all other cards: title = top heading
        card_title  = str(props.get("title", "") or props.get("heading", "")).strip()
        # Attribution block — author/name = speaker name, role/subtitle = role line
        attr_name   = str(props.get("author", "") or props.get("name", "")).strip()
        attr_role   = str(props.get("role", "") or props.get("subtitle", "")).strip()
        attribution = str(props.get("attribution", "")).strip()
        icon_name   = str(props.get("icon-name", props.get("icon_name", ""))).strip()

        # Flatten to single attribution string if explicit, else build from parts
        if not attribution and (attr_name or attr_role):
            if attr_name and attr_role:
                attribution = f"{attr_name} — {attr_role}"
            else:
                attribution = attr_name or attr_role

        quote_color = ctx.card_body_color(props, default_token="on-primary-container")
        attr_color  = ctx.card_subtitle_color(props, default_token="on-primary-container")
        title_color = ctx.card_title_color(props, default_token="text-default")

        attr_name_sz = max(ctx.font_size("annotation"), ctx.font_size("caption"))
        attr_meta_sz = ctx.font_size("annotation")
        has_attr_block = bool(attribution or attr_name or attr_role)

        # ── Card header (title at top) ─────────────────────────────────────
        show_header      = bool(card_title) and ctx.card_section_enabled(props, "title", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "title", default=True)
        div_color        = ctx.card_line_color("title", ctx.color("line-default"), props)

        # Compute title_sz unconditionally — used as the quote font ceiling
        title_sz = ctx.card_title_font_size(card_title or "X", w - PAD * 2, h, props)

        # Quote vertical alignment within its available zone: top | middle | bottom
        quote_valign = str(props.get("quote-valign", props.get("quote_valign", "middle"))).strip().lower()
        if quote_valign not in ("top", "middle", "bottom"):
            quote_valign = "middle"

        cy = y + PAD
        if show_header:
            header_h   = ctx.card_title_h(w, h, props)
            header_gap = ctx.card_title_gap(h, props)
            ctx.text(x + PAD, cy, w - PAD * 2, header_h,
                     card_title, size=title_sz, bold=True,
                     color=title_color,
                     align=ctx.card_title_align(props, default="left"), valign="middle")
            cy += header_h + header_gap
            if show_header_line:
                lx, lw = ctx.card_divider_span("title", x + PAD, w - PAD * 2, props)
                ctx.divider(lx, cy, lw, color=div_color)
                cy += 1 + GAP_M

        # ── Attribution zone (pinned to bottom) ────────────────────────────
        icon_sz = 0
        attr_h = 0
        attr_text_w = w - PAD * 2
        if has_attr_block:
            icon_sz = min(ctx.icon_size(w, h, props), max(0, h // 6)) if icon_name else 0
            attr_text_w = w - PAD * 2 - (icon_sz + GAP_S if icon_sz else 0)
            attr_lines = 0
            if attr_name:
                attr_lines += self._wrap_lines(ctx, attr_name, attr_text_w, attr_name_sz, bold=True)
            if attr_role:
                attr_lines += self._wrap_lines(ctx, attr_role, attr_text_w, attr_meta_sz)
            if not attr_name and not attr_role and attribution:
                attr_lines += self._wrap_lines(ctx, attribution, attr_text_w, attr_name_sz, bold=True)
            attr_line_h = max(attr_name_sz, attr_meta_sz)
            attr_h = max(icon_sz, int(max(1, attr_lines) * attr_line_h * 1.3))

        # ── Quote area ─────────────────────────────────────────────────────
        q_mark_sz = max(ctx.font_size("heading-sub"), min(ctx.font_size("heading-display"), int(min(w, h) * 0.12)))
        q_mark_h  = max(int(q_mark_sz * 0.9), ctx.font_size("heading-sub"))

        quote_zone_top    = cy
        quote_zone_bottom = y + h - PAD - (attr_h + GAP_S if has_attr_block else 0)
        quote_zone_h      = max(24, quote_zone_bottom - quote_zone_top)
        # available height for the quote text itself (below the opening mark)
        quote_available_h = max(24, quote_zone_h - q_mark_h)

        # Ceiling = card title font size (never larger than the heading)
        # Use the harmonized slide body font size for quote text, to avoid
        # disjoint styling versus other cards in the same layout row.
        slide_body_sz = ctx.slide_font_size("body", props)
        quote_sz = slide_body_sz

        quote_lines = self._wrap_lines(ctx, quote, w - PAD * 2, quote_sz)
        quote_box_h = min(quote_available_h,
                          max(int(quote_sz * 1.35), int(quote_lines * quote_sz * 1.28)))

        # Vertical placement of the entire block (mark + text) within the zone
        block_h = q_mark_h + quote_box_h
        if quote_valign == "middle":
            block_offset = max(0, (quote_zone_h - block_h) // 2)
        elif quote_valign == "bottom":
            block_offset = max(0, quote_zone_h - block_h)
        else:  # top
            block_offset = 0
        block_start = quote_zone_top + block_offset

        ctx.text(x + PAD, block_start, q_mark_h, q_mark_h, "\u201C",
                 size=q_mark_sz, bold=True,
                 color=ctx.quote_mark_color(props),
                 align="left", valign="top", inner_margin=0)

        ctx.text(x + PAD, block_start + q_mark_h, w - PAD * 2, max(24, quote_box_h), quote,
                 size=quote_sz,
                 color=quote_color,
                 align="left", valign="top", inner_margin=0)

        # ── Attribution block (bottom) ─────────────────────────────────────
        if has_attr_block:
            attr_y = y + h - PAD - attr_h
            text_x = x + PAD
            if icon_sz:
                ctx.draw_icon(x + PAD, attr_y, icon_sz, icon_sz, icon_name,
                              color=ctx.color("primary"))
                text_x += icon_sz + GAP_S

            if attr_name or attr_role:
                cursor_y = attr_y
                if attr_name:
                    name_lines = self._wrap_lines(ctx, attr_name, attr_text_w, attr_name_sz, bold=True)
                    name_h = max(int(attr_name_sz * 1.25), int(name_lines * attr_name_sz * 1.22))
                    ctx.text(text_x, cursor_y, attr_text_w, name_h,
                             attr_name,
                             size=attr_name_sz, bold=True,
                             color=attr_color,
                             align="left", valign="top", inner_margin=0)
                    cursor_y += name_h + GAP_XS
                if attr_role:
                    ctx.text(text_x, cursor_y, attr_text_w, max(1, attr_y + attr_h - cursor_y),
                             attr_role,
                             size=attr_meta_sz, bold=False, italic=True,
                             color=attr_color,
                             align="left", valign="top", inner_margin=0)
            elif attribution:
                ctx.text(text_x, attr_y, attr_text_w, attr_h,
                         f"\u2014 {attribution}",
                         size=attr_name_sz, bold=True, italic=True,
                         color=attr_color,
                         align="left", valign="middle", inner_margin=0)
