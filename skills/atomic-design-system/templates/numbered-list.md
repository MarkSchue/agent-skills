# Template: numbered-list

```yaml
id: numbered-list
type: template
description: Vertical-stack slide for presenting 3–6 numbered items with icons and short descriptions.
tags: [list, numbered, steps, process, how-to, ranking]
preview: previews/templates/numbered-list.png
canvas-size: "{{design-config.canvas}}"
max_elements: 7
compatible_aspect_ratios: ["16:9", "4:3"]
compatible_molecules: [mission-card, objective-card, role-card]
```

## Slot Definitions

```
┌─────────────────────────────────────────────────────────────────────────┐
│  [SLOT-HEADER]  full width title                                        │
├─────────────────────────────────────────────────────────────────────────┤
│  ① [SLOT-ITEM-1]  ─────────────────────── full width, compact row     │
│  ② [SLOT-ITEM-2]  ─────────────────────── full width, compact row     │
│  ③ [SLOT-ITEM-3]  ─────────────────────── full width, compact row     │
│  ④ [SLOT-ITEM-4]  ─────────────────────── (optional)                  │
│  ⑤ [SLOT-ITEM-5]  ─────────────────────── (optional)                  │
│  ⑥ [SLOT-ITEM-6]  ─────────────────────── (optional)                  │
└─────────────────────────────────────────────────────────────────────────┘
```

- Number glyph uses `{{theme.color.primary}}` fill + bold `{{theme.typography.heading}}`.
- Each item row: number · optional icon · title text · optional description text.

## Slot Specifications

| Slot | Accepts | Required | Width | Height |
|---|---|---|---|---|
| `slot-header` | `text-heading` | no | 100% | auto |
| `slot-item-1` | atom pair: `icon-wrapper` + `text-heading` + `text-body` | yes | 100% | `{{theme.spacing.xl}}` + padding |
| `slot-item-2` | same | yes | 100% | same |
| `slot-item-3` | same | yes | 100% | same |
| `slot-item-4` through `slot-item-6` | same | no | 100% | same |

- Row height auto-adjusts based on description line count
- Separator between rows: `{{theme.shape.divider}}`

## Background & Decoration

- Background: `{{theme.color.surface}}`
- Number circle fill: `{{theme.color.primary}}` at 15% opacity
- Number text: `{{theme.color.primary}}`

## Design Constraints

- Minimum 3 items required; maximum 6 before content overflows canvas
- If an item has no description, row height reduces to single-line height
- Step numbers auto-increment from 1 — do not pass numbers in content

## Validation Rules

- Total item heights + header + margins ≤ canvas height (skill warns if close to overflow)
- `slot-item-1` and `slot-item-2` and `slot-item-3` must be populated

## Example Usage

```yaml
template: numbered-list
slots:
  slot-header:
    atom: text-heading
    params: {text: "Implementation Approach", level: h2}
  slot-item-1:
    params:
      title: "Discovery & Requirements"
      description: "Stakeholder interviews, current-state mapping, gap analysis"
      icon-name: search
  slot-item-2:
    params:
      title: "Architecture Design"
      description: "System design, integration patterns, data model"
      icon-name: blueprint
  slot-item-3:
    params:
      title: "Pilot Deployment"
      description: "Single-site rollout, feedback collection, KPI baselining"
      icon-name: rocket
  slot-item-4:
    params:
      title: "Scale & Optimize"
      description: "Organization-wide rollout and continuous improvement"
      icon-name: scale
```
