# Template: row-2-1

```yaml
id: row-2-1
type: template
description: >
  Two rows where the top row is twice the height of the bottom row (2:1 ratio).
  Ideal for a main chart or visual on top with a source note or KPI strip below.
tags: [rows, asymmetric, two-row, tall-top]
compatible_molecules: [chart-card, mission-card, kpi-card, stacked-text]
```

## Layout Pictogram

```
┌──────────────────────────────────────────────────────────────────────────┐
│  SLIDE TITLE   ─────────────────────── [header divider]                 │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │                                                                │     │
│  │                    BLOCK A  (top, 2× height)                  │     │
│  │                                                                │     │
│  │                                                                │     │
│  └────────────────────────────────────────────────────────────────┘     │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │                    BLOCK B  (bottom, 1× height)               │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                                                                          │
│  ─────── [footer divider]                       [page number]           │
└──────────────────────────────────────────────────────────────────────────┘
```

## Slot Specifications

| Slot | Accepts | Required | Height |
|------|---------|----------|--------|
| Block A (top) | any molecule | yes | `(content_h − gap) × 2/3` |
| Block B (bottom) | any molecule | no | `(content_h − gap) × 1/3` |

## CSS Token Reference

Same tokens as `row-2`. Height ratio is fixed at 2:1 by the layout slug.

## Example Usage

```markdown
# Revenue Breakdown
<!-- layout: row-2-1 -->

## Segment Share
```yaml
molecule: chart-card
chart-type: pie
title: Revenue by Segment
slices:
  - label: Enterprise
    value: 58
  - label: Mid-Market
    value: 28
  - label: SMB
    value: 14
```

## Source Note
```yaml
molecule: mission-card
statement: "Data as of end of Q2 2025. Enterprise = customers with > 1 000 seats."
```
```
