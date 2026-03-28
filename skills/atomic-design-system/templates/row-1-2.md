# Template: row-1-2

```yaml
id: row-1-2
type: template
description: >
  Two rows where the bottom row is twice the height of the top row (1:2 ratio).
  Ideal for a headline KPI on top, with a main chart or content area below.
tags: [rows, asymmetric, two-row, tall-bottom]
compatible_molecules: [kpi-card, chart-card, mission-card, stacked-text]
```

## Layout Pictogram

```
┌──────────────────────────────────────────────────────────────────────────┐
│  SLIDE TITLE   ─────────────────────── [header divider]                 │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │                    BLOCK A  (top, 1× height)                  │     │
│  └────────────────────────────────────────────────────────────────┘     │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │                                                                │     │
│  │                   BLOCK B  (bottom, 2× height)                │     │
│  │                                                                │     │
│  │                                                                │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                                                                          │
│  ─────── [footer divider]                       [page number]           │
└──────────────────────────────────────────────────────────────────────────┘
```

## Slot Specifications

| Slot | Accepts | Required | Height |
|------|---------|----------|--------|
| Block A (top) | any molecule | yes | `(content_h − gap) × 1/3` |
| Block B (bottom) | any molecule | no | `(content_h − gap) × 2/3` |

## CSS Token Reference

Same tokens as `row-2`. Height ratio is fixed at 1:2 by the layout slug.

## Example Usage

```markdown
# Performance Deep Dive
<!-- layout: row-1-2 -->

## Key Number
```yaml
molecule: kpi-card
value: "€ 4.2 M"
unit: Total Revenue YTD
trend: up
```

## Quarterly Chart
```yaml
molecule: chart-card
chart-type: bar
title: Quarterly Revenue (€ M)
labels: [Q1, Q2, Q3, Q4]
values: [0.98, 1.1, 1.0, 1.12]
```
```
