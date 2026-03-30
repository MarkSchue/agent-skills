"""TopicCard — compact title + topic rows with optional takeaway (also registered as stacked-text)"""
from __future__ import annotations


class TopicCard:
    """Render a compact topic card for adaptive 2/3/4-column grids.

    Supports ``text_align: left | center | right`` to align all text elements.
    """

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

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               body: str = "", **_) -> None:
        pad = ctx.PAD
        inner_x = x + pad
        inner_y = y + pad
        inner_w = w - pad * 2
        inner_bottom = y + h - pad
        divider_color = ctx.card_line_color("header", ctx.color("line-default"), props)
        title_color = ctx.card_title_color(props, default_token="text-default")
        body_color = ctx.card_body_color(props, default_token="text-default")

        # Global text alignment — controls title, body rows, and takeaway.
        # Per-element overrides (header_align) still take precedence for the title.
        text_align = str(props.get("text_align") or props.get("text-align") or "left").strip().lower()

        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        title = str(props.get("title", "") or props.get("headline", "") or props.get("heading", "")).strip()
        items = self._items_from_props(props, body=body)
        takeaway = self._takeaway_from_props(props)

        current_y = inner_y
        show_header = bool(title) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)

        if show_header:
            title_h = max(36, min(56, int(h * 0.10)))
            title_size = min(ctx.font_size("heading"), 24)
            explicit_header_align = ctx._prop_value(props, "header_align", "header-align", "title_align", "title-align")
            if explicit_header_align is not None:
                title_align = ctx.card_header_align(props, default=text_align)
            else:
                title_align = text_align
            ctx.text(inner_x, current_y, inner_w, title_h, title,
                     size=title_size, bold=True,
                     color=title_color,
                     align=title_align, valign="middle")
            current_y += title_h + ctx.spacing("s")

        if show_header_line:
            line_x, line_w = ctx.card_divider_span("header", inner_x, inner_w, props)
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

            for index, item in enumerate(items):
                item_y = current_y + index * (item_h + ctx.spacing("m"))
                if item_y >= content_bottom:
                    break

                if index > 0:
                    divider_y = item_y - ctx.spacing("s")
                    ctx.divider(inner_x, divider_y, inner_w, color=divider_color)

                text = str(item.get("text", "") or item.get("body", "") or item.get("value", "")).strip()
                ctx.text(inner_x, item_y, inner_w, item_h, text,
                         size=ctx.font_size("body"),
                         color=body_color,
                         align=text_align, valign="top")

        if takeaway:
            takeaway_y = inner_bottom - takeaway_h
            chevron_w = max(30, min(44, int(inner_w * 0.11)))
            if text_align == "center":
                # Centre-aligned takeaway keeps chevrons as prefix text
                ctx.text(inner_x, takeaway_y, inner_w, takeaway_h, f"»» {takeaway}",
                         size=min(ctx.font_size("heading"), 24), bold=True,
                         color=title_color,
                         align="center", valign="middle")
            else:
                text_x = inner_x + chevron_w + ctx.spacing("s")
                text_w = max(24, inner_w - chevron_w - ctx.spacing("s"))
                ctx.text(inner_x, takeaway_y, chevron_w, takeaway_h, "»»",
                         size=min(ctx.font_size("heading"), 22), bold=True,
                         color=divider_color,
                         align="left", valign="middle")
                ctx.text(text_x, takeaway_y, text_w, takeaway_h, takeaway,
                         size=min(ctx.font_size("heading"), 24), bold=True,
                         color=title_color,
                         align=text_align, valign="middle")
