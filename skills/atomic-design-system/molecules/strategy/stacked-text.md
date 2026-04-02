````markdown
# Molecule: stacked-text

```yaml
id: stacked-text
type: molecule
domain: strategy
layout: stacked-header-rows
description: Compact column card with a title, repeated body rows, and optional takeaway line. Supports text_align, text_valign, body_font_size overrides.
tags: [strategy, topic, overview, grid, column, summary]
preview: previews/molecules/topic-card.png
required_atoms: [text-heading, text-body, shape-divider]
min_atoms: 2
max_atoms: 8
```

## Layout

```
┌─────────────────────────────────────────────────────┐
│  [text-heading: Card title]                         │
│  ────────────────────────────────────────────────   │
│  [text-body: Topic summary]                         │
│  ────────────────────────────────────────────────   │
│  [text-body: Topic summary]                         │
│  ────────────────────────────────────────────────   │
│  [text-body: Topic summary]                         │
│  [shape-divider color]  »»  [text-heading: Takeaway]│
└─────────────────────────────────────────────────────┘
```

- One compact card per slide column
- Intended for adaptive `grid-3` layouts with 2, 3, or 4 cards
- Dividers span the full content width
- Optional takeaway line sits at the bottom and reuses the divider color for the chevrons

## Atoms and Roles

| Atom | Role | Required |
|---|---|---|
| `text-heading` | Card title | yes |
| `shape-divider` | Header and row separators | yes |
| `text-body` | Repeated topic summary rows | yes |
| `text-heading` | Optional takeaway line | no |

## Visual Properties

| Property | Token |
|---|---|
| Card background | `{{theme.color.bg-card}}` |
| Card border | `{{theme.color.border-default}}` |
| Card corner radius | `{{theme.borders.radius-medium}}` |
| Title color | `{{theme.color.card-title-color}}` |
| Body color | `{{theme.color.card-body-color}}` |
| Divider color | `{{theme.color.card-header-line-color}}` |
| Takeaway chevrons | `{{theme.color.line-default}}` |
| Takeaway text | `{{theme.color.card-title-color}}` |

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `body` | string | Value from props. |
| `body_font_size/body-font-size` | int(px)/size token | Size/spacing value (px or token). |
| `heading` | string | Value from props. |
| `headline` | string | Value from props. |
| `items` | list | List of data items. |
| `rows` | list | List of data items. |
| `takeaway` | string | Value from props. |
| `takeaway_line/takeaway-line` | string | Value from props. |
| `text` | string | Value from props. |
| `text_align/text-align` | enum | Alignment enum (left/center/right or top/middle/bottom). |
| `text_valign/text-valign` | enum | Alignment enum (left/center/right or top/middle/bottom). |
| `title` | string | Text string. |
| `topics` | string | Value from props. |
## Example

```yaml
molecule: topic-card
params:
  title: "Modernization"
  items:
    - text: "Energy-efficient upgrade packages improve ride comfort and reduce operating cost."
    - text: "Predictive maintenance bundles shorten downtime across legacy installations."
    - text: "Remote monitoring adds visibility for branch teams and service management."
  takeaway: "Modernization drives efficiency and comfort."
```

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Card container | `.card` | `background`, `border-color`, `border-radius` |
| Title text | shared `--card-title-color` + `--card-title-align` | `color`, `alignment` |
| Row body | shared `--card-body-color` | `color` |
| Divider | shared `--card-title-line-*` tokens | `display`, `color`, `alignment`, `width` |
| Takeaway chevrons | shared `--card-title-line-color` | `color` |
| Takeaway text | shared `--card-title-color` | `color` |

````
