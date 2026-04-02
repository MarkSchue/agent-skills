# Text Card

General-purpose text card with heading, body text, and typography variants.

## Layout

```
┌─────────────────────────────────────────────────────┐
│  [text-label: card title]          [icon: ●]        │
│  ─────────────────────────────── (header line)      │
│  [text-caption: subtitle]                           │
│                                                     │
│  [text-h1: heading]                                 │
│  [text-h2: subheading]                              │
│                                                     │
│  [text-body: body paragraph / bullets]              │
│                                                     │
│  [text-caption: caption]                            │
│  [text-footnote: footnote]                          │
│                                                     │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  (footer line, opt.)      │
│  [text-caption: footer]      (optional, base class)  │
└─────────────────────────────────────────────────────┘
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
| `content.heading` | string | — | Heading text (uses `.text-h1`) |
| `content.subheading` | string | — | Subheading text (uses `.text-h2`) |
| `content.bullets` | list | — | Bullet list items |
| `content.caption` | string | — | Caption text below body |
| `content.footnote` | string | — | Footnote text at bottom |
| `content.footer` | string | — | Source attribution or footnote text rendered at the card bottom |
| `subtitle` | string | — | Subtitle text below the header line |
| `subtitle_visible` | bool | `false` | Explicitly show/hide subtitle (auto-`true` when `subtitle` text is set) |
| `subtitle_alignment` | string | `left` | `left` \| `center` \| `right` |
| `icon.name` | string | `""` | Icon ligature or codepoint (e.g. `"article"` for Material Symbols Outlined) |
| `icon.visible` | bool | `false` | Show/hide the title icon |
| `icon.position` | string | `right` | `left` \| `right` — which side of the title row |
| `icon.color` | string | accent | Icon foreground color (hex or token) |
| `icon.size` | int | `20` | Icon size in px |

## Supported Overrides

All `.card-base` overrides plus subtitle and icon tokens:
- `card_subtitle_font_size` — subtitle text size (px)
- `card_subtitle_font_color` — subtitle text color
- `card_subtitle_font_style` — `normal` or `italic`
- `card_subtitle_alignment` — `left` | `center` | `right`
- `card_icon_name` — icon ligature / codepoint
- `card_icon_position` — `left` or `right`
- `card_icon_color` — icon foreground color
- `card_icon_size` — icon size in px
- `card_icon_background_color` — icon badge background

Footer tokens (shared with all card types):
- `card_footer_font_size` — footer font size (px)
- `card_footer_font_color` — footer text color
- `card_footer_font_weight` — `normal` | `bold`
- `card_footer_font_style` — `normal` | `italic`
- `card_footer_alignment` — `left` | `center` | `right`
- `card_footer_margin_top` — space above footer text (px)
- `card_footer_line_visible` — `true` | `false` — show/hide divider above footer
- `card_footer_line_color` — divider color
- `card_footer_line_width` — divider thickness (px)

## Design Tokens Used

- `.card-base` — container, title, header line, footer + footer line (`--card-footer-*`), subtitle (`--card-subtitle-*`), icon (`--card-icon-*`)
- `.text-h1` — heading
- `.text-h2` — subheading
- `.text-body` — body paragraph
- `.text-caption` — caption
- `.text-footnote` — footnote

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
  card_background: "#F8FAFC"
```
