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
| `--card-title-line-color` | #E5E7EB | |
| `--card-title-line-width` | 1 | px |
| `--card-title-line-alignment` | left | |
| `--card-title-line-visible` | true | |
| `--card-footer-line-color` | #E5E7EB | footer divider line colour |
| `--card-footer-line-width` | 1 | px — footer divider thickness |
| `--card-footer-line-visible` | false | show/hide footer line (independent of footer text) |
| `--card-title-line-gap` | 8 | px — breathing room between title baseline and divider |
| `--card-subtitle-margin-top` | 6 | px — gap between header line and subtitle |
| `--card-subtitle-margin-bottom` | 8 | px — gap between subtitle and body |
| `--card-body-gap-top` | 8 | px — gap between header area and body when no subtitle is shown |
| `--card-footer-font-size` | 10 | px — footer text size |
| `--card-footer-font-color` | #9CA3AF | footer text colour |
| `--card-footer-font-weight` | 400 | footer text weight |
| `--card-footer-font-style` | normal | normal \| italic |
| `--card-footer-alignment` | left | left \| center \| right |
| `--card-footer-margin-top` | 8 | px — gap between body / line and footer |
| `--card-body-font-size` | 14 | px |
| `--card-body-font-color` | #374151 | |
| `--card-body-font-weight` | 400 | |
| `--card-body-bullet-indent` | 12 | px — left indent of bullet list items relative to body left edge |
| `--card-bullet-style` | disc | bullet marker shape: `disc` \| `circle` \| `square` \| `dash` \| `arrow` \| `none` |
| `--card-bullet-color` | var(--color-text-default) | bullet marker color (independent of body text color) |
| `--card-bullet-size` | 0 | `0` = match body font size; explicit px value for a different marker size |
| `--card-heading-line-height` | 1.3 | unitless multiplier — applied to heading font size; override per variant |
| `--card-body-line-height` | 1.3 | unitless multiplier — applied to body font size; override per variant |
| `--card-item-icon-size` | 20 | px — body/entry icon size (distinct from title icon `--card-icon-size`) |
| `--card-item-icon-gap` | 8 | px — gap between entry icon and entry text |
| `--card-item-icon-color` | var(--color-text-default) | entry icon colour; override at variant or instance level |
| `--card-item-icon-font-weight` | 700 | bold glyph weight for icon-font ligatures |
| `--card-gap-top` | 0 | px — extra space above the first item/block |
| `--card-gap-bottom` | 0 | px — extra space below the last item/block |
| `--card-gap-between` | 8 | px — spacing between items (around divider lines) |
| `--card-heading-gap` | 8 | px — gap between item heading and item body text |
| `--card-block-vertical-alignment` | top | top \| middle \| bottom — content alignment within each item slot |

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

> **Base token override pattern**
>
> Heading and body typography tokens (`--card-heading-font-*`, `--card-body-font-*`,
> `--card-label-font-*`) are defined once in `.card-base`. Each card variant class overrides
> only the values that differ from the defaults. For example, `.card--agenda` sets
> `--card-heading-font-weight: 600` to use semibold headings; all other heading font
> properties inherit from `.card-base`.
>
> In per-card `style_overrides:` YAML, use the base token names (e.g. `card_heading_font_color`,
> `card_body_font_size`) — they are scoped to that card instance only.

### KPI — `.card--kpi`
| Token | Default |
|-------|---------|
| `--card-kpi-value-font-size` | 48 |
| `--card-kpi-value-font-color` | var(--color-primary) |
| `--card-kpi-value-font-weight` | 700 |
| `--card-kpi-trend-color-up` | var(--color-success) |
| `--card-kpi-trend-color-down` | var(--color-error) |
| `--card-kpi-trend-color-neutral` | var(--color-text-muted) |
| `--card-label-font-size` | 12 | overrides base 11; slightly larger for metric context |

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

