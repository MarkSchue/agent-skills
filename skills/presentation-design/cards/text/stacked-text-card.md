# Stacked Text Card

Multi-block text card with 2–4 equal-height content regions. Each block consists
of an h2-style heading and a body text paragraph. Divider lines between blocks are
drawn at fixed proportional positions so two cards with the same number of blocks
always align their dividers — even when one card has much shorter text.

## Layout

```
┌─────────────────────────────────────────────────────┐
│  [text-label: card title]          [icon: ●]        │
│  ─────────────────────────────── (header line)      │
│  [text-caption: subtitle]                           │
│                                                     │
│  [text-h2: block 1 heading]                         │
│  [text-body: block 1 body text]                     │
│                                                     │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─  (inter-block divider, opt.)    │
│                                                     │
│  [text-h2: block 2 heading]                         │
│  [text-body: block 2 body text]                     │
│                                                     │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─  (inter-block divider, opt.)    │
│                                                     │
│  [text-h2: block 3 heading]   (up to 4 blocks)      │
│  [text-body: block 3 body text]                     │
│                                                     │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  (footer line, opt.)      │
│  [text-caption: footer]      (optional, base class)  │
└─────────────────────────────────────────────────────┘
```

**Consistent distribution guarantee:** All `n`-block cards on a slide divide
the body area into `n` exactly equal slots. Divider lines appear at
`k/n × available_height` for `k = 1…n−1`, independent of text content.

- Icon is optional and appears on the right by default; set `icon.position: left` to flip it.
- Subtitle is optional; appears directly below the header line as muted caption text.
- Divider lines between blocks default to 50% width, matching title-line style.
- Alignment (heading, body, divider) can be set per-card or per variant class.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `stacked-text-card` |
| `content.blocks` | list | List of 2–4 block dicts or plain strings |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content.blocks[].heading` | string | — | Block heading (h2-style); omit for body-only blocks |
| `content.blocks[].body` | string | — | Block body text (text-body style) |
| `content.footer` | string | — | Source attribution or footnote text rendered at the card bottom |
| `subtitle` | string | — | Subtitle text below the header line |
| `subtitle_visible` | bool | `false` | Explicitly show/hide subtitle (auto-`true` when `subtitle` text is set) |
| `subtitle_alignment` | string | `left` | `left` \| `center` \| `right` |
| `icon.name` | string | `""` | Icon ligature or codepoint (e.g. `"format_list_bulleted"`) |
| `icon.visible` | bool | `false` | Show/hide the title icon |
| `icon.position` | string | `right` | `left` \| `right` — which side of the title row |
| `icon.color` | string | accent | Icon foreground color |
| `icon.size` | int | `20` | Icon size in px |

## Supported Overrides

All `.card-base` overrides plus `.card--stacked-text` tokens:

**Heading (h2-style — applied to every block heading):**
- `card_stacked_text_heading_font_size` — heading font size (px); default matches `.text-h2`
- `card_stacked_text_heading_font_color` — heading text color
- `card_stacked_text_heading_font_weight` — `400` | `600` | `700`
- `card_stacked_text_heading_font_style` — `normal` | `italic`
- `card_stacked_text_heading_alignment` — `left` | `center` | `right`

**Body text (text-body style — applied to every block body):**
- `card_stacked_text_body_font_size` — body font size (px); default matches `.text-body`
- `card_stacked_text_body_font_color` — body text color
- `card_stacked_text_body_font_weight` — `400` | `600`
- `card_stacked_text_body_font_style` — `normal` | `italic`
- `card_stacked_text_body_alignment` — `left` | `center` | `right`

**Inter-block divider line:**
- `card_stacked_text_divider_visible` — `true` | `false` — show/hide lines between blocks
- `card_stacked_text_divider_color` — line color (defaults to title-line color)
- `card_stacked_text_divider_width` — line thickness in px
- `card_stacked_text_divider_length_pct` — line length as % of card body width (`0`–`100`); default `50`
- `card_stacked_text_divider_alignment` — `left` | `center` | `right`

**Vertical spacing:**
- `card_stacked_text_gap_top` — extra space above the first block (px); `0` by default
- `card_stacked_text_gap_bottom` — extra space below the last block (px); `0` by default
- `card_stacked_text_gap_between` — visual space around each inter-block divider (px); default `8`
- `card_stacked_text_heading_gap` — gap between heading and body text within one block (px); default `4`

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
- `.card--stacked-text` — heading style, body style, inter-block divider, vertical gaps

## Example

```yaml
type: stacked-text-card
title: "Our Approach"
content:
  blocks:
    - heading: "Discovery"
      body: "We listen first. Two weeks of stakeholder interviews and data review."
    - heading: "Design"
      body: "Rapid prototyping with weekly feedback loops to stay aligned."
    - heading: "Delivery"
      body: "Phased rollout with embedded support for the first 90 days."
style_overrides:
  card_stacked_text_divider_length_pct: 40
  card_stacked_text_heading_alignment: left
  card_stacked_text_body_alignment: left
```

```yaml
# Two-block variant with icon and subtitle
type: stacked-text-card
title: "Performance vs. Cost"
subtitle: "Strategic trade-off analysis"
icon:
  name: "balance"
  visible: true
content:
  blocks:
    - heading: "High Performance"
      body: "Cloud-native architecture with horizontal scaling and 99.9 % SLA."
    - heading: "Cost Efficiency"
      body: "Shared services model reduces per-tenant overhead by up to 40 %."
```
