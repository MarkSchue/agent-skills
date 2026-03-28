# Material Design 3 — Design Principles

**Source:** https://m3.material.io/

---

## Core Philosophy

> **"Material You" — design that adapts to the individual, not the other way around.**

Material Design 3 (Material You) is built on three interconnected values:

1. **Personal** — Colors, shapes, and sizes adapt to the user's identity and preferences
2. **Adaptive** — Layouts, components, and content respond to device, context, and input
3. **Expressive** — Motion, shape, and color convey personality and brand character

---

## The 5 Design Principles

### 1. Token-First Architecture

Every visual property — color, type, shape, spacing, motion — is expressed as
a **named semantic token**, not a raw value. Tokens decouple visual decisions from
implementation, enabling theming without touching component code.

```
❌  fill="#6750a4"          →  hardcoded value, breaks on theme change
✅  fill=ctx.color("primary") →  semantic token, resolves at theme time
```

### 2. Semantic Pairing

Colors exist in designed pairs. The `on-*` token for any fill is the only
guaranteed accessible text color for content on that fill.

```
primary → on-primary         (not on-primary-container, not surface)
primary-container → on-primary-container
surface → on-surface         (or on-surface-variant for secondary text)
```

Breaking pairings invalidates the contrast guarantees built into the system.

### 3. Accessible by Default

M3 is designed to be WCAG 2.1 AA compliant when tokens are used correctly:
- All standard `on-*` / fill pairs meet 4.5:1 contrast for normal text
- `outline` meets 3:1 against surface
- Three contrast levels (standard / medium / high) are supported via token adjustments

### 4. Adaptive Hierarchy via Scale

M3 provides a complete scale system for every dimension:
- **Color**: 26 roles (5 groups) with consistent tonal relationships
- **Type**: 15 styles across 5 roles (Display → Label)
- **Shape**: 6-step corner radius scale
- **Spacing**: 4dp grid with semantic aliases
- **Elevation**: 5-level tonal surface system

Components map to a single point on each scale. Customize by adjusting the
entire scale uniformly, not by changing individual component values.

### 5. Separation of Platform and Design

Material tokens translate to platform-specific implementations at build time.
The same semantic token `md.sys.color.primary` is `#6750a4` in light theme but
`#d0bcff` in dark theme. On iOS it becomes a dynamic Color token; on Android a
ColorStateList; on Web a CSS custom property.

---

## What Makes M3 Different from M2

| Aspect | Material 2 | Material 3 |
|---|---|---|
| Color | 5 colors (primary, secondary, error, surface, bg) | 26 semantic roles across 6 groups |
| Dynamic color | No | Yes — user wallpaper / content-based |
| Elevation | Drop shadows at 5 levels | Tonal surface-container scale |
| Typography | 13 styles (fixed names) | 15 baseline + 15 emphasized styles |
| Shape system | Limited | 6-step token scale + shape morphing |
| Motion | Easing curves + duration | Physics-based spring system |
| Icon library | Material Icons (fixed weight) | Material Symbols (4-axis variable font) |
| Base grid | 8dp | 4dp |

---

## Key Design Decisions for Presentations

| Decision | Rule | Reason |
|---|---|---|
| Background fill | Use `surface` or `surface-container-*` | Neutral, accessible |
| Card fills | Use `surface-container-low` or `surface-container` | Communicates elevation |
| Highlighted cards | Use `primary-container` | High-emphasis without full primary |
| Text on colored fill | Use the matching `on-*` token | Ensures 4.5:1 contrast |
| KPI / metric values | Use `primary` or `on-primary-container` | High brand emphasis |
| Status indicators | Use `error` / `warning` / `success` | Semantic, standard meaning |
| Dividers | Use `outline-variant` | Decorative, not interactive |
| Section borders | Use `outline` | Structural, interactive boundary |

---

## Anti-Patterns

| ❌ Never | Why |
|---|---|
| Hardcode any `#hex` color value | Breaks theming and dark mode |
| Use `on-surface` as a fill/background | On-* tokens are for text/icons only |
| Use `primary` for body text decoration | Dilutes the primary accent hierarchy |
| Apply `outline` to dividers | Wrong contrast level — use `outline-variant` |
| Mix shape radius values from different scale steps | Inconsistent visual language |
| Use font sizes not on the type scale | Components may reflow unexpectedly |
| Use the same typography role for different hierarchy levels | Breaks scan-ability |

---

## References

- 🏠 [Material Design 3 home](https://m3.material.io/)
- 🎨 [Theme Builder (generate custom palettes)](https://m3.material.io/theme-builder)
- 📦 [Material Web components](https://github.com/material-components/material-web)
- 📱 [Jetpack Compose Material 3](https://developer.android.com/jetpack/compose/designsystems/material3)
- 🐦 [Flutter Material 3](https://docs.flutter.dev/ui/design/material)