### Stacked Text — `.card--stacked-text`
| Token | Default | Description |
|-------|---------|-------------|
| `--card-heading-font-*` | *(from `.card-base`)* | Override any base heading token here to scope it to stacked-text cards. |
| `--card-body-font-*` | *(from `.card-base`)* | Override any base body token here. |
| `--card-heading-line-height` | 1.25 | unitless multiplier for heading line height (base default: 1.3) |
| `--card-body-line-height` | 1.25 | unitless multiplier for body line height (base default: 1.3) |
| `--card-stacked-text-divider-visible` | true | show/hide inter-block lines |
| `--card-stacked-text-divider-color` | var(--color-border) | divider line colour |
| `--card-stacked-text-divider-width` | 1 | px — divider thickness |
| `--card-stacked-text-divider-length-pct` | 50 | 0–100 — length as % of card body width |
| `--card-stacked-text-divider-alignment` | left | `left` \| `center` \| `right` |
| `--card-stacked-text-gap-top` | 0 | px — space above first block (uses `--card-gap-top` base token) |
| `--card-stacked-text-gap-bottom` | 0 | px — space below last block (uses `--card-gap-bottom` base token) |
| `--card-stacked-text-gap-between` | 8 | px — visual padding on each side of a divider (uses `--card-gap-between`) |
| `--card-stacked-text-heading-gap` | 8 | px — gap between heading and body within a block (uses `--card-heading-gap`) |
| `--card-stacked-text-block-vertical-alignment` | top | `top` \| `middle` \| `bottom` (uses `--card-block-vertical-alignment`) |
| `--card-stacked-text-key-takeaway-font-size` | 12 | px |
| `--card-stacked-text-key-takeaway-font-color` | var(--color-text-default) | |
| `--card-stacked-text-key-takeaway-font-weight` | 700 | bold by default |
| `--card-stacked-text-key-takeaway-font-style` | normal | |
| `--card-stacked-text-key-takeaway-alignment` | left | |
| `--card-stacked-text-key-takeaway-margin-top` | 8 | px — space between last block and key takeaway |

### Icon Item Text — `.card--icon-item-text`
| Token | Default | Description |
|-------|---------|-------------|
| `--card-heading-font-*` | *(from `.card-base`)* | Override any base heading token to scope it to icon-item-text cards. |
| `--card-body-font-*` | *(from `.card-base`)* | Override any base body token here. |
| `--card-heading-line-height` | 1.3 | unitless multiplier — inherits from `.card-base`; override here to change |
| `--card-body-line-height` | 1.3 | unitless multiplier — inherits from `.card-base`; override here to change |
| `--card-item-icon-size` | 20 | px — entry icon size (inherits from `.card-base` `--card-item-icon-size`) |
| `--card-item-icon-gap` | 8 | px — gap between icon and text area (inherits from `.card-base`) |
| `--card-item-icon-color` | var(--color-text-default) | icon colour (inherits from `.card-base`) |
| `--card-item-icon-font-weight` | 700 | icon glyph weight (inherits from `.card-base`) |
| *(icon font-family)* | var(--icon-font-family) | Always inherited from global `--icon-font-family`; no variant override needed. |
| `--card-icon-item-text-divider-visible` | true | show/hide item dividers |
| `--card-icon-item-text-divider-color` | var(--color-border) | divider line colour |
| `--card-icon-item-text-divider-width` | 1 | px — divider thickness |
| `--card-icon-item-text-divider-length-pct` | 100 | 0–100 — length as % of card width |
| `--card-icon-item-text-divider-alignment` | left | `left` \| `center` \| `right` |
| `--card-gap-top` | 0 | px — space above first item (inherits from `.card-base`) |
| `--card-gap-bottom` | 0 | px — space below last item (inherits from `.card-base`) |
| `--card-gap-between` | 8 | px — space around each item divider (inherits from `.card-base`) |
| `--card-heading-gap` | 8 | px — gap between item heading and body (inherits from `.card-base`) |
| `--card-block-vertical-alignment` | top | `top` \| `middle` \| `bottom` (inherits from `.card-base`) |

