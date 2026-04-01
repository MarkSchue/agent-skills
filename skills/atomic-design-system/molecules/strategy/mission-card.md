# Molecule: mission-card

```yaml
id: mission-card
type: molecule
domain: strategy
layout: hero-full
description: Card presenting a mission or vision statement with a decorative icon and title.
tags: [strategy, mission, vision, statement]
preview: previews/molecules/mission-card.png
required_atoms: [icon-wrapper, text-heading, text-body, shape-divider]
min_atoms: 2
max_atoms: 4
```

## Layout

```
┌─────────────────────────────────────────────────────┐
│  [icon-wrapper]  [text-heading: Title]               │
│  ─────────────────────────────── [shape-divider]    │
│  [text-body: Mission statement text]                 │
└─────────────────────────────────────────────────────┘
```

- Alignment: Vertical-Stack
- Padding: `{{theme.spacing.l}}`
- Icon left-aligned with title on same row

## Atoms and Roles

| Atom | Role | Required |
|---|---|---|
| `icon-wrapper` | Visual | no |
| `text-heading` | Title | yes |
| `shape-divider` | Divider | no |
| `text-body` | Statement | yes |

## Visual Properties

| Property | Token |
|---|---|
| Card background | `{{theme.color.surface}}` |
| Card border | `{{theme.shape.border-subtle}}` |
| Card corner radius | `{{theme.borders.radius-medium}}` |
| Card padding | `{{theme.spacing.l}}` |
| Icon fill | `{{theme.color.primary}}` |

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `icon` | string | Value from props. |
| `icon-name` | string | Value from props. |
| `mission` | string | Text string. |
| `statement` | string | Text string. |
| `title` | string | Text string. |
## Example

```yaml
molecule: mission-card
params:
  title: "Our Mission"
  statement: "We accelerate the world's transition to sustainable industrial processes through intelligent automation."
  icon-name: target
```

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Card container | `.mission-card` | `background`, `border-color`, `border-radius` |
| Icon badge | `.mission-card__icon-badge` | `background`, `color`, `border-radius` |
| Title text | `.mission-card__title` → `u-text-on-surface u-type-label` | `color`, `font-size` |
| Body text | `.mission-card__body` → `u-text-on-surface u-type-body` | `color`, `font-size` |
| Tag element | `.mission-card__tag` → `u-text-on-surface-variant u-type-caption` | `color`, `font-size` |
