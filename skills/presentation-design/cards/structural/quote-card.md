# Quote Card

Displays a quotation with attribution. Supports highlight/accent styling.

## Layout

```
┌─────────────────────────────────────────────────────┐
│  [text-label: card title]          [icon: ●]        │
│  ─────────────────────────────── (header line)      │
│  [text-caption: subtitle]                           │
│                                                     │
│  ┃  "Quote text goes here, spanning one or more     │
│  ┃   lines as needed for the full quotation."       │
│                                                     │
│              — [text-body: attribution]              │
│                [text-caption: role / org]            │
└─────────────────────────────────────────────────────┘
```

- Left accent bar drawn next to quote text.
- Icon is optional and appears on the right by default; set `icon.position: left` to flip it.
- Subtitle is optional; appears directly below the header line as muted caption text.
- Quote text in italic or styled font.
- Attribution below, right-aligned or centered.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `quote-card` |
| `content.quote` | string | The quotation text |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content.attribution` | string | — | Speaker / author name |
| `content.role` | string | — | Role or organization |
| `subtitle` | string | — | Subtitle text below the header line |
| `subtitle_visible` | bool | `false` | Explicitly show/hide subtitle (auto-`true` when `subtitle` text is set) |
| `subtitle_alignment` | string | `left` | `left` \| `center` \| `right` |
| `icon.name` | string | `""` | Icon ligature or codepoint (e.g. `"format_quote"` for Material Symbols Outlined) |
| `icon.visible` | bool | `false` | Show/hide the title icon |
| `icon.position` | string | `right` | `left` \| `right` — which side of the title row |
| `icon.color` | string | accent | Icon foreground color (hex or token) |
| `icon.size` | int | `20` | Icon size in px |

## Supported Overrides

All `.card-base` overrides plus `.card--quote` tokens:
- `card_quote_accent_color` — left bar color
- `card_quote_accent_width` — left bar width in px
- `card_quote_font_size` — quote text size
- `card_quote_font_style` — `italic` or `normal`
- `card_quote_font_color` — quote text color

Subtitle and icon tokens (shared with all card types):
- `card_subtitle_font_size` / `card_subtitle_font_color` / `card_subtitle_font_style`
- `card_subtitle_alignment` — `left` | `center` | `right`
- `card_icon_name` / `card_icon_position` / `card_icon_color` / `card_icon_size`

## Design Tokens Used

- `.card-base` — container, title, header line, subtitle (`--card-subtitle-*`), icon (`--card-icon-*`)
- `.card--quote` — accent bar, quote text styling
- `.text-body` — attribution name
- `.text-caption` — role / org text

## Example

```yaml
type: quote-card
subtitle: "On leadership and culture"
icon:
  name: "format_quote"
  position: left
content:
  quote: "The best way to predict the future is to invent it."
  attribution: "Alan Kay"
  role: "Computer Scientist"
style_overrides:
  card_quote_accent_color: "#0066CC"
```
