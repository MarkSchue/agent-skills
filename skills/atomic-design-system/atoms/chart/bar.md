# Atom: chart-bar

```yaml
id: chart-bar
type: data-viz
description: Horizontal or vertical bar chart populated with labeled numeric series data.
tags: [chart, data, performance, bar, comparison]
preview: previews/atoms/chart-bar.png
svg-source: atoms/svg/chart-bar.svg
```

## Visual Properties

| Property | Token |
|---|---|
| Bar fill | `{{theme.color.primary}}` |
| Axis / grid lines | `{{theme.shape.thin-line}}` |
| Axis label text | `{{theme.color.on-surface}}` |
| Value label text | `{{theme.color.on-surface}}` |
| Background | `{{theme.color.surface}}` |
| Series 2+ colors | `{{theme.color.secondary}}`, `{{theme.color.accent}}` |

## Data Input Schema

```yaml
data-input-schema:
  labels:    # list of string, one per bar / category
    type: list[string]
    required: true
    example: ["Q1", "Q2", "Q3", "Q4"]
  values:    # numeric value for each label (matches length of labels)
    type: list[number]
    required: true
    example: [120, 145, 98, 160]
  unit:      # displayed after values (e.g. "$k", "%", "units")
    type: string
    required: false
    default: ""
  series-name:   # legend entry for this data series
    type: string
    required: false
  orientation:   # "vertical" (default) or "horizontal"
    type: enum[vertical, horizontal]
    required: false
    default: vertical
  label_position:  # where value annotations appear
    type: enum[above, inside-bottom]
    required: false
    default: above
    description: |
      "above"         — value floats above each bar (default)
      "inside-bottom" — value rendered inside the bar near its bottom edge,
                        using on-filled contrast color. Best for taller bars.
                        Falls back to "above" if the bar is too short.
```

## Display Options (Verbal Configuration)

Instead of remembering key names, describe what you want in plain language and the agent
translates it. Examples:

| Natural language instruction | Resolved option |
|---|---|
| "add the numbers inside the bars at the bottom" | `label_position: inside-bottom` |
| "show values above each bar" | `label_position: above` |
| "put the labels inside" | `label_position: inside-bottom` |

## Behavior

- If the user provides data matching the schema in a `\`\`\`chart:bar` fenced block, the atom uses
  that data at assembly time.
- If required data is missing or has wrong length, the skill uses labeled placeholder values
  (`[A, B, C, D]`, `[25, 50, 75, 60]`) and notifies the user.
- Multi-series: repeat the `values` key as `values_2`, `values_3` with corresponding series names.
- Bars are sized proportionally; the tallest bar fills ~80% of the chart height.
- No hardcoded pixel dimensions; canvas width/height from `design-config.yaml` `canvas` section.

## Example Fenced Block in Markdown

```chart:bar
labels: [Jan, Feb, Mar, Apr]
values: [42, 67, 55, 89]
unit: "%"
series-name: Completion Rate
orientation: vertical
```

## Notes

- SVG source `atoms/svg/chart-bar.svg` is recolored at assembly; do not edit the SVG directly.
- For multi-color series, each series color maps to `primary`, `secondary`, `accent` in order.
