# Molecule: data-insight-panel

```yaml
id: data-insight-panel
type: molecule
domain: data
layout: header-dual-column
description: Wide panel combining a chart with a text insight summary and optional supporting KPIs.
tags: [data, insight, analysis, chart, summary]
preview: previews/molecules/data-insight-panel.png
required_atoms: [text-heading, text-body, chart-bar, badge-status, shape-divider]
min_atoms: 2
max_atoms: 6
```

## Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  [text-heading: Panel Title]   [badge-status: timeframe]         │
│  ───────────────────────── [shape-divider]                       │
│                                                                  │
│  [chart-bar or chart-pie: 60% width]  │  [text-body: insight]   │
│                                       │  [text-body: insight]   │
│                                                                  │
│  [kpi-card mini] [kpi-card mini] [kpi-card mini]                 │
└──────────────────────────────────────────────────────────────────┘
```

- Left 60%: chart atom. Right 40%: written key insights as bullets.
- Bottom strip (optional): 2-3 mini KPI values.

## Atoms and Roles

| Atom | Role | Required |
|---|---|---|
| `text-heading` | Panel title | yes |
| `chart-bar` or `chart-pie` | Main chart | yes |
| `text-body` | Insight bullets | yes |
| `badge-status` | Time period label | no |
| `shape-divider` | Section separator | no |

## Visual Properties

| Property | Token |
|---|---|
| Panel background | `{{theme.color.surface}}` |
| Panel border | `{{theme.shape.border-subtle}}` |
| Title color | `{{theme.color.on-surface}}` |
| Insight bullet color | `{{theme.color.primary}}` |
| Padding | `{{theme.spacing.l}}` |

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `insights` | string | Value from props. |
| `show_bullets/show-bullets` | bool | Boolean toggle (true/false). |
| `text_align/text-align` | enum | Alignment enum (left/center/right or top/middle/bottom). |
| `timeframe` | string | Value from props. |
| `title` | string | Text string. |
## Example

```yaml
molecule: data-insight-panel
params:
  title: "Revenue by Segment"
  chart-type: pie
  chart-data:
    slices:
      - label: "Enterprise"; value: 55
      - label: "Mid-Market"; value: 30
      - label: "SMB"; value: 15
  insights:
    - "Enterprise grew 22% YoY, now representing majority share"
    - "SMB churn offset growth; requires retention focus"
  timeframe: "FY 2024"
```

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Panel container | `.data-insight-panel` | `background`, `border-color`, `border-radius` |
| Title text | `.data-insight-panel__title` → `u-text-on-surface u-type-label u-bold` | `color`, `font-size`, `font-weight` |
| Insight item text | `.data-insight-panel__item` → `u-text-on-surface-variant u-type-caption` | `color`, `font-size` |
