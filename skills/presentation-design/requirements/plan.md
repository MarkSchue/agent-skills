# Implementation Plan for `presentation-design` Skill

## Goal
Build a new reusable skill for creating presentations from structured Markdown using:
- a card-based design system
- CSS token-driven theming
- documented slide layouts and card types
- deterministic Python renderers for PowerPoint and draw.io export
- a registry-first workflow so future agents can inspect capability quickly without loading all docs

---

## 1. Target Deliverables

The skill should ship with these core artifacts:

1. `SKILL.md`
   - defines what the skill does
   - explains when to use it
   - explains the workflow for reading registry files first

2. Registry YAML files
   - `registry.yaml` for cards, layouts, scripts, and references
   - optional `registry-tags.yaml` for keyword/tag lookup

3. Structured documentation
   - one Markdown spec per card
   - one Markdown spec per layout
   - each spec starts with a character-based layout pictogram
   - each spec documents parameters, required fields, optional fields, override tokens, and examples

4. Theme system
   - base CSS token class for slide-level styling
   - base CSS token class for card-level styling
   - subclass/variant classes for specific card and layout types

5. Python renderer stack
   - markdown parser
   - agenda injector
   - theme/token loader
   - layout engine
   - card renderer registry
   - exporters for `.pptx` and `.drawio`

6. Shared Python environment
   - one skill-local virtual environment inside the skill folder
   - one requirements file for all renderer dependencies

7. Examples and validation
   - sample `presentation-definition.md`
   - sample `theme.css`
   - validation/lint scripts for schema and token usage

8. Presentation scaffolding workflow
   - a CLI/script command to scaffold a new presentation project in one step
   - generated files include `presentation-definition.md`, `theme.css`, `output/`, and `assets/`
   - generated folder tree must match the required structure exactly
   - include usage docs and customization guidance in generated files/references
   - `theme.css` is copied from the skill-level theme template (not generated from scratch)

---

## 2. Proposed Skill Folder Structure

```text
skills/presentation-design/
├── SKILL.md
├── registry.yaml
├── registry-tags.yaml
├── requirements.txt
├── .venv/
├── references/
│   ├── deck-syntax.md
│   ├── token-reference.md
│   ├── architecture.md
│   └── inheritance-model.md
├── cards/
│   ├── text/
│   ├── media/
│   ├── data/
│   └── structural/
├── layouts/
│   ├── title-slide.md
│   ├── grid-1x1.md
│   ├── grid-1x2.md
│   ├── grid-1x3.md
│   ├── grid-1x4.md
│   ├── grid-2x1.md
│   ├── grid-2x2.md
│   ├── grid-2x3.md
│   ├── grid-2x4.md
│   ├── grid-3x1.md
│   ├── grid-3x2.md
│   ├── grid-3x3.md
│   └── grid-3x4.md
├── themes/
│   ├── base.css
│   └── default-theme.css
├── scripts/
│   ├── models/
│   ├── parsing/
│   ├── rendering/
│   ├── exporting/
│   ├── validation/
│   ├── cli/
│   ├── scaffold_presentation.py
│   ├── extract_theme.py  # Future-proofing for extracting design tokens from PPTX/Websites
│   └── build_presentation.py
└── examples/
    ├── minimal-presentation-definition.md
    └── minimal-theme.css
```

This keeps documentation, registry data, theme assets, and Python logic separated and scalable.

### 2.1 Required scaffolded presentation project structure

The scaffold command must generate this exact project structure for each new presentation:

```text
presentation-name/
├── presentation-definition.md
├── theme.css
├── output/
│   ├── presentation.pptx
│   └── presentation.drawio
└── assets/
   ├── images/
   ├── charts/
   ├── diagrams/
   └── logos/
```

Implementation note:
- `presentation.pptx` and `presentation.drawio` should be created as placeholder targets (e.g., via `.gitkeep` or documented output expectations) so the folder shape is immediately visible after scaffolding.

---

