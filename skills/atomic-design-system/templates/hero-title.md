# Template: hero-title

```yaml
id: hero-title
type: template
description: Full-width hero slide with a large central title, subtitle, and optional background accent.
tags: [hero, title, cover, intro, section-break]
preview: previews/templates/hero-title.png
canvas-size: "{{design-config.canvas}}"
max_elements: 3
compatible_aspect_ratios: ["16:9", "4:3"]
compatible_molecules: [mission-card, quote-card, text-heading, text-body]
```

## Slot Definitions

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                         ┌───────────────┐                               │
│  [accent-line]          │  SLOT-ICON    │  (optional, centered)         │
│                         └───────────────┘                               │
│                                                                         │
│                   ┌─────────────────────────┐                          │
│                   │  SLOT-HEADLINE           │  (centered, H1)          │
│                   └─────────────────────────┘                          │
│                                                                         │
│                   ┌─────────────────────────┐                          │
│                   │  SLOT-SUBTITLE           │  (centered, body)        │
│                   └─────────────────────────┘                          │
│                                                                         │
│  [accent-block: bottom-left decorative element]                        │
└─────────────────────────────────────────────────────────────────────────┘
```

## Slot Specifications

| Slot | Accepts | Required | Position | Width | Height |
|---|---|---|---|---|---|
| `slot-icon` | `icon-wrapper` | no | Center, top 35% | `{{theme.spacing.xl}}` × `{{theme.spacing.xl}}` | auto |
| `slot-headline` | `text-heading` (H1) | yes | Center 40-60% vertical | 70% canvas width | auto |
| `slot-subtitle` | `text-body` | no | Center 55-70% vertical | 60% canvas width | auto |

## Background & Decoration

- Background fill: `{{theme.color.surface}}`
- Top-left accent block: `{{theme.color.primary}}` at 8% opacity, full height, 12% canvas width
- Bottom accent line: `{{theme.shape.accent-line}}`, 30% canvas width, anchored bottom-left

## Design Constraints

- `slot-headline` text wraps to maximum 2 lines; font from `{{theme.typography.heading-display}}`
- `slot-subtitle` text wraps to maximum 3 lines; font from `{{theme.typography.body}}`
- No molecule may span more than one slot
- Total visual weight: low (whitespace dominant)

## Validation Rules

- Sum of slot heights + `{{theme.spacing.xl}}` margins must not exceed canvas height
- Headline and subtitle must both be centered horizontally
- Aspect ratio must be `16:9` or `4:3` — not `A4`

## Example Usage

```yaml
template: hero-title
slots:
  slot-icon:
    atom: icon-wrapper
    params: {icon-name: "industry", fill-token: primary}
  slot-headline:
    atom: text-heading
    params: {text: "Industrial AI Summit 2025", level: h1}
  slot-subtitle:
    atom: text-body
    params: {text: "Driving transformation through intelligent automation"}
```
