"""Resolved style tokens for a single compare-card render."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from scripts.rendering.compare_card._data import is_false, is_true

if TYPE_CHECKING:
    from scripts.rendering.compare_card._renderer import CompareCardRenderer


@dataclass(slots=True)
class CompareStyle:
    """All resolved style tokens for one compare-card render pass.

    Built once per ``render_body`` call via :meth:`resolve` so the actual
    rendering code reads cleanly without hundreds of inline ``self._tok(...)``
    invocations.
    """

    # Header row
    header_h: float
    header_bg: str
    header_fg: str
    header_size: float
    header_weight: str
    header_style: str
    header_align: str
    hl_header_bg: str
    hl_header_fg: str
    hl_col_bg: str

    # Topic / label column
    topic_visible: bool
    topic_col_pct: float
    topic_col_bg: str
    topic_col_header_bg: str
    topic_col_header_fg: str
    topic_size: float
    topic_color: str
    topic_weight: str
    topic_style: str
    topic_align: str

    # Topic badge / marker
    topic_marker: str
    topic_badge_shape: str
    topic_badge_color: str
    topic_badge_size: float
    topic_badge_fs: float
    topic_badge_fc: str
    topic_badge_gap: float

    # Body cells
    cell_size: float
    cell_color: str
    cell_weight: str
    cell_style: str
    cell_align: str
    cell_bg: str
    cell_icon_size: float
    cell_icon_color: str
    pad_x: float
    pad_y: float

    # Row geometry
    row_h_tok: Any
    row_min_h: float

    # Stripes / separators / border
    stripe_visible: bool
    stripe_color: str
    row_sep_visible: bool
    row_sep_color: str
    row_sep_width: float
    col_sep_visible: bool
    col_sep_color: str
    col_sep_width: float
    grid_bdr_visible: bool
    grid_bdr_color: str
    grid_bdr_width: float

    # Summary row
    has_summary: bool
    summ_h: float
    summ_bg: str
    summ_fg: str
    summ_size: float
    summ_weight: str
    summ_style: str
    summ_align: str
    summ_hl_bg: str
    summ_hl_fg: str

    # Misc
    icon_font_family: str

    @classmethod
    def resolve(
        cls,
        r: "CompareCardRenderer",
        topic_visible_raw: Any,
        topic_width_pct_raw: Any,
        has_summary_explicit: bool,
    ) -> "CompareStyle":
        """Resolve every compare-card token via the renderer's chain."""
        tok = r._tok
        rsv = r.resolve

        # Topic visibility — content overrides CSS token
        if topic_visible_raw is not None:
            topic_visible = not is_false(topic_visible_raw)
        else:
            tv = tok("label-col-visible")
            topic_visible = not is_false(tv) if tv is not None else True

        # Summary visibility — explicit (content.summary present) wins, else CSS
        if has_summary_explicit:
            has_summary = True
        else:
            sv = tok("summary-visible")
            has_summary = is_true(sv) if sv is not None else False

        hl_col_bg_raw = tok("highlight-col-bg-color")
        cell_bg_tok = tok("body-bg-color")

        return cls(
            # Header
            header_h=float(tok("heading-height", 28)),
            header_bg=str(tok("heading-bg-color") or rsv("color-primary") or "#1A1A2E"),
            header_fg=str(tok("heading-font-color") or rsv("color-text-inverse") or "#FFFFFF"),
            header_size=float(tok("heading-font-size", 9)),
            header_weight=str(tok("heading-font-weight") or "700"),
            header_style=str(tok("heading-font-style") or "normal"),
            header_align=str(tok("heading-alignment") or "center"),
            hl_header_bg=str(tok("highlight-col-heading-bg-color") or rsv("color-accent") or "#3B82F6"),
            hl_header_fg=str(tok("highlight-col-heading-font-color") or "#FFFFFF"),
            hl_col_bg=str(hl_col_bg_raw) if hl_col_bg_raw else "",

            # Topic / label column
            topic_visible=topic_visible,
            topic_col_pct=float(topic_width_pct_raw or tok("label-col-width-pct", 25)) / 100,
            topic_col_bg=str(tok("label-col-bg-color") or rsv("color-surface-sunken") or "#F3F4F6"),
            topic_col_header_bg=str(tok("label-col-heading-bg-color")
                                    or tok("heading-bg-color")
                                    or rsv("color-primary") or "#1A1A2E"),
            topic_col_header_fg=str(tok("label-col-heading-font-color")
                                    or tok("heading-font-color")
                                    or rsv("color-text-inverse") or "#FFFFFF"),
            topic_size=float(tok("label-font-size", 11)),
            topic_color=str(tok("label-font-color") or rsv("color-text-default") or "#1F2937"),
            topic_weight=str(tok("label-font-weight") or "700"),
            topic_style=str(tok("label-font-style") or "normal"),
            topic_align=str(tok("label-alignment") or "left"),

            # Badge
            topic_marker=str(tok("label-marker") or "none").lower(),
            topic_badge_shape=str(tok("label-badge-shape") or "circle").lower(),
            topic_badge_color=str(tok("label-badge-color") or rsv("color-accent") or "#3B82F6"),
            topic_badge_size=float(tok("label-badge-size", 18)),
            topic_badge_fs=float(tok("label-badge-font-size", 8)),
            topic_badge_fc=str(tok("label-badge-font-color") or "#FFFFFF"),
            topic_badge_gap=float(tok("label-badge-gap", 6)),

            # Body cells
            cell_size=float(tok("body-font-size", 11)),
            cell_color=str(tok("body-font-color") or rsv("color-text-subtle") or "#374151"),
            cell_weight=str(tok("body-font-weight") or "400"),
            cell_style=str(tok("body-font-style") or "normal"),
            cell_align=str(tok("body-alignment") or "center"),
            cell_bg=str(cell_bg_tok) if cell_bg_tok else "",
            cell_icon_size=float(tok("body-icon-size", 14)),
            cell_icon_color=str(tok("body-icon-color") or rsv("color-text-default") or "#374151"),
            pad_x=float(tok("body-padding-x", 6)),
            pad_y=float(tok("body-padding-y", 4)),

            # Row geometry
            row_h_tok=tok("row-height"),
            row_min_h=float(tok("row-min-height", 24)),

            # Stripes / separators
            stripe_visible=is_true(tok("row-stripe-visible")) if tok("row-stripe-visible") is not None else False,
            stripe_color=str(tok("row-stripe-color") or rsv("color-surface-sunken") or "#F3F4F6"),
            row_sep_visible=(not is_false(tok("row-separator-visible"))) if tok("row-separator-visible") is not None else True,
            row_sep_color=str(tok("row-separator-color") or rsv("color-border") or "#E5E7EB"),
            row_sep_width=float(tok("row-separator-width", 1)),
            col_sep_visible=(not is_false(tok("col-separator-visible"))) if tok("col-separator-visible") is not None else True,
            col_sep_color=str(tok("col-separator-color") or rsv("color-border") or "#E5E7EB"),
            col_sep_width=float(tok("col-separator-width", 1)),
            grid_bdr_visible=(not is_false(tok("grid-border-visible"))) if tok("grid-border-visible") is not None else True,
            grid_bdr_color=str(tok("grid-border-color") or rsv("color-border") or "#E5E7EB"),
            grid_bdr_width=float(tok("grid-border-width", 1)),

            # Summary
            has_summary=has_summary,
            summ_h=float(tok("summary-height", 32)),
            summ_bg=str(tok("summary-bg-color") or rsv("color-primary") or "#1A1A2E"),
            summ_fg=str(tok("summary-font-color") or rsv("color-text-inverse") or "#FFFFFF"),
            summ_size=float(tok("summary-font-size", 11)),
            summ_weight=str(tok("summary-font-weight") or "700"),
            summ_style=str(tok("summary-font-style") or "normal"),
            summ_align=str(tok("summary-alignment") or "center"),
            summ_hl_bg=str(tok("summary-highlight-bg-color") or rsv("color-accent") or "#3B82F6"),
            summ_hl_fg=str(tok("summary-highlight-font-color") or "#FFFFFF"),

            icon_font_family=str(rsv("icon-font-family") or "Material Symbols Outlined"),
        )
