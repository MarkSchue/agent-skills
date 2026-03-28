# Template: comparison-2col

```yaml
id: comparison-2col
type: template
description: Two equal-width content columns for side-by-side comparison slides.
tags: [comparison, two-column, versus, decision, split]
preview: previews/templates/comparison-2col.png
canvas-size: "{{design-config.canvas}}"
max_elements: 3
compatible_aspect_ratios: ["16:9", "4:3"]
compatible_molecules: [comparison-card, mission-card, kpi-card, quote-card, objective-card]
```

## Slot Definitions

```
┌─────────────────────────────────────────────────────────────────────────┐
│  [SLOT-HEADER]  ─────────────────────────────────────── full width      │
├──────────────────────────────────┬──────────────────────────────────────┤
│                                  │                                      │
│         SLOT-LEFT                │         SLOT-RIGHT                   │
│        (45% width)               │        (45% width)                   │
│                                  │                                      │
│                                  │                                      │
└──────────────────────────────────┴──────────────────────────────────────┘
```

## Slot Specifications

| Slot | Accepts | Required | Position | Width | Height |
|---|---|---|---|---|---|
| `slot-header` | `text-heading` | no | Top, full width | 100% canvas width | auto |
| `slot-left` | Any molecule | yes | Left 45%, top margin to bottom margin | 45% | 80% canvas height |
| `slot-right` | Any molecule | yes | Right 45%, same vertical extent | 45% | 80% canvas height |

- Column gutter: `{{theme.spacing.m}}` (center divider)
- Outer margin: `{{design-config.canvas.margin}}`

## Background & Decoration

- Background: `{{theme.color.surface}}`
- Center divider: `{{theme.shape.divider}}`
- Header underline: `{{theme.shape.accent-line}}`

## Design Constraints

- Left and right slots must have identical vertical bounds
- Slot content is capped to slot height; overflow is truncated
- Use `comparison-card` molecule when both sides are feature comparisons

## Validation Rules

- `slot-left` width + gutter + `slot-right` width + 2 × margin ≤ canvas width
- Neither slot may be empty

## Example Usage

```yaml
template: comparison-2col
slots:
  slot-header:
    atom: text-heading
    params: {text: "Build vs. Buy: Automation Platform", level: h2}
  slot-left:
    molecule: comparison-card
    role: left
  slot-right:
    molecule: comparison-card
    role: right
```
