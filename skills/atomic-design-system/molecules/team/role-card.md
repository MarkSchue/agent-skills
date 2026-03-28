# Molecule: role-card

```yaml
id: role-card
type: molecule
domain: team
layout: stacked-header-body
description: Card defining an organizational role with responsibilities, required skills, and reporting line.
tags: [team, role, responsibilities, org-design, hr]
preview: previews/molecules/role-card.png
required_atoms: [text-heading, text-body, badge-status, shape-divider, icon-wrapper]
min_atoms: 2
max_atoms: 5
```

## Layout

```
┌──────────────────────────────────────────────────────┐
│  [icon-wrapper]  [text-heading: Role Title]          │
│                  [badge-status: Level / Band]        │
│  ─────────────────────── [shape-divider]             │
│  Responsibilities:                                   │
│  [text-body: bullet list]                            │
│  ─────────────────────── [shape-divider]             │
│  Reports to: [text-body]                             │
└──────────────────────────────────────────────────────┘
```

- Role title is prominent; level badge is secondary.
- Responsibilities formatted as bullets via `text-body`.

## Atoms and Roles

| Atom | Role | Required |
|---|---|---|
| `text-heading` | Role title | yes |
| `badge-status` | Level / band | no |
| `text-body` | Responsibilities list | yes |
| `text-body` | Reports-to line | no |
| `icon-wrapper` | Role / department icon | no |
| `shape-divider` | Section separator | no |

## Visual Properties

| Property | Token |
|---|---|
| Card background | `{{theme.color.surface}}` |
| Card border | `{{theme.shape.border-subtle}}` |
| Card radius | `{{theme.borders.radius-medium}}` |
| Role icon fill | `{{theme.color.primary}}` |

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `title` | string | Role / position title |
| `level` | string | Grade or band (e.g. "L5", "Senior") |
| `responsibilities` | `list[string]` | Key responsibilities (3-6 bullets) |
| `reports-to` | string | Manager role title |
| `icon-name` | string | Functional area icon |

## Example

```yaml
molecule: role-card
params:
  title: "Senior Product Manager"
  level: "L5"
  responsibilities:
    - "Own product vision and roadmap for the core platform"
    - "Coordinate cross-functional delivery squads"
    - "Define and track success metrics"
  reports-to: "VP Product"
  icon-name: product
```

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Card container | `.role-card` | `background`, `border-color`, `border-radius` |
| Title text | `.role-card__title` → `u-text-on-surface u-type-label` | `color`, `font-size` |
| Detail text | `.role-card__detail` → `u-text-on-surface-variant u-type-annotation` | `color`, `font-size` |
| Badge element | `.role-card__badge` → `u-bg-primary u-text-on-primary` | `background`, `color` |
