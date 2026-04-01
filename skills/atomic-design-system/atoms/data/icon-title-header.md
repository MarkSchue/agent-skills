# Atom: icon-title-header

```yaml
id: icon-title-header
type: composite
description: Header row with a square icon tile, bold title, subtitle, and optional right-aligned pill badge.
tags: [header, icon, title, subtitle, badge, pill, section-header]
preview: previews/atoms/icon-title-header.png
```

## Layout Primitive
```
layout: fill-zone
zone-role: header
```
Full-width header occupying the top portion of the parent card.

## Parameters
| Parameter | Type | Required | Description |
|---|---|---|---|
| `icon` | string | no |
| `icon-bg-token` | color-token | no |
| `icon-color-token` | color-token | no |
| `pill` | string | no |
| `pill-bg-token` | color-token | no |
| `pill-color-token` | color-token | no |
| `subtitle` | string | no |
| `title` | string | yes |
## Visual Properties
| Property | Token / Formula |
|---|---|
| Zone height | `max(40, int(card_h * 0.15))` |
| Icon tile size | `zone_h - PAD * 2` × same (square) |
| Icon tile radius | `{{theme.borders.radius-medium}}` |
| Title font size | `max(14, int(zone_h * 0.35))` pt, bold |
| Subtitle font size | `max(11, int(zone_h * 0.25))` pt |
| Pill height | `zone_h * 0.50` |
| Pill border radius | `{{theme.borders.radius-large}}` |

## Renderer Notes
- Icon tile is left-anchored with PAD offset from card left edge
- Title sits vertically centered to right of icon tile with gap = PAD
- Pill floats right-anchored to card right edge minus PAD
- Divider line (`border-subtle`) drawn below this zone when inside `stats-chart-panel`

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Icon element | `.icon-title-header__icon` → `u-text-primary` | `border-radius` |
| Title text | `.icon-title-header__title` → `u-text-on-surface u-type-label` | `font-size` |
| Badge element | `.icon-title-header__badge` → `u-bg-primary u-text-on-primary` | `font-size` |
