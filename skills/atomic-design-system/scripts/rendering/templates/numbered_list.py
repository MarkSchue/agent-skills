"""NumberedListLayout — numbered-list template renderer.

Renders a vertical list of numbered items with circular badge labels.
Item height is evenly distributed across the available content area
(capped at 140 px to stay readable on shorter canvases).
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
            iy_inner = iy + (item_h - 44) // 2
            ctx.rect(x, iy_inner, 44, 44,
                     fill=ctx.color("primary"), radius=22)
            ctx.text(x, iy_inner, 44, 44, str(i + 1),
                     size=20, bold=True, color=ctx.color("text-on-filled"),
                     align="center", valign="middle")
            ctx.text(x + 56, iy_inner, w - 56, 44, text,
                     size=16, color=ctx.color("text-default"),
                     align="left", valign="middle")
            if iy + item_h > y + h:
                break
