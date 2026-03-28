# Template: grid-2-1

```yaml
id: grid-2-1
type: template
description: >
  Two columns where the left column is twice the width of the right column (2:1 ratio).
  Ideal for pairing a main content molecule with a supporting KPI or callout.
tags: [grid, asymmetric, two-column, featured, wide-left]
compatible_molecules: [mission-card, chart-card, objective-card, kpi-card, stacked-text]
```

## Layout Pictogram

```
┌──────────────────────────────────────────────────────────────────────────┐
│  [accent bar]   [logo-primary]                    [logo-secondary]       │
│  SLIDE TITLE                                                             │
│  ─────────────────────────────────────────── [header divider]           │
│                                                                          │
│  ┌─────────────────────────────────────┐  ┌─────────────────┐           │
│  │                                     │  │                 │           │
│  │         BLOCK A  (2× width)         │  │  BLOCK B (1×)   │           │
│  │                                     │  │                 │           │
│  │                                     │  │                 │           │
│  └─────────────────────────────────────┘  └─────────────────┘           │
│                                                                          │
│  ─────── [footer divider]                       [page number]           │
└──────────────────────────────────────────────────────────────────────────┘
```

## Slot Specifications

| Slot | Accepts | Required | Width |
|------|---------|----------|-------|
| Block A (left) | any molecule | yes | `(canvas_w − 2×margin − gap) × 2/3` |
| Block B (right) | any molecule | no | `(canvas_w − 2×margin − gap) × 1/3` |

## CSS Token Reference

Same tokens as `grid-2`. Width ratio is fixed at 2:1 by the layout slug.

## Example Usage

```markdown
# Strategic Mission
<!-- layout: grid-2-1 -->

## Our Mission
```yaml
molecule: mission-card
title: Drive Platform Growth
statement: "Accelerate adoption of the unified data platform across all business units."
icon-name: rocket_launch
```

## Adoption Rate
```yaml
molecule: kpi-card
value: 73 %
unit: Adoption
trend: up
```
```
