---
name: presentation-design
description: "Card-based presentation design system. Build slide decks from a structured Markdown definition file and a CSS token theme. Cards and layouts are documented, registered, and rendered deterministically by Python scripts into PowerPoint (.pptx) and draw.io (.drawio) output. Use this skill whenever a user asks to create, build, design, or scaffold a presentation, slide deck, or visual document."
argument-hint: "<presentation-definition.md> [--stylesheet <theme.css>] [--output <file.pptx|file.drawio>]"
metadata:
  author: MarkSchue
  version: "0.1.0"
---

# Presentation Design Skill

A card-based, token-driven presentation design system. Slides are defined in
a structured Markdown file (`presentation-definition.md`). All visual styling
is controlled by CSS design tokens in `theme.css`. Python scripts parse the
Markdown, resolve tokens, and export deterministic output to `.pptx` or
`.drawio`.

**Always read `registry.yaml` before loading any other file.** Load card and
layout Markdown specs only for elements you will actually use.

---

## Quick Start

### 1. Scaffold a new presentation

```bash
python scripts/scaffold_presentation.py "My Presentation" --path ~/slides
```

This creates:
```
My Presentation/
├── presentation-definition.md   # your slide content
├── theme.css                    # SPARSE overrides — only tokens you want to change.
│                                # Inherits everything else from the skill's base.css,
│                                # so future base.css updates cascade automatically.
├── output/                      # build output target
└── assets/
    ├── images/
    ├── charts/
    ├── diagrams/
    └── logos/
```

### 2. Edit `presentation-definition.md`

Use the structured Markdown syntax (see `references/deck-syntax.md`):

```markdown
# Introduction

## Welcome Slide
### Main Message
```yaml
type: text-card
content:
  heading: "Welcome to Our Presentation"
  body: "A brief overview of key topics."
```​

## Key Metrics
### Revenue
```yaml
type: kpi-card
content:
  value: "$4.2M"
  trend: "up"
  label: "Annual Revenue"
```​

# Results
## ...
```

### 3. Build the presentation

```bash
python scripts/build_presentation.py presentation-definition.md \
  --stylesheet theme.css \
  --output output/presentation.pptx
```

---

## Assembly Pipeline

Follow in sequence. Do not skip or reorder.

### Phase 1 — Planning
- If input is raw/unstructured content: create a structured
  `presentation-definition.md` with `#` sections, `##` slides, `###` cards,
  and YAML card blocks. Ask clarifying questions before producing output.
- If a structured file is already provided, skip to Phase 2.

### Phase 1b — Numbering Sync (automatic, every build)
- If `presentation-definition.md` contains a `<!-- numbering … -->` block,
  `sync_numbering.py` resolves and renumbers all `%%` placeholders **before**
  parsing. Both bare `%%` and previously-resolved numbers (e.g. `US-PH01-03`)
  are matched so that insertions, deletions, and reorderings always produce a
  gap-free sequence. See `references/deck-syntax.md#numbering-ranges`.

### Phase 2 — Selection
- Load `registry.yaml`. For each slide, select a layout and cards.
- Report every automatic design decision so the user can override.
- Prefer tags matching the slide's domain/content.

### Phase 3 — Retrieval
- Load only the Markdown spec files for layouts and cards selected in Phase 2.
- Do not speculatively load all card/layout specs.

### Phase 4 — Theming
- Load the project's `theme.css` once per invocation (not per slide).
- Apply the token override chain: per-card override → per-slide override →
  variant CSS class → base CSS class → Python fallback default.

### Phase 5 — Agenda Injection
- Parse all `#` section headings.
- Generate an agenda data model once.
- Inject an agenda slide at each section boundary with the current section
  highlighted and others muted.
- Dynamic column layout: 1–4 sections → 1 col; 5–8 → 2 cols; 9+ → 3 cols.

### Phase 6 — Assembly
- Produce the target file (`.pptx`, `.drawio`, or both).
- Log: layouts/cards used, theme tokens applied, output format.
- If a required card type is missing, halt and report before producing output.
- Respect `<!-- DONE -->` below any `## Slide Title` — never modify frozen
  slides.

---

## Skill Folder Structure

