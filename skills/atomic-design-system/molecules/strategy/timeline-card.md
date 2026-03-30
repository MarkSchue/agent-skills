# Molecule: timeline-card

```yaml
id: timeline-card
type: molecule
domain: strategy
layout: card
description: Card-framed horizontal or vertical milestone timeline with status dots, date labels, event labels, descriptions, and full per-instance overrides.
tags: [strategy, timeline, milestones, roadmap, phases, card]
preview: previews/molecules/timeline-card.png
required_atoms: [text-heading, text-body, badge-status, shape-divider]
min_atoms: 2
max_atoms: 8
```

## Layout — Horizontal (default)

```
┌──────────────────────────────────────────────────────────────────────┐
│  [title]                                                              │
│  ─────────────────────────────────────────────────────────────────   │
│                                                                       │
│  Wk 1–4     Wk 5–14     Wk 15–22    Wk 23–34    TBD                 │
│    ●────────────●────────────●────────────●────────────●             │
│  Phase 0    Phase 1     Phase 2     Phase 3     Phase 4              │
│  Mobilize   Baseline    Arch.       Planning    Execution             │
└──────────────────────────────────────────────────────────────────────┘
```

## Layout — Vertical

```
┌──────────────────────────────────────────────────────────────────────┐
│  [title]                                                              │
│  ────────────────────────────────────────────────────────────────    │
│                                                                       │
│  Q1 2025 ●  Kick-off                                                 │
│            Team assembled, scope confirmed                            │
│  Q2 2025 ●  Alpha Launch                                             │
│            Core features live in staging                              │
│  Q3 2025 ●  Beta                                                     │
│            Public beta, feedback loop                                 │
└──────────────────────────────────────────────────────────────────────┘
```

## Parameters

| Parameter             | Type    | Required | Description                                           |
|-----------------------|---------|----------|-------------------------------------------------------|
| `title`               | string  | no       | Optional card header title                           |
| `orientation`         | enum    | no       | `horizontal` (default) · `vertical`                  |
| `events`              | list    | yes      | Array of event objects (see below)                   |
| `axis-position`       | float   | no       | Horizontal only — axis position as 0..1 fraction of content height (default: 0.40) |
| `dot-radius`          | int     | no       | Dot/badge radius in px (default: auto-scaled; auto-enlarged when badge type is set) |
| `dot-badge-type`      | enum    | no       | `none` (plain dot, default) · `number` (auto 01,02…) · `text` (reads `badge` per event) · `icon` (reads `badge` as icon name) |
| `dot-badge-color`     | color   | no       | Badge circle fill color (default: `primary`)         |
| `dot-badge-text-color`| color   | no       | Text/icon color inside badge (default: `on-primary`) |
| `result`              | object  | no       | Optional target/result node at the end of the axis — `{label, description, color}`. Also accepts a plain string as shorthand for `label`. |
| `line-color`          | color   | no       | Axis line color (default: `border-subtle`)           |
| `date-color`          | color   | no       | Date label color (default: `primary`)                |
| `label-color`         | color   | no       | Event label color (default: `on-surface`)            |
| `desc-color`          | color   | no       | Description color (default: `on-surface-variant`)    |
| `show-header`         | bool    | no       | Show/hide card header section (default: true if title set) |
| `show-header-line`    | bool    | no       | Show/hide divider below header (default: true)       |
| `bg-color`            | color   | no       | Card background override                             |

### Event object fields

| Field         | Type   | Required | Description                                                     |
|---------------|--------|----------|-----------------------------------------------------------------|
| `date`        | string | yes      | Date / period label (e.g. `"Q1 2025"`)                         |
| `label`       | string | yes      | Short event name                                               |
| `description` | string | no       | Supporting detail text                                         |
| `status`      | enum   | no       | `success` · `warning` · `error` · `neutral` · `primary` (default: neutral) — controls plain-dot color |
| `badge`       | string | no       | Custom text/icon override for the badge circle; takes precedence over auto-number |

### Result object fields

| Field         | Type   | Description                                              |
|---------------|--------|----------------------------------------------------------|
| `label`       | string | Bold text shown at the end of the axis                  |
| `description` | string | Optional smaller text below the label                   |
| `color`       | color  | Text color override (default: `on-surface`)             |

## CSS Token Map

| Token                      | Role                     | Fallback        |
|----------------------------|--------------------------|-----------------|
| `--color-timeline-line`    | Axis line color          | `border-subtle` |
| `--color-timeline-date`    | Date label color         | `primary`       |
| `--color-timeline-label`   | Event label color        | `on-surface`    |
| `--color-timeline-desc`    | Description color        | `on-surface-variant` |

## Example — Horizontal with numbered badges and result node

```yaml
molecule: timeline-card
title: Five-Phase Roadmap
orientation: horizontal
dot-badge-type: number          # auto-numbers dots 01, 02, …
dot-badge-color: primary
dot-badge-text-color: on-primary
axis-position: 0.38
result:
  label: "Target State"
  description: "Go-live Q4"
  color: on-surface
events:
  - date: "Wk 1–4"
    label: "Phase 0"
    description: "Mobilize — scope, governance, access"
    status: success
  - date: "Wk 5–14"
    label: "Phase 1"
    description: "Current state baseline"
    status: neutral
  - date: "Wk 15–22"
    label: "Phase 2"
    description: "Target architecture & decision"
    status: neutral
  - date: "Wk 23–34"
    label: "Phase 3"
    description: "Detailed transition planning"
    status: neutral
  - date: "TBD"
    label: "Phase 4"
    description: "Execution waves"
    status: neutral
```

## Example — Horizontal (plain, no badges)

```yaml
molecule: timeline-card
title: Five-Phase Roadmap
orientation: horizontal
events:
  - date: "Wk 1–4"
    label: "Phase 0"
    description: "Mobilize — scope, governance, access"
    status: success
  - date: "Wk 5–14"
    label: "Phase 1"
    description: "Current state baseline"
    status: neutral
  - date: "Wk 15–22"
    label: "Phase 2"
    description: "Target architecture & decision"
    status: neutral
```

## Example — Vertical (history)

```yaml
molecule: timeline-card
title: Company Milestones
orientation: vertical
events:
  - date: "2018"
    label: "Founded"
    description: "Incorporated in Munich"
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
