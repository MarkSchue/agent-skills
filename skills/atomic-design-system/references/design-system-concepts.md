# Atomic Design System — Concepts & Glossary

## 1. What Is Atomic Design?

Atomic design is a methodology for building interfaces from the smallest reusable units upward. It was introduced by Brad Frost and adapts naturally to presentation slides.

The hierarchy used in this skill:

| Level | Description | Examples |
|-------|-------------|---------|
| **Atom** | Single-purpose visual element; cannot be split further | icon, badge, text, chart |
| **Molecule** | Composed of 2–5 atoms; expresses a single idea | KPI card, profile card, mission card |
| **Template** | Fixed-zone layout that wires molecules into a slide | hero-title, data-insight, grid-3 |

### Why Not "Organisms" or "Pages"?

In Frost's original work there are five levels. This skill collapses organisms and pages because:
- Slides are single-screen artefacts — they have no global navigation or multi-page scroll
- A template already describes the full canvas zone arrangement
- Adding organisms would duplicate what templates already encode

---

## 2. Token System

Tokens are named references to visual properties. Instead of encoding `#0043CE` directly in a molecule file, you write `{{theme.color.primary}}`. This single indirection makes every element instantly re-brandable.

### Token Namespaces

| Namespace | Examples | Description |
|-----------|---------|-------------|
| `theme.color.*` | `primary`, `surface`, `accent` | Brand palette |
| `theme.shape.*` | `card`, `badge`, `chip` | Border-radius presets |
| `theme.spacing.*` | `sm`, `md`, `lg`, `xl` | Margin / padding scale |
| `theme.font.family.*` | `sans`, `mono` | Typeface stacks |
| `theme.font.size.*` | `xs`, `sm`, `md`, `lg`, `xl` | Type scale in px |
| `theme.elevation.*` | `card`, `modal` | Shadow / depth |

### Resolution Order

When the design system resolves a token:

1. Load the active `design-config.yaml`
2. Merge the referenced preset (e.g. `carbon.yaml`)
3. Merge the target-platform bridge (e.g. `drawio.yaml`)
4. Replace `{{token}}` placeholders with the resolved value

Token resolution is depth-first; nested objects are resolved recursively by `DesignSystem.resolve_dict()`.

---

## 2b. Per-Card Instance Overrides

Beyond the global theme, individual card instances in `deck.md` can override geometry
and color values via their YAML props block.  This forms a three-tier override chain:

```
Per-card prop  (deck.md YAML)
    ↓  if absent
CSS theme token  (theme.css)
    ↓  if absent / 0
Computed default  (context.py formula)
```

### Overridable Keys

All keys accept both hyphen (`card-padding`) and underscore (`card_padding`) forms.

| Key | Type | Effect |
|-----|------|--------|
| `card-padding` | int (px) | Inner padding of the card body |
| `card-header-height` | int (px) | Reserved height for the header zone |
| `card-header-gap` | int (px) | Gap between header and body |
| `card-header-font-size` | int (px) | Title font size in the header |
| `icon-size` | int (px) | Icon bounding-box size |
| `icon-radius` | int (px) | Icon background corner radius |
| `header-line-color` | hex | Colour of the header divider line |
| `footer-line-color` | hex | Colour of the footer divider line |
| `card_bg` | `filled\|clean\|alt\|featured` | Semantic card background variant |
| `title-color` | hex | Card title text colour |
| `body-color` | hex | Body / description text colour |
| `icon-bg` | hex | Icon background fill |
| `icon-fg` | hex | Icon foreground / glyph colour |
| `icon-stroke` | hex | Icon stroke / outline colour |
| `show-header` | bool\* | Show or hide the whole header zone |
| `show-header-line` | bool\* | Show or hide the header divider line |
| `show-footer` | bool\* | Show or hide the footer zone |
| `show-footer-line` | bool\* | Show or hide the footer divider line |
| `header-align` | `left\|center\|right` | Title alignment in the header |
| `header-line-width` | `50%` etc. | Width of the header line as a % of card width |
| `header-line-align` | `left\|center\|right` | Alignment of the header line |

\* Boolish: `none / false / 0 / off / hide / hidden / suppress` → disabled; `true / 1 / yes / on / show` → enabled.

### Renderer Rule

Every molecule Python class **must** pass `props` to every geometry helper (see `context.py`
module docstring for the canonical call pattern).  This is a non-negotiable authoring rule
enforced by code review — a molecule that computes geometry inline ignores both CSS tokens
and per-card overrides.

