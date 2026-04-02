"""
Presentation structure models: DeckModel, SectionModel, SlideModel, CardModel.

These models are the normalized internal representation produced by the parser
and consumed by the layout engine, card renderers, and exporters.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CardModel:
    """A single card within a slide.

    Attributes:
        title: Card heading text (from ``### …``).
        card_type: Registry card type id (e.g. ``text-card``, ``kpi-card``).
        content: Arbitrary content dict parsed from the card YAML block.
        style_overrides: Per-card CSS token overrides from ``style_overrides:`` key.
        props: Raw props dict from the YAML block (passed to geometry helpers).
        asset_refs: Resolved asset paths referenced by this card.
        subtitle: Optional subtitle text shown below the header line (muted caption).
        icon: Optional icon dict with keys: ``name``, ``visible``, ``position``,
              ``color``, ``size``.  Rendered beside the card title by the base class.
    """

    title: str = ""
    card_type: str = "text-card"
    content: dict[str, Any] = field(default_factory=dict)
    style_overrides: dict[str, Any] = field(default_factory=dict)
    props: dict[str, Any] = field(default_factory=dict)
    asset_refs: list[str] = field(default_factory=list)
    subtitle: str = ""
    icon: dict[str, Any] = field(default_factory=dict)


@dataclass
class SlideModel:
    """A single slide within a section.

    Attributes:
        title: Slide title text (from ``## …``).
        subtitle: Optional subtitle text.
        cards: Ordered list of cards on this slide.
        layout: Explicit layout id if set (e.g. ``grid-2x2``), else ``None`` for auto.
        slide_overrides: Per-slide CSS/theme overrides from the ``<!-- slide … -->`` block.
        is_frozen: True if ``<!-- DONE -->`` appears directly below the ``##`` heading.
        is_generated: True for auto-injected slides (e.g. agenda).
        notes: Speaker notes text.
    """

    title: str = ""
    subtitle: str = ""
    cards: list[CardModel] = field(default_factory=list)
    layout: str | None = None
    slide_overrides: dict[str, Any] = field(default_factory=dict)
    is_frozen: bool = False
    is_generated: bool = False
    notes: str = ""


@dataclass
class SectionModel:
    """A top-level ``# Section`` grouping.

    Attributes:
        title: Section heading (used for agenda entries).
        slides: Ordered list of slides in this section.
    """

    title: str = ""
    slides: list[SlideModel] = field(default_factory=list)


@dataclass
class DeckModel:
    """Root model for an entire presentation deck.

    Attributes:
        title: Deck title (first ``#`` heading or metadata).
        sections: Ordered list of sections.
        metadata: Top-level YAML metadata from the deck header (if any).
    """

    title: str = ""
    sections: list[SectionModel] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def all_slides(self) -> list[SlideModel]:
        """Flat list of all slides across all sections."""
        return [s for sec in self.sections for s in sec.slides]

    @property
    def section_titles(self) -> list[str]:
        """List of section titles (for agenda generation)."""
        return [sec.title for sec in self.sections]
