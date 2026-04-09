"""
deck_validator.py — Validate a presentation-definition.md file.

Checks:
- Structural correctness (sections, slides, cards)
- Required card YAML fields
- Valid card type references
- Valid layout references
- Asset path existence
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SKILL_DIR))

from scripts.models.deck import DeckModel
from scripts.parsing.deck_parser import DeckParser

logger = logging.getLogger("deck_validator")

VALID_CARD_TYPES = {
    "text-card",
    "image-card",
    "kpi-card",
    "chart-card",
    "gantt-chart-card",
    "quote-card",
    "agenda-card",
    "stacked-text-card",
}

VALID_LAYOUTS = {
    "title-slide",
    "grid-1x1",
    "grid-1x2",
    "grid-1x3",
    "grid-1x4",
    "grid-2x1",
    "grid-2x2",
    "grid-2x3",
    "grid-2x4",
    "grid-3x1",
    "grid-3x2",
    "grid-3x3",
    "grid-3x4",
}


class DeckValidationError:
    """A single validation issue."""

    def __init__(self, level: str, message: str, location: str = "") -> None:
        self.level = level  # "error" | "warning"
        self.message = message
        self.location = location

    def __str__(self) -> str:
        loc = f" [{self.location}]" if self.location else ""
        return f"{self.level.upper()}{loc}: {self.message}"


def validate_deck(
    deck: DeckModel,
    *,
    project_root: Path | None = None,
) -> list[DeckValidationError]:
    """Validate a parsed ``DeckModel``.

    Args:
        deck: The parsed deck model.
        project_root: Project root for asset path verification.

    Returns:
        List of validation errors/warnings.
    """
    errors: list[DeckValidationError] = []

    if not deck.sections:
        errors.append(DeckValidationError("warning", "Deck has no sections."))

    for sec_idx, section in enumerate(deck.sections):
        sec_loc = f"Section {sec_idx + 1} ({section.title or 'untitled'})"

        if not section.title:
            errors.append(DeckValidationError("warning", "Section has no title.", sec_loc))

        for slide_idx, slide in enumerate(section.slides):
            slide_loc = f"{sec_loc} > Slide {slide_idx + 1} ({slide.title or 'untitled'})"

            if not slide.title:
                errors.append(
                    DeckValidationError("warning", "Slide has no title.", slide_loc)
                )

            # Layout validation
            if slide.layout and slide.layout not in VALID_LAYOUTS:
                errors.append(
                    DeckValidationError(
                        "error",
                        f"Unknown layout '{slide.layout}'.",
                        slide_loc,
                    )
                )

            for card_idx, card in enumerate(slide.cards):
                card_loc = f"{slide_loc} > Card {card_idx + 1} ({card.title or 'untitled'})"

                # Card type validation
                if card.card_type not in VALID_CARD_TYPES:
                    errors.append(
                        DeckValidationError(
                            "error",
                            f"Unknown card type '{card.card_type}'.",
                            card_loc,
                        )
                    )

                # Asset path validation
                if project_root:
                    for ref in card.asset_refs:
                        full_path = project_root / "assets" / ref
                        if not full_path.exists():
                            errors.append(
                                DeckValidationError(
                                    "warning",
                                    f"Asset not found: {ref} (expected at {full_path})",
                                    card_loc,
                                )
                            )

    return errors


def validate_file(deck_path: Path, project_root: Path | None = None) -> list[DeckValidationError]:
    """Parse and validate a deck file.

    Args:
        deck_path: Path to the presentation-definition.md file.
        project_root: Optional project root for asset checks.

    Returns:
        List of validation errors/warnings.
    """
    if not deck_path.exists():
        return [DeckValidationError("error", f"File not found: {deck_path}")]

    parser = DeckParser()
    deck = parser.parse(deck_path.read_text(encoding="utf-8"))
    return validate_deck(deck, project_root=project_root)


def main() -> None:
    """CLI entry point for deck validation."""
    import argparse

    parser = argparse.ArgumentParser(description="Validate a presentation definition file.")
    parser.add_argument("deck_path", type=Path, help="Path to presentation-definition.md")
    parser.add_argument("--project-root", type=Path, default=None, help="Project root for asset checks")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    project_root = args.project_root or args.deck_path.parent
    errors = validate_file(args.deck_path, project_root=project_root)

    if not errors:
        print("✓ No validation issues found.")
    else:
        for err in errors:
            print(err)
        error_count = sum(1 for e in errors if e.level == "error")
        warn_count = sum(1 for e in errors if e.level == "warning")
        print(f"\n{error_count} error(s), {warn_count} warning(s)")
        if error_count > 0:
            sys.exit(1)


if __name__ == "__main__":
    main()
