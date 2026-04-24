# Text Card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

General-purpose text card with heading, body text, and typography variants.

## Layout

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  [text-label: card title]          [icon: â—]        â”‚
â”‚  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ (header line)      â”‚
â”‚  [text-caption: subtitle]                           â”‚
â”‚                                                     â”‚
â”‚  [text-h1: heading]                                 â”‚
â”‚  [text-h2: subheading]                              â”‚
â”‚                                                     â”‚
â”‚  [text-body: body paragraph / bullets]              â”‚
â”‚                                                     â”‚
â”‚  [text-caption: caption]                            â”‚
â”‚  [text-footnote: footnote]                          â”‚
â”‚                                                     â”‚
â”‚  â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€  (footer line, opt.)      â”‚
â”‚  [text-caption: footer]      (optional, base class)  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

- Title sits at the top with an optional header line below it.
- Icon is optional and appears on the right by default; set `icon.position: left` to flip it.
- Subtitle is optional; displayed directly below the header line using muted caption styling.
- Body area supports heading, subheading, body text, bullets, caption, and footnote.
- All text styles resolve from the `.text-*` token families.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `text-card` |
| `content.body` | string or list | Main body text or bullet list |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content.heading` | string | â€” | Heading text (uses `.text-h1`) |
| `content.subheading` | string | â€” | Subheading text (uses `.text-h2`) |
| `content.bullets` | list | â€” | Bullet list items |
| `content.caption` | string | â€” | Caption text below body |
| `content.footnote` | string | â€” | Footnote text at bottom |
| `content.footer` | string | â€” | Source attribution or footnote text rendered at the card bottom |
| `subtitle` | string | â€” | Subtitle text below the header line |
| `subtitle_visible` | bool | `false` | Explicitly show/hide subtitle (auto-`true` when `subtitle` text is set) |
| `subtitle_alignment` | string | `left` | `left` \| `center` \| `right` |
| `icon.name` | string | `""` | Icon ligature or codepoint (e.g. `"article"` for Material Symbols Outlined) |
| `icon.visible` | bool | `false` | Show/hide the title icon |
| `icon.position` | string | `right` | `left` \| `right` â€” which side of the title row |
| `icon.color` | string | accent | Icon foreground color (hex or token) |
| `icon.size` | int | `20` | Icon size in px |

## Supported Overrides

All `.card-base` overrides plus subtitle and icon tokens:
- `card_subtitle_font_size` â€” subtitle text size (px)
- `card_subtitle_font_color` â€” subtitle text color
- `card_subtitle_font_style` â€” `normal` or `italic`
- `card_subtitle_alignment` â€” `left` | `center` | `right`
- `card_body_gap_top` â€” space between the header area and body content when subtitle is absent (px)
- `card_icon_name` â€” icon ligature / codepoint
- `card_icon_position` â€” `left` or `right`
- `card_icon_color` â€” icon foreground color
- `card_icon_size` â€” icon size in px
- `card_icon_background_color` â€” icon badge background

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

## Design Tokens Used

- `.card-base` â€” container, title, header line, footer + footer line (`--card-footer-*`), subtitle (`--card-subtitle-*`), icon (`--card-icon-*`)
- `.text-h1` â€” heading
- `.text-h2` â€” subheading
- `.text-body` â€” body paragraph
- `.text-caption` â€” caption
- `.text-footnote` â€” footnote

## Example

```yaml
type: text-card
subtitle: "Strategic priorities for FY2026"
icon:
  name: "lightbulb"
  position: right
content:
  heading: "Our Vision"
  body: "We believe in building products that matter."
  bullets:
    - "Customer-first approach"
    - "Data-driven decisions"
    - "Continuous improvement"
  caption: "Updated Q3 2025"
style_overrides:
  card-background: "#F8FAFC"
```
