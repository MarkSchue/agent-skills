# Atom: metric-footer

```yaml
id: metric-footer
type: text
description: Two-pair label-value footer row pinned to card bottom; for range, unit, or reference context.
tags: [footer, metric, label, range, reference, context, bottom]
preview: previews/atoms/metric-footer.png
```

## Layout Primitive
```
layout: fill-zone
zone-role: footer
```
Pinned to the bottom of the parent card. Sits above `border-subtle` top separator line.

## Parameters
| Parameter | Type | Required | Description |
|---|---|---|---|
| `left-label` | string | yes | Left label text e.g. "Heart rate" |
| `left-value` | string | no | Left value text e.g. "60–100 bpm"; if absent only label shown |
| `right-label` | string | no | Right label text |
| `right-value` | string | no | Right value text e.g. "2L per day" |
| `color-token` | color-token | no | Text color; defaults `on-surface-variant` |
| `separator` | boolean | no | Draw top border line; defaults `true` |

## Visual Properties
| Property | Token / Formula |
|---|---|
| Height | `max(28, int(card_h * 0.08))` |
| Font size | 10pt |
| Text color | `{{theme.color.on-surface-variant}}` |
| Separator | 1px `{{theme.color.border-subtle}}` top-of-zone |
| Horizontal alignment | left-label left-anchored; right-label right-anchored |

## Renderer Notes
- Footer zone is always the bottom `max(28, card_h * 0.08)` pixels of the card
- Only `left-label` is required; right side pair is optional
- Separator line spans full card width minus PAD*2

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Divider line | `.metric-footer__divider` → `u-border-subtle` | `border-color` |
| Label text | `.metric-footer__label` → `u-text-on-surface-variant u-type-caption` | `font-size` |
| Value text | `.metric-footer__value` → `u-text-on-surface u-type-label` | `font-size` |
