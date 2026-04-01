"""
QuarterGridCard — 4-to-6 item numbered/icon quarter grid
==========================================================
Renders a grid of ``QuarterAtom`` cells, laid out in a configurable number
of columns (default 2) and as many rows as needed to hold all items.

Typical use cases
-----------------
* 4 items → 2 × 2 grid
* 6 items → 2 × 3 or 3 × 2 grid (set ``columns: 3``)

Layout
------
Cells are separated by thin line dividers (colour comes from the active CSS
theme).  No individual cell borders are drawn — the "open grid" look is
achieved purely through the divider lines.  An optional outer card background
and border are drawn around the whole molecule.

Props (YAML / md-file)
----------------------
::

    items:                  # list of up to 6 quarter items
      - number:   "01"        # short badge, e.g. "01"–"06"  (mutually exclusive with icon)
        icon:     ""          # Material Icons concept, e.g. "analytics"
        headline: "Title"     # bold headline, \\n for second line
        text:     "Body…"     # descriptive paragraph
    columns:      2           # 2 (default) or 3
    align:        left        # item text alignment: left | center | right
    accent:       primary     # CSS color token for number / icon badge
    line-color:   line-default # CSS color token for the grid divider lines

Design tokens used
------------------
* ``--color-{accent}``        (number / icon badge colour)
* ``--color-{line-color}``    (grid divider colour)
* ``--color-on-surface``      (headline text)
* ``--color-on-surface-variant`` (body text)
* ``--color-bg-card``         (outer card background)
* ``--color-border-default``  (outer card border)
"""

from __future__ import annotations
import math

from rendering.atoms.text.quarter_atom import QuarterAtom  # type: ignore[import]

_ATOM = QuarterAtom()


class QuarterGridCard:
    """Render a 4–6 item quarter grid molecule (registered as ``4-6-card``)."""

    # ── Prop helpers ──────────────────────────────────────────────────────────

    @staticmethod
    def _items(props: dict) -> list[dict]:
        """Normalise ``items`` from props into a list of dicts (max 6)."""
        raw = props.get("items") or props.get("quarters") or []
        result: list[dict] = []
        if isinstance(raw, list):
            for item in raw:
                if isinstance(item, dict):
                    result.append(item)
                elif isinstance(item, str) and item.strip():
                    result.append({"text": item.strip()})
        return result[:6]

    # ── Main render ───────────────────────────────────────────────────────────

    def render(
        self,
        ctx,
        props: dict,
        x: int,
        y: int,
        w: int,
        h: int,
        **_,
    ) -> None:
        items      = self._items(props)
        n_cols     = max(1, min(3, int(props.get("columns", 2) or 2)))
        align      = str(props.get("align", "left") or "left").strip().lower()
        accent_tok = str(props.get("accent", "primary") or "primary").strip()
        line_tok   = str(props.get("line-color", "line-default") or "line-default").strip()

        accent_color  = ctx.color(accent_tok)
        line_color    = ctx.color(line_tok)
        title_color   = ctx.card_title_color(props, default_token="on-surface")
        body_color    = ctx.card_body_color(props, default_token="on-surface-variant")

        # ── Outer card background ─────────────────────────────────────────────
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        if not items:
            return

        pad = ctx.card_pad_px(w, h, props)
        inner_x = x + pad
        inner_y = y + pad
        inner_w = w - pad * 2
        inner_h = h - pad * 2

        # ── Optional card title (standard header contract) ─────────────────────
        card_title = str(props.get("title", "") or "").strip()
        show_header      = bool(card_title) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)
        if show_header:
            header_h   = ctx.card_header_h(w, h, props)
            header_gap = ctx.card_header_gap(h, props)
            title_size = ctx.card_header_font_size(card_title, inner_w, h, props)
            ctx.text(inner_x, inner_y, inner_w, header_h, card_title,
                     size=title_size, bold=True,
                     color=title_color,
                     align=ctx.card_header_align(props, default=align),
                     valign="middle", inner_margin=0)
            inner_y += header_h + header_gap
            if show_header_line:
                lx, lw = ctx.card_divider_span("header", inner_x, inner_w, props)
                ctx.divider(lx, inner_y, lw,
                            color=ctx.card_line_color("header", ctx.color("line-default"), props))
                inner_y += ctx.spacing("m")
            inner_h = (y + h - pad) - inner_y

        # ── Grid dimensions ───────────────────────────────────────────────────
        n_rows  = math.ceil(len(items) / n_cols)
        cell_w  = inner_w // n_cols
        cell_h  = inner_h // n_rows

        # ── Draw cells ────────────────────────────────────────────────────────
        for idx, item in enumerate(items):
            col = idx % n_cols
            row = idx // n_cols
            cx  = inner_x + col * cell_w
            cy  = inner_y + row * cell_h

            _ATOM.render(
                ctx, cx, cy, cell_w, cell_h,
                label    = str(item.get("number", item.get("label", "")) or ""),
                icon     = str(item.get("icon",   "") or ""),
                headline = str(item.get("headline", item.get("title", "")) or ""),
                text     = str(item.get("text",  item.get("body",  "")) or ""),
                align        = str(item.get("align", align)),
                accent_color = accent_color,
                title_color  = title_color,
                body_color   = body_color,
            )

        # ── Vertical dividers between columns ─────────────────────────────────
        for col in range(1, n_cols):
            lx = inner_x + col * cell_w
            ctx.line(lx, inner_y, lx, inner_y + inner_h, color=line_color)

        # ── Horizontal dividers between rows ──────────────────────────────────
        for row in range(1, n_rows):
            ly = inner_y + row * cell_h
            ctx.divider(inner_x, ly, inner_w, color=line_color)
