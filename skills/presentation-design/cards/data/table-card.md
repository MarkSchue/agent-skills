# Table Card

Card that embeds a data table with themed header row, optional sum/total row,
alternating row shading, and full design-token control. In PowerPoint the
table is rendered as a native Excel-OLE object so formulas and in-place editing
are supported. In draw.io a standard table shape is used.

## Layout

```
┌─────────────────────────────────────────────────────┐
│  [text-label: card title]          [icon: ●]        │
│  ─────────────────────────────── (header line)      │
│  [text-caption: subtitle]                           │
│                                                     │
│  ┌───────┬───────────────┬──────────┬─────────┐     │
│  │ Col 1 │    Col 2      │  Col 3   │  Col 4  │     │  ← header row (themed)
│  ├───────┼───────────────┼──────────┼─────────┤     │
│  │  A    │   Value 1     │   123    │   45 %  │     │  ← data rows
│  │  B    │   Value 2     │   456    │   78 %  │     │  ← (opt. alternating bg)
│  │  C    │   Value 3     │   789    │   12 %  │     │
│  ├───────┼───────────────┼──────────┼─────────┤     │
│  │ Total │               │  1368    │  135 %  │     │  ← sum/total row (themed)
│  └───────┴───────────────┴──────────┴─────────┘     │
│                                                     │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  (footer line, opt.)      │
│  [text-caption: footer]      (optional, base class)  │
└─────────────────────────────────────────────────────┘
```

- The heading row uses `--card-table-heading-*` tokens for background and text.
- Data rows can optionally alternate background colour (`--card-table-stripe-*`).
- The sum/total row (last row) uses `--card-table-sum-*` tokens when
  `content.sum_row: true` is set.
- Column widths are auto-distributed by default; override with `content.col_widths`.
- In PPTX the table is embedded as a native `table` shape (python-pptx built-in)
  so that PowerPoint's full table-editing and formula toolbar are available
  when the slide is opened in PowerPoint.
