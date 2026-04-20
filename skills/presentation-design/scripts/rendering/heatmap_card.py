"""
HeatmapCardRenderer — Renders a cluster-based heat-map overview card.

Each cluster (e.g. HR, Information Technology) is rendered as a bordered container
with a filled heading bar and a grid of coloured fact tiles inside.  Every fact tile
is coloured according to its ``level`` (0–5) using the deck-global
``--color-heat-{level}`` and ``--color-on-heat-{level}`` tokens defined in
``.theme-colors``.

Cluster layout:

    ┌──────────────────────────────┐
    │█████ Cluster Name ████████████│   ← filled heading bar (cluster-heading-bg)
    │  ┌──────┐ ┌──────┐ ┌──────┐  │
    │  │ Fact │ │ Fact │ │ Fact │  │   ← fact tiles (coloured by level)
    │  └──────┘ └──────┘ └──────┘  │
    │  ┌──────┐ ┌──────┐           │
    │  │ Fact │ │ Fact │           │
    │  └──────┘ └──────┘           │
    └──────────────────────────────┘

Grid configuration:

    ``content.cluster_columns``   — per-card override for number of cluster columns
    ``content.fact_columns``      — per-card override for fact columns inside every cluster
    ``content.page``              — 1-based page index for pagination (default 1)
    ``--card-heatmap-cluster-columns``  — CSS default (4)
    ``--card-heatmap-fact-columns``     — CSS default (3)

Cluster sizing:
    All clusters are rendered at the **same height**, computed from the cluster with
    the largest number of facts.  Cluster width is derived uniformly from available
    card-body width divided by the column count.

Pagination:
    ``clusters_per_page = n_cluster_cols × n_cluster_rows_that_fit``
    The page-1 offset selects the first window; page-2 selects the second, etc.

Heat level colours::

    level 0 → --color-heat-0 / --color-on-heat-0  (gray — not applicable)
    level 1 → --color-heat-1 / --color-on-heat-1  (green — low)
    level 2 → --color-heat-2 / --color-on-heat-2  (lime  — low-medium)
    level 3 → --color-heat-3 / --color-on-heat-3  (yellow — medium)
    level 4 → --color-heat-4 / --color-on-heat-4  (orange — high)
    level 5 → --color-heat-5 / --color-on-heat-5  (red   — critical)

YAML content structure::

    content:
      cluster_columns: 4          # optional — overrides CSS token
      fact_columns: 3             # optional — overrides CSS token
      page: 1                     # optional — 1-based page index
      clusters:
        - name: "HR"
          facts:
            - text: "ERP Suite"
              level: 3
            - text: "Payroll Global"
              level: 4
        - name: "Information Technology"
          facts:
            - text: "Jira"
              level: 1

All visual properties are controlled by CSS tokens on ``.card--heatmap``.
"""

from __future__ import annotations

import math

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox

# Fallback heat colours (used when theme tokens are not resolved)
_HEAT_BG_FALLBACKS = {
    0: "#E5E7EB",
    1: "#22C55E",
    2: "#84CC16",
    3: "#EAB308",
    4: "#F97316",
    5: "#EF4444",
}
_HEAT_FG_FALLBACKS = {
    0: "#1A1A2E",
    1: "#1A1A2E",
    2: "#1A1A2E",
    3: "#1A1A2E",
    4: "#FFFFFF",
    5: "#FFFFFF",
}


