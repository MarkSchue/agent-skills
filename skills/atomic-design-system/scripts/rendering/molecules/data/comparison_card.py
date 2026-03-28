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

    # ── Public entry point ────────────────────────────────────────────────────

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        attributes = props.get("attributes", []) or []

        # Free-text path: ``left:`` / ``right:`` plain strings
        if not attributes:
            left_text  = str(props.get("left",  "") or "")
            right_text = str(props.get("right", "") or "")
            if left_text or right_text:
                self._render_text_columns(ctx, props, x, y, w, h,
                                          left_text, right_text)
                return
            # Nothing to draw — render placeholder outline only
            ctx.rect(x, y, w, h,
                     fill=ctx.color("bg-card"),
                     stroke=ctx.color("border-default"),
                     radius=ctx.rad())
            return

        # Structured attributes path (original)
        self._render_attributes(ctx, props, x, y, w, h, attributes)

    # ── Free-text columns renderer ────────────────────────────────────────────

    def _render_text_columns(self, ctx, props: dict,
                              x: int, y: int, w: int, h: int,
                              left_text: str, right_text: str) -> None:
        """Render two side-by-side text panels from free-form strings."""
        highlight   = str(props.get("highlight", "none"))
        pad         = ctx.PAD
        header_h    = max(36, int(h * 0.12))
        col_gap     = ctx.gutter
        col_w       = (w - col_gap) // 2
        rx          = x + col_w + col_gap

        # Card outline
        ctx.rect(x, y, w, h,
                 fill=ctx.color("bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        # Column fills
        l_fill = (ctx.color("primary")             if highlight == "left"
                  else ctx.color("surface-variant"))
        r_fill = (ctx.color("primary")             if highlight == "right"
                  else ctx.color("primary-container"))
        l_tc   = (ctx.color("on-primary")          if highlight == "left"
                  else ctx.color("on-surface"))
        r_tc   = (ctx.color("on-primary")          if highlight == "right"
                  else ctx.color("on-primary-container"))

        l_header, l_body = _parse_text_column(left_text)
        r_header, r_body = _parse_text_column(right_text)

        # Left column header
        ctx.rect(x, y, col_w, header_h,
                 fill=l_fill,
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())
        ctx.text(x + pad, y + 4, col_w - pad * 2, header_h - 8, l_header,
                 size=ctx.font_size("label"), bold=True,
                 color=l_tc, align="center", valign="middle")

        # Right column header
        ctx.rect(rx, y, col_w, header_h,
                 fill=r_fill,
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())
        ctx.text(rx + pad, y + 4, col_w - pad * 2, header_h - 8, r_header,
                 size=ctx.font_size("label"), bold=True,
                 color=r_tc, align="center", valign="middle")

        # Body area: bullet lists
        body_y = y + header_h + 4
        body_h = max(0, h - header_h - 4)
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

        col_w = (w - 8) // 2
        rx    = x + col_w + 8

        l_fill = (ctx.color("primary")        if highlight == "left"
                  else ctx.color("surface-variant"))
        l_tc   = (ctx.color("on-primary")     if highlight == "left"
                  else ctx.color("on-surface"))
        r_fill = (ctx.color("primary")        if highlight == "right"
                  else ctx.color("surface-variant"))
        r_tc   = (ctx.color("on-primary")     if highlight == "right"
                  else ctx.color("on-surface"))

        ctx.rect(x,  y, col_w, 48, fill=l_fill,
                 stroke=ctx.color("border-default"), radius=ctx.rad())
        ctx.text(x + 8, y + 12, col_w - 16, 24, left_label,
                 size=ctx.font_size("label"), bold=(highlight == "left"), color=l_tc,
                 align="center")

        ctx.rect(rx, y, col_w, 48, fill=r_fill,
                 stroke=ctx.color("border-default"), radius=ctx.rad())
        ctx.text(rx + 8, y + 12, col_w - 16, 24, right_label,
                 size=ctx.font_size("label"), bold=(highlight == "right"), color=r_tc,
                 align="center")

        row_h  = 38
        row_y  = y + 56
        alt_bg = ctx.color("surface-variant")
        sub_bg = ctx.color("surface")

        for i, attr in enumerate(attributes):
            if not isinstance(attr, dict):
                continue
            row_bg = alt_bg if i % 2 == 0 else sub_bg
            name   = str(attr.get("attribute", ""))
            l_val  = str(attr.get("left",  ""))
            r_val  = str(attr.get("right", ""))

            ctx.rect(x, row_y, w, 24, fill=row_bg)
            ctx.text(x + 8, row_y + 3, w - 16, 18, name,
                     size=ctx.font_size("annotation"), bold=True,
                     color=ctx.color("on-surface-variant"))
            row_y += 24

            ctx.rect(x,  row_y, col_w, row_h, fill=row_bg)
            ctx.text(x + 10, row_y + 8, col_w - 18, row_h - 14, l_val,
                     size=ctx.font_size("caption"), color=ctx.color("on-surface"))
            ctx.rect(rx, row_y, col_w, row_h, fill=row_bg)
            ctx.text(rx + 10, row_y + 8, col_w - 18, row_h - 14, r_val,
                     size=ctx.font_size("caption"), bold=(highlight == "right"),
                     color=ctx.color("on-surface"))
            row_y += row_h
            if row_y > y + h - 10:
                break
