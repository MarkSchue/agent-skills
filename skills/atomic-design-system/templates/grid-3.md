# Template: grid-3

```yaml
id: grid-3
type: template
description: Adaptive card grid that scales from two to four equally-sized columns for parallel content.
tags: [grid, adaptive, cards, parallel, overview]
preview: previews/templates/grid-3.png
canvas-size: "{{design-config.canvas}}"
max_elements: 4
compatible_aspect_ratios: ["16:9", "4:3"]
compatible_molecules: [mission-card, topic-card, kpi-card, profile-card, role-card, objective-card, location-card, contact-card, quote-card, waveform-card, dot-chart-card, daily-header-card, header-list-card]
```

## Slot Definitions

```
┌─────────────────────────────────────────────────────────────────────────┐
│  [SLOT-HEADER]  ──────────────────────────────────────── full width     │
├───────────────┬───────────────┬───────────────┬───────────────┬──────────┤
│               │               │               │               │          │
│   SLOT-A      │   SLOT-B      │   SLOT-C      │   SLOT-D      │ adaptive │
│   (equal)     │   (equal)     │   (equal)     │   (equal)     │ 2–4 cols │
│               │               │               │               │          │
│               │               │               │               │          │
└───────────────┴───────────────┴───────────────┴───────────────┴──────────┘
```

## Slot Specifications

| Slot | Accepts | Required | Width | Height |
|---|---|---|---|---|
| `slot-header` | `text-heading` | no | 100% | auto |
| `slot-a` | Any molecule | yes | adaptive | 75% canvas height |
| `slot-b` | Any molecule | no | adaptive | 75% canvas height |
| `slot-c` | Any molecule | no | adaptive | 75% canvas height |
| `slot-d` | Any molecule | no | adaptive | 75% canvas height |

- Column gutter: `{{theme.spacing.m}}`
- Outer margin: `{{design-config.canvas.margin}}`
- All populated card slots are equal height and share the available content area

## Background & Decoration

- Background: `{{theme.color.surface}}`
- Card borders provided by individual molecules' `border-subtle` tokens

## Design Constraints

- Best results come from compact cards with a consistent information density across all columns
- `topic-card` is the preferred molecule for 4-column layouts because it remains readable at narrower widths
- Slot heights are synchronized to the shared content area; shorter cards keep bottom breathing room

## Validation Rules

- `n × slot width + (n - 1) × gutter + 2 × margin ≤ canvas width`, where `n ∈ {2, 3, 4}`
- The renderer derives the column count from the number of populated molecule blocks
- More than 4 blocks are ignored by the renderer

## Example Usage

```yaml
template: grid-3
slots:
  slot-header:
    atom: text-heading
    params: {text: "Q3 Highlights", level: h2, accent-rule: true}
  slot-a:
    molecule: topic-card
    params:
      title: "Modernization"
      items:
        - {label: "Topic", text: "Upgrade packages reduce energy use and improve ride comfort."}
        - {label: "Topic", text: "Retrofit offers address ageing controller installations."}
  slot-b:
    molecule: topic-card
    params:
      title: "Service"
      items:
        - {label: "Topic", text: "Remote support workflows shorten dispatch time."}
        - {label: "Topic", text: "Predictive alerts improve first-time fix rate."}
  slot-c:
    molecule: topic-card
    params:
      title: "Digital"
      items:
        - {label: "Topic", text: "Customer apps increase transparency for building managers."}
        - {label: "Topic", text: "Usage dashboards highlight peak traffic patterns."}
  slot-d:
    molecule: topic-card
    params:
      title: "Portfolio"
      items:
        - {label: "Topic", text: "Bundled contracts simplify multi-site renewal conversations."}
        - {label: "Topic", text: "Cross-sell packages raise service penetration per account."}
```
