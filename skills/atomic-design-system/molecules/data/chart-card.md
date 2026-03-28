# Molecule: chart-card

```yaml
id: chart-card
type: molecule
domain: data
layout: hero-full
description: Self-contained card wrapping any chart atom with a title, timeframe badge, and data source note.
tags: [data, chart, visualization, wrapper, figure]
preview: previews/molecules/chart-card.png
required_atoms: [text-heading, text-body, badge-status, chart-bar, chart-pie]
min_atoms: 2
max_atoms: 4
```

## Layout

```
┌──────────────────────────────────────────────────────┐
│  [text-heading: Chart Title]  [badge-status: period] │
│  ─────────────────────────── [shape-divider]         │
│                                                      │
│     [chart-bar  OR  chart-pie  OR  chart-gantt]      │
│                                                      │
│  [text-body: Source / note]                          │
└──────────────────────────────────────────────────────┘
```

- Chart type is inferred from `chart-type` parameter.
- Card acts as a semantic wrapper; the chart atom carries its own data schema.

## Atoms and Roles

| Atom | Role | Required |
|---|---|---|
| `text-heading` | Chart title | yes |
| `chart-bar` or `chart-pie` or `chart-gantt` | Chart | yes |
| `badge-status` | Time period badge | no |
| `text-body` | Data source note | no |
| `shape-divider` | Header separator | no |

## Visual Properties

| Property | Token |
|---|---|
| Card background | `{{theme.color.surface}}` |
| Card border | `{{theme.shape.border-subtle}}` |
| Card radius | `{{theme.borders.radius-medium}}` |
| Source text color | `{{theme.color.neutral}}` |
| Padding | `{{theme.spacing.l}}` |

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `title` | string | Chart heading |
| `chart-type` | enum | `bar` · `pie` · `gantt` |
| `chart-data` | object | Data passed to the chosen chart atom's schema |
| `period` | string | Optional time period badge text |
| `source` | string | Data source attribution |

## Example

```yaml
molecule: chart-card
params:
  title: "Monthly Net New Customers"
  chart-type: bar
  chart-data:
    labels: [Jan, Feb, Mar, Apr, May, Jun]
    values: [34, 41, 38, 52, 61, 58]
    unit: customers
  period: "H1 2025"
  source: "CRM Export – 2025-07-01"
```

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Card container | `.chart-card` | `background`, `border-radius` |
| Title text | `.chart-card__title` → `u-text-on-surface u-type-label` | `color`, `font-size` |
| Bar element | `.chart-card__bar` → `u-bg-primary` | `background` |
| Bar label text | `.chart-card__bar-label` → `u-text-on-primary u-type-annotation` | `color`, `font-size` |
| Legend text | `.chart-card__legend` → `u-text-on-surface-variant u-type-annotation` | `color`, `font-size` |
