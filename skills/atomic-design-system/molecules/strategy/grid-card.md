# grid-card

**Molecule slug:** `grid-card`
**Domain:** strategy
**Category:** Matrix / Overview

A flexible matrix grid card. Rows run vertically; an optional first column shows
row-label chips (colored fill). Column headers sit above the data rows. Individual
cells can **span multiple columns**. All proportions, colours, and row heights are
fully customisable.

## Design anatomy

```
┌──────────────────────────────────────────────────────────────────┐
│  [Optional card title header]                                    │
│  ┌──────┬───────────────────┬──────────────────┬──────────────┐  │
│  │      │  Col A            │  Col B           │  Col C       │  │  ← column headers
│  │      │  (subtitle)       │  (subtitle)      │  [badge]     │  │
│  ├──────┼───────────────────┴──────────────────┴──────────────┤  │
│  │ Row1 │  Cell spanning all 3 columns (span: 3)              │  │
│  ├──────┼───────────────────┬──────────────────┬──────────────┤  │
│  │ Row2 │  Cell A           │  Cell B+C (span:2)              │  │
│  ├──────┼───────────────────┼──────────────────┬──────────────┤  │
│  │ Row3 │  Cell A           │  Cell B          │  Cell C      │  │
│  └──────┴───────────────────┴──────────────────┴──────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `badge-fill` | color-token | Value from props. |
| `badge-text-color` | color-token | Color token name (theme color). |
| `border-color` | color-token | Color token name (theme color). |
| `cell-fill` | color-token | Value from props. |
| `cell-text-color` | color-token | Color token name (theme color). |
| `col-header-fill` | color-token | Value from props. |
| `col-header-height` | int(px)/size token | Size/spacing value (px or token). |
| `col-header-text-color` | color-token | Color token name (theme color). |
| `columns` | list | List of data items. |
| `label-col-align` | enum | Alignment enum (left/center/right or top/middle/bottom). |
| `label-col-fill` | color-token | Label text content. |
| `label-col-text-color` | color-token | Color token name (theme color). |
| `rows` | list | List of data items. |
| `title` | string | Text string. |
## Examples

### Stakeholder matrix (matches screenshot pattern)

```yaml
molecule: grid-card
title: Initiative Overview
label-col-width: 0.13
label-col-fill: primary
col-header-fill: surface-variant
columns:
  - label: "BOM Accuracy"
    subtitle: "(EBOM→MBOM→OBOM)"
    badge: "Global MFG"
  - label: "Design Accuracy"
    subtitle: "(Mech/Elect DWG)"
    badge: "Global R&D PDC"
  - label: "SW Dev Tools"
    subtitle: "(AI Code Assistant)"
    badge: "Global R&D GCSW"
rows:
  - label: Sponsor
    cells:
      - text: Provides strategic direction and secures resources to support the project's success
        span: 3
  - label: Tech. Lead
    cells:
      - text: Drives the AI solution's development and owns delivery of business value
        span: 3
  - label: Resources
    cells:
      - text: "Partner:"
        subtitle: MSFT
      - text: "Partner:"
        subtitle: TBD (Rescale)
      - text: "Partner:"
        subtitle: CuriousBox
```

### Simple 3×3 grid without a label column

```yaml
molecule: grid-card
label-col-width: 0
columns:
  - label: "Q1"
  - label: "Q2"
  - label: "Q3"
rows:
  - cells:
      - text: Discovery & scoping
      - text: Pilot build
      - text: Rollout begins
  - cells:
      - text: 15 interviews
        align: center
      - text: "3 teams"
        align: center
      - text: "7 teams"
        align: center
```

### Per-row height control + cell spanning

```yaml
molecule: grid-card
label-col-width: 0.15
columns:
  - label: "Area A"
  - label: "Area B"
  - label: "Area C"
rows:
  - label: Summary
    height: 0.25
    cells:
      - text: This row gets 25 % of the available content height and spans all columns
        span: 3
  - label: Detail
    cells:
      - text: Normal cell
      - text: Wider (spans 2)
        span: 2
  - label: Status
    cells:
      - text: Green
        fill: success-container
        text-color: on-success-container
        align: center
      - text: Amber
        fill: warning-container
        text-color: on-warning-container
        align: center
      - text: Red
        fill: error-container
        text-color: on-error-container
        align: center
```

## CSS design tokens

| Token                          | Description                          |
|--------------------------------|--------------------------------------|
| `--color-primary`              | Default row-label fill               |
| `--color-on-primary`           | Default row-label text               |
| `--color-surface-variant`      | Default column-header fill           |
| `--color-on-surface`           | Default cell text color              |
| `--color-border-default`       | Grid line / cell border color        |
| `--color-bg-card`              | Default data-cell background         |
