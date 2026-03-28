# Apple Liquid Glass — Motion & Animation

**Source:** https://developer.apple.com/design/human-interface-guidelines/motion  
**"Meet Liquid Glass" WWDC 2025**

---

## Philosophy

> "Liquid Glass moves with **spring physics** — it accelerates quickly, overshoots slightly, 
> and settles with a natural bounce that feels alive, not mechanical."

Liquid Glass animation is fundamentally different from both Material (curves + durations) and 
Carbon (easing functions). It uses **spring-based animations** — defined by stiffness, damping,
and mass, not duration.

---

## Spring Parameters

| Motion Token | Stiffness | Damping | Mass | Approx Duration | Characteristic |
|---|---|---|---|---|---|
| `spring-snappy` | 400 | 28 | 1.0 | ~280ms | Fast UI response, button feedback |
| `spring-default` | 280 | 22 | 1.0 | ~420ms | Standard transitions, cards |
| `spring-smooth` | 160 | 20 | 1.0 | ~580ms | Gentle appearances, overlays |
| `spring-bouncy` | 400 | 14 | 1.0 | ~350ms | Playful elements, badges |

---

## Equivalent CSS Timing Curves (for static approximation)

Since PPTX animations use Bézier curves, use these equivalents:

| Motion Token | CSS Equivalent | PPTX effect |
|---|---|---|
| `spring-snappy` | `cubic-bezier(0.33, 1, 0.68, 1)` — easeOutCubic | Fast appear, no bounce |
| `spring-default` | `cubic-bezier(0.34, 1.56, 0.64, 1)` — easeOutBack | Slight scale overshoot |
| `spring-smooth` | `cubic-bezier(0.25, 1, 0.5, 1)` — easeOutQuart | Smooth, dignified |
| `spring-bouncy` | `cubic-bezier(0.68, -0.55, 0.27, 1.55)` — easeInOutBack | Visible bounce |

---

## Animation Patterns

### Liquid Glass Material Effects
- **Appear**: scale from 92% + fade in → 100% at rest. Uses `spring-default`.
- **Dismiss**: scale to 88% + fade out. Uses `spring-snappy`.
- **Morph**: glass shape fluidly changes corners/size. Uses `spring-smooth`.
- **Highlight**: brief luminosity pulse on interaction. 80ms, easeOut.

### Navigation Transitions
- **Push**: new view slides in from right while current fades. 400ms `spring-default`.
- **Modal presentation**: sheet rises from bottom, detaches 8pt from screen edge. 500ms `spring-smooth`.
- **Popover / glass dropdown**: drops from source with slight scale. 300ms `spring-snappy`.

### Tab Bar Minimization
- **Minimize on scroll**: tab bar recedes with `spring-smooth` 580ms.
- **Re-expand**: instant spring-snappy response on reverse scroll.

---

## Reduced Motion

When **Reduce Motion** is enabled:
- All spring animations → instant or brief fade (100–200ms)
- Glass morphing → crossfade only (no scale or geometric change)
- Translucency effects may be replaced with opaque surfaces

Any custom motion in slides should have a static alternative for accessibility.

---

## Delay Hierarchy

For staggered list / card appearances:
```
Card 1: 0ms delay
Card 2: 60ms delay
Card 3: 120ms delay
...each card: +60ms
```

This stagger uses `spring-default` per item and creates a cascade feel.
