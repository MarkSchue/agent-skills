# Template: grid-row-2-2

```yaml
id: grid-row-2-2
type: template
description: >
  2 × 2 grid (2 columns, 2 rows) with equal cell sizes. Blocks are placed in
  row-major order: (1,1), (1,2), (2,1), (2,2). Ideal for dashboard-style slides.
tags: [grid, rows, 2x2, dashboard, four-cell]
compatible_molecules: [kpi-card, mission-card, stacked-text]
```

## Layout Pictogram

```
┌──────────────────────────────────────────────────────────────────────────┐
│  SLIDE TITLE   ─────────────────────── [header divider]                 │
│                                                                          │
│  ┌───────────────────────────┐  ┌───────────────────────────┐           │
│  │                           │  │                           │           │
│  │       cell (1,1)          │  │       cell (1,2)          │           │
│  │                           │  │                           │           │
│  └───────────────────────────┘  └───────────────────────────┘           │
│  ┌───────────────────────────┐  ┌───────────────────────────┐           │
│  │                           │  │                           │           │
│  │       cell (2,1)          │  │       cell (2,2)          │           │
│  │                           │  │                           │           │
│  └───────────────────────────┘  └───────────────────────────┘           │
│                                                                          │
│  ─────── [footer divider]                       [page number]           │
└──────────────────────────────────────────────────────────────────────────┘
```

## Slot Specifications

Blocks are assigned in row-major order (left-to-right, top-to-bottom):

| Index | Position | Width | Height |
|-------|----------|-------|--------|
| 0 | row 1, col 1 | `(cw − gap) / 2` | `(ch − gap) / 2` |
| 1 | row 1, col 2 | same | same |
| 2 | row 2, col 1 | same | same |
| 3 | row 2, col 2 | same | same |

## CSS Token Reference

Same tokens as `grid-2` and `row-2`. Grid dimensions are fixed at 2×2 by the layout slug.

## Example Usage

```markdown
# Key Metrics
<!-- layout: grid-row-2-2 -->

## Users
```yaml
molecule: kpi-card
value: "18 400"
unit: MAU
trend: up
```

## Revenue
```yaml
molecule: kpi-card
value: "€ 4.2 M"
unit: YTD
trend: up
```

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
```
