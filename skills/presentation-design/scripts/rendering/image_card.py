"""
ImageCardRenderer — Renders image-card content with fullbleed, framed, or circular styles.
"""

from __future__ import annotations

import logging
from pathlib import Path

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox

logger = logging.getLogger(__name__)


class ImageCardRenderer(BaseCardRenderer):
    """Renderer for ``image-card`` type.

    Resolves the image display mode from the card's ``image_style`` prop
    (``fullbleed``, ``framed``, ``circular``), defaulting to ``framed``.
    """

    variant = None  # image style tokens live in base families

    def __init__(self, theme, *, project_root: str | Path | None = None) -> None:
        super().__init__(theme)
        self.project_root = Path(project_root) if project_root else None

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        """Render the image element with the selected display style."""
        content = card.content if isinstance(card.content, dict) else {}
        image_path = content.get("image", "")
        alt_text = content.get("alt", "")
        caption = content.get("caption", "")
        image_style = card.props.get("image_style", "framed")

        # Resolve full asset path
        resolved_path = self._resolve_asset(image_path)

        if image_style == "fullbleed":
            self._render_fullbleed(box, resolved_path, alt_text)
        elif image_style == "circular":
            self._render_circular(box, resolved_path, alt_text)
        else:
            self._render_framed(box, resolved_path, alt_text)

        # Caption
        if caption:
            caption_size = float(self.resolve("text-caption-font-size") or 11)
            box.add(
                {
                    "type": "text",
                    "x": box.x,
                    "y": box.y + box.h - caption_size - 4,
                    "w": box.w,
                    "text": caption,
                    "font_size": caption_size,
                    "font_color": self.resolve("text-caption-font-color") or "#888888",
                    "alignment": "center",
                }
            )

    def _render_fullbleed(self, box: RenderBox, path: str, alt: str) -> None:
        box.add(
            {
                "type": "image",
                "x": box.x,
                "y": box.y,
                "w": box.w,
                "h": box.h,
                "src": path,
                "alt": alt,
                "fit": "cover",
                "border_radius": 0,
            }
        )

    def _render_framed(self, box: RenderBox, path: str, alt: str) -> None:
        br = self.resolve("image-framed-border-radius") or 4
        bw = self.resolve("image-framed-border-width") or 1
        bc = self.resolve("image-framed-border-color") or "#E0E0E0"
        pad = float(self.resolve("image-framed-padding") or 8)
        box.add(
            {
                "type": "image",
                "x": box.x + pad,
                "y": box.y + pad,
                "w": box.w - 2 * pad,
                "h": box.h - 2 * pad - 20,  # leave room for caption
                "src": path,
                "alt": alt,
                "fit": "contain",
                "border_radius": br,
                "border_width": bw,
                "border_color": bc,
            }
        )

    def _render_circular(self, box: RenderBox, path: str, alt: str) -> None:
        size = min(box.w, box.h) * 0.7
        cx = box.x + (box.w - size) / 2
        cy = box.y + (box.h - size) / 2
        br = self.resolve("image-circular-border-radius") or "50%"
        bc = self.resolve("image-circular-border-color") or "transparent"
        box.add(
            {
                "type": "image",
                "x": cx,
                "y": cy,
                "w": size,
                "h": size,
                "src": path,
                "alt": alt,
                "fit": "cover",
                "border_radius": br,
                "border_color": bc,
            }
        )

    def _resolve_asset(self, rel_path: str) -> str:
        """Resolve a relative asset path against the project root.

        If the file doesn't exist, log a warning and return the path anyway
        (the exporter will render a placeholder).
        """
        if not rel_path:
            return ""
        if self.project_root:
            full = self.project_root / "assets" / rel_path
            if not full.exists():
                logger.warning(
                    "Asset not found: %s (expected at %s)", rel_path, full
                )
        return rel_path
