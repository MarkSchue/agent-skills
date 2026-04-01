# Atom: stat-display

```yaml
id: stat-display
type: text
description: Large metric number with superscript unit and optional sublabel — the canonical big-number display atom.
tags: [stat, number, metric, kpi, value, display, large]
preview: previews/atoms/stat-display.png
```

## Layout Primitive
```
layout: kpi-zone  (or fill-zone when standalone)
zone-role: stat-right
```

## Parameters
| Parameter | Type | Required | Description |
|---|---|---|---|
| `align` | enum | no |
| `sublabel` | string | no |
| `sublabel-color-token` | color-token | no |
| `unit` | string | no |
| `unit-color-token` | color-token | no |
| `value` | string | yes |
| `value-color-token` | color-token | no |
## Visual Properties
| Property | Token / Formula |
|---|---|
| Value font | `{{theme.typography.font-family}}` |
| Value size | `max(36, min(96, int(zone_h * 0.20)))` pt |
| Unit size | `max(14, int(zone_h * 0.06))` pt, superscript-aligned top-right |
| Sublabel size | 11pt, `{{theme.color.on-surface-variant}}` |
| Value color | `{{theme.color.on-surface}}` |

## Sizing Zones
When used inside `split-left-right`:
  - zone_h = card_h × 0.60 (value+unit block in center of right zone)
  - sublabel sits 6px below value baseline

When used standalone (stacked stat in `stats-chart-panel`):
  - zone_h = allocated row height (card_h / n_stats)

## Renderer Notes
- Value and unit rendered on the same baseline; unit is smaller and top-aligned
- If `align: right` the entire block is right-aligned within the zone (default for health cards)
- If `align: left` the block is left-aligned (default for stats-chart-panel stacked stats)

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Value text | `.stat-display__value` → `u-text-on-primary-container u-type-annotation` | `font-size`, `font-weight` |
| Label text | `.stat-display__label` → `u-text-on-primary-container u-type-caption` | `font-size` |
