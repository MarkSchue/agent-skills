# Title Slide Layout

Full-canvas title layout for section openers and deck covers.
No card slots — the entire slide body is reserved for the title, subtitle, and optional background image.

## Pictogram

```
┌─────────────────────────────────────────────────────────────────┐
│  [logo-primary]                           [logo-secondary]     │
│                                                                 │
│                                                                 │
│                                                                 │
│                                                                 │
│               [slide-title: large centered]                     │
│               [slide-subtitle: centered]                        │
│                                                                 │
│                                                                 │
│                                                                 │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  [footer-text]                              [page-number]      │
└─────────────────────────────────────────────────────────────────┘
```

## Purpose

Opening slide, section dividers, or closing slides. Draws only the slide chrome (title, subtitle, logos, footer) with no card grid.

## Card Count

0 cards. The slide body is empty or filled with a background image.

## Placement Map

| Region | Content |
|--------|---------|
| Top-left | Primary logo |
| Top-right | Secondary logo |
| Center | Title + Subtitle |
| Bottom | Footer line, footer text, page number |

## Supported Overrides

All `.slide-base` tokens, plus:
- `background` — background color or image path
- `title_color`, `title_font_size` — title styling
- `subtitle_color`, `subtitle_font_size` — subtitle styling
- `hide_footer` — suppress footer region

## Limitations

- No card slots — cards placed on a title-slide layout are ignored.
- Background image must be a single full-bleed image.

## Example

```markdown
## Welcome to Q3 Review
<!-- slide
layout: title-slide
background: "assets/images/cover-bg.jpg"
-->
```
