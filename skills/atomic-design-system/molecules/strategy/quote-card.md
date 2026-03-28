# Molecule: quote-card

```yaml
id: quote-card
type: molecule
domain: strategy
layout: hero-full
description: Pull-quote card with large typographic quote marks, attribution, and an optional portrait icon.
tags: [strategy, quote, testimonial, attribution, customer]
preview: previews/molecules/quote-card.png
required_atoms: [text-heading, text-body, icon-wrapper, shape-divider]
min_atoms: 1
max_atoms: 4
```

## Layout

```
┌──────────────────────────────────────────────────────┐
│  [shape-divider: accent-line]  (top left accent)     │
│                                                      │
│  " [text-body: Quote text] "                         │
│                                                      │
│  [icon-wrapper]  [text-heading: Name]                │
│                  [text-body: Title / Organization]  │
└──────────────────────────────────────────────────────┘
```

- Quote marks are typographic decorations using `{{theme.color.primary}}` (large, light opacity)
- Attribution row: optional portrait or icon left-aligned with name and title

## Atoms and Roles

| Atom | Role | Required |
|---|---|---|
| `text-body` | Quote text | yes |
| `text-heading` | Attribution name | no |
| `text-body` | Attribution title | no |
| `icon-wrapper` | Portrait / logo | no |
| `shape-divider` | Accent top rule | no |

## Visual Properties

| Property | Token |
|---|---|
| Card background | `{{theme.color.surface}}` |
| Accent rule | `{{theme.shape.accent-line}}` |
| Quote mark color | `{{theme.color.primary}}` |
| Quote text font | `{{theme.typography.body}}` |
| Attribution font | `{{theme.typography.caption}}` |
| Card radius | `{{theme.borders.radius-medium}}` |

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `quote` | string | The pull-quote text |
| `name` | string | Attributed person's name |
| `title` | string | Person's role or organization |
| `icon-name` | string | Portrait icon or company logo icon |

## Example

```yaml
molecule: quote-card
params:
  quote: "This platform reduced our planning cycle from 6 weeks to 3 days."
  name: "Maria Schneider"
  title: "VP Operations, MegaCorp AG"
  icon-name: user-avatar
```

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Card container | `.quote-card` | `background`, `border-radius` |
| Quote mark | `.quote-card__mark` | `color`, `font-size` |
| Quote text | `.quote-card__text` → `u-text-on-surface u-type-body` | `color`, `font-size` |
| Attribution text | `.quote-card__attribution` → `u-text-on-surface-variant u-type-caption` | `color`, `font-size` |
