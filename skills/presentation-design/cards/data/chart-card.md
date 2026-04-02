# Chart Card

Card that embeds a chart visual from a referenced image or generated chart data.

## Layout

```
┌─────────────────────────────────────────────────────┐
│  [text-label: card title]          [icon: ●]        │
│  ─────────────────────────────── (header line)      │
│  [text-caption: subtitle]                           │
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
- Icon is optional and appears on the right by default; set `icon.position: left` to flip it.
- Subtitle is optional; appears directly below the header line as muted caption text.
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
| `subtitle` | string | — | Subtitle text below the header line |
| `subtitle_visible` | bool | `false` | Explicitly show/hide subtitle (auto-`true` when `subtitle` text is set) |
| `icon.name` | string | `""` | Icon ligature or codepoint (e.g. `"bar_chart"` for Material Symbols Outlined) |
| `icon.visible` | bool | `false` | Show/hide the title icon |
| `icon.position` | string | `right` | `left` \| `right` — which side of the title row |
| `icon.color` | string | accent | Icon foreground color (hex or token) |
| `icon.size` | int | `20` | Icon size in px |

## Supported Overrides

All `.card-base` overrides plus `.card--chart` tokens:
- `card_chart_image_fit` — `contain` or `cover`
- `card_chart_image_border_radius` — rounding of chart image corners
- `card_chart_caption_font_size` — caption size
- `card_chart_caption_font_color` — caption color

Subtitle and icon tokens (shared with all card types):
- `card_subtitle_font_size` / `card_subtitle_font_color` / `card_subtitle_font_style`
- `card_icon_name` / `card_icon_position` / `card_icon_color` / `card_icon_size`

## Design Tokens Used

- `.card-base` — container, title, header line, subtitle (`--card-subtitle-*`), icon (`--card-icon-*`)
- `.card--chart` — image fit, border radius, caption
- `.image-framed` — chart image rendering
- `.text-caption` — source/caption text

## Example

```yaml
type: chart-card
subtitle: "Quarterly breakdown by region"
icon:
  name: "bar_chart"
  position: right
content:
  image: "charts/revenue-q3.png"
  alt: "Revenue by region Q3 2024"
  caption: "Source: Internal BI dashboard"
style_overrides:
  card_chart_image_fit: contain
```
