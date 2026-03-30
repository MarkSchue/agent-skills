"""NumberedListLayout — numbered-list template renderer.

Renders a vertical list of numbered items with circular numbered badges.

Two modes:
  • **Card-block mode** (preferred): when the slide contains `### card blocks`,
    each block is dispatched to its molecule renderer. A circular number badge
    sits to the left of each card. Items fill the available content area
    evenly, capped at 140 px height each.
  • **Legacy text mode** (backward compat): reads lines matching `1. text`
    from ``slide.body_paragraphs`` and renders them as plain text rows with
    a number badge.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from md_parser import Slide  # type: ignore[import]


class NumberedListLayout:
    """Full-slide numbered list with circular numbered badges per item."""

    def render(self, ctx, slide: "Slide", blocks: list,
               margin: int, content_y: int, content_h: int,
               width: int, height: int, dispatch_fn) -> None:
        x = margin
        y = content_y + ctx.spacing("m")
        w = width - 2 * margin
        h = content_h - ctx.spacing("m")

        badge_d   = 44  # badge circle diameter
        badge_gap = ctx.spacing("m")  # gap between badge right edge and card

        # ── Card-block mode ───────────────────────────────────────────────
        real_blocks = [b for b in blocks if b.get("molecule")]
        if real_blocks:
            n        = len(real_blocks)
            item_gap = ctx.spacing("s")
            item_h   = min(140, (h - item_gap * (n - 1)) // max(n, 1))
            card_x   = x + badge_d + badge_gap
            card_w   = w - badge_d - badge_gap

            for i, block in enumerate(real_blocks):
                iy      = y + i * (item_h + item_gap)
                badge_y = iy + (item_h - badge_d) // 2
                # Number badge
                ctx.rect(x, badge_y, badge_d, badge_d,
                         fill=ctx.color("primary"), radius=badge_d // 2)
                ctx.text(x, badge_y, badge_d, badge_d, str(i + 1),
                         size=20, bold=True, color=ctx.color("text-on-filled"),
                         align="center", valign="middle")
                # Molecule card
                dispatch_fn(
                    ctx,
                    block.get("molecule", ""),
                    block.get("props") or {},
                    block.get("body", ""),
                    card_x, iy, card_w, item_h,
                    slide, i,
                )
                if iy + item_h > y + h:
                    break
            return

        # ── Legacy text mode ──────────────────────────────────────────────
        items = []
        for para in slide.body_paragraphs:
            for line in para.splitlines():
                if re.match(r"^\d+\.", line.strip()):
                    items.append(line.strip())
        if not items:
            return

        item_h = min(140, (h - 16) // max(len(items), 1))
        for i, item_text in enumerate(items):
            text = re.sub(r"^\d+\.\s*", "", item_text)
            text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
            iy       = y + i * item_h
            iy_inner = iy + (item_h - badge_d) // 2
            ctx.rect(x, iy_inner, badge_d, badge_d,
                     fill=ctx.color("primary"), radius=badge_d // 2)
            ctx.text(x, iy_inner, badge_d, badge_d, str(i + 1),
                     size=20, bold=True, color=ctx.color("text-on-filled"),
                     align="center", valign="middle")
            ctx.text(x + badge_d + badge_gap, iy_inner, w - badge_d - badge_gap,
                     badge_d, text,
                     size=16, color=ctx.color("text-default"),
                     align="left", valign="middle")
            if iy + item_h > y + h:
                break
