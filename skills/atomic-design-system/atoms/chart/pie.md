# Atom: chart-pie

```yaml
id: chart-pie
type: data-viz
description: Pie or donut chart showing proportional distribution of a numeric dataset.
tags: [chart, data, distribution, pie, proportion]
preview: previews/atoms/chart-pie.png
svg-source: atoms/svg/chart-pie.svg
```

## Visual Properties

| Property | Token |
|---|---|
| Slice 1 fill | `{{theme.color.primary}}` |
| Slice 2 fill | `{{theme.color.secondary}}` |
| Slice 3+ fill | `{{theme.color.accent}}`, `{{theme.color.neutral}}` |
| Label text | `{{theme.color.on-surface}}` |
| Background | `{{theme.color.surface}}` |
| Donut center | `{{theme.color.surface}}` (transparent for pie) |

## Data Input Schema

```yaml
data-input-schema:
  slices:
    type: list[object]
    required: true
    items:
      label:   {type: string, required: true}
      value:   {type: number, required: true}
    example:
      - {label: "Product A", value: 45}
      - {label: "Product B", value: 30}
      - {label: "Product C", value: 25}
  unit:
    type: string
    required: false
    default: "%"
  style:
    type: enum[pie, donut]
    required: false
    default: pie
  show-labels:
    type: boolean
    required: false
    default: true
  legend_position:
    type: enum[right, left, below, above]
    required: false
    default: right
    description: |
      "right"  — legend column to the right of the chart (default)
      "left"   — legend column to the left of the chart
      "below"  — legend as a compact horizontal strip below the chart;
                 chart circle becomes larger to use the full card width
      "above"  — legend strip above the chart; larger chart below
```

## Display Options (Verbal Configuration)

Describe what you want in plain language — the agent translates it:

| Natural language instruction | Resolved option |
|---|---|
| "put the legend below the chart" | `legend_position: below` |
| "legend on the right" | `legend_position: right` (default) |
| "move the legend to the left" | `legend_position: left` |
| "legend above" | `legend_position: above` |

When `legend_position` is `below` or `above`, the circle is larger because it
can use the full card width instead of sharing it with the legend column.

## Behavior

- Values are automatically normalised to percentage of total.
- Up to 6 slices supported; slices beyond 6 are merged into "Other".
- Donut style: hollow center with optional center label (e.g. total or title).
- Slice colors are assigned in order from the color token sequence: `primary`, `secondary`,
  `accent`, `neutral`, then tints of `primary` and `secondary`.

## Example Fenced Block in Markdown

```chart:pie
slices:
  - label: "Enterprise"
    value: 55
  - label: "Mid-Market"
    value: 30
  - label: "SMB"
    value: 15
unit: "%"
style: donut
```

## Notes

- SVG source `atoms/svg/chart-pie.svg` is recolored at assembly time.
- If only two slices are provided, a half-and-half composition is used automatically.