```
presentation-design/
├── SKILL.md              this file
├── registry.yaml         card/layout/script registry — read FIRST
├── registry-tags.yaml    keyword tags for registry lookup
├── requirements.txt      Python dependencies
├── .venv/                skill-local virtual environment
├── references/
│   ├── deck-syntax.md    presentation definition syntax
│   ├── token-reference.md  CSS token catalogue
│   ├── setup.md          environment setup guide
│   ├── architecture.md   system architecture
│   └── inheritance-model.md  Python/CSS inheritance
├── cards/
│   ├── text/             text-card.md, stacked-text-card.md, icon_item_text.md, numbered_text_card.md
│   ├── media/            image-card.md
│   ├── data/             kpi-card.md, chart-card.md, gantt-chart-card.md, table-card.md, stat-grid-card.md
│   └── structural/       agenda-card.md, quote-card.md, timeline-card.md,
│                         scope-card.md, compare-card.md, heatmap-card.md, callout-card.md,
│                         section-divider-card.md, quadrant-card.md,
│                         process-flow-card.md, pyramid-card.md,
│                         step-card.md, gauge-card.md,
│                         circular-infographic-card.md,
│                         calendar-card.md
├── layouts/
│   ├── title-slide.md
│   ├── grid-1x1.md … grid-3x4.md
├── themes/
│   ├── base.css          full token set — source-of-truth template
│   └── default-theme.css reference-only sparse override example
├── scripts/
│   ├── models/           domain classes
│   ├── parsing/          Markdown + YAML parser
│   ├── rendering/        card and layout renderers
│   ├── exporting/        PPTX and draw.io exporters (always kept in sync)
│   ├── validation/       lint and schema checks
│   ├── cli/              thin CLI wrappers for all scripts
│   ├── build_presentation.py  main build orchestrator
│   ├── scaffold_presentation.py
│   ├── sync_numbering.py      pre-build %%-placeholder resolver
│   └── extract_theme.py  (future: token extraction from PPTX/web)
└── examples/
    ├── minimal-presentation-definition.md
    └── minimal-theme.css
```

---

## Environment Setup

This skill uses one canonical virtual environment at
`skills/presentation-design/.venv`.

```bash
cd skills/presentation-design
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run all scripts through this venv:
```bash
.venv/bin/python scripts/build_presentation.py <args>
```

See `references/setup.md` for full details.

For Python/CSS class hierarchy and the token resolution chain see
`references/inheritance-model.md`.

---

## Token Override Chain

All visual values are resolved through a single precedence chain. No renderer
may short-circuit this order.

1. **Per-card override** — `style_overrides:` in the card's YAML block
2. **Per-slide override** — `<!-- slide ... -->` comment block below `## Title`
3. **Variant CSS class** — e.g. `.card--kpi`, `.layout--grid-2x2`
4. **Base CSS class** — `.slide-base`, `.card-base`
5. **Python fallback default** — hardcoded safe value in renderer

### Base Token Override Pattern

Typography tokens (`--card-heading-font-*`, `--card-body-font-*`, `--card-label-font-*`)
are defined once in `.card-base` with sensible defaults. Card variant classes override
**only the values that differ** from those base defaults:

```css
/* ✓ Correct — override the base token inside the variant scope */
.card--agenda {
  --card-heading-font-weight: 600;       /* semibold — overrides base 700 */
  --card-body-font-color: var(--color-text-muted);  /* overrides base text-subtle */
}

/* ✗ Avoid — redundant variant-specific alias when value matches base */
.card--stacked-text {
  --card-stacked-text-heading-font-size: 14;  /* same as base 14 — no-op */
}
```

In per-card `style_overrides:` YAML, use the base token names to scope a value
to that one card instance:

```yaml
style_overrides:
  card-heading-font-color: "#003087"   # scopes to this card only
  card-body-font-size: 12              # scopes to this card only
```

---

## Design Principles

### 1 — No Hardcoded Visual Values
Every color, font size, spacing, radius, and font family must come from the
theme token system. No literal hex codes, pixel values, or font names in
renderer code.

### 2 — CSS Extensibility
New tokens may be freely added or renamed — update all renderers, CSS, and docs in the same commit. Every token must have a safe default and an inline comment in the CSS file.

### 3 — Registry-First Discovery
Read `registry.yaml` before loading any spec file. Load specs only for the
cards/layouts actually needed.

### 4 — Deterministic Python Rendering
All layout, parsing, and styling logic lives in Python scripts. The Markdown
file is content only. The CSS file is tokens only. Python is the orchestrator.

### 5 — Frozen Slide Protection
Any slide with `<!-- DONE -->` below its `## Title` is frozen and must not
be modified during rendering.

### 6 — Shared Card Contract
All cards share one base card system: common title, header line, body region,
container styling, **and footer**. The footer area (optional text + optional
divider line above it) is implemented entirely in `BaseCardRenderer` and
activates automatically for every card type. No subclass code is needed:
- Enable the footer line: set `--card-footer-line-visible: true` in CSS or `style_overrides`
- Supply footer text: add `content.footer: "…"` to the card YAML
Specialized cards extend — never replace — the base.

---

## Diagram Design Principles

Diagrams are architecture or flow drawings embedded in slides via the
`image-card` type.  The build pipeline converts draw.io source files to SVG
automatically.