## 3. Architecture Decisions

### 3.1 Source-of-truth split
- Markdown deck = presentation content and per-instance overrides
- CSS = theme tokens, layout defaults, and style inheritance
- Python = parsing, validation, layout resolution, inheritance logic, agenda injection, and exporting
- Registry YAML = capability discovery for agents and future automation

### 3.2 Registry-first workflow
Before reading all specs, the agent should:
1. read `registry.yaml`
2. identify candidate layouts and cards by tags/keywords/purpose
3. load only the specific card/layout docs required

This directly satisfies the requirement to minimize chat context and keep the workflow efficient.

### 3.3 Deterministic rendering
Most interpretation logic should live in Python scripts, not in Markdown prose.
That means:
- strict markdown parsing rules
- normalized internal models
- CSS token lookup through one API layer
- layout placement computed by renderer classes
- exporters acting as thin output adapters

### 3.4 Scaffolding behavior and source templates
Scaffolding must be implemented as deterministic Python logic, with this behavior:
- command: `scripts/scaffold_presentation.py <presentation-name> [--path <dir>]`
- create required folder/file structure in one run
- copy skill-level theme template into the project-level `theme.css`
- create starter `presentation-definition.md` with section/slide/card examples
- create `README.md` in the generated presentation folder with quick-start instructions
- avoid overwriting existing files unless explicit `--force` is provided

---

## 4. Proposed Data Model

### 4.1 Core domain classes

#### Theme and tokens
- `ThemeTokens`
- `SlideTheme`
- `CardTheme`
- `TypographyScale`
- `ColorPalette`
- `SpacingScale`
- `BorderStyleSet`
- `ShadowSet`

#### Presentation structure
- `DeckModel`
- `SectionModel`
- `SlideModel`
- `CardModel`
- `AgendaModel`

#### Rendering abstractions
- `BaseLayoutRenderer`
- `TitleSlideLayoutRenderer`
- `GridLayoutRenderer`
- `BaseCardRenderer`
- `TextCardRenderer`
- `ImageCardRenderer`
- later: `KpiCardRenderer`, `ChartCardRenderer`, etc.

#### Infrastructure
- `DeckParser`
- `ThemeLoader`
- `RegistryLoader`
- `AgendaInjector`
- `SlideFreezeGuard`
- `PptxExporter`
- `DrawioExporter`

### 4.2 Inheritance strategy
Use two parallel inheritance systems:

1. Python classes
   - `BaseCardRenderer` defines shared card behavior
   - specialized renderers extend it with content-specific body rendering
   - `BaseLayoutRenderer` defines slide frame calculation and placement hooks

2. CSS classes
   - base slide class for global slide tokens
   - base card class for shared card tokens
   - subclasses/variants for layout-specific and card-specific token additions

This matches the requirement for both Python and CSS inheritance.

---

## 5. Markdown Presentation Contract

### 5.1 Deck syntax
Implement a strict parser for this structure:
- `# Section Title` → section and agenda entry
- `## Slide Title` → slide title
- `### Card Title` → card title
- fenced YAML block below each card → card definition

### 5.2 Recommended parsing rules
- preserve source order exactly
- support optional slide metadata YAML comment block immediately below `##` for per-slide overrides (see 5.4)
- reserve `<!-- DONE -->` immediately below `##` for freeze protection; frozen check must run before any override parsing
- support slide-level YAML metadata block in comments later if needed

### 5.3 Internal normalized schema
Each card YAML block should normalize into:
- `type`
- `content`
- `props`
- `style_overrides`
- `asset_refs` (relative paths resolved against the project `assets/` folder — see §11.4)

This gives a stable renderer interface even if raw user input varies.

### 5.4 Per-slide and per-card override syntax
The requirement explicitly states that slides *and* cards can each override the global CSS tokens. Model both override points:

**Per-slide override** — a YAML comment block directly below the `## Slide Title` line (but after `<!-- DONE -->` check):
```markdown
## My Slide Title
<!-- slide
background: "#F5F5F5"
title_color: "#003087"
hide_footer: true
-->
### Card Title
```

