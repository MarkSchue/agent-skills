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

    def render(self, slide, *, page_number: int = 1) -> RenderBox:
        """Render chrome + large centered title/subtitle in the body area."""
        canvas = super().render(slide, page_number=page_number)
        overrides = slide.slide_overrides

        chrome = canvas.chrome  # type: ignore[attr-defined]
        body_x = chrome.body_x
        body_y = chrome.body_y
        body_w = chrome.body_w
        body_h = chrome.body_h

        # ── Large centered title ───────────────────────────────────────────
        title_size = float(
            self._resolve("title-slide-title-font-size", overrides) or 40
        )
        title_color = (
            self._resolve("title-slide-title-font-color", overrides)
            or self._resolve("slide-title-font-color", overrides)
            or "#1A1A1A"
        )
        title_weight = (
            str(self._resolve("title-slide-title-font-weight", overrides) or "700")
        )

        title_h = title_size * 1.4
        # Vertically center title block in body (starting at ~35% from top)
        title_y = body_y + body_h * 0.30

        canvas.add(
            {
                "type": "text",
                "x": body_x,
                "y": title_y,
                "w": body_w,
                "h": title_h,
                "text": slide.title or "",
                "font_size": title_size,
                "font_color": title_color,
                "font_weight": title_weight,
                "alignment": "center",
                "wrap": True,
            }
        )

        # ── Subtitle ───────────────────────────────────────────────────────
        if slide.subtitle:
            sub_size = float(
                self._resolve("title-slide-subtitle-font-size", overrides) or 20
            )
            sub_color = (
                self._resolve("title-slide-subtitle-font-color", overrides)
                or self._resolve("slide-subtitle-font-color", overrides)
                or "#555555"
            )
            sub_h = sub_size * 2.5
            sub_y = title_y + title_h + 16

            canvas.add(
                {
                    "type": "text",
                    "x": body_x,
                    "y": sub_y,
                    "w": body_w,
                    "h": sub_h,
                    "text": slide.subtitle,
                    "font_size": sub_size,
                    "font_color": sub_color,
                    "alignment": "center",
                    "wrap": True,
                }
            )

        return canvas
