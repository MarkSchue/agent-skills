# Molecule: dot-chart-card

```yaml
id: dot-chart-card
type: molecule
domain: data
description: Split-layout card with lollipop dot-line chart on the left and a large stat number on the right.
tags: [data, dot-line, lollipop, metric, split-layout, visualization]
required_atoms: [chart-dot-line, stat-display, metric-footer]
min_atoms: 2
max_atoms: 3
preview: previews/molecules/dot-chart-card.png
```

## Layout Primitive
```
layout: split-left-right
```

## Zone Breakdown
```
┌─────────────────────────────────────────────────────┐
│  [chart-dot-line: left 42%] [stat-display: right 58%] │
│  lollipop sticks fill zone  │  large value + unit   │
│                             │  vertically centered  │
├─────────────────────────────────────────────────────┤
│  [metric-footer: left-label · right-label]          │
└─────────────────────────────────────────────────────┘
```

Zones identical to `waveform-card`:
- Footer height: `max(28, int(h * 0.08))`
- Main zone height: `h - footer_h - PAD`
- Left viz zone width: `w * 0.42`
- Right stat zone width: `w - left_w - PAD`

## Parameters
| Parameter | Type | Required | Description |
|---|---|---|---|
| `value` | string | yes | Stat value e.g. "1100" |
| `unit` | string | no | Unit label |
| `dot-data` | `list[number]` | no | Values for lollipop positions (5–10 recommended) |
| `dot-color-token` | color-token | no | Dot fill token; defaults `error` (red) |
| `left-label` | string | no | Footer left label |
| `right-label` | string | no | Footer right label |

## Visual Properties
- Background: `{{theme.color.surface}}` (light / white)
- Dot fill: `{{theme.color.error}}` (red, matches screenshot)
- Stick line: `{{theme.color.on-surface-variant}}`
- Stat value color: `{{theme.color.on-surface}}`
- Footer text: `{{theme.color.on-surface-variant}}`
- Border: 1px `{{theme.color.border-subtle}}`
- Border radius: `{{theme.borders.radius-medium}}`

## Renderer Notes
- Light background — tokens are used as-is (no dark-flip)
- `dot-data` defaults to `[0.5, 0.7, 0.4, 0.8, 0.6, 0.9, 0.5]` if absent

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Card container | `.dot-chart-card` | `background`, `border-color`, `border-radius` |
| Title text | `.dot-chart-card__title` → `u-text-on-surface u-type-label` | `color`, `font-size` |
| Dot element | `.dot-chart-card__dot` → `u-bg-primary` | `background` |
| Line element | `.dot-chart-card__line` → `u-border-subtle` | `border-color` |
