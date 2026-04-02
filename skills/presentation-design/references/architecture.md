# System Architecture

## Pipeline Overview

```
presentation-definition.md ──┐
                             │
theme.css ───────────────────┤
                             ▼
                    ┌─────────────────┐
                    │   DeckParser    │  Parse MD → sections, slides, cards
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  ThemeLoader    │  Parse CSS → token dict
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ AgendaInjector  │  Generate + inject agenda slides
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ SlideFreezeGuard│  Skip <!-- DONE --> slides
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Layout Resolver │  Select layout renderer per slide
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Card Resolver  │  Select card renderer per card
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    Exporter     │  PPTX or draw.io output
                    └─────────────────┘
```

## Module Map

```
scripts/
├── build_presentation.py     CLI entry point — orchestrates pipeline
├── scaffold_presentation.py  Project scaffolder
├── extract_theme.py          (future) Token extraction
├── models/
│   ├── __init__.py
│   ├── deck.py               DeckModel, SectionModel, SlideModel, CardModel
│   ├── theme.py              ThemeTokens, SlideTheme, CardTheme
│   └── agenda.py             AgendaModel
├── parsing/
│   ├── __init__.py
│   ├── deck_parser.py        Markdown → DeckModel
│   ├── yaml_extractor.py     YAML block extraction + normalization
│   └── slide_overrides.py    Per-slide override parsing
├── rendering/
│   ├── __init__.py
│   ├── base_card.py          BaseCardRenderer
│   ├── text_card.py          TextCardRenderer
│   ├── image_card.py         ImageCardRenderer
│   ├── kpi_card.py           KpiCardRenderer
│   ├── chart_card.py         ChartCardRenderer
│   ├── quote_card.py         QuoteCardRenderer
│   ├── agenda_card.py        AgendaCardRenderer
│   ├── base_layout.py        BaseLayoutRenderer
│   ├── title_slide.py        TitleSlideLayoutRenderer
│   └── grid_layout.py        GridLayoutRenderer
├── exporting/
│   ├── __init__.py
│   ├── pptx_exporter.py      PptxExporter
│   └── drawio_exporter.py    DrawioExporter
├── validation/
│   ├── __init__.py
│   ├── deck_validator.py     Deck syntax checks
│   └── token_validator.py    CSS token lint
└── cli/
    └── __init__.py
```

## Data Flow

1. `build_presentation.py` receives `presentation-definition.md` + `theme.css`
2. `DeckParser` produces `DeckModel` (list of `SectionModel` → `SlideModel` → `CardModel`)
3. `ThemeLoader` produces `ThemeTokens` (flat dict of all resolved token values)
4. `AgendaInjector` reads sections from `DeckModel`, creates agenda `SlideModel` entries
5. `SlideFreezeGuard` marks frozen slides (`is_frozen = True`)
6. For each non-frozen slide, the pipeline:
   a. Resolves a `LayoutRenderer` based on card count or explicit `<!-- layout: -->` tag
   b. Resolves a `CardRenderer` for each card based on `type` field
   c. Applies token override chain: card override → slide override → variant → base → fallback
7. `Exporter` writes the final slide objects to `.pptx` or `.drawio`
