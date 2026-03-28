# Template: grid-4

```yaml
id: grid-4
type: template
description: >
  Four equal-width columns for dense parallel content such as quarterly KPIs
  or competitive feature comparisons.
tags: [grid, four-column, dense, quarterly, comparison]
compatible_molecules: [kpi-card, mission-card, stacked-text]
```

## Layout Pictogram

```
┌──────────────────────────────────────────────────────────────────────────┐
│  [accent bar]   [logo-primary]                    [logo-secondary]       │
│  SLIDE TITLE                                                             │
│  ─────────────────────────────────────────── [header divider]           │
│                                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│  │          │  │          │  │          │  │          │               │
│  │ BLOCK A  │  │ BLOCK B  │  │ BLOCK C  │  │ BLOCK D  │               │
│  │ (25% w)  │  │ (25% w)  │  │ (25% w)  │  │ (25% w)  │               │
│  │          │  │          │  │          │  │          │               │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘               │
│                                                                          │
│  ─────── [footer divider]                       [page number]           │
└──────────────────────────────────────────────────────────────────────────┘
```

## Slot Specifications

| Slot | Accepts | Required | Width |
|------|---------|----------|-------|
| Block A–D | any molecule | A required | `(canvas_w − 2×margin − 3×gap) / 4` |

## CSS Token Reference

Same tokens as `grid-2`. Column count is fixed at 4 by the layout slug.

## Example Usage

```markdown
# Quarterly Revenue
<!-- layout: grid-4 -->

## Q1
```yaml
molecule: kpi-card
value: "€ 980 K"
trend: up
```

## Q2
```yaml
molecule: kpi-card
value: "€ 1.1 M"
trend: up
```

## Q3
```yaml
molecule: kpi-card
value: "€ 1.0 M"
trend: neutral
```

## Q4
```yaml
molecule: kpi-card
value: "€ 1.12 M"
trend: up
```
```
