"""ObjectiveCard — OKR objective with key-result progress bars"""
from __future__ import annotations


class ObjectiveCard:
    """Render an OKR objective card with key-result progress bars.

    Follows the same token-driven header/divider/body pattern as all other cards.
    All colors, alignment, and section-visibility props are respected.

    Per-KR customization (inside each key-results list item):
        unit  : string appended to the value (default comes from global progress-unit or "%")
                e.g.  unit: " PD"  →  "68 PD"
        color : optional color token or hex for this KR's ratio label + bar

    Global prop overrides:
        ratio-color    : "auto" (default, uses progress thresholds) | CSS color token
        progress-unit  : default unit for all KRs (fallback when per-KR unit not set)
    """

    def _pct_color(self, ctx, pct: int) -> str:
        """Return the appropriate progress color, respecting CSS token overrides."""
        if pct >= 80:
            return ctx.theme_var("--color-progress-high", ctx.color("success"))
        if pct >= 40:
            return ctx.theme_var("--color-progress-mid",  ctx.color("warning"))
        return ctx.theme_var("--color-progress-low", ctx.color("error"))

    def render(self, ctx, props: dict, x: int, y: int, w: int, h: int,
               **_) -> None:
        # Centralized padding + header height for consistent baseline alignment
        card_pad = ctx.card_pad_px(w, h, props)
        inner_w  = w - card_pad * 2

        # ── Card frame ────────────────────────────────────────────────────
        ctx.rect(x, y, w, h,
                 fill=ctx.card_bg_color(props, "bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad())

        quarter = str(props.get("quarter", ""))
        obj     = str(props.get("objective", ""))
        krs     = (props.get("key-results") or [])[:5]

        show_header      = bool(quarter or obj) and ctx.card_section_enabled(props, "header", default=True)
        show_header_line = show_header and ctx.card_line_enabled(props, "header", default=True)

        # ── Token resolution (standard card contract) ─────────────────────
        title_color   = ctx.card_title_color(props, default_token="text-default")
        header_align  = ctx.card_header_align(props, default="left")
        divider_color = ctx.card_line_color("header", ctx.color("line-default"), props)
        badge_bg      = ctx.theme_var("--color-objective-badge-bg", ctx.color("primary"))
        badge_fg      = ctx.theme_var("--color-objective-badge-fg", ctx.color("on-primary"))
        bar_track     = ctx.theme_var("--color-progress-bar-track",  ctx.color("surface-variant"))

        # Global ratio-color: "auto" uses _pct_color(pct), else resolve as color token
        ratio_color_mode = str(props.get("ratio-color", "auto")).strip().lower()
        global_unit      = str(props.get("progress-unit", "%"))

        GAP_XS = ctx.spacing("xs")   # 4
        GAP_S  = ctx.spacing("s")    # 8
        GAP_M  = max(12, int(h * 0.024))  # responsive, matches ChartCard post-divider

        # Centralized header height so divider lines are aligned across all cards.
        header_h   = ctx.card_header_h(w, h, props)
        header_gap = ctx.card_header_gap(h, props)

        oy = y + card_pad

        # ── Header row: quarter badge (left) + objective title (right) ────
        # Both rendered inline within header_h — mirrors MissionCard's
        # icon-right / title-left pattern, just with badge on the left.
        if show_header:
            qbadge_h = min(header_h - 4, max(20, min(28, int(h * 0.048))))
            badge_w  = max(60, len(quarter) * 9 + 20) if quarter else 0
            badge_gap = GAP_S if quarter else 0

            # Quarter badge — vertically centred in header_h
            if quarter:
                badge_y = oy + max(0, (header_h - qbadge_h) // 2)
                ctx.badge(x + card_pad, badge_y, badge_w, qbadge_h, quarter,
                          fill=badge_bg, text_color=badge_fg)

            # Objective title — fills the remaining width beside the badge
            title_x = x + card_pad + badge_w + badge_gap
            title_w = max(40, inner_w - badge_w - badge_gap)
            obj_sz = ctx.card_header_font_size(obj, title_w, h, props)
            if obj:
                ctx.text(title_x, oy, title_w, header_h, obj,
                         size=obj_sz, bold=True,
                         color=title_color,
                         align=header_align, valign="middle")

            oy += header_h + header_gap

        # ── Header divider ────────────────────────────────────────────────
        if show_header_line:
            line_x, line_w = ctx.card_divider_span("header", x + card_pad, inner_w, props)
            ctx.divider(line_x, oy, line_w, color=divider_color)
            oy += GAP_M

        # ── Key-result rows ───────────────────────────────────────────────
        n_krs      = max(len(krs), 1)
        kr_row_gap = GAP_S   # ctx.spacing("s") = 8 px between KR rows
        kr_area_h  = y + h - oy - card_pad - kr_row_gap * (n_krs - 1)
        kr_slot_h  = max(36, min(80, kr_area_h // n_krs))
        bar_h      = max(4, min(10, kr_slot_h // 7))
        label_h    = kr_slot_h - bar_h - GAP_XS

        kr_sz   = min(ctx.font_size("body"), max(ctx.font_size("caption"), int(kr_slot_h * 0.35)))
        ratio_w = max(52, int(inner_w * 0.13))
        text_w  = inner_w - ratio_w - GAP_S

        ky = oy
        for kr in krs:
            if not isinstance(kr, dict):
                continue

            text  = str(kr.get("text", ""))
            pct   = int(kr.get("progress", 0))
            unit  = str(kr.get("unit", global_unit))
            label = f"{pct}{unit}"

            # Resolve color: per-KR override > global ratio-color > auto
            kr_color_raw = str(kr.get("color", "")).strip()
            if kr_color_raw:
                pct_c = ctx.color(kr_color_raw) if not kr_color_raw.startswith("#") else kr_color_raw
            elif ratio_color_mode != "auto":
                pct_c = ctx.color(ratio_color_mode)
            else:
                pct_c = self._pct_color(ctx, pct)

            # KR text label
            ctx.text(x + card_pad, ky, text_w, label_h, text,
                     size=kr_sz,
                     color=ctx.card_body_color(props, default_token="on-surface-variant"),
                     align="left", valign="middle")

            # Ratio label (68%, 84 PD, …)
            ctx.text(x + card_pad + text_w + GAP_S, ky, ratio_w, label_h, label,
                     size=kr_sz, bold=True,
                     color=pct_c, align="right", valign="middle")

            # Progress bar
            bar_y  = ky + label_h
            bar_r  = bar_h // 2
            ctx.rect(x + card_pad, bar_y, inner_w, bar_h,
                     fill=bar_track, radius=bar_r)
            fill_w = max(bar_h, inner_w * pct // 100)
            ctx.rect(x + card_pad, bar_y, fill_w, bar_h,
                     fill=pct_c, radius=bar_r)

            ky += kr_slot_h + kr_row_gap
            if ky > y + h - card_pad:
                break
