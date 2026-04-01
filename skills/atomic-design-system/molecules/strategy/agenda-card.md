# Molecule: agenda-card

```yaml
id: agenda-card
type: card
description: Agenda schedule card composing multiple agenda-entry atoms in a responsive stacked layout.
tags: [agenda, schedule, program, event, list, strategy, card, layout, entry, rows]
domain: strategy
required_atoms: [agenda-entry, shape-divider]
preview: previews/molecules/strategy/agenda-card.png
```

## Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  [icon-wrapper: optional]   [text-heading: title]                  │
│ ──────────────────────────────────────── header divider ────────── │
│  [agenda-entry: label | title / description ]                      │
│  ─────────────────────────────────── entry separator ──────────────│
│  [agenda-entry: label | title / description ] ← highlighted        │
│  ─────────────────────────────────── entry separator ──────────────│
│  [agenda-entry: label | title / description ]                      │
│                                                                     │
│  (unused space when entries are fewer than available rows)          │
└────────────────────────────────────────────────────────────────────┘
```

- All `agenda-entry` rows share an identical left `label_w` for perfect column alignment.
- Row height scales with card height and entry count — more entries → shorter rows.
- The card does **not** stretch entries to fill empty space; unused space sits at the bottom.
- Each row renders a number, time, or icon label left-aligned, with title + description right.

---

## Visual Properties

Uses the standard card token vocabulary. See `references/token-reference.md §Card Instance Override Keys`.

| Property | Token |
|---|---|
| Card background | `{{theme.color.bg-card}}` via `card_bg_color()` |
| Card border | `{{theme.color.border-default}}` |
| Card radius | `ctx.rad()` |
| Header title | `{{theme.color.text-default}}` via `card_title_color()` |
| Entry label (number/time) | `{{theme.color.primary}}` |
| Entry icon tile | `{{theme.color.primary}}` (bg) / `{{theme.color.on-primary}}` (fg) |
| Entry title text | `{{theme.color.on-surface}}` |
| Entry body text | `{{theme.color.on-surface-variant}}` |
| Entry separator | `{{theme.color.line-default}}` via `card_line_color()` |
| Highlighted row | `{{theme.color.primary-container}}` tint |

---


## Parameters

| Parameter | Type | Description |
|---|---|---|
| `divider_color/divider-color` | color-token | Color token name (theme color). |
| `entries` | string | Value from props. |
| `icon` | string | Value from props. |
| `icon-name` | string | Value from props. |
| `items` | list | List of data items. |
| `label_width/label-width` | int(px)/size token | Size/spacing value (px or token). |
| `row-height` | int(px)/size token | Size/spacing value (px or token). |
| `show_dividers/show-dividers` | string | Boolean toggle (true/false). |
| `title` | string | Text string. |
## Props Schema

```yaml
title: "Agenda"                    # card header title (optional)
icon: "calendar"                   # header icon concept (optional)
entries:                           # list of agenda entries (required)
  - label_type: number             # "number" | "time" | "icon" (default: number)
    label: "01"                    # ordinal, time range, or icon concept name
    title: "Opening | Jane Smith"  # bold entry heading
    description: "Welcome remarks\nStrategic overview"  # 0–2 lines of body text
    highlight: false               # true = marks this entry as current / active

  - label_type: time
    label: "08:00–12:00"
    title: "Workshop | Group"
    description: "Hands-on session"
    highlight: true                # only one entry should be highlighted at a time

  - label_type: icon
    label: "coffee"
    title: "Coffee Break"

# ── Customisation ──────────────────────────────────────
show-dividers: true                # show separator lines between entries (default: true)
divider-color: ""                  # hex override for entry separator color
label-width: 0                     # px override for left column width (0 = auto)
row-height: 0                      # px override for each row height (0 = auto)

# ── Standard card overrides (see token-reference.md) ──
card-padding: 0                    # 0 = auto
card-header-height: 0
show-header: true
show-header-line: true
header-line-color: ""
card_bg: ""                        # filled | clean | alt | featured
title-color: ""
```

---

## Highlight Behaviour

Set `highlight: true` on exactly one entry to indicate the currently active agenda point.
A `primary-container` tint covers the full row width behind that entry's content.

Typical use: build one slide per agenda point with only the current entry highlighted.

---

## Responsive Sizing

| Variable | Auto formula | Override prop |
|---|---|---|
| Row height | `max(48, available_body_h / n_entries)` | `row-height` |
| Label column width | max of all per-entry label estimates | `label-width` |
| Label font size | `min(int(row_h × 0.50), 36)` for numbers | — |
| Time font size | `min(int(row_h × 0.24), 16)` | — |
| Icon tile size | `min(int(row_h × 0.65), label_w − 8)` | — |
| Title font size | `ctx.font_size("label")` (theme role) | — |
| Body font size | `ctx.font_size("caption")` (theme role) | — |

Row height is computed **before** the label column — ensuring both scale together.

---

## CSS Class Map

| Element | CSS Class |
|---|---|
| Card container | `.card` |
| Header title | `.u-text-on-surface .u-type-label` |
| Entry label (number) | `.u-text-primary .u-type-heading-sub` |
| Entry label (time) | `.u-text-primary .u-type-caption` |
| Icon tile bg | `.u-bg-primary` |
| Icon glyph | `.u-text-on-primary` |
| Entry title | `.u-text-on-surface .u-type-label` |
| Entry description | `.u-text-on-surface-variant .u-type-caption` |
| Row separator | `.u-border-subtle` |
| Highlight tint | `.u-bg-primary-container` |

---

## Example deck.md usage

```markdown
## Agenda
<!-- card: agenda-card -->
title: Tagesordnung
icon: "event_note"
entries:
  - label_type: number
    label: "01"
    title: "Begrüßung | Moderatorin"
    description: "Willkommen & Überblick"
  - label_type: time
    label: "09:00–11:00"
    title: "Workshop | Alle Gruppen"
    description: "Interaktive Sessions\nGruppenarbeit"
    highlight: true
  - label_type: icon
    label: "coffee"
    title: "Kaffeepause"
  - label_type: time
    label: "11:15–12:00"
    title: "Ergebnispräsentation"
    description: "Vorstellung der Resultate"
```

---

## Notes

- The parent template controls the absolute position and total size of this card.
- The first `agenda-entry` row never shows a separator above it.
- `show-dividers: false` suppresses all entry separators simultaneously.
- This molecule does **not** use a footer section; footer tokens are ignored.
