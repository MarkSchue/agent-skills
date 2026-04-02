"""
ChartCardRenderer — Renders chart-card with an image and optional caption.
"""

from __future__ import annotations

import logging
from pathlib import Path

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox

logger = logging.getLogger(__name__)


class ChartCardRenderer(BaseCardRenderer):
    """Renderer for ``chart-card`` type."""

    variant = "card--chart"

    def __init__(self, theme, *, project_root: str | Path | None = None) -> None:
        super().__init__(theme)
        self.project_root = Path(project_root) if project_root else None

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        """Render chart image and optional caption."""
        content = card.content if isinstance(card.content, dict) else {}
        image_path = content.get("image", "")
        alt_text = content.get("alt", "")
        caption = content.get("caption", "")

        image_fit = self.resolve("card-chart-image-fit") or "contain"
        border_radius = self.resolve("card-chart-image-border-radius") or 4

        # Resolve asset path
        if image_path and self.project_root:
            full = self.project_root / "assets" / image_path
            if not full.exists():
                logger.warning(
                    "Chart asset not found: %s (expected at %s)", image_path, full
                )

        # Reserve caption space
        caption_h = 20 if caption else 0
        img_h = box.h - caption_h

        # Chart image
        if image_path:
            box.add(
                {
                    "type": "image",
                    "x": box.x,
                    "y": box.y,
                    "w": box.w,
                    "h": img_h,
                    "src": image_path,
                    "alt": alt_text,
                    "fit": image_fit,
                    "border_radius": border_radius,
                }
            )
        else:
            # Placeholder box for missing chart
            box.add(
                {
                    "type": "rect",
                    "x": box.x,
                    "y": box.y,
                    "w": box.w,
                    "h": img_h,
                    "fill": "#F5F5F5",
                    "stroke": "#CCCCCC",
                    "stroke_width": 1,
                    "rx": border_radius,
                }
            )
            box.add(
                {
                    "type": "text",
                    "x": box.x,
                    "y": box.y + img_h * 0.4,
                    "w": box.w,
                    "text": "[chart placeholder]",
                    "font_size": 12,
                    "font_color": "#AAAAAA",
                    "alignment": "center",
                }
            )

        # Caption
        if caption:
            caption_size = float(
                self.resolve("card-chart-caption-font-size") or 11
            )
            caption_color = (
                self.resolve("card-chart-caption-font-color") or "#888888"
            )
            caption_align = self.resolve("card-chart-caption-alignment") or "center"
            box.add(
                {
                    "type": "text",
                    "x": box.x,
                    "y": box.y + img_h + 4,
                    "w": box.w,
                    "text": caption,
                    "font_size": caption_size,
                    "font_color": caption_color,
                    "alignment": caption_align,
                }
            )
