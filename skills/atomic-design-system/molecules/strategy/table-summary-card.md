# table-summary-card

**Molecule slug:** `table-summary-card`
**Domain:** strategy
**Category:** Summary / KPI

A companion card that presents the most important insights from a data table:
a **KPI strip** of key metrics and a set of **annotated remarks** (assumptions,
notes, warnings, etc.). Can be placed to the **left** of a table (stacked layout)
or **below** it (stacked or side-by-side), with optional **table-companion styling**
that visually attaches the card to the table above via a coloured accent stripe
and a slightly highlighted background.

## Design anatomy

### `layout: stacked` (default)

```
┌──────────────────────────────────────────────────────────────┐
│  ████████ accent stripe  (table-mode only)                   │
│  [Optional title]                                            │
│  63 K          12.4 M €       −3 d        ← KPI strip       │
│  Revenue       ARR Impact     Time saved                     │
│  ──────────────────────────────────────────────────────────  │
│  [Assumption]  FX rate fixed at 1.12 EUR/USD for all calcs   │
│  [Remark]      Q4 actuals not yet available; Q3 used         │
│  [Note]        Headcount includes contractors                 │
└──────────────────────────────────────────────────────────────┘
```

### `layout: side-by-side`

```
┌──────────────────────────────────────────────────────────────┐
│  ████ accent stripe  (table-mode: true)                      │
│  63 K     │  [Assumption]  FX rate fixed at 1.12 EUR/USD     │
│  Revenue  │  [Remark]      Q4 actuals not yet available      │
│  12.4 M € │  [Note]        Headcount includes contractors    │
│  ARR      │                                                  │
└──────────────────────────────────────────────────────────────┘
```

## Parameters

### Card-level

| Parameter            | Type   | Default             | Description |
|----------------------|--------|---------------------|-------------|
| `title`              | string | —                   | Optional card header title |
| `kpis`               | list   | —                   | KPI metric objects (see below) |
| `info`               | list   | —                   | Annotation / remark objects (see below) |
| `layout`             | enum   | `stacked`           | `stacked` · `side-by-side` |
| `kpi-col-frac`       | float  | `0.40`              | Fraction of width used by KPI column in `side-by-side` mode |
| `table-mode`         | bool   | `false`             | Enable table-companion styling: accent stripe + highlighted bg |
| `accent-color`       | color  | `primary`           | Top stripe color and section divider accent in table-mode |
| `accent-stripe-h`    | int    | `4`                 | Height of the top accent stripe in px (0 to disable) |
| `kpi-value-color`    | color  | `text-highlight`    | Global KPI value text color |
| `kpi-value-size`     | int    | auto                | Explicit font-size in px for all KPI values |
| `kpi-label-color`    | color  | `on-surface-variant`| Metric label and sub-label text color |
| `kpi-fill`           | color  | `bg-card`           | Background fill for each KPI chip area |
| `kpi-border`         | bool   | `false`             | Draw a border around individual KPI chips |
| `kpi-divider`        | bool   | `false`             | Draw vertical dividers between KPI chips |
| `info-text-color`    | color  | `on-surface-variant`| Body text color for annotation rows |
| `info-label-color`   | color  | `surface`           | Text color inside annotation type badges |
| `info-text-size`     | int    | body font           | Explicit font-size in px for annotation body text |
| `border-color`       | color  | `border-subtle`     | Divider and chip border color |
| `show-header`        | bool   | auto                | Show/hide card title header |
| `show-header-line`   | bool   | `true` (`false` in `table-mode` unless explicitly overridden) | Line below card title header |
| `bg-color`           | color  | `bg-card` / `primary-container` in table-mode | Card background |

### KPI object fields

| Field        | Type   | Required | Description |
|--------------|--------|----------|-------------|
| `label`      | string | no       | Small metric name shown above the value |
| `value`      | string | yes      | Main metric display value (e.g. `"87"`, `"12.4 M"`) |
| `value-unit` | string | no       | Unit suffix appended to value (e.g. `"%"`, `"M €"`) |
| `trend`      | enum   | no       | `up` · `down` · `neutral` — adds arrow prefix |
| `sublabel`   | string | no       | Tiny secondary line below the value (e.g. `"YTD"`) |
| `color`      | color  | no       | Per-KPI value color override |

### Info object fields

| Field    | Type   | Required | Description |
|----------|--------|----------|-------------|
| `type`   | enum   | no       | `assumption` · `remark` · `note` · `warning` · `info` — controls badge color and default label |
| `label`  | string | no       | Custom badge text (overrides `type` default) |
| `text`   | string | yes      | Annotation body text |
| `color`  | color  | no       | Badge fill color override |

### Badge colors by type

| Type         | Default badge fill         | Notes |
|--------------|----------------------------|-------|
| `assumption` | `on-surface-variant`       | Grey — factual basis |
| `remark`     | `primary`                  | Brand color — key observations |
| `note`       | `secondary`                | Secondary — informational |
| `warning`    | `warning`                  | Amber — caveats / risks |
| `info`       | `secondary`                | Alias for `note` |

## Examples

### Standalone summary (left of table)

```yaml
molecule: table-summary-card
title: Cost Estimation Summary
kpis:
  - label: Total Cost
    value: "€ 86,400"
    trend: up
  - label: Avg. Day Rate
    value: "€ 800"
  - label: Duration
    value: "9 wks"
info:
  - type: assumption
    text: All rates based on 2025 rate card; travel costs excluded
  - type: remark
    text: Phase 2 scope not yet fully estimated — add 15–20 % contingency
  - type: note
    text: Sign-off required from GBL IT before procurement can proceed
```

### Table-companion (placed below a table)

```yaml
molecule: table-summary-card
table-mode: true
accent-color: primary
layout: stacked
kpis:
  - label: Total project budget
    value: "€ 1.2 M"
    trend: neutral
    sublabel: "incl. contingency"
  - label: FTE effort
    value: "38"
    value-unit: "person-months"
  - label: Go-live
    value: "Q3 2026"
info:
  - type: assumption
    text: Headcount based on current org structure; no backfill assumed
  - type: warning
    text: Regulatory approval timeline may extend Phase 3 by up to 6 weeks
```

### KPI-only, with dividers, side-by-side layout

```yaml
molecule: table-summary-card
layout: side-by-side
kpi-col-frac: 0.35
kpi-divider: true
kpis:
  - label: Revenue impact
    value: "+12.4 M €"
    color: success
  - label: Cost reduction
    value: "−8 %"
    color: primary
  - label: Payback
    value: "14 mo"
info:
  - type: remark
    text: Revenue uplift is net of implementation costs and excludes upsell scenarios
  - type: assumption
    text: Churn rate remains stable at 4.2 % annually
  - type: note
    text: Full sensitivity analysis available in the appendix
```

## CSS design tokens

| Token                          | Description                              |
|--------------------------------|------------------------------------------|
| `--color-primary`              | Default accent stripe + remark badge     |
| `--color-text-highlight`       | Default KPI value color                  |
| `--color-on-surface-variant`   | KPI labels and annotation body text      |
| `--color-primary-container`    | Card bg in table-mode                    |
| `--color-border-subtle`        | Dividers and optional chip borders       |
| `--color-warning`              | Warning badge fill                       |