**Per-card override** — fields inside the card YAML block under a `style_overrides:` key:
```yaml
type: text-card
content: ...
style_overrides:
  card_background: "#FFFFFF"
  header_line_color: "#003087"
```

Both override levels feed into the same precedence chain defined in §6.3. The Python `SlideModel` must carry a `slide_overrides` dict alongside its card list.

---

## 6. Theme and CSS Token System

## 6.1 Base CSS contract
Create a CSS token model with two main layers:

1. slide tokens
   - canvas size
   - margins
   - card gaps
   - background color/image
   - title, subtitle, divider, logos, footer, page number

2. card tokens
   - background
   - border
   - radius
   - padding
   - header visibility/alignment
   - title styling
   - header line styling
   - body typography defaults
   - media presentation defaults

## 6.2 Token namespaces
Use explicit namespaces to keep the theme extensible, for example:
- `--canvas-*`
- `--slide-title-*`
- `--slide-subtitle-*`
- `--slide-divider-*`
- `--slide-logo-primary-*`
- `--slide-logo-secondary-*`
- `--slide-footer-*`
- `--slide-page-number-*`
- `--card-*`
- `--text-h1-*`
- `--text-h2-*`
- `--text-body-*`
- `--text-caption-*`
- `--text-label-*`
- `--text-quote-*`
- `--text-footnote-*`
- `--image-fullbleed-*`
- `--image-framed-*`
- `--image-circular-*`

## 6.3 Override priority
Implement one consistent precedence chain:
1. per-card or per-slide Markdown override (from YAML blocks in `presentation-definition.md`)
2. layout/card variant CSS class (e.g., `.card--kpi`, `.layout--grid-2x2`)
3. base CSS token class (`.slide-base`, `.card-base`)
4. Python fallback default

This chain must be documented and enforced centrally — no renderer may short-circuit it by reading raw override values directly.

## 6.4 CSS extensibility rule
The CSS classes for slides and cards must be designed to be **addable without breaking**. Rules:
- New tokens may always be appended to the base class without changing existing token names.
- Token names may be renamed when the new name is strictly cleaner; update all renderers, CSS, and docs in the same commit.
- Every new token must supply a safe default value so existing presentations that do not set it still render correctly.
- Document each token with an inline comment in the CSS file explaining its role and accepted values.

## 6.5 Mandatory per-element token coverage
For every slide chrome element listed below, the CSS token set must cover **all** of these properties (using the appropriate `--slide-<element>-*` namespace):
`font-size`, `font-color`, `font-weight`, `background-color`, `border-color`, `border-width`, `border-radius`, `padding`, `margin`, `position`, `width`, `height`, `alignment`.

Elements requiring full coverage:
- slide title · slide subtitle · title line (divider) · primary logo · secondary logo · footer line · footer text · page number

This list must be the source of truth for `references/token-reference.md`.

## 6.6 Body text style token families
Define these seven text style families as explicit CSS token groups (e.g., `--text-h1-font-size`, `--text-h1-color`, …):
- `--text-h1-*` — Heading 1
- `--text-h2-*` — Heading 2
- `--text-body-*` — Body text
- `--text-caption-*` — Caption text
- `--text-label-*` — Label text
- `--text-quote-*` — Quote text
- `--text-footnote-*` — Footnote text

Each family covers at minimum: `font-size`, `font-color`, `font-weight`, `background-color`, `italic` (bool flag), `bold` (bool flag).

## 6.7 Image style token families
Define these three image presentation modes as explicit CSS token groups:
- `--image-fullbleed-*` — image fills the full card body; no border, border-radius: 0
- `--image-framed-*` — image with configurable `border-color`, `border-width`, `border-radius`, `padding`
- `--image-circular-*` — image cropped to circle; `border-radius`, `border-color`, `size`

