"""GridRowLayout — grid-row-2-2 and grid-row-3-2 template renderers.

Renders a grid of cols × rows cells. Blocks are placed in row-major order
(left-to-right, top-to-bottom).
    cols=2, rows=2  → grid-row-2-2  (2×2 equal cells)
    cols=3, rows=2  → grid-row-3-2  (3 columns, 2 rows, equal cells)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from md_parser import Slide  # type: ignore[import]


class GridRowLayout:
    """cols × rows content grid.  Dispatches each cell to a molecule via dispatch_fn."""

    def __init__(self, cols: int = 2, rows: int = 2) -> None:
        self.cols = cols
        self.rows = rows

    def render(self, ctx, slide: "Slide", blocks: list,
               margin: int, content_y: int, content_h: int,
               width: int, height: int, dispatch_fn) -> None:
        from slide_helpers import _blocks_from_body, _compute_ref_sizes  # type: ignore[import]

        if not blocks:
            blocks = _blocks_from_body(slide)

        cols     = self.cols
        rows     = self.rows
        gap      = ctx.content_gap
        cap_pad  = ctx.content_padding
        blk_pad  = ctx.block_padding
        blk_bg   = ctx.block_bg_color

        # Adjust content zone for content-area padding
        cx0      = margin + cap_pad
        cy0      = content_y + cap_pad
        cw       = width - 2 * margin - 2 * cap_pad
        ch_avail = content_h - 2 * cap_pad

        cell_w = (cw - gap * (cols - 1)) // cols
        cell_h = (ch_avail - gap * (rows - 1)) // rows
        card_rw = max(1, cell_w - 2 * blk_pad)
        card_rh = max(1, cell_h - 2 * blk_pad)

        ctx.ref_sizes = _compute_ref_sizes(ctx, blocks[:cols * rows], slide, card_rw, card_rh)
        ctx.ref_h = cell_h  # harmonise sizing — all cells equal height, scale to cell
        for idx, block in enumerate(blocks[:cols * rows]):
            row_i = idx // cols
            col_i = idx % cols

            ox = cx0 + col_i * (cell_w + gap)
            oy = cy0 + row_i * (cell_h + gap)

            # Optional block background
            if blk_bg and blk_bg not in ("transparent", "none", ""):
                ctx.rect(ox, oy, cell_w, cell_h, fill=blk_bg)

            rx  = ox + blk_pad
            ry  = oy + blk_pad
            rw  = cell_w - 2 * blk_pad
            rh  = cell_h - 2 * blk_pad

            mol = block.get("molecule") or (
                  slide.molecule_hints[idx] if idx < len(slide.molecule_hints) else "")

            block_props = dict(block.get("props", {}))
            if "title" not in block_props and block.get("title"):
                block_props["title"] = block["title"]

            dispatch_fn(ctx, mol, block_props, block.get("body", ""),
                        rx, ry, rw, rh, slide, idx)

        ctx.ref_h = None  # clear slide reference height
        ctx.ref_sizes = {}  # clear slide font size harmonization
