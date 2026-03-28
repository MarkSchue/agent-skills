# Material Design 3 — Typography

**Source:** https://m3.material.io/styles/typography/overview  
**Source:** https://m3.material.io/styles/typography/type-scale-tokens

---

## Overview

M3 uses a **15-style type scale** (plus 15 emphasized counterparts in M3 Expressive).
All styles are built on the **Major Second ratio (1.125)** anchored at 14sp.

The type scale is organized into 5 role groups: Display, Headline, Title, Body, Label.
Each group has three sizes: Large, Medium, Small.

---

## Default Typeface

| Purpose | Font | Stack |
|---|---|---|
| Brand (large, expressive) | Roboto / Roboto Flex | `'Roboto', sans-serif` |
| Plain (small, readable) | Roboto | `'Roboto', sans-serif` |
| Mono | Roboto Mono | `'Roboto Mono', monospace` |

Custom typefaces can be set separately for **brand** (Display/Headline) and **plain**
(Body/Label/Title) roles — enabling expressive brand expression at large sizes while
maintaining readability at small sizes.

---

## Complete Type Scale

### Display — for hero moments, editorial, numbers at a glance

| Style | Size (sp) | Weight | Line-height | Letter-spacing | Token |
|---|---|---|---|---|---|
| Display Large | 57 | 400 | 1.12 (64sp) | -0.25 | `md.sys.typescale.display-large` |
| Display Medium | 45 | 400 | 1.15 (52sp) | 0 | `md.sys.typescale.display-medium` |
| Display Small | 36 | 400 | 1.22 (44sp) | 0 | `md.sys.typescale.display-small` |

**Use:** KPI numbers, hero statistics, splash headings. Never for body text.

### Headline — for prominent labels and page-level headings

| Style | Size (sp) | Weight | Line-height | Letter-spacing | Token |
|---|---|---|---|---|---|
| Headline Large | 32 | 400 | 1.25 (40sp) | 0 | `md.sys.typescale.headline-large` |
| Headline Medium | 28 | 400 | 1.28 (36sp) | 0 | `md.sys.typescale.headline-medium` |
| Headline Small | 24 | 400 | 1.33 (32sp) | 0 | `md.sys.typescale.headline-small` |

**Use:** Card titles, section headings, dialog titles, prominent UI labels.

### Title — for component-level headings and support labels

| Style | Size (sp) | Weight | Line-height | Letter-spacing | Token |
|---|---|---|---|---|---|
| Title Large | 22 | 400 | 1.27 (28sp) | 0 | `md.sys.typescale.title-large` |
| Title Medium | 16 | 500 | 1.50 (24sp) | +0.15 | `md.sys.typescale.title-medium` |
| Title Small | 14 | 500 | 1.43 (20sp) | +0.10 | `md.sys.typescale.title-small` |

**Use:** Top app bar text, list headers, navigation item labels.

### Body — for reading and paragraph text

| Style | Size (sp) | Weight | Line-height | Letter-spacing | Token |
|---|---|---|---|---|---|
| Body Large | 16 | 400 | 1.50 (24sp) | +0.50 | `md.sys.typescale.body-large` |
| Body Medium | 14 | 400 | 1.43 (20sp) | +0.25 | `md.sys.typescale.body-medium` |
| Body Small | 12 | 400 | 1.33 (16sp) | +0.40 | `md.sys.typescale.body-small` |

**Use:** Running text, descriptions, list item content, form helper text.

### Label — for UI control labels, captions, metadata

| Style | Size (sp) | Weight | Line-height | Letter-spacing | Token |
|---|---|---|---|---|---|
| Label Large | 14 | 500 | 1.43 (20sp) | +0.10 | `md.sys.typescale.label-large` |
| Label Medium | 12 | 500 | 1.33 (16sp) | +0.50 | `md.sys.typescale.label-medium` |
| Label Small | 11 | 500 | 1.45 (16sp) | +0.50 | `md.sys.typescale.label-small` |

**Use:** Button text, chip labels, badge text, tab labels, form field labels,
tooltip text.

---

## M3 Expressive: Emphasized Styles

Added May 2025. 15 additional styles — one per baseline style — indicated by the
`.emphasized` suffix: `md.sys.typescale.emphasized.display-large`.

Emphasized styles have:
- **Higher weight** (typically 500–700 vs. the baseline 400–500)
- Same size and line-height as their baseline counterpart
- Intended for: selected states, primary CTAs, unread indicators, editorial emphasis

```
Baseline:   md.sys.typescale.headline-large   → 32sp / wt 400
Emphasized: md.sys.typescale.emphasized.headline-large → 32sp / wt 700
```

---

## Mapping to Atomic Design System Roles

| Core system role | M3 token | Size | Notes |
|---|---|---|---|
| `heading-display` | `display-large` | 57sp | KPI numbers, hero figures |
| `heading` | `headline-large` | 32sp | Main card/slide headings |
| `heading-sub` | `headline-small` | 24sp | Sub-headings |
| `body` | `body-large` | 16sp | Body copy |
| `label` | `label-large` | 14sp | Labels, chips, table headers |
| `caption` | `label-medium` | 12sp | Captions, helper text |
| `annotation` | `label-small` | 11sp | Footnotes, metadata |

---

## Usage Rules

1. **Do not change type sizes** when customizing typography — sizes affect how
   components reflow. Change weight or font-family instead.
2. **Avoid sizes not on the scale**. If needed, extend the scale using the Major
   Second ratio: next size = current × 1.125.
3. **Line lengths**: Target 40-60 characters per line for optimal readability.
4. **Color for type**: Use `on-surface` for body text. Use `on-surface-variant`
   for secondary/hint text. Never use arbitrary hex values.
5. **Weight for hierarchy**: Use weight contrast to distinguish levels within the
   same size — especially in tight layouts.

---

## Font Size Unit Conversion

| sp | rem (at 16px root) |
|---|---|
| 11sp | 0.6875rem |
| 12sp | 0.75rem |
| 14sp | 0.875rem |
| 16sp | 1rem |
| 22sp | 1.375rem |
| 24sp | 1.5rem |
| 28sp | 1.75rem |
| 32sp | 2rem |
| 36sp | 2.25rem |
| 45sp | 2.8125rem |
| 57sp | 3.5625rem |
