# user-story-card

Structured field-grid card for writing agile user stories, SAFe features, or any
form-style template. A **Story ID badge** appears prominently in the header beside
an optional title. The content area renders a configurable N-column grid of labelled
fields — each field has a **bold label** at the top of its cell and optional value
text below.

## When to use

- User story / backlog item details during sprint reviews or planning workshops
- SAFe PI planning boards — Feature or Story cards
- Requirement templates, intake forms, or any two-column structured layout
- Job stories, JTBD canvases, or similar structured artefacts

---

## Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `id` | string | — | Story ID shown as a badge in the header (e.g. `US-042`) |
| `id-fill` | color | `primary` | ID badge background |
| `id-text-color` | color | `on-primary` | ID badge text |
| `title` | string | — | Story summary / title next to the ID badge |
| `status` | string | — | Optional status badge text (e.g. `In Review`, `Done`) |
| `status-fill` | color | `secondary` | Status badge background |
| `status-text-color` | color | `on-secondary` | Status badge text |
| `n-cols` | int 1–4 | `2` | Number of field columns |
| `fields` | list | **required** | Field objects (see below) |
| `label-color` | color | `on-surface` | Default field label color |
| `label-size` | int | auto | Field label font size in px |
| `value-color` | color | `on-surface-variant` | Default field value color |
| `value-size` | int | auto | Field value font size in px |
| `placeholder-color` | color | `on-surface-variant` | Color for `placeholder` text when `value` is empty |
| `cell-fill` | color | `bg-card` | Default cell background |
| `border-color` | color | `border-default` | Grid borders |
| `cell-pad` | int | `spacing("s")` | Cell inner padding in px |

### Field object

Each entry in `fields` is a YAML mapping:

| Key | Type | Default | Description |
|---|---|---|---|
| `label` | string | — | Bold heading at the top of the cell |
| `value` | string | — | Content text below the label |
| `placeholder` | string | — | Greyed text shown when `value` is empty |
| `span` | int | `1` | How many columns this field spans |
| `height` | float or int | auto | Row height: `0.0–1.0` = fraction of content area; `>1` = px |
| `fill` | color | card default | Per-cell background override |
| `label-color` | color | — | Per-field label color override |
| `value-color` | color | — | Per-field value color override |
| `bold-value` | bool | `false` | Bold weight for value text |
| `align` | string | `left` | Text alignment: `left` / `center` / `right` |

---

## Examples

### Minimal — custom fields

```markdown
---
molecule: user-story-card
id: US-042
title: Export reports as PDF
status: In Progress
n-cols: 2
fields:
  - label: "As a…"
    value: "finance manager"
  - label: "I want to…"
    value: "export monthly summaries as PDF"
  - label: "So that…"
    value: "I can share them with stakeholders without requiring system access"
    span: 2
    height: 0.35
  - label: "Acceptance criteria:"
    height: 0.35
    placeholder: "Given / When / Then …"
  - label: "Story points:"
    value: "5"
  - label: "Priority:"
    value: "High"
---
```

### SAFe template — all standard fields

```markdown
---
molecule: user-story-card
id: US-007
title: Real-time dashboard refresh
status: Ready
n-cols: 2
fields:
  - label: "Description:"
    value: "As a operations analyst, I want the dashboard to refresh every 30 seconds so that I always see current KPI data without manually reloading."
    height: 0.28
  - label: "Benefit hypothesis:"
    placeholder: "We believe that <outcome> will be achieved for <user> by <capability>. We will know we have succeeded when <measurable signal>."
    height: 0.28
  - label: "Nonfunctional requirements:"
    placeholder: "Performance, security, availability …"
    height: 0.28
  - label: "Acceptance criteria:"
    placeholder: "Given / When / Then …"
    height: 0.28
  - label: "User business value:"
    value: "8"
  - label: "Cost of delay:"
    value: "13"
  - label: "Time criticality:"
    value: "8"
  - label: "Job size:"
    value: "5"
  - label: "Risk reduction and/or opportunity enablement value:"
    value: "3"
  - label: "Weighted Shortest Job First (WSJF):"
    value: "5.8"
  - label: "Notes:"
    span: 2
    placeholder: "Dependencies, assumptions, open questions …"
---
```

### Minimal with theme overrides

```markdown
---
molecule: user-story-card
id: F-12
id-fill: secondary
title: Notification preferences
status: Done
status-fill: success
status-text-color: on-success
n-cols: 1
fields:
  - label: "Description:"
    value: "Users can control which notifications they receive via email, SMS, or push."
    height: 0.4
  - label: "Acceptance criteria:"
    height: 0.4
  - label: "Story points:"
    value: "3"
---
```

---

## Design notes

- **Row heights** are computed from the `height` prop on any field in a row.
  The tallest explicit height in the row wins. Rows without an explicit height
  share the remaining space equally.
- **Full-span rows** (`span: 2` in a 2-column layout) automatically span the
  full content width. Use them for Notes, criteria, or description fields.
- **Placeholder text** renders at `placeholder-color` — useful in templates
  where the content will be filled in live during a meeting.
- The **Story ID badge** uses `id-fill` / `id-text-color` and sits alongside the
  card title in the fixed-height header. The status badge floats right.
- Setting `cell-fill` to a token like `surface-container` gives a subtle
  depth to the grid while keeping borders clean.