Each `ImageCardRenderer` instance resolves its display mode via the card's `image_style` prop, defaulting to `framed`.

---

## 7. Layout System Plan

## 7.1 First layout set
Implement these first:
- `title-slide`
- `grid-1x1`
- `grid-1x2`
- `grid-2x2`
- `grid-3x2`
- `grid-3x3`
- `grid-3x4`

Then complete the full matrix up to 3 rows x 4 columns.

## 7.2 Shared layout responsibilities
Every layout renderer should handle:
- 16:9 canvas
- top/right margins
- inter-card spacing
- title/subtitle region
- logos
- footer line
- footer text
- page number
- background fill/image
- card slot allocation

## 7.3 Layout documentation
Each layout Markdown file should include:
- pictogram
- purpose
- ideal card count
- placement map
- supported overrides
- limitations
- example usage in deck syntax

---

## 8. Card System Plan

## 8.1 Minimum viable card set
Start with a small reusable set:
- `text-card`
- `image-card`
- `quote-card`
- `kpi-card`
- `chart-card`
- `agenda-card`

This satisfies the requirement for lean, reusable building blocks.

## 8.2 Shared card base behavior
The base card system should provide:
- title visibility
- title alignment
- header line visibility
- header line color/width/alignment
- body region geometry
- card container styling
- body typography helpers
- optional per-card background and border overrides

## 8.3 Specific card extensions
Specialized subclasses add only type-specific concerns:
- `TextCardRenderer` → text blocks and typography variants
- `ImageCardRenderer` → source, fit, crop, frame, circle mode
- `KpiCardRenderer` → metric emphasis, trend, supporting label
- `ChartCardRenderer` → chart payload and legend behavior
- `AgendaCardRenderer` → section list and active-section highlight

## 8.4 Card documentation standard
Each card spec must contain:
1. title and summary
2. pictogram
3. required fields
4. optional fields
5. supported overrides
6. design tokens used
7. example YAML block
8. notes on layout behavior

---

## 9. Agenda Injection Plan

Implement agenda generation as a dedicated preprocessing step:

1. parse all `#` sections
2. generate a single agenda data model exactly once at the beginning of Markdown file parsing
3. inject an agenda slide whenever a section changes (one injection per section boundary)
4. visually highlight the current/active section on each injected agenda slide; all other sections appear in a muted/inactive style
5. the agenda definition is maintained once in source but rendered N times (once per section transition)

Recommended implementation:
- `AgendaInjector` runs after parsing and before rendering
- injected slides are tagged `is_generated: True` so exporters and future tooling can distinguish them from authored slides

### 9.1 Agenda slide layout
The agenda slide must use the same design theme and chrome as all other slides (title bar, footer, page number, logos). Define a dedicated `AgendaSlideRenderer` (or a configurable `agenda` layout in the registry) that:
- uses a standard layout template (default: `grid-1xN` where N is the number of sections, capped to a sane maximum)
- automatically distributes section entries evenly across the available body area
- truncates or wraps gracefully when section count exceeds the layout's slot capacity

### 9.2 Dynamic layout for variable section count
The agenda renderer must auto-adjust layout and spacing based on the actual number of sections:
- 1–4 sections → single column, generous spacing
- 5–8 sections → two columns
- 9+ sections → three columns or compact mode with reduced font size
- document the thresholds and their behavior in the agenda card spec
- allow the user to override column count and font size via per-slide overrides

---

## 10. DONE Slide Protection

Implement a freeze guard that:
- detects `<!-- DONE -->` directly below the `##` slide title
- preserves the slide's existing layout/content during future rendering runs
- skips renderer mutation for frozen slides

Recommended behavior:
- parser stores `slide.is_frozen`
- build pipeline can optionally log skipped slides
- exporters should not regenerate frozen slide internals unless explicitly forced later

This requirement is important enough to treat as a first-class feature, not a later enhancement.

---

## 11. Exporter Plan

## 11.1 Output targets
Implement exporters behind a common interface:
- `PptxExporter`
- `DrawioExporter`

