"""
TitleSlideLayoutRenderer — Full-canvas title slide with no card slots.
"""

from __future__ import annotations

from typing import Any

from scripts.rendering.base_layout import BaseLayoutRenderer, RenderBox, SlideChrome


class TitleSlideLayoutRenderer(BaseLayoutRenderer):
    """Layout renderer for ``title-slide`` — no card grid."""

    def compute_card_slots(
        self,
        chrome: SlideChrome,
        overrides: dict[str, Any] | None,
    ) -> list[RenderBox]:
        """Title slide has zero card slots."""
        return []
