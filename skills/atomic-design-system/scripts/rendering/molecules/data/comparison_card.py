"""ComparisonCard — two-column attribute comparison table

Supports two data formats:

1. **Structured attributes** (original):
   Expects ``attributes: [{attribute, left, right}]`` list with optional
   ``left-label`` / ``right-label`` and ``highlight`` props.

2. **Free-text columns** (simple):
   When ``attributes`` is absent/empty but ``left`` and ``right`` plain-text
   strings are present, renders them as two side-by-side text panels.
   The first non-empty line of each string is used as the column header;
   remaining lines are rendered as a bullet list.
"""
from __future__ import annotations
import math
import re

from rendering.atoms.text.bullet_list import BulletListAtom  # type: ignore[import]


def _strip_markdown_bold(text: str) -> str:
    """Remove ``**bold**`` markers from a string."""
    return re.sub(r"\*\*(.+?)\*\*", r"\1", text)


def _parse_text_column(text: str) -> tuple[str, list[str]]:
    """Return ``(header, body_lines)`` from a multi-line column string."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return "", []
    header = _strip_markdown_bold(lines[0])
    body   = [_strip_markdown_bold(ln) for ln in lines[1:]]
    return header, body


class ComparisonCard:
    """Render a two-column comparison card."""

    def layout_requirements(self, ds, props: dict, body: str = "") -> dict:
        """Return a conservative minimum width/height for safe layout planning."""
        attributes = list(props.get("attributes") or [])
        left_text = str(props.get("left", "") or "")
        right_text = str(props.get("right", "") or "")
        density = len(attributes) if attributes else max(1, (len(left_text) + len(right_text)) // 140)
        min_width = ds.font_size("body") * 34 + ds.spacing("l") * 2
        min_height = ds.font_size("body") * 10 + density * ds.font_size("body") * 2
        return {"min_width": int(max(560, min_width)), "min_height": int(max(240, min_height))}

    def _wrap_lines(self, ctx, text: str, width: int, size: int,
                    bold: bool = False) -> int:
        """Estimate the number of wrapped text lines for a given box width."""
        usable_w = max(1, int(width))
        total = 0
        for raw_line in str(text or "").splitlines() or [""]:
            line = raw_line.strip() or " "
            est_w = ctx.estimate_text_width(line, size, bold=bold)
            total += max(1, int(math.ceil(est_w / max(1.0, usable_w * 0.94))))
        return max(1, total)

    def _text_block_h(self, ctx, text: str, width: int, size: int,
                      bold: bool = False, leading: float = 1.35) -> int:
        """Estimate the height required for wrapped text."""
        lines = self._wrap_lines(ctx, text, width, size, bold=bold)
        return max(int(size * leading), int(lines * size * leading))

    # ── Public entry point ────────────────────────────────────────────────────

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        attributes = props.get("attributes", []) or []

        # Card frame — drawn once here for all rendering paths
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        # ── Standard card title header ─────────────────────────────────────
        title      = str(props.get("title", "")).strip()
        show_title = bool(title) and ctx.card_section_enabled(props, "title", default=True)
        show_tline = show_title and ctx.card_line_enabled(props, "title", default=True)
        pad        = ctx.card_pad_px(w, h, props)
        content_y  = y
        if show_title or show_tline:
            title_color = ctx.card_title_color(props, default_token="text-default")
            title_align = ctx.card_title_align(props, default="left")
            div_color   = ctx.card_line_color("title", ctx.color("line-default"), props)
            cy = y + pad
            if show_title:
                th   = ctx.card_title_h(w, h, props)
                tgap = ctx.card_title_gap(h, props)
                tsz  = ctx.card_title_font_size(title, w - pad * 2, h, props)
                ctx.text(x + pad, cy, w - pad * 2, th, title,
                         size=tsz, bold=True, color=title_color,
                         align=title_align, valign="middle")
                cy += th + tgap
            if show_tline:
                lx, lw = ctx.card_divider_span("title", x + pad, w - pad * 2, props)
                ctx.divider(lx, cy, lw, color=div_color)
                cy += ctx.spacing("m")
            content_y = cy
        content_h = max(20, y + h - content_y)

        # ── Dispatch to column renderers ────────────────────────────────────
        if not attributes:
            left_text  = str(props.get("left",  "") or "")
            right_text = str(props.get("right", "") or "")
            if left_text or right_text:
                self._render_text_columns(ctx, props, x, content_y, w, content_h,
                                          left_text, right_text)
            return

        # Structured attributes path (original)
        self._render_attributes(ctx, props, x, content_y, w, content_h, attributes)

    # ── Free-text columns renderer ────────────────────────────────────────────

    def _render_text_columns(self, ctx, props: dict,
                              x: int, y: int, w: int, h: int,
                              left_text: str, right_text: str) -> None:
        """Render two side-by-side text panels from free-form strings."""
        highlight   = str(props.get("highlight", "none"))
        pad         = ctx.card_pad_px(w, h, props)
        col_gap     = max(ctx.spacing("s"), min(ctx.gutter, max(0, w // 18)))
        col_w       = max(20, (w - col_gap) // 2)
        rx          = x + col_w + col_gap
        header_max  = max(ctx.font_size("annotation"), min(ctx.font_size("label"), int(h * 0.06)))
        header_min  = ctx.font_size("annotation")

        # Column fills — highlighted column uses header_strip palette, other uses muted container
        l_fill = (ctx.header_strip_bg(props)         if highlight == "left"
                  else ctx.color("surface-variant"))
        r_fill = (ctx.header_strip_bg(props)         if highlight == "right"
                  else ctx.color("primary-container"))
        l_tc   = (ctx.header_strip_color(props)      if highlight == "left"
                  else ctx.color("on-surface"))
        r_tc   = (ctx.header_strip_color(props)      if highlight == "right"
                  else ctx.color("on-primary-container"))

        l_header, l_body = _parse_text_column(left_text)
        r_header, r_body = _parse_text_column(right_text)
        l_header_sz = ctx.fit_text_size(l_header or " ", col_w - pad * 2,
                        max_size=header_max,
                        min_size=header_min,
                        bold=True)
        r_header_sz = ctx.fit_text_size(r_header or " ", col_w - pad * 2,
                        max_size=header_max,
                        min_size=header_min,
                        bold=True)
        header_sz   = max(header_min, min(l_header_sz, r_header_sz))
        header_h    = max(int(header_sz * 2.0), ctx.card_title_h(w, h, props))

        # Left column header
        ctx.rect(x, y, col_w, header_h,
                 fill=l_fill,
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())
        ctx.text(x + pad, y + 4, col_w - pad * 2, header_h - 8, l_header,
                 size=header_sz, bold=True,
                 color=l_tc, align="center", valign="middle", inner_margin=0)

        # Right column header
        ctx.rect(rx, y, col_w, header_h,
                 fill=r_fill,
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())
        ctx.text(rx + pad, y + 4, col_w - pad * 2, header_h - 8, r_header,
                 size=header_sz, bold=True,
                 color=r_tc, align="center", valign="middle", inner_margin=0)

        # Body area: bullet lists
        body_y = y + header_h + ctx.spacing("xs")
        body_h = max(0, h - header_h - ctx.spacing("xs"))
        body_color = ctx.color("on-surface")

        if l_body:
            BulletListAtom().render(
                ctx, x + pad, body_y, col_w - pad * 2, body_h,
                items=l_body, color=body_color)

        if r_body:
            BulletListAtom().render(
                ctx, rx + pad, body_y, col_w - pad * 2, body_h,
                items=r_body, color=body_color)

    # ── Structured attributes renderer (original) ─────────────────────────────

    def _render_attributes(self, ctx, props: dict,
                            x: int, y: int, w: int, h: int,
                            attributes: list) -> None:
        left_label  = str(props.get("left-label",  "Option A"))
        right_label = str(props.get("right-label", "Option B"))
        highlight   = str(props.get("highlight",   "none"))

        pad       = ctx.card_pad_px(w, h, props)
        col_gap   = max(ctx.spacing("s"), min(ctx.gutter, max(0, w // 20)))
        col_w     = max(20, (w - col_gap) // 2)
        rx        = x + col_w + col_gap
        header_max = max(ctx.font_size("annotation"), min(ctx.font_size("label"), int(h * 0.06)))
        header_min = ctx.font_size("annotation")
        header_l_sz = ctx.fit_text_size(left_label, col_w - pad * 2,
                                        max_size=header_max,
                                        min_size=header_min,
                                        bold=True)
        header_r_sz = ctx.fit_text_size(right_label, col_w - pad * 2,
                                        max_size=header_max,
                                        min_size=header_min,
                                        bold=True)
        header_sz   = max(header_min, min(header_l_sz, header_r_sz))
        header_h    = max(int(header_sz * 2.0), ctx.card_title_h(w, h, props))
        row_gap     = ctx.spacing("xs")
        label_pad_x = max(ctx.spacing("xs"), pad // 2)
        value_pad_x = max(ctx.spacing("xs"), pad // 2)
        body_y      = y + header_h + row_gap
        available_h = max(24, y + h - body_y)

        l_fill = (ctx.color("primary")        if highlight == "left"
                  else ctx.color("surface-variant"))
        l_tc   = (ctx.color("on-primary")     if highlight == "left"
                  else ctx.color("on-surface"))
        r_fill = (ctx.color("primary")        if highlight == "right"
                  else ctx.color("surface-variant"))
        r_tc   = (ctx.color("on-primary")     if highlight == "right"
                  else ctx.color("on-surface"))

        ctx.rect(x,  y, col_w, header_h, fill=l_fill,
                 stroke=ctx.color("border-default"), radius=ctx.rad())
        ctx.text(x + pad, y, col_w - pad * 2, header_h, left_label,
                 size=header_sz, bold=(highlight == "left"), color=l_tc,
                 align="center", valign="middle", inner_margin=0)

        ctx.rect(rx, y, col_w, header_h, fill=r_fill,
                 stroke=ctx.color("border-default"), radius=ctx.rad())
        ctx.text(rx + pad, y, col_w - pad * 2, header_h, right_label,
                 size=header_sz, bold=(highlight == "right"), color=r_tc,
                 align="center", valign="middle", inner_margin=0)

        alt_bg = ctx.color("surface-variant")
        sub_bg = ctx.color("surface")

        if not attributes:
            return

        caption_max = ctx.font_size("caption")
        caption_min = max(ctx.font_size("annotation"), min(caption_max, int(caption_max * 0.85)))
        attr_max    = ctx.font_size("annotation")
        attr_min    = max(ctx.font_size("annotation"), min(attr_max, int(attr_max * 0.9)))

        def _measure_rows(attr_sz: int, value_sz: int) -> tuple[int, list[tuple[int, int]]]:
            total = 0
            dims: list[tuple[int, int]] = []
            for attr in attributes:
                if not isinstance(attr, dict):
                    continue
                name  = str(attr.get("attribute", ""))
                l_val = str(attr.get("left", ""))
                r_val = str(attr.get("right", ""))
                name_h = self._text_block_h(ctx, name, w - label_pad_x * 2,
                                            attr_sz, bold=True, leading=1.2)
                val_h = max(
                    self._text_block_h(ctx, l_val, col_w - value_pad_x * 2,
                                       value_sz, leading=1.25),
                    self._text_block_h(ctx, r_val, col_w - value_pad_x * 2,
                                       value_sz, bold=(highlight == "right"), leading=1.25),
                )
                name_h = max(int(attr_sz * 1.4), name_h) + row_gap
                val_h = max(int(value_sz * 1.5), val_h) + row_gap
                dims.append((name_h, val_h))
                total += name_h + val_h
            return total, dims

        chosen_attr_sz = attr_max
        chosen_value_sz = caption_max
        dims: list[tuple[int, int]] = []
        for value_sz in range(caption_max, caption_min - 1, -1):
            attr_sz = max(attr_min, min(attr_max, value_sz))
            total_h, candidate_dims = _measure_rows(attr_sz, value_sz)
            chosen_attr_sz = attr_sz
            chosen_value_sz = value_sz
            dims = candidate_dims
            if total_h <= available_h:
                break

        row_y = body_y

        for i, attr in enumerate(attributes):
            if not isinstance(attr, dict):
                continue
            row_bg = alt_bg if i % 2 == 0 else sub_bg
            name   = str(attr.get("attribute", ""))
            l_val  = str(attr.get("left",  ""))
            r_val  = str(attr.get("right", ""))
            name_h, val_h = dims[i] if i < len(dims) else (
                int(chosen_attr_sz * 1.5), int(chosen_value_sz * 1.6)
            )
            if row_y >= y + h:
                break

            rem_h = y + h - row_y
            name_h = min(name_h, max(int(chosen_attr_sz * 1.4), rem_h))

            ctx.rect(x, row_y, w, name_h, fill=row_bg)
            ctx.text(x + label_pad_x, row_y + row_gap // 2, w - label_pad_x * 2,
                     max(1, name_h - row_gap), name,
                     size=chosen_attr_sz, bold=True,
                     color=ctx.color("on-surface-variant"),
                     align="left", valign="middle", inner_margin=0)
            row_y += name_h
            if row_y >= y + h:
                break

            rem_h = y + h - row_y
            val_h = min(val_h, max(int(chosen_value_sz * 1.5), rem_h))

            ctx.rect(x, row_y, col_w, val_h, fill=row_bg)
            ctx.text(x + value_pad_x, row_y + row_gap // 2,
                     col_w - value_pad_x * 2, max(1, val_h - row_gap), l_val,
                     size=chosen_value_sz, color=ctx.color("on-surface"),
                     align="left", valign="middle", inner_margin=0)
            ctx.rect(rx, row_y, col_w, val_h, fill=row_bg)
            ctx.text(rx + value_pad_x, row_y + row_gap // 2,
                     col_w - value_pad_x * 2, max(1, val_h - row_gap), r_val,
                     size=chosen_value_sz, bold=(highlight == "right"),
                     color=ctx.color("on-surface"),
                     align="left", valign="middle", inner_margin=0)
            row_y += val_h
            if row_y >= y + h:
                break
