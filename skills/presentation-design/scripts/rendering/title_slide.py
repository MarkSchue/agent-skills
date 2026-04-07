"""
TitleSlideLayoutRenderer — Full-canvas title slide with no card slots.
"""

from __future__ import annotations

from typing import Any

from scripts.rendering.base_layout import BaseLayoutRenderer, RenderBox, SlideChrome


class TitleSlideLayoutRenderer(BaseLayoutRenderer):
    """Layout renderer for ``title-slide`` — no card grid."""

    def __init__(self, theme, project_root=None) -> None:
        super().__init__(theme, project_root=project_root)

    def compute_card_slots(
        self,
        chrome: SlideChrome,
        overrides: dict[str, Any] | None,
    ) -> list[RenderBox]:
        """Title slide has zero card slots."""
        return []
