#!/usr/bin/env python3
"""
build_presentation.py — Main CLI entry point for building a presentation.

Usage:
    python scripts/cli/build_presentation.py <project_dir> [--format pptx|drawio|both]

Pipeline:
    1. Load registry
    2. Parse presentation-definition.md
    3. Load CSS theme tokens
    4. Inject agenda slides
    5. Skip frozen slides
    6. Resolve layout renderer per slide
    7. Resolve card renderer per card
    8. Export to target format(s)
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Ensure the skill scripts directory is on the path
SKILL_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SKILL_DIR))

from scripts.models.deck import DeckModel, SlideModel
from scripts.models.theme import ThemeTokens
from scripts.parsing.deck_parser import DeckParser
from scripts.parsing.theme_loader import ThemeLoader
from scripts.rendering.agenda_injector import AgendaInjector
from scripts.rendering.base_card import BaseCardRenderer, RenderBox
from scripts.rendering.base_layout import BaseLayoutRenderer
from scripts.rendering.grid_layout import GridLayoutRenderer, create_grid_renderer
from scripts.rendering.title_slide import TitleSlideLayoutRenderer
from scripts.rendering.text_card import TextCardRenderer
from scripts.rendering.image_card import ImageCardRenderer
from scripts.rendering.kpi_card import KpiCardRenderer
from scripts.rendering.chart_card import ChartCardRenderer
from scripts.rendering.quote_card import QuoteCardRenderer
from scripts.rendering.agenda_card import AgendaCardRenderer
from scripts.rendering.stacked_text_card import StackedTextCardRenderer
from scripts.exporting.pptx_exporter import PptxExporter
from scripts.exporting.drawio_exporter import DrawioExporter

logger = logging.getLogger("build_presentation")


# ── Card renderer registry ──────────────────────────────────────────────────

def _card_renderer_for(
    card_type: str, theme: ThemeTokens, project_root: Path
) -> BaseCardRenderer:
    """Return the correct card renderer instance for *card_type*."""
    if card_type == "text-card":
        return TextCardRenderer(theme)
    if card_type == "image-card":
        return ImageCardRenderer(theme, project_root=project_root)
    if card_type == "kpi-card":
        return KpiCardRenderer(theme)
    if card_type == "chart-card":
        return ChartCardRenderer(theme, project_root=project_root)
    if card_type == "quote-card":
        return QuoteCardRenderer(theme)
    if card_type == "agenda-card":
        return AgendaCardRenderer(theme)
    if card_type == "stacked-text-card":
        return StackedTextCardRenderer(theme)
    logger.warning("Unknown card type '%s' — falling back to text-card", card_type)
    return TextCardRenderer(theme)


# ── Layout renderer registry ────────────────────────────────────────────────

def _layout_renderer_for(
    layout_id: str | None, card_count: int, theme: ThemeTokens
) -> BaseLayoutRenderer:
    """Return the correct layout renderer for *layout_id* or auto-select."""
    if layout_id == "title-slide":
        return TitleSlideLayoutRenderer(theme)
    if layout_id and layout_id.startswith("grid-"):
        return create_grid_renderer(layout_id, theme)

    # Auto-select based on card count
    auto_map = {
        0: "title-slide",
        1: "grid-1x1",
        2: "grid-1x2",
        3: "grid-1x3",
        4: "grid-2x2",
        5: "grid-2x3",  # 5 cards → 2×3 with one empty
        6: "grid-2x3",
        7: "grid-2x4",  # 7 cards → 2×4 with one empty
        8: "grid-2x4",
        9: "grid-3x3",
        10: "grid-3x4",  # 10–12 → 3×4
        11: "grid-3x4",
        12: "grid-3x4",
    }
    resolved = auto_map.get(card_count, "grid-3x4")
    if resolved == "title-slide":
        return TitleSlideLayoutRenderer(theme)
    return create_grid_renderer(resolved, theme)


# ── Build pipeline ──────────────────────────────────────────────────────────

def build(project_dir: Path, output_format: str = "both") -> None:
    """Run the full build pipeline.

    Args:
        project_dir: Path to the presentation project folder.
        output_format: ``pptx``, ``drawio``, or ``both``.
    """
    # 1. Locate source files
    deck_path = project_dir / "presentation-definition.md"
    if not deck_path.exists():
        # Also try deck.md for compatibility
        deck_path = project_dir / "deck.md"
    if not deck_path.exists():
        logger.error("No presentation-definition.md found in %s", project_dir)
        sys.exit(1)

    theme_path = project_dir / "theme.css"
    base_css = SKILL_DIR / "themes" / "base.css"

    # 2. Parse deck
    parser = DeckParser()
    deck = parser.parse(deck_path.read_text(encoding="utf-8"))
    logger.info("Parsed %d sections, %d total slides", len(deck.sections), len(deck.all_slides))

    # 3. Load theme tokens (base → project theme)
    loader = ThemeLoader()
    theme_files = [base_css]
    if theme_path.exists():
        theme_files.append(theme_path)
    theme = loader.load(*theme_files)

    # 4. Inject agenda slides
    injector = AgendaInjector()
    deck = injector.inject(deck)
    logger.info("After agenda injection: %d total slides", len(deck.all_slides))

    # 5–8. Render each slide
    rendered_slides: list[RenderBox] = []
    page_num = 1

    for slide in deck.all_slides:
        # Skip frozen slides — preserve as-is (empty render)
        if slide.is_frozen:
            logger.info("Skipping frozen slide: %s", slide.title)
            # Still need a placeholder canvas for the exporter
            canvas_w = int(theme.resolve("canvas-width") or 1280)
            canvas_h = int(theme.resolve("canvas-height") or 720)
            placeholder = RenderBox(0, 0, canvas_w, canvas_h)
            placeholder.add({
                "type": "rect", "x": 0, "y": 0,
                "w": canvas_w, "h": canvas_h,
                "fill": "#FFFFFF", "rx": 0,
            })
            placeholder.add({
                "type": "text", "x": canvas_w * 0.3, "y": canvas_h * 0.45,
                "w": canvas_w * 0.4, "text": f"[FROZEN] {slide.title}",
                "font_size": 18, "font_color": "#AAAAAA", "alignment": "center",
            })
            rendered_slides.append(placeholder)
            page_num += 1
            continue

        # Resolve layout
        layout_renderer = _layout_renderer_for(
            slide.layout, len(slide.cards), theme
        )
        canvas = layout_renderer.render(slide, page_number=page_num)

        # Render cards into slots
        card_slots = getattr(canvas, "card_slots", [])
        for i, card in enumerate(slide.cards):
            if i >= len(card_slots):
                logger.warning(
                    "Slide '%s': card '%s' exceeds slot count (%d slots)",
                    slide.title, card.title, len(card_slots),
                )
                break
            slot = card_slots[i]
            renderer = _card_renderer_for(card.card_type, theme, project_dir)
            renderer.render(card, slot, slide_overrides=slide.slide_overrides)
            canvas.elements.extend(slot.elements)

        rendered_slides.append(canvas)
        page_num += 1

    # 9. Export
    output_dir = project_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    canvas_w = int(theme.resolve("canvas-width") or 1280)
    canvas_h = int(theme.resolve("canvas-height") or 720)

    if output_format in ("pptx", "both"):
        pptx_exp = PptxExporter(project_root=project_dir)
        pptx_exp.export(
            rendered_slides,
            output_dir / "presentation.pptx",
            canvas_width=canvas_w,
            canvas_height=canvas_h,
        )

    if output_format in ("drawio", "both"):
        drawio_exp = DrawioExporter(project_root=project_dir)
        drawio_exp.export(
            rendered_slides,
            output_dir / "presentation.drawio",
            canvas_width=canvas_w,
            canvas_height=canvas_h,
        )

    logger.info("Build complete — %d slides exported to %s", len(rendered_slides), output_dir)


# ── CLI ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a presentation from a structured Markdown definition."
    )
    parser.add_argument(
        "project_dir",
        type=Path,
        help="Path to the presentation project folder.",
    )
    parser.add_argument(
        "--format",
        choices=["pptx", "drawio", "both"],
        default="both",
        dest="output_format",
        help="Output format (default: both).",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging.",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    build(args.project_dir.resolve(), args.output_format)


if __name__ == "__main__":
    main()
