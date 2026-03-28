"""DataInsightLayout — data-insight template renderer.

Chart present  →  58 / 42 split: chart-card (left) + first block (right)
No chart       →  blocks dispatched individually:
                   • 1 block  → full-width
                   • 2 blocks → 58 / 42 split (first left, second right)
                   • 3+       → first left, remaining stacked on right
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from md_parser import Slide  # type: ignore[import]

from rendering.molecules import MOLECULE_REGISTRY  # type: ignore[import]


class DataInsightLayout:
    """Flexible data + insight split layout."""

    def render(self, ctx, slide: "Slide", blocks: list,
               margin: int, content_y: int, content_h: int,
               width: int, height: int, dispatch_fn) -> None:
        from slide_helpers import _blocks_from_body, _extract_section_blocks  # type: ignore[import]

        cy      = content_y + ctx.spacing("m")
        avail_h = content_h - ctx.spacing("m")
        inner_w = width - 2 * margin

        # ── Chart present: original 58/42 chart + first block ─────────────────
        if slide.chart_blocks:
            chart_w = int(inner_w * 0.58)
            right_w = inner_w - chart_w - ctx.gutter
            rx      = margin + chart_w + ctx.gutter

            chart      = slide.chart_blocks[0]
            chart_data = dict(chart.data)
            if not chart_data.get("title"):
                chart_data["title"] = slide.title

            MOLECULE_REGISTRY["chart-card"].render(
                ctx, chart.chart_type, chart_data,
                margin, cy, chart_w, avail_h)

            # Use section blocks if available, otherwise body
            right_blocks = blocks or _extract_section_blocks(slide) or _blocks_from_body(slide)
            if right_blocks:
                b = right_blocks[0]
                dispatch_fn(ctx, b["molecule"], b["props"], b["body"],
                            rx, cy, right_w, avail_h, slide, 0)
            return

        # ── No chart: dispatch section blocks individually ─────────────────────
        if not blocks:
            blocks = _extract_section_blocks(slide) or _blocks_from_body(slide)

        if not blocks:
            return

        if len(blocks) == 1:
            # Single block → full width
            b = blocks[0]
            dispatch_fn(ctx, b["molecule"], b["props"], b["body"],
                        margin, cy, inner_w, avail_h, slide, 0)

        elif len(blocks) == 2:
            # Two blocks → 58 / 42 horizontal split
            left_w  = int(inner_w * 0.58)
            right_w = inner_w - left_w - ctx.gutter
            rx      = margin + left_w + ctx.gutter

            b0, b1 = blocks[0], blocks[1]
            dispatch_fn(ctx, b0["molecule"], b0["props"], b0["body"],
                        margin, cy, left_w, avail_h, slide, 0)
            dispatch_fn(ctx, b1["molecule"], b1["props"], b1["body"],
                        rx, cy, right_w, avail_h, slide, 1)

        else:
            # 3+ blocks → first block left (58%), rest stacked on right (42%)
            left_w   = int(inner_w * 0.58)
            right_w  = inner_w - left_w - ctx.gutter
            rx       = margin + left_w + ctx.gutter
            right_bk = blocks[1:]
            stack_h  = max(20, avail_h // len(right_bk))

            b0 = blocks[0]
            dispatch_fn(ctx, b0["molecule"], b0["props"], b0["body"],
                        margin, cy, left_w, avail_h, slide, 0)

            for i, b in enumerate(right_bk):
                by = cy + i * stack_h
                dispatch_fn(ctx, b["molecule"], b["props"], b["body"],
                            rx, by, right_w, stack_h - ctx.gutter, slide, i + 1)
