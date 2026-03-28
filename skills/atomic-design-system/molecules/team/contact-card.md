# Molecule: contact-card

```yaml
id: contact-card
type: molecule
domain: team
layout: flow-list
description: Business contact card with name, role, contact channels, and company affiliation.
tags: [team, contact, business-card, communication, outreach]
preview: previews/molecules/contact-card.png
required_atoms: [icon-wrapper, text-heading, text-body, badge-status, shape-divider]
min_atoms: 2
max_atoms: 5
```

## Layout

```
┌──────────────────────────────────────────────────────┐
│  [icon-wrapper: contact or org icon]                 │
│  [text-heading: Name]                                │
│  [text-body: Title · Organization]                   │
│  ─────────────────── [shape-divider]                 │
│  📧 [text-body: email]                               │
│  🔗 [text-body: linkedin / url]                      │
│  📞 [text-body: phone] (optional)                    │
└──────────────────────────────────────────────────────┘
```

- Contact channel rows each start with a small icon from `icon-wrapper`.
- Channel icons are resolved from Carbon / Lucide icon set.

## Atoms and Roles

| Atom | Role | Required |
|---|---|---|
| `icon-wrapper` | Person / org avatar | no |
| `text-heading` | Name | yes |
| `text-body` | Title + org | no |
| `shape-divider` | Section divider | no |
| `icon-wrapper` + `text-body` | Contact channel row | yes (min 1) |

## Visual Properties

| Property | Token |
|---|---|
| Card background | `{{theme.color.surface}}` |
| Card border | `{{theme.shape.border-subtle}}` |
| Card radius | `{{theme.borders.radius-medium}}` |
| Channel icon fill | `{{theme.color.primary}}` |
| Name color | `{{theme.color.on-surface}}` |

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `name` | string | Contact's full name |
| `title` | string | Role / job title |
| `organization` | string | Company or team name |
| `email` | string | Email address |
| `url` | string | Website or LinkedIn URL |
| `phone` | string | Phone number (optional) |
| `icon-name` | string | Avatar icon |

## Example

```yaml
molecule: contact-card
params:
  name: "Klaus Berger"
  title: "Account Executive"
  organization: "Acme Solutions GmbH"
  email: "k.berger@acme.de"
  url: "linkedin.com/in/klausberger"
  icon-name: user
```

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Card container | `.contact-card` | `background`, `border-color`, `border-radius` |
| Name text | `.contact-card__name` → `u-text-on-surface-variant u-type-label` | `color`, `font-size` |
| Detail text | `.contact-card__detail` → `u-text-on-surface-variant u-type-annotation` | `color`, `font-size` |
| Divider line | `.contact-card__divider` → `u-border-subtle` | `border-color` |
