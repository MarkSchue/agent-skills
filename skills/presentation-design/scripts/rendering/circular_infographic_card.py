"""
CircularInfographicCardRenderer — Concentric ring infographic with two
rings (inner + outer). Each ring is divided into N equal angular segments
in distinct colours. Optionally a single segment per ring can be marked
``highlighted: true`` to bump it slightly outward and draw the eye.

Content schema::

    type: circular-infographic-card
    content:
      inner_ring:
        segments:
          - { label: "Strategy",  color: "#000099" }
          - { label: "People",    color: "#3F4DC9" }
          - { label: "Process",   color: "#7A87E0", highlighted: true }
          - { label: "Tech",      color: "#A8B1ED" }
      outer_ring:
        style: donut    # or "arrow" for chevron-tipped segments
        segments:
          - { label: "Discover" }
          - { label: "Define"   }
          - { label: "Design"   }
          - { label: "Develop"  }
          - { label: "Deploy", highlighted: true }
          - { label: "Operate"  }

Tokens (variant prefix ``card-circular-infographic-``):
    outer-radius-pct (0..1 of min(box.w, box.h)/2),
    inner-radius-pct (0..1; inner ring outer radius),
    inner-hole-pct   (0..1; inner ring inner radius / inner ring outer radius),
    ring-gap         (px between inner and outer rings),
    highlight-bump   (px; how much a highlighted segment bulges out),
    segment-stroke-color, segment-stroke-width,
    label-font-size, label-font-color, label-font-weight,
    palette          (semicolon-separated hex list, used when a segment has no `color`).
"""

from __future__ import annotations

from typing import Any

from scripts.models.deck import CardModel
from scripts.parsing.inline_markdown import text_and_runs
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class CircularInfographicCardRenderer(BaseCardRenderer):
    """Renderer for ``circular-infographic-card`` type."""

    variant = "card--circular-infographic"

    def _tok(self, name: str, default: Any = None) -> Any:
        return self._resolve_tok("circular-infographic", name, default)

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        content = card.content if isinstance(card.content, dict) else {}
        inner_def = content.get("inner_ring") or {}
        outer_def = content.get("outer_ring") or {}
        inner_segs = list(inner_def.get("segments") or [])
        outer_segs = list(outer_def.get("segments") or [])
        if not inner_segs and not outer_segs:
            return

        # ── Tokens ────────────────────────────────────────────────────
        outer_r_pct  = float(self._tok("outer-radius-pct") or 0.95)
        inner_r_pct  = float(self._tok("inner-radius-pct") or 0.55)
        inner_hole   = float(self._tok("inner-hole-pct")   or 0.35)
        ring_gap     = float(self._tok("ring-gap") or 6)
        bump         = float(self._tok("highlight-bump") or 14)
        seg_stroke   = self._tok("segment-stroke-color") or "#FFFFFF"
        seg_sw       = float(self._tok("segment-stroke-width") or 2)
        lbl_size     = float(self._tok("label-font-size") or 11)
        lbl_color    = self._tok("label-font-color") or self.resolve("color-text-on-primary") or "#FFFFFF"
        lbl_weight   = self._tok("label-font-weight") or "bold"

        primary = self.resolve("color-primary") or "#000099"
        palette_raw = self._tok("palette") or (
            f"{primary};#3F4DC9;#7A87E0;#A8B1ED;#5A67E0;#2533B0;#A0A8E5;#1F2A8A"
        )
        palette = [c.strip() for c in str(palette_raw).split(";") if c.strip()]

        # ── Geometry ──────────────────────────────────────────────────
        cx = box.x + box.w / 2
        cy = box.y + box.h / 2
        max_r = min(box.w, box.h) / 2 - 4
        outer_ro = max_r * outer_r_pct
        inner_ro = max_r * inner_r_pct
        outer_ri = inner_ro + ring_gap
        inner_ri = inner_ro * inner_hole

        def _color_for(seg: dict, idx: int) -> str:
            return str(seg.get("color") or palette[idx % len(palette)])

        def _emit_ring(
            segs: list[dict],
            ri: float, ro: float,
            *,
            style: str = "donut",
        ) -> None:
            if not segs:
                return
            n = len(segs)
            sweep = 360.0 / n
            # Start at top (-90°), go CW
            for i, seg in enumerate(segs):
                start = -90.0 + i * sweep
                end   = start + sweep
                color = _color_for(seg, i)
                hi = bool(seg.get("highlighted"))
                ro_eff = ro + (bump if hi else 0)
                # We always emit a donut-slice. The "arrow" style adds a
                # small radial chevron tip via a separate triangle element
                # (TODO: native arrow shape). For now, both styles look
                # identical except a highlighted segment in arrow style
                # gets the bump (which is plenty of visual emphasis).
                box.add({
                    "type": "arc",
                    "cx": cx, "cy": cy,
                    "outer_radius": ro_eff,
                    "inner_radius": ri,
                    "start_angle": start,
                    "end_angle":   end,
                    "fill": color,
                    "stroke": seg_stroke,
                    "stroke_width": seg_sw,
                })

                # Label centred along the segment's mid-angle, on the
                # mid-radius. Skip if the segment is too narrow.
                label = str(seg.get("label", "") or "")
                if not label or sweep < 12:
                    continue
                import math
                mid_angle = math.radians((start + end) / 2)
                mid_r = (ri + ro_eff) / 2
                tx = cx + mid_r * math.cos(mid_angle)
                ty = cy + mid_r * math.sin(mid_angle)
                # Estimate label size and centre it on (tx, ty)
                lbl_w = max(40.0, len(label) * lbl_size * 0.6)
                lbl_h = lbl_size + 4
                box.add({
                    "type": "text",
                    "x": tx - lbl_w / 2,
                    "y": ty - lbl_h / 2,
                    "w": lbl_w,
                    "h": lbl_h,
                    **text_and_runs(label),
                    "font_size": lbl_size,
                    "font_color": lbl_color,
                    "font_weight": lbl_weight,
                    "alignment": "center",
                    "vertical_align": "middle",
                })

        outer_style = str(outer_def.get("style") or "donut").lower()
        inner_style = str(inner_def.get("style") or "donut").lower()

        # Outer ring first (drawn underneath).  With adj3=0 these are solid pies
        # from the centre out to outer_ro, so they cover the whole disc area.
        _emit_ring(outer_segs, outer_ri, outer_ro, style=outer_style)

        # White mask ring covering the interior up to outer_ri — creates the visual
        # gap between the outer and inner rings.  The inner ring arcs are then drawn
        # on top of this, so they appear as a distinct inner ring.
        if outer_ri > 0:
            slide_bg = self.resolve("color-background") or "#FFFFFF"
            box.add({
                "type": "ellipse",
                "x": cx - outer_ri,
                "y": cy - outer_ri,
                "w": outer_ri * 2,
                "h": outer_ri * 2,
                "fill": slide_bg,
                "stroke": "none",
                "stroke_width": 0,
            })

        _emit_ring(inner_segs, inner_ri, inner_ro, style=inner_style)

        # Center mask ellipse — creates the inner hole in PPTX (blockArc adj3
        # does not reliably hollow out the shape). In drawio this is harmless
        # since arcs already render hollow via arcWidth.
        if inner_ri > 0:
            slide_bg = self.resolve("color-background") or "#FFFFFF"
            box.add({
                "type": "ellipse",
                "x": cx - inner_ri,
                "y": cy - inner_ri,
                "w": inner_ri * 2,
                "h": inner_ri * 2,
                "fill": slide_bg,
                "stroke": "none",
                "stroke_width": 0,
            })
