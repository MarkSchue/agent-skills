````markdown
# Molecule: topic-card

```yaml
id: stacked-text
type: molecule
domain: strategy
layout: stacked-header-rows
description: Compact column card with a title, repeated topic rows, and optional takeaway line. Also registered as topic-card (legacy alias).
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
| `title` | string | Card heading shown in the header area |
| `items` | `list[object] \| list[string]` | Topic rows as `{text}` / `{body}` or plain strings |
| `takeaway` | string | Optional bold takeaway line at the bottom |
| `takeaway-line` | string | Hyphenated alias for `takeaway` |
| `card_bg` | enum | Optional existing card background override (`default`, `clean`, `filled`, `alt`, `featured`) |
| `header_align` | enum | Optional shared card header alignment override (`left`, `center`, `right`) |
| `show_header_line` | boolean | Optional divider below the title; defaults to `true` |
| `header_line_width` | string/number | Optional shared divider width override (`100%`, `0.7`, `70`) |
| `header_line_align` | enum | Optional shared divider alignment override (`left`, `center`, `right`) |
| `text_align` | enum | Global text alignment for all text elements: title, rows, takeaway (`left`, `center`, `right`). Defaults to `left`. When `center`, the takeaway chevrons (»») are suppressed. |

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
| Title text | shared `--card-title-color` + `--card-header-title-align` | `color`, `alignment` |
| Row body | shared `--card-body-color` | `color` |
| Divider | shared `--card-header-line-*` tokens | `display`, `color`, `alignment`, `width` |
| Takeaway chevrons | shared `--card-header-line-color` | `color` |
| Takeaway text | shared `--card-title-color` | `color` |

````
