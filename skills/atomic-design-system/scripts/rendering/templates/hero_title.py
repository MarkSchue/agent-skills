"""HeroTitleLayout — hero-title (default) template renderer.

Full-bleed slide with:
  - 8 px primary brand stripe at top
  - Geometry-aware decorative element bottom-right
      radius-large >= 32  (e.g. Liquid Glass) → dual concentric ellipses
      radius-large >= 20  (e.g. Material)     → single organic ellipse
      radius-large <  20  (e.g. Carbon)       → sharp filled rectangle
  - Body content: free text, single molecule, or multi-molecule row
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from md_parser import Slide  # type: ignore[import]


class HeroTitleLayout:
    """Full-bleed hero slide with brand stripe and geometry-adaptive decoration."""

    def render(self, ctx, slide: "Slide", blocks: list,
               margin: int, content_y: int, content_h: int,
               width: int, height: int, dispatch_fn) -> None:
        from slide_helpers import _merge_block_props  # type: ignore[import]

        # -- Brand stripe -------------------------------------------------------
        ctx.rect(0, 0, width, 8, fill=ctx.color("primary"))

        # -- Geometry-adaptive decoration (bottom-right) -----------------------
        # Keep decoration minimal on content-rich slides to avoid visual artifacts.
        has_molecules = bool(slide.molecule_hints)
        if not has_molecules:
            _deco_r = ctx.rad("radius-large")
            if _deco_r >= 32:
                # Liquid Glass: two concentric circles — outer glass pane + inner accent
                ctx.ellipse(width - 460, height - 440, 350, 350,
                            fill=ctx.color("primary-container"))
                ctx.ellipse(width - 370, height - 390, 200, 200,
                            fill=ctx.color("primary"))
            elif _deco_r >= 20:
                # Material: single organic ellipse
                ctx.ellipse(width - 340, height - 340, 300, 300,
                            fill=ctx.color("primary-container"))
            else:
                # Carbon: sharp geometric rectangle
                ctx.rect(width - 280, height - 280, 240, 240,
                         fill=ctx.color("primary-container"), radius=_deco_r)
        # When molecules are present: no decoration at all — avoids phantom shapes

        # -- Body content ------------------------------------------------------
        mols = slide.molecule_hints
        n    = len(mols)

        if n == 0:
            # Plain text body
            body = "\n".join(slide.body_paragraphs)
            ctx.text(margin, content_y + ctx.spacing("m"),
                     width - 2 * margin, content_h // 2, body,
                     size=ctx.font_size("heading-sub"), color=ctx.color("text-default"),
                     align="left", valign="top")

        elif n == 1:
            # Single molecule spanning full content width
            props = _merge_block_props(blocks) if blocks else {}
            body  = "\n".join(slide.body_paragraphs)
            dispatch_fn(ctx, mols[0], props, body,
                        margin, content_y + ctx.spacing("m"),
                        width - 2 * margin, content_h - ctx.spacing("m"), slide, 0)

        else:
            # Multi-molecule row — equal widths
            mol_w = (width - 2 * margin - (n - 1) * ctx.gutter) // n
            for i, mol in enumerate(mols):
                mx    = margin + i * (mol_w + ctx.gutter)
                props = blocks[i].get("props", {}) if i < len(blocks) else {}
                body  = blocks[i].get("body",  "")  if i < len(blocks) else ""
                dispatch_fn(ctx, mol, props, body,
                            mx, content_y + ctx.spacing("m"), mol_w,
                            content_h - ctx.spacing("m"), slide, i)
