# Molecule: comparison-card

```yaml
id: comparison-card
type: molecule
domain: data
layout: split-left-right
description: Side-by-side comparison of two options, scenarios, or time periods with labeled attributes.
tags: [data, comparison, before-after, option, versus]
preview: previews/molecules/comparison-card.png
required_atoms: [text-heading, text-body, badge-status, shape-divider, icon-wrapper]
min_atoms: 2
max_atoms: 6
```

## Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  [text-heading: Comparison Title]                                │
│  ────────────── [shape-divider] ──────────────                   │
│                                                                  │
│  ┌──────────────────────┐  │  ┌──────────────────────┐          │
│  │ [text-heading: A]    │  │  │ [text-heading: B]     │          │
│  │ [text-body: attrs]   │  │  │ [text-body: attrs]    │          │
│  │ [badge-status]       │  │  │ [badge-status]        │          │
│  └──────────────────────┘  │  └──────────────────────┘          │
└──────────────────────────────────────────────────────────────────┘
```

- Two equally-sized columns separated by a `{{theme.shape.divider}}` vertical rule.
- Optional row-by-row attribute comparison (feature matrix style).

## Atoms and Roles

| Atom | Role | Required |
|---|---|---|
| `text-heading` | Card title + Column headers | yes |
| `text-body` | Attribute list per column | yes |
| `badge-status` | Highlight / recommendation badge | no |
| `shape-divider` | Vertical divider | no |
| `icon-wrapper` | Check/cross icons per attribute | no |

## Visual Properties

| Property | Token |
|---|---|
| Background | `{{theme.color.surface}}` |
| Left column highlight | `{{theme.color.surface}}` |
| Right column highlight | `{{theme.color.primary}}` at 10% opacity |
| Divider | `{{theme.shape.divider}}` |
| Recommended badge | `{{theme.color.success}}` |

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `attributes` | string | Value from props. |
| `highlight` | string | Value from props. |
| `left` | string | Value from props. |
| `left-label` | string | Label text content. |
| `right` | string | Value from props. |
| `right-label` | string | Label text content. |
## Example

```yaml
molecule: comparison-card
params:
  title: "Deployment Options"
  left:
    label: "On-Premise"
    attributes:
      - "Full data control"
      - "Higher setup cost"
      - "12-week deployment"
  right:
    label: "Cloud SaaS"
    attributes:
      - "Instant deployment"
      - "Subscription pricing"
      - "Automatic updates"
    badge: "Recommended"
  recommended: right
```

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Card container | `.comparison-card` | `background`, `border-color`, `border-radius` |
| Header area | `.comparison-card__header` | `background`, `color`, `font-size` |
| Row label text | `.comparison-card__row-label` → `u-text-on-surface u-type-label` | `color`, `font-size` |
| Row value text | `.comparison-card__row-value` → `u-text-on-surface u-type-body` | `color`, `font-size` |
| Footer area | `.comparison-card__footer` → `u-text-on-surface-variant u-type-caption` | `color`, `font-size` |
