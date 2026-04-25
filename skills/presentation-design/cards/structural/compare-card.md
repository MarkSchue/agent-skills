---
name: compare-card
description: >
  Renders a feature/option comparison matrix with an optional left topic
  column, up to 5 comparison columns with styled headers, data cells
  containing text or icons, and an optional bottom summary row.  All colours,
  typography, separators, and badge markers are fully token-driven.
---

# compare-card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

## Layout

```
+--------------+-------------+-------------+-------------+
| (topic hdr)  |  Column A   | * Column B  |  Column C   |  ← header row
+--------------+-------------+-------------+-------------+
| ① Feature 1  |  text       |  ✓ icon     |  text       |  ← data rows
| ② Feature 2  |  Limited    |  Full       |  Full       |
+--------------+-------------+-------------+-------------+
| Conclusion   |             |  Best Pick  |             |  ← summary row
+--------------+-------------+-------------+-------------+

 *  Column B has  highlight: true  → accent background in both header and data area.
```

---

## Required fields

| Field | Description |
|-------|-------------|
| `type` | Must be `compare-card` |
| `content.columns` | List of 1–5 comparison column descriptors (each needs at least `label`) |
| `content.rows` | List of data rows; each row must have `cells` matching the column count |

---

## Optional fields

### `content.topic_col`

| Key | Type | Description |
|-----|------|-------------|
| `visible` | bool | Override `--card-compare-label-col-visible` |
| `label` | string | Header text for the topic column |
| `width_pct` | number | Override `--card-compare-label-col-width-pct` (% of card width) |

### `content.columns[]`

| Key | Type | Description |
|-----|------|-------------|
| `label` | string | Column header text |
| `highlight` | bool | Apply accent header bg + lighter data-area bg (default `false`) |

### `content.col_widths`

List of relative widths for the comparison columns (e.g. `[1, 2, 1]`).
If omitted, equal widths are used.

### `content.rows[].topic`

May be a plain string or a dict:

| Key | Type | Description |
|-----|------|-------------|
| `text` | string | Topic label text |
| `icon` | string | Material Symbols ligature — used when `--card-compare-label-marker: icon` |
| `number` | int | Explicit badge number (when `--card-compare-label-marker: number`; defaults to row index + 1) |

### `content.rows[].cells[]`

Each cell may be a **plain string** (rendered as text) or a **dict**:

| Key | Type | Description |
|-----|------|-------------|
| `value` | string | Text label |
| `icon` | string | Material Symbols ligature — renders an icon element instead of text |
| `color` | string | Override text / icon colour for this cell |
| `alignment` | string | `left` \| `center` \| `right` — override cell alignment |
| `highlighted` | bool | Used in summary rows — applies accent background |
| `bg_color` | string | Per-cell background fill override |

### `content.summary`

| Key | Type | Description |
|-----|------|-------------|
| `topic` | string | Label in topic column of summary row |
| `cells` | list | Same format as `rows[].cells[]`; `highlighted: true` applies accent bg + white text |

---

## Topic marker modes

| `--card-compare-label-marker` | Effect |
|-------------------------------|--------|
| `none` (default) | Plain topic text, no badge |
| `number` | Sequential badge (1, 2, 3 …); badge shape from `--card-compare-label-badge-shape` |
| `icon` | Per-row `topic.icon` value rendered inside badge shape |

Badge shape is controlled by `--card-compare-label-badge-shape`:
`circle` (default) · `square` · `none` (no background behind number/icon)

---

## CSS tokens

See [token-reference.md › Compare — `.card--compare`](../references/token-reference.md)
for the full list of `--card-compare-*` tokens.

---

## Example

```yaml
type: compare-card
title: Lösungsansatz Vergleich
content:
  topic_col:
    visible: true
    label: "Kriterium"
    width_pct: 28
  columns:
    - label: "Option A"
    - label: "Option B"
      highlight: true
    - label: "Option C"
  col_widths: [1, 1, 1]
  rows:
    - topic:
        text: "Kosten"
      cells:
        - value: "Niedrig"
          color: "#10B981"
        - value: "Mittel"
        - value: "Hoch"
          color: "#EF4444"
    - topic:
        text: "Datenmigration"
      cells:
        - {icon: check, color: "#10B981"}
        - {icon: check, color: "#10B981"}
        - {icon: close, color: "#EF4444"}
    - topic:
        text: "API-Zugang"
      cells:
        - value: "Vollständig"
        - value: "Vollständig"
        - value: "Eingeschränkt"
    - topic:
        text: "Support"
      cells:
        - value: "E-Mail"
        - value: "24/7"
          color: "#10B981"
        - value: "E-Mail"
  summary:
    topic: "Empfehlung"
    cells:
      - value: ""
      - value: "Optimal"
        highlighted: true
      - value: ""
```

### With numbered badges enabled (via theme or per-slide CSS)

```yaml
type: compare-card
title: Feature Matrix
# In your theme / slide CSS:
#   --card-compare-label-marker: number;
#   --card-compare-label-badge-shape: circle;
content:
  topic_col:
    visible: true
    label: "Feature"
  columns:
    - label: "Basic"
    - label: "Pro"
      highlight: true
  rows:
    - topic:
        text: "Benutzeranzahl"
      cells:
        - "Bis 10"
        - "Unbegrenzt"
    - topic:
        text: "Exportformate"
      cells:
        - {icon: close, color: "#9CA3AF"}
        - {icon: check, color: "#10B981"}
```
