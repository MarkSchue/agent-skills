# Atom: text-body

```yaml
id: text-body
type: text
description: Multi-line body copy or bullet list applying the active body typography token.
tags: [text, body, copy, paragraph, bullets]
preview: previews/atoms/text-body.png
```

## Visual Properties

| Property | Token |
|---|---|
| Font / size / weight | `{{theme.typography.body}}` |
| Color | `{{theme.color.on-surface}}` |
| Line height | `{{theme.typography.line-height}}` |
| Bullet color | `{{theme.color.primary}}` |
| Paragraph spacing | `{{theme.spacing.s}}` |

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `color-token` | color-token | no |
| `emphasis` | `list[string]` | no |
| `format` | enum | no |
| `max-lines` | integer | no |
| `text` | `string \ | list[string]` |
## Behavior

- If `text` is a list, default format is `bullets`.
- Bullet character and spacing follow the `preset` defaults (e.g. Carbon uses `–`, Material uses `•`).
- Numbered list auto-increments; no manual numbering required.
- Bold emphasis: wrap substring with `**...**` in text; rendered using `{{theme.color.primary}}` bold.

## Example Usage in Molecule

```yaml
atoms:
  - id: text-body
    role: Body
    params:
      text:
        - "Increased revenue by 18% YoY"
        - "Expanded into 3 new markets"
        - "NPS score improved from 42 to 61"
      format: bullets
```
