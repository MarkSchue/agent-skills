# Template: grid-1-2

```yaml
id: grid-1-2
type: template
description: >
  Two columns where the right column is twice the width of the left column (1:2 ratio).
  Ideal for a narrow callout or KPI on the left with a wide main content on the right.
tags: [grid, asymmetric, two-column, featured, wide-right]
compatible_molecules: [kpi-card, mission-card, chart-card, objective-card, stacked-text]
```

## Layout Pictogram

```
┌──────────────────────────────────────────────────────────────────────────┐
│  [accent bar]   [logo-primary]                    [logo-secondary]       │
│  SLIDE TITLE                                                             │
│  ─────────────────────────────────────────── [header divider]           │
│                                                                          │
│  ┌─────────────────┐  ┌─────────────────────────────────────┐           │
│  │                 │  │                                     │           │
│  │  BLOCK A (1×)   │  │        BLOCK B  (2× width)          │           │
│  │                 │  │                                     │           │
│  │                 │  │                                     │           │
│  └─────────────────┘  └─────────────────────────────────────┘           │
│                                                                          │
│  ─────── [footer divider]                       [page number]           │
└──────────────────────────────────────────────────────────────────────────┘
```

## Slot Specifications

| Slot | Accepts | Required | Width |
|------|---------|----------|-------|
| Block A (left) | any molecule | yes | `(canvas_w − 2×margin − gap) × 1/3` |
| Block B (right) | any molecule | no | `(canvas_w − 2×margin − gap) × 2/3` |

## CSS Token Reference

Same tokens as `grid-2`. Width ratio is fixed at 1:2 by the layout slug.

## Example Usage

```markdown
# Team OKR Status
<!-- layout: grid-1-2 -->

## Status
```yaml
molecule: kpi-card
value: On Track
trend: up
icon-name: check_circle
```

## Objective Progress
```yaml
molecule: objective-card
quarter: "Q3 2025"
objective: "Establish the data platform as the enterprise analytics standard"
key-results:
  - text: Onboard 8 business units
    progress: 75
  - text: Train 200 analysts
    progress: 90
```
```
