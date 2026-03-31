# Token Reference — Complete Catalogue

All tokens available in the Atomic Design System. Every token listed here
can appear in atom/molecule/template markdown files as `{{theme.<namespace>.<name>}}`.

---

## Color Tokens

| Token | Role | Notes |
|-------|------|-------|
| `theme.color.primary` | Main brand color — buttons, key highlights | Usually a vibrant hue |
| `theme.color.on-primary` | Text/icons on primary backgrounds | Must pass WCAG AA contrast |
| `theme.color.secondary` | Supporting accent, secondary buttons | Complements primary |
| `theme.color.accent` | Emphasis, highlights, callout borders | Use sparingly |
| `theme.color.surface` | Card and panel backgrounds | Usually near-white |
| `theme.color.on-surface` | Default text color on surfaces | Typically near-black |
| `theme.color.background` | Slide canvas background | Can differ from surface |
| `theme.color.neutral` | Borders, dividers, disabled states | Grey family |
| `theme.color.success` | Positive trend, completed, on-track | Semantic green |
| `theme.color.warning` | At-risk, partial progress | Semantic amber/orange |
| `theme.color.error` | Off-track, critical, destructive | Semantic red |

### Color Value Format
All color values must be valid CSS hex codes:
- 6-digit long form: `#0043CE`
- 3-digit short form not recommended (use full form for clarity)

---

## Shape Tokens

Shape tokens define the `border-radius` profile of elements.

| Token | draw.io `arcSize` | PPTX EMU | Visual |
|-------|-------------------|----------|--------|
| `theme.shape.sharp` | 0 | 0 | Square corners |
| `theme.shape.card` | 4 | ~38100 | Subtle rounding |
| `theme.shape.chip` | 8 | ~76200 | Small pill-like |
| `theme.shape.badge` | 12 | ~114300 | Noticeable curve |
| `theme.shape.pill` | 50 | ~475250 | Fully rounded ends |
| `theme.shape.circle` | 100 | — | Perfect circle |
| `theme.shape.diamond` | 0 | — | Rotated square |

---

## Spacing Tokens

Spacing tokens drive padding, gap, and margin values throughout elements.

| Token | Value (px) | Usage |
|-------|-----------|-------|
| `theme.spacing.xs` | 4 | Tight intra-element gaps |
| `theme.spacing.sm` | 8 | Default inner padding |
| `theme.spacing.md` | 16 | Card body padding |
| `theme.spacing.lg` | 24 | Section separation |
| `theme.spacing.xl` | 40 | Template zone margins |
| `theme.spacing.2xl` | 64 | Full-width panel padding |

---

## Typography Tokens

### Font Family

| Token | Usage |
|-------|-------|
| `theme.font.family.sans` | Body text, UI labels |
| `theme.font.family.serif` | Long-form reading text |
| `theme.font.family.mono` | Code snippets, data labels |
| `theme.font.family.display` | Hero headings (can equal sans) |

### Font Size

| Token | Value (px) | Usage |
|-------|-----------|-------|
| `theme.font.size.xs` | 11 | Captions, footnotes |
| `theme.font.size.sm` | 13 | Labels, data ticks |
| `theme.font.size.md` | 16 | Body text |
| `theme.font.size.lg` | 20 | Subheadings |
| `theme.font.size.xl` | 28 | Section headings |
| `theme.font.size.2xl` | 40 | Slide titles |
| `theme.font.size.hero` | 56 | Hero template headline |

### Font Weight

| Token | Value | Usage |
|-------|-------|-------|
| `theme.font.weight.regular` | 400 | Body text |
| `theme.font.weight.medium` | 500 | Labels, secondary headings |
| `theme.font.weight.semibold` | 600 | Card titles |
| `theme.font.weight.bold` | 700 | Primary headings |

---

## Elevation Tokens

Elevation adds shadow/depth to floating or raised elements.

| Token | Description | draw.io `shadow` | PPTX outer_shadow |
|-------|-------------|-----------------|-------------------|
| `theme.elevation.none` | Flat, no shadow | `shadow=0` | None |
| `theme.elevation.card` | Slight lift for cards | `shadow=1` | blur=6pt, dist=2pt |
| `theme.elevation.dropdown` | Dropdown / tooltip | `shadow=1` | blur=8pt, dist=4pt |
| `theme.elevation.modal` | Modal dialog overlay | `shadow=1` | blur=24pt, dist=8pt |

