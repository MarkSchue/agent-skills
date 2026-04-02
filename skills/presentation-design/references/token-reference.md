# Token Reference — CSS Design Token Catalogue

This file is the complete catalogue of all CSS design tokens available in the
presentation design system. It is auto-generated from `themes/base.css`.

---

## Token Override Priority

1. Per-card override (`style_overrides:` in card YAML)
2. Per-slide override (`<!-- slide ... -->` comment block)
3. Variant CSS class (e.g., `.card--kpi`)
4. Base CSS class (`.slide-base`, `.card-base`)
5. Python fallback default

---

## Slide Tokens — `.slide-base`

### Canvas

| Token | Default | Description |
|-------|---------|-------------|
| `--canvas-width` | 12192000 | EMU — slide width (16:9) |
| `--canvas-height` | 6858000 | EMU — slide height (16:9) |
| `--canvas-padding-top` | 48 | px — top margin |
| `--canvas-padding-right` | 48 | px — right margin |
| `--canvas-padding-bottom` | 48 | px — bottom margin |
| `--canvas-padding-left` | 48 | px — left margin |
| `--canvas-card-gap` | 16 | px — spacing between cards |
| `--canvas-background-color` | #FFFFFF | slide background color |
| `--canvas-background-image` | none | background image URL |

### Slide Title

| Token | Default | Description |
|-------|---------|-------------|
| `--slide-title-font-size` | 28 | px |
| `--slide-title-font-color` | #1A1A2E | |
| `--slide-title-font-weight` | 700 | |
| `--slide-title-background-color` | transparent | |
| `--slide-title-border-color` | transparent | |
| `--slide-title-border-width` | 0 | px |
| `--slide-title-border-radius` | 0 | px |
| `--slide-title-padding` | 0 0 8 0 | px (T R B L) |
| `--slide-title-margin` | 0 | px |
| `--slide-title-position` | top-left | |
| `--slide-title-width` | auto | |
| `--slide-title-height` | auto | |
| `--slide-title-alignment` | left | |

### Slide Subtitle

| Token | Default | Description |
|-------|---------|-------------|
| `--slide-subtitle-font-size` | 16 | px |
| `--slide-subtitle-font-color` | #6B7280 | |
| `--slide-subtitle-font-weight` | 400 | |
| `--slide-subtitle-background-color` | transparent | |
| `--slide-subtitle-border-color` | transparent | |
| `--slide-subtitle-border-width` | 0 | px |
| `--slide-subtitle-border-radius` | 0 | px |
| `--slide-subtitle-padding` | 0 | px |
| `--slide-subtitle-margin` | 4 0 0 0 | px |
| `--slide-subtitle-position` | below-title | |
| `--slide-subtitle-width` | auto | |
| `--slide-subtitle-height` | auto | |
| `--slide-subtitle-alignment` | left | |

### Title Line (Divider)

| Token | Default | Description |
|-------|---------|-------------|
| `--slide-divider-border-color` | #E5E7EB | divider line color |
| `--slide-divider-border-width` | 2 | px — thickness |
| `--slide-divider-margin` | 8 0 16 0 | px |
| `--slide-divider-width` | 100% | |
| `--slide-divider-height` | 2 | px |
| `--slide-divider-alignment` | left | |

### Primary Logo

| Token | Default | Description |
|-------|---------|-------------|
| `--slide-logo-primary-padding` | 12 | px |
| `--slide-logo-primary-position` | top-right | |
| `--slide-logo-primary-width` | 120 | px |
| `--slide-logo-primary-height` | 40 | px |

### Secondary Logo

| Token | Default | Description |
|-------|---------|-------------|
| `--slide-logo-secondary-padding` | 12 | px |
| `--slide-logo-secondary-position` | top-left | |
| `--slide-logo-secondary-width` | 120 | px |
| `--slide-logo-secondary-height` | 40 | px |

### Footer Line

| Token | Default | Description |
|-------|---------|-------------|
| `--slide-footer-line-border-color` | #E5E7EB | |
| `--slide-footer-line-border-width` | 1 | px |
| `--slide-footer-line-width` | 100% | |

### Footer Text

| Token | Default | Description |
|-------|---------|-------------|
| `--slide-footer-font-size` | 10 | px |
| `--slide-footer-font-color` | #9CA3AF | |
| `--slide-footer-position` | bottom-right | |

### Page Number

| Token | Default | Description |
|-------|---------|-------------|
| `--slide-page-number-font-size` | 10 | px |
| `--slide-page-number-font-color` | #9CA3AF | |
| `--slide-page-number-position` | bottom-left | |

---

## Card Tokens — `.card-base`