### Agenda — `.card--agenda`
| Token | Default |
|-------|---------|
| `--card-heading-font-color` | var(--color-text-subtle) | inactive heading colour (overrides base: text-default) |
| `--card-heading-font-weight` | 600 | semibold headings (overrides base: 700) |
| `--card-body-font-color` | var(--color-text-muted) | body text colour (overrides base: text-subtle) |
| `--card-agenda-active-number-color` | var(--color-primary) | highlighted col 1 — number |
| `--card-agenda-active-heading-color` | var(--color-primary) | highlighted col 2 — section title |
| `--card-agenda-active-body-color` | var(--color-text-subtle) | highlighted col 3 — info text |
| `--card-agenda-active-font-weight` | 700 |
| `--card-agenda-inactive-color` | var(--color-text-muted) |
| `--card-agenda-inactive-font-weight` | 400 |
| `--card-agenda-row-height` | 36 |
| `--card-agenda-number-font-size` | 14 |
| `--card-agenda-number-font-color` | var(--color-text-muted) |
| `--card-agenda-number-font-weight` | 400 |

---

### Scope — `.card--scope`

| Token | Default | Description |
|-------|---------|-------------|
| `--card-body-font-color` | var(--color-text-muted) | scope item body colour (overrides base: text-subtle) |
| `--card-scope-columns` | `2` | Tile columns (1–4) |
| `--card-scope-item-gap` | `12` | px — gap between tiles |
| `--card-scope-item-bg-color` | `var(--color-surface-subtle)` | Tile background fill |
| `--card-scope-item-border-color` | `var(--color-border)` | Tile border colour |
| `--card-scope-item-border-width` | `1` | px |
| `--card-scope-item-border-radius` | `4` | px — tile corner radius |
| `--card-scope-item-padding` | `12` | px — inner tile padding |
| `--card-scope-badge-size` | `20` | px — badge diameter |
| `--card-scope-badge-font-size` | `9` | px |
| `--card-scope-badge-font-color` | `#FFFFFF` | |
| `--card-scope-badge-gap` | `8` | px — gap from badge to title |
| `--card-scope-item-marker` | `number` | `number` \| `check` \| `icon` |
| `--card-scope-check-icon-name` | `check` | Material Symbols ligature |
| `--card-scope-status-in-scope-color` | `var(--color-accent)` | |
| `--card-scope-status-out-of-scope-color` | `var(--color-text-muted)` | |
| `--card-scope-status-conditional-color` | `var(--color-warning)` | |
| `--card-scope-heading-line-height` | `1.2` | uses `--card-heading-line-height` base token; base default: 1.3 |
| `--card-scope-body-margin-top` | `4` | px — gap between heading and body text |
| `--card-scope-status-label-visible` | `false` | Show status tag at tile bottom-right |
| `--card-scope-status-label-font-size` | `8` | px |
| `--card-scope-status-label-gap` | `4` | px |

### Compare — `.card--compare`

