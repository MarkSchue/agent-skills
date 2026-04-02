---
name: presentation-design
description: >
  Card-based presentation design system. Build slide decks from a structured
  Markdown definition file and a CSS token theme. Cards and layouts are
  documented, registered, and rendered deterministically by Python scripts
  into PowerPoint (.pptx) and draw.io (.drawio) output.
  Use this skill whenever a user asks to create, build, design, or scaffold
  a presentation, slide deck, or visual document.
metadata:
  author: MarkSchue
  version: "0.1.0"
  argument-hint: <presentation-definition.md> [--stylesheet <theme.css>] [--output <file.pptx|file.drawio>]
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
├── theme.css                    # copied from skill template — customise here
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
│   ├── text/             text-card.md
│   ├── media/            image-card.md
│   ├── data/             kpi-card.md, chart-card.md
│   └── structural/       agenda-card.md, quote-card.md
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
│   ├── exporting/        PPTX and draw.io exporters
│   ├── validation/       lint and schema checks
│   ├── scaffold_presentation.py
│   ├── build_presentation.py
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

---

## Token Override Chain

All visual values are resolved through a single precedence chain. No renderer
may short-circuit this order.

1. **Per-card override** — `style_overrides:` in the card's YAML block
2. **Per-slide override** — `<!-- slide ... -->` comment block below `## Title`
3. **Variant CSS class** — e.g. `.card--kpi`, `.layout--grid-2x2`
4. **Base CSS class** — `.slide-base`, `.card-base`
5. **Python fallback default** — hardcoded safe value in renderer

---

## Design Principles

### 1 — No Hardcoded Visual Values
Every color, font size, spacing, radius, and font family must come from the
theme token system. No literal hex codes, pixel values, or font names in
renderer code.

### 2 — CSS Extensibility Without Breakage
New tokens may be appended but never renamed. Every new token must have a safe
default. Every token must have an inline comment in the CSS file.

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
and container styling. Specialized cards extend — never replace — the base.
