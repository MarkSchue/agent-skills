# Atom: icon-wrapper

```yaml
id: icon-wrapper
type: icon
description: Embeds an SVG icon at a specified size with theme-token fill and role annotation.
tags: [icon, svg, decorative, status]
preview: previews/atoms/icon-wrapper.png
```

## Visual Properties

| Property | Token |
|---|---|
| Fill color | `{{theme.color.primary}}` |
| Background (optional) | `{{theme.color.surface}}` |
| Size (default) | `{{theme.spacing.l}}` × `{{theme.spacing.l}}` |
| Padding | `{{theme.spacing.xs}}` |

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `download-url` | string | no |
| `fill-token` | color-token | no |
| `icon-name` | string | yes |
| `role` | string | no |
| `size` | token \ | px |
| `source` | string | yes |
## Behavior

- The SVG fill and stroke attributes are mapped to `fill-token` at assembly time.
- The source SVG file is never modified; recoloring is applied only in the output.
- If no `download-url` is provided, the skill resolves the icon from the named set.
- Multiple distinct fill colors in one SVG are mapped to separate named color tokens declared in
  the parent molecule's `atom-color-map`.

## Example Usage in Molecule

```yaml
atoms:
  - id: icon-wrapper
    role: Visual
    params:
      source: carbon
      icon-name: chart--bar
      fill-token: primary
      size: "{{theme.spacing.xl}}"
```

## Notes

- Icons are catalogued in `registry.yaml` with semantic tags for discoverability.
- Icon sets in scope for v1: Carbon, Lucide. Material is optional.