---

## 3. Six-Phase Pipeline

The agent follows this pipeline on every slide-generation request:

### Phase 1 — Planning
Parse the user's natural-language brief into a structured outline:
- How many slides are needed?
- What content domain (strategy / data / team)?
- Is a design config available, or should defaults apply?

### Phase 2 — Template Selection
For each slide, pick the most semantically relevant template from `templates/*.md`.

Selection heuristics:
- Opening/closing slide → `hero-title`
- Two competing options → `comparison-2col`
- Three equal items → `grid-3`
- Steps or process → `numbered-list`
- One chart + insights → `data-insight`

### Phase 3 — Molecule Retrieval
For each template zone, identify required molecules from `molecules/**/*.md`.

Molecules are retrieved via `registry.yaml` using tag matching. The agent prefers molecules whose `domain` matches the slide domain.

### Phase 4 — Theming
Resolve all `{{token}}` placeholders using `DesignSystem.load()` with the project's `design-config.yaml`. If no config is provided, `assets/default-design-config.yaml` is used.

### Phase 5 — Data Injection
Replace molecule `data-input-schema` fields with actual user-supplied data:
- Numbers, labels, names, chart values, progress percentages, etc.
- Validate that required fields are present

### Phase 6 — Assembly
Produce the requested output format:
- **Markdown** (`.md`) — annotated slide source file
- **draw.io** (`.drawio`) — mxGraph XML via `drawio_builder.py`
- **PowerPoint** (`.pptx`) — python-pptx output via `pptx_builder.py`

---

## 4. Visual Extraction Workflow

When a user provides a visual source (screenshot, PPTX, URL), the agent follows a 5-step approval loop:

1. **Analyze** — run `visual_extractor.py` to discover colors, fonts, border radii
2. **Present** — display the proposed token mappings before writing anything
3. **Confirm** — ask which tokens to accept, rename, or reject
4. **Summarize** — report what was mapped and what remains (and fallback values)
5. **Write** — with `--write` flag, merge approved tokens into `design-config.yaml`

> The agent NEVER modifies `design-config.yaml` without showing extraction results first.

---

## 5. Adding New Elements

### New Atom
1. Create `atoms/<type>-<name>.md` following the atom schema
2. Add entry to `registry.yaml` under `atoms:`
3. Ensure all tags appear in `registry-tags.yaml`
4. Run `scripts/lint.py` — must exit 0

### New Molecule
1. Create `molecules/<domain>/<type>-<name>.md`
2. Declare `required_atoms:` — list only atoms it composes
3. Add entry to `registry.yaml` under `molecules:`
4. Run `scripts/lint.py`

### New Template
1. Create `templates/<layout-name>.md`
2. Declare `compatible_molecules:` — list molecule IDs that fit each zone
3. Add entry to `registry.yaml` under `templates:`
4. Run `scripts/lint.py`

---

## 6. Glossary

| Term | Definition |
|------|------------|
| **Atom** | The smallest visual unit; a single-purpose component |
| **Badge** | A pill-shaped label conveying status or category |
| **Bridge** | A YAML file that maps semantic tokens to platform-specific attributes |
| **Canvas** | The full slide surface; default 1280 × 720 px (16:9) |
| **Data Injection** | Phase 5; replacing schema fields with real content |
| **Design Config** | Project-level YAML combining preset, color, typography, and spacing choices |
| **Domain** | Content category: `strategy`, `data`, or `team` |
| **Elevation** | A shadow/depth effect token (e.g. `card`, `modal`) |
| **Molecule** | 2–5 atoms composed into a named, self-contained component |
| **Preset** | A pre-built design bundle matching a known design system (Carbon, Material, Fluent, Ant) |
| **Registry** | `registry.yaml` — the always-loaded index of all elements |
| **Shape Token** | A border-radius profile name (e.g. `card`, `chip`, `pill`) |
| **Slot** | A named zone inside a template that accepts exactly one molecule |
| **Template** | A fixed layout that divides the canvas into named zones/slots |
| **Token** | A `{{theme.namespace.name}}` placeholder that resolves to a concrete value |
| **Visual Extractor** | `scripts/visual_extractor.py` — derives token proposals from images or files |
| **Zone** | Synonym for slot in templates; specifies position and size as a fraction of canvas |
