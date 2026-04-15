"""
ScopeCardRenderer — Renders a project scope overview as a grid of visual tiles.

Each tile displays one scope item with:
  - A status-coloured circular badge (number / checkmark / custom icon)
  - A bold item heading (right of the badge)
  - Optional body text in muted text (below the badge row)

Grid configuration:
  ``content.layout_columns``          — per-card column override (int, 1–4)
  ``--card-scope-columns``            — default column count (CSS token, default 2)
  Rows are computed automatically: ``ceil(len(items) / n_cols)``

Marker types (``--card-scope-item-marker``):
  ``number``  — sequential 1-based number inside a filled circle (default)
  ``check``   — checkmark icon inside a filled circle; icon name from
                ``--card-scope-check-icon-name`` (default "check")
  ``icon``    — per-item ``icon`` field used as the icon name inside the badge;
                falls back to ``--card-scope-check-icon-name`` when no per-item
                icon is supplied

Status colours (badge fill per item ``status`` field):
  ``in-scope``     → ``--card-scope-status-in-scope-color``    (default: color-accent)
  ``out-of-scope`` → ``--card-scope-status-out-of-scope-color`` (default: color-text-muted)
  ``conditional``  → ``--card-scope-status-conditional-color`` (default: color-warning)
  (unset)          → in-scope colour

YAML content structure::

    content:
      layout_columns: 2          # optional — overrides CSS token
      items:
        - heading: "Data Migration"
          body: "Move all legacy records to the new platform."
          status: in-scope        # in-scope | out-of-scope | conditional
          icon: "storage"         # Material Symbols name (used when marker=icon)
        - heading: "Reporting"
          status: conditional

All visual properties are controlled by CSS tokens on ``.card--scope``.
"""

from __future__ import annotations

import math

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox


class ScopeCardRenderer(BaseCardRenderer):
    """Renderer for ``scope-card`` type."""

    variant = "card--scope"

    # ── Helpers ──────────────────────────────────────────────────────────

    def _tok(self, name: str, default: object = None) -> object:
        """Resolve ``card-scope-{name}`` with automatic fallback to ``card-{name}``."""
        return self._resolve_tok("scope", name, default)

    def _status_badge_color(self, status: str | None) -> str:
        """Return the resolved badge fill colour for *status*."""
        s = (status or "").strip().lower()
        if s == "out-of-scope":
            return str(
                self._tok("status-out-of-scope-color")
                or self.resolve("color-text-muted")
                or "#9CA3AF"
            )
        if s == "conditional":
            return str(
                self._tok("status-conditional-color")
                or self.resolve("color-warning")
                or "#F59E0B"
            )
        # default: in-scope
        return str(
            self._tok("status-in-scope-color")
            or self.resolve("color-accent")
            or "#3B82F6"
        )

    # ── Body rendering ────────────────────────────────────────────────────

    def render_body(self, card: CardModel, box: RenderBox) -> None:  # noqa: C901
        """Render scope items as a grid of visual tiles into *box*."""
        content = card.content if isinstance(card.content, dict) else {}
        raw_items: list = content.get("items", [])

        if not raw_items:
            return

        # Normalise items to dicts
        items: list[dict] = []
        for entry in raw_items:
            if isinstance(entry, dict):
                items.append(entry)
            else:
                items.append({"heading": str(entry)})

        # ── Grid geometry ──────────────────────────────────────────────
        # content.layout_columns takes priority over CSS token
        n_cols = int(content.get("layout_columns") or self._tok("columns", 2))
        n_cols = max(1, min(4, n_cols))
        n_rows = math.ceil(len(items) / n_cols)

        gap = float(self._tok("item-gap", 12))
        tile_w = (box.w - gap * (n_cols - 1)) / n_cols
        tile_h = max(1.0, (box.h - gap * (n_rows - 1)) / n_rows)

        # ── Tile style tokens ──────────────────────────────────────────
        tile_bg = str(self._tok("item-bg-color") or "transparent")
        tile_border_color = str(
            self._tok("item-border-color") or self.resolve("color-border") or "#E5E7EB"
        )
        tile_border_width_raw = self._tok("item-border-width")
        tile_border_width = float(tile_border_width_raw) if tile_border_width_raw is not None else 1
        tile_border_radius = float(self._tok("item-border-radius") or 4)
        tile_padding = float(self._tok("item-padding") or 12)
        tile_border_stroke = "none" if tile_border_width <= 0 else tile_border_color

        # ── Badge tokens ───────────────────────────────────────────────
        badge_size = float(self._tok("badge-size") or 20)
        badge_font_size = float(self._tok("badge-font-size") or 9)
        # badge_font_color is a constant white — intentionally hardcoded as it
        # represents "text on a coloured background"; no semantic token exists for this.
        badge_font_color = str(self._tok("badge-font-color") or "#FFFFFF")
        badge_gap = float(self._tok("badge-gap") or 8)

        # ── Marker mode ────────────────────────────────────────────────
        marker_type = str(self._tok("item-marker") or "number").lower()
        check_icon_name = str(self._tok("check-icon-name") or "check")
        icon_font_family = str(
            self.resolve("icon-font-family") or "Material Symbols Outlined"
        )

        # ── Item heading tokens ────────────────────────────────────────────
        h_size = float(self._tok("heading-font-size") or 11)
        h_color = str(
            self._tok("heading-font-color")
            or self.resolve("color-text-default")
            or "#1F2937"
        )
        h_weight = str(self._tok("heading-font-weight") or "700")
        h_lh = h_size * float(self._tok("heading-line-height") or 1.2)

        # ── Item body text tokens ─────────────────────────────────────────
        body_size = float(self._tok("body-font-size") or 9)
        body_color = str(
            self._tok("body-font-color")
            or self.resolve("color-text-muted")
            or "#9CA3AF"
        )
        body_weight = str(self._tok("body-font-weight") or "400")
        body_margin_top = float(self._tok("body-margin-top") or 4)
        body_lh = body_size * 1.3

        # ── Status label tokens (optional small tag at tile bottom-right) ─
        status_label_vis_raw = self._tok("status-label-visible")
        status_label_visible = status_label_vis_raw in (True, "true", "True")
        status_label_size = float(self._tok("status-label-font-size") or 8)

        # ── Render tiles ───────────────────────────────────────────────
        for i, item in enumerate(items):
            col = i % n_cols
            row = i // n_cols

            tx = box.x + col * (tile_w + gap)
            ty = box.y + row * (tile_h + gap)

            # Tile background
            box.add(
                {
                    "type": "rect",
                    "x": tx,
                    "y": ty,
                    "w": tile_w,
                    "h": tile_h,
                    "fill": tile_bg,
                    "stroke": tile_border_stroke,
                    "stroke_width": tile_border_width,
                    "rx": tile_border_radius,
                }
            )

            # Content area inside tile padding
            cx = tx + tile_padding
            cy = ty + tile_padding
            cw = tile_w - 2 * tile_padding

            # ── Badge circle ───────────────────────────────────────────
            badge_color = self._status_badge_color(item.get("status"))
            bx = cx
            by = cy

            box.add(
                {
                    "type": "ellipse",
                    "x": bx,
                    "y": by,
                    "w": badge_size,
                    "h": badge_size,
                    "fill": badge_color,
                    "stroke": "none",
                    "stroke_width": 0,
                }
            )

            # Badge interior: number, checkmark, or per-item icon
            if marker_type == "number":
                box.add(
                    {
                        "type": "text",
                        "x": bx,
                        "y": by,
                        "w": badge_size,
                        "h": badge_size,
                        "text": str(i + 1),
                        "font_size": badge_font_size,
                        "font_color": badge_font_color,
                        "font_weight": "700",
                        "alignment": "center",
                        "vertical_align": "middle",
                        "wrap": False,
                    }
                )
            else:
                # "check" uses check_icon_name for every item.
                # "icon"  prefers the per-item ``icon`` field, falls back to check_icon_name.
                if marker_type == "icon":
                    icon_name = str(item.get("icon") or check_icon_name)
                else:
                    icon_name = check_icon_name

                box.add(
                    {
                        "type": "icon",
                        "x": bx,
                        "y": by,
                        "w": badge_size,
                        "h": badge_size,
                        "name": icon_name,
                        "font_family": icon_font_family,
                        "font_size": badge_size * 0.65,
                        "color": badge_font_color,
                    }
                )

            # ── Heading text (right of badge) ──────────────────────────
            text_x = cx + badge_size + badge_gap
            text_w = max(1.0, cw - badge_size - badge_gap)
            badge_row_h = max(h_size, badge_size)
            heading_text = str(item.get("heading") or "")

            if heading_text:
                box.add(
                    {
                        "type": "text",
                        "x": text_x,
                        "y": by,
                        "w": text_w,
                        "h": badge_row_h,
                        "text": heading_text,
                        "font_size": h_size,
                        "font_color": h_color,
                        "font_weight": h_weight,
                        "alignment": "left",
                        "vertical_align": "middle",
                        "line_height": h_lh,
                        "wrap": True,
                    }
                )

            # ── Body text (below the badge row) ────────────────────────
            body_text = str(item.get("body") or item.get("description") or "")
            if body_text:
                body_y = by + badge_row_h + body_margin_top
                # Available height below body text start, up to tile bottom padding
                avail_body_h = ty + tile_h - tile_padding - body_y
                if avail_body_h > body_size:
                    box.add(
                        {
                            "type": "text",
                            "x": cx,
                            "y": body_y,
                            "w": cw,
                            "h": max(body_size, avail_body_h),
                            "text": body_text,
                            "font_size": body_size,
                            "font_color": body_color,
                            "font_weight": body_weight,
                            "alignment": "left",
                            "line_height": body_lh,
                            "wrap": True,
                        }
                    )

            # ── Optional status label (bottom-right of tile) ───────────
            if status_label_visible:
                status_val = str(item.get("status") or "in-scope")
                status_label_color = self._status_badge_color(item.get("status"))
                label_y = ty + tile_h - tile_padding - status_label_size
                if label_y > ty + tile_padding:
                    box.add(
                        {
                            "type": "text",
                            "x": cx,
                            "y": label_y,
                            "w": cw,
                            "h": status_label_size,
                            "text": status_val,
                            "font_size": status_label_size,
                            "font_color": status_label_color,
                            "font_weight": "400",
                            "alignment": "right",
                            "wrap": False,
                        }
                    )