| Token | Default | Description |
|-------|---------|-------------|
| `--card-background-color` | #FFFFFF | card surface |
| `--card-border-color` | #E5E7EB | |
| `--card-border-width` | 1 | px |
| `--card-border-radius` | 8 | px |
| `--card-padding` | 16 | px |
| `--card-shadow` | 0 1 3 rgba(0,0,0,0.1) | |
| `--card-title-font-size` | 16 | px |
| `--card-title-font-color` | #1A1A2E | |
| `--card-title-font-weight` | 600 | |
| `--card-title-alignment` | left | |
| `--card-title-visible` | true | |
| `--card-header-line-color` | #E5E7EB | |
| `--card-header-line-width` | 1 | px |
| `--card-header-line-alignment` | left | |
| `--card-header-line-visible` | true | |
| `--card-footer-line-color` | #E5E7EB | |
| `--card-footer-line-width` | 1 | px |
| `--card-footer-line-visible` | false | |
| `--card-body-font-size` | 14 | px |
| `--card-body-font-color` | #374151 | |
| `--card-body-font-weight` | 400 | |

---

## Text Style Families

### Heading 1 — `.text-h1`
| Token | Default |
|-------|---------|
| `--text-h1-font-size` | 24 |
| `--text-h1-font-color` | #1A1A2E |
| `--text-h1-font-weight` | 700 |
| `--text-h1-background-color` | transparent |
| `--text-h1-italic` | false |
| `--text-h1-bold` | true |

### Heading 2 — `.text-h2`
| Token | Default |
|-------|---------|
| `--text-h2-font-size` | 20 |
| `--text-h2-font-color` | #1A1A2E |
| `--text-h2-font-weight` | 600 |
| `--text-h2-background-color` | transparent |
| `--text-h2-italic` | false |
| `--text-h2-bold` | true |

### Body — `.text-body`
| Token | Default |
|-------|---------|
| `--text-body-font-size` | 14 |
| `--text-body-font-color` | #374151 |
| `--text-body-font-weight` | 400 |
| `--text-body-background-color` | transparent |
| `--text-body-italic` | false |
| `--text-body-bold` | false |

### Caption — `.text-caption`
| Token | Default |
|-------|---------|
| `--text-caption-font-size` | 12 |
| `--text-caption-font-color` | #6B7280 |
| `--text-caption-font-weight` | 400 |

### Label — `.text-label`
| Token | Default |
|-------|---------|
| `--text-label-font-size` | 12 |
| `--text-label-font-color` | #6B7280 |
| `--text-label-font-weight` | 600 |

### Quote — `.text-quote`
| Token | Default |
|-------|---------|
| `--text-quote-font-size` | 18 |
| `--text-quote-font-color` | #374151 |
| `--text-quote-italic` | true |

### Footnote — `.text-footnote`
| Token | Default |
|-------|---------|
| `--text-footnote-font-size` | 10 |
| `--text-footnote-font-color` | #9CA3AF |

---

## Image Style Families

### Full Bleed — `.image-fullbleed`
| Token | Default |
|-------|---------|
| `--image-fullbleed-border-radius` | 0 |
| `--image-fullbleed-padding` | 0 |
| `--image-fullbleed-object-fit` | cover |

### Framed — `.image-framed`
| Token | Default |
|-------|---------|
| `--image-framed-border-color` | #E5E7EB |
| `--image-framed-border-width` | 1 |
| `--image-framed-border-radius` | 4 |
| `--image-framed-padding` | 8 |

### Circular — `.image-circular`
| Token | Default |
|-------|---------|
| `--image-circular-border-color` | #E5E7EB |
| `--image-circular-border-width` | 2 |
| `--image-circular-border-radius` | 50% |
| `--image-circular-size` | 120 |

---

## Card Variant Tokens

### KPI — `.card--kpi`
| Token | Default |
|-------|---------|
| `--card-kpi-value-font-size` | 48 |
| `--card-kpi-value-font-color` | #1A1A2E |
| `--card-kpi-value-font-weight` | 700 |
| `--card-kpi-trend-color-up` | #10B981 |
| `--card-kpi-trend-color-down` | #EF4444 |
| `--card-kpi-trend-color-neutral` | #6B7280 |
| `--card-kpi-label-font-size` | 12 |
| `--card-kpi-label-font-color` | #6B7280 |

### Chart — `.card--chart`
| Token | Default |
|-------|---------|
| `--card-chart-axis-color` | #9CA3AF |
| `--card-chart-axis-font-size` | 10 |
| `--card-chart-grid-color` | #F3F4F6 |
| `--card-chart-legend-font-size` | 11 |
| `--card-chart-legend-position` | bottom |

### Quote — `.card--quote`
| Token | Default |
|-------|---------|
| `--card-quote-mark-color` | #D1D5DB |
| `--card-quote-mark-size` | 48 |
| `--card-quote-attribution-font-size` | 12 |
| `--card-quote-attribution-font-color` | #6B7280 |

### Agenda — `.card--agenda`
| Token | Default |
|-------|---------|
| `--card-agenda-active-color` | #1A1A2E |
| `--card-agenda-active-font-weight` | 700 |
| `--card-agenda-inactive-color` | #9CA3AF |
| `--card-agenda-inactive-font-weight` | 400 |
| `--card-agenda-bullet-color` | #3B82F6 |
| `--card-agenda-entry-font-size` | 16 |
| `--card-agenda-entry-spacing` | 12 |
