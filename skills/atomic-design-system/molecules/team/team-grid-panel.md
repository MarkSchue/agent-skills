# Molecule: team-grid-panel

```yaml
id: team-grid-panel
type: molecule
domain: team
layout: profile-stack
description: Grid panel composing multiple profile-cards in a responsive 2- or 3-column layout.
tags: [team, grid, people, org, lineup]
preview: previews/molecules/team-grid-panel.png
required_atoms: [text-heading, text-body, icon-wrapper, badge-status]
min_atoms: 2
max_atoms: 9
```

## Layout

```
┌────────────────────────────────────────────────────────────────┐
│  [text-heading: Team Title]                                    │
│  ────────────── [shape-divider]                                │
│                                                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                     │
│  │ profile  │  │ profile  │  │ profile  │                     │
│  │ card     │  │ card     │  │ card     │                     │
│  └──────────┘  └──────────┘  └──────────┘                     │
│  ┌──────────┐  ┌──────────┐                                    │
│  │ profile  │  │ profile  │                                    │
│  └──────────┘  └──────────┘                                    │
└────────────────────────────────────────────────────────────────┘
```

- Column count: 2 (≤4 people), 3 (5-9 people).
- Each cell is a mini `profile-card` with name, title, and optional icon.

## Atoms and Roles

| Atom | Role | Required |
|---|---|---|
| `text-heading` | Panel title | no |
| `icon-wrapper` | Per-person avatar | no |
| `text-body` | Per-person name + title | yes |
| `badge-status` | Per-person department | no |

## Visual Properties

| Property | Token |
|---|---|
| Panel background | `{{theme.color.surface}}` |
| Cell border | `{{theme.shape.border-subtle}}` |
| Gutter between cells | `{{theme.spacing.m}}` |
| Panel padding | `{{theme.spacing.l}}` |

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `title` | string | Panel heading |
| `members` | `list[object]` | Array of `{name, title, department, icon-name}` |
| `columns` | integer | Override column count (2 or 3) |

## Example

```yaml
molecule: team-grid-panel
params:
  title: "Leadership Team"
  members:
    - name: "Anna Müller"; title: "CTO"; department: "Engineering"
    - name: "Jonas Weber"; title: "CFO"; department: "Finance"
    - name: "Lena Braun"; title: "CMO"; department: "Marketing"
    - name: "Felix Koch";  title: "COO"; department: "Operations"
```

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Panel container | `.team-grid-panel` | `border-radius` |
| Member cell | `.team-grid-panel__member` → `u-bg-surface u-border-subtle` | `background`, `border-color` |
| Avatar element | `.team-grid-panel__avatar` → `u-bg-primary` | `background` |
| Name text | `.team-grid-panel__name` → `u-text-on-surface-variant u-type-label` | `color`, `font-size` |
| Role text | `.team-grid-panel__role` → `u-text-on-surface-variant u-type-caption` | `color`, `font-size` |
| Detail text | `.team-grid-panel__detail` → `u-text-on-surface-variant u-type-annotation` | `color`, `font-size` |
