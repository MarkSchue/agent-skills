# Atom: text-heading

```yaml
id: text-heading
type: text
description: A styled heading line applying the active typography heading token and optional accent rule.
tags: [text, heading, typography, title]
preview: previews/atoms/text-heading.png
```

## Visual Properties

| Property | Token |
|---|---|
| Font / size / weight | `{{theme.typography.heading}}` |
| Color | `{{theme.color.on-surface}}` |
| Accent underline color | `{{theme.color.primary}}` |
| Accent underline thickness | `{{theme.shape.accent-line}}` |
| Margin bottom | `{{theme.spacing.s}}` |

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `accent-rule` | boolean | no |
| `align` | enum | no |
| `color-token` | color-token | no |
| `level` | enum | no |
| `text` | string | yes |
## Behavior

- Font size and weight are resolved from `{{theme.typography.heading}}` (or `heading-sub` for h3).
- `accent-rule: true` renders a short horizontal rule using `{{theme.shape.accent-line}}` color and
  `{{theme.shape.thick-line}}` stroke width beneath the text.
- No line wrapping by default; if text overflows, truncate with an ellipsis.

## Example Usage in Molecule

```yaml
atoms:
  - id: text-heading
    role: Title
    params:
      text: "Q3 Performance Review"
      level: h2
      accent-rule: true
```
