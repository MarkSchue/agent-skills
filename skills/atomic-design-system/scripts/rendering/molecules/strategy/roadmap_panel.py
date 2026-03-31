"""RoadmapPanel — three swim-lane roadmap with vertical connector line"""
from __future__ import annotations


_LANE_FILLS = [
    "primary-container",
    "secondary-container",
    "surface-variant",
]


class RoadmapPanel:
    """Render a multi-lane roadmap panel with coloured item dots connected by a
    vertical line inside each lane card."""

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        lanes = props.get("lanes", []) or []
        if not lanes:
            return

        n       = len(lanes)
        GAP     = ctx.spacing("m")           # gap between lane cards
        OUTER   = ctx.spacing("s")           # outer margin on left/right

        lane_w  = (w - OUTER * 2 - GAP * (n - 1)) // max(n, 1)

        # ── sizes (scaled to lane width so cards never overflow) ──────────
        pad       = max(12, min(20, int(lane_w * 0.07)))   # inner card padding
        dot_d     = max(14, min(20, int(lane_w * 0.065)))  # dot diameter
        dot_r     = dot_d // 2
        line_w    = 2                                       # connector line width
        label_sz  = max(12, ctx.font_size("caption"))      # lane header
        title_sz  = max(11, ctx.font_size("body"))         # item title
        desc_sz   = max(10, ctx.font_size("caption"))      # item description
        label_h   = int(label_sz * 1.5)
        title_h   = int(title_sz * 1.5)
        desc_h    = int(desc_sz  * 1.5)
        item_gap  = ctx.spacing("s")                       # gap between items
        item_h    = title_h + desc_h + item_gap            # height per item slot

        for i, lane in enumerate(lanes):
            if not isinstance(lane, dict):
                continue

            lx   = x + OUTER + i * (lane_w + GAP)
            ly   = y
            fill = ctx.color(_LANE_FILLS[i % len(_LANE_FILLS)])

            # Lane card background
            ctx.rect(lx, ly, lane_w, h,
                     fill=fill, stroke=ctx.color("border-subtle"),
                     radius=ctx.rad())

            # Lane header label
            ctx.text(lx + pad, ly + pad, lane_w - pad * 2, label_h,
                     str(lane.get("label", "")),
                     size=label_sz, bold=True,
                     color=ctx.color("on-surface"),
                     valign="middle")

            # Divider under header
            div_y = ly + pad + label_h + ctx.spacing("xs")
            ctx.divider(lx + pad, div_y, lane_w - pad * 2,
                        color=ctx.color("border-subtle"))

            items = [it for it in (lane.get("items", []) or []) if isinstance(it, dict)]
            if not items:
                continue

            # ── item layout ───────────────────────────────────────────────
            content_top = div_y + ctx.spacing("s")
            dot_x       = lx + pad + dot_r          # centre X of all dots
            text_x      = dot_x + dot_r + ctx.spacing("s")
            text_w      = max(20, lx + lane_w - pad - text_x)

            # Compute centre Y for each dot
            dot_ys = []
            iy = content_top + dot_r          # first dot centre
            for _ in items:
                dot_ys.append(iy)
                iy += item_h

            # Draw vertical connector line (behind all dots)
            if len(dot_ys) >= 2:
                line_x = dot_x - line_w // 2
                ctx.rect(line_x, dot_ys[0], line_w, dot_ys[-1] - dot_ys[0],
                         fill=ctx.color("border-subtle"), stroke=None)

            # Draw each item
            for j, item in enumerate(items):
                if j >= len(dot_ys):
                    break
                cy       = dot_ys[j]
                status   = str(item.get("status", "neutral"))
                dot_c, _ = ctx.status_color(status)

                # Status dot (drawn over the connector line)
                ctx.ellipse(dot_x - dot_r, cy - dot_r,
                            dot_d, dot_d,
                            fill=dot_c,
                            stroke=fill)   # ring in card fill colour hides line segment

                # Item text block (title + description)
                item_top = cy - dot_r
                ctx.text(text_x, item_top, text_w, title_h,
                         str(item.get("text", "")),
                         size=title_sz, bold=True,
                         color=ctx.color("on-surface"),
                         valign="middle")

                desc = str(item.get("description", ""))
                if desc:
                    ctx.text(text_x, item_top + title_h, text_w, desc_h, desc,
                             size=desc_sz, bold=False,
                             color=ctx.color("on-surface-variant"),
                             valign="top")
