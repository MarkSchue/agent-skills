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

### Card-level

| Parameter              | Type   | Default              | Description |
|------------------------|--------|----------------------|-------------|
| `title`                | string | —                    | Optional card header title |
| `columns`              | list   | —                    | Column header definitions (see below). If omitted, inferred from row cell counts. |
| `rows`                 | list   | **required**         | Data row definitions (see below) |
| `label-col-width`      | float  | `0.14`               | Fraction of inner card width for the row-label column. Set to `0` to hide. |
| `label-col-fill`       | color  | `primary`            | Background fill for row-label cells |
| `label-col-text-color` | color  | `on-primary`         | Text color in row-label cells |
| `label-col-align`      | enum   | `center`             | `center` · `left` · `right` — text alignment in row labels |
| `col-header-fill`      | color  | `surface-variant`    | Default background for column-header row |
| `col-header-text-color`| color  | `on-surface`         | Default text color in column headers |
| `col-header-height`    | int    | auto (≈20% of height)| Explicit px height for the column-header row |
| `cell-fill`            | color  | `bg-card`            | Default data-cell background |
| `cell-text-color`      | color  | `on-surface`         | Default data-cell text color |
| `border-color`         | color  | `border-default`     | Cell border / grid-line color |
| `border-radius`        | int    | `0`                  | Corner radius of each cell in px |
| `cell-pad`             | int    | spacing s (8)        | Inner cell padding in px |
| `badge-fill`           | color  | `on-surface`         | Default badge background (column-headers + cells) |
| `badge-text-color`     | color  | `surface`            | Default badge text color |
| `show-header`          | bool   | auto                 | Show/hide the card title header block |
| `show-header-line`     | bool   | `true`               | Line below the card title header |
| `bg-color`             | color  | `bg-card`            | Card background color override |

### Column object fields

| Field        | Type   | Required | Description |
|--------------|--------|----------|-------------|
| `label`      | string | no       | Column header bold text |
| `subtitle`   | string | no       | Smaller secondary line below the header label |
| `badge`      | string | no       | Small pill badge at the bottom of the header cell |
| `width`      | float  | no       | Relative fraction of the content width (auto-normalised across columns) |
| `fill`       | color  | no       | Per-column header background override |
| `text-color` | color  | no       | Per-column header text color override |

### Row object fields

| Field         | Type          | Required | Description |
|---------------|---------------|----------|-------------|
| `label`       | string        | no       | Row label text (displayed in the left column) |
| `label-fill`  | color         | no       | Per-row label cell background override |
| `label-color` | color         | no       | Per-row label text color override |
| `height`      | int or float  | no       | `> 1` = explicit px · `0..1` = fraction of content height |
| `cells`       | list          | yes      | Ordered list of cell objects (left → right) |

### Cell object fields

| Field              | Type   | Required | Description |
|--------------------|--------|----------|-------------|
| `text`             | string | yes      | Main cell content |
| `bold`             | bool   | no       | Bold weight for `text`                         default: `false` |
| `subtitle`         | string | no       | Smaller secondary line below `text` |
| `badge`            | string | no       | Small pill inside the cell |
| `badge-fill`       | color  | no       | Per-cell badge fill override |
| `badge-text-color` | color  | no       | Per-cell badge text color override |
| `span`             | int    | no       | Number of columns this cell covers             default: `1` |
| `fill`             | color  | no       | Cell background override |
| `text-color`       | color  | no       | Cell text color override |
| `align`            | enum   | no       | `left` · `center` · `right`                    default: `left` |
| `valign`           | enum   | no       | `top` · `middle` · `bottom`                    default: `middle` |

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
