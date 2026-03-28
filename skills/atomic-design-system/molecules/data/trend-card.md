# Molecule: trend-card

```yaml
id: trend-card
type: molecule
domain: data
layout: kpi-zone
description: Card showing a metric trend over time with a small sparkline bar chart and contextual annotation.
tags: [data, trend, sparkline, time-series, performance]
preview: previews/molecules/trend-card.png
required_atoms: [text-heading, text-body, chart-bar, badge-status]
min_atoms: 2
max_atoms: 4
```

## Layout

```
┌──────────────────────────────────────────┐
│  [text-body: Metric label]               │
│  [text-heading: Current value]           │
│  [badge-status: △ Change vs prior]       │
│  ─────────────────────── sparkline ─     │
│  [chart-bar: mini, 5-12 periods]         │
└──────────────────────────────────────────┘
```

- Sparkline is a compact `chart-bar` rendered at reduced height (40-60px equivalent).
- Last bar highlighted in `{{theme.color.primary}}`; prior bars in `{{theme.color.neutral}}`.

## Atoms and Roles

| Atom | Role | Required |
|---|---|---|
| `text-body` | Metric label | yes |
| `text-heading` | Current value | yes |
| `badge-status` | Trend badge | no |
| `chart-bar` | Sparkline trend | no |

## Visual Properties

| Property | Token |
|---|---|
| Card background | `{{theme.color.surface}}` |
| Card border | `{{theme.shape.border-subtle}}` |
| Card radius | `{{theme.borders.radius-medium}}` |
| Current bar | `{{theme.color.primary}}` |
| Prior bars | `{{theme.color.neutral}}` |

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `label` | string | Metric name |
| `value` | string | Current period value |
| `change` | string | Period-on-period delta |
| `trend` | enum | `up` · `down` · `neutral` |
| `sparkline` | `list[number]` | 5-12 historical values in chronological order |
| `unit` | string | Unit suffix |

## Example

```yaml
molecule: trend-card
params:
  label: "Weekly Active Users"
  value: "142K"
  change: "+7%"
  trend: up
  unit: users
  sparkline: [98, 105, 112, 118, 125, 131, 142]
```

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Card container | `.trend-card` | `background`, `border-color`, `border-radius` |
| Value text | `.trend-card__value` → `u-text-on-secondary-container u-type-annotation` | `color`, `font-size`, `font-weight` |
| Label text | `.trend-card__label` → `u-text-on-secondary-container u-type-caption` | `color`, `font-size` |
| Trend up indicator | `.trend-card__trend--up` → `u-text-success` | `color` |
| Trend down indicator | `.trend-card__trend--down` → `u-text-error` | `color` |
| Subtitle text | `.trend-card__subtitle` → `u-text-on-surface-variant u-type-caption` | `color`, `font-size` |
