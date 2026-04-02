# Image Card

Card displaying an image in full-bleed, framed, or circular presentation mode.

## Layout

```
┌─────────────────────────────────────────────────────┐
│  [text-label: card title]          [icon: ●]        │
│  ─────────────────────────────── (header line)      │
│  [text-caption: subtitle]                           │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │                                               │  │
│  │            [image: source]                    │  │
│  │                                               │  │
│  └───────────────────────────────────────────────┘  │
│                                                     │
│  [text-caption: caption]                            │
└─────────────────────────────────────────────────────┘
```

- Image fills the body area in one of three styles: fullbleed, framed, circular.
- Icon is optional and appears on the right by default; set `icon.position: left` to flip it.
- Subtitle is optional; appears directly below the header line as muted caption text.
- Optional caption below the image.
- Image style tokens control border, radius, and padding.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `image-card` |
| `content.source` | string | Relative path to image in `assets/` |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content.caption` | string | — | Caption below image |
| `content.alt` | string | — | Alt text for accessibility |
| `content.image_style` | string | `framed` | `fullbleed` \| `framed` \| `circular` |
| `subtitle` | string | — | Subtitle text below the header line |
| `subtitle_visible` | bool | `false` | Explicitly show/hide subtitle (auto-`true` when `subtitle` text is set) |
| `subtitle_alignment` | string | `left` | `left` \| `center` \| `right` |
| `icon.name` | string | `""` | Icon ligature or codepoint (e.g. `"photo_camera"` for Material Symbols Outlined) |
| `icon.visible` | bool | `false` | Show/hide the title icon |
| `icon.position` | string | `right` | `left` \| `right` — which side of the title row |
| `icon.color` | string | accent | Icon foreground color (hex or token) |
| `icon.size` | int | `20` | Icon size in px |

## Supported Overrides

All `.card-base` overrides plus:
- Image style tokens from `.image-fullbleed`, `.image-framed`, or `.image-circular`

Subtitle and icon tokens (shared with all card types):
- `card_subtitle_font_size` / `card_subtitle_font_color` / `card_subtitle_font_style`
- `card_subtitle_alignment` — `left` | `center` | `right`
- `card_icon_name` / `card_icon_position` / `card_icon_color` / `card_icon_size`

## Design Tokens Used

- `.card-base` — container, title, header line, subtitle (`--card-subtitle-*`), icon (`--card-icon-*`)
- `.image-framed` / `.image-fullbleed` / `.image-circular` — image presentation
- `.text-caption` — caption

## Example

```yaml
type: image-card
subtitle: "Annual company retreat 2025"
icon:
  name: "photo_camera"
  position: right
content:
  source: "assets/images/team-photo.jpg"
  caption: "Our team at the annual retreat"
  image_style: framed
```
