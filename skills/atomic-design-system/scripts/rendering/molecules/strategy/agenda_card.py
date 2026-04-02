"""
AgendaCard — responsive schedule card composing AgendaEntryAtom rows
=====================================================================
Renders a card-backed, vertically stacked list of agenda entries.  All
entries share a common ``label_w`` so numbers, times, and icons align to
one vertical edge and titles align to another.

Layout
------
  ┌────────────────────────────────────────────────────────────────────┐
  │  [icon]  Card Title                      header divider (opt.)    │
  │ ─────────────────────────────────────────────────────────────────│
  │  01    Topic | Presenter                                          │
  │        Description line 1 · line 2                               │
  │  ─────────────────────────────────────────────────────────────── │
  │  08:00  Topic | Presenter              ← highlighted row         │
  │  ─────────────────────────────────────────────────────────────── │
  │  ☕     Coffee Break                                               │
  │                                                                    │
  │  (empty space if entries < available rows)                         │
  └────────────────────────────────────────────────────────────────────┘

Responsive sizing
-----------------
* ``row_h``    — computed from available body height ÷ n_entries;
                 clamped to [MIN_ROW_H, MAX_ROW_H].  Override via ``row-height``.
* ``label_w``  — derived from the widest label inside the group;
                 each label type (number/time/icon) has its own estimation
                 formula that depends on ``row_h``.  Override via ``label-width``.

All geometry helpers receive ``props`` — CSS token + per-card override chain
is preserved for every measurement.
"""
from __future__ import annotations

from rendering.atoms.ui.agenda_entry import AgendaEntryAtom

_ATOM = AgendaEntryAtom()

# Row-height guard-rails (px)
_MIN_ROW_H = 44
_MAX_ROW_H = 160

# Padding inside the label column on each side
_LABEL_PAD = 10

# Icon tile fraction of row height
_ICON_TILE_RATIO = 0.65


def _parse_entries(props: dict) -> list[dict]:
    """Extract and normalise the ``entries`` list from props."""
    # items is canonical; entries kept as backward-compat alias
    raw = props.get("items") or props.get("entries") or []
    result: list[dict] = []
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict):
                result.append(item)
            elif isinstance(item, str) and item.strip():
                result.append({"title": item.strip()})
    return result


def _estimate_label_w(label_type: str, label: str, row_h: int) -> int:
    """Return the minimum column width needed for one label at the given row height."""
    lp2 = _LABEL_PAD * 2
    if label_type == "icon":
        tile_s = max(24, int(row_h * _ICON_TILE_RATIO))
        return tile_s + lp2 + 8
    elif label_type == "time":
        # compact bold font — slightly narrower than heading role
        t_sz = max(10, min(int(row_h * 0.24), 16))
        return max(80, int(len(str(label)) * t_sz * 0.65) + lp2)
    else:  # number
        n_sz = max(14, min(int(row_h * 0.50), 36))
        return max(44, int(len(str(label)) * n_sz * 0.65) + lp2)


