# Molecule: profile-card

```yaml
id: profile-card
type: molecule
domain: team
layout: profile-stack
description: Individual person card with avatar/icon, name, title, and optional contact details.
tags: [team, person, profile, bio, contact]
preview: previews/molecules/profile-card.png
required_atoms: [icon-wrapper, text-heading, text-body, badge-status]
min_atoms: 2
max_atoms: 4
```

## Layout

```
┌──────────────────────────────────────────┐
│         [icon-wrapper: avatar]           │
│      [text-heading: Full Name]           │
│      [text-body: Job Title]              │
│      [badge-status: Department]          │
│      [text-body: email / linkedin]       │
└──────────────────────────────────────────┘
```

- Center-aligned layout (default) or left-aligned.
- Avatar is a circle-cropped icon placeholder or user-supplied graphic ID.

## Atoms and Roles

| Atom | Role | Required |
|---|---|---|
| `icon-wrapper` | Avatar | no |
| `text-heading` | Name | yes |
| `text-body` | Job title | yes |
| `badge-status` | Department tag | no |
| `text-body` | Contact info | no |

## Visual Properties

| Property | Token |
|---|---|
| Card background | `{{theme.color.surface}}` |
| Card border | `{{theme.shape.border-subtle}}` |
| Card radius | `{{theme.borders.radius-medium}}` |
| Avatar bg | `{{theme.color.primary}}` at 10% opacity |
| Avatar stroke | `{{theme.shape.border-subtle}}` |
| Name color | `{{theme.color.on-surface}}` |
| Title color | `{{theme.color.neutral}}` |

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `bio` | string | Value from props. |
| `department` | string | Value from props. |
| `email` | string | Value from props. |
| `name` | string | Text string. |
| `title` | string | Text string. |
## Example

```yaml
molecule: profile-card
params:
  name: "Dr. Anna Müller"
  title: "Chief Technology Officer"
  department: "Engineering"
  contact: "a.mueller@company.com"
  icon-name: user
  align: center
```

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Card container | `.profile-card` | `background`, `border-color`, `border-radius` |
| Avatar element | `.profile-card__avatar` | `background`, `border-radius` |
| Name text | `.profile-card__name` → `u-text-on-surface-variant u-type-label` | `color`, `font-size` |
| Role text | `.profile-card__role` → `u-text-on-surface-variant u-type-caption` | `color`, `font-size` |
| Detail text | `.profile-card__detail` → `u-text-on-surface-variant u-type-annotation` | `color`, `font-size` |
| Badge element | `.profile-card__badge` → `u-bg-primary u-text-on-primary` | `background`, `color` |
