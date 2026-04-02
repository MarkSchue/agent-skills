# Chart Card

Card that embeds a chart visual from a referenced image or generated chart data.

## Layout

```
┌─────────────────────────────────────────────────────┐
│  [text-label: card title]                           │
│  ─────────────────────────────── (header line)      │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │                                               │  │
│  │           [image: chart visual]               │  │
│  │                                               │  │
│  └───────────────────────────────────────────────┘  │
│                                                     │
│  [text-caption: source attribution]                 │
└─────────────────────────────────────────────────────┘
```

- Chart image fills the card body area.
- An optional caption/source line sits below the chart.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `chart-card` |
| `content.image` | string | Path to chart image (relative to `assets/images/`) |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content.alt` | string | — | Alt text for the chart |
| `content.caption` | string | — | Source attribution or description |

## Supported Overrides

All `.card-base` overrides plus `.card--chart` tokens:
- `card_chart_image_fit` — `contain` or `cover`
- `card_chart_image_border_radius` — rounding of chart image corners
- `card_chart_caption_font_size` — caption size
- `card_chart_caption_font_color` — caption color

## Design Tokens Used

- `.card-base` — container, title, header line
- `.card--chart` — image fit, border radius, caption
- `.image-framed` — chart image rendering
- `.text-caption` — source/caption text

## Example

```yaml
type: chart-card
content:
  image: "charts/revenue-q3.png"
  alt: "Revenue by region Q3 2024"
  caption: "Source: Internal BI dashboard"
style_overrides:
  card_chart_image_fit: contain
```