### 7 — One Draw.io File, Multiple Named Tabs

All diagrams for a single topic belong in one `.drawio` file as named pages
(tabs).  Never create a separate file per diagram.

```
assets/diagrams/
  application-landscape.drawio    ← multi-tab source
  current-state.svg               ← auto-generated by the build
  target-state.svg                ← auto-generated by the build
```

### 8 — YAML Reference Format

Reference a diagram in a card's YAML using `"relative/path.drawio#page-name"`:

```yaml
type: image-card
subtitle: "Single global S/4HANA — China access via unrestricted WAN"
content:
  source: "diagrams/application-landscape.drawio#current-state"
  image_style: fullbleed
```

- The `source` path is relative to `assets/` (same convention as all other assets).
- The fragment `#page-name` must match the draw.io page name exactly.
- No `assets/` prefix in the value — the renderer adds it.
- Use `content.source` (preferred) or `content.image` for the path.
- Put `image_style` inside `content:`, not at the top level (top-level keys are ignored by the parser).

### 9 — Build-Time SVG Generation

At render time `image_card.py` detects the `.drawio#page-name` syntax and calls
`scripts/rendering/drawio_renderer.py`, which:

1. Reads the `.drawio` XML and extracts the named page.
2. Converts the page's `mxGraphModel` cells to SVG.
3. Writes `{page-name}.svg` next to the `.drawio` source file.
4. Returns the SVG path to the image-card renderer.

The SVG is **only regenerated when the `.drawio` source is newer** than the
cached SVG (mtime-based).  To force regeneration, touch the `.drawio` file or
delete the cached `.svg`.

### 10 — Design Diagrams at Image-Card Body Dimensions

Before placing content in a draw.io page, set the page dimensions to match the
image-card body area to avoid letterboxing:

| Scenario | Recommended page size |
|---|---|
| `image_style: fullbleed` + title + subtitle | 1280 × 648 px |
| `image_style: fullbleed` + title only | 1280 × 664 px |
| `image_style: fullbleed` + no title | 1280 × 720 px (full canvas) |

These values assume the default canvas of **1280 × 720 px**.  If the theme
overrides `--canvas-width` / `--canvas-height`, adjust proportionally.

In the draw.io `mxGraphModel`, set `pageWidth` and `pageHeight` accordingly:

```xml
<mxGraphModel pageWidth="1280" pageHeight="648" ...>
```

The renderer uses these values as the SVG `viewBox`, ensuring the content
fills the slide area at 1:1 without scaling distortion.

### 11 — Supported mxGraph Feature Subset

Only use the following mxGraph features.  The Python renderer does **not**
support the full mxGraph specification.

| Feature | Supported styles |
|---|---|
| Rectangle vertex | `fillColor`, `strokeColor`, `strokeWidth`, `rounded`, `arcSize`, `dashed`, `opacity` |
| Ellipse vertex | same as rectangle + `perimeter=ellipsePerimeter` in style |
| Text-only vertex | `text` flag in style + `fillColor=none`, `strokeColor=none` |
| Edge / connector | `strokeColor`, `strokeWidth`, `endArrow`, `startArrow`, `dashed`, waypoints |
| Label (all shapes) | `fontColor`, `fontSize`, `fontStyle` (bitmask: 1=bold, 2=italic), `align`, `verticalAlign` |
| Multi-line labels | use `&#xa;` or literal newline in the `value` attribute |

**Not supported**: `mxgraph.*` shape libraries, swimlanes, tables, images embedded
in cells, HTML rich text beyond tag stripping, curved edges, gradient fills.

### 12 — Use Brand Colours from Theme Tokens

All colours used in diagrams must be sourced from the project's theme palette.
Never introduce ad-hoc hex codes.  Document any new colour in the theme file
before using it in a diagram.

For the LAPP project:

| Token name | Hex | Usage |
|---|---|---|
| `--color-primary` | `#EE711C` | RoW zone, SAP core modules |
| `--color-secondary` | `#1A1A1A` | Titles, outlines, HANA DB |
| `--color-accent` | `#E2001A` | China zone, risk callouts |
| `--color-success` (custom) | `#22C55E` | Target-state CN elements |
| Light orange | `#F2A05A` | SAP extended modules |
| Light grey | `#F2F2F2` | Master data tiles |
| RISE green | `#84CC16` | CN secondary modules |
| Risk amber | `#FFE4B5` | Risk callout backgrounds |

### 13 — Fill the Allocated Slot; Never Letterbox or Stretch

A fullbleed diagram image must use every available pixel in the card body area.
Whitespace around a diagram and distorted shapes both look unprofessional.

**How the renderer achieves this**

