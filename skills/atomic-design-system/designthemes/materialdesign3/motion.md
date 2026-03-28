# Material Design 3 — Motion System

**Source:** https://m3.material.io/styles/motion/overview

---

## Overview

M3 Expressive (May 2025) replaced the previous easing/duration system with a
**physics-based spring system**. Springs produce motion that feels natural and
alive — like real objects with mass and elasticity.

The system has two preset **motion schemes**: Expressive and Standard.

---

## Motion Schemes

### Expressive (default for most products)
- Based on spring physics with **overshoot and bounce**
- Use for: hero moments, FAB transitions, page-level animations
- Feel: energetic, personalized, playful

### Standard
- Spring physics with **no overshoot** — smooth ease-in-out feel
- Use for: utilitarian products, data-heavy interfaces, productivity apps
- Feel: efficient, functional, calm

---

## Spring Tokens

Each scheme provides 6 spring tokens (3 speeds × 2 types):

| Speed | Spatial | Effects |
|---|---|---|
| Fast | `motion.spring.fast.spatial` | `motion.spring.fast.effects` |
| Default | `motion.spring.default.spatial` | `motion.spring.default.effects` |
| Slow | `motion.spring.slow.spatial` | `motion.spring.slow.effects` |

**Spatial springs** — used for position, size, rotation, corner radius animation.
These may overshoot in the Expressive scheme.

**Effects springs** — used for color, opacity, fill. No overshoot in any scheme
(overshoot on fades would look wrong).

### Speed Guidelines

| Speed | Use case |
|---|---|
| Fast | Small components (buttons, switches), micro-interactions |
| Default | Partially-covering transitions (bottom sheet, nav rail expansion) |
| Slow | Full-screen animations, page transitions |

---

## Spring Token Implementation

Calling a spring: declare the scheme, then use the token.

```kotlin
// Jetpack Compose
val motionScheme = MaterialTheme.motionScheme  // expressive or standard
// Use token:
motionScheme.fastSpatialSpec<Float>()
```

The scheme is set at the product level — switching scheme changes all motion
automatically without touching individual component code.

---

## Legacy Easing (Pre-M3 Expressive Fallback)

For platforms without spring support, use these cubic-bezier curves:

| Curve | Function | Cubic-Bezier |
|---|---|---|
| Standard (emphasized) | Element stays fully visible | `cubic-bezier(0.2, 0, 0, 1)` |
| Standard (decelerate) | Element enters view | `cubic-bezier(0, 0, 0, 1)` |
| Standard (accelerate) | Element exits view | `cubic-bezier(0.3, 0, 1, 1)` |
| Expressive spatial | Overshoots, bouncs | Spring-based only |

**Duration (legacy):**

| Token | Duration | Use |
|---|---|---|
| `motion.duration.short-1` | 50ms | Icon swaps, state changes |
| `motion.duration.short-2` | 100ms | Small fades, hover |
| `motion.duration.medium-1` | 200ms | Component entrances |
| `motion.duration.medium-2` | 300ms | Panel transitions |
| `motion.duration.long-1` | 400ms | Page transitions |
| `motion.duration.long-2` | 500ms | Full-screen transitions |

---

## Motion Principles

1. **Purposeful** — every motion must communicate something (state change, origin,
   relationship between elements).
2. **Natural** — follow physics; avoid mechanical linear motion.
3. **Responsive** — user interactions must have immediate feedback (≤ 100ms).
4. **Unobtrusive** — good motion goes unnoticed; it supports the task, not
   distracts from it.
5. **Accessible** — always provide reduced-motion alternatives for users with
   vestibular disorders.

---

## Reduced Motion

Always respect the `prefers-reduced-motion` media query. When enabled:
- Replace spatial transitions with simple opacity fades
- Keep effects (opacity, color) transitions — these are generally safe
- Eliminate overshoot/bounce entirely
- Reduce all durations by 50% minimum

---

## Key Animation Patterns

| Pattern | Spring | Notes |
|---|---|---|
| FAB → Activity | Expressive, default spatial | Container transform, expressive overshoot |
| Bottom sheet open | Expressive, default spatial | Entrance from below with slight bounce |
| Card expand | Expressive, default spatial | Scale + translate |
| Dialog appear | Standard, fast spatial | No bounce — utilitarian, focused |
| Navigation transition | Expressive, slow spatial | Cross-fade with directional shift |
| Color transition | Effects, default | No overshoot |
| Opacity fade | Effects, fast | Clean, invisible |
| Icon morph | Expressive, fast spatial | Morphing shape + weight |
