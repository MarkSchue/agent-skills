# Apple Liquid Glass — Design Principles

**Source:** https://developer.apple.com/design/human-interface-guidelines/  
**WWDC 2025:** "Meet Liquid Glass" · "Adopting Liquid Glass"

---

## Core Philosophy

> **"Liquid Glass — interfaces that float, breathe, and adapt like light through glass."**

Apple Liquid Glass is built on the convergence of three experiences:
1. **Depth** — A layered visual hierarchy where functional controls float above content
2. **Fluidity** — Spring-based physics that mimic real-world material behavior
3. **Harmony** — Concentric design that aligns interface geometry with hardware form factors

---

## The 5 Liquid Glass Principles

### 1. Glass as Functional Layer

Liquid Glass is not a cosmetic effect — it is an **information-carrying material**.
Glass surfaces signal function: they tell users where controls live, where to tap,
and where the app ends and the content begins.

```
✅ Use glass for navigation, controls, overlays — elements that act
✅ Use glass sparingly — only the most important functional elements
❌ Do not apply glass to every background — it will dilute the signal
❌ Do not stack glass on glass — it obscures the content beneath
```

### 2. Continuous Corner Radius (Squircle Geometry)

Every element in Liquid Glass uses a **continuous corner radius** — the mathematical
superellipse (squircle) rather than a circle arc. This gives corners a smooth, "melted"
quality that feels different from circular-corner radius:

```
Concentric radii rule:
  Outer container:  radius-large  (36)  → most curvature, signals "container"
  Inner card:       radius-medium (20)  → less curvature, signals "content area"
  Inner element:    radius-sharp  (10)  → minimal curvature, signals "actionable item"
```

Never use `radius = 0` (sharp corners) in Liquid Glass — this breaks the glass language.
Minimum corner radius is `radius-sharp: 10`.

### 3. Content Beneath, Controls Above

Liquid Glass establishes a **two-plane depth model**:
- **Content plane**: images, text, data — what the app is about
- **Glass plane**: navigation, controls, bars — how you interact with the app

Glass elements should always feel like they are *floating* above the content, not embedded in it.
In static media (PPTX, draw.io), simulate this with:
- Larger corner radii on glass elements than on content cards
- Light drop shadows (blur 16px, opacity 10%) under glass surfaces
- White/near-white fills versus content-specific fills

### 4. Adaptive Color (System Color Intelligence)

Liquid Glass adapts color to context automatically in native iOS/macOS apps.
In static media, choose system semantic colors:

```
Primary tint:     #007AFF (System Blue)   — NOT purple, NOT custom blue
On light:         #000000 (Label primary) — NOT gray, NOT off-black
Secondary text:   #6D6D72 (Label secondary)
Success:          #34C759 (System Green)  — Do NOT substitute custom greens
Error:            #FF3B30 (System Red)    — Do NOT substitute custom reds
```

Breaking from system colors severs the perceptual cohesion Apple builds across all
Apple platforms. Users recognize these colors and derive meaning from them instantly.

### 5. Typographic Hierarchy with SF Pro

SF Pro is not just a typeface — it is the **visual voice** of Liquid Glass.
Its optical sizing, weight system, and tracking values are calibrated for Apple displays.

```
✅ Use Bold (700) for Large Title and Display headings
✅ Use Semibold (600) for card headers and navigation titles
✅ Use Regular (400) for body and secondary content
✅ Maintain the Dynamic Type scale proportions (34 / 22 / 17 / 15 / 13)
❌ Do not compress or stretch SF Pro letterforms
❌ Do not apply manual letter-spacing overrides to Display text
❌ Do not mix SF Pro with incompatible rounded fonts (use SF Pro Rounded if needed)
```

---

## What Makes Liquid Glass Different

### vs Material Design 3 (Google)
| Aspect | Material 3 | Liquid Glass |
|---|---|---|
| Primary color | Warm purple tonal | Cool system blue |
| Font | Roboto (screen-neutral) | SF Pro (Apple-optimized) |
| Corner radius | 4 → 28px range | 10 → 36px range |
| Surface | Tinted `primary-container` fills | Translucent white glass |
| Elevation | Tonal color shift | Shadow + vibrancy blur |
| Motion | Easing curves | Spring physics |
| Color roles | 26 roles (full tonal palette) | Dynamic system colors |

### vs Carbon Design System (IBM)
| Aspect | Carbon v11 | Liquid Glass |
|---|---|---|
| Shape | Sharp (0–8px radius) | Ultra-rounded (10–36px) |
| Primary color | IBM Blue (`#0f62fe`) | System Blue (`#007AFF`) |
| Surface | Flat gray layers | Translucent glass |
| Typography | IBM Plex Sans (geometric) | SF Pro (humanist) |
| Grid | 8px strict mini-unit | 8pt flexible |
| Depth | Flat layer elevation | Glass + shadow depth |
| Tone | Industrial, technical | Airy, personal, expressive |

---

## Accessibility Principles

1. **Color is never the only signal** — always pair color with shape, position, or typography
2. **Reduced transparency mode**: all glass effects replaced with opaque fills
3. **Increased contrast mode**: border strength increases, text weight increases
4. **Dynamic Type**: all text scales from smallest to accessibility-XXL
5. **System colors automatically adapt** — do not override with custom opacity hacks

---

## Anti-Patterns (DO NOT DO)

```
❌ radius-sharp: < 10   — no sharp corners in Liquid Glass
❌ Hard-coded hex colors — always use token aliases that respect light/dark
❌ Stacking glass on glass — maximum one glass layer per visual zone
❌ Non-SF-Pro fonts for primary content (use only for branded headlines)
❌ Dense padding — Liquid Glass breathes. Never reduce canvas.padding below 16.
❌ Multiple competing accent colors per slide — one dominant primary, one secondary max
```
