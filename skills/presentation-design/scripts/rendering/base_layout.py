"""
BaseLayoutRenderer — Abstract base for all layout renderers.

Handles shared slide chrome: title, subtitle, divider, logos, footer, page number.
Subclasses implement :meth:`compute_card_slots` to define card placement for
their specific grid geometry.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from scripts.models.deck import SlideModel
from scripts.models.theme import ThemeTokens
from scripts.rendering.base_card import RenderBox


class SlideChrome:
    """Pre-computed slide chrome geometry.

    Attributes:
        body_x: Left edge of the card body area.
        body_y: Top edge of the card body area (below title/divider).
        body_w: Width of the card body area.
        body_h: Height of the card body area (above footer).
    """

    __slots__ = ("body_x", "body_y", "body_w", "body_h")

    def __init__(self, body_x: float, body_y: float, body_w: float, body_h: float):
        self.body_x = body_x
        self.body_y = body_y
        self.body_w = body_w
        self.body_h = body_h


class BaseLayoutRenderer(ABC):
    """Abstract base for all layout renderers.

    Args:
        theme: The loaded ``ThemeTokens`` for the current deck.
    """

    def __init__(self, theme: ThemeTokens) -> None:
        self.theme = theme

    # ── public API ────────────────────────────────────────────────────────

    def render(
        self,
        slide: SlideModel,
        *,
        page_number: int = 1,
    ) -> RenderBox:
        """Render the slide chrome and compute card slots.

        Returns a :class:`RenderBox` for the full canvas, populated with chrome
        elements and containing the card slot bounding boxes via the
        :meth:`compute_card_slots` return value.
        """
        overrides = slide.slide_overrides

        canvas_w = float(self._resolve("canvas-width", overrides) or 1280)
        canvas_h = float(self._resolve("canvas-height", overrides) or 720)

        canvas = RenderBox(0, 0, canvas_w, canvas_h)

        # Background
        bg = self._resolve("canvas-background-color", overrides) or "#FFFFFF"
        canvas.add(
            {
                "type": "rect",
                "x": 0,
                "y": 0,
                "w": canvas_w,
                "h": canvas_h,
                "fill": bg,
                "rx": 0,
            }
        )

        # Margins
        ml = float(self._resolve("canvas-padding-left", overrides) or 48)
        mr = float(self._resolve("canvas-padding-right", overrides) or 48)
        mt = float(self._resolve("canvas-padding-top", overrides) or 48)
        mb = float(self._resolve("canvas-padding-bottom", overrides) or 48)

        y_cursor = mt

        # Logos
        y_cursor = self._render_logos(canvas, ml, mr, y_cursor, overrides)

        # Title
        if slide.title:
            title_size = float(
                self._resolve("slide-title-font-size", overrides) or 28
            )
            canvas.add(
                {
                    "type": "text",
                    "x": ml,
                    "y": y_cursor,
                    "w": canvas_w - ml - mr,
                    "h": title_size + 4,
                    "text": slide.title,
                    "font_size": title_size,
                    "font_color": self._resolve("slide-title-font-color", overrides)
                    or "#1A1A1A",
                    "font_weight": self._resolve(
                        "slide-title-font-weight", overrides
                    )
                    or "bold",
                    "alignment": self._resolve(
                        "slide-title-alignment", overrides
                    )
                    or "left",
                }
            )
            y_cursor += title_size + 4

        # Subtitle
        if slide.subtitle:
            sub_size = float(
                self._resolve("slide-subtitle-font-size", overrides) or 18
            )
            canvas.add(
                {
                    "type": "text",
                    "x": ml,
                    "y": y_cursor,
                    "w": canvas_w - ml - mr,
                    "h": sub_size + 4,
                    "text": slide.subtitle,
                    "font_size": sub_size,
                    "font_color": self._resolve(
                        "slide-subtitle-font-color", overrides
                    )
                    or "#555555",
                }
            )
            y_cursor += sub_size + 4

        # Divider line
        div_width = float(
            self._resolve("slide-divider-border-width", overrides) or 1
        )
        if div_width > 0:
            canvas.add(
                {
                    "type": "line",
                    "x1": ml,
                    "y1": y_cursor,
                    "x2": canvas_w - mr,
                    "y2": y_cursor,
                    "stroke": self._resolve(
                        "slide-divider-border-color", overrides
                    )
                    or "#CCCCCC",
                    "stroke_width": div_width,
                }
            )
            y_cursor += div_width + 8

        # Footer region
        footer_y = canvas_h - mb
        hide_footer = overrides.get("hide_footer", False) if overrides else False
        if not hide_footer:
            footer_y = self._render_footer(
                canvas, ml, mr, canvas_w, canvas_h, mb, page_number, overrides
            )

        # Compute body region
        chrome = SlideChrome(
            body_x=ml,
            body_y=y_cursor,
            body_w=canvas_w - ml - mr,
            body_h=footer_y - y_cursor - 8,
        )

        # Store chrome and card slots on the canvas for downstream use
        canvas.chrome = chrome  # type: ignore[attr-defined]
        canvas.card_slots = self.compute_card_slots(chrome, overrides)  # type: ignore[attr-defined]

        return canvas

    @abstractmethod
    def compute_card_slots(
        self,
        chrome: SlideChrome,
        overrides: dict[str, Any] | None,
    ) -> list[RenderBox]:
        """Return a list of bounding boxes for card placement.

        Must be implemented by every subclass.
        """

    # ── token resolution ─────────────────────────────────────────────────

    def _resolve(self, token: str, overrides: dict[str, Any] | None = None) -> Any:
        return self.theme.resolve(token, overrides=overrides)

    # ── chrome rendering helpers ─────────────────────────────────────────

    def _render_logos(
        self,
        canvas: RenderBox,
        ml: float,
        mr: float,
        y: float,
        overrides: dict[str, Any] | None,
    ) -> float:
        """Render primary and secondary logo placeholders. Return updated Y."""
        logo_h = 30  # placeholder height
        # Primary logo top-left
        canvas.add(
            {
                "type": "placeholder",
                "role": "logo-primary",
                "x": ml,
                "y": y,
                "w": 120,
                "h": logo_h,
            }
        )
        # Secondary logo top-right
        canvas.add(
            {
                "type": "placeholder",
                "role": "logo-secondary",
                "x": canvas.w - mr - 120,
                "y": y,
                "w": 120,
                "h": logo_h,
            }
        )
        return y + logo_h + 4

    def _render_footer(
        self,
        canvas: RenderBox,
        ml: float,
        mr: float,
        canvas_w: float,
        canvas_h: float,
        mb: float,
        page_number: int,
        overrides: dict[str, Any] | None,
    ) -> float:
        """Render footer line, text, and page number. Return the top Y of footer region."""
        footer_size = float(
            self._resolve("slide-footer-font-size", overrides) or 10
        )
        footer_h = footer_size + 16  # line + text + padding
        footer_top = canvas_h - mb - footer_h

        # Footer line
        canvas.add(
            {
                "type": "line",
                "x1": ml,
                "y1": footer_top,
                "x2": canvas_w - mr,
                "y2": footer_top,
                "stroke": self._resolve("slide-divider-border-color", overrides)
                or "#CCCCCC",
                "stroke_width": 1,
            }
        )

        # Footer text placeholder (left-aligned)
        canvas.add(
            {
                "type": "placeholder",
                "role": "footer-text",
                "x": ml,
                "y": footer_top + 4,
                "w": canvas_w * 0.6,
                "h": footer_size,
            }
        )

        # Page number (right-aligned)
        pn_size = float(
            self._resolve("slide-page-number-font-size", overrides) or 10
        )
        canvas.add(
            {
                "type": "text",
                "x": canvas_w - mr - 40,
                "y": footer_top + 4,
                "w": 40,
                "text": str(page_number),
                "font_size": pn_size,
                "font_color": self._resolve(
                    "slide-page-number-font-color", overrides
                )
                or "#888888",
                "alignment": "right",
            }
        )

        return footer_top
