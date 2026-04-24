# Icon Item Text Card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

Text card with 1â€“5 item rows, each containing a heading, body text, and an
optional icon or label. Item icons can be placed on the left or right side of
each row, and may render as a glyph, number, or plain text.

## Layout

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  [text-label: card title]          [icon: â—]        â”‚
â”‚  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ (header line)      â”‚
â”‚  [text-caption: subtitle]                           â”‚
â”‚                                                     â”‚
â”‚  [icon] [text-h2: item 1 heading]                   â”‚
â”‚         [text-body: item 1 body text]               â”‚
â”‚                                                     â”‚
â”‚  â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€  (inter-item divider, opt.)      â”‚
â”‚                                                     â”‚
â”‚  [text-h2: item 2 heading]   [icon]                 â”‚
â”‚  [text-body: item 2 body text]                      â”‚
â”‚                                                     â”‚
â”‚  ... up to 5 items ...                              â”‚
â”‚                                                     â”‚
â”‚  â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€ â”€  (footer line, opt.)       â”‚
â”‚  [text-caption: footer]      (optional, base class)  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `icon_item_text` |
| `content.blocks` | list | List of 1â€“5 item dicts or plain strings |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content.blocks[].heading` | string | â€” | Item heading text |
| `content.blocks[].body` | string | â€” | Item body text |
| `content.blocks[].icon` | string  dict | â€” | Optional icon value, label, or glyph name |
| `content.blocks[].icon.position` | string | `left` | `left`  `right` |
| `content.blocks[].icon.color` | string | â€” | Icon/label colour |
| `content.blocks[].icon.size` | int | â€” | Icon size in px |
| `content.blocks[].icon.font_family` | string | â€” | Icon font family for glyph names |
| `content.blocks[].icon.visible` | bool | `true` | Show/hide the icon cell |
| `content.footer` | string | â€” | Footer text rendered at the card bottom |
| `subtitle` | string | â€” | Subtitle text below the header line |
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
- `card_heading_font_size` â€” heading font size (px)
- `card_heading_font_color` â€” heading text colour
- `card_heading_font_weight` â€” `400` | `600` | `700`
- `card_heading_font_style` â€” `normal` | `italic`
- `card_icon_item_text_heading_alignment` â€” `left` | `center` | `right`
- `card_icon_item_text_heading_line_height` â€” unitless multiplier

**Item body:**
- `card_body_font_size` â€” body font size (px)
- `card_body_font_color` â€” body text colour
- `card_body_font_weight` â€” `400` | `600`
- `card_body_font_style` â€” `normal` | `italic`
- `card_icon_item_text_body_alignment` â€” `left` | `center` | `right`
- `card_icon_item_text_body_line_height` â€” unitless multiplier

**Item icon:**
- `card_icon_item_text_icon_size` â€” icon width/height in px
- `card_icon_item_text_icon_gap` â€” gap between icon and text area in px
- `card_icon_item_text_icon_color` â€” default icon/label colour
- `card_icon_item_text_icon_font_family` â€” icon font family for glyphs
- `card_icon_item_text_icon_font_weight` â€” label weight for text icons

**Item divider:**
- `card_icon_item_text_divider_visible` â€” `true`  `false`
- `card_icon_item_text_divider_color` â€” divider line colour
- `card_icon_item_text_divider_width` â€” line thickness in px
- `card_icon_item_text_divider_length_pct` â€” line length as % of card width
- `card_icon_item_text_divider_alignment` â€” `left`  `center`  `right`

**Vertical spacing:**
- `card_icon_item_text_gap_top` â€” extra space above the first item (px)
- `card_icon_item_text_gap_bottom` â€” extra space below the last item (px)
- `card_icon_item_text_gap_between` â€” space around each item divider (px)
- `card_icon_item_text_heading_gap` â€” gap between heading and body text within an item (px)
- `card_body_gap_top` â€” space between the title/header area and the first item when no subtitle is present (px)
- `card_icon_item_text_block_vertical_alignment` â€” `top` | `middle` | `bottom`

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
