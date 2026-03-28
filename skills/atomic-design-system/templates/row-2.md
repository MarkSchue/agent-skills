# Template: row-2

```yaml
id: row-2
type: template
description: >
  Two equal-height rows stacked vertically, each spanning the full content width.
  Ideal for a highlight block on top and a supporting chart or statement below.
tags: [rows, two-row, stacked, vertical]
compatible_molecules: [mission-card, chart-card, kpi-card, objective-card, stacked-text]
```

## Layout Pictogram

```
┌──────────────────────────────────────────────────────────────────────────┐
│  [accent bar]   [logo-primary]                    [logo-secondary]       │
│  SLIDE TITLE                                                             │
│  ─────────────────────────────────────────── [header divider]           │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │                                                                │     │
│  │                       BLOCK A  (row 1)                        │     │
│  │                     (50% content height)                       │     │
│  └────────────────────────────────────────────────────────────────┘     │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │                                                                │     │
│  │                       BLOCK B  (row 2)                        │     │
│  │                     (50% content height)                       │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                                                                          │
│  ─────── [footer divider]                       [page number]           │
└──────────────────────────────────────────────────────────────────────────┘
```

## Slot Specifications

| Slot | Accepts | Required | Height |
|------|---------|----------|--------|
| Block A (top) | any molecule | yes | `(content_h − gap) / 2` |
| Block B (bottom) | any molecule | no | same |

## CSS Token Reference

### Content area & blocks
| Token | Default | Purpose |
|-------|---------|---------|
| `--content-area-bg-color` | `transparent` | Content-zone background |
| `--content-area-padding` | `0` | Inset around all rows (px) |
| `--content-block-gap` | `24` | Gap between the two rows (px) |
| `--content-block-bg-color` | `transparent` | Default fill per row |
| `--content-block-padding` | `0` | Inner padding per row (px) |

(Slide-chrome and divider tokens same as `grid-2` — see that template.)

## Example Usage

```markdown
# Platform Highlights
<!-- layout: row-2 -->

## Summary
```yaml
molecule: mission-card
title: Platform Highlights
statement: "Record reliability at 99.94 % uptime this quarter."
icon-name: summarize
```

## Revenue Trend
```yaml
molecule: chart-card
chart-type: bar
title: Monthly Revenue (€ K)
labels: [Jan, Feb, Mar, Apr, May, Jun]
values: [620, 710, 680, 790, 840, 920]
```
```