Generated presentation folders should route exporter output by default to:
- `output/presentation.pptx`
- `output/presentation.drawio`

## 11.2 Shared render pipeline
Suggested build flow:
1. load registry
2. parse deck markdown
3. load CSS theme tokens
4. normalize slide/card models
5. inject agenda slides
6. skip frozen slides where applicable
7. resolve layout renderer per slide
8. resolve card renderer per card
9. export to target format

## 11.3 Exporter design principle
Keep format-specific code thin.
All layout geometry and styling decisions should be resolved before exporter output where possible.

## 11.4 Asset resolution
The renderer must resolve all relative asset paths (images, charts, diagrams) from the project-level `assets/` folder. Rules:
- `asset_refs` in the normalized card model store paths relative to the project root
- the build pipeline receives the project root as a required argument and passes it to all card renderers
- if an asset cannot be found at the resolved path, the renderer must:
  1. log a clear warning with the expected absolute path
  2. render a placeholder box with the missing asset path text (do not silently skip or crash)
- asset resolution must be tested in the smoke test suite using the example project

---

## 12. Validation and Tooling

Create validation scripts for:
- deck syntax correctness
- card YAML schema correctness
- registry consistency
- missing card/layout references
- unresolved CSS tokens
- asset path validity
- duplicate layout or card slugs

Optional but valuable:
- lint to ensure all documented cards exist in registry
- lint to ensure all registry entries have Markdown docs
- smoke test that builds example deck to both output formats

Scaffolding validations:
- verify scaffold output tree matches required structure
- verify `theme.css` is copied from the canonical skill-level template
- verify scaffold does not overwrite files without `--force`

---

## 13. Recommended Implementation Phases

### Phase 1 — Scaffold the skill
- create folder structure
- create `requirements.txt`
- create skill-local `.venv` inside `skills/presentation-design/`
- add placeholder docs and registries
- document venv setup in `SKILL.md` and in a dedicated `references/setup.md`:
  - how to create the venv
  - how to activate it
  - how to install dependencies
  - how to run the build script

### Phase 1b — Add presentation scaffolder (new)
- implement `scripts/scaffold_presentation.py`
- generate required project tree with `presentation-definition.md` and `theme.css`
- ensure `output/` and `assets/{images,charts,diagrams,logos}` are created
- set default output targets to `output/presentation.pptx` and `output/presentation.drawio`
- add scaffold usage docs and customization notes

### Phase 2 — Define contracts
- write `SKILL.md`
- define deck syntax doc
- define registry schema
- define card and layout spec template
- define CSS token naming scheme

### Phase 3 — Build the parser layer
- implement Markdown parser
- implement YAML extraction and schema normalization
- implement section/slide/card model creation
- add `DONE` detection

### Phase 4 — Build theming
- implement CSS token loader
- implement token inheritance and override resolution (§6.3 chain)
- create `themes/base.css` with full token set per §6.4–6.7; every token must have an inline comment
- create `themes/default-theme.css` with a neutral default value for every token
- validate that all 7 text style families and 3 image style families have complete token coverage

### Phase 5 — Build layout engine
- implement base layout renderer
- implement title slide and core grid layouts
- place slide chrome elements

### Phase 6 — Build card engine
- implement base card renderer
- implement first card set
- connect card docs to registry

### Phase 7 — Agenda system
- implement agenda extraction and injection
- add active-section highlighting behavior

### Phase 8 — Exporters
- implement PPTX exporter
- implement draw.io exporter
- ensure both consume the same internal models

### Phase 9 — Validation and examples
- create sample deck and theme
- add validation scripts
- run smoke tests

### Phase 10 — Documentation hardening
- complete all card/layout docs
- complete token reference
- complete inheritance/architecture docs

---

## 14. Suggested First Milestone

