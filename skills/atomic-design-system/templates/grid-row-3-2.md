# Template: grid-row-3-2

```yaml
id: grid-row-3-2
type: template
description: >
  3 × 2 grid (3 columns, 2 rows) with equal cell sizes. Blocks placed in row-major
  order. Ideal for comparing two scenarios across three dimensions.
tags: [grid, rows, 3x2, dashboard, six-cell]
compatible_molecules: [kpi-card, mission-card, stacked-text]
```

## Layout Pictogram

```
┌──────────────────────────────────────────────────────────────────────────┐
│  SLIDE TITLE   ─────────────────────── [header divider]                 │
│                                                                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐         │
│  │                 │  │                 │  │                 │         │
│  │   cell (1,1)    │  │   cell (1,2)    │  │   cell (1,3)    │         │
│  │                 │  │                 │  │                 │         │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐         │
│  │                 │  │                 │  │                 │         │
│  │   cell (2,1)    │  │   cell (2,2)    │  │   cell (2,3)    │         │
│  │                 │  │                 │  │                 │         │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘         │
│                                                                          │
│  ─────── [footer divider]                       [page number]           │
└──────────────────────────────────────────────────────────────────────────┘
```

## Slot Specifications

Blocks are assigned in row-major order (left-to-right, top-to-bottom):

| Index | Position | Width | Height |
|-------|----------|-------|--------|
| 0 | row 1, col 1 | `(cw − 2×gap) / 3` | `(ch − gap) / 2` |
| 1 | row 1, col 2 | same | same |
| 2 | row 1, col 3 | same | same |
| 3 | row 2, col 1 | same | same |
| 4 | row 2, col 2 | same | same |
| 5 | row 2, col 3 | same | same |

## CSS Token Reference

Same tokens as `grid-2` and `row-2`. Grid dimensions are fixed at 3×2 by the layout slug.

## Example Usage

```markdown
# Quarterly KPIs by Metric
<!-- layout: grid-row-3-2 -->

## Q1 Revenue
```yaml
molecule: kpi-card
value: "€ 980 K"
trend: up
```

## Q2 Revenue
```yaml
molecule: kpi-card
value: "€ 1.1 M"
trend: up
```

## Q3 Revenue
```yaml
molecule: kpi-card
value: "€ 1.0 M"
trend: neutral
```

## Q1 Users
```yaml
molecule: kpi-card
value: "14 200"
unit: MAU
trend: up
```

## Q2 Users
```yaml
molecule: kpi-card
value: "16 100"
unit: MAU
trend: up
```

## Q3 Users
```yaml
molecule: kpi-card
value: "18 400"
unit: MAU
trend: up
```
```