Generated SVGs have `preserveAspectRatio="xMidYMid slice"` which is CSS
`object-fit: cover`.  Given a viewBox of the designed page size and the actual
card-body width × height as the SVG `width`/`height` attributes:

- The content is scaled so **both dimensions fill the allocation** (no letterboxing).
- If the slot aspect ratio differs from the design ratio, the SVG **symmetrically
  clips** the excess from whichever axis overflows.
- The PPTX exporter places the SVG at exactly `(x, y, card_body_w, card_body_h)`
  and lets the SVG handle the rest internally.
- The draw.io exporter uses `imageAspect=0` so the draw.io renderer also defers
  to the SVG's own `preserveAspectRatio`.

**Design the draw.io page at the actual card body ratio**

The card body ratio changes with the slide's chrome (title, subtitle, footer,
take-away bar, card header, padding).  The build pipeline prints the actual box
dimensions in the WARNING log if an image is not found; otherwise, calculate:

```
slot_w = canvas_w  - canvas_padding_left - canvas_padding_right
slot_h = canvas_h  - canvas_padding_top  - canvas_padding_bottom
       - slide_title_height              (title_font * 1.2 + 8)
       - slide_divider                   (1 + 8 px)
       - take_away_bar                   (~48 px if present)
       - footer                          (~24 px if present)
       - card_title_height               (card_title_font * 1.2 + title_line_gap + 1 px line)
       - card_subtitle_height            (sub_font + margin_top + margin_bottom, if present)
       - 2 × card_padding
```

For the LAPP deck (grid-1x1, with slide title, take-away, card title, no subtitle):

| Dimension | Approximate value |
|---|---|
| `slot_w` | 1184 px |
| `slot_h` | 495 px |
| Ratio | ≈ 2.39 : 1 |

Designing the draw.io page at `1184 × 495` (or `2390 × 990` for higher fidelity)
will result in **zero clipping**.

**Safe zone guideline — if designing at non-exact dimensions**

When the page ratio cannot exactly match the slot ratio, keep all critical
content (zone boundaries, module boxes, key text) within a **safe zone** of at
least 40 px from each edge.  The `slice` crop is symmetric: content outside the
safe zone may be clipped when the slide is rendered.

Do **not** place important content (title bars, legends, call-out boxes) at the
very edge of the page if the design ratio differs from the slot ratio.

---

## Adding a New Card Type

Follow these six steps to add a fully supported card type to the skill.
All steps are required; omitting any one will leave the pipeline, theme, or
documentation out of sync.

### Step 1 — Write the renderer

Create `scripts/rendering/<name>_card.py`:

```python
from scripts.rendering.base_card import BaseCardRenderer, RenderBox
from scripts.models.deck import CardModel

class MyCardRenderer(BaseCardRenderer):
    """Renderer for ``my-card`` type."""
    variant = "card--my"

    def render_body(self, card: CardModel, box: RenderBox) -> None:
        # Token access: self._tok("my-token", default)
        # Float shorthand: self._f("my-size", 14.0)
        ...
```

`BaseCardRenderer` automatically handles the card container, title, header line,
icon, subtitle, and footer.  Override only `render_body`.

### Step 2 — Register in the build pipeline

Add the new card type to `_card_renderer_for()` in
`scripts/build_presentation.py`:

```python
if card_type in ("my-card", "my_card"):
    return MyCardRenderer(theme)
```

Also add the import at the top of the file.

### Step 3 — Add CSS tokens

Add a `.card--my` variant block to `themes/base.css`:

```css
.card--my {
    /* My-card-specific tokens */
    --card-my-body-font-size:   14;
    --card-my-body-font-color:  var(--color-text-primary);
    /* Footer overrides (shared with all card types) */
    /* --card-footer-line-visible: false; */
}
```

### Step 4 — Register in registry.yaml

Add an entry to `registry.yaml` and `registry-tags.yaml`:

```yaml
# registry.yaml
- id: my-card
  label: My Card
  category: text          # text | data | media | structural
  renderer: scripts/rendering/my_card.py
  css_variant: card--my
  description: "One-line description."
```

### Step 5 — Write the card spec

Create `cards/<category>/my-card.md`.  Use an existing spec as a template.
The spec must include:
- `content.footer` in the Optional Fields table
- A "Footer tokens (shared with all card types)" sub-section in Supported Overrides
- The footer zone in the `## Layout` pictogram
- `.card-base` footer tokens in `## Design Tokens Used`

### Step 6 — Update reference documentation

- Add the new class to the Python and CSS hierarchies in
  `references/inheritance-model.md`.
- Add all new CSS tokens to `references/token-reference.md`.

> **Verification:** rebuild the test deck with `--format both` and confirm the
> new card type renders without errors or warnings.


