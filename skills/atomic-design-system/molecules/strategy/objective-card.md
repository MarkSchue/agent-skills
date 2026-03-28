# Molecule: objective-card

```yaml
id: objective-card
type: molecule
domain: strategy
layout: stacked-header-body
description: OKR-style card showing a strategic objective with key results and progress indicators.
tags: [strategy, okr, objective, goals, progress]
preview: previews/molecules/objective-card.png
required_atoms: [text-heading, text-body, badge-status, shape-divider]
min_atoms: 2
max_atoms: 5
```

## Layout

```
┌────────────────────────────────────────────┐
│  [badge-status: Quarter]                   │
│  [text-heading: Objective title]           │
│  ─────────────────── [shape-divider]       │
│  Key Results:                              │
│  ○ [text-body: KR1]  [badge-status: 80%]  │
│  ○ [text-body: KR2]  [badge-status: 45%]  │
│  ○ [text-body: KR3]  [badge-status: 100%] │
└────────────────────────────────────────────┘
```

- Vertical stack with key results as repeating rows
- Progress badge variant derived from value (≥80% = success, 40-79% = warning, <40% = error)

## Atoms and Roles

| Atom | Role | Required |
|---|---|---|
| `text-heading` | Objective | yes |
| `text-body` | Key result text | yes (1-5 KRs) |
| `badge-status` | Quarter label | no |
| `badge-status` | Progress indicator | no (per KR) |
| `shape-divider` | Section separator | no |

## Visual Properties

| Property | Token |
|---|---|
| Card background | `{{theme.color.surface}}` |
| Card border | `{{theme.shape.border-subtle}}` |
| Card radius | `{{theme.borders.radius-medium}}` |
| KR bullet color | `{{theme.color.primary}}` |

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `objective` | string | The strategic objective statement |
| `quarter` | string | Label e.g. "Q3 2025" |
| `key-results` | `list[object]` | Array of `{text, progress}` (progress 0-100) |

## Example

```yaml
molecule: objective-card
params:
  objective: "Achieve market leadership in DACH region"
  quarter: "Q3 2025"
  key-results:
    - text: "Grow MRR to €5M"
      progress: 82
    - text: "Close 10 enterprise deals"
      progress: 60
    - text: "NPS above 50"
      progress: 100
```

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Card container | `.objective-card` | `background`, `border-color`, `border-radius` |
| Badge element | `.objective-card__badge` → `u-bg-primary u-text-on-primary` | `background`, `color` |
| Title text | `.objective-card__title` → `u-text-on-surface u-type-label` | `color`, `font-size` |
| Body text | `.objective-card__body` → `u-text-on-surface u-type-body` | `color`, `font-size` |
| Progress bar track | `.objective-card__progress-bar` → `u-bg-surface-variant` | `background` |
| Progress bar fill | `.objective-card__progress-fill` → `u-bg-success` | `background` |
