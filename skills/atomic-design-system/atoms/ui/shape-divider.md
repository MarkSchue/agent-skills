# Atom: shape-divider

```yaml
id: shape-divider
type: shape
description: A horizontal or vertical rule used to separate visual regions, applying a shape token.
tags: [shape, divider, separator, rule, line]
preview: previews/atoms/shape-divider.png
```

## Visual Properties

| Property | Token |
|---|---|
| Line color | Resolved from `token` parameter |
| Line width | Resolved from `token` parameter |
| Dash pattern | Resolved from `token` parameter |
| Opacity | Resolved from `token` parameter |

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `length` | token \ | percent |
| `margin-v` | token | no |
| `orientation` | enum | no |
| `token` | shape-token | yes |
## Behavior

- All visual properties (color, stroke width, dash pattern, opacity) are read from the named
  shape token in `design-config.yaml`.
- `accent-line` is a short, bold, colored rule (typically `primary`-colored, thick).
- `divider` is a subtle, full-width separator (typically `neutral`-colored, thin).
- `background-line` renders in the surface color for invisible but spaced structure.

## Standard Shape Token Characteristics

| Token | Typical use | Stroke color | Width | Dash |
|---|---|---|---|---|
| `accent-line` | Section emphasis | `primary` | thick | solid |
| `background-line` | Invisible spacer | `surface` | thin | solid |
| `thin-line` | Grid / axis | `neutral` | 1 | solid |
| `thick-line` | Strong border | `on-surface` | 3 | solid |
| `divider` | Content separation | `neutral` | 1 | solid, 30% opacity |
| `border-subtle` | Card outline | `neutral` | 1 | solid, 50% opacity |
| `border-strong` | Focus / emphasis | `primary` | 2 | solid |

## Example Usage in Molecule

```yaml
atoms:
  - id: shape-divider
    role: Divider
    params:
      token: divider
      orientation: horizontal
      margin-v: "{{theme.spacing.m}}"
```