class HeatmapCardRenderer(BaseCardRenderer):
    """Renderer for ``heatmap-card`` type."""

    variant = "card--heatmap"

    # ── Helpers ──────────────────────────────────────────────────────────

    def _tok(self, name: str, default: object = None) -> object:
        """Resolve ``card-heatmap-{name}`` with automatic fallback to ``card-{name}``."""
        return self._resolve_tok("heatmap", name, default)

    def _heat_colors(self, level: int) -> tuple[str, str]:
        """Return ``(background, text)`` colour pair for the given heat *level* (0–5)."""
        lvl = max(0, min(5, int(level)))
        bg_token = f"color-heat-{lvl}"
        fg_token = f"color-on-heat-{lvl}"
        bg = str(self.resolve(bg_token) or _HEAT_BG_FALLBACKS[lvl])
        fg = str(self.resolve(fg_token) or _HEAT_FG_FALLBACKS[lvl])
        return bg, fg

    # ── Body rendering ────────────────────────────────────────────────────

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        """Render cluster grid with heat-map fact tiles into *box*."""
        content = card.content if isinstance(card.content, dict) else {}
        raw_clusters: list = content.get("clusters", [])

        if not raw_clusters:
            return

        # ── Normalise cluster list ─────────────────────────────────────
        clusters: list[dict] = []
        for entry in raw_clusters:
            if isinstance(entry, dict):
                clusters.append(entry)
            else:
                clusters.append({"name": str(entry), "facts": []})

        # Normalise facts inside each cluster
        for cluster in clusters:
            raw_facts = cluster.get("facts") or []
            norm_facts: list[dict] = []
            for f in raw_facts:
                if isinstance(f, dict):
                    norm_facts.append(f)
                else:
                    norm_facts.append({"text": str(f), "level": 0})
            cluster["facts"] = norm_facts

        # ── Grid configuration ─────────────────────────────────────────
        n_cluster_cols = int(
            content.get("cluster_columns")
            or self._tok("cluster-columns", 4)
        )
        n_cluster_cols = max(1, n_cluster_cols)

        n_fact_cols = int(
            content.get("fact_columns")
            or self._tok("fact-columns", 3)
        )
        n_fact_cols = max(1, n_fact_cols)

        page = int(content.get("page") or self._tok("page", 1))
        page = max(1, page)

        # ── Spacing / size tokens ──────────────────────────────────────
        cluster_gap = float(self._tok("cluster-gap", 12))
        cluster_padding = float(self._tok("cluster-padding", 6))
        cluster_border_width = float(self._tok("cluster-border-width", 1))
        cluster_border_color = str(
            self._tok("cluster-border-color")
            or self.resolve("color-border-strong")
            or "#9CA3AF"
        )
        cluster_border_radius = float(self._tok("cluster-border-radius", 4))
        cluster_border_stroke = (
            "none" if cluster_border_width <= 0 else cluster_border_color
        )

        heading_height = float(self._tok("cluster-heading-height", 22))
        heading_bg = str(
            self._tok("cluster-heading-bg")
            or self.resolve("color-primary")
            or "#1A1A2E"
        )
        heading_font_color = str(
            self._tok("cluster-heading-font-color")
            or self.resolve("color-on-primary")
            or "#FFFFFF"
        )
        heading_font_size = float(self._tok("cluster-heading-font-size", 11))
        heading_font_weight = str(self._tok("cluster-heading-font-weight", "700"))
        heading_alignment = str(self._tok("cluster-heading-alignment", "left"))
        heading_padding = float(self._tok("cluster-heading-padding", 6))

        fact_gap = float(self._tok("fact-gap", 3))
        fact_height = float(self._tok("fact-height", 36))
        fact_border_radius = float(self._tok("fact-border-radius", 2))
        fact_padding = float(self._tok("fact-padding", 3))
        fact_font_size = float(self._tok("fact-font-size", 9))
        fact_font_weight = str(self._tok("fact-font-weight", "400"))
        fact_text_align = str(self._tok("fact-text-alignment", "center"))

        # ── Legend tokens ──────────────────────────────────────────────
        legend_vis_raw = self._tok("legend-visible", True)
        legend_visible = legend_vis_raw not in (False, "false", "False")
        legend_height = float(self._tok("legend-height", 18))
        legend_margin_bottom = float(self._tok("legend-margin-bottom", 8))
        legend_swatch_size = float(self._tok("legend-swatch-size", 12))
        legend_swatch_radius = float(self._tok("legend-swatch-radius", 2))
        legend_swatch_gap = float(self._tok("legend-swatch-gap", 4))
        legend_item_gap = float(self._tok("legend-item-gap", 16))
        legend_font_size = float(self._tok("legend-font-size", 9))
        legend_font_color = str(
            self._tok("legend-font-color")
            or self.resolve("color-text-muted")
            or "#6B7280"
        )

        # ── Legend labels per level ────────────────────────────────────
        _LEGEND_LABELS = {
            0: "0 – n/a",
            1: "1 – low",
            2: "2 – low-med",
            3: "3 – medium",
            4: "4 – high",
            5: "5 – critical",
        }

        # ── Uniform cluster height ─────────────────────────────────────
        # Driven by the cluster with the most facts so all clusters are equal-sized
        max_facts = max((len(c.get("facts") or []) for c in clusters), default=1)
        max_fact_rows = math.ceil(max_facts / n_fact_cols)
        # height = heading bar + top padding + fact rows + fact gaps + bottom padding
        cluster_h = (
            heading_height
            + cluster_padding
            + max_fact_rows * fact_height
            + max(0, max_fact_rows - 1) * fact_gap
            + cluster_padding
        )

        # ── Uniform cluster width ──────────────────────────────────────
        cluster_w = (box.w - cluster_gap * (n_cluster_cols - 1)) / n_cluster_cols

        # ── Legend occupies the top of the body area ──────────────────
        legend_reserved = (legend_height + legend_margin_bottom) if legend_visible else 0.0
        cluster_area_y = box.y + legend_reserved
        cluster_area_h = box.h - legend_reserved

        # ── Pagination: how many cluster rows fit in available height? ──
        if cluster_h > 0:
            # How many rows fit — at least 1
            n_cluster_rows = max(
                1,
                int(
                    (cluster_area_h + cluster_gap) / (cluster_h + cluster_gap)
                ),
            )
        else:
            n_cluster_rows = 1

        clusters_per_page = n_cluster_cols * n_cluster_rows
        page_offset = (page - 1) * clusters_per_page
        page_clusters = clusters[page_offset: page_offset + clusters_per_page]

        if not page_clusters:
            return

        # ── Render legend ──────────────────────────────────────────────
        if legend_visible:
            # Estimate total width of all 6 items to center the legend
            approx_label_w = legend_font_size * 6.5  # rough avg char width × max label len
            item_w = legend_swatch_size + legend_swatch_gap + approx_label_w
            total_legend_w = 6 * item_w + 5 * legend_item_gap
            legend_start_x = box.x + max(0.0, (box.w - total_legend_w) / 2)
            legend_y = box.y + (legend_height - legend_swatch_size) / 2

            for lvl in range(6):
                swatch_bg, _ = self._heat_colors(lvl)
                ix = legend_start_x + lvl * (item_w + legend_item_gap)

                # Coloured swatch square
                box.add(
                    {
                        "type": "rect",
                        "x": ix,
                        "y": legend_y,
                        "w": legend_swatch_size,
                        "h": legend_swatch_size,
                        "fill": swatch_bg,
                        "stroke": "none",
                        "stroke_width": 0,
                        "rx": legend_swatch_radius,
                    }
                )

                # Label text beside the swatch
                box.add(
                    {
                        "type": "text",
                        "x": ix + legend_swatch_size + legend_swatch_gap,
                        "y": legend_y,
                        "w": approx_label_w,
                        "h": legend_swatch_size,
                        "text": _LEGEND_LABELS[lvl],
                        "font_size": legend_font_size,
                        "font_color": legend_font_color,
                        "font_weight": "400",
                        "alignment": "left",
                        "vertical_align": "middle",
                        "wrap": False,
                    }
                )

        # ── Render clusters ────────────────────────────────────────────
        for i, cluster in enumerate(page_clusters):
            col = i % n_cluster_cols
            row = i // n_cluster_cols

            cx = box.x + col * (cluster_w + cluster_gap)
            cy = cluster_area_y + row * (cluster_h + cluster_gap)

            # Cluster container border
            box.add(
                {
                    "type": "rect",
                    "x": cx,
                    "y": cy,
                    "w": cluster_w,
                    "h": cluster_h,
                    "fill": "transparent",
                    "stroke": cluster_border_stroke,
                    "stroke_width": cluster_border_width,
                    "rx": cluster_border_radius,
                }
            )

            # ── Cluster heading bar ────────────────────────────────────
            # Clipped to the top of the container with the same corner radius
            box.add(
                {
                    "type": "rect",
                    "x": cx,
                    "y": cy,
                    "w": cluster_w,
                    "h": heading_height,
                    "fill": heading_bg,
                    "stroke": "none",
                    "stroke_width": 0,
                    "rx": cluster_border_radius,
                    # Bottom corners square to merge visually with the body area
                    "rx_bottom": 0,
                }
            )
            # Heading text
            cluster_name = str(cluster.get("name") or "")
            if cluster_name:
                box.add(
                    {
                        "type": "text",
                        "x": cx + heading_padding,
                        "y": cy,
                        "w": cluster_w - 2 * heading_padding,
                        "h": heading_height,
                        "text": cluster_name,
                        "font_size": heading_font_size,
                        "font_color": heading_font_color,
                        "font_weight": heading_font_weight,
                        "alignment": heading_alignment,
                        "vertical_align": "middle",
                        "wrap": False,
                    }
                )

            # ── Fact tile grid ─────────────────────────────────────────
            facts = cluster.get("facts") or []
            body_x = cx + cluster_padding
            body_y_start = cy + heading_height + cluster_padding
            fact_area_w = cluster_w - 2 * cluster_padding
            fact_w = (fact_area_w - fact_gap * (n_fact_cols - 1)) / n_fact_cols

            for j, fact in enumerate(facts):
                fc = j % n_fact_cols
                fr = j // n_fact_cols

                fx = body_x + fc * (fact_w + fact_gap)
                fy = body_y_start + fr * (fact_height + fact_gap)

                level = 0
                try:
                    level = int(fact.get("level") or 0)
                except (TypeError, ValueError):
                    level = 0
                level = max(0, min(5, level))

                fact_bg, fact_fg = self._heat_colors(level)
                fact_text = str(fact.get("text") or "")

                # Fact tile background
                box.add(
                    {
                        "type": "rect",
                        "x": fx,
                        "y": fy,
                        "w": fact_w,
                        "h": fact_height,
                        "fill": fact_bg,
                        "stroke": "none",
                        "stroke_width": 0,
                        "rx": fact_border_radius,
                    }
                )

                # Fact label text
                if fact_text:
                    box.add(
                        {
                            "type": "text",
                            "x": fx + fact_padding,
                            "y": fy,
                            "w": max(1.0, fact_w - 2 * fact_padding),
                            "h": fact_height,
                            "text": fact_text,
                            "font_size": fact_font_size,
                            "font_color": fact_fg,
                            "font_weight": fact_font_weight,
                            "alignment": fact_text_align,
                            "vertical_align": "middle",
                            "wrap": True,
                        }
                    )
