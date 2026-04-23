"""
DrawioRenderer â€” thin wrapper around DrawioSvgRenderer.

All rendering logic lives in :mod:`scripts.drawio_svg_renderer`.
This module keeps the public ``ensure_diagram_svg`` API used by
:mod:`scripts.rendering.image_card` unchanged.
"""

from __future__ import annotations

import logging
from pathlib import Path

from scripts.drawio_svg_renderer import DrawioSvgRenderer as _DrawioSvgRenderer

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Public API â€” kept for backward-compatibility with image_card.py
# ---------------------------------------------------------------------------

# Re-export the class under the legacy name so any code that imported
# DrawioRenderer directly still works.
DrawioRenderer = _DrawioSvgRenderer

_renderer = _DrawioSvgRenderer()


def ensure_diagram_svg(
    drawio_path: Path,
    page_name: str,
    out_dir: Path,
    target_width: float | None = None,
    target_height: float | None = None,
) -> Path:
    """Render *page_name* from *drawio_path* to an SVG file in *out_dir*.

    Delegates to :class:`scripts.drawio_svg_renderer.DrawioSvgRenderer`.
    The SVG is regenerated only when the source ``.drawio`` file is newer
    than the cached SVG (mtime-based invalidation).
    """
    return _renderer.ensure_svg(
        drawio_path, page_name, out_dir, target_width, target_height
    )

# --- Everything below this line has been removed and lives in ---
# --- scripts/drawio_svg_renderer.py                           ---

