# Molecule: daily-header-card

```yaml
id: daily-header-card
type: molecule
domain: data
description: Full-width dark hero card with a large multi-line title and a date/time footer row.
tags: [data, header, title, date, time, overview, display, hero]
required_atoms: [text-heading, text-body, metric-footer]
min_atoms: 2
max_atoms: 3
preview: previews/molecules/daily-header-card.png
```

## Layout Primitive
```
layout: hero-full
```

## Zone Breakdown
```
┌──────────────────────────────────────────────────┐
│  [text-heading: large multi-line title]          │
│  [text-heading: line 2 of title if needed]       │
│                                                  │
├──────────────────────────────────────────────────┤
│  [date text: left]              [time: right]    │
└──────────────────────────────────────────────────┘
```

Proportions:
- Title zone: `h - footer_h - PAD * 2`
- Footer height: `max(24, int(h * 0.10))`
- Title font: `max(28, int(h * 0.12))` pt, bold, `surface` color

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `date` | string | Value from props. |
| `left_label/left-label` | string | Label text content. |
| `left_value/left-value` | string | Value from props. |
| `right_label/right-label` | string | Label text content. |
| `right_value/right-value` | string | Value from props. |
| `stat_color/stat-color` | color-token | Color token name (theme color). |
| `subtitle` | string | Text string. |
| `text_align/text-align` | enum | Alignment enum (left/center/right or top/middle/bottom). |
| `time` | string | Value from props. |
| `title` | string | Text string. |
## Visual Properties
- Background: `{{theme.color.on-surface}}` (dark)
- Title color: `{{theme.color.surface}}` (white / near-white)
- Date color: `{{theme.color.on-surface-variant}}`
- Time color: `{{theme.color.on-surface-variant}}`
- No border, no separator between title and footer
- Border radius: `{{theme.borders.radius-medium}}`

## Renderer Notes
- Title wraps — allow up to 3 lines; each line at title_sz pt
- No icon, no badge — purely typographic
- Date left-anchored, time right-anchored in footer zone
- Footer typography uses the shared card footer tokens (`--card-footer-*`) so it stays aligned with other cards

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Card container | `.daily-header-card` | `background`, `border-radius` |
| Date text | `.daily-header-card__date` → `u-text-on-surface-variant u-type-caption` | `color`, `font-size` |
| Subtitle text | `.daily-header-card__subtitle` → `u-text-on-surface-variant u-type-caption` | `color`, `font-size` |
