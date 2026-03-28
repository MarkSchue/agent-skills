# Material Design 3 — Shape System

**Source:** https://m3.material.io/styles/shape  
**Source:** https://m3.material.io/styles/shape/corner-radius-scale

---

## Overview

Shape in M3 expresses personality, reinforces brand, and communicates state.
Every component maps to a shape token. Shapes are defined by their **corner radius**
using a 6-step scale from Extra-Small (sharp) to Full (pill/circle).

---

## Corner Radius Scale

| Token | Value | Typical Components |
|---|---|---|
| `shape-none` | 0dp | Dividers, separators |
| `shape-extra-small` | 4dp | Text fields, menu items, tooltip, snackbars |
| `shape-small` | 8dp | Chips, text field alternate variant |
| `shape-medium` | 12dp | Cards, dialogs, input menus |
| `shape-large` | 16dp | Navigation drawers, sheets (small) |
| `shape-extra-large` | 28dp | Bottom sheets, extended FAB, large dialogs |
| `shape-full` | 50% | Badges, avatar chips, circular FABs, pills |

---

## Default Component Shape Mappings

| Component | Shape Token | Radius |
|---|---|---|
| Badge | Full | 50% |
| Bottom app bar | None | 0dp |
| Bottom sheet | Extra-Large (top only) | 28dp |
| Button (filled/outlined/tonal) | Full | 50% |
| Card | Medium | 12dp |
| Chip | Small | 8dp |
| Dialog | Extra-Large | 28dp |
| Extended FAB | Large | 16dp |
| FAB | Large | 16dp |
| Navigation bar | None | 0dp |
| Navigation drawer | Full (trailing corners) | 50% |
| Navigation rail | None | 0dp |
| Progress indicator | Full | 50% |
| Snackbar | Extra-Small | 4dp |
| Switch (track) | Full | 50% |
| Text field (filled) | Extra-Small (top only) | 4dp |
| Text field (outlined) | Extra-Small | 4dp |
| Tooltip | Extra-Small | 4dp |
| Top app bar | None | 0dp |

---

## Shape Morphing (M3 Expressive)

M3 Expressive introduced a **Material Shape Library** with 20+ custom shapes
(stars, arrows, blobs, etc.) that can morph seamlessly between each other using
the physics-based spring animation system.

Current availability:
- ✅ Jetpack Compose
- ✅ MDC-Android
- ❌ Flutter (coming)
- ❌ Web (coming)

Shape morph is used in: Standard Button Group, Loading Indicator.

---

## Customization Rules

1. **Always use the token scale** — do not hardcode arbitrary corner radii.
2. Shape conveys brand: rounder shapes feel friendlier; sharper shapes feel
   more technical/precise. Be intentional.
3. When customizing, keep all components proportionally consistent — don't mix
   `full` chips with `extra-small` cards in the same screen.
4. For asymmetric shapes, only round specific corners (e.g., dialogs opened from
   the bottom can use full top-left/right corners with square bottom corners).
5. The `full` shape (50%) on non-square containers creates a pill/stadium shape,
   not a circle. Use a square container for true circles.

---

## Shape in the Atomic Design System

The atomic system maps shape tokens as follows:

| Config key | M3 Token |
|---|---|
| `borders.radius-sharp` | `shape-extra-small` (4dp) |
| `borders.radius-medium` | `shape-medium` (12dp) |
| `borders.radius-large` | `shape-extra-large` (28dp) |

Use `ctx.rad("sharp" | "medium" | "large")` in molecule/atom code.
Never hardcode a corner radius as a numeric literal.
