# KPI Card

Key performance indicator card with large metric value, trend indicator, and label.

## Layout

```
┌─────────────────────────────────────────────────────┐
│  [text-label: card title]          [icon: ●]        │
│  ─────────────────────────────── (header line)      │
│  [text-caption: subtitle]                           │
│                                                     │
│              [stat: value]                          │
│              ↑ [trend: direction]                   │
│                                                     │
│              [text-caption: label]                  │
└─────────────────────────────────────────────────────┘
```

- Large metric value displayed prominently in center/left.
- Icon is optional and appears on the right by default; set `icon.position: left` to flip it.
- Subtitle is optional; appears directly below the header line as muted caption text.
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
| `subtitle` | string | — | Subtitle text below the header line |
| `subtitle_visible` | bool | `false` | Explicitly show/hide subtitle (auto-`true` when `subtitle` text is set) |
| `icon.name` | string | `""` | Icon ligature or codepoint (e.g. `"trending_up"` for Material Symbols Outlined) |
| `icon.visible` | bool | `false` | Show/hide the title icon |
| `icon.position` | string | `right` | `left` \| `right` — which side of the title row |
| `icon.color` | string | accent | Icon foreground color (hex or token) |
| `icon.size` | int | `20` | Icon size in px |

## Supported Overrides

All `.card-base` overrides plus `.card--kpi` tokens:
- `card_kpi_value_font_size` — metric size
- `card_kpi_value_font_color` — metric color
- `card_kpi_trend_color_up` — positive trend color
- `card_kpi_trend_color_down` — negative trend color

Subtitle and icon tokens (shared with all card types):
- `card_subtitle_font_size` / `card_subtitle_font_color` / `card_subtitle_font_style`
- `card_icon_name` / `card_icon_position` / `card_icon_color` / `card_icon_size`

## Design Tokens Used

- `.card-base` — container, title, header line, subtitle (`--card-subtitle-*`), icon (`--card-icon-*`)
- `.card--kpi` — value size/color, trend colors, label
- `.text-caption` — label text

## Example

```yaml
type: kpi-card
subtitle: "Q3 2025 Performance"
icon:
  name: "trending_up"
  position: right
content:
  value: "$4.2M"
  trend: "up"
  label: "Annual Revenue"
  comparison: "+18% vs Q2"
style_overrides:
  card_kpi_value_font_size: 56
```
