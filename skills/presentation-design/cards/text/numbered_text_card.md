# Numbered Text Card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

Three-column list card with an optional indicator badge (col 1), a heading (col 2),
and optional body text (col 3). Supports an active-row highlight bar, dynamic
multi-line row heights, per-column alignment, and full CSS token customisation.

## Layout

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  Card Title                                                              â”‚
â”‚  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€    â”‚
â”‚                                                                          â”‚
â”‚ â–Œ  â•­â”€â”€â”€â•®  Heading One                   Body text on the right side     â”‚ â† active row
â”‚    â”‚ 1 â”‚                                (can wrap to multiple lines)     â”‚
â”‚    â•°â”€â”€â”€â•¯                                                                 â”‚
â”‚    â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€     â”‚
â”‚    â•­â”€â”€â”€â•®  Heading Two                   More info text here              â”‚
â”‚    â”‚ 2 â”‚                                                                 â”‚
â”‚    â•°â”€â”€â”€â•¯                                                                 â”‚
â”‚    â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€     â”‚
â”‚    â•­â”€â”€â”€â•®  Heading Three                                                  â”‚
â”‚    â”‚ 3 â”‚  (no body defined â€” col 3 hidden entirely)                      â”‚
â”‚    â•°â”€â”€â”€â•¯                                                                 â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
  â•°â”€â”€â”€â”€â•´  â•°â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•´  â•°â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•´
  col 1         col 2                              col 3
  badge /     heading (main text,              body text (optional,
  icon /      h2-style, multi-line)            multi-line, right side)
  number
```

**Column visibility is automatic:** if _no_ entry in `rows` supplies a value for
`col1`, column 1 is not rendered and column 2 expands to fill the space. Likewise
column 3 only appears when at least one row has a non-empty `body` value.

Row height is _dynamic_ â€” the renderer estimates how many lines each column needs
and sizes the row to fit the taller of col 2 or col 3, plus vertical padding.
When all rows together exceed the available card body height they are scaled
proportionally.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `numbered_text_card` |
| `content.rows` | list | One entry per row (see format below) |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content.highlight` | int | â€” | 0-based index of the row to highlight with the accent bar |
| `content.footer` | string | â€” | Footer text rendered at the bottom of the card |
| `title` | string | â€” | Card header title |
| `subtitle` | string | â€” | Subtitle text below the header line |
| `icon.*` | dict | â€” | Title icon â€” same fields as all other cards (`name`, `visible`, `position`, `color`) |

### Row entry format

Each item in `content.rows` can be a plain string (treated as `heading` with an
auto-incremented numeric `col1`) or a dict:

```yaml
content:
  rows:
    - col1: "01"               # indicator text, icon ligature, or emoji
      heading: "Step One"
      body: "Describe the step in detail â€” can span multiple lines."
    - col1: "02"
      heading: "Step Two"
      body: ""                 # empty â†’ no body rendered for this row
    - "Plain string row"       # col1 auto = "3", no body
```

## Badge Shapes

Set `card_numbered_text_badge_shape` (globally via CSS or per card via
`style_overrides`) to choose how the col 1 indicator is styled:

| Shape | Description |
|-------|-------------|
| `circle` | Circular coloured disc centred in col 1 (default) |
| `square` | Equal-width square centred in col 1 |
| `rectangle` | Full-height rectangle spanning the entire col 1 width and row height |
| `none` | Plain text / icon, no background shape |

`badge_size` controls the diameter / side length for `circle` and `square`.
For `rectangle` the width is the full `col1_width_pct` and height tracks the row.

## Supported Overrides

All `.card-base` overrides plus `.card--numbered-text` tokens:

**Highlight bar (requires `content.highlight` to be set):**
- `card_numbered_text_highlight_bar_visible` â€” `true` | `false`
- `card_numbered_text_highlight_bar_color` â€” bar fill colour
- `card_numbered_text_highlight_bar_width` â€” thickness in px
- `card_numbered_text_highlight_bar_gap` â€” gap between bar and col 1 in px

**Active row text:**
- `card_numbered_text_active_col1_font_color` â€” col 1 text on active row
- `card_numbered_text_active_badge_color` â€” badge fill on active row
- `card_numbered_text_active_heading_font_color` â€” col 2 heading on active row
- `card_numbered_text_active_heading_font_weight` â€” e.g. `700`
- `card_numbered_text_active_body_font_color` â€” col 3 body on active row
- `card_numbered_text_active_font_style` â€” `normal` | `italic`

