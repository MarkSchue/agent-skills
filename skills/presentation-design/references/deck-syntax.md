# Deck Syntax — Presentation Definition Format

This document defines the structured Markdown syntax for `presentation-definition.md`.

---

## Structure Hierarchy

```
# Section Title          → agenda entry + section grouping
## Slide Title           → one slide
<!-- DONE -->            → (optional) freeze this slide
<!-- slide ... -->       → (optional) per-slide overrides
### Card Title           → one card on the slide
```yaml
type: card-type
content: ...
style_overrides: ...
```​
```

---

## Sections — `#`

Each `#` heading creates a **section** and an **agenda entry**. Sections group
slides logically and drive the automatic agenda injection system.

```markdown
# Introduction
# Key Results
# Next Steps
```

---

## Slides — `##`

Each `##` heading creates a **slide**. The heading text becomes the slide title.

```markdown
## Welcome to the Team
## Q3 Revenue Summary
```

### Frozen slides — `<!-- DONE -->`

Place `<!-- DONE -->` on the line immediately below `##` to mark a slide as
frozen. The renderer will never modify frozen slides.

```markdown
## Final Approved Slide
<!-- DONE -->
### Revenue Chart
...
```

### Per-slide overrides — `<!-- slide ... -->`

Place a YAML comment block below `##` (after `<!-- DONE -->` if present) to
override slide-level CSS tokens for this specific slide.

```markdown
## Custom Background Slide
<!-- slide
background: "#F0F4F8"
title_color: "#003087"
hide_footer: true
hide_page_number: false
-->
### Card Title
...
```

Supported per-slide override keys:
| Key | Type | Description |
|-----|------|-------------|
| `background` | string | Slide background color (hex) |
| `background_image` | string | Path to background image |
| `title_color` | string | Slide title font color |
| `title_size` | int | Slide title font size (px) |
| `title_alignment` | string | left \| center \| right |
| `hide_footer` | bool | Hide footer text |
| `hide_page_number` | bool | Hide page number |
| `hide_divider` | bool | Hide title divider line |
| `hide_logo_primary` | bool | Hide primary logo |
| `hide_logo_secondary` | bool | Hide secondary logo |

---

## Cards — `###`

Each `###` heading creates a **card** on the current slide. The heading text
becomes the card title.

Below the heading, include a fenced YAML code block with the card definition:

```markdown
### Our Mission
```yaml
type: text-card
content:
  heading: "Building the Future"
  body: "We are committed to innovation and excellence."
  bullets:
    - "Customer-first approach"
    - "Data-driven decisions"
style_overrides:
  card_background: "#F8FAFC"
  header_line_color: "#3B82F6"
```​
```

### Card YAML schema

Every card YAML block normalizes to this schema:

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `type` | yes | string | Card type identifier (e.g. `text-card`) |
| `content` | yes | object | Card-specific content fields |
| `subtitle` | no | string | Subtitle text displayed below the header line |
| `icon` | no | object | Title icon config: `{ name, position, color, size, visible }` |
| `style_overrides` | no | object | Per-card CSS token overrides |
| `asset_refs` | no | list | Relative paths to assets used by this card |

### Per-card override keys

| Key | Type | Description |
|-----|------|-------------|
| `card_background` | string | Card background color |
| `card_border_color` | string | Card border color |
| `card_border_radius` | int | Card border radius (px) |
| `card_padding` | int | Card inner padding (px) |
| `title_visible` | bool | Show/hide card title |
| `title_alignment` | string | left \| center \| right |
| `header_line_visible` | bool | Show/hide header divider |
| `header_line_color` | string | Header divider color |
| `header_line_width` | int | Header divider thickness (px) |
| `footer_line_visible` | bool | Show/hide footer divider |
| `subtitle_visible` | bool | Show/hide subtitle below header line |
| `subtitle_font_color` | string | Subtitle text color |
| `subtitle_font_size` | int | Subtitle font size (px) |
| `subtitle_font_style` | string | `normal` \| `italic` |
| `icon_visible` | bool | Show/hide icon next to card title |
| `icon_name` | string | Icon ligature or Unicode codepoint (e.g. `"bar_chart"`) |
| `icon_position` | string | `left` \| `right` |
| `icon_color` | string | Icon foreground color |
| `icon_size` | int | Icon size in px |
| `icon_background_color` | string | Icon badge background color |

---

## Layout selection

The layout for each slide is determined automatically by the number of `###`
cards on the slide:
- 0 cards → `title-slide`
- 1 card → `grid-1x1`
- 2 cards → `grid-1x2`
- 3 cards → `grid-1x3`
- 4 cards → `grid-2x2`
- 6 cards → `grid-2x3`

Override the auto-selected layout with a `<!-- layout: grid-3x3 -->` comment
below the `##` heading.

---

## Complete example

```markdown
# Introduction

## Welcome
### Greeting
```yaml
type: text-card
content:
  heading: "Hello, World"
  body: "Welcome to our presentation."
```​

# Key Metrics

## Revenue Dashboard
### Q3 Revenue
```yaml
type: kpi-card
content:
  value: "$4.2M"
  trend: "up"
  label: "vs Q2"
```​

### Customer Growth
```yaml
type: kpi-card
content:
  value: "12,500"
  trend: "up"
  label: "Active users"
```​
```
