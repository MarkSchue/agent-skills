# Molecule: timeline-panel

```yaml
id: timeline-panel
type: molecule
domain: strategy
layout: flow-list
description: Horizontal or vertical timeline showing ordered events or milestones with dates and labels.
tags: [strategy, timeline, history, milestones, roadmap]
preview: previews/molecules/timeline-panel.png
required_atoms: [text-heading, text-body, badge-status, shape-divider]
min_atoms: 2
max_atoms: 8
```

## Layout

```
┌───────────────────────────────────────────────────────────────────┐
│  [text-heading: Panel Title]                                       │
│                                                                    │
│  ●──────────────●──────────────●──────────────●                   │
│  [date]        [date]         [date]          [date]               │
│  [text-body]   [text-body]    [text-body]     [text-body]          │
│  [badge]       [badge]        [badge]                              │
└───────────────────────────────────────────────────────────────────┘
```

- Orientation: Horizontal (default) or Vertical
- Node count: 2–8 items
- Connector line uses `{{theme.shape.thin-line}}`
- Milestone nodes use `{{theme.color.primary}}` fill

## Atoms and Roles

| Atom | Role | Required |
|---|---|---|
| `text-heading` | Title | no |
| `text-body` | Event label + description | yes (per node) |
| `badge-status` | Status indicator | no (per node) |
| `shape-divider` | Connector between nodes | yes |

## Visual Properties

| Property | Token |
|---|---|
| Connector line | `{{theme.shape.thin-line}}` |
| Node fill (done) | `{{theme.color.primary}}` |
| Node fill (future) | `{{theme.color.neutral}}` |
| Node fill (current) | `{{theme.color.accent}}` |
| Background | `{{theme.color.surface}}` |
| Padding | `{{theme.spacing.l}}` |

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `title` | string | Optional panel heading |
| `orientation` | enum | `horizontal` · `vertical` |
| `events` | `list[object]` | Array of `{date, label, description, status}` |

## Example

```yaml
molecule: timeline-panel
params:
  title: "Company Milestones"
  orientation: horizontal
  events:
    - date: "2018"
      label: "Founded"
      description: "Company incorporated in Munich"
      status: success
    - date: "2020"
      label: "Series A"
      description: "$12M raised"
      status: success
    - date: "2023"
      label: "IPO"
      description: "Listed on XETRA"
      status: primary
    - date: "2025"
      label: "Global Expansion"
      description: "Target: 20 countries"
      status: neutral
```

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Panel container | `.timeline-panel` | `border-radius` |
| Axis line | `.timeline-panel__axis` → `u-border-subtle` | `border-color` |
| Event title text | `.timeline-panel__event-title` → `u-text-on-surface u-type-label u-bold` | `color`, `font-size`, `font-weight` |
| Event body text | `.timeline-panel__event-body` → `u-text-on-surface-variant u-type-caption` | `color`, `font-size` |
| Dot element | `.timeline-panel__dot` → `u-bg-primary` | `background` |
