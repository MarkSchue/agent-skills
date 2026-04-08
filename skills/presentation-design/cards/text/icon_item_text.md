# Icon Item Text Card

Text card with 1–5 item rows, each containing a heading, body text, and an
optional icon or label. Item icons can be placed on the left or right side of
each row, and may render as a glyph, number, or plain text.

## Layout

```
┌─────────────────────────────────────────────────────┐
│  [text-label: card title]          [icon: ●]        │
│  ─────────────────────────────── (header line)      │
│  [text-caption: subtitle]                           │
│                                                     │
│  [icon] [text-h2: item 1 heading]                   │
│         [text-body: item 1 body text]               │
│                                                     │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─  (inter-item divider, opt.)      │
│                                                     │
│  [text-h2: item 2 heading]   [icon]                 │
│  [text-body: item 2 body text]                      │
│                                                     │
│  ... up to 5 items ...                              │
│                                                     │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  (footer line, opt.)       │
│  [text-caption: footer]      (optional, base class)  │
└─────────────────────────────────────────────────────┘
```

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `icon_item_text` |
| `content.blocks` | list | List of 1–5 item dicts or plain strings |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content.blocks[].heading` | string | — | Item heading text |
| `content.blocks[].body` | string | — | Item body text |
| `content.blocks[].icon` | string  dict | — | Optional icon value, label, or glyph name |
| `content.blocks[].icon.position` | string | `left` | `left`  `right` |
| `content.blocks[].icon.color` | string | — | Icon/label colour |
| `content.blocks[].icon.size` | int | — | Icon size in px |
| `content.blocks[].icon.font_family` | string | — | Icon font family for glyph names |
| `content.blocks[].icon.visible` | bool | `true` | Show/hide the icon cell |
| `content.footer` | string | — | Footer text rendered at the card bottom |
| `subtitle` | string | — | Subtitle text below the header line |
| `subtitle_visible` | bool | `false` | Explicitly show/hide subtitle |
| `subtitle_alignment` | string | `left` | `left`  `center`  `right` |
| `icon.name` | string | `""` | Card-level title icon ligature or codepoint |
| `icon.visible` | bool | `false` | Show/hide the card title icon |
| `icon.position` | string | `right` | `left`  `right` |
| `icon.color` | string | accent | Card title icon colour |
| `icon.size` | int | `20` | Card title icon size in px |

## Supported Overrides

All `.card-base` overrides plus `.card--icon-item-text` tokens:

**Item heading:**
- `card_icon_item_text_heading_font_size` — heading font size (px)
- `card_icon_item_text_heading_font_color` — heading text colour
- `card_icon_item_text_heading_font_weight` — `400`  `600`  `700`
- `card_icon_item_text_heading_font_style` — `normal`  `italic`
- `card_icon_item_text_heading_alignment` — `left`  `center`  `right`

**Item body:**
- `card_icon_item_text_body_font_size` — body font size (px); default matches other card body text
- `card_icon_item_text_body_font_color` — body text colour
- `card_icon_item_text_body_font_weight` — `400`  `600`
- `card_icon_item_text_body_font_style` — `normal`  `italic`
- `card_icon_item_text_body_alignment` — `left`  `center`  `right`

**Item icon:**
- `card_icon_item_text_icon_size` — icon width/height in px
- `card_icon_item_text_icon_gap` — gap between icon and text area in px
- `card_icon_item_text_icon_color` — default icon/label colour
- `card_icon_item_text_icon_font_family` — icon font family for glyphs
- `card_icon_item_text_icon_font_weight` — label weight for text icons

**Item divider:**
- `card_icon_item_text_divider_visible` — `true`  `false`
- `card_icon_item_text_divider_color` — divider line colour
- `card_icon_item_text_divider_width` — line thickness in px
- `card_icon_item_text_divider_length_pct` — line length as % of card width
- `card_icon_item_text_divider_alignment` — `left`  `center`  `right`

**Vertical spacing:**
- `card_icon_item_text_gap_top` — extra space above the first item (px)
- `card_icon_item_text_gap_bottom` — extra space below the last item (px)
- `card_icon_item_text_gap_between` — space around each item divider (px)
- `card_icon_item_text_heading_gap` — gap between heading and body text within an item (px)
- `card_body_gap_top` — space between the title/header area and the first item when no subtitle is present (px)
- `card_icon_item_text_block_vertical_alignment` — `top` | `middle` | `bottom`

## Example

```yaml
type: icon_item_text
title: "Key Drivers & Challenges"
content:
  blocks:
    - icon:
        name: "trending_up"
        position: left
      heading: "Geopolitical Uncertainty"
      body: "Increasing trade restrictions raise the risk of sudden IT isolation requirements."
    - icon: "2"
      heading: "Data Sovereignty & Regulatory Pressure"
      body: "Local data storage mandates are driving a need for more decoupled architecture."
    - icon:
        text: "A"
        position: right
      heading: "Operational Dependency on Central Systems"
      body: "A central SAP system creates a single point of failure for key workflows."
```
