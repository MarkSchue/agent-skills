---
name: atomic-design-system
description: Headless presentation design system for building slides in draw.io and PowerPoint from a structured library of atoms, molecules, templates, and semantic design tokens. Use this skill whenever a user asks to create, build, or design a slide deck, presentation, or visual document — even if they say "just make slides" or "put this in a presentation". Also use this skill for visual token extraction from screenshots, existing presentations, or websites; for initializing or managing design configurations; and for any draw.io or PPTX output task.
metadata:
  author: MarkSchue
  version: "1.0.0"
  argument-hint: <deck.md> [--output <file.pptx|file.drawio>]
---

# Atomic Design System

A headless presentation design system. Atoms, molecules, and templates are assembled by a deterministic
six-phase pipeline. All visual properties are design-agnostic; the active `theme.css` resolves every
design token to concrete values at assembly time.

**Always read `registry.yaml` before loading any other file.** Load element Markdown files only for
elements you will actually use.

---

## Six-Phase Assembly Pipeline

Follow in sequence. Do not skip or reorder.

### Phase 1 — Planning
- If input is raw content: create an annotated Markdown template with `# Slide Title`, `<!-- layout: ... -->`,
  `<!-- card: ... -->`, and `[TODO: ...]` placeholders. Ask clarifying questions before producing output.
- If a structured Markdown file is provided, skip to Phase 2.

### Phase 2 — Selection
- Load `registry.yaml`. For each slide, select one template and up to three molecules.
- Report every automatic design decision so the user can override. Prefer tags matching the slide's domain.

### Phase 3 — Retrieval
- Load only the Markdown files for elements selected in Phase 2. No speculative loading.
- Context budget per slide: `registry.yaml` + 1 template + ≤3 molecules = 5 files max.
- Load atom files only when the parent molecule specifically requires introspection.

### Phase 4 — Theming
- Load the project's `theme.css` once per invocation (not per slide).
- Read the active design system's `principles.md` (`materialdesign3`, `carbon`, or `liquidglass`).
  Let those principles constrain every structural decision (radii, spacing, motion, elevation model).
- **Brand override scope:** project `theme.css` may only override `--color-*` and `--font-family`.
  Radii, spacing, and elevation are owned by the design system — do not change per project.