| Token | Default | Description |
|-------|---------|-------------|
| **Header row** | | |
| `--card-compare-heading-height` | `28` | px — row height of the header |
| `--card-compare-heading-bg-color` | `var(--color-primary)` | Default header cell background |
| `--card-heading-font-color` | `var(--color-text-inverse)` | Header label text colour (overrides base: text-default) |
| `--card-compare-heading-alignment` | `center` | `left` \| `center` \| `right` |
| **Highlighted column** | | |
| `--card-compare-highlight-col-heading-bg-color` | `var(--color-accent)` | Header bg for highlighted columns |
| `--card-compare-highlight-col-heading-font-color` | `#FFFFFF` | Header text for highlighted columns |
| `--card-compare-highlight-col-bg-color` | `var(--color-surface-raised)` | Data-area background for highlighted columns |
| **Topic column** | | |
| `--card-compare-label-col-visible` | `true` | Show/hide left topic column |
| `--card-compare-label-col-width-pct` | `25` | Width of topic column as % of card width |
| `--card-compare-label-col-bg-color` | `var(--color-surface-sunken)` | Topic column background |
| `--card-compare-label-col-heading-bg-color` | `var(--color-primary)` | Topic column header background |
| `--card-compare-label-col-heading-font-color` | `var(--color-text-inverse)` | Topic column header text colour |
| `--card-label-font-color` | `var(--color-text-default)` | Label text colour (overrides base: text-muted) |
| `--card-label-font-weight` | `700` | Bold labels (overrides base: 400) |
| `--card-compare-label-alignment` | `left` | |
| **Topic marker / badge** | | |
| `--card-compare-label-marker` | `none` | `none` \| `number` \| `icon` |
| `--card-compare-label-badge-shape` | `circle` | `circle` \| `square` \| `none` |
| `--card-compare-label-badge-color` | `var(--color-accent)` | Badge background fill |
| `--card-compare-label-badge-size` | `18` | px — badge width & height |
| `--card-compare-label-badge-font-size` | `8` | px — text inside badge |
| `--card-compare-label-badge-font-color` | `#FFFFFF` | Colour inside badge |
| `--card-compare-label-badge-gap` | `6` | px — gap from badge right edge to label |
| **Data cells** | | |
| *(heading/body font)* | *(from `.card-base`)* | Override `--card-body-font-*` to scope to compare cards. |
| `--card-compare-body-alignment` | `center` | `left` \| `center` \| `right` |
| `--card-compare-body-bg-color` | `transparent` | Default per-cell background (can be overridden per cell in YAML) |
| `--card-compare-body-icon-size` | `14` | px — icon element size in cells |
| `--card-compare-body-icon-color` | `var(--color-text-default)` | Default icon colour (overridable per cell) |
| `--card-compare-body-padding-x` | `6` | px — horizontal inner cell padding |
| `--card-compare-body-padding-y` | `4` | px — vertical inner cell padding |
| **Row geometry** | | |
| `--card-compare-row-height` | `32` | px — fixed data row height |
| `--card-compare-row-min-height` | `24` | px — minimum row height when auto-scaling |
| `--card-compare-row-stripe-visible` | `false` | Alternating row stripe |
| `--card-compare-row-stripe-color` | `var(--color-surface-sunken)` | |
| `--card-compare-row-separator-visible` | `true` | Horizontal lines between rows |
| `--card-compare-row-separator-color` | `var(--color-border)` | |
| `--card-compare-row-separator-width` | `1` | px |
| **Column separators** | | |
| `--card-compare-col-separator-visible` | `true` | Vertical lines between columns |
| `--card-compare-col-separator-color` | `var(--color-border)` | |
| `--card-compare-col-separator-width` | `1` | px |
| **Outer border** | | |
| `--card-compare-grid-border-visible` | `true` | Outer rect stroke |
| `--card-compare-grid-border-color` | `var(--color-border)` | |
| `--card-compare-grid-border-width` | `1` | px |
| **Summary row** | | |
| `--card-compare-summary-height` | `32` | px |
| `--card-compare-summary-bg-color` | `var(--color-primary)` | Full-width background |
| `--card-compare-summary-font-color` | `var(--color-text-inverse)` | |
| `--card-compare-summary-font-size` | `11` | px |
| `--card-compare-summary-font-weight` | `700` | |
| `--card-compare-summary-font-style` | `normal` | |
| `--card-compare-summary-alignment` | `center` | |
| `--card-compare-summary-highlight-bg-color` | `var(--color-accent)` | Accent background for cells with `highlighted: true` |
| `--card-compare-summary-highlight-font-color` | `#FFFFFF` | Text colour in highlighted summary cells |
