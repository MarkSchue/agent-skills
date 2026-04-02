# Agenda Card

Auto-generated table-of-contents card listing all `#`-level sections in the deck.
Typically injected automatically by the AgendaInjector rather than authored manually.

## Layout

Dynamic column layout based on section count:

```
1–4 sections (1 column)         5–8 sections (2 columns)
┌───────────────────────┐       ┌───────────────────────────────┐
│  [text-label: Agenda] │       │  [text-label: Agenda]         │
│  ──────────────────── │       │  ──────────────────────────── │
│                       │       │                               │
│  1. Section A         │       │  1. Section A   5. Section E  │
│  2. Section B         │       │  2. Section B   6. Section F  │
│  3. Section C         │       │  3. Section C   7. Section G  │
│  4. Section D         │       │  4. Section D   8. Section H  │
└───────────────────────┘       └───────────────────────────────┘

9+ sections (3 columns)
┌───────────────────────────────────────────┐
│  [text-label: Agenda]                     │
│  ──────────────────────────────────────── │
│                                           │
│  1. Sec A    5. Sec E    9.  Sec I        │
│  2. Sec B    6. Sec F    10. Sec J        │
│  3. Sec C    7. Sec G    11. Sec K        │
│  4. Sec D    8. Sec H    12. Sec L        │
└───────────────────────────────────────────┘
```

Current-section highlighting: the section matching the current position
is rendered in a distinct color or bold weight.

All column layouts support an optional title icon and subtitle, identical
to other card types: set `icon.name` to show an icon beside the agenda title,
and `subtitle` to add a muted line directly below the header divider.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `agenda-card` |
| `content.sections` | list | List of section titles (auto-populated) |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content.highlight` | int | — | Index of current section to highlight (0-based) |
| `content.columns` | int | auto | Force column count (1, 2, or 3) |
| `subtitle` | string | — | Subtitle text below the header line |
| `subtitle_visible` | bool | `false` | Explicitly show/hide subtitle (auto-`true` when `subtitle` text is set) |
| `icon.name` | string | `""` | Icon ligature or codepoint (e.g. `"list"` for Material Symbols Outlined) |
| `icon.visible` | bool | `false` | Show/hide the title icon |
| `icon.position` | string | `right` | `left` \| `right` — which side of the title row |
| `icon.color` | string | accent | Icon foreground color (hex or token) |
| `icon.size` | int | `20` | Icon size in px |

## Supported Overrides

All `.card-base` overrides plus `.card--agenda` tokens:
- `card_agenda_item_font_size` — section item font size
- `card_agenda_item_font_color` — section item color
- `card_agenda_highlight_font_color` — highlighted section color
- `card_agenda_highlight_font_weight` — highlighted section weight
- `card_agenda_column_gap` — gap between columns in px
- `card_agenda_number_font_color` — numbering color

Subtitle and icon tokens (shared with all card types):
- `card_subtitle_font_size` / `card_subtitle_font_color` / `card_subtitle_font_style`
- `card_icon_name` / `card_icon_position` / `card_icon_color` / `card_icon_size`

## Design Tokens Used

- `.card-base` — container, title, header line, subtitle (`--card-subtitle-*`), icon (`--card-icon-*`)
- `.card--agenda` — item styling, highlight, column layout
- `.text-body` — section item text

## Example

```yaml
type: agenda-card
subtitle: "Session overview"
icon:
  name: "list"
  position: right
content:
  sections:
    - "Introduction"
    - "Problem Statement"
    - "Proposed Solution"
    - "Timeline"
    - "Budget"
  highlight: 2
style_overrides:
  card_agenda_highlight_font_color: "#0066CC"
```
