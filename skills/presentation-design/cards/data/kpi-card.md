# KPI Card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

Key performance indicator card with large metric value, trend indicator, and label.

## Layout

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  [text-label: card title]          [icon: â—]        â”‚
â”‚  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ (header line)      â”‚
â”‚  [text-caption: subtitle]                           â”‚
â”‚                                                     â”‚
â”‚              [stat: value]                          â”‚
â”‚              â†‘ [trend: direction]                   â”‚
â”‚                                                     â”‚
â”‚              [text-caption: label]                  â”‚
â”‚                                                     â”‚
â”‚  â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€  (footer line, opt.)      â”‚
â”‚  [text-caption: footer]      (optional, base class)  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
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
| `content.label` | string | â€” | Supporting label text |
| `content.comparison` | string | â€” | Comparison text (e.g. "vs Q2") |
| `content.footer` | string | â€” | Source attribution or footnote text rendered at the card bottom |
| `subtitle` | string | â€” | Subtitle text below the header line |
| `subtitle_visible` | bool | `false` | Explicitly show/hide subtitle (auto-`true` when `subtitle` text is set) |
| `subtitle_alignment` | string | `left` | `left` \| `center` \| `right` |
| `icon.name` | string | `""` | Icon ligature or codepoint (e.g. `"trending_up"` for Material Symbols Outlined) |
| `icon.visible` | bool | `false` | Show/hide the title icon |
| `icon.position` | string | `right` | `left` \| `right` â€” which side of the title row |
| `icon.color` | string | accent | Icon foreground color (hex or token) |
| `icon.size` | int | `20` | Icon size in px |

## Supported Overrides

All `.card-base` overrides plus `.card--kpi` tokens:
- `card_kpi_value_font_size` â€” metric size
- `card_kpi_value_font_color` â€” metric color
- `card_kpi_trend_color_up` â€” positive trend color
- `card_kpi_trend_color_down` â€” negative trend color

Footer tokens (shared with all card types):
- `card_footer_font_size` â€” footer font size (px)
- `card_footer_font_color` â€” footer text color
- `card_footer_font_weight` â€” `normal` | `bold`
- `card_footer_font_style` â€” `normal` | `italic`
- `card_footer_alignment` â€” `left` | `center` | `right`
- `card_footer_margin_top` â€” space above footer text (px)
- `card_footer_line_visible` â€” `true` | `false` â€” show/hide divider above footer
- `card_footer_line_color` â€” divider color
- `card_footer_line_width` â€” divider thickness (px)

Subtitle and icon tokens (shared with all card types):
- `card_subtitle_font_size` / `card_subtitle_font_color` / `card_subtitle_font_style`
- `card_subtitle_alignment` â€” `left` | `center` | `right`
- `card_icon_name` / `card_icon_position` / `card_icon_color` / `card_icon_size`

## Design Tokens Used

- `.card-base` â€” container, title, header line, footer + footer line (`--card-footer-*`), subtitle (`--card-subtitle-*`), icon (`--card-icon-*`)
- `.card--kpi` â€” value size/color, trend colors, label
- `.text-caption` â€” label text

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
  card-kpi-value-font-size: 56
```
