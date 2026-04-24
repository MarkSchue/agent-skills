# Quote Card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

Displays a quotation with attribution. Supports highlight/accent styling.

## Layout

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  [text-label: card title]          [icon: â—]        â”‚
â”‚  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ (header line)      â”‚
â”‚  [text-caption: subtitle]                           â”‚
â”‚                                                     â”‚
â”‚  â”ƒ  "Quote text goes here, spanning one or more     â”‚
â”‚  â”ƒ   lines as needed for the full quotation."       â”‚
â”‚                                                     â”‚
â”‚              â€” [text-body: attribution]              â”‚
â”‚                [text-caption: role / org]            â”‚
â”‚                                                     â”‚
â”‚  â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€  (footer line, opt.)      â”‚
â”‚  [text-caption: footer]      (optional, base class)  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
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
| `content.attribution` | string | â€” | Speaker / author name |
| `content.role` | string | â€” | Role or organization |
| `content.footer` | string | â€” | Source attribution or footnote text rendered at the card bottom |
| `subtitle` | string | â€” | Subtitle text below the header line |
| `subtitle_visible` | bool | `false` | Explicitly show/hide subtitle (auto-`true` when `subtitle` text is set) |
| `subtitle_alignment` | string | `left` | `left` \| `center` \| `right` |
| `icon.name` | string | `""` | Icon ligature or codepoint (e.g. `"format_quote"` for Material Symbols Outlined) |
| `icon.visible` | bool | `false` | Show/hide the title icon |
| `icon.position` | string | `right` | `left` \| `right` â€” which side of the title row |
| `icon.color` | string | accent | Icon foreground color (hex or token) |
| `icon.size` | int | `20` | Icon size in px |

## Supported Overrides

All `.card-base` overrides plus `.card--quote` tokens:
- `card_quote_accent_color` â€” left bar color
- `card_quote_accent_width` â€” left bar width in px
- `card_quote_font_size` â€” quote text size
- `card_quote_font_style` â€” `italic` or `normal`
- `card_quote_font_color` â€” quote text color

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
- `.card--quote` â€” accent bar, quote text styling
- `.text-body` â€” attribution name
- `.text-caption` â€” role / org text

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
  card-quote-accent-color: "#0066CC"
```