- In draw.io a standard table shape with properly styled header cells is used.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `table-card` |
| `content.headers` | list[string] | Column header labels |
| `content.rows` | list[list[string]] | Table data rows (list of row lists) |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content.sum_row` | bool | `false` | Treat the last data row as a sum/total row with distinct styling |
| `content.col_widths` | list[float] | auto | Explicit column width fractions (must sum to ≤ 1.0); e.g. `[0.2, 0.4, 0.2, 0.2]` |
| `content.col_alignments` | list[string] | `left` | Per-column text alignment: `left` \| `center` \| `right` |
| `content.header_alignment` | string | — | Override alignment for ALL header cells; falls back to per-column alignment |
| `content.stripe_rows` | bool | `false` | Alternate row background colour (overrides token `--card-table-stripe-visible`) |
| `content.footer` | string | — | Source attribution or footnote text rendered at the card bottom |
| `subtitle` | string | — | Subtitle text below the header line |
| `subtitle_visible` | bool | `false` | Explicitly show/hide subtitle |
| `subtitle_alignment` | string | `left` | `left` \| `center` \| `right` |
| `icon.name` | string | `""` | Icon ligature (e.g. `"table_chart"`) |
| `icon.visible` | bool | `false` | Show/hide the title icon |
| `icon.position` | string | `right` | `left` \| `right` |
| `icon.color` | string | accent | Icon foreground color |
| `icon.size` | int | `20` | Icon size in px |

## Style Overrides

All `.card-base` tokens apply. Additionally, `.card--table` specific overrides:

### Header row
- `card_table_heading_bg_color` — header row fill colour
- `card_heading_font_color` — header text colour (base token override applies to this card only)
- `card_heading_font_size` — header font size (px)
- `card_heading_font_weight` — `normal` | `bold`
- `card_heading_font_style` — `normal` | `italic`
- `card_table_heading_alignment` — `left` | `center` | `right`
- `card_table_heading_height` — header row height (px)

### Body rows
- `card_body_font_size` — body row font size (px)
- `card_body_font_color` — body row text colour
- `card_body_font_weight` — `normal` | `bold`
- `card_body_font_style` — `normal` | `italic`
- `card_table_body_height` — body row height (px)
- `card_table_body_bg_color` — default row background colour
- `card_table_body_alignment` — default cell text alignment

### Alternating row stripe
- `card_table_stripe_visible` — `true` | `false` — enable alternating row shading
- `card_table_stripe_color` — fill colour for odd/even alternating rows

### Sum / total row
- `card_table_sum_bg_color` — sum row fill colour
- `card_table_sum_font_color` — sum row text colour
- `card_table_sum_font_size` — sum row font size (px)
- `card_table_sum_font_weight` — `normal` | `bold`
- `card_table_sum_font_style` — `normal` | `italic`
- `card_table_sum_alignment` — sum row cell alignment
- `card_table_sum_height` — sum row height (px)

### Grid lines
- `card_table_border_color` — inner and outer cell border colour
- `card_table_border_width` — border line thickness (px)
- `card_table_header_border_color` — border colour below header (overrides border_color)

### Shared
- `card_table_padding_x` — horizontal cell padding (px)
- `card_table_padding_y` — vertical cell padding (px)
- `card_table_body_min_height` — minimum row height when content grows (px)

Footer tokens (shared with all card types):
- `card_footer_font_size` / `card_footer_font_color` / `card_footer_font_weight`
- `card_footer_font_style` / `card_footer_alignment` / `card_footer_margin_top`
- `card_footer_line_visible` / `card_footer_line_color` / `card_footer_line_width`

Subtitle and icon tokens (shared with all card types):
- `card_subtitle_font_size` / `card_subtitle_font_color` / `card_subtitle_font_style`
- `card_subtitle_alignment`
- `card_icon_name` / `card_icon_position` / `card_icon_color` / `card_icon_size`

## Design Tokens Used

- `.card-base` — container, title, header line, footer, subtitle, icon
- `.card--table` — all table-specific tokens listed above

## PowerPoint Notes

In PPTX output the table is rendered as a native `GraphicFrame` table shape
(python-pptx `add_table`). Because PowerPoint's native table supports cell
formatting (fill, font), the theme tokens map directly to python-pptx cell
properties. Users can double-click the table in PowerPoint and edit data,
add formulas, or reformat cells interactively.

> **Excel OLE alternative:** If you need full spreadsheet calculation inside
> the table on the slide, set `content.excel_ole: true`. The renderer will
> fall back to representing the table data as structured text with
> formula-friendly notation in cell values (e.g. `=SUM(C2:C4)` is preserved
> as literal text) since PowerPoint OLE objects require an external Excel
> workbook binary which cannot be generated portably. For full OLE support,
> insert the Excel object manually after the build step.

## Examples

### Basic table
```yaml
type: table-card
title: "Quarterly Revenue"
content:
  headers: ["Region", "Q1", "Q2", "Q3", "Q4"]
  rows:
    - ["EMEA",   "1.2M", "1.4M", "1.6M", "1.8M"]
    - ["APAC",   "0.8M", "0.9M", "1.1M", "1.2M"]
    - ["AMER",   "2.1M", "2.3M", "2.5M", "2.8M"]
    - ["Total",  "4.1M", "4.6M", "5.2M", "5.8M"]
  sum_row: true
  col_alignments: ["left", "right", "right", "right", "right"]
```

### With alternating rows and style overrides
```yaml
type: table-card
title: "Cost Breakdown"
subtitle: "FY 2025 — all values in EUR"
icon:
  name: "table_chart"
  visible: true
  position: right
content:
  headers: ["Category", "Budget", "Actual", "Variance"]
  rows:
    - ["Personnel",    "500K", "490K",  "+10K"]
    - ["Infrastructure","200K","215K", "-15K"]
    - ["Marketing",    "150K", "140K",  "+10K"]
    - ["Total",        "850K", "845K",  "+5K"]
  sum_row: true
  stripe_rows: true
  col_widths: [0.35, 0.22, 0.22, 0.21]
  col_alignments: ["left", "right", "right", "right"]
  footer: "Source: Finance dashboard, April 2026"
style_overrides:
  card_table_header_bg_color: "#1A1A2E"
  card_table_header_font_color: "#FFFFFF"
  card_table_stripe_color: "#F3F4F6"
  card_table_sum_bg_color: "#E5E7EB"
  card_table_sum_font_weight: bold
```
