"""ObjectiveCard — OKR objective with key-result progress bars"""
from __future__ import annotations


class ObjectiveCard:
    """Render an OKR objective card with a highlighted objective and key-result progress bars.

    Deck aliases accepted:
        title         → card header (standard)
        quarter       → small badge left of title (optional)
        objective     → highlighted objective statement below the header
        key-results / key_results → list of KRs (strings or dicts)
        progress      → global fallback progress % for all KRs (0-100)

    Per-KR dict keys (when KRs are dicts):
        text          → KR label
        progress      → override %, else falls back to global `progress:` prop
        unit          → suffix (default: global `progress-unit:` or "%")
        color         → token or hex for this KR's bar + ratio

    Per-instance customization:
        text-align        → "left" (default) | "center" | "right" for objective + KR labels
        objective-color   → css token for objective text (default: "primary")
        objective-bg      → false | none to disable objective background; true/unspecified for default theme color; or explicit color token/hex
        ratio-color       → "auto" (default) | css token for all ratio labels
        progress-unit     → default unit suffix (default: "%")
        show-progress     → true (default) | false — hide bar + ratio entirely
        bar-height        → override bar height in px
    """

    def _pct_color(self, ctx, pct: int) -> str:
        if pct >= 80:
            return ctx.theme_var("--color-progress-high", ctx.color("success"))
        if pct >= 40:
            return ctx.theme_var("--color-progress-mid",  ctx.color("warning"))
        return ctx.theme_var("--color-progress-low", ctx.color("error"))

    @staticmethod
    def _normalize_krs(raw_krs, global_pct: int, global_unit: str) -> list[dict]:
        """Normalize KR entries: strings or dicts → list of {text, progress, unit, color}."""
        out = []
        for item in (raw_krs or []):
            if isinstance(item, dict):
                out.append({
                    "text":     str(item.get("text", item.get("label", ""))).strip(),
                    "progress": int(item.get("progress", global_pct)),
                    "unit":     str(item.get("unit", global_unit)),
                    "color":    str(item.get("color", "")).strip(),
                })
            elif isinstance(item, str) and item.strip():
                out.append({
                    "text":     item.strip(),
                    "progress": global_pct,
                    "unit":     global_unit,
                    "color":    "",
                })
        return out

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        card_pad = ctx.card_pad_px(w, h, props)
        inner_w  = w - card_pad * 2

        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        # ── Props ─────────────────────────────────────────────────────────
        title   = str(props.get("title",   ""))
        quarter = str(props.get("quarter", ""))
        obj     = str(props.get("objective", ""))

        # KR aliases: key-results, key_results
        raw_krs = (props.get("key-results")
                   or props.get("key_results")
                   or [])
        if not isinstance(raw_krs, list):
            raw_krs = []

        global_pct  = int(props.get("progress", 0))
        global_unit = str(props.get("progress-unit", props.get("progress_unit", "%")))
        krs         = self._normalize_krs(raw_krs, global_pct, global_unit)[:6]

        text_align        = str(props.get("text-align", props.get("text_align", "left")))
        obj_color_token   = str(props.get("objective-color", props.get("objective_color", "primary")))
        obj_bg_raw        = props.get("objective-bg", props.get("objective_bg", "auto"))
        ratio_color_mode  = str(props.get("ratio-color", props.get("ratio_color", "auto"))).lower()
        show_progress     = str(props.get("show-progress", props.get("show_progress", "true"))).lower() not in ("false", "no", "0")
        bar_h_override    = props.get("bar-height", props.get("bar_height", None))

        # ── Token resolution ──────────────────────────────────────────────
        title_color   = ctx.card_title_color(props, default_token="text-default")
        body_color    = ctx.card_body_color(props, default_token="text-secondary")
        header_align  = ctx.card_header_align(props, default="left")
        divider_color = ctx.card_line_color("header", ctx.color("line-default"), props)
        badge_bg      = ctx.theme_var("--color-objective-badge-bg", ctx.color("primary"))
        badge_fg      = ctx.theme_var("--color-objective-badge-fg", ctx.color("on-primary"))
        bar_track     = ctx.theme_var("--color-progress-bar-track",  ctx.color("surface-variant"))
        obj_color     = ctx.color(obj_color_token)

        # Determine objective strip background (allow disableing)
        if isinstance(obj_bg_raw, str) and obj_bg_raw.strip().lower() in ("none", "false", "transparent", "auto"):
            objective_bg = None
        elif obj_bg_raw is True:
            objective_bg = ctx.theme_var("--color-objective-strip-bg", ctx.color("primary-container"))
        elif obj_bg_raw:
            objective_bg = (ctx.color(obj_bg_raw) if not str(obj_bg_raw).strip().startswith("#") else str(obj_bg_raw).strip())
        else:
            objective_bg = None if obj_bg_raw in (None, "") else ctx.theme_var("--color-objective-strip-bg", ctx.color("primary-container"))

        GAP_XS = ctx.spacing("xs")
        GAP_S  = ctx.spacing("s")
        GAP_M  = max(10, int(h * 0.022))

        # ── Standard header ───────────────────────────────────────────────
        show_header      = bool(title or quarter) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)
        header_h         = ctx.card_header_h(w, h, props)
        header_gap       = ctx.card_header_gap(h, props)

        oy = y + card_pad

        if show_header:
            badge_w   = 0
            badge_gap = 0
            if quarter:
                q_sz    = ctx.font_size("caption")
                badge_h = max(18, int(q_sz * 1.8))
                badge_w = max(44, int(ctx.estimate_text_width(quarter, q_sz, bold=True))
                              + ctx.spacing("m") * 2)
                badge_gap = GAP_S
                badge_y = oy + max(0, (header_h - badge_h) // 2)
                ctx.badge(x + card_pad, badge_y, badge_w, badge_h, quarter,
                          fill=badge_bg, text_color=badge_fg,
                          size=q_sz, radius=ctx.rad())

            title_x = x + card_pad + badge_w + badge_gap
            title_w = max(40, inner_w - badge_w - badge_gap)
            if title:
                title_sz = ctx.card_header_font_size(title, title_w, h, props)
                ctx.text(title_x, oy, title_w, header_h, title,
                         size=title_sz, bold=True,
                         color=title_color,
                         align=header_align, valign="middle", inner_margin=0)
            oy += header_h + header_gap

        if show_header_line:
            line_x, line_w = ctx.card_divider_span("header", x + card_pad, inner_w, props)
            ctx.divider(line_x, oy, line_w, color=divider_color)
            oy += GAP_M

        # ── Objective callout block ───────────────────────────────────────
        # Budget: use up to 35% of remaining height for the objective, or
        # a minimum of 2 lines of heading-sub text.
        remaining   = y + h - oy - card_pad
        obj_max_h   = max(int(remaining * 0.38), int(ctx.font_size("heading-sub") * 3.2))
        obj_h       = 0
        if obj and ctx.card_section_enabled(props, "objective", default=True):
            obj_sz  = ctx.fit_text_size(
                obj, inner_w,
                max_size=ctx.font_size("heading-sub"),
                min_size=ctx.font_size("body"),
                bold=True, safety=0.88,
            )
            # Estimate lines to size the box
            avg_chars = max(1, int(inner_w / max(1, obj_sz * 0.55)))
            n_lines   = max(1, -(-len(obj) // avg_chars))   # ceiling div
            line_h    = int(obj_sz * 1.45)
            obj_h     = min(obj_max_h, max(int(line_h * 1.1), n_lines * line_h + GAP_S))

            # Optional tinted background strip (toggle via objective-bg)
            strip_pad = max(4, int(h * 0.008))
            if objective_bg:
                ctx.rect(x + card_pad, oy, inner_w, obj_h,
                         fill=objective_bg,
                         radius=max(4, ctx.rad() // 2))

            ctx.text(x + card_pad + strip_pad, oy + strip_pad,
                     inner_w - strip_pad * 2, obj_h - strip_pad * 2,
                     obj, size=obj_sz, bold=True,
                     color=obj_color,
                     align=text_align, valign="middle", inner_margin=0)
            oy += obj_h + GAP_M

        # ── Key-result rows ───────────────────────────────────────────────
        if not krs:
            return

        n_krs      = len(krs)
        kr_gap     = max(GAP_S, int(h * 0.015))
        avail_h    = max(0, y + h - oy - card_pad - kr_gap * (n_krs - 1))
        kr_slot_h  = max(28, avail_h // max(n_krs, 1))

        # Bar height: token → prop override
        bar_h = int(bar_h_override) if bar_h_override is not None \
            else max(6, min(14, kr_slot_h // 5))

        label_h = max(16, kr_slot_h - bar_h - GAP_XS)
        kr_sz   = ctx.fit_text_size(
            "Sample KR text",
            inner_w,
            max_size=ctx.font_size("body"),
            min_size=ctx.font_size("caption"),
            bold=False, safety=0.90,
        )
        ratio_w = max(44, int(inner_w * 0.14))
        text_w  = inner_w - ratio_w - GAP_S

        ky = oy
        for kr in krs:
            text  = kr["text"]
            pct   = kr["progress"]
            unit  = kr["unit"]
            label = f"{pct}{unit}"

            # Color resolution
            if kr["color"]:
                raw = kr["color"]
                pct_c = raw if raw.startswith("#") else ctx.color(raw)
            elif ratio_color_mode != "auto":
                pct_c = ctx.color(ratio_color_mode)
            else:
                pct_c = self._pct_color(ctx, pct)

            # KR label
            ctx.text(x + card_pad, ky, text_w, label_h, text,
                     size=kr_sz,
                     color=body_color,
                     align=text_align, valign="middle", inner_margin=0)

            # Ratio (only when show-progress)
            if show_progress:
                ctx.text(x + card_pad + text_w + GAP_S, ky,
                         ratio_w, label_h, label,
                         size=kr_sz, bold=True,
                         color=pct_c, align="right", valign="middle", inner_margin=0)

            # Progress bar
            if show_progress:
                bar_y = ky + label_h
                bar_r = bar_h // 2
                ctx.rect(x + card_pad, bar_y, inner_w, bar_h,
                         fill=bar_track, radius=bar_r)
                fill_w = max(bar_h, int(inner_w * pct / 100))
                ctx.rect(x + card_pad, bar_y, fill_w, bar_h,
                         fill=pct_c, radius=bar_r)

            ky += kr_slot_h + kr_gap
            if ky > y + h - card_pad:
                break
