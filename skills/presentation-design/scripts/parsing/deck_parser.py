"""
DeckParser — Structured Markdown to DeckModel.

Parses a presentation-definition.md file into the normalized DeckModel tree:
  # Section  → SectionModel
  ## Slide   → SlideModel
  ### Card   → CardModel  (with fenced YAML body)

Supports:
- ``<!-- DONE -->`` freeze markers
- ``<!-- slide ... -->`` per-slide override blocks
- fenced YAML card bodies with ``style_overrides`` extraction
"""

from __future__ import annotations

import re
from typing import Any

import yaml

from scripts.models.deck import CardModel, DeckModel, SectionModel, SlideModel

# ── regex patterns ───────────────────────────────────────────────────────────

_RE_SECTION = re.compile(r"^#\s+(.+)$")
_RE_SLIDE = re.compile(r"^##\s+(.+)$")
_RE_CARD = re.compile(r"^###\s+(.+)$")
_RE_DONE = re.compile(r"^\s*<!--\s*DONE\s*-->\s*$", re.IGNORECASE)
_RE_SLIDE_OVERRIDE_START = re.compile(r"^\s*<!--\s*slide\s*$")
_RE_SLIDE_OVERRIDE_END = re.compile(r"^\s*-->\s*$")
_RE_FENCE_START = re.compile(r"^```(yaml|yml)\s*$", re.IGNORECASE)
_RE_FENCE_END = re.compile(r"^```\s*$")


class DeckParser:
    """Parse a presentation-definition Markdown string into a ``DeckModel``."""

    def parse(self, text: str) -> DeckModel:
        """Parse *text* and return a :class:`DeckModel`.

        Args:
            text: The full Markdown source of the presentation definition.

        Returns:
            Populated ``DeckModel`` with sections, slides, and cards.
        """
        lines = text.splitlines()
        deck = DeckModel()
        current_section: SectionModel | None = None
        current_slide: SlideModel | None = None
        current_card: CardModel | None = None

        i = 0
        while i < len(lines):
            line = lines[i]

            # ── # Section ────────────────────────────────────────────────
            m = _RE_SECTION.match(line)
            if m:
                current_section = SectionModel(title=m.group(1).strip())
                deck.sections.append(current_section)
                current_slide = None
                current_card = None
                if not deck.title:
                    deck.title = current_section.title
                i += 1
                continue

            # ── ## Slide ─────────────────────────────────────────────────
            m = _RE_SLIDE.match(line)
            if m:
                current_slide = SlideModel(title=m.group(1).strip())
                current_card = None
                # Ensure there's a section to attach to
                if current_section is None:
                    current_section = SectionModel(title="")
                    deck.sections.append(current_section)
                current_section.slides.append(current_slide)

                # Look ahead for <!-- DONE --> and <!-- slide ... --> blocks
                i += 1
                i = self._parse_slide_markers(lines, i, current_slide)
                continue

            # ── ### Card ─────────────────────────────────────────────────
            m = _RE_CARD.match(line)
            if m:
                current_card = CardModel(title=m.group(1).strip())
                if current_slide is None:
                    # Orphan card — create an implicit slide
                    current_slide = SlideModel(title="")
                    if current_section is None:
                        current_section = SectionModel(title="")
                        deck.sections.append(current_section)
                    current_section.slides.append(current_slide)
                current_slide.cards.append(current_card)
                i += 1
                continue

            # ── Fenced YAML block ────────────────────────────────────────
            if _RE_FENCE_START.match(line) and current_card is not None:
                yaml_lines: list[str] = []
                i += 1
                while i < len(lines) and not _RE_FENCE_END.match(lines[i]):
                    yaml_lines.append(lines[i])
                    i += 1
                if i < len(lines):
                    i += 1  # skip closing fence
                self._apply_card_yaml(current_card, "\n".join(yaml_lines))
                continue

            i += 1

        return deck

    # ── private helpers ──────────────────────────────────────────────────

    def _parse_slide_markers(
        self, lines: list[str], i: int, slide: SlideModel
    ) -> int:
        """Consume optional ``<!-- DONE -->`` and ``<!-- slide … -->`` blocks.

        Returns the updated line index *i*.
        """
        # Check for <!-- DONE -->
        if i < len(lines) and _RE_DONE.match(lines[i]):
            slide.is_frozen = True
            i += 1

        # Check for <!-- slide … --> override block
        if i < len(lines) and _RE_SLIDE_OVERRIDE_START.match(lines[i]):
            yaml_lines: list[str] = []
            i += 1  # skip opening <!-- slide
            while i < len(lines) and not _RE_SLIDE_OVERRIDE_END.match(lines[i]):
                yaml_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1  # skip closing -->
            try:
                data = yaml.safe_load("\n".join(yaml_lines))
                if isinstance(data, dict):
                    slide.slide_overrides = data
            except yaml.YAMLError:
                pass  # malformed YAML; skip silently

        return i

    def _apply_card_yaml(self, card: CardModel, yaml_text: str) -> None:
        """Parse a YAML string and populate card fields."""
        try:
            data = yaml.safe_load(yaml_text)
        except yaml.YAMLError:
            return
        if not isinstance(data, dict):
            return

        card.card_type = data.get("type", card.card_type)
        card.content = data.get("content", card.content)
        card.style_overrides = data.get("style_overrides", card.style_overrides)
        card.props = data.get("props", card.props)
        card.subtitle = str(data.get("subtitle", card.subtitle) or "")
        raw_icon = data.get("icon")
        if isinstance(raw_icon, dict):
            card.icon = raw_icon

        # Collect asset references from content
        self._extract_asset_refs(card)

    def _extract_asset_refs(self, card: CardModel) -> None:
        """Walk the card content dict and collect image/asset paths."""
        refs: list[str] = []
        content = card.content
        if isinstance(content, dict):
            for key in ("image", "logo", "chart", "diagram", "background"):
                if key in content and isinstance(content[key], str):
                    refs.append(content[key])
        card.asset_refs = refs