class AgendaCard:
    """Render a full agenda card with header, entry rows, and optional highlight."""

    def render(
        self, ctx, props: dict, x: int, y: int, w: int, h: int, **_
    ) -> None:

        # ── 1. Card background & border ───────────────────────────────────────
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        # ── 2. Resolve entries ────────────────────────────────────────────────
        entries = _parse_entries(props)
        if not entries:
            return

        # ── 3. Standard card geometry helpers (with props override chain) ─────
        pad        = ctx.card_pad_px(w, h, props)
        inner_w    = w - pad * 2
        header_gap = ctx.card_title_gap(h, props)

        # ── 4. Header section ─────────────────────────────────────────────────
        card_title  = str(props.get("title",  "") or "").strip()
        icon_raw    = str(props.get("icon",   "") or
                          props.get("icon-name", "") or "").strip()
        show_header = bool(card_title or icon_raw) and \
                      ctx.card_section_enabled(props, "title", default=True)
        show_hline  = show_header and \
                      ctx.card_line_enabled(props, "title", default=True)

        title_color = ctx.card_title_color(props, default_token="text-default")
        hline_color = ctx.card_line_color("title", ctx.color("line-default"), props)
        icon_bg     = ctx.icon_bg(props)
        icon_fg     = ctx.icon_fg(props)

        header_h  = ctx.card_title_h(w, h, props)
        icon_sz   = ctx.icon_size(w, h, props) if icon_raw else 0
        icon_sz   = min(icon_sz, header_h)
        icon_r    = ctx.icon_radius(icon_sz, props) if icon_raw else 0

        current_y = y + pad

        if show_header:
            text_w     = inner_w - (icon_sz + header_gap if icon_raw else 0)
            title_sz   = ctx.card_title_font_size(card_title, max(40, text_w), h, props)
            if card_title:
                ctx.text(
                    x + pad, current_y, max(40, text_w), header_h,
                    card_title,
                    size=title_sz, bold=True,
                    color=title_color,
                    align=ctx.card_title_align(props, default="left"),
                    valign="middle",
                )
            if icon_raw:
                ix = x + w - pad - icon_sz
                iy = current_y + max(0, (header_h - icon_sz) // 2)
                ctx.rect(ix, iy, icon_sz, icon_sz,
                         fill=icon_bg, stroke=ctx.icon_stroke(props), radius=icon_r)
                ctx.draw_icon(ix, iy, icon_sz, icon_sz, icon_raw, color=icon_fg)
            current_y += header_h + header_gap

        if show_hline:
            hline_x, hline_w = ctx.card_divider_span("title", x + pad, inner_w, props)
            ctx.divider(hline_x, current_y, hline_w, color=hline_color)
            current_y += max(8, int(h * 0.018))

        # ── 5. Body geometry ──────────────────────────────────────────────────
        body_top    = current_y
        body_bottom = y + h - pad
        body_h      = max(0, body_bottom - body_top)
        n           = len(entries)

        # Row height — responsive: fills body when entries are more,
        # but does NOT stretch when there are few entries.
        row_h_auto  = max(_MIN_ROW_H, body_h // n) if n else _MIN_ROW_H
        row_h_auto  = min(row_h_auto, _MAX_ROW_H)
        row_h_prop  = int(props.get("row-height") or 0)
        row_h       = row_h_prop if row_h_prop > 0 else row_h_auto

        # Label column width — responsive: derived from widest label in the group
        # after row_h is known (font sizes depend on row_h).
        label_w_prop = int(props.get("label-width") or props.get("label_width") or 0)
        if label_w_prop > 0:
            label_w = label_w_prop
        else:
            label_w = max(
                _estimate_label_w(
                    str(e.get("label_type") or e.get("label-type") or "number"),
                    str(e.get("label", "")),
                    row_h,
                )
                for e in entries
            )
            label_w += 4  # small buffer for visual comfort

        # Gap between label column and text column
        gap = max(8, int(row_h * 0.18))

        # ── 6. Entry colour defaults ──────────────────────────────────────────
        show_divs   = ctx._boolish(props.get("show-dividers",
                                             props.get("show_dividers", True)), True)
        _div_color  = (str(props.get("divider-color") or
                           props.get("divider_color") or "").strip()
                       or ctx.card_line_color("title", ctx.color("line-default"), props))
        # ── Agenda color resolution (props → CSS token → semantic fallback) ─
        def _agenda_color(prop_keys: list, css_token: str, fallback: str) -> str:
            for k in prop_keys:
                v = str(props.get(k) or "").strip()
                if v:
                    return v
            return ctx.theme_var(css_token, ctx.color(fallback))

        _label_col  = _agenda_color(["label-color",     "label_color"],     "--color-agenda-label",        "primary")
        _icon_bg    = _agenda_color(["icon-bg",          "icon_bg"],         "--color-agenda-icon-bg",      "primary")
        _icon_fg    = _agenda_color(["icon-fg",          "icon_fg"],         "--color-agenda-icon-fg",      "on-primary")
        _title_col  = _agenda_color(["title-color",      "title_color"],     "--color-agenda-title",        "on-surface")
        _body_col   = _agenda_color(["body-color",       "body_color"],      "--color-agenda-body",         "on-surface-variant")
        _hl_col     = _agenda_color(["highlight-bg",     "highlight_bg"],    "--color-agenda-highlight-bg", "primary-container")

        # ── 7. Render each entry using AgendaEntryAtom ────────────────────────
        for i, entry in enumerate(entries):
            row_y = body_top + i * row_h

            # Do not overflow beyond the card's padded bottom edge
            if row_y + row_h > body_bottom + row_h // 2:
                break   # remaining rows would be clipped — stop gracefully

            # First entry never draws a separator above itself
            first_entry = (i == 0)

            _ATOM.render(
                ctx,
                x=x + pad,
                y=row_y,
                w=inner_w,
                h=row_h,
                label_w=label_w,
                gap=gap,
                label_type=str(
                    entry.get("label_type") or entry.get("label-type") or "number"
                ).strip().lower(),
                label=str(entry.get("label", "") or ""),
                # headline is canonical; title kept as alias
                # body is canonical; description kept as alias
                title=str(entry.get("headline") or entry.get("title") or ""),
                description=str(entry.get("body") or entry.get("description") or ""),
                highlight=bool(entry.get("highlight", False)),
                show_divider=show_divs and not first_entry,
                # Pass resolved colour defaults — atom uses them when no override
                label_color=_label_col,
                icon_bg_color=_icon_bg,
                icon_fg_color=_icon_fg,
                title_color=_title_col,
                body_color=_body_col,
                highlight_color=_hl_col,
                divider_color=_div_color,
            )