### Phase 5 — Data Injection
- For each data-viz atom, extract data from the MD fenced block (` ```chart:<type> `).
- Use labeled placeholder values for missing data and notify the user.

### Phase 6 — Assembly
- Produce the target file (`.drawio`, `.pptx`, or both when `platform: both`).
- Log: elements used, theme tokens, platform.
- If a required atom is missing, halt and report before producing any output.
- **CSS stylesheet:** builders auto-detect `theme.css` next to `deck.md`. Always run from the project
  directory or pass `--stylesheet <project>/theme.css` explicitly. Never invoke builders bare without
  a stylesheet — they silently fall back to the bundled materialdesign3 base and discard brand overrides.
- **Template/builder architecture (Principle 2):** layout logic lives in `rendering/templates/`.
  Shared helpers live in `slide_helpers.py`. Both builders are thin orchestrators — scaffold + delegate
  to `TEMPLATE_REGISTRY`. Adding/changing a template only requires editing `rendering/templates/*.py`.

### Phase 7 — Visual QA (required for every PPTX output)

**Assume there are problems. Your job is to find them.**

1. **Convert to images:**
   ```bash
   python scripts/qa_render.py <output.pptx> --output-dir <project>/qa/ --dpi 150
   ```

2. **Inspect with a subagent** (fresh eyes; you have been staring at the code). Give the subagent the
   generated image paths and ask it to check for:
   - Overlapping or overflowing elements · Text cut off at edges/box boundaries
   - Elements too close (< 12px) or cards nearly touching · Uneven gaps / cramped areas
   - Insufficient slide-edge margins · Misaligned columns
   - Low-contrast text or icons · Excessive wrapping from narrow text boxes
   - Placeholder text still visible · Wrong card background for the theme

3. **Fix** all reported issues.

4. **Re-verify affected slides only** (`--slides 3 7`). One fix can create a new problem.

5. **Repeat** until a full pass finds no new issues.

> **inner_margin tip:** Pass `inner_margin=0` to `ctx.text()` when a text box must align precisely
> with an adjacent shape — python-pptx applies ~5pt default internal padding otherwise.
>
> **Draw.io:** QA render does not apply (requires a desktop install). Review draw.io output manually.

---

## Design System Structure

```
atomic-design-system/
├── SKILL.md · registry.yaml · registry-tags.yaml
├── atoms/           icon-wrapper · chart-bar · chart-pie · chart-gantt · badge-status
│                    text-heading · text-body · shape-divider · svg/
├── molecules/
│   ├── strategy/    mission-card · timeline-panel · objective-card · quote-card · roadmap-panel
│   ├── data/        kpi-card · trend-card · data-insight-panel · comparison-card · chart-card
│   └── team/        profile-card · team-grid-panel · contact-card · role-card · location-card
├── templates/       hero-title · comparison-2col · grid-3 · numbered-list · data-insight
├── designthemes/    materialdesign3/theme.css · carbon/theme.css · liquidglass/theme.css
├── previews/        atoms/ · molecules/ · templates/
├── assets/          theme-bridges/ · neutral-theme.yaml
├── references/      design-system-concepts.md · token-reference.md
├── scripts/         (see Scripts section)
└── evals/           evals.json
```

---

## Token Syntax

### CSS Custom Property Namespaces

| Namespace | Example | Python Accessor |
|---|---|---|
| `--color-<token>` | `--color-primary: #6750a4` | `ctx.color("primary")` |
| `--font-<role>-size` | `--font-heading-size: 32` | `ctx.font_size("heading")` |
| `--font-<role>-weight` | `--font-heading-weight: 700` | `ctx.font_bold("heading")` |
| `--font-family` | `--font-family: "Roboto"` | `ctx.font` |
| `--radius-<level>` | `--radius-medium: 12` | `ctx.rad("radius-medium")` |
| `--spacing-<size>` | `--spacing-m: 16` | `ctx.spacing("m")` |
| `--canvas-<prop>` | `--canvas-padding: 28` | `ctx.PAD` |

### Standard Color Tokens
`primary` · `on-primary` · `primary-container` · `on-primary-container` ·
`secondary` · `on-secondary` · `secondary-container` · `on-secondary-container` ·
`accent` · `neutral` · `outline` · `surface` · `surface-variant` ·
`on-surface` · `on-surface-variant` · `border-subtle` ·
`error` · `on-error` · `warning` · `success` · `on-success`

> No atom, molecule, or template file may contain a literal hex color, RGB value, or
> platform-specific syntax. Lint will flag violations.

---

## Design Principles

### Principle 1 — No Hardcoded Visual Values

Every color, font size, spacing value, border radius, and font family in atom/molecule Python files
**MUST** come from the `RenderContext` API (`ctx`). No literal values permitted.

| What | Forbidden | Required |
|---|---|---|
| Colors | `"#6750a4"`, `RGBColor(...)` | `ctx.color("primary")` |
| Font sizes | `size=12` | `ctx.font_size("caption")` |
| Font family | `"Roboto"` | `ctx.font` |
| Spacing | `gap=16` | `ctx.spacing("m")` |
| Radii | `radius=12` | `ctx.rad("radius-medium")` |

**Typography scale:**

| Role | Token | Default (material) |
|---|---|---|
| `"heading-display"` | Display text | 57 |
| `"heading"` | Slide title | 32 |
| `"heading-sub"` | Section title | 24 |
| `"body"` | Primary content | 16 |
| `"label"` | Card titles, UI labels | 14 |
| `"caption"` | Secondary text, metadata | 12 |
| `"annotation"` | Axis labels, badges | 11 |

Dynamic/computed sizes (`min(48, max(32, int(h * 0.07)))`) are permitted only when the size must
scale with card height. Use a typography token as the floor/ceiling where possible.

**Rules for every new or edited atom/molecule:**
1. Never introduce a literal hex — always `ctx.color("<token>")`.
2. Never write `size=<number>` — always `ctx.font_size("<role>")`.
3. If no existing role fits, add the new role to `theme.css` and the table above first.
4. **Always use `ctx.card_bg_color(props, "bg-card")` as the default for the card container.**
   Never hard-code `"bg-card-filled"`, `"bg-card-clean"`, `"bg-card-alt"`, or `"bg-card-featured"`
   as a renderer default. The user opts in via `card_bg:` in deck.md.

**Card background override via deck.md:**

| `card_bg:` value | Resolves to token | Typical use |
|---|---|---|
| *(omitted)* | `--color-bg-card` | Default harmonized surface (all cards) |
| `clean` | `--color-bg-card-clean` | Minimal / white feel |
| `filled` | `--color-bg-card-filled` | Accented / primary-container |
| `alt` | `--color-bg-card-alt` | Secondary-container variant |
| `featured` | `--color-bg-card-featured` | Vivid hero / primary color |

---

### Principle 2 — Template/Builder Architecture: TEMPLATE_REGISTRY

`pptx_builder.py` and `drawio_builder.py` are **thin orchestrators**. They scaffold each slide
(background, title, divider) then delegate all layout logic to `TEMPLATE_REGISTRY`.

| Layer | File | Responsibility |
|---|---|---|
| Orchestrators | `pptx_builder.py` / `drawio_builder.py` | Scaffold + look up template + call `layout.render()` |
| Shared helpers | `slide_helpers.py` | `_extract_section_blocks()`, `dispatch()`, prop parsing |
| Layout registry | `rendering/templates/__init__.py` | `TEMPLATE_REGISTRY` dict: slug → renderer instance |
| Layout classes | `rendering/templates/*.py` | One class per template; implements `render(...)` |
| Molecule registry | `rendering/molecules/__init__.py` | `MOLECULE_REGISTRY` dict: slug → renderer instance |

**Adding a new template:**
1. Create `rendering/templates/<name>.py` with a class implementing `render(self, ctx, slide, blocks, margin, content_y, content_h, width, height, dispatch_fn) → None`.
2. Register in `rendering/templates/__init__.py` → `TEMPLATE_REGISTRY`.
3. Add to `registry.yaml` and the templates list in this file.

---

### Principle 3 — Utility-First CSS: Reduce, Reuse, Reference

Sub-element styling uses shared utility classes (`u-*`) rather than per-element component rules.
Theme CSS defines `u-*` classes for 8 token groups: radius, background, text-color, border-color,
typography, padding, gap, weight.

- Document `__value → u-text-on-primary-container u-type-annotation` instead of adding a CSS rule.
- Combine utilities (e.g. `u-bg-primary u-text-on-primary`) rather than adding `.my-badge { ... }`.

**BEM `__element` class is permitted only when the element:**
1. Combines ≥ 3 distinct non-utility properties.
2. Uses a non-standard value not expressible from a single utility.
3. Has design-system shape identity that must be fixed (e.g. avatar: primary fill + radius-large).

Everything else → utility classes only. Document assignments in the element's `.md` CSS Class Map.

---

### Principle 4 — Visual Representation in Every Element Spec

Every atom, molecule, and template spec **MUST** start with a `## Layout` section containing
an ASCII-art visual illustrating the component structure.

```
┌─────────────────────────────────────────────────────┐
│  [atom-type: description]   [atom-type: description] │
│  [atom-type: description]                            │
└─────────────────────────────────────────────────────┘
```

Rules: use Unicode box-drawing chars (`┌ ┐ └ ┘ ─ │`); use `[atom-type: role]` placeholders;
52–60 chars wide; follow with 1–3 bullets explaining layout intent and special behaviour.

When creating or editing any element:
1. Add `## Layout` immediately after YAML front-matter if missing.
2. Upgrade existing ASCII that lacks `[atom-type: ...]` style.
3. Update the ASCII after any structural layout change.

---

### Principle 5 — Smart Input Interpretation: The User Is Not a Developer

Every molecule/atom renderer must accept the widest reasonable range of user-supplied values
and interpret them intelligently — never raise `ValueError` or silently ignore data.

All parsing lives in `scripts/rendering/input_utils.py`. Route every user-supplied value through
the appropriate helper.

| Helper | Accepts | Returns |
|---|---|---|
| `parse_numeric(raw)` | `"35"`, `"35%"`, `"35 (#color primary)"`, `"84,500"`, `"12.1M"` | `float` |
| `resolve_color(raw, ctx, fallback)` | Token name, CSS name, hex (with/without `#`), English phrase | hex string |
| `slice_color(raw_value, ctx, palette)` | Slice value with optional inline `(color x)` annotation | hex string |
| `resolve_icon(description)` | Single char, emoji, or natural-language phrase | single char |
| `resolve_trend(raw)` | `"up"`, `"rising"`, `"↑"`, `"positive"`, `"green"`, … | `"up"` / `"down"` / `"neutral"` |
| `resolve_legend_position(raw)` | `"bottom"`, `"side"`, `"under"`, `"right"`, … | `"below"` / `"above"` / `"left"` / `"right"` |

**Color input examples:** `primary`, `"#FF6600"`, `FF6600`, `orange`, `dark blue`, `brand blue`.
Slice annotations: `35 (#color primary)`, `45 (color orange)`, `28 (color #FF6600)`.

**Rules for every new or edited renderer:**
1. Color fields (`color:`, `fill:`, `border:`, any color-like key) → `resolve_color(raw, ctx, fallback)`.
2. Numeric fields (`value:`, slice values) → `parse_numeric(raw)`. Never call `float()` / `int()` directly.
3. Icon/symbol fields → `resolve_icon(raw)`. Never use `raw[0].upper()`.
4. Trend/direction fields → `resolve_trend(raw)`. Never compare `raw == "up"` directly.
5. Legend position fields → `resolve_legend_position(raw)`.
6. New interpretation categories → add to `input_utils.py` as a new helper with accepted-forms docstring.

---

### Principle 6 — Harmonized Card System: One Card Language Everywhere

Every card-based molecule and every Markdown card spec **MUST** participate in one shared card styling system.
No renderer or spec may invent a separate card container language when the visual role is still “card”.

**This principle applies to all relevant sources:**
- Python renderers in `scripts/rendering/molecules/**/*.py`
- Markdown specs in `atoms/**/*.md`, `molecules/**/*.md`, and `templates/**/*.md`
- Theme stylesheets in `theme.css`

**Required shared card contract**

1. **One canonical card container**
  - All card renderers use the same semantic container contract:
    - background → `ctx.card_bg_color(props, "bg-card")`
    - border color → `ctx.color("border-default")`
    - radius → `ctx.rad()`
  - Markdown CSS Class Maps must document the card container as `.card`, not a per-card block such as `.kpi-card`, `.trend-card`, or `.topic-card`.

2. **Shared title/body tokens**
  - Card title text must resolve from shared theme tokens, not ad-hoc per-card colors.
  - Card body text must resolve from shared theme tokens, not ad-hoc per-card colors.
  - Use `RenderContext` helpers for this where available.

3. **Shared header/footer system**
  - Headers and footers are semantic card sections.
  - Visibility, divider display, divider color, divider alignment, divider width, and text alignment must be controlled by shared `--card-*` tokens and may be overridden per card via verbal configuration.
  - New or edited card renderers must use the shared card-section helpers instead of bespoke CSS-variable lookups.

4. **Shared icon-badge system**
  - Any card header may optionally display an icon badge.
  - Icon badge background, foreground, and alignment must come from shared card tokens.
  - Do not create KPI-only icon-badge theme tokens for a behavior that is generic to cards.

5. **Per-card overrides remain allowed**
  - The user may override card presentation verbally on any individual card.
  - Supported override categories include header visibility, footer visibility, divider visibility, text alignment, divider width/alignment, card background, and icon placement.

6. **Spec documentation must mirror the shared system**
  - In Markdown specs, Visual Properties and CSS Class Maps must reference shared card tokens/classes where applicable:
    - `.card`
    - shared `--card-*` tokens
    - shared text tokens for title/body/subtitle

**Rules for every new or edited card renderer/spec:**
1. Card container → shared card contract only.
2. Card title/body colors → shared card tokens only.
3. Header/footer divider behavior → shared card tokens only.
4. Optional header icon badge → shared card icon tokens only.
5. Document the container as `.card` in the spec.
6. If a card intentionally deviates, document the reason explicitly in the spec under `## Visual Properties`.

---

## Theme Stylesheet (CSS)

Each design system provides `theme.css`. A project references it:
```css
@import "materialdesign3";   /* inherit base tokens + classes */
:root {
  /* Override: brand colors + font-family only */
  --color-primary:  #6200ee;
  --font-family:    "Inter", sans-serif;
  /* Do NOT change: radii, spacing, elevation */
}
```

### Design Token Categories

| Category | Properties | Example |
|---|---|---|
| Colors (21 tokens) | `--color-primary`, `--color-surface`, … | `--color-primary: #6750a4` |
| Typography (7 roles × 3) | `--font-family`, `--font-heading-size`, `--font-heading-weight`, … | `--font-heading-size: 32` |
| Borders | `--radius-sharp`, `--radius-medium`, `--radius-large` | `--radius-medium: 12` |
| Spacing | `--spacing-xs` … `--spacing-xl` | `--spacing-m: 16` |
| Canvas | `--canvas-width/height/margin/padding/gutter/baseline-grid` | `--canvas-padding: 28` |
| Elevation (4 levels) | `--elevation-{none\|low\|medium\|high}-{blur\|distance\|angle\|opacity}` | `--elevation-low-blur: 2` |

### CSS Structure (3 sections per theme file)

1. **Utility classes (`u-*`)** — radius, bg, text-color, border-color, typography, padding, gap, weight.
2. **Component classes (BEM block)** — container identity only; sub-elements documented as utility combos in comments.
3. **Exceptional `__element` classes** — only when ≥ 3 unique non-utility properties combine.

---

## Design System Layers

```
designthemes/<system>/theme.css    ← Layer 1 — Design System Theme
         ↓  complete token vocabulary + component classes
<project>/theme.css                ← Layer 2 — Project Brand Override
         ↓  @import base; override --color-* + --font-family only
atoms / molecules / templates       ← Render layer — design-agnostic
```

**Brand Customization Contract:**

| Category | Project May Override? |
|---|---|
| `--color-*` (all semantic tokens) | ✅ Yes |
| `--font-family` | ✅ Yes |
| `--canvas-*` (output size, margin) | ✅ Yes |
| `--radius-*` | ❌ No — design system authority |
| `--spacing-*` | ❌ No — design system grid |
| `--elevation-*` | ❌ No — design system depth model |

**Design-system-specific rules:**
- **materialdesign3:** continuous rounding scale; shadow-based elevation; M3 spring motion tokens; `primary`/`on-primary` role pairing.
- **carbon:** sharp/minimally-rounded (4px max); depth via `layer` color steps; IBM productive/expressive cubic-bezier durations; IBM Blue 60 reserved for single focal points.

---

## Visual Extraction Workflow

When a user provides a screenshot, `.pptx`, `.drawio`, or URL to "match this design":

1. **Analyze** — identify dominant colors, role-based usage, shape patterns, spacing.
2. **Present findings** — list every proposed token assignment with reasoning before writing anything.
3. **Wait for approval** — user may accept, reject, or rename each token individually.
4. **Write** only approved tokens to the design system's `theme.css`.
5. **Report** what was found and what was not found (e.g. "No elevation/shadow detected").

---

## Markdown Slide Input Format

```markdown
---
theme: ./theme.css
---

# Slide Title
<!-- layout: hero-title -->

Content goes here.

## Section
<!-- layout: data-insight -->
<!-- card: kpi-card, trend-card -->

```chart:bar
labels: [Q1, Q2, Q3]
values: [82, 91, 105]
unit: M€
```
```

- `#` H1 = new slide · `##` H2 = new section (same slide unless followed by `#`)
- `<!-- layout: <template-id> -->` = force template · `<!-- card: <molecule-id>, ... -->` = suggest molecules
- No hint = skill auto-selects from registry

---

## Adding New Elements

1. Create the Markdown spec in the correct folder:
   - Atom: `atoms/<type>-<variant>.md` · Molecule: `molecules/<domain>/<role>-card.md` · Template: `templates/<structure>.md`
2. Add a registry entry in `registry.yaml`.
3. Generate a preview PNG: `python scripts/preview_generator.py <element-id>`.
4. Run `python scripts/lint.py` to validate naming, tokens, and registry consistency.

---

## References

Load only when deeper guidance is needed:
- `references/design-system-concepts.md` — Atomic design theory, token system design, glossary
- `references/token-reference.md` — Complete token catalogue with allowed values and defaults

---

## Scripts

Run with the project's Python environment:

| Script | Purpose |
|---|---|
| `scripts/lint.py` | Full validation (naming, tokens, registry) |
| `scripts/preview_generator.py [id]` | Regenerate preview PNGs |
| `scripts/visual_extractor.py <source>` | Extract tokens from image / PPTX / URL |
| `scripts/drawio_builder.py <md> [--stylesheet theme.css]` | Build draw.io output |
| `scripts/pptx_builder.py <md> [--stylesheet theme.css]` | Build PowerPoint output |
| `scripts/qa_render.py <pptx> [--output-dir DIR] [--dpi N] [--slides N …]` | Convert PPTX → per-slide JPEG for Phase 7 QA |
| `scripts/css_loader.py` | CSS stylesheet parser (used by `design_system_utils.py`) |

Both builders auto-detect `theme.css` next to `<md-file>` if `--stylesheet` is omitted.
Always run from the project directory or pass `--stylesheet` explicitly.
