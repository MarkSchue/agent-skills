# IBM Carbon Design System

**Source:** https://carbondesignsystem.com/  
**Version:** Carbon v11 — React Components ^1.103.0 (2024–2026)

---

## What is Carbon?

Carbon is IBM's open-source design system for digital products and experiences.
It provides a complete, production-ready library of components, guidelines,
patterns, and tooling built on IBM's Design Language.

**Key philosophy:** *Efficient, accessible, data-rich products built from a
rigorous, systematic approach to every visual element.*

Carbon powers IBM's product portfolio: IBM Cloud, Watson, IBM.com, and more.

---

## Core Pillars

| Pillar | Description |
|---|---|
| **Color** | Neutral gray base palette + IBM core blue. Token-based, with 4 themes |
| **Typography** | IBM Plex typeface family with productive/expressive type sets |
| **2x Grid** | 8px mini unit base. Fluid + fixed grids. 5 breakpoints |
| **Spacing** | 13-step spacing scale (2px–160px), all multiples of 8/4 |
| **Motion** | Productive + Expressive styles. 3 easing curves. 6 duration tokens |
| **Iconography** | Carbon Icons — flat, 16px/20px/24px/32px fixed-size SVG library |

---

## 4 Themes

| Theme | Background | Style |
|---|---|---|
| **White** | `#ffffff` | Light; default for most products |
| **Gray 10** | `#f4f4f4` | Light; softer, alternative light |
| **Gray 90** | `#262626` | Dark; medium dark |
| **Gray 100** | `#161616` | Dark; deepest dark, maximum contrast |

Layer model: light themes alternate White ↔ Gray 10; dark themes get one step
lighter with each layer.

---

## Quick Reference: Ready-to-Use Configs

| File | Theme | Background |
|---|---|---|
| `design-config.yaml` | White theme | `#ffffff` |
| `design-config-dark.yaml` | Gray 100 theme | `#161616` |

---

## Core Color Tokens (10 Groups)

```
background        → Page backgrounds
layer             → Stacked surface layers (layering model)
field             → Input and form backgrounds
border            → Dividers, rules, borders
text              → Type and type styles
link              → Standalone and inline link colors
icon              → Icons and pictograms
support           → Status indicators (error, warning, success, info)
focus             → Focus rings and states
skeleton          → Loading skeleton states
```

See [colors.md](./colors.md) for complete token values per theme.

---

## Typography Quick Reference

**Typeface:** IBM Plex Sans (primary), IBM Plex Serif, IBM Plex Mono

| Style | Size | Weight | Token |
|---|---|---|---|
| Productive Heading 06 | 42px | 300 | `$productive-heading-06` |
| Productive Heading 05 | 36px | 400 | `$productive-heading-05` |
| Productive Heading 04 | 28px | 400 | `$productive-heading-04` |
| Productive Heading 03 | 20px | 400 | `$productive-heading-03` |
| Productive Heading 02 | 16px | 600 | `$productive-heading-02` |
| Productive Heading 01 | 14px | 600 | `$productive-heading-01` |
| Body 02 | 16px | 400 | `$body-02` |
| Body 01 | 14px | 400 | `$body-01` |
| Label 01 | 12px | 400 | `$label-01` |
| Code 01 | 12px | 400 mono | `$code-01` |

---

## 2x Grid Quick Reference

| Breakpoint | Width | Columns | Gutter |
|---|---|---|---|
| Small (`sm`) | 320px | 4 | 0 |
| Medium (`md`) | 672px | 8 | 16px |
| Large (`lg`) | 1056px | 16 | 16px |
| X-Large (`xlg`) | 1312px | 16 | 16px |
| Max (`max`) | 1584px | 16 | 24px |

Mini unit: **8px** — all dimensions are multiples of 8px (or 4px for fine spacing).

---

## Resources

- 🏠 [Carbon homepage](https://carbondesignsystem.com/)
- 🎨 [Color tokens](https://carbondesignsystem.com/elements/color/tokens/)
- 📝 [Typography type sets](https://carbondesignsystem.com/elements/typography/type-sets/)
- 📐 [2x Grid](https://carbondesignsystem.com/elements/2x-grid/overview/)
- ✨ [Motion](https://carbondesignsystem.com/elements/motion/overview/)
- 🔤 [Carbon Icons](https://carbondesignsystem.com/elements/icons/library/)
- 📦 [GitHub: carbon-design-system/carbon](https://github.com/carbon-design-system/carbon)
