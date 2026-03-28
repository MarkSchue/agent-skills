# Material Design 3 — Color System

**Source:** https://m3.material.io/styles/color/system/overview  
**Source:** https://m3.material.io/styles/color/roles

---

## How the Color System Works

M3 uses the **HCT color space** (Hue-Chroma-Tone) — a perceptually accurate space
that guarantees harmonic relationships. Every scheme is generated from one or more
source hues. The system algorithmically creates all 26+ roles from those hues,
ensuring accessible contrast ratios by construction.

```
Source hue → Tonal palette (tone 0–100) → Color roles mapped to tones
```

The same role tokenss are used in both light and dark themes — only the assigned
tone changes. This ensures components look intentional in both modes.

---

## Color Role Groups (26 standard roles)

### 1. Primary Group
Highest-emphasis elements: FABs, prominent buttons, active states.

| Role | Light | Dark | Use |
|---|---|---|---|
| `primary` | #6750a4 | #d0bcff | Fill for most important actions |
| `on-primary` | #ffffff | #381e72 | Text/icons on primary |
| `primary-container` | #eaddff | #4f378b | FAB container, active chip |
| `on-primary-container` | #21005d | #eaddff | Text/icons on primary-container |

### 2. Secondary Group
Less prominent elements: filter chips, inactive nav icons.

| Role | Light | Dark | Use |
|---|---|---|---|
| `secondary` | #625b71 | #cbc2db | Low-emphasis fills |
| `on-secondary` | #ffffff | #332d41 | Text/icons on secondary |
| `secondary-container` | #e8def8 | #4a4458 | Tonal button, recessive fill |
| `on-secondary-container` | #1d192b | #e8def8 | Text/icons on secondary-container |

### 3. Tertiary Group
Complementary accent, optional special emphasis: badges, call-outs.

| Role | Light | Dark | Use |
|---|---|---|---|
| `tertiary` | #7d5260 | #efb8c8 | Complementary fills |
| `on-tertiary` | #ffffff | #492532 | Text/icons on tertiary |
| `tertiary-container` | #ffd8e4 | #633b48 | Complementary container |
| `on-tertiary-container` | #31111d | #ffd8e4 | Text/icons on tertiary-container |

### 4. Error Group
Always static (does not adapt dynamically). Communicates error states.

| Role | Light | Dark | Use |
|---|---|---|---|
| `error` | #b3261e | #f2b8b5 | Error fill, text, icons |
| `on-error` | #ffffff | #601410 | Text/icons on error |
| `error-container` | #f9dedc | #8c1d18 | Error container background |
| `on-error-container` | #410e0b | #f9dedc | Text/icons on error-container |

### 5. Surface Group
Neutral backgrounds and containers for the overall UI structure.

| Role | Light | Dark | Use |
|---|---|---|---|
| `surface` | #fffbfe | #1c1b1f | Default page background |
| `on-surface` | #1c1b1f | #e6e1e5 | Primary text and icons |
| `on-surface-variant` | #49454f | #cac4d0 | Secondary/hint text |
| `surface-variant` | #e7e0ec | #49454f | Alternative surface |
| `surface-container-lowest` | #ffffff | #0f0d13 | Elevation 0 (flat) |
| `surface-container-low` | #f7f2fa | #1d1b20 | Elevated card (lv 1) |
| `surface-container` | #f3edf7 | #211f26 | Navigation, menus (lv 2) |
| `surface-container-high` | #ece6f0 | #2b2930 | Dialogs, FAB (lv 3) |
| `surface-container-highest` | #e6e0e9 | #36343b | Top sheets (lv 4-5) |

### 6. Outline Group

| Role | Light | Dark | Use |
|---|---|---|---|
| `outline` | #79747e | #938f99 | Text field borders, important dividers (3:1 contrast) |
| `outline-variant` | #cac4d0 | #49454f | Decorative dividers (not for interaction boundaries) |

---

## Color Pairing Rules

> **Golden rule:** Always use the `on-*` counterpart of any fill color for text
> and icons. Never pair two arbitrary colors — use only the designed pairs.

| Fill | Text/Icons on top |
|---|---|
| `primary` | `on-primary` |
| `primary-container` | `on-primary-container` |
| `secondary` | `on-secondary` |
| `secondary-container` | `on-secondary-container` |
| `tertiary` | `on-tertiary` |
| `tertiary-container` | `on-tertiary-container` |
| `error` | `on-error` |
| `error-container` | `on-error-container` |
| `surface` / any surface-container | `on-surface` or `on-surface-variant` |
| `inverse-surface` | `inverse-on-surface` |

---

## Contrast Requirements (WCAG)

| Pair | Minimum contrast | Required for |
|---|---|---|
| Any fill + its `on-*` | 4.5:1 | Small text (< 18sp) |
| Fill + `on-*` for large text | 3:1 | Text ≥ 18sp / bold ≥ 14sp |
| `outline` vs surface | 3:1 | Interactive boundaries |
| `outline-variant` vs surface | < 3:1 | Decorative only |

---

## Dynamic Color vs Baseline Scheme

| Mode | How it works |
|---|---|
| **Baseline** | Fixed colors. Good for products with a fixed brand identity. |
| **Content-based** | Colors derived from a local image (album art, product photo). |
| **User-generated** | Colors derived from user's wallpaper (Android 12+). |

For presentations and printed material, use the **baseline** scheme.

---

## Add-On Color Roles (Advanced)

### Fixed Accent Colors
Same tone in light AND dark themes. Use for brand expressions that must not
invert across themes. Includes `primary-fixed`, `primary-fixed-dim`,
`on-primary-fixed`, `on-primary-fixed-variant` (and equivalents for secondary/tertiary).

### Bright and Dim Surfaces
`surface-bright` stays bright in both light and dark theme.
`surface-dim` stays dim in both light and dark theme.
Use for split-panel layouts needing consistent hierarchy across themes.

---

## Usage Anti-Patterns

| ❌ Don't | ✅ Do |
|---|---|
| Use `surface-container` as text color | Use `on-surface` |
| Use `outline` for decorative dividers | Use `outline-variant` |
| Use `outline-variant` as an interactive border | Use `outline` |
| Pair `primary` with `primary-container` (both fills) | Use `primary` + `on-primary` |
| Use fixed colors where adaptive contrast is needed | Use container roles |
