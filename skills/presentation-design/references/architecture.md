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


## Token Inheritance Pattern

All card renderers use a **two-step card-base fallback** for shared typographic
properties. This ensures consistent typography across all card types by default,
while still allowing per-card overrides in CSS.

### Resolution chain for body/heading tokens

```
card-{variant}-{name}   (e.g. --card-timeline-body-font-size)
        ↓ absent/empty
card-{name}             (e.g. --card-body-font-size  in .card-base)
        ↓ absent/empty
Python default          (hardcoded in renderer as last resort)
```

### Implementation

`BaseCardRenderer` exposes a `_resolve_tok(variant_prefix, name, default)` method
that implements this chain. Card renderers call it via a local `_tok` helper:

```python
# In every card renderer:
def _tok(self, name: str, default: Any = None) -> Any:
    return self._resolve_tok("my-card", name, default)

def _f(self, name: str, default: float) -> float:
    return float(self._tok(name, default))

# Usage — variant-specific first, card-base fallback automatic:
b_size  = float(self._tok("body-font-size",    14))
h_color = self._tok("heading-font-color", "#1A1A1A")
```

### Shared base tokens in `.card-base`

These tokens in `.card-base` define the global defaults that all cards inherit
when their variant-specific token is absent or commented out:

| Token | Default | Purpose |
|---|---|---|

---

## Design Principles

### Body ↔ Bullets are interchangeable

**Every card that accepts a `body` field also accepts a `bullets` list as an
alternative (or replacement) for that body text.**  This is a universal
content-model rule, not a per-card feature.

When `bullets` is present, the renderer calls `BaseCardRenderer._emit_bullet_list()`
and emits a native `bullet_list` element (OOXML `<a:buChar>` in PPTX;
HTML `<br/>`-separated spans in draw.io) instead of a plain `text` element.
Bullet style, colour, character, and indent are all controlled via
`--card-bullet-*` CSS tokens so the design can be overridden globally or
per-card without touching renderer code.

```yaml
# plain body — always valid
content:
  heading: "Our Approach"
  body: "We focus on quality and delivery."

# bullet variant — valid on every card type with a body slot
content:
  heading: "Our Approach"
  bullets:
    - "Quality over speed"
    - "Continuous delivery"
    - "Data-driven decisions"
```

**Implementation rule:** Every new card renderer that renders a `body` field **must**
also check for a `bullets` list in the same content slot and delegate to
`self._emit_bullet_list()` when the list is non-empty.  The height estimation
lookup must likewise call `self._bullet_list_height()` for the bullets branch.
See `BaseCardRenderer._emit_bullet_list` and `_bullet_list_height` in
`rendering/base_card.py` for the shared implementation.
| `--card-body-font-size` | `14` px | Body text size |
| `--card-body-font-color` | `var(--color-text-subtle)` | Body text colour |
| `--card-body-font-weight` | `400` | Body text weight |
| `--card-body-font-style` | `normal` | Body text style |
| `--card-body-alignment` | `left` | Body paragraph alignment |
| `--card-heading-font-size` | `14` px | Heading size inside card body |
| `--card-heading-font-color` | `var(--color-text-default)` | Heading colour |
| `--card-heading-font-weight` | `700` | Heading weight |
| `--card-heading-font-style` | `normal` | Heading style |
| `--card-heading-alignment` | `left` | Heading alignment |

### Rules for new card renderers

1. **Always define a `_tok` helper** using `_resolve_tok` — never call
   `self.resolve(f"card-{variant}-{name}")` directly for body/heading tokens.
2. **Variant-specific CSS tokens are optional** — the base defaults apply
   automatically. Only add variant tokens to override the default.
3. **Card-specific structural tokens** (e.g. `--card-timeline-spine-color`)
   have no base equivalent; use `_tok` with an explicit fallback default.
4. **Never hardcode hex colours** as defaults if a semantic colour token exists
   in `.card-base` — reference it via `_resolve_tok` instead.
