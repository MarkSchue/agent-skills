# Atom: badge-status

```yaml
id: badge-status
type: badge
description: Small pill-shaped label indicating a status, category, or priority level.
tags: [badge, status, label, indicator, priority]
preview: previews/atoms/badge-status.png
```

## Visual Properties

| Property | Token |
|---|---|
| Background (success) | `{{theme.color.success}}` |
| Background (warning) | `{{theme.color.warning}}` |
| Background (error)   | `{{theme.color.error}}` |
| Background (neutral) | `{{theme.color.neutral}}` |
| Background (primary) | `{{theme.color.primary}}` |
| Label text | `{{theme.color.on-primary}}` |
| Border radius | `{{theme.borders.radius-large}}` |
| Padding H | `{{theme.spacing.s}}` |
| Padding V | `{{theme.spacing.xs}}` |
| Font | `{{theme.typography.caption}}` |

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `icon-id` | string | no |
| `text` | string | yes |
| `variant` | enum | yes |
## Behavior

- Background color is chosen from the `variant` parameter, not from a direct token reference.
- Text color is always `on-primary` (contrast-checked against variant background in theme).
- If `icon-id` is set, the icon is rendered at 12px / `{{theme.spacing.s}}` before the text.
- Do not use this atom for long labels; prefer `text-body` or `text-heading` for running copy.

## Example Usage in Molecule

```yaml
atoms:
  - id: badge-status
    role: Status
    params:
      text: "On Track"
      variant: success
```

```yaml
atoms:
  - id: badge-status
    role: Priority
    params:
      text: "High"
      variant: error
      icon-id: warning
```
