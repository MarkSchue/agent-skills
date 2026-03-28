# Template: grid-2

```yaml
id: grid-2
type: template
description: >
  Two equal-width columns for side-by-side content. Columns share the full
  available height. Gutter and padding are CSS-token-driven.
tags: [grid, two-column, comparison, parallel, split]
compatible_molecules: [kpi-card, mission-card, chart-card, objective-card, quote-card, stacked-text]
```

## Layout Pictogram

```
┌──────────────────────────────────────────────────────────────────────────┐
│  [accent bar]                                                            │
│  [logo-primary]                              [logo-secondary]            │
│  ────────────────────────────────────────────────────────────────────── │
│  SLIDE TITLE                                                             │
│  ──────────────────────────────────── [header divider]                  │
│                                                                          │
│  ┌─────────────────────────────┐  ┌─────────────────────────────┐       │
│  │                             │  │                             │       │
│  │         BLOCK A             │  │         BLOCK B             │       │
│  │       (50% width)           │  │       (50% width)           │       │
│  │                             │  │                             │       │
│  │                             │  │                             │       │
│  └─────────────────────────────┘  └─────────────────────────────┘       │
│                                                                          │
│  ──────────────────────────── [footer divider]                          │
│  [footer text]                                    [page number]          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Slot Specifications

| Slot | Accepts | Required | Width |
|------|---------|----------|-------|
| Block A | any molecule | yes | `(canvas_w − 2×margin − gap) / 2` |
| Block B | any molecule | no | same as A |

The renderer auto-scales to the number of populated blocks (1–2).

## CSS Token Reference

### Slide chrome
| Token | Default | Purpose |
|-------|---------|---------|
| `--slide-bg-color` | `var(--color-surface)` | Whole-slide background fill |
| `--slide-bg-image` | `none` | Background image |
| `--logo-primary-src` | `none` | Left logo |
| `--logo-secondary-src` | `none` | Right logo |

### Header / footer lines
| Token | Default | Purpose |
|-------|---------|---------|
| `--slide-divider-width` | `100%` | Header line span |
| `--slide-divider-align` | `left` | `left` \| `center` \| `right` |
| `--slide-footer-divider-width` | `100%` | Footer line span |
| `--slide-footer-divider-align` | `left` | `left` \| `center` \| `right` |

### Content area & blocks
| Token | Default | Purpose |
|-------|---------|---------|
| `--content-area-bg-color` | `transparent` | Content-zone background |
| `--content-area-padding` | `0` | Inset around all blocks (px) |
| `--content-block-gap` | `24` | Gap between the two columns (px) |
| `--content-block-bg-color` | `transparent` | Default fill for each column |
| `--content-block-padding` | `0` | Inner padding per column (px) |

## Example Usage

```markdown
# Revenue vs. Users
<!-- layout: grid-2 -->

## Revenue
```yaml
molecule: kpi-card
value: "€ 4.2 M"
unit: YTD
trend: up
```

## Active Users
```yaml
molecule: kpi-card
value: "18 400"
unit: MAU
trend: up
```
```