Shadow color is always derived from `theme.color.neutral` at 40% opacity.

---

## Canvas Tokens

| Token | Default | Description |
|-------|---------|-------------|
| `theme.canvas.width` | 1280 | Slide width in pixels |
| `theme.canvas.height` | 720 | Slide height in pixels |
| `theme.canvas.aspect` | `16:9` | Aspect ratio label |
| `theme.canvas.platform` | `drawio` | Target format |

Supported platforms: `drawio`, `pptx`, `figma`.

---

## Using Tokens in Element Files

### In Atoms

```markdown
## Token Usage

| Property | Token |
|----------|-------|
| Fill color | `{{theme.color.primary}}` |
| Border radius | `{{theme.shape.card}}` |
| Font | `{{theme.font.family.sans}}` |
```

### In Presentation Prose

When describing a molecule's visual style, always reference tokens rather than
raw hex values:

> "The card background resolves to `{{theme.color.surface}}` with a subtle
> `{{theme.elevation.card}}` drop shadow."

This ensures every molecule file remains preset-agnostic and re-themes without edits.

---

## Extending the Token System

To add a new token:

1. Add it to `assets/default-design-config.yaml` under the correct namespace
2. Add it to `assets/neutral-theme.yaml` with a greyscale fallback
3. Add it to all four preset files under `assets/presets/`
4. Map it to platform attributes in `assets/theme-bridges/drawio.yaml` and `pptx.yaml`
5. Document it in this file

The `scripts/lint.py` resolver checks that all `{{theme.*}}` tokens in element
files resolve without error when loaded against `neutral-theme.yaml`.

---

## Card Instance Override Keys

These keys are written in the YAML front-matter of an individual card block in `deck.md`.
They bypass the theme and apply only to that one card instance.  Both hyphen (`card-padding`)
and underscore (`card_padding`) variants are accepted by all helpers.

The **priority chain** for every geometry helper is:
`per-card prop → CSS theme token (--card-*) → computed default`

### Geometry Overrides

| Key | Type | Geometry Helper | Description |
|-----|------|-----------------|-------------|
| `card-padding` | int (px) | `ctx.card_pad_px(w, h, props)` | Inner padding of the card body |
| `card-header-height` | int (px) | `ctx.card_header_h(w, h, props)` | Reserved height of the header zone |
| `card-header-gap` | int (px) | `ctx.card_header_gap(h, props)` | Gap between header and body |
| `card-header-font-size` | int (px) | `ctx.card_header_font_size(title, tw, h, props)` | Title font size in the header |
| `icon-size` | int (px) | `ctx.icon_size(w, h, props)` | Icon bounding-box size |
| `icon-radius` | int (px) | `ctx.icon_radius(size, props)` | Icon background corner radius |

### Color Overrides

| Key | Type | Helper | Description |
|-----|------|--------|-------------|
| `header-line-color` | hex | `ctx.card_line_color("header", default, props)` | Header divider line colour |
| `footer-line-color` | hex | `ctx.card_line_color("footer", default, props)` | Footer divider line colour |
| `footer-color` | hex | `ctx.card_footer_color(props)` | Footer metadata text colour |
| `card_bg` | `filled\|clean\|alt\|featured` | `ctx.card_bg_color(props, "bg-card")` | Semantic card background variant |
| `title-color` | hex | `ctx.card_title_color(props)` | Card title text colour |
| `body-color` | hex | `ctx.card_body_color(props)` | Body / description text colour |
| `icon-bg` | hex | `ctx.icon_bg(props)` | Icon background fill |
| `icon-fg` | hex | `ctx.icon_fg(props)` | Icon foreground / glyph colour |
| `icon-stroke` | hex | `ctx.icon_stroke(props)` | Icon stroke / outline colour |

### Visibility Toggles

Accepted falsy values: `none / false / 0 / off / hide / hidden / suppress`
Accepted truthy values: `true / 1 / yes / on / show`

