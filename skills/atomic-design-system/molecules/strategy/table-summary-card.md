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

| Parameter | Type | Description |
|---|---|---|
| `accent-color` | color-token | Color token name (theme color). |
| `border-color` | color-token | Color token name (theme color). |
| `info` | string | Value from props. |
| `info-label-color` | color-token | Color token name (theme color). |
| `info-text-color` | color-token | Color token name (theme color). |
| `info-text-size` | int(px)/size token | Size/spacing value (px or token). |
| `kpi-col-frac` | string | Value from props. |
| `kpi-fill` | color-token | Value from props. |
| `kpi-label-color` | color-token | Color token name (theme color). |
| `kpi-value-color` | color-token | Color token name (theme color). |
| `kpi-value-size` | int(px)/size token | Size/spacing value (px or token). |
| `kpis` | string | Value from props. |
| `layout` | string | Value from props. |
| `show_title_line/show-title-line` | string | Value from props. |
| `title` | string | Text string. |
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
