"""
ImageCardRenderer — Renders image-card content with fullbleed, framed, or circular styles.

Draw.io diagram support
-----------------------
When the ``image`` value follows the pattern ``"path/to/file.drawio#page-name"``,
the renderer automatically converts the named draw.io page to SVG at build time
(via :mod:`scripts.rendering.drawio_renderer`).  The SVG is written to the same
``assets/diagrams/`` directory and named ``{page-name}.svg``.  The SVG is only
regenerated when the ``.drawio`` source file is newer than the cached SVG
(mtime-based cache invalidation).

The image-card's body dimensions (``box.w`` × ``box.h``) are passed to the
renderer so the SVG ``width``/``height`` attributes match the available slide
area, ensuring a perfect fill with no letterboxing.
"""

from __future__ import annotations

import logging
from pathlib import Path

from scripts.models.deck import CardModel
from scripts.rendering.base_card import BaseCardRenderer, RenderBox
from scripts.rendering.drawio_renderer import ensure_diagram_svg

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
        image_path = content.get("image", "") or content.get("source", "")
        alt_text = content.get("alt", "")
        caption = content.get("caption", "")
        image_style = (
            card.props.get("image_style")
            or content.get("image_style")
            or "framed"
        )

        # ── Draw.io page reference: "diagrams/file.drawio#page-name" ──────
        image_path = self._resolve_drawio(image_path, box.w, box.h)

        # Resolve full asset path
        resolved_path = self._resolve_asset(image_path)

        # Reserve vertical space for caption when present — all image styles honour this
        caption_size = float(self.resolve("text-caption-font-size") or 11)
        caption_reserved = (caption_size + 4) if caption else 0.0

        if image_style == "fullbleed":
            self._render_fullbleed(box, resolved_path, alt_text,
                                   caption_reserved=caption_reserved)
        elif image_style == "circular":
            self._render_circular(box, resolved_path, alt_text)
        else:
            self._render_framed(box, resolved_path, alt_text,
                                caption_reserved=caption_reserved)

        # Caption text rendered below the image
        if caption:
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

    def _render_fullbleed(self, box: RenderBox, path: str, alt: str,
                          *, caption_reserved: float = 0.0) -> None:
        box.add(
            {
                "type": "image",
                "x": box.x,
                "y": box.y,
                "w": box.w,
                "h": box.h - caption_reserved,
                "src": path,
                "alt": alt,
                "fit": "cover",
                "border_radius": 0,
            }
        )

    def _render_framed(self, box: RenderBox, path: str, alt: str,
                       *, caption_reserved: float = 0.0) -> None:
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
                "h": box.h - 2 * pad - caption_reserved,
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

    def _resolve_drawio(self, image_path: str, box_w: float, box_h: float) -> str:
        """If *image_path* is a ``"rel/path.drawio#page-name"`` reference,
        convert the named draw.io page to SVG (cached, mtime-tracked) and
        return the relative SVG path.  Otherwise return *image_path* unchanged.
        """
        if not image_path or ".drawio#" not in image_path:
            return image_path

        # Split "diagrams/file.drawio#page-name"
        drawio_rel, page_name = image_path.split("#", 1)

        if not self.project_root:
            logger.warning(
                "Cannot resolve draw.io reference '%s': project_root not set.",
                image_path,
            )
            return image_path

        drawio_abs = self.project_root / "assets" / drawio_rel
        if not drawio_abs.exists():
            logger.warning("Draw.io file not found: %s", drawio_abs)
            return image_path

        # SVG lives alongside the draw.io file, named after the page
        out_dir = drawio_abs.parent
        svg_path = ensure_diagram_svg(
            drawio_path   = drawio_abs,
            page_name     = page_name,
            out_dir       = out_dir,
            target_width  = box_w  if box_w  > 0 else None,
            target_height = box_h  if box_h  > 0 else None,
        )

        # Return relative path (relative to assets/) for _resolve_asset
        try:
            rel = svg_path.relative_to(self.project_root / "assets")
            return str(rel).replace("\\", "/")
        except ValueError:
            return str(svg_path)

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
