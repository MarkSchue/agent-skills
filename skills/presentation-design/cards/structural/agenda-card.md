# Agenda Card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

Auto-generated table-of-contents card listing all `#`-level sections in the deck.
Typically injected automatically by the AgendaInjector rather than authored manually.

## Layout

Single-column list. Each section is a row with three sub-columns:

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  Agenda                         [icon: â—] (opt., base)â”‚
â”‚  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€  â”‚
â”‚  [text-caption: subtitle]        (opt., base class)  â”‚
â”‚                                                      â”‚
â”‚ â–Œ  01   Introduction            30 min | Jane Doe   â”‚ â† active (bar + bold)
â”‚    02   Problem Statement        20 min | Team       â”‚
â”‚    03   Proposed Solution        40 min | John Doe   â”‚
â”‚    04   Timeline & Budget        15 min              â”‚
â”‚    05   Q & A                                        â”‚
â”‚                                                      â”‚
â”‚  â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€  (footer line, opt.)       â”‚
â”‚  [text-caption: footer]      (optional, base class)   â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
     â•°â”€â•´  â•°â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•´       â•°â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•´
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
| `content.highlight` | int | â€” | Index of current section to highlight (0-based) |
| `content.footer` | string | â€” | Source attribution or footnote text rendered at the card bottom |
| `subtitle` | string | â€” | Subtitle text below the header line |
| `subtitle_visible` | bool | `false` | Explicitly show/hide subtitle (auto-`true` when `subtitle` text is set) |
| `subtitle_alignment` | string | `left` | `left` \| `center` \| `right` |
| `icon.name` | string | `""` | Icon ligature or codepoint (e.g. `"list"` for Material Symbols Outlined) |
| `icon.visible` | bool | `false` | Show/hide the title icon |
| `icon.position` | string | `right` | `left` \| `right` â€” which side of the title row |
| `icon.color` | string | accent | Icon foreground color (hex or token) |
| `icon.size` | int | `20` | Icon size in px |

### Extended section entry format

Each entry in `content.sections` can be a plain string or a dict:

```yaml
content:
  sections:
    - title: "Introduction"
      number: "01"           # optional â€” defaults to 1-based index
      info: "30 min | Jane"  # optional â€” shown in col 3
    - "Problem Statement"    # plain string â€” number auto, no info
```

## Supported Overrides

All `.card-base` overrides plus `.card--agenda` tokens:

**Highlight bar:**
- `card_agenda_highlight_bar_visible` â€” `true` | `false` â€” show/hide the left accent bar
- `card_agenda_highlight_bar_color` â€” bar fill colour
- `card_agenda_highlight_bar_width` â€” bar thickness in px
- `card_agenda_highlight_bar_gap` â€” space (px) between bar and column 1

**Active state (applied to number + title when row is highlighted):**
- `card_agenda_active_color` â€” text colour for active row
- `card_agenda_active_font_weight` â€” font weight for active row (e.g. `700`)
- `card_agenda_active_font_style` â€” `normal` | `italic`

**Inactive state:**
- `card_agenda_inactive_color` â€” text colour for other rows
- `card_agenda_inactive_font_weight` â€” font weight for inactive rows
- `card_agenda_inactive_font_style` â€” `normal` | `italic`

**Column 1 â€” number / icon / time:**
- `card_agenda_col1_width_pct` â€” column width as % of usable row (10â€“20 recommended)
- `card_agenda_col1_alignment` â€” `left` | `center` | `right`
- `card_agenda_number_font_size` â€” font size (px)
- `card_agenda_number_font_color` â€” inactive state colour
- `card_agenda_number_font_weight` â€” font weight
- `card_agenda_number_font_style` â€” `normal` | `italic`

**Row separator (horizontal rule between entries):**
- `card_agenda_separator_visible` â€” `true` | `false` â€” show/hide the divider line between rows
- `card_agenda_separator_color` â€” line colour
- `card_agenda_separator_width` â€” line thickness in px
- `card_agenda_separator_inset` â€” horizontal inset (px) from each side edge; `0` = full card width

**Column 2 â€” section title (h2-style):**
- `card_agenda_col2_width_pct` â€” column width as % of usable row (20â€“60 recommended)
- `card_agenda_col2_alignment` â€” `left` | `center` | `right`
- `card_agenda_entry_font_size` â€” title font size (px)
- `card_agenda_entry_font_color` â€” inactive state colour
- `card_agenda_entry_font_weight` â€” semibold by default (`600`)
- `card_agenda_entry_font_style` â€” `normal` | `italic`
- `card_agenda_entry_spacing` â€” vertical gap between rows (px)

**Column 3 â€” optional info (text-body, up to 2 lines):**
- `card_agenda_col3_alignment` â€” `left` | `center` | `right`
- `card_agenda_info_font_size` â€” font size (px)
- `card_agenda_info_font_color` â€” colour
- `card_agenda_info_font_weight` â€” font weight
- `card_agenda_info_font_style` â€” `normal` | `italic`

Footer tokens (shared with all card types):
- `card_footer_font_size` â€” footer font size (px)
- `card_footer_font_color` â€” footer text color
- `card_footer_font_weight` â€” `normal` | `bold`
- `card_footer_font_style` â€” `normal` | `italic`
- `card_footer_alignment` â€” `left` | `center` | `right`
- `card_footer_margin_top` â€” space above footer text (px)
- `card_footer_line_visible` â€” `true` | `false` â€” show/hide divider above footer
- `card_footer_line_color` â€” divider color
- `card_footer_line_width` â€” divider thickness (px)

Subtitle and icon tokens (shared with all card types):
- `card_subtitle_font_size` / `card_subtitle_font_color` / `card_subtitle_font_style`
- `card_subtitle_alignment` â€” `left` | `center` | `right`
- `card_icon_name` / `card_icon_position` / `card_icon_color` / `card_icon_size`

## Design Tokens Used

- `.card-base` â€” container, title, header line, footer + footer line (`--card-footer-*`), subtitle (`--card-subtitle-*`), icon (`--card-icon-*`)
- `.card--agenda` â€” highlight bar, active/inactive row styles, three-column widths and alignments
- `.text-h2` â€” col 2 title proportions (entry font tokens default to h2-like sizes/weights)
- `.text-body` â€” col 3 info text proportions

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
  card-agenda-highlight-bar-color: "#0066CC"
  card-agenda-active-color: "#0066CC"
  card-agenda-col1-alignment: center