The first usable milestone should include:
- `SKILL.md`
- `registry.yaml`
- `deck-syntax.md`
- `base.css` and `default-theme.css`
- parser for sections/slides/cards with slide-level override support
- `title-slide`, `grid-1x1`, and `grid-2x2`
- `text-card`, `image-card`, and `agenda-card`
- agenda injection with dynamic column layout
- asset resolution with missing-asset placeholder
- PPTX export

That milestone is enough to validate the core architecture before implementing the full 3x4 layout matrix and richer card types.

### What must be explicitly included in Milestone 1
- `SKILL.md` with venv setup docs
- `registry.yaml` and `registry-tags.yaml`
- `references/deck-syntax.md` with per-slide override syntax example
- `references/setup.md`
- `themes/base.css` (fully comment-documented) and `themes/default-theme.css`
- parser for sections/slides/cards with slide-level YAML override support
- `title-slide`, `grid-1x1`, and `grid-2x2` layouts
- `text-card`, `image-card`, and `agenda-card` with full CSS token coverage
- agenda injection with dynamic column layout (§9.2)
- asset resolution with placeholder fallback (§11.4)
- PPTX export
- `scripts/scaffold_presentation.py`

---

## 15. Risks and Mitigations

### Risk 1: CSS becomes only decorative, while logic leaks into Markdown
**Mitigation:** keep all layout resolution and inheritance in Python, with Markdown limited to content and overrides.

### Risk 2: Card definitions drift and become inconsistent
**Mitigation:** enforce one shared card schema and one base card class contract.

### Risk 3: Exporters diverge in behavior
**Mitigation:** keep one normalized render model and thin target-specific exporters.

### Risk 4: Registry becomes stale
**Mitigation:** add validation ensuring every documented layout/card appears in registry and vice versa.

### Risk 5: Frozen slide support becomes brittle
**Mitigation:** model frozen slides explicitly in parser and build pipeline from the start.

### Risk 6: Agenda layout breaks with unusual section counts
**Mitigation:** implement and test all three column modes (1-col, 2-col, 3-col) from the start against 1, 4, 5, 8, and 9+ sections.

### Risk 7: Asset paths are brittle across environments
**Mitigation:** always resolve assets relative to the explicit project root arg; log missing assets as warnings rather than errors; smoke test must include a slide with a real image asset.

### Risk 8: Theme CSS grows undocumented
**Mitigation:** enforce the inline-comment documentation rule from the first token; include a CI lint check that flags tokens without a comment.

---

## 16. Immediate Next Steps

1. scaffold the `presentation-design` skill folder with venv and document setup
2. implement `scripts/scaffold_presentation.py` with the required output tree
3. define the registry schema and `SKILL.md`
4. write `references/deck-syntax.md` including per-slide and per-card override syntax
5. write the canonical card and layout spec templates
6. implement the CSS base token set (§6.4–6.7) with inline comments
7. implement the parser and normalized internal models (incl. `slide_overrides` and `asset_refs`)
8. implement the CSS token loader and override resolution chain
9. build layout renderers: `title-slide`, `grid-1x1`, `grid-2x2`
10. build card renderers: `text-card`, `image-card`, `agenda-card`
11. implement `AgendaInjector` with dynamic column layout and active-section highlighting
12. implement asset resolution with placeholder fallback
13. add PPTX exporter, run smoke test with example deck

---

## 17. Definition of Done for the Skill

The skill is ready when:
- a user can write a structured `presentation-definition.md`
- the system can parse sections, slides, and cards deterministically
- agenda slides are injected automatically at section changes
- frozen slides marked with `<!-- DONE -->` remain untouched
- layouts are selected from a documented registry
- cards are selected from a documented registry
- theming is driven by CSS tokens with per-slide/per-card overrides
- output can be generated to `.pptx` and `.drawio`
- a new presentation can be scaffolded in one command with the required folder structure
- generated `theme.css` is copied from the skill-level CSS template and is ready for customization
- every card and layout has its own Markdown documentation with pictogram and schema
- the skill is documented well enough that future agents can discover capabilities via registry first
