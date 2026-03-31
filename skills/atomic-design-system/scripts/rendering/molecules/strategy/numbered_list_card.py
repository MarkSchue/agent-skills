"""NumberedListCard — row-based list with number/icon/badge gutter, optional
bold headline column, and body text column. Fully configurable proportions and
typography; horizontal dividers between rows.

Design anatomy
──────────────
  ┌──────────────────────────────────────────────────────────┐
  │  [Optional title header]                                 │
  │  01   Bold headline text   Body text wraps across the    │
  │                            right column at body size     │
  │  ──────────────────────────────────────────────────────  │
  │  02   Bold headline text   Body text wraps …             │
  │  ──────────────────────────────────────────────────────  │
  │  03   (no headline)        Body text only …              │
  │  ──────────────────────────────────────────────────────  │
  └──────────────────────────────────────────────────────────┘

Number zone variants (number-type)
────────────────────────────────────
  number   — plain colored text, zero-padded ("01", "02", …)   [default]
  badge    — colored filled circle / rounded rect with number
  icon     — icon rendered via ctx.draw_icon()
  none     — gutter is hidden; headline+body fill full width

Per-card overrides (all optional)
───────────────────────────────────
  title              : card header title
  items              : list of row objects            (required)
  number-type        : number | badge | icon | none   default: number
  number-color       : plain-number text color        default: primary
  number-size        : explicit px for the number     default: auto
  number-align       : left | center                  default: left
  number-col-frac    : 0..1 fraction of inner width   default: 0.10
  badge-fill         : badge background               default: primary
  badge-text-color   : badge label color              default: on-primary
  badge-shape        : circle | rounded | square      default: rounded
  badge-size         : explicit badge diameter in px  default: auto
  headline-col-frac  : 0..1 fraction of inner width   default: 0.30
  headline-size      : explicit px for headline       default: auto
  headline-color     : headline text color            default: on-surface
  body-size          : explicit px for body text      default: auto
  body-color         : body text color                default: on-surface-variant
  show-dividers      : bool — dividers between rows   default: true
  divider-color      : row divider color              default: border-subtle
  row-valign         : top | middle                   default: middle
  column-gap         : px gap between the 3 zones     default: spacing("m")
"""
from __future__ import annotations


