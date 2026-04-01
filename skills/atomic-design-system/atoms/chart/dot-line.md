# Atom: chart-dot-line

```yaml
id: chart-dot-line
type: data-viz
description: Lollipop / dumbbell chart with vertical tick lines and dots at top and bottom of each stick.
tags: [chart, lollipop, dumbbell, dot-line, data-viz, scatter, visualization]
preview: previews/atoms/chart-dot-line.png
```

## Data Input Schema
```yaml
data-input-schema:
  values:      list[number], required: true    # one value per stick; normalized to [min, max] of the list
  dot-color-token: color-token, required: false, default: "error"    # color for dots
  line-color-token: color-token, required: false, default: "on-surface-variant"
```

## Layout Primitive
```
layout: fill-zone
zone-role: viz-left
```
Sticks are evenly spaced horizontally, filling the zone width.
Each stick: top dot at value-proportional height, bottom dot at baseline, vertical line connecting them.

## Visual Properties
| Property | Token |
|---|---|
| Dot fill | `{{theme.color.error}}` (overridable via `dot-color-token`) |
| Stick line | `{{theme.color.on-surface-variant}}` |
| Background | transparent |
| Dot radius | `max(5, int(zone_h * 0.04))` |
| Line width | 2px |

## Parameters
| Parameter | Type | Required | Description |
|---|---|---|---|
| `dot-color-token` | color-token | no |
| `line-color-token` | color-token | no |
| `values` | list[number] | yes |
## Renderer Notes
- Normalize `values` to `[0, 1]` range within the atom
- Top dot Y = `zone_y + zone_h - value * (zone_h - dot_r * 2) - dot_r`
- Bottom dot Y = `zone_y + zone_h - dot_r`
- Both top and bottom dots drawn at same X; line spans between them
- No axis labels, no gridlines

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Dot element | `.dot-line__dot` → `u-bg-primary` | `background`, `border-radius` |
| Line element | `.dot-line__line` → `u-border-subtle` | `border-color` |
