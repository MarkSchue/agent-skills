# Molecule: header-list-card

```yaml
id: header-list-card
type: molecule
domain: team
description: Card with a prominent header strip (avatar · name · detail), a labeled two-column item list, and an optional CTA button.
tags: [team, list, items, profile, header-strip, cta, schedule, booking]
required_atoms: [icon-wrapper, text-heading, text-body, badge-status, shape-divider]
min_atoms: 3
max_atoms: 5
preview: previews/molecules/header-list-card.png
```

## Layout Primitive
```
layout: stacked-header-body
```

## Zone Breakdown
```
┌───────────────────────────────────────────────────┐
│  [Header strip]                                   │
│  avatar · header-name · header-detail             │
├───────────────────────────────────────────────────┤
│  section-label                                    │
│  ┌────────────────┐  ┌────────────────┐           │
│  │ item-label     │  │ item-label     │           │
│  │ item-avatar    │  │ item-avatar    │           │
│  │ item-title     │  │ item-title     │           │
│  │ item-detail    │  │ item-detail    │           │
│  └────────────────┘  └────────────────┘           │
├───────────────────────────────────────────────────┤
│  [icon btn]  [icon btn]  [CTA button: right]      │
└───────────────────────────────────────────────────┘
```

Zone proportions:
- Header strip height: `max(52, int(h * 0.13))`
- Section label height: 22px
- Item cards: 2 columns, height `max(80, int(h * 0.22))` each
- Footer bar height: `max(40, int(h * 0.09))`

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `cta-label` | string | Label text content. |
| `header-detail` | string | Value from props. |
| `header-name` | string | Value from props. |
| `items` | list | List of data items. |
| `section-label` | string | Label text content. |
## Visual Properties
- Background: `{{theme.color.surface-variant}}`
- Header name: `{{theme.color.on-surface}}` 14pt bold
- Header detail: `{{theme.color.on-surface-variant}}` 11pt
- Section label: `{{theme.color.on-surface-variant}}` 12pt
- Item card bg: `{{theme.color.surface}}` with `border-subtle` border
- Item label: `{{theme.color.on-surface}}` 13pt bold
- Item title: `{{theme.color.on-surface}}` 11pt bold
- Item detail: `{{theme.color.on-surface-variant}}` 10pt
- CTA button: `{{theme.color.primary}}` bg, `{{theme.color.on-primary}}` text, `radius-large`
- Divider between header strip and item list: `{{theme.color.border-subtle}}`
- Border radius: `{{theme.borders.radius-medium}}`

## Renderer Notes
- Header avatar: small circle (radius = `strip_h * 0.38`) filled with `primary`, centered vertically in strip
- Item avatar: small square with `radius-medium` (24×24px), filled `surface-variant`
- If `items` has more than 2 entries, only the first 2 are shown
- CTA button right-anchored in the footer bar; icon buttons are 36×36 circles left-anchored

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Card container | `.header-list-card` | `background`, `border-color`, `border-radius` |
| Avatar element | `.header-list-card__avatar` → `u-bg-primary` | `background` |
| Title text | `.header-list-card__title` → `u-text-on-surface u-type-label` | `color`, `font-size` |
| Subtitle text | `.header-list-card__subtitle` → `u-text-on-surface-variant u-type-caption` | `color`, `font-size` |
| Badge element | `.header-list-card__badge` → `u-bg-primary u-text-on-primary` | `background`, `color` |
| Row label text | `.header-list-card__row-label` → `u-text-on-surface u-type-label` | `color`, `font-size` |
| Row value text | `.header-list-card__row-value` → `u-text-on-surface u-type-body` | `color`, `font-size` |
| Divider line | `.header-list-card__divider` → `u-border-subtle` | `border-color` |
