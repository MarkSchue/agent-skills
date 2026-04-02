"""
BaseCardRenderer — Abstract base for all card renderers.

Every card renderer subclass must implement :meth:`render_body`. The base class
handles:

- card container geometry (background, border, radius, padding)
- card title rendering
- header line rendering
- token resolution through the standard 4-level priority chain

Subclasses should call ``self.resolve(token_name)`` to look up any token
value — this method transparently applies the override chain using the current
card's ``style_overrides`` and the renderer's variant name.

No renderer may short-circuit the priority chain by reading
``card.style_overrides`` or ``card.props`` directly for token lookups.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from scripts.models.deck import CardModel
from scripts.models.theme import ThemeTokens


class RenderBox:
    """Axis-aligned bounding box for a rendered element.

    Attributes:
        x: Left edge in px.
        y: Top edge in px.
        w: Width in px.
        h: Height in px.
        elements: Child rendered elements (exporter-agnostic dicts).
    """

    __slots__ = ("x", "y", "w", "h", "elements", "chrome", "card_slots")

    def __init__(self, x: float, y: float, w: float, h: float) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.elements: list[dict[str, Any]] = []
        self.chrome: Any = None
        self.card_slots: Any = None

    def add(self, element: dict[str, Any]) -> None:
        self.elements.append(element)


class BaseCardRenderer(ABC):
    """Abstract base for all card renderers.

    Args:
        theme: The loaded ``ThemeTokens`` for the current deck.
        variant: CSS variant class name (e.g. ``card--kpi``), or ``None``.
    """

    variant: str | None = None

    def __init__(self, theme: ThemeTokens) -> None:
        self.theme = theme
        self._card: CardModel | None = None
        self._slide_overrides: dict[str, Any] = {}

    # ── public API ────────────────────────────────────────────────────────

    def render(
        self,
        card: CardModel,
        box: RenderBox,
        *,
        slide_overrides: dict[str, Any] | None = None,
    ) -> RenderBox:
        """Render *card* into the given *box*.

        Args:
            card: The card model to render.
            box: The allocated bounding box for this card.
            slide_overrides: Per-slide overrides that should also feed into
                             token resolution (lower priority than card overrides).

        Returns:
            The *box* populated with render elements.
        """
        self._card = card
        self._slide_overrides = slide_overrides or {}

        # Container
        self._render_container(box)

        # Title + header line
        body_y = self._render_header(card, box)

        # Delegate body to subclass
        body_box = RenderBox(
            x=box.x + self._pad_left,
            y=body_y,
            w=box.w - self._pad_left - self._pad_right,
            h=box.y + box.h - body_y - self._pad_bottom,
        )
        self.render_body(card, body_box)
        box.elements.extend(body_box.elements)

        self._card = None
        self._slide_overrides = {}
        return box

    @abstractmethod
    def render_body(self, card: CardModel, box: RenderBox) -> None:
        """Render card-type-specific body content into *box*.

        Must be implemented by every subclass.
        """

    # ── token resolution ─────────────────────────────────────────────────

    def resolve(self, token_name: str) -> Any:
        """Resolve a token through the 4-level priority chain.

        Priority: card override → slide override → variant → base → fallback.
        """
        # Merge slide overrides (lower priority) with card overrides (higher)
        merged = {**self._slide_overrides}
        if self._card and self._card.style_overrides:
            merged.update(self._card.style_overrides)
        return self.theme.resolve(
            token_name,
            variant=self.variant,
            overrides=merged if merged else None,
        )

    # ── private rendering helpers ────────────────────────────────────────

    @property
    def _pad_left(self) -> float:
        return float(self.resolve("card-padding") or 16)

    @property
    def _pad_right(self) -> float:
        return float(self.resolve("card-padding") or 16)

    @property
    def _pad_top(self) -> float:
        return float(self.resolve("card-padding") or 16)

    @property
    def _pad_bottom(self) -> float:
        return float(self.resolve("card-padding") or 16)

    def _render_container(self, box: RenderBox) -> None:
        """Add a container rectangle element to *box*."""
        box.add(
            {
                "type": "rect",
                "x": box.x,
                "y": box.y,
                "w": box.w,
                "h": box.h,
                "fill": self.resolve("card-background"),
                "stroke": self.resolve("card-border-color"),
                "stroke_width": self.resolve("card-border-width"),
                "rx": self.resolve("card-border-radius"),
            }
        )

    def _render_header(self, card: CardModel, box: RenderBox) -> float:
        """Render title + header line. Return the Y-coordinate for body start."""
        y = box.y + self._pad_top

        if card.title:
            title_size = self.resolve("card-title-font-size") or 16
            line_gap = float(self.resolve("card-title-line-gap") or 8)
            box.add(
                {
                    "type": "text",
                    "x": box.x + self._pad_left,
                    "y": y,
                    "w": box.w - self._pad_left - self._pad_right,
                    "h": float(title_size) + line_gap,
                    "text": card.title,
                    "font_size": title_size,
                    "font_color": self.resolve("card-title-font-color"),
                    "font_weight": self.resolve("card-title-font-weight"),
                }
            )
            y += float(title_size) + line_gap

            # Header line
            line_width = self.resolve("card-title-line-width")
            if line_width and float(line_width) > 0:
                box.add(
                    {
                        "type": "line",
                        "x1": box.x + self._pad_left,
                        "y1": y,
                        "x2": box.x + box.w - self._pad_right,
                        "y2": y,
                        "stroke": self.resolve("card-title-line-color"),
                        "stroke_width": line_width,
                    }
                )
                y += float(line_width) + 8

        return y
