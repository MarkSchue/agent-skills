# Image Card

Card displaying an image in full-bleed, framed, or circular presentation mode.

## Layout

```
┌─────────────────────────────────────────────────────┐
│  [text-label: card title]                           │
│  ─────────────────────────────── (header line)      │
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

## Supported Overrides

All `.card-base` overrides plus:
- Image style tokens from `.image-fullbleed`, `.image-framed`, or `.image-circular`

## Design Tokens Used

- `.card-base` — container, title, header line
- `.image-framed` / `.image-fullbleed` / `.image-circular` — image presentation
- `.text-caption` — caption

## Example

```yaml
type: image-card
content:
  source: "assets/images/team-photo.jpg"
  caption: "Our team at the annual retreat"
  image_style: framed
```
