# Atom: agenda-entry

```yaml
id: agenda-entry
type: layout
description: Single horizontal agenda row with number, time, or icon label and title/description text.
tags: [agenda, schedule, list, layout, entry, row, event, program, highlight]
preview: previews/atoms/agenda-entry.png
```

## Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│ ─────────────────────── separator line (optional) ───────────────── │
│  [label: number │ time │ icon]  │  [text-heading: title]            │
│                                 │  [text-body: description line 1]  │
│                                 │  [text-body: description line 2]  │
└─────────────────────────────────────────────────────────────────────┘
```

- The left column width (`label_w`) is a **fixed, shared** value across all entries in one group
  so number, time, and icon labels all align to the same x-position regardless of variant.
- A thin horizontal separator is drawn above each row by default (`show_divider: true`).
- Highlight mode draws a `primary-container` tinted background behind the full row width to
  indicate the currently active agenda point.

---

## Visual Properties

| Property | Token | Notes |
|---|---|---|
| Label color (number / time) | `{{theme.color.primary}}` | Accent colour |
| Icon tile background | `{{theme.color.primary}}` | Same accent fill |
| Icon foreground / glyph | `{{theme.color.on-primary}}` | High-contrast glyph |
| Icon tile corner radius | `{{theme.borders.radius-medium}}` | Matches card language |
| Title text | `{{theme.color.on-surface}}` | Bold, `label` role |
| Description text | `{{theme.color.on-surface-variant}}` | Regular weight, `caption` role |
| Separator line | `{{theme.color.border-subtle}}` | 1 px horizontal rule |
| Highlight background | `{{theme.color.primary-container}}` | Light tint behind full row |

---

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `description` | string | no |
| `gap` | int (px) | no |
| `highlight` | bool | no |
| `label` | string | yes |
| `label_type` | enum | no |
| `label_w` | int (px) | yes |
| `show_divider` | bool | no |
| `title` | string | yes |
## Label Variants

### `number`
Large ordinal label (e.g. `01`) rendered in `primary` colour, vertically centred in the label
column. Font size scales with row height.

### `time`
Compact time string (e.g. `08:00–12:00`) in `primary` colour, auto-sized to fit the column
width without clipping. Use bold weight.

### `icon`
A rounded tile filled with `primary` colour, with an icon glyph in `on-primary` colour,
centred in the column.  Pass a Material/Carbon concept name as `label`
(e.g. `"coffee"`, `"arrow_forward"`, `"settings"`).

---

## Highlight

When `highlight: true` the entire row receives a `primary-container` background tint behind
every element.  This is intended for in-presentation navigation: one entry is highlighted to
show the current topic while the others remain neutral.

---

## Alignment Contract

The **parent molecule** (`agenda-card`, once implemented) is responsible for:

1. Computing `label_w` as the maximum visual width needed by any label across **all** entries.
2. Passing the **same** `label_w` and `gap` values to every `AgendaEntryAtom.render()` call.
3. Distributing row heights and y-positions so entries form a contiguous stack.

This ensures vertical alignment of labels **and** titles across all three label variants.

---

## Example Python Call

```python
from rendering.atoms import AgendaEntryAtom

atom = AgendaEntryAtom()

# Shared geometry — identical label_w for every entry in the group
label_w = 80
gap     = 16
row_h   = 70

entries = [
    dict(label_type="number", label="01",
         title="Opening | Jane Smith",
         description="Welcome remarks\nStrategic overview",
         highlight=False, show_divider=False),
    dict(label_type="time", label="08:00–12:00",
         title="Workshop | Group",
         description="Hands-on session",
         highlight=True, show_divider=True),
    dict(label_type="icon", label="coffee",
         title="Coffee Break",
         description="",
         highlight=False, show_divider=True),
]

for i, entry in enumerate(entries):
    atom.render(ctx, x, content_y + i * (row_h + 1), w, row_h,
                label_w=label_w, gap=gap, **entry)
```

---

## CSS Class Map

| Element | CSS Class | Notes |
|---|---|---|
| Row container | `.card` | Full-width, height = row_h |
| Highlight background | `.u-bg-primary-container` | Spans full row width |
| Label (number) | `.u-text-primary u-type-heading-sub` | Large, bold |
| Label (time) | `.u-text-primary u-type-caption` | Compact, bold |
| Icon tile | `.u-bg-primary` | Radius via `--radius-medium` |
| Icon glyph | `.u-text-on-primary` | Centred in tile |
| Title | `.u-text-on-surface u-type-label` | Bold |
| Description | `.u-text-on-surface-variant u-type-caption` | Regular weight |
| Separator | `.u-border-subtle` | 1 px horizontal rule |

---

## Notes

- Do not render this atom in isolation; it is designed to be stacked vertically by
  a parent `agenda-card` molecule.
- The `agenda-card` molecule (to be added) will handle row height distribution, label_w
  calculation, and the outer card container.
