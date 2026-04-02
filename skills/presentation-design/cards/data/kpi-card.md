# KPI Card

Key performance indicator card with large metric value, trend indicator, and label.

## Layout

```
┌─────────────────────────────────────────────────────┐
│  [text-label: card title]                           │
│  ─────────────────────────────── (header line)      │
│                                                     │
│              [stat: value]                          │
│              ↑ [trend: direction]                   │
│                                                     │
│              [text-caption: label]                  │
└─────────────────────────────────────────────────────┘
```

- Large metric value displayed prominently in center/left.
- Trend arrow (up/down/neutral) with color-coded indicator.
- Supporting label below the metric.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `kpi-card` |
| `content.value` | string | The metric value (e.g. "$4.2M", "12,500") |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content.trend` | string | `neutral` | `up` \| `down` \| `neutral` |
| `content.label` | string | — | Supporting label text |
| `content.comparison` | string | — | Comparison text (e.g. "vs Q2") |

## Supported Overrides

All `.card-base` overrides plus `.card--kpi` tokens:
- `card_kpi_value_font_size` — metric size
- `card_kpi_value_font_color` — metric color
- `card_kpi_trend_color_up` — positive trend color
- `card_kpi_trend_color_down` — negative trend color

## Design Tokens Used

- `.card-base` — container, title, header line
- `.card--kpi` — value size/color, trend colors, label
- `.text-caption` — label text

## Example

```yaml
type: kpi-card
content:
  value: "$4.2M"
  trend: "up"
  label: "Annual Revenue"
  comparison: "+18% vs Q2"
style_overrides:
  card_kpi_value_font_size: 56
```
