# table-card

Card-framed native table for strategy and estimation content. It uses the
platform table primitive, so exported output stays editable in PowerPoint and
draw.io while still following the design system card contract.

## When to use

- Estimates, effort breakdowns, and cost tables
- Comparison grids with totals
- Simple tabular strategy data that should remain editable after export

---

## Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `title` | string | — | Card header title |
| `subtitle` | string | — | Optional subtitle below the title |
| `columns` | list | auto | Column definitions: `label`, `width`, `align` |
| `rows` | list | `[]` | Data rows as lists or dicts |
| `total` | list/dict | — | Optional single total row |
| `has-header` | bool | auto | Show header row when column labels exist |
| `alt-rows` | bool | `true` | Alternate row fill colors |
| `header-fill` | color | `primary` | Header row background |
| `header-text-color` | color | `on-primary` | Header row text color |
| `row-fill` | color | `surface` | Base data row fill |
| `alt-fill` | color | `surface-variant` | Alternating row fill |
| `total-fill` | color | `surface-variant` | Total row background |
| `total-text-color` | color | `on-surface` | Total row text color |
| `border-color` | color | `border-subtle` | Grid line color |
| `text-size` | int | body size | Table body font size |
| `bold-header` | bool | `true` | Bold header labels |
| `bold-total` | bool | `true` | Bold total row |

### Column definition

| Key | Type | Description |
|---|---|---|
| `label` | string | Header text |
| `width` | float | Relative width fraction |
| `align` | string | `left`, `center`, or `right` |

---

## Examples

### Basic effort table

```markdown
---
molecule: table-card
title: Delivery effort by workstream
columns:
  - { label: Workstream, width: 0.42, align: left }
  - { label: Days, width: 0.18, align: center }
  - { label: Cost, width: 0.22, align: right }
  - { label: Owner, width: 0.18, align: left }
rows:
  - [Platform setup, 12, "€ 9,600", Architecture]
  - [API integration, 18, "€ 14,400", Backend]
  - [UI rollout, 10, "€ 8,000", Frontend]
total: [Total, 40, "€ 32,000", ""]
---
```

### Rows as dictionaries

```markdown
---
molecule: table-card
title: Initiative sizing
columns:
  - { label: Initiative, width: 0.5 }
  - { label: Complexity, width: 0.2, align: center }
  - { label: Confidence, width: 0.3, align: right }
rows:
  - Initiative: Self-service onboarding
    Complexity: Medium
    Confidence: 80%
  - Initiative: Legacy migration
    Complexity: High
    Confidence: 55%
---
```

### Subtle companion style

```markdown
---
molecule: table-card
title: Budget assumptions
subtitle: FY25 planning baseline
header-fill: secondary
header-text-color: on-secondary
row-fill: bg-card
alt-fill: surface-container
border-color: border-default
columns:
  - { label: Item, width: 0.5 }
  - { label: Amount, width: 0.25, align: right }
  - { label: Notes, width: 0.25 }
rows:
  - [Vendor licenses, "€ 45,000", Annual contract]
  - [Implementation, "€ 120,000", External support]
---
```

---

## Notes

- `rows` can be provided as lists or dictionaries.
- If `columns` are omitted, the table infers the number of columns from the
  first row.
- `total` is rendered as a dedicated final summary row.
- Because the renderer uses the native table primitive, users can still resize
  columns and edit cells after export.

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `alt-fill` | color-token | Value from props. |
| `alt-rows` | string | Value from props. |
| `bold-header` | string | Value from props. |
| `bold-total` | string | Value from props. |
| `border-color` | color-token | Color token name (theme color). |
| `columns` | list | List of data items. |
| `has-header` | string | Value from props. |
| `header-fill` | color-token | Value from props. |
| `header-text-color` | color-token | Color token name (theme color). |
| `row-fill` | color-token | Value from props. |
| `rows` | list | List of data items. |
| `subtitle` | string | Text string. |
| `text-size` | int(px)/size token | Size/spacing value (px or token). |
| `title` | string | Text string. |
| `total` | string | Value from props. |
| `total-fill` | color-token | Value from props. |
| `total-text-color` | color-token | Color token name (theme color). |