| Key | Helper | Description |
|-----|--------|-------------|
| `show-header` | `ctx.card_section_enabled("header", props)` | Show or hide the whole header zone |
| `show-header-line` | `ctx.card_line_enabled("header", props)` | Show or hide the header divider line |
| `show-footer` | `ctx.card_section_enabled("footer", props)` | Show or hide the footer zone |
| `show-footer-line` | `ctx.card_line_enabled("footer", props)` | Show or hide the footer divider line |

### Alignment Overrides

| Key | Accepted Values | Helper | Description |
|-----|-----------------|--------|-------------|
| `header-align` | `left \| center \| right` | `ctx.card_header_align(props)` | Title alignment in the header |
| `header-line-width` | `50%` etc. | `ctx.card_divider_span(w, props)` | Width of the header line as % of card width |
| `header-line-align` | `left \| center \| right` | `ctx.card_header_align(props)` | Alignment of the header line |

### Shared Footer Theme Tokens

These CSS tokens provide one shared footer typography contract for cards that render metadata rows,
references, timeframes, dates, or source notes.

| Token | Helper | Description |
|-----|--------|-------------|
| `--card-footer-height` | `ctx.card_footer_h(h, props)` | Shared footer zone height |
| `--card-footer-gap` | `ctx.card_footer_gap(h, props)` | Shared gap between footer and surrounding content/divider |
| `--card-footer-font-size` | `ctx.card_footer_font_size(props)` | Shared footer font size |
| `--card-footer-color` | `ctx.card_footer_color(props)` | Shared footer text colour |
| `--card-footer-italic` | `ctx.card_footer_italic(props)` | Shared footer italic toggle |

### Shared Footer Instance Overrides

These keys apply only to a single card instance in `deck.md`.

| Key | Helper | Description |
|-----|--------|-------------|
| `card-footer-height` | `ctx.card_footer_h(h, props)` | Override footer zone height for one card |
| `card-footer-gap` | `ctx.card_footer_gap(h, props)` | Override footer gap for one card |
| `footer-font-size` | `ctx.card_footer_font_size(props)` | Override footer font size for one card |
| `footer-color` | `ctx.card_footer_color(props)` | Override footer text colour for one card |
| `footer-italic` | `ctx.card_footer_italic(props)` | Override footer italic style for one card |

### Renderer Authoring Rule

Every molecule Python class **must** pass `props` to every geometry helper call.
Never compute geometry inline — this bypasses both CSS tokens and per-card overrides.
See `context.py` module docstring for the canonical call pattern.

---

## Agenda Card Component Tokens

Defined in every theme CSS file.  Override them per-theme or per-card.

### CSS Theme Tokens (`--color-agenda-*`)

| Token | Default | Description |
|-------|---------|-------------|
| `--color-agenda-label` | `var(--color-primary)` | Number / time / icon label colour |
| `--color-agenda-icon-bg` | `var(--color-primary)` | Icon badge background fill |
| `--color-agenda-icon-fg` | `var(--color-on-primary)` | Icon badge glyph / letter colour |
| `--color-agenda-title` | `var(--color-on-surface)` | Entry title text colour |
| `--color-agenda-body` | `var(--color-on-surface-variant)` | Entry description / body colour |
| `--color-agenda-highlight-bg` | `var(--color-primary-container)` | Highlighted entry row background |
| `--color-agenda-highlight-fg` | `var(--color-on-primary-container)` | Highlighted entry text colour |
| `--color-agenda-divider` | `var(--color-line-default)` | Between-entry divider line colour |

### Per-Card Instance Override Keys

Written in the YAML block of an `agenda-card` molecule in `deck.md`.
Priority chain: **per-card prop → `--color-agenda-*` CSS token → semantic fallback**.

| Key | Description |
|-----|-------------|
| `label-color` | Override `--color-agenda-label` for this card only |
| `icon-bg` | Override `--color-agenda-icon-bg` for this card only |
| `icon-fg` | Override `--color-agenda-icon-fg` for this card only |
| `title-color` | Override `--color-agenda-title` for this card only |
| `body-color` | Override `--color-agenda-body` for this card only |
| `highlight-bg` | Override `--color-agenda-highlight-bg` for this card only |
| `show-dividers` | `true/false` — show or hide the between-entry divider lines |
| `divider-color` | Colour for between-entry dividers |
| `show-header` | `true/false` — show or hide the card header zone |
