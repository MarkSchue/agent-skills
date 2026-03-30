# column-conclusion-card

**Molecule slug:** `column-conclusion-card`
**Domain:** strategy
**Category:** Summary / Insight

A metric-column layout with **2–5 equal columns** and an optional full-width conclusion
section below a decorated divider. Each column can independently show an icon, a large
value with unit, a bold headline, and body text — all centred (or left/right) as a unit.
Use it for key-number summaries, section recaps, or before/after comparisons.

## Design anatomy

```
┌──────────────────────────────────────────────────────────────────┐
│  [Optional title header]                                         │
│                                                                  │
│   [icon]        [icon]        [icon]         ← optional          │
│   87 %          12.4 M        +3             ← large, primary    │
│   Bold          Bold          Bold           ← headline (bold)   │
│   Headline      Headline      Headline                           │
│   Supporting    Supporting    Supporting      ← body (muted)     │
│   body text     body text     body text                          │
│                                                                  │
│  ─────────────────────[∨]─────────────────────  ← divider+chev  │
│       Lorem ipsum dolor sit amet — conclusion text               │
└──────────────────────────────────────────────────────────────────┘
```

## Parameters

| Parameter              | Type   | Default              | Description |
|------------------------|--------|----------------------|-------------|
| `title`                | string | —                    | Optional card header title |
| `columns`              | list   | **required**         | Array of 2–5 column objects (see below) |
| `text-align`           | enum   | `center`             | `center` · `left` · `right` — applies to all column content |
| `value-color`          | color  | `primary`            | Global color for metric values (all columns) |
| `value-size`           | int    | auto                 | Explicit font-size in px for metric values |
| `icon-size`            | int    | auto                 | Explicit icon size in px |
| `icon-color`           | color  | `on-surface-variant` | Global icon color (overridden per column with `color`) |
| `column-gap`           | int    | auto (spacing m)     | Gap between columns in px |
| `conclusion`           | string | —                    | Full-width bold text below the divider |
| `conclusion-color`     | color  | `on-surface`         | Conclusion text color |
| `conclusion-size`      | int    | auto                 | Font-size in px for conclusion |
| `conclusion-bold`      | bool   | `true`               | Bold weight for conclusion text |
| `conclusion-align`     | enum   | `center`             | `center` · `left` · `right` for conclusion only |
| `show-divider`         | bool   | `true`               | Draw the full-width horizontal divider above the conclusion |
| `show-chevron`         | bool   | `true`               | Draw the downward ∨ chevron on the divider (only when `conclusion` is set) |
| `chevron-color`        | color  | `on-surface-variant` | Chevron fill color |
| `divider-color`        | color  | `border-subtle`      | Conclusion divider color |
| `show-header`          | bool   | auto                 | Show/hide the card title header block |
| `show-header-line`     | bool   | `true`               | Line below the title header |
| `bg-color`             | color  | `bg-card`            | Card background color override |

### Column object fields

| Field        | Type   | Required | Description |
|--------------|--------|----------|-------------|
| `headline`   | string | yes      | Bold column heading |
| `body`       | string | no       | Supporting text (smaller, muted) |
| `value`      | string | no       | Large metric number or text (e.g. `"87"`, `"12.4"`) |
| `value-unit` | string | no       | Unit appended after the value (e.g. `"%"`, `"M €"`) |
| `icon`       | string | no       | Icon description / emoji rendered above the value |
| `color`      | color  | no       | Per-column accent — overrides both `value-color` and `icon-color` |

## Example — 3 columns with metrics and conclusion

```yaml
molecule: column-conclusion-card
title: Results at a Glance
text-align: center
value-color: primary
conclusion: Together these improvements deliver a step-change in customer satisfaction and operational efficiency.
show-chevron: true
columns:
  - icon: star
    value: "87"
    value-unit: "%"
    headline: Customer\nSatisfaction
    body: Up from 71 % in Q3, driven by faster resolution times
  - icon: trending_up
    value: "12.4"
    value-unit: M €
    headline: Revenue\nImpact
    body: Incremental ARR attributed to the new service tier
  - icon: schedule
    value: "−3"
    value-unit: days
    headline: Time to\nResolution
    color: success
    body: Median resolution cycle reduced across all priority levels
```

## Example — 2 columns, no icons, left-aligned text

```yaml
molecule: column-conclusion-card
text-align: left
show-chevron: false
conclusion: Addressing the gap in SMB onboarding unlocks the largest near-term growth lever.
conclusion-align: center
columns:
  - value: "62"
    value-unit: "%"
    headline: Current state
    body: Share of new SMB accounts that complete onboarding within 14 days
  - value: "89"
    value-unit: "%"
    headline: Target state
    color: primary
    body: Benchmark from top-quartile SaaS peers
```

## CSS design tokens

| Token                        | Description                        | Default via theme |
|------------------------------|------------------------------------|-------------------|
| `--color-primary`            | Default metric value color         | theme primary     |
| `--color-on-surface`         | Headline and conclusion text       | dark              |
| `--color-on-surface-variant` | Body text and icon default         | medium grey       |
| `--color-border-subtle`      | Conclusion divider line            | light grey        |
