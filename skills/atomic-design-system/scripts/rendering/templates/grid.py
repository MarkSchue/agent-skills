"""GridLayout — grid-3 and comparison-2col template renderer.

Renders N equal-width molecule columns spanning the full content area.
    cols=2 → comparison-2col
    cols=3 → grid-3
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from md_parser import Slide  # type: ignore[import]


class GridLayout:
    """N-column card grid. Dispatches each column to a molecule via dispatch_fn."""

    def __init__(self, cols: int) -> None:
        self.cols = cols

    def render(self, ctx, slide: "Slide", blocks: list,
               margin: int, content_y: int, content_h: int,
               width: int, height: int, dispatch_fn) -> None:
        from slide_helpers import _blocks_from_body, _compute_ref_sizes  # type: ignore[import]

        if not blocks:
            blocks = _blocks_from_body(slide)

        cols = self.cols
        if self.cols == 3 and blocks:
            cols = min(4, max(1, len(blocks)))

        card_w = (width - 2 * margin - (cols - 1) * ctx.gutter) // cols
        card_h = content_h

        ctx.ref_sizes = _compute_ref_sizes(ctx, blocks[:cols], slide, card_w, card_h)
        ctx.ref_h = card_h  # all columns same height — consistent within slide
        for i, block in enumerate(blocks[:cols]):
            cx  = margin + i * (card_w + ctx.gutter)
            cy  = content_y
            mol = block.get("molecule") or (
                  slide.molecule_hints[i] if i < len(slide.molecule_hints) else "")
            # Inject the ## heading as "title" prop so molecules can render a
            # proper card header even when the deck author didn't set title:
            block_props = dict(block.get("props", {}))
            if "title" not in block_props and block.get("title"):
                block_props["title"] = block["title"]
            dispatch_fn(ctx, mol, block_props, block.get("body", ""),
                        cx, cy, card_w, card_h, slide, i)
        ctx.ref_h = None  # clear slide reference height
        ctx.ref_sizes = {}  # clear slide font size harmonization


class AsymmetricGridLayout:
    """Multi-column layout with configurable per-column width ratios.

    Pass any number of integer weights — one per column:

        weights=(2, 1)     → two columns, left 2× the width of right  (grid-2-1)
        weights=(1, 2)     → two columns, right 2× the width of left  (grid-1-2)
        weights=(2, 1, 1)  → three columns, first is 2× the other two (grid-2-1-1)
    """

    def __init__(self, weights: tuple[int, ...] = (1, 1)) -> None:
        self.weights = weights

    def render(self, ctx, slide: "Slide", blocks: list,
               margin: int, content_y: int, content_h: int,
               width: int, height: int, dispatch_fn) -> None:
        from slide_helpers import _blocks_from_body, _compute_ref_sizes  # type: ignore[import]

        if not blocks:
            blocks = _blocks_from_body(slide)

        n        = len(self.weights)
        gap      = ctx.content_gap
        cap_pad  = ctx.content_padding
        blk_pad  = ctx.block_padding
        blk_bg   = ctx.block_bg_color

        # Adjust content zone for content-area padding
        cx0      = margin + cap_pad
        cy0      = content_y + cap_pad
        cw       = width - 2 * margin - 2 * cap_pad
        ch_avail = content_h - 2 * cap_pad

        total_w   = sum(self.weights) or n
        avail_w   = cw - gap * (n - 1)

        # Compute each column width from weights, ensure they sum exactly to avail_w
        col_widths: list[int] = []
        for i, wt in enumerate(self.weights):
            if i < n - 1:
                col_widths.append(max(1, int(avail_w * wt / total_w)))
            else:
                col_widths.append(max(1, avail_w - sum(col_widths)))

        card_h = ch_avail - 2 * blk_pad
        rep_card_w = max(1, max(col_widths) - 2 * blk_pad) if col_widths else max(1, avail_w // n - 2 * blk_pad)

        ctx.ref_sizes = _compute_ref_sizes(ctx, blocks[:n], slide, rep_card_w, card_h)
        ctx.ref_h = card_h  # all columns same height — consistent within slide
        for i, col_w in enumerate(col_widths):
            if i >= len(blocks):
                break
            block = blocks[i]
            ox    = cx0 + sum(col_widths[:i]) + i * gap
            oy    = cy0

            # Optional block background
            if blk_bg and blk_bg not in ("transparent", "none", ""):
                ctx.rect(ox, oy, col_w, ch_avail, fill=blk_bg)

            mol = block.get("molecule") or (
                  slide.molecule_hints[i] if i < len(slide.molecule_hints) else "")

            block_props = dict(block.get("props", {}))
            if "title" not in block_props and block.get("title"):
                block_props["title"] = block["title"]

            dispatch_fn(ctx, mol, block_props, block.get("body", ""),
                        ox + blk_pad, oy + blk_pad,
                        col_w - 2 * blk_pad, card_h, slide, i)
        ctx.ref_h = None  # clear slide reference height
        ctx.ref_sizes = {}  # clear slide font size harmonization
