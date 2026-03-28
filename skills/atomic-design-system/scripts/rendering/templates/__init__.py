"""
TEMPLATE_REGISTRY — maps every layout slug to its renderer instance.

Parallel to MOLECULE_REGISTRY in rendering/molecules/.
To add a new template:
  1. Create rendering/templates/<name>.py with a class that has:
         render(self, ctx, slide, blocks, margin, content_y, content_h,
                width, height, dispatch_fn) -> None
  2. Import it here and add it to TEMPLATE_REGISTRY.
  3. Add a template spec .md in .github/agents/atomic-design-system/templates/.
"""

from rendering.templates.hero_title      import HeroTitleLayout
from rendering.templates.grid            import GridLayout, AsymmetricGridLayout
from rendering.templates.row_layout      import RowLayout
from rendering.templates.grid_row_layout import GridRowLayout

TEMPLATE_REGISTRY: dict = {
    # ── Hero ──────────────────────────────────────────────────────────────
    "hero-title":       HeroTitleLayout(),

    # ── Column grids ──────────────────────────────────────────────────────
    "grid-2":           GridLayout(cols=2),
    "grid-3":           GridLayout(cols=3),
    "grid-4":           GridLayout(cols=4),

    # ── Asymmetric column grids ───────────────────────────────────────────
    "grid-2-1":         AsymmetricGridLayout(weights=(2, 1)),
    "grid-1-2":         AsymmetricGridLayout(weights=(1, 2)),

    # ── Row layouts ───────────────────────────────────────────────────────
    "row-2":            RowLayout(rows=2),
    "row-3":            RowLayout(rows=3),
    "row-2-1":          RowLayout(row_weights=(2, 1)),
    "row-1-2":          RowLayout(row_weights=(1, 2)),

    # ── Grid × row layouts ────────────────────────────────────────────────
    "grid-row-2-2":     GridRowLayout(cols=2, rows=2),
    "grid-row-3-2":     GridRowLayout(cols=3, rows=2),
}

__all__ = ["TEMPLATE_REGISTRY"]
