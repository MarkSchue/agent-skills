# Molecule: stats-chart-panel

```yaml
id: stats-chart-panel
type: molecule
domain: data
description: Wide panel with icon-title header, stacked stat column on the left, and a bar chart on the right.
tags: [data, stats, chart, panel, dual-column, bar-chart, periodic, visualization]
required_atoms: [icon-title-header, stat-display, chart-bar, shape-divider]
min_atoms: 3
max_atoms: 5
preview: previews/molecules/stats-chart-panel.png
```

## Layout Primitive
```
layout: header-dual-column
```

## Zone Breakdown
```
┌──────────────────────────────────────────────────────────┐
│  [icon-title-header: full width]  [pill: right]          │
├─────────────────────┬────────────────────────────────────┤
│  [stat-display ×N:  │  [chart-bar: right 65%]            │
│   left 35%,         │   vertical bars with dotted ref    │
│   stacked]          │   lines + bar-top labels           │
│                     │                                    │
└─────────────────────┴────────────────────────────────────┘
```

Zone proportions (relative to card height `h` and width `w`):
- Header height: `max(40, int(h * 0.18))`
- Body height: `h - header_h - PAD * 2`
- Left stat column width: `w * 0.35`
- Right chart width: `w - left_w - PAD`

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `badge` | string | Value from props. |
| `chart-labels` | string | Label text content. |
| `chart-unit` | string | Value from props. |
| `chart-values` | list | List of data items. |
| `highlight-bar` | string | Value from props. |
| `labels` | string | Label text content. |
| `period` | string | Value from props. |
| `ref-lines` | string | Value from props. |
| `stats` | list | List of data items. |
| `subtitle` | string | Text string. |
| `text_align/text-align` | enum | Alignment enum (left/center/right or top/middle/bottom). |
| `title` | string | Text string. |
| `unit` | string | Text string. |
| `values` | list | Value from props. |
## Visual Properties
- Background: `{{theme.color.on-surface}}` (dark)
- Icon tile bg: `{{theme.color.primary}}`
- Title color: `{{theme.color.surface}}`
- Subtitle color: `{{theme.color.on-surface-variant}}`
- Pill bg: `{{theme.color.surface-variant}}`, text: `{{theme.color.on-surface}}`
- Stat value color: `{{theme.color.surface}}`
- Stat label color: `{{theme.color.on-surface-variant}}`
- Highlighted bar: `{{theme.color.primary}}`
- Normal bars: `{{theme.color.surface-variant}}` at 60% opacity (muted)
- Reference lines: `{{theme.color.on-surface-variant}}` dotted
- Bar top labels: `{{theme.color.on-surface-variant}}` 9pt
- Border radius: `{{theme.borders.radius-medium}}`

## Renderer Notes
- Dark background; tokens used via dark-surface variants
- Stats column `dot-color-token` (if present per stat) draws a small dot before the stat label
- Reference lines drawn as dotted horizontal strokes at their proportional Y positions
- Highlighted bar uses `primary` color; all other bars use muted `surface-variant`

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Panel container | `.stats-chart-panel` | `background`, `border-color`, `border-radius` |
| Header text | `.stats-chart-panel__header` → `u-text-on-surface u-type-label u-bold` | `color`, `font-size`, `font-weight` |
| Bar element | `.stats-chart-panel__bar` → `u-bg-primary` | `background` |
| Bar label text | `.stats-chart-panel__bar-label` → `u-text-on-primary u-type-annotation` | `color`, `font-size` |
| Badge element | `.stats-chart-panel__badge` → `u-bg-primary u-text-on-primary` | `background`, `color` |
| Legend text | `.stats-chart-panel__legend` → `u-text-on-surface-variant u-type-annotation` | `color`, `font-size` |
