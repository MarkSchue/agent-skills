"""RoadmapPanel — three swim-lane roadmap with vertical connector line"""
from __future__ import annotations


class RoadmapPanel:
    """Render a multi-lane roadmap panel with coloured item dots connected by a
    vertical line inside each lane card.

    Per-card overrides (all optional)
    ───────────────────────────────────
      title              : card header title
      lanes              : list of lane objects  (or use now/next/later shorthands)
      now / next / later : string-list shorthands mapped to lane labels
      text-align         : left | center | right for lane labels + items  default: left
      label-color        : token for lane label text                       default: on-surface
      item-color         : token for item title text                       default: on-surface
      desc-color         : token for description text                      default: on-surface-variant
      dot-color          : token for item dot fill                         default: primary
      line-color         : token for connector line                        default: border-subtle
      show-header        : bool — show card title header                   default: true (if title set)
      show-header-line   : bool — divider below card title                 default: true
      lane-gap           : px gap between lane cards                       default: spacing("m")
    """

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        lanes = list(props.get("lanes") or [])

        # ── Normalise now/next/later shorthand into lanes list ─────────────
        if not lanes:
            for key, label in [("now", "Now"), ("next", "Next"), ("later", "Later")]:
                raw = props.get(key) or []
                if raw:
                    items = []
                    for entry in raw:
                        if isinstance(entry, dict):
                            items.append(entry)
                        elif isinstance(entry, str) and entry.strip():
                            items.append({"text": entry.strip()})
                    if items:
                        lanes.append({"label": label, "items": items})
        if not lanes:
            return

        n = len(lanes)

        # ── Card contract ─────────────────────────────────────────────────
        pad        = ctx.card_pad_px(w, h, props)
        inner_w    = w - pad * 2
        card_title = str(props.get("title", "")).strip()
        show_header      = bool(card_title) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)
        title_color  = ctx.card_title_color(props, default_token="text-default")
        header_align = ctx.card_header_align(props, default="left")
        div_color    = ctx.card_line_color("header", ctx.color("line-default"), props)
        text_align   = str(props.get("text-align", "left")).strip().lower()
        if text_align not in ("left", "center", "right"):
            text_align = "left"

        # Token helpers — all overridable via props
        label_color_token = str(props.get("label-color", "on-surface")).strip()
        item_color_token  = str(props.get("item-color",  "on-surface")).strip()
        desc_color_token  = str(props.get("desc-color",  "on-surface-variant")).strip()
        dot_color_token   = str(props.get("dot-color",   "primary")).strip()
        line_color_token  = str(props.get("line-color",  "border-subtle")).strip()

        # ── Card outer frame ──────────────────────────────────────────────
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        GAP_XS = ctx.spacing("xs")
        GAP_S  = ctx.spacing("s")
        GAP_M  = ctx.spacing("m")

        cy = y + pad

        # ── Standard card header ──────────────────────────────────────────
        if show_header:
            header_h   = ctx.card_header_h(w, h, props)
            header_gap = ctx.card_header_gap(h, props)
            title_sz   = ctx.card_header_font_size(card_title, inner_w, h, props)
            ctx.text(x + pad, cy, inner_w, header_h,
                     card_title, size=title_sz, bold=True,
                     color=title_color, align=header_align, valign="middle",
                     inner_margin=0)
            cy += header_h + header_gap
            if show_header_line:
                lx, lw = ctx.card_divider_span("header", x + pad, inner_w, props)
                ctx.divider(lx, cy, lw, color=div_color)
                cy += 1 + GAP_M

        # ── Lane geometry ─────────────────────────────────────────────────
        raw_lane_gap = props.get("lane-gap", "")
        try:
            lane_gap = max(0, int(raw_lane_gap))
        except (ValueError, TypeError):
            lane_gap = GAP_M

        lane_w      = max(20, (inner_w - lane_gap * (n - 1)) // n)
        lanes_top   = cy
        lanes_h     = max(20, y + h - pad - lanes_top)

        # Lane label font = same scale as card header for visual consistency
        # Use "heading-sub" as category title tone, capped to title_sz
        label_ref     = card_title if card_title else "Now"
        label_sz_full = ctx.card_header_font_size(label_ref, lane_w - pad * 2, h, props)
        label_sz      = label_sz_full  # same size as card title
        label_h       = max(int(label_sz * 1.4), ctx.card_header_h(lane_w, lanes_h, props))
        label_gap     = GAP_M          # breathing room between lane label divider and first item

        # ── Max items across all lanes → shared vertical grid ─────────────
        all_items = []
        for lane in lanes:
            if not isinstance(lane, dict):
                continue
            items = [it for it in (lane.get("items") or []) if isinstance(it, dict)]
            all_items.append(items)

        max_items   = max((len(its) for its in all_items), default=1)
        content_top = lanes_top + label_h + GAP_S + 1 + label_gap   # below label divider
        content_h   = max(20, y + h - pad - content_top)

        # dot / text sizing
        dot_d  = max(12, min(18, int(lane_w * 0.06)))
        dot_r  = dot_d // 2
        line_w_px = 2
        title_sz  = max(ctx.font_size("caption"), min(ctx.font_size("body"), int(lane_w * 0.08)))
        desc_sz   = ctx.font_size("annotation")

        # Slot height: divide content_h equally by max_items so columns align
        slot_h = max(dot_d * 2, content_h // max(max_items, 1))

        # ── Draw each lane ─────────────────────────────────────────────────
        for i, lane in enumerate(lanes):
            if not isinstance(lane, dict):
                continue

            lx    = x + pad + i * (lane_w + lane_gap)
            items = all_items[i]

            # Lane sub-card background (subtle tint per lane, always readable)
            lane_fill_tokens = ["primary-container", "secondary-container", "surface-variant"]
            lane_bg   = ctx.color(lane_fill_tokens[i % len(lane_fill_tokens)])
            ctx.rect(lx, lanes_top, lane_w, lanes_h,
                     fill=lane_bg,
                     stroke=ctx.color("border-subtle"),
                     radius=ctx.rad())

            # Lane label (same font size as card title)
            label_text = str(lane.get("label", ""))
            ctx.text(lx + pad, lanes_top + (label_h - int(label_sz * 1.2)) // 2,
                     lane_w - pad * 2, int(label_sz * 1.2),
                     label_text,
                     size=label_sz, bold=True,
                     color=ctx.color(label_color_token),
                     align=text_align, valign="middle", inner_margin=0)

            # Divider below lane label
            div_y_lane = lanes_top + label_h + GAP_S
            ctx.divider(lx + pad, div_y_lane, lane_w - pad * 2,
                        color=ctx.color(line_color_token))

            if not items:
                continue

            # Dot centre X
            dot_cx  = lx + pad + dot_r
            text_x  = dot_cx + dot_r + GAP_S
            text_w  = max(20, lx + lane_w - pad - text_x)

            # Compute dot Y positions using shared slot height
            dot_ys = []
            for j in range(len(items)):
                slot_center = content_top + j * slot_h + slot_h // 2
                dot_ys.append(slot_center)

            # Vertical connector line (behind dots)
            if len(dot_ys) >= 2:
                lx_line = dot_cx - line_w_px // 2
                ctx.rect(lx_line, dot_ys[0], line_w_px, dot_ys[-1] - dot_ys[0],
                         fill=ctx.color(line_color_token), stroke=None)

            # Items
            for j, item in enumerate(items):
                if j >= len(dot_ys):
                    break
                cy_dot = dot_ys[j]

                # Status dot
                status = str(item.get("status", "neutral"))
                dot_c, _ = ctx.status_color(status)
                if dot_c == ctx.color("neutral"):
                    dot_c = ctx.color(dot_color_token)
                ctx.ellipse(dot_cx - dot_r, cy_dot - dot_r,
                            dot_d, dot_d,
                            fill=dot_c,
                            stroke=lane_bg)

                # Title + description centred on dot
                item_top = cy_dot - dot_r
                item_avail = slot_h - dot_d
                t_h = max(int(title_sz * 1.4), dot_d)
                d_h = max(int(desc_sz * 1.4), 0)

                ctx.text(text_x, item_top, text_w, t_h,
                         str(item.get("text", "")),
                         size=title_sz, bold=True,
                         color=ctx.color(item_color_token),
                         align=text_align, valign="middle", inner_margin=0)

                desc = str(item.get("description", ""))
                if desc and item_avail > d_h:
                    ctx.text(text_x, item_top + t_h, text_w, d_h, desc,
                             size=desc_sz, bold=False,
                             color=ctx.color(desc_color_token),
                             align=text_align, valign="top", inner_margin=0)
