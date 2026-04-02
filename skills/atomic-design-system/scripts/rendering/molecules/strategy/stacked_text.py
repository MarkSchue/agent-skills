"""StackedText — compact title + body rows with optional takeaway (molecule: stacked-text)"""
from __future__ import annotations


class StackedText:
    """Render a compact stacked-text card for adaptive 2/3/4-column grids.

    Supports ``text_align: left | center | right`` to align all text elements.
    """

    def layout_requirements(self, ds, props: dict, body: str = "") -> dict:
        """Return a conservative minimum width/height for safe layout planning."""
        items = self._items_from_props(props, body=body)
        takeaway = self._takeaway_from_props(props)
        title = str(props.get("title", "") or props.get("headline", "") or "").strip()
        longest = max([len(str(item.get("text", "") or item.get("body", "") or "")) for item in items] or [len(body)])
        min_width = max(ds.font_size("body") * 22, ds.font_size("body") * 18 + min(200, longest * 2))
        min_height = ds.font_size("body") * 10 + max(0, len(items) - 1) * ds.font_size("body") * 2
        if title:
            min_height += ds.font_size("heading-sub") * 2
        if takeaway:
            min_height += ds.font_size("heading-sub") * 3
        return {"min_width": int(min_width), "min_height": int(max(220, min_height))}

    @staticmethod
    def _items_from_props(props: dict, body: str = "") -> list[dict]:
        """Normalize rows from common topic-card authoring shapes."""
        raw_items = props.get("items") or props.get("topics") or props.get("rows") or []
        items: list[dict] = []

        if isinstance(raw_items, list):
            for item in raw_items:
                if isinstance(item, dict):
                    items.append(item)
                elif isinstance(item, str) and item.strip():
                    items.append({"text": item.strip()})

        if items:
            return items[:6]

        fallback_text = str(props.get("text", "") or props.get("body", "") or body).strip()
        if fallback_text:
            return [{"text": fallback_text}]
        return []

    @staticmethod
    def _takeaway_from_props(props: dict) -> str:
        """Return optional takeaway text."""
        return str(
            props.get("takeaway", "")
            or props.get("takeaway-line", "")
            or props.get("takeaway_line", "")
        ).strip()

    def preferred_font_sizes(self, ctx, props: dict, w: int, h: int) -> dict:
        """Return the natural body size estimate for the template pre-pass averaging.

        Uses the same responsive formula as render() so the template can collect
        a realistic preferred size from each card before deciding the slide average.
        """
        items = self._items_from_props(props)
        item_count = max(1, len(items))
        pad = ctx.card_pad_px(w, h, props)
        title = str(props.get("title", "") or props.get("headline", "") or "").strip()
        takeaway = self._takeaway_from_props(props)
        header_h = ctx.card_title_h(w, h, props) if title else 0
        header_gap = ctx.card_title_gap(h, props) if title else 0
        takeaway_h = max(68, int(h * 0.14)) if takeaway else 0
        available_h = max(96, h - pad * 2 - header_h - header_gap - takeaway_h
                          - ctx.spacing("m") * max(item_count - 1, 0))
        item_h = max(56, available_h // item_count)
        base = ctx.font_size("body")
        explicit = ctx._prop_value(props, "body_font_size", "body-font-size")
        if explicit is not None:
            try:
                return {"body": int(explicit)}
            except (ValueError, TypeError):
                pass
        responsive = min(int(item_h * 0.40), base * 2)
        return {"body": max(base, min(responsive, 32))}

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               body: str = "", **_) -> None:
        pad = ctx.card_pad_px(w, h, props)
        inner_x = x + pad
        inner_y = y + pad
        inner_w = w - pad * 2
        inner_bottom = y + h - pad
        divider_color = ctx.card_line_color("title", ctx.color("line-default"), props)
        title_color = ctx.card_title_color(props, default_token="text-default")
        body_color = ctx.card_body_color(props, default_token="text-default")

        # Global text alignment — controls title, body rows, and takeaway.
        text_align = str(props.get("text_align") or props.get("text-align") or "center").strip().lower()

        # Vertical alignment for body rows.
        text_valign = str(props.get("text_valign") or props.get("text-valign") or "middle").strip().lower()

        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        title = str(props.get("title", "") or props.get("headline", "") or props.get("heading", "")).strip()
        items = self._items_from_props(props, body=body)
        takeaway = self._takeaway_from_props(props)

        current_y = inner_y
        show_header = bool(title) and ctx.card_section_enabled(props, "title", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "title", default=True)

        header_h   = ctx.card_title_h(w, h, props)
        header_gap = ctx.card_title_gap(h, props)

        if show_header:
            title_size = ctx.card_title_font_size(title, inner_w, h, props)
            title_align = ctx.card_title_align(props, default="center")
            ctx.text(inner_x, current_y, inner_w, header_h, title,
                     size=title_size, bold=True,
                     color=title_color,
                     align=title_align, valign="middle", inner_margin=0)
            current_y += header_h + header_gap

        if show_header_line:
            line_x, line_w = ctx.card_divider_span("title", inner_x, inner_w, props)
            ctx.divider(line_x, current_y, line_w, color=divider_color)
            current_y += ctx.spacing("m")

        takeaway_h = 0
        takeaway_gap = 0
        if takeaway:
            takeaway_h = max(68, int(h * 0.14))
            takeaway_gap = ctx.spacing("m")

        content_bottom = inner_bottom - takeaway_h - takeaway_gap
        if not items:
            items = [{"text": ""}] if takeaway else []

        if items:
            item_count = len(items)
            available_h = max(96, content_bottom - current_y - ctx.spacing("m") * max(item_count - 1, 0))
            item_h = max(56, available_h // max(item_count, 1))

            # Body font size: uses slide-harmonized size from ctx.slide_font_size()
            # which respects the pre-pass average, per-slide overrides, and per-card
            # overrides.  The legacy ``body_font_size`` / ``body-font-size`` prop is
            # checked first for backward compatibility with existing deck.md files.
            explicit_body_size = ctx._prop_value(props, "body_font_size", "body-font-size")
            if explicit_body_size is not None:
                body_size = int(explicit_body_size)
            else:
                body_size = ctx.slide_font_size("body", props)

            # don’t allow body rows to exceed title size when title is present
            if show_header and title_size is not None:
                body_size = min(body_size, title_size)

            for index, item in enumerate(items):
                item_y = current_y + index * (item_h + ctx.spacing("m"))
                if item_y >= content_bottom:
                    break

                if index > 0:
                    divider_y = item_y - ctx.spacing("s")
                    ctx.divider(inner_x, divider_y, inner_w, color=divider_color)

                text = str(item.get("text", "") or item.get("body", "") or item.get("value", "")).strip()
                ctx.text(inner_x, item_y, inner_w, item_h, text,
                         size=body_size,
                         color=body_color,
                         align=text_align, valign=text_valign)

        if takeaway:
            takeaway_y = inner_bottom - takeaway_h
            chevron_w = max(30, min(44, int(inner_w * 0.11)))
            if text_align == "center":
                # Centre-aligned takeaway keeps chevron as prefix text
                ctx.text(inner_x, takeaway_y, inner_w, takeaway_h, f"» {takeaway}",
                         size=min(ctx.font_size("heading"), 24), bold=True,
                         color=title_color,
                         align="center", valign="middle")
            else:
                text_x = inner_x + chevron_w + ctx.spacing("s")
                text_w = max(24, inner_w - chevron_w - ctx.spacing("s"))
                ctx.text(inner_x, takeaway_y, chevron_w, takeaway_h, "»",
                         size=min(ctx.font_size("heading"), 22), bold=True,
                         color=title_color,
                         align="left", valign="middle")
                ctx.text(text_x, takeaway_y, text_w, takeaway_h, takeaway,
                         size=min(ctx.font_size("heading"), 24), bold=True,
                         color=title_color,
                         align=text_align, valign="middle")
