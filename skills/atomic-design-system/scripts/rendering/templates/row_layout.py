"""RowLayout — row-2, row-3, row-2-1, row-1-2 template renderers.

Renders N stacked rows spanning the full content width.
    rows=2                → row-2     (two equal-height rows)
    rows=3                → row-3     (three equal-height rows)
    row_weights=(2, 1)    → row-2-1   (top row is twice the height of the bottom)
    row_weights=(1, 2)    → row-1-2   (bottom row is twice the height of the top)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from md_parser import Slide  # type: ignore[import]


class RowLayout:
    """N-row content layout.  Dispatches each row to a molecule via dispatch_fn."""

    def __init__(self, rows: int = 2,
                 row_weights: tuple[int, ...] | None = None) -> None:
        self.rows = rows
        # Normalise weights: use equal weights when not specified
        if row_weights is not None:
            self.weights = tuple(row_weights)
        else:
            self.weights = tuple(1 for _ in range(rows))

    def render(self, ctx, slide: "Slide", blocks: list,
               margin: int, content_y: int, content_h: int,
               width: int, height: int, dispatch_fn) -> None:
        from slide_helpers import _blocks_from_body  # type: ignore[import]

        if not blocks:
            blocks = _blocks_from_body(slide)

        rows        = max(len(self.weights), 1)
        gap         = ctx.content_gap
        cap_pad     = ctx.content_padding
        blk_pad     = ctx.block_padding
        blk_bg      = ctx.block_bg_color

        # Adjust content zone for content-area padding
        cx0      = margin + cap_pad
        cy0      = content_y + cap_pad
        cw       = width - 2 * margin - 2 * cap_pad
        ch_avail = content_h - 2 * cap_pad

        total_weight = sum(self.weights) or rows
        # unit_h is the height of a weight-1 row, consistent across all row
        # layouts with the same total_weight so that weight-1 rows (e.g. the
        # bottom row in row-2-1 and every row in row-3) start at the same
        # absolute Y and produce identical divider positions cross-slide.
        #   ch_avail = unit_h * total_weight + (total_weight - 1) * gap
        #   → unit_h = (ch_avail - (total_weight - 1) * gap) / total_weight
        # A weight-w row spans w units plus (w-1) gutters that it absorbs.
        unit_h      = (ch_avail - (total_weight - 1) * gap) / total_weight
        row_heights = [
            max(1, int(unit_h * w + (w - 1) * gap))
            for w in self.weights
        ]
        # Correct rounding error on the last row
        between_rows_gap = gap * (rows - 1)
        assigned = sum(row_heights[:-1]) + between_rows_gap
        row_heights[-1] = max(1, ch_avail - assigned)

        card_w   = cw - 2 * blk_pad
        cursor_y = cy0

        # Use the smallest row card height as ref_h so the header zone is
        # proportional to the compact rows. Tall rows get the same small header,
        # leaving more body space — matching visual rhythm across row layouts.
        min_card_h = min(max(1, rh - 2 * blk_pad) for rh in row_heights)
        ctx.ref_h = min_card_h  # harmonise header sizing across all rows in this slide
        for i, row_h in enumerate(row_heights):
            if i >= len(blocks):
                break
            block = blocks[i]
            rx    = cx0 + blk_pad
            ry    = cursor_y + blk_pad
            rh    = row_h - 2 * blk_pad

            # Optional block background
            if blk_bg and blk_bg not in ("transparent", "none", ""):
                ctx.rect(cx0, cursor_y, cw, row_h, fill=blk_bg)

            mol = block.get("molecule") or (
                  slide.molecule_hints[i] if i < len(slide.molecule_hints) else "")

            block_props = dict(block.get("props", {}))
            if "title" not in block_props and block.get("title"):
                block_props["title"] = block["title"]

            dispatch_fn(ctx, mol, block_props, block.get("body", ""),
                        rx, ry, card_w, rh, slide, i)

            cursor_y += row_h + gap

        ctx.ref_h = None  # clear slide reference height