**Column 1 â€” indicator:**
- `card_numbered_text_col1_width_pct` â€” column width as % of usable row width
- `card_numbered_text_col1_alignment` â€” `left` | `center` | `right`
- `card_numbered_text_col1_font_size` â€” px
- `card_numbered_text_col1_font_color` â€” used when `badge_shape` is `none`
- `card_numbered_text_col1_font_weight`
- `card_numbered_text_col1_font_style` â€” `normal` | `italic`
- `card_numbered_text_col1_font_family` â€” set to icon font name for Material Symbols ligatures

**Column 1 badge:**
- `card_numbered_text_badge_shape` â€” `circle` | `square` | `rectangle` | `none`
- `card_numbered_text_badge_color` â€” background fill colour
- `card_numbered_text_badge_size` â€” diameter / side length in px (circle / square)
- `card_numbered_text_badge_on_color` â€” text / icon colour drawn on the badge

**Column 2 â€” heading:**
- `card_numbered_text_col2_width_pct` â€” column width as % of usable row width
- `card_numbered_text_col2_alignment` â€” `left` | `center` | `right`
- `card_heading_font_size` â€” px
- `card_heading_font_color`
- `card_heading_font_weight`
- `card_heading_font_style` â€” `normal` | `italic`
- `card_numbered_text_heading_line_height` â€” unitless multiplier (e.g. `1.3`)

**Column 3 â€” body text:**
- `card_numbered_text_col3_alignment` â€” `left` | `center` | `right`
- `card_body_font_size` â€” px
- `card_body_font_color`
- `card_body_font_weight`
- `card_body_font_style` â€” `normal` | `italic`
- `card_numbered_text_body_line_height` â€” unitless multiplier

**Row geometry:**
- `card_numbered_text_row_vertical_alignment` â€” `top` | `middle` | `bottom`
- `card_numbered_text_row_min_height` â€” minimum row height in px (0 = auto)
- `card_numbered_text_row_padding` â€” vertical padding inside each row in px
- `card_numbered_text_heading_body_gap` â€” gap between heading and body (future stacked mode) in px

**Row separators:**
- `card_numbered_text_separator_visible` â€” `true` | `false`
- `card_numbered_text_separator_color`
- `card_numbered_text_separator_width` â€” px
- `card_numbered_text_separator_inset` â€” px inset from each edge (0 = full width)

**Outer spacing:**
- `card_numbered_text_gap_top` â€” extra space above first row in px
- `card_numbered_text_gap_bottom` â€” extra space below last row in px

## Full Example

```yaml
type: numbered_text_card
title: "Implementation Roadmap"
style_overrides:
  card-numbered-text-badge-shape: circle
  card-numbered-text-badge-color: "#003087"
  card-numbered-text-badge-on-color: "#FFFFFF"
  card-numbered-text-badge-size: 30
  card-numbered-text-col1-width-pct: 12
  card-numbered-text-col2-width-pct: 40
  card-numbered-text-col2-alignment: left
  card-numbered-text-col3-alignment: left
  card-numbered-text-row-vertical-alignment: middle
  card-numbered-text-separator-visible: true
  card-heading-font-size: 13
  card-body-font-size: 11
content:
  highlight: 0
  rows:
    - col1: "01"
      heading: "Architecture Review"
      body: "Assess current integration points and define separation strategy."
    - col1: "02"
      heading: "Data Sovereignty Audit"
      body: "Classify data by residency requirements and flag cross-border flows."
    - col1: "03"
      heading: "Local Infrastructure Setup"
      body: "Provision on-premise or regional cloud nodes for SAP workloads."
    - col1: "04"
      heading: "Cutover & Validation"
      body: "Execute phased cutover with rollback plan; validate system health."
```

### Icon ligatures in col 1

```yaml
type: numbered_text_card
style_overrides:
  card-numbered-text-badge-shape: circle
  card-numbered-text-col1-font-family: "Material Symbols Outlined"
  card-numbered-text-badge-size: 32
content:
  rows:
    - col1: "check_circle"
      heading: "Completed"
      body: "This step is done."
    - col1: "pending"
      heading: "In Progress"
      body: "Currently being worked on."
    - col1: "block"
      heading: "Blocked"
      body: "Needs resolution before proceeding."
```
