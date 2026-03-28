# Template: grid-3

```yaml
id: grid-3
type: template
description: >
  Three equal-width columns for parallel content. Scales to the number of
  populated blocks (2–4). Gutter and padding are CSS-token-driven.
tags: [grid, three-column, parallel, overview, cards]
compatible_molecules: [kpi-card, mission-card, chart-card, objective-card, quote-card, stacked-text]
```

## Layout Pictogram

```
┌──────────────────────────────────────────────────────────────────────────┐
│  [accent bar]                                                            │
│  [logo-primary]                              [logo-secondary]            │
│  SLIDE TITLE                                                             │
│  ──────────────────────────────────────────────── [header divider]      │
│                                                                          │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐               │
│  │               │  │               │  │               │               │
│  │   BLOCK A     │  │   BLOCK B     │  │   BLOCK C     │               │
│  │  (33% width)  │  │  (33% width)  │  │  (33% width)  │               │
│  │               │  │               │  │               │               │
│  │               │  │               │  │               │               │
│  └───────────────┘  └───────────────┘  └───────────────┘               │
│                                                                          │
│  ──────────────────── [footer divider]  [page number]                   │
└──────────────────────────────────────────────────────────────────────────┘
```

## Slot Specifications

| Slot | Accepts | Required | Width |
|------|---------|----------|-------|
| Block A | any molecule | yes | `(canvas_w − 2×margin − 2×gap) / 3` |
| Block B | any molecule | no | same |
| Block C | any molecule | no | same |

Renderer auto-scales to 2–4 blocks.

## CSS Token Reference

### Content area & blocks
| Token | Default | Purpose |
|-------|---------|---------|
| `--content-area-bg-color` | `transparent` | Content-zone background |
| `--content-area-padding` | `0` | Inset around all blocks (px) |
| `--content-block-gap` | `24` | Column gutter (px) |
| `--content-block-bg-color` | `transparent` | Default fill per column |
| `--content-block-padding` | `0` | Inner padding per column (px) |

(Slide-chrome and divider tokens same as `grid-2` — see that template.)

## Example Usage

```markdown
# KPIs at a Glance
<!-- layout: grid-3 -->

## Reliability
```yaml
molecule: kpi-card
value: 99.94 %
trend: up
```

## Latency
```yaml
molecule: kpi-card
value: 48 ms
trend: down
```

## Errors
```yaml
molecule: kpi-card
value: 0.06 %
trend: down
```
```
