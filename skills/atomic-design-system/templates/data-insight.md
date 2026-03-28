# Template: data-insight

```yaml
id: data-insight
type: template
description: Wide chart on the left with key insights and supporting KPIs on the right.
tags: [data, insight, analysis, chart, mixed, performance]
preview: previews/templates/data-insight.png
canvas-size: "{{design-config.canvas}}"
max_elements: 4
compatible_aspect_ratios: ["16:9"]
compatible_molecules: [data-insight-panel, chart-card, kpi-card, trend-card, comparison-card]
```

## Slot Definitions

```
┌─────────────────────────────────────────────────────────────────────────┐
│  [SLOT-HEADER]  ─────────────────────────────────────── full width      │
├────────────────────────────────────┬────────────────────────────────────┤
│                                    │  [SLOT-INSIGHT]                    │
│   SLOT-CHART                       │  key insights + headline numbers   │
│   (58% width, tall)                │  (38% width)                       │
│                                    │  ──────────────── (divider)        │
│                                    │  [SLOT-KPI-ROW]                    │
│                                    │  2-3 mini KPIs                     │
└────────────────────────────────────┴────────────────────────────────────┘
```

## Slot Specifications

| Slot | Accepts | Required | Width | Height |
|---|---|---|---|---|
| `slot-header` | `text-heading` | no | 100% | auto |
| `slot-chart` | `chart-card`, `data-insight-panel`, `trend-card` | yes | 58% | 78% canvas height |
| `slot-insight` | `text-body` (bullet insights) | yes | 38% | 50% of slot-chart height |
| `slot-kpi-row` | up to 3 × `kpi-card` in a row | no | 38% | remaining height in right column |

- Gutter between left and right: `{{theme.spacing.l}}`
- Outer margin: `{{design-config.canvas.margin}}`

## Background & Decoration

- Background: `{{theme.color.surface}}`
- Right-column KPI separator: `{{theme.shape.divider}}`
- Header accent: `{{theme.shape.accent-line}}`

## Design Constraints

- `slot-chart` must be a data visualization molecule (chart-card, data-insight-panel, or trend-card)
- `slot-kpi-row` KPIs are rendered as a horizontal strip; stack vertically if only 1-2 are provided
- `slot-insight` should contain 3-5 bullet points for maximum readability

## Validation Rules

- `slot-chart` width + gutter + `slot-insight` width + 2 × margin ≤ canvas width
- Aspect ratio must be `16:9` (not `4:3` — insufficient horizontal space)

## Example Usage

```yaml
template: data-insight
slots:
  slot-header:
    atom: text-heading
    params: {text: "Q3 Revenue Analysis", level: h2, accent-rule: true}
  slot-chart:
    molecule: chart-card
    params:
      title: "Revenue by Month"
      chart-type: bar
      chart-data:
        labels: [Jul, Aug, Sep]
        values: [3.8, 4.1, 4.5]
        unit: M€
  slot-insight:
    atom: text-body
    params:
      text:
        - "September achieved record monthly revenue at €4.5M"
        - "MoM growth consistent at ~8% across all three months"
        - "Enterprise segment drove 60% of September bookings"
      format: bullets
  slot-kpi-row:
    molecules:
      - kpi-card: {label: "Total Q3", value: "€12.4M", change: "+22%", trend: up}
      - kpi-card: {label: "New Logos", value: "34", change: "+6", trend: up}
      - kpi-card: {label: "Churn", value: "1.8%", change: "-0.3%", trend: up}
```
