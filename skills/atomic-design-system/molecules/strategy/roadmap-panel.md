# Molecule: roadmap-panel

```yaml
id: roadmap-panel
type: molecule
domain: strategy
layout: flow-list
description: Product or strategic roadmap panel organized in swim-lanes (Now / Next / Later or quartely).
tags: [strategy, roadmap, planning, swimlane, product]
preview: previews/molecules/roadmap-panel.png
required_atoms: [text-heading, text-body, badge-status, shape-divider]
min_atoms: 3
max_atoms: 12
```

## Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  [text-heading: Roadmap Title]                                   │
│  ─────────────────────────────────── [shape-divider]             │
│  NOW                  NEXT                   LATER               │
│  ─────────────────  ─────────────────  ─────────────────         │
│  [text-body: Item]  [text-body: Item]  [text-body: Item]         │
│  [badge]            [badge]            [badge]                   │
│  [text-body: Item]  [text-body: Item]                            │
└──────────────────────────────────────────────────────────────────┘
```

- Swim-lane headers are rendered with `{{theme.color.primary}}` underline.
- Items within each lane are vertically stacked.

## Atoms and Roles

| Atom | Role | Required |
|---|---|---|
| `text-heading` | Panel title + Lane headers | yes |
| `text-body` | Item label + description | yes (1-4 per lane) |
| `badge-status` | Item status or tag | no |
| `shape-divider` | Lane separator | no |

## Visual Properties

| Property | Token |
|---|---|
| Lane header color | `{{theme.color.primary}}` |
| Lane header underline | `{{theme.shape.accent-line}}` |
| Item card background | `{{theme.color.surface}}` |
| Item card border | `{{theme.shape.border-subtle}}` |
| Background | `{{theme.color.surface}}` |
| Padding | `{{theme.spacing.l}}` |

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `desc-color` | color-token | Color token name (theme color). |
| `dot-color` | color-token | Color token name (theme color). |
| `item-color` | color-token | Color token name (theme color). |
| `label-color` | color-token | Color token name (theme color). |
| `lane-gap` | int(px)/size token | Size/spacing value (px or token). |
| `items` | list | List of lane objects. **Canonical.** Alias: `lanes`. Each lane has `label` (header) and `items[]` (inner items). |
| `line-color` | color-token | Color token name (theme color). |
| `text-align` | enum | Alignment enum (left/center/right or top/middle/bottom). |
| `title` | string | Text string. |
## Example

```yaml
molecule: roadmap-panel
params:
  title: "Product Roadmap 2025"
  items:                            # canonical (alias: lanes)
    - label: "Now"
      items:
        - headline: "Mobile App v2.0"  # item text — alias: text
          body: "iOS + Android release"  # alias: description
          status: primary
    - label: "Next"
      items:
        - headline: "API v3"
          body: "GraphQL support"
          status: neutral
        - headline: "SSO Integration"
          body: "SAML 2.0"
          status: neutral
    - label: "Later"
      items:
        - headline: "AI Insights"
          body: "Predictive analytics"
          status: neutral
```

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Panel container | `.roadmap-panel` | `border-radius` |
| Phase container | `.roadmap-panel__phase` → `u-border-subtle` | `border-color` |
| Phase title text | `.roadmap-panel__phase-title` → `u-text-on-surface u-type-label u-bold` | `color`, `font-size`, `font-weight` |
| Milestone text | `.roadmap-panel__milestone` → `u-text-on-surface-variant u-type-caption` | `color`, `font-size` |
| Dot element | `.roadmap-panel__dot` → `u-bg-primary` | `background` |
