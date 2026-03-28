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
| Parameter | Type | Required | Description |
|---|---|---|---|
| `title` | string | yes | Main title text e.g. "Daily healthy overview" |
| `date` | string | no | Date string e.g. "Sunday, 10 October 2023" |
| `time` | string | no | Time string e.g. "11:00 AM" |

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

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Card container | `.daily-header-card` | `background`, `border-radius` |
| Date text | `.daily-header-card__date` → `u-text-on-surface-variant u-type-annotation` | `color`, `font-size` |
| Subtitle text | `.daily-header-card__subtitle` → `u-text-on-surface-variant u-type-caption` | `color`, `font-size` |
