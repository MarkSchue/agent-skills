# Molecule: location-card

```yaml
id: location-card
type: molecule
domain: team
layout: flow-list
description: Office or site card showing location name, address, team headcount, and key contact.
tags: [team, location, office, site, geography]
preview: previews/molecules/location-card.png
required_atoms: [icon-wrapper, text-heading, text-body, badge-status]
min_atoms: 2
max_atoms: 5
```

## Layout

```
┌──────────────────────────────────────────────────────┐
│  [icon-wrapper: location / flag icon]                │
│  [text-heading: City / Site Name]                    │
│  [text-body: Full address]                           │
│  ─────────────────── [shape-divider]                 │
│  [badge-status: Headcount]  [badge-status: Timezone] │
│  [text-body: Key contact name]                       │
└──────────────────────────────────────────────────────┘
```

- Location icon can be a map-pin, flag, or building icon.
- Badges provide at-a-glance metadata about the site.

## Atoms and Roles

| Atom | Role | Required |
|---|---|---|
| `icon-wrapper` | Location icon | no |
| `text-heading` | Site name | yes |
| `text-body` | Address | no |
| `badge-status` | Headcount badge | no |
| `badge-status` | Timezone badge | no |
| `text-body` | Key contact | no |
| `shape-divider` | Section separator | no |

## Visual Properties

| Property | Token |
|---|---|
| Card background | `{{theme.color.surface}}` |
| Card border | `{{theme.shape.border-subtle}}` |
| Card radius | `{{theme.borders.radius-medium}}` |
| Location icon fill | `{{theme.color.accent}}` |
| Badge variant | `neutral` |

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `site` | string | City or site name |
| `address` | string | Full postal address |
| `headcount` | integer | Number of employees at site |
| `timezone` | string | e.g. "CET", "EST", "JST" |
| `contact` | string | Key contact name + title |
| `icon-name` | string | Icon (e.g. `location`, `building`, `flag`) |

## Example

```yaml
molecule: location-card
params:
  site: "Munich HQ"
  address: "Leopoldstraße 12, 80802 München, DE"
  headcount: 340
  timezone: "CET"
  contact: "Petra Hausmann – Office Manager"
  icon-name: building
```

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Card container | `.location-card` | `background`, `border-color`, `border-radius` |
| Name text | `.location-card__name` → `u-text-on-surface-variant u-type-label` | `color`, `font-size` |
| Detail text | `.location-card__detail` → `u-text-on-surface-variant u-type-annotation` | `color`, `font-size` |
| Icon element | `.location-card__icon` → `u-text-primary` | `color` |
