# Template: hero-title

```yaml
id: hero-title
type: template
description: >
  Full-width hero slide with a large central title, optional subtitle, and decorative
  accent bar. Acts as a cover, section break, or intro slide.
tags: [hero, title, cover, intro, section-break]
compatible_molecules: [mission-card, quote-card, stacked-text]
```

## Layout Pictogram

```
┌──────────────────────────────────────────────────────────────────────────┐
│  [accent bar — full width, top, optional]                                │
│  [logo-primary left │ ················· │ logo-secondary right]          │
│  ──────────────────────────────────────── [header divider, optional]    │
│                                                                          │
│                                                                          │
│                   ┌──────────────────────────┐                          │
│                   │       TITLE (H1)          │                          │
│                   └──────────────────────────┘                          │
│                                                                          │
│                   ┌──────────────────────────┐                          │
│                   │    subtitle / molecule    │                          │
│                   └──────────────────────────┘                          │
│                                                                          │
│                                                                          │
│  ──────────────────────────────────────── [footer divider, optional]    │
│  [footer text left]                         [page number right]          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Slot Specifications

| Slot | Accepts | Required | Notes |
|------|---------|----------|-------|
| `title` | plain text (H1) | yes | Centred, large heading |
| `body` | any molecule or plain text | no | Centred below title |

## CSS Token Reference

All tokens live in the `:root` block of your `theme.css`.

### Slide chrome
| Token | Default | Purpose |
|-------|---------|---------|
| `--slide-bg-color` | `var(--color-surface)` | Whole-slide background fill |
| `--slide-bg-image` | `none` | Background image path / URL |
| `--logo-primary-src` | `none` | Left-logo file path |
| `--logo-primary-width` | `120` | Left-logo width (px) |
| `--logo-primary-height` | `40` | Left-logo height (px) |
| `--logo-secondary-src` | `none` | Right-logo file path (`none` = hidden) |
| `--logo-secondary-width` | `80` | Right-logo width (px) |
| `--logo-secondary-height` | `30` | Right-logo height (px) |

### Header / footer lines
| Token | Default | Purpose |
|-------|---------|---------|
| `--slide-divider-width` | `100%` | Header line span — `100%`, `50%`, or px value |
| `--slide-divider-align` | `left` | `left` \| `center` \| `right` |
| `--slide-footer-divider-width` | `100%` | Footer line span |
| `--slide-footer-divider-align` | `left` | `left` \| `center` \| `right` |

### Content area
| Token | Default | Purpose |
|-------|---------|---------|
| `--content-area-bg-color` | `transparent` | Content-zone background fill |
| `--content-area-bg-image` | `none` | Content-zone background image |
| `--content-area-padding` | `0` | Inset margin inside the content zone (px) |
| `--content-block-gap` | `24` | Gap between molecule blocks (px) |
| `--content-block-bg-color` | `transparent` | Default fill for each block |
| `--content-block-padding` | `0` | Inner padding per block (px) |

## Example Usage

```markdown
# Atomic Design System
<!-- layout: hero-title -->
subtitle: "Token-driven slide templates · PPTX + draw.io"
```
