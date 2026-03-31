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

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        PAD = ctx.card_pad_px(w, h, props)
        GAP_S = ctx.spacing("s")
        GAP_XS = ctx.spacing("xs")
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        quote       = str(props.get("quote", ""))
        name        = str(props.get("name", "")).strip()
        title       = str(props.get("title", "")).strip()
        attribution = str(props.get("attribution", "")).strip()
        icon_name   = str(props.get("icon-name", props.get("icon_name", ""))).strip()
        if not attribution:
            if name and title:
                attribution = f"{name} — {title}"
            else:
                attribution = name or title

        quote_color = ctx.card_body_color(props, default_token="on-primary-container")
        attr_color  = ctx.card_subtitle_color(props, default_token="on-primary-container")

        attr_name_sz = max(ctx.font_size("annotation"), ctx.font_size("caption"))
        attr_meta_sz = ctx.font_size("annotation")
        attr_text = [part for part in [name, title] if part]
        has_attr_block = bool(attribution or attr_text)

        icon_sz = 0
        attr_h = 0
        attr_text_w = w - PAD * 2
        if has_attr_block:
            icon_sz = min(ctx.icon_size(w, h, props), max(0, h // 6)) if icon_name else 0
            attr_text_w = w - PAD * 2 - (icon_sz + GAP_S if icon_sz else 0)
            attr_lines = 0
            if name:
                attr_lines += self._wrap_lines(ctx, name, attr_text_w, attr_name_sz, bold=True)
            if title:
                attr_lines += self._wrap_lines(ctx, title, attr_text_w, attr_meta_sz)
            if not name and not title and attribution:
                attr_lines += self._wrap_lines(ctx, attribution, attr_text_w, attr_name_sz, bold=True)
            attr_line_h = max(attr_name_sz, attr_meta_sz)
            attr_h = max(icon_sz, int(max(1, attr_lines) * attr_line_h * 1.3))

        q_mark_sz = max(ctx.font_size("heading-sub"), min(ctx.font_size("heading-display"), int(min(w, h) * 0.12)))
        q_mark_h = max(int(q_mark_sz * 0.9), ctx.font_size("heading-sub"))
        quote_top = y + PAD + q_mark_h
        quote_h = max(24, h - PAD * 2 - q_mark_h - (attr_h + GAP_S if has_attr_block else 0))
        quote_max_sz = max(ctx.font_size("body"), min(ctx.font_size("heading-sub"), int(min(w, h) * 0.06)))
        quote_min_sz = ctx.font_size("caption")
        quote_sz = self._fit_block_size(ctx, quote, w - PAD * 2, quote_h,
                                        max_size=quote_max_sz,
                                        min_size=quote_min_sz,
                                        leading=1.28)
        quote_lines = self._wrap_lines(ctx, quote, w - PAD * 2, quote_sz)
        quote_box_h = min(quote_h, max(int(quote_sz * 1.35), int(quote_lines * quote_sz * 1.28)))

        ctx.text(x + PAD, y + PAD, q_mark_h, q_mark_h, "\u201C",
                 size=q_mark_sz, bold=True,
                 color=ctx.color("primary"),
                 align="left", valign="top", inner_margin=0)

        qy = quote_top
        ctx.text(x + PAD, qy, w - PAD * 2, max(24, quote_box_h), quote,
                 size=quote_sz,
                 color=quote_color,
                 align="left", valign="top", inner_margin=0)

        if has_attr_block:
            attr_y = y + h - PAD - attr_h
            text_x = x + PAD
            if icon_sz:
                ctx.draw_icon(x + PAD, attr_y, icon_sz, icon_sz, icon_name,
                              color=ctx.color("primary"))
                text_x += icon_sz + GAP_S

            if name or title:
                cursor_y = attr_y
                if name:
                    name_lines = self._wrap_lines(ctx, name, attr_text_w, attr_name_sz, bold=True)
                    name_h = max(int(attr_name_sz * 1.25), int(name_lines * attr_name_sz * 1.22))
                    ctx.text(text_x, cursor_y, attr_text_w, name_h,
                             name,
                             size=attr_name_sz, bold=True,
                             color=attr_color,
                             align="left", valign="top", inner_margin=0)
                    cursor_y += name_h + GAP_XS
                if title:
                    title_h = max(int(attr_meta_sz * 1.2),
                                  int(self._wrap_lines(ctx, title, attr_text_w, attr_meta_sz) * attr_meta_sz * 1.2))
                    ctx.text(text_x, cursor_y, attr_text_w, max(1, attr_y + attr_h - cursor_y),
                             title,
                             size=attr_meta_sz, bold=False, italic=True,
                             color=attr_color,
                             align="left", valign="top", inner_margin=0)
            elif attribution:
                ctx.text(text_x, attr_y, attr_text_w, attr_h,
                         f"\u2014 {attribution}",
                         size=attr_name_sz, bold=True, italic=True,
                         color=attr_color,
                         align="left", valign="middle", inner_margin=0)
