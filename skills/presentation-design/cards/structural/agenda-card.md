# Agenda Card

Auto-generated table-of-contents card listing all `#`-level sections in the deck.
Typically injected automatically by the AgendaInjector rather than authored manually.

## Layout

Single-column list. Each section is a row with three sub-columns:

```
┌──────────────────────────────────────────────────────┐
│  Agenda                         [icon: ●] (opt., base)│
│  ──────────────────────────────────────────────────  │
│  [text-caption: subtitle]        (opt., base class)  │
│                                                      │
│ ▌  01   Introduction            30 min | Jane Doe   │ ← active (bar + bold)
│    02   Problem Statement        20 min | Team       │
│    03   Proposed Solution        40 min | John Doe   │
│    04   Timeline & Budget        15 min              │
│    05   Q & A                                        │
│                                                      │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  (footer line, opt.)       │
│  [text-caption: footer]      (optional, base class)   │
└──────────────────────────────────────────────────────┘
     ╰─╴  ╰──────────────╴       ╰───────────────────╴
     col1        col2                    col3
   number/    section title            optional info
   icon/time   (h2-style)          (text-body, 2 lines)
```

The active section is marked with a vertical accent bar on the left edge;
its number and title are rendered in the active colour and font weight.
All other sections use the inactive colour and weight.
Column widths are controlled by percent tokens; columns align across all rows.

The card supports an optional title icon beside the heading (via `.card-base`
`--card-icon-*` tokens or the `icon:` YAML field), an optional subtitle below the
header line (via `.card-base` `--card-subtitle-*` tokens or the `subtitle:` YAML
field), an optional header divider (via `.card-base` `--card-title-line-*` tokens),
and an optional footer area (via `--card-footer-*` tokens).

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `agenda-card` |
| `content.sections` | list | List of section titles **or** dicts `{title, number, info}` (auto-populated) |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content.highlight` | int | — | Index of current section to highlight (0-based) |
| `content.footer` | string | — | Source attribution or footnote text rendered at the card bottom |
| `subtitle` | string | — | Subtitle text below the header line |
| `subtitle_visible` | bool | `false` | Explicitly show/hide subtitle (auto-`true` when `subtitle` text is set) |
| `subtitle_alignment` | string | `left` | `left` \| `center` \| `right` |
| `icon.name` | string | `""` | Icon ligature or codepoint (e.g. `"list"` for Material Symbols Outlined) |
| `icon.visible` | bool | `false` | Show/hide the title icon |
| `icon.position` | string | `right` | `left` \| `right` — which side of the title row |
| `icon.color` | string | accent | Icon foreground color (hex or token) |
| `icon.size` | int | `20` | Icon size in px |

### Extended section entry format

Each entry in `content.sections` can be a plain string or a dict:

```yaml
content:
  sections:
    - title: "Introduction"
      number: "01"           # optional — defaults to 1-based index
      info: "30 min | Jane"  # optional — shown in col 3
    - "Problem Statement"    # plain string — number auto, no info
```

## Supported Overrides

All `.card-base` overrides plus `.card--agenda` tokens:

**Highlight bar:**
- `card_agenda_highlight_bar_visible` — `true` | `false` — show/hide the left accent bar
- `card_agenda_highlight_bar_color` — bar fill colour
- `card_agenda_highlight_bar_width` — bar thickness in px
- `card_agenda_highlight_bar_gap` — space (px) between bar and column 1

**Active state (applied to number + title when row is highlighted):**
- `card_agenda_active_color` — text colour for active row
- `card_agenda_active_font_weight` — font weight for active row (e.g. `700`)
- `card_agenda_active_font_style` — `normal` | `italic`

**Inactive state:**
- `card_agenda_inactive_color` — text colour for other rows
- `card_agenda_inactive_font_weight` — font weight for inactive rows
- `card_agenda_inactive_font_style` — `normal` | `italic`

**Column 1 — number / icon / time:**
- `card_agenda_col1_width_pct` — column width as % of usable row (10–20 recommended)
- `card_agenda_col1_alignment` — `left` | `center` | `right`
- `card_agenda_number_font_size` — font size (px)
- `card_agenda_number_font_color` — inactive state colour
- `card_agenda_number_font_weight` — font weight
- `card_agenda_number_font_style` — `normal` | `italic`

**Row separator (horizontal rule between entries):**
- `card_agenda_separator_visible` — `true` | `false` — show/hide the divider line between rows
- `card_agenda_separator_color` — line colour
- `card_agenda_separator_width` — line thickness in px
- `card_agenda_separator_inset` — horizontal inset (px) from each side edge; `0` = full card width

**Column 2 — section title (h2-style):**
- `card_agenda_col2_width_pct` — column width as % of usable row (20–60 recommended)
- `card_agenda_col2_alignment` — `left` | `center` | `right`
- `card_agenda_entry_font_size` — title font size (px)
- `card_agenda_entry_font_color` — inactive state colour
- `card_agenda_entry_font_weight` — semibold by default (`600`)
- `card_agenda_entry_font_style` — `normal` | `italic`
- `card_agenda_entry_spacing` — vertical gap between rows (px)

**Column 3 — optional info (text-body, up to 2 lines):**
- `card_agenda_col3_alignment` — `left` | `center` | `right`
- `card_agenda_info_font_size` — font size (px)
- `card_agenda_info_font_color` — colour
- `card_agenda_info_font_weight` — font weight
- `card_agenda_info_font_style` — `normal` | `italic`

Footer tokens (shared with all card types):
- `card_footer_font_size` — footer font size (px)
- `card_footer_font_color` — footer text color
- `card_footer_font_weight` — `normal` | `bold`
- `card_footer_font_style` — `normal` | `italic`
- `card_footer_alignment` — `left` | `center` | `right`
- `card_footer_margin_top` — space above footer text (px)
- `card_footer_line_visible` — `true` | `false` — show/hide divider above footer
- `card_footer_line_color` — divider color
- `card_footer_line_width` — divider thickness (px)

Subtitle and icon tokens (shared with all card types):
- `card_subtitle_font_size` / `card_subtitle_font_color` / `card_subtitle_font_style`
- `card_subtitle_alignment` — `left` | `center` | `right`
- `card_icon_name` / `card_icon_position` / `card_icon_color` / `card_icon_size`

## Design Tokens Used

- `.card-base` — container, title, header line, footer + footer line (`--card-footer-*`), subtitle (`--card-subtitle-*`), icon (`--card-icon-*`)
- `.card--agenda` — highlight bar, active/inactive row styles, three-column widths and alignments
- `.text-h2` — col 2 title proportions (entry font tokens default to h2-like sizes/weights)
- `.text-body` — col 3 info text proportions

## Example

```yaml
type: agenda-card
subtitle: "Session overview"
content:
  sections:
    - title: "Introduction"
      number: "01"
      info: "30 min"
    - title: "Problem Statement"
      number: "02"
      info: "20 min"
    - title: "Proposed Solution"
      number: "03"
      info: "40 min"
    - title: "Q & A"
      number: "04"
  highlight: 2
style_overrides:
  card_agenda_highlight_bar_color: "#0066CC"
  card_agenda_active_color: "#0066CC"
  card_agenda_col1_alignment: center
