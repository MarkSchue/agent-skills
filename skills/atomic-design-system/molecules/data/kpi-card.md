# Molecule: kpi-card

```yaml
id: kpi-card
type: molecule
domain: data
layout: kpi-zone
description: Single KPI card showing a metric value, unit, trend indicator, and comparison reference.
tags: [data, kpi, metric, performance, value]
preview: previews/molecules/kpi-card.png
required_atoms: [text-heading, text-body, badge-status, icon-wrapper]
min_atoms: 1
max_atoms: 4
```

## Layout

```
┌────────────────────────────────┐
│  [icon-wrapper]  [text-body: KPI Label]     │
│  [text-heading: Value + Unit]               │
│  [badge-status: Change △ +12%]             │
│  [text-body: vs. Prior Period]              │
└─────────────────────────────────────────────┘
```

- Compact vertical stack; designed to be placed 3-4 per slide in a grid template.
- Value is large / prominent using `{{theme.typography.heading}}`.

## Atoms and Roles

| Atom | Role | Required |
|---|---|---|
| `text-body` | KPI label | yes |
| `text-heading` | KPI value | yes |
| `badge-status` | Trend / change badge | no |
| `icon-wrapper` | Metric icon | no |
| `text-body` | Comparison reference | no |

## Visual Properties

| Property | Token |
|---|---|
| Card background | `{{theme.color.surface}}` |
| Card border | `{{theme.shape.border-subtle}}` |
| Card radius | `{{theme.borders.radius-medium}}` |
| Value color | `{{theme.color.on-surface}}` |
| Positive trend | `{{theme.color.success}}` |
| Negative trend | `{{theme.color.error}}` |
| Neutral trend | `{{theme.color.neutral}}` |

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `change` | string | Text string. |
| `comparison` | string | Value from props. |
| `delta` | string | Value from props. |
| `icon` | string | Value from props. |
| `icon-name` | string | Value from props. |
| `label` | string | Text string. |
| `reference` | string | Value from props. |
| `text_align/text-align` | enum | Alignment enum (left/center/right or top/middle/bottom). |
| `title` | string | Text string. |
| `trend` | string | Trend enum (up/down/neutral). |
| `unit` | string | Text string. |
| `value` | string | Text string. |
## Example

```yaml
molecule: kpi-card
params:
  title: "Annual Recurring Revenue"  # canonical (alias: label)
  value: "€12.4M"
  change: "+18%"
  trend: up
  reference: "vs FY2023"
  icon-name: currency
```

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Card container | `.kpi-card` | `background`, `border-color`, `border-radius` |
| Value text | `.kpi-card__value` → `u-text-on-primary-container u-type-annotation` | `color`, `font-size`, `font-weight` |
| Label text | `.kpi-card__label` → `u-text-on-primary-container u-type-caption` | `color`, `font-size` |
| Trend up indicator | `.kpi-card__trend--up` → `u-text-success` | `color` |
| Trend down indicator | `.kpi-card__trend--down` → `u-text-error` | `color` |
| Subtitle text | `.kpi-card__subtitle` → `u-text-on-surface-variant u-type-caption` | `color`, `font-size` |
