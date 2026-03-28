# Material Design 3 (Material You)

**Source:** https://m3.material.io/  
**Version:** M3 / Material You — 2024 (with M3 Expressive updates May 2025)

---

## What is Material Design 3?

Material Design 3 is Google's open-source design system. It provides an adaptive,
accessible, and expressive framework for building digital products across Android,
iOS, Flutter, and Web. M3 is built on a token-based architecture — every visual
property is expressed as a named token, enabling seamless theming via the
Material Theme Builder.

**Key philosophy:** *Personalized, adaptive, and accessible products built from
a small set of flexible, semantic color roles that ensure contrast at all times.*

---

## Core Pillars

| Pillar | Description |
|---|---|
| **Color** | 26+ semantic roles generated from a single source hue via HCT color space |
| **Typography** | 15 baseline + 15 emphasized type styles built on the Major Second scale |
| **Shape** | 6-step corner radius scale (Extra-Small → Full) with shape morphing |
| **Spacing** | 4dp grid with semantic spacing tokens |
| **Elevation** | Tonal surface colors replace shadows for depth; shadows remain optional |
| **Motion** | Physics-based spring system (Expressive & Standard schemes) |
| **Iconography** | Material Symbols — variable font with Fill, Weight, Grade, Optical Size axes |

---

## Quick Reference: Ready-to-Use Configs

| File | Theme | Background |
|---|---|---|
| `design-config.yaml` | Baseline Purple — Light | `#fffbfe` |
| `design-config-dark.yaml` | Baseline Purple — Dark | `#1c1b1f` |

---

## Core Color Roles (26 Standard)

```
Accent  →  primary / on-primary / primary-container / on-primary-container
           secondary / on-secondary / secondary-container / on-secondary-container
           tertiary / on-tertiary / tertiary-container / on-tertiary-container

Error   →  error / on-error / error-container / on-error-container

Surface →  surface / on-surface / on-surface-variant
           surface-container-lowest / -low / default / -high / -highest

Outline →  outline / outline-variant

Utility →  scrim / shadow / inverse-surface / inverse-on-surface / inverse-primary
```

See [colors.md](./colors.md) for full role definitions, pairing rules, and contrast requirements.

---

## Typography Quick Reference

| Role Token | Default Size | Weight | Use Case |
|---|---|---|---|
| `display-large` | 57sp | 400 | Hero text, numbers |
| `display-medium` | 45sp | 400 | Prominent headings |
| `display-small` | 36sp | 400 | Section headings |
| `headline-large` | 32sp | 400 | Card titles, prominent labels |
| `headline-medium` | 28sp | 400 | Sub-section headings |
| `headline-small` | 24sp | 400 | Component headings |
| `title-large` | 22sp | 400 | Top app bar, key labels |
| `title-medium` | 16sp | 500 | Navigation, emphasis |
| `title-small` | 14sp | 500 | Supporting emphasis |
| `body-large` | 16sp | 400 | Primary reading text |
| `body-medium` | 14sp | 400 | Secondary reading text |
| `body-small` | 12sp | 400 | Annotations, captions |
| `label-large` | 14sp | 500 | Buttons, interactive |
| `label-medium` | 12sp | 500 | Chips, filters |
| `label-small` | 11sp | 500 | Micro labels |

Font: Roboto (default), Roboto Flex for variable axes.

---

## Shape Scale

| Token | Corner Radius | Example Components |
|---|---|---|
| `shape-extra-small` | 4dp | Text fields, menus |
| `shape-small` | 8dp | Chips, snackbars |
| `shape-medium` | 12dp | Cards, dialogs |
| `shape-large` | 16dp | Navigation drawers |
| `shape-extra-large` | 28dp | FABs, bottom sheets |
| `shape-full` | 50% | Badges, avatar chips |

---

## Elevation Model

Unlike M2, M3 uses **tonal surface overlays** rather than drop shadows for depth.
Elevation is communicated via tone on the `surface-container-*` scale.

| Level | Surface Token | Shadow |
|---|---|---|
| 0 (Ground) | `surface` | None |
| 1 | `surface-container-low` | Optional subtle |
| 2 | `surface-container` | Optional |
| 3 | `surface-container-high` | Optional |
| 4-5 | `surface-container-highest` | Optional |

---

## Resources

- 🎨 [Material Theme Builder](https://m3.material.io/theme-builder) — generate custom palettes
- 📚 [Color System](https://m3.material.io/styles/color/system/overview)
- 📝 [Type Scale](https://m3.material.io/styles/typography/type-scale-tokens)
- 📐 [Shape System](https://m3.material.io/styles/shape)
- ✨ [Motion System](https://m3.material.io/styles/motion/overview)
- 🔤 [Material Symbols](https://fonts.google.com/icons)
