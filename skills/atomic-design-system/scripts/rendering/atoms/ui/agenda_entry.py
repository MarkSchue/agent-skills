"""
AgendaEntryAtom — single agenda row (number / time / icon + title / description)
=================================================================================
Renders one horizontal agenda row.  Multiple rows must be placed by the parent
molecule with a shared ``label_w`` so the left-column **and** right-column
content aligns across all entries.

Layout
------
  ┌──────────────────────────────────────────────────────────────────────┐
  │ ─────────────────── separator line (show_divider) ────────────────── │
  │  [label: number│time│icon]  │  [title (bold)]                        │
  │                             │  [description line 1]                  │
  │                             │  [description line 2]                  │
  └──────────────────────────────────────────────────────────────────────┘

Left column variants
  number : large accent-coloured ordinal, e.g. "01"
  time   : compact accent-coloured time range, e.g. "08:00–12:00"
  icon   : icon glyph in a rounded accent background tile, e.g. "coffee"

Highlight mode
  When ``highlight=True`` a light primary-container tint covers the full row
  before all other elements — this marks the *current* agenda point in a
  step-through presentation.

Alignment contract
  Pass the **same** ``label_w`` and ``gap`` values to every AgendaEntryAtom
  call inside one agenda group.  The parent molecule is responsible for
  computing label_w from the widest label across all entries.
"""
from __future__ import annotations

# Fraction of row_h used for the icon tile height (avoids perfect-square crop)
_ICON_TILE_RATIO = 0.65


class AgendaEntryAtom:
    """Render one horizontal agenda row.

    Designed to be stacked vertically by a parent `agenda-card` molecule.
    Do not render in isolation — the parent manages vertical positioning,
    row heights, and the shared ``label_w`` / ``gap`` contract.
    """

    def render(
        self,
        ctx,
        x: int,
        y: int,
        w: int,
        h: int,
        *,
        label_w: int,
        gap: int = 12,
        label_type: str = "number",
        label: str = "",
        title: str = "",
        description: str = "",
        highlight: bool = False,
        show_divider: bool = True,
        # --- optional colour overrides (resolved by the parent molecule) ---
        label_color: str | None = None,
        icon_bg_color: str | None = None,
        icon_fg_color: str | None = None,
        title_color: str | None = None,
        body_color: str | None = None,
        highlight_color: str | None = None,
        divider_color: str | None = None,
    ) -> None:
        """Render one agenda row.

        Parameters
        ----------
        ctx              : RenderContext
        x, y             : top-left corner in pixels
        w, h             : bounding box dimensions in pixels
        label_w          : width of the left label column (shared across a group)
        gap              : horizontal gap between label column and text column
        label_type       : ``"number"`` | ``"time"`` | ``"icon"``
        label            : text (number/time) or icon concept name (icon variant)
        title            : bold heading, e.g. ``"Topic | Presenter"``
        description      : body text; use ``\\n`` for up to 2 lines
        highlight        : True draws a primary-container background behind the row
        show_divider     : True draws a 1 px separator above the row
        label_color      : hex override for number/time text (default: primary)
        icon_bg_color    : hex override for icon tile background (default: primary)
        icon_fg_color    : hex override for icon glyph (default: on-primary)
        title_color      : hex override for title text (default: on-surface)
        body_color       : hex override for description text (default: on-surface-variant)
        highlight_color  : hex override for highlight tint (default: primary-container)
        divider_color    : hex override for separator line (default: border-subtle)
        """

        # ── Resolve colours from theme (allow caller to override) ────────────
        _label_col  = label_color     or ctx.color("primary")
        _icon_bg    = icon_bg_color   or ctx.color("primary")
        _icon_fg    = icon_fg_color   or ctx.color("on-primary")
        _title_col  = title_color     or ctx.color("on-surface")
        _body_col   = body_color      or ctx.color("on-surface-variant")
        _hl_col     = highlight_color or ctx.color("primary-container")
        _div_col    = divider_color   or ctx.color("border-subtle")

        # ── 1. Separator above this row ──────────────────────────────────────
        if show_divider:
            ctx.divider(x, y, w, color=_div_col)

        # ── 2. Highlight background (drawn before content) ───────────────────
        if highlight:
            ctx.rect(x, y, w, h, fill=_hl_col, stroke=None, radius=0)

        # ── 3. Left label column ─────────────────────────────────────────────
        label_cx = x  # label column starts at x, spans label_w

        if label_type == "icon":
            # Centred rounded tile with icon glyph
            tile_s = max(24, min(int(h * _ICON_TILE_RATIO), label_w - 8))
            tile_x = label_cx + (label_w - tile_s) // 2
            tile_y = y + (h - tile_s) // 2
            ctx.rect(tile_x, tile_y, tile_s, tile_s,
                     fill=_icon_bg, stroke=None,
                     radius=ctx.icon_radius(tile_s))
            if label:
                ctx.draw_icon(tile_x, tile_y, tile_s, tile_s,
                              label, color=_icon_fg)

        elif label_type == "time":
            # Compact time string — bold, auto-sized, centred vertically
            # Choose a font size that fits the label_w width
            t_sz = max(10, min(int(h * 0.24), 16))
            ctx.text(
                label_cx, y, label_w, h,
                label,
                size=t_sz, bold=True,
                color=_label_col,
                align="center", valign="middle",
            )

        else:  # "number" (default)
            # Large ordinal, prominently sized
            n_sz = max(14, min(int(h * 0.50), 36))
            ctx.text(
                label_cx, y, label_w, h,
                label,
                size=n_sz, bold=True,
                color=_label_col,
                align="center", valign="middle",
            )

        # ── 4. Right text column ─────────────────────────────────────────────
        tx = x + label_w + gap
        tw = max(1, w - label_w - gap)

        t_sz = ctx.font_size("label")
        d_sz = ctx.font_size("caption")
        t_h  = int(t_sz * 1.45)
        d_h  = int(d_sz * 1.40)

        # Parse description — support both \n-delimited string and list
        if isinstance(description, list):
            desc_lines = [str(ln) for ln in description if str(ln).strip()]
        else:
            desc_lines = [ln for ln in (description or "").split("\n") if ln.strip()]
        n_desc = min(len(desc_lines), 2)

        total_text_h = t_h + n_desc * d_h
        start_ty = y + max(0, (h - total_text_h) // 2)

        ctx.text(
            tx, start_ty, tw, t_h,
            title,
            size=t_sz, bold=True,
            color=_title_col,
            align="left", valign="top",
        )

        for i, line in enumerate(desc_lines[:2]):
            ctx.text(
                tx, start_ty + t_h + i * d_h, tw, d_h,
                line,
                size=d_sz, bold=False,
                color=_body_col,
                align="left", valign="top",
            )
