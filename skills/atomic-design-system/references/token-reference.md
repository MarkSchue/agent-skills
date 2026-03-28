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
