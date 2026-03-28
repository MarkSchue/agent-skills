# Molecule: waveform-card

```yaml
id: waveform-card
type: molecule
domain: data
description: Split-layout card with amplitude waveform visualization on the left and a large stat number on the right.
tags: [data, waveform, metric, split-layout, visualization, signal]
required_atoms: [chart-waveform, stat-display, metric-footer]
min_atoms: 2
max_atoms: 3
preview: previews/molecules/waveform-card.png
```

## Layout Primitive
```
layout: split-left-right
```

## Zone Breakdown
```
┌─────────────────────────────────────────────────────┐
│  [chart-waveform: left 42%]  [stat-display: right 58%] │
│  amplitude bars fill zone   │  large value + unit   │
│                             │  vertically centered  │
├─────────────────────────────────────────────────────┤
│  [metric-footer: left-label · right-label·value]    │
└─────────────────────────────────────────────────────┘
```

Zones (proportional to card height `h`):
- Footer height: `max(28, int(h * 0.08))`
- Main zone height: `h - footer_h - PAD`
- Left viz zone width: `w * 0.42`
- Right stat zone width: `w - left_w - PAD`

## Parameters
| Parameter | Type | Required | Description |
|---|---|---|---|
| `value` | string | yes | Stat value e.g. "90" |
| `unit` | string | no | Unit label e.g. "bpm" |
| `waveform-data` | `list[float 0–1]` | no | Amplitude values; auto-generates if absent |
| `left-label` | string | no | Footer left label text |
| `right-label` | string | no | Footer right label |
| `right-value` | string | no | Footer right value |

## Visual Properties
- Background: `{{theme.color.on-surface}}` (dark surface)
- Waveform bar color: `{{theme.color.primary}}` tint at 70% opacity → use `on-primary-container` on dark bg
- Stat value color: `{{theme.color.surface}}` (white on dark)
- Unit color: `{{theme.color.surface}}` (smaller, same row)
- Footer text: `{{theme.color.on-surface-variant}}`
- Footer separator: `{{theme.color.border-subtle}}` (30% opacity on dark bg)
- Border radius: `{{theme.borders.radius-medium}}`
- No outer border/stroke

## Renderer Notes
- Card background is `on-surface` (dark); all text tokens flipped to light variants
- stat-display `value-color-token: surface` and `unit-color-token: surface`
- Footer `color-token: on-surface-variant` but rendered with reduced opacity on dark bg
- Auto-waveform if `waveform-data` absent

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Card container | `.waveform-card` | `background`, `border-color`, `border-radius` |
| Title text | `.waveform-card__title` → `u-text-on-surface u-type-label` | `color`, `font-size` |
| Bar element | `.waveform-card__bar` → `u-bg-primary` | `background` |
| Timestamp text | `.waveform-card__timestamp` → `u-text-on-surface-variant u-type-annotation` | `color`, `font-size` |