class NumberedListCard:
    """Render a numbered list with gutter, optional headline, and body text per row."""

    def layout_requirements(self, ds, props: dict, body: str = "") -> dict:
        """Return a conservative minimum width/height for safe layout planning."""
        items = list(props.get("items") or [])
        title = str(props.get("title", "")).strip()
        count = max(1, len(items))
        has_headline = any(
            isinstance(item, dict) and str(item.get("headline", "")).strip()
            for item in items
        )
        longest_body = max(
            [len(str((item.get("body") if isinstance(item, dict) else item) or "")) for item in items] or [len(body)]
        )
        longest_headline = max(
            [len(str(item.get("headline", ""))) for item in items if isinstance(item, dict)] or [0]
        )
        min_width = ds.font_size("body") * 28
        if has_headline:
            min_width += ds.font_size("label") * 4
        min_width += min(160, longest_body * 2)
        min_width += min(80, longest_headline * 2)
        min_height = max(ds.font_size("body") * 14, count * ds.font_size("body") * 4)
        if title:
            min_height += ds.font_size("heading-sub") * 2
        return {"min_width": int(min_width), "min_height": int(min_height)}

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _rc(self, ctx, raw: str, fallback: str) -> str:
        raw = (raw or "").strip()
        if not raw:
            return ctx.color(fallback)
        return raw if raw.startswith("#") else ctx.color(raw)

    def _int_prop(self, props: dict, key: str, default: int) -> int:
        v = props.get(key, "")
        try:
            return max(0, int(v))
        except (ValueError, TypeError):
            return default

    def _float_prop(self, props: dict, key: str, default: float) -> float:
        v = props.get(key, "")
        try:
            return max(0.0, min(1.0, float(v)))
        except (ValueError, TypeError):
            return default

    # ── Row drawing ───────────────────────────────────────────────────────────

    def _draw_badge(self, ctx, cx, cy, sz, shape, fill, text_color, label, text_size):
        """Draw a badge (circle / rounded / square) centred at (cx, cy)."""
        bx = cx - sz // 2
        by = cy - sz // 2
        if shape == "circle":
            ctx.ellipse(bx, by, sz, sz, fill=fill)
        elif shape == "square":
            ctx.rect(bx, by, sz, sz, fill=fill, stroke=None, radius=0)
        else:  # rounded (default)
            r = max(4, sz // 4)
            ctx.rect(bx, by, sz, sz, fill=fill, stroke=None, radius=r)
        ctx.text(bx, by, sz, sz, label,
                 size=text_size, bold=True, color=text_color,
                 align="center", valign="middle", inner_margin=0)

    def _draw_row(self, ctx, props,
                  rx, ry, rw, rh,
                  item, idx,
                  number_type, number_col_w, headline_col_w, body_col_w,
                  col_gap,
                  has_any_headline,
                  num_sz, hl_sz, body_sz,
                  num_color, badge_fill, badge_text_color, badge_shape, badge_sz,
                  hl_color, body_color,
                  num_align, row_valign):

        # ── Column X positions ─────────────────────────────────────────────
        num_x  = rx
        hl_x   = rx + (number_col_w + col_gap if number_type != "none" else 0)
        body_x = hl_x + (headline_col_w + col_gap if has_any_headline else 0)

        cy_mid = ry + rh // 2   # vertical centre of row

        if number_type == "none":
            pass  # no gutter
        elif number_type == "badge":
            bsz     = badge_sz if badge_sz else max(20, min(rh - 8, number_col_w - 4, 40))
            label   = _row_label(idx, item, "badge")
            per_col = item.get("color", "")
            b_fill  = self._rc(ctx, str(per_col), "primary") if per_col else badge_fill
            b_tcol  = badge_text_color
            self._draw_badge(ctx,
                             num_x + number_col_w // 2, cy_mid, bsz,
                             badge_shape, b_fill, b_tcol,
                             label, max(8, bsz // 3))
        elif number_type == "icon":
            icon_str = str(item.get("icon", item.get("badge", "")) or "")
            if icon_str:
                isz = min(rh - 8, number_col_w - 4)
                isz = max(12, isz)
                per_col = item.get("color", "")
                i_color = self._rc(ctx, str(per_col), "on-surface-variant") if per_col else num_color
                ctx.draw_icon(num_x, ry + (rh - isz) // 2,
                              number_col_w, isz,
                              icon_str, color=i_color)
        else:  # number (default)
            label = _row_label(idx, item, "number")
            per_col = item.get("color", "")
            n_color = self._rc(ctx, str(per_col), "primary") if per_col else num_color
            n_align = num_align
            valign  = "middle"
            ctx.text(num_x, ry, number_col_w, rh,
                     label, size=num_sz, bold=True,
                     color=n_color, align=n_align, valign=valign,
                     inner_margin=0)

        # ── Headline ───────────────────────────────────────────────────────
        headline = str(item.get("headline", "")).strip()
        if has_any_headline:
            if headline:
                ctx.text(hl_x, ry, headline_col_w, rh,
                         headline, size=hl_sz, bold=True,
                         color=hl_color, align="left", valign="middle",
                         inner_margin=0)

        # ── Body ───────────────────────────────────────────────────────────
        body = str(item.get("body", item.get("text", "")) or "").strip()
        if body:
            bvalign = row_valign
            ctx.text(body_x, ry, body_col_w, rh,
                     body, size=body_sz, bold=False,
                     color=body_color, align="left", valign=bvalign,
                     inner_margin=0)

    # ── Main render ───────────────────────────────────────────────────────────

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:

        items = list(props.get("items") or [])
        if not items:
            return

        n = len(items)

        # ── Card contract ─────────────────────────────────────────────────
        pad     = ctx.card_pad_px(w, h, props)
        inner_w = w - pad * 2
        title   = str(props.get("title", ""))

        show_header      = bool(title) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)

        title_color  = ctx.card_title_color(props, default_token="text-default")
        header_align = ctx.card_header_align(props, default="left")
        hdr_div_c    = ctx.card_line_color("header", ctx.color("line-default"), props)
        bg_color     = ctx.card_bg_color(props, "bg-card")

        # ── Card frame ────────────────────────────────────────────────────
        ctx.rect(x, y, w, h,
                 fill=bg_color,
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        GAP_XS = ctx.spacing("xs")
        GAP_S  = ctx.spacing("s")
        GAP_M  = ctx.spacing("m")

        cy = y + pad

        # ── Optional header ───────────────────────────────────────────────
        if show_header:
            header_h   = ctx.card_header_h(w, h, props)
            header_gap = ctx.card_header_gap(h, props)
            title_size = ctx.card_header_font_size(title, inner_w, h, props)
            ctx.text(x + pad, cy, inner_w, header_h,
                     title, size=title_size, bold=True,
                     color=title_color, align=header_align, valign="middle")
            cy += header_h + header_gap
            if show_header_line:
                lx, lw = ctx.card_divider_span("header", x + pad, inner_w, props)
                ctx.divider(lx, cy, lw, color=hdr_div_c)
                cy += 1 + GAP_S

        # ── Content bounds ────────────────────────────────────────────────
        content_top    = cy
        content_bottom = y + h - pad
        content_h      = max(20, content_bottom - content_top)

        # ── Column proportions ────────────────────────────────────────────
        number_type = str(props.get("number-type", "number")).strip().lower()
        if number_type not in ("number", "badge", "icon", "none"):
            number_type = "number"

        col_gap = self._int_prop(props, "column-gap", GAP_M)

        # Check whether any item has a headline — determines if we show/allocate
        # the headline column at all.
        has_any_headline = any(
            str(item.get("headline", "")).strip()
            for item in items
            if isinstance(item, dict)
        )

        num_col_frac = self._float_prop(props, "number-col-frac", 0.10)
        hl_col_frac  = self._float_prop(props, "headline-col-frac", 0.30)

        if number_type == "none":
            num_col_w  = 0
            gaps_total = col_gap if has_any_headline else 0
        else:
            num_col_w  = max(18, int(inner_w * num_col_frac))
            gaps_total = col_gap * (2 if has_any_headline else 1)

        if has_any_headline:
            hl_col_w = max(40, int(inner_w * hl_col_frac))
        else:
            hl_col_w = 0

        body_col_w = max(20, inner_w - num_col_w - hl_col_w - gaps_total)

        # ── Typography ────────────────────────────────────────────────────
        auto_num_sz  = max(11, min(28, int(content_h / n * 0.45)))
        auto_hl_sz   = max(11, min(22, int(content_h / n * 0.35)))
        auto_body_sz = ctx.font_size("body")

        num_sz  = self._int_prop(props, "number-size",   0) or auto_num_sz
        hl_sz   = self._int_prop(props, "headline-size", 0) or auto_hl_sz
        body_sz = self._int_prop(props, "body-size",     0) or auto_body_sz

        num_color        = self._rc(ctx, str(props.get("number-color",  "")), "primary")
        badge_fill       = self._rc(ctx, str(props.get("badge-fill",    "")), "primary")
        badge_text_color = self._rc(ctx, str(props.get("badge-text-color", "")), "on-primary")
        badge_shape      = str(props.get("badge-shape", "rounded")).strip().lower()
        if badge_shape not in ("circle", "rounded", "square"):
            badge_shape = "rounded"
        badge_sz_prop = self._int_prop(props, "badge-size", 0)

        hl_color    = self._rc(ctx, str(props.get("headline-color", "")), "on-surface")
        body_color  = self._rc(ctx, str(props.get("body-color",     "")), "on-surface-variant")
        num_align   = str(props.get("number-align", "left")).strip().lower()
        if num_align not in ("left", "center"):
            num_align = "left"
        row_valign  = str(props.get("row-valign", "middle")).strip().lower()
        if row_valign not in ("top", "middle"):
            row_valign = "middle"

        show_dividers = str(props.get("show-dividers", "true")).lower() not in ("false", "no", "0")
        div_color     = self._rc(ctx, str(props.get("divider-color", "")), "border-subtle")

        # ── Row height allocation ─────────────────────────────────────────
        # Dividers between rows (not after last)
        n_div_px  = 1
        n_divs    = (n - 1) if show_dividers else 0
        div_gap   = GAP_S   # space above and below each divider

        total_div_h = n_divs * (n_div_px + div_gap * 2)
        row_h       = max(20, (content_h - total_div_h) // n)

        # ── Per-row rendering ─────────────────────────────────────────────
        ry = content_top

        for i, item in enumerate(items):
            if not isinstance(item, dict):
                item = {"body": str(item)}

            # Resolve per-row badge size
            bsz = badge_sz_prop or max(20, min(row_h - 8, num_col_w - 4, 40))

            # Draw the row
            self._draw_row(
                ctx, props,
                x + pad, ry, inner_w, row_h,
                item, i,
                number_type=number_type,
                number_col_w=num_col_w,
                headline_col_w=hl_col_w,
                body_col_w=body_col_w,
                col_gap=col_gap,
                has_any_headline=has_any_headline,
                num_sz=num_sz, hl_sz=hl_sz, body_sz=body_sz,
                num_color=num_color,
                badge_fill=badge_fill,
                badge_text_color=badge_text_color,
                badge_shape=badge_shape,
                badge_sz=bsz,
                hl_color=hl_color,
                body_color=body_color,
                num_align=num_align,
                row_valign=row_valign,
            )

            ry += row_h

            # Divider between rows
            if show_dividers and i < n - 1:
                ry += div_gap
                ctx.divider(x + pad, ry, inner_w, color=div_color)
                ry += n_div_px + div_gap


# ── Module-level helper (avoids closure pickling issues) ──────────────────────

def _row_label(idx: int, item: dict, mode: str) -> str:
    """Return display label for the number/badge gutter."""
    custom = str(item.get("number", item.get("badge", "")) or "").strip()
    if custom:
        return custom
    n = idx + 1
    return f"{n:02d}"
