# Apple Liquid Glass — Color Roles

**Source:** https://developer.apple.com/design/human-interface-guidelines/color  
**Platform:** iOS · iPadOS · macOS (Liquid Glass / UIKit / AppKit system colors)

---

## System Color Palette

Apple's Liquid Glass uses **dynamic system colors** — named colors that automatically
adapt between Light and Dark mode (and accessibility variants like increased contrast,
differentiate without color, etc.).

### Primary System Colors

| Token | Light | Dark | Semantic Use |
|---|---|---|---|
| `primary` | `#007AFF` | `#0A84FF` | Interactive elements, tint, links |
| `secondary` | `#5856D6` | `#5E5CE6` | Secondary actions, badges |
| `tertiary` | `#32ADE6` | `#64D2FF` | Tertiary accents, information |
| `error` | `#FF3B30` | `#FF453A` | Destructive actions, validation errors |
| `warning` | `#FF9500` | `#FF9F0A` | Caution states, warnings |
| `success` | `#34C759` | `#30D158` | Confirmation, positive outcomes |

### Apple System Full Palette (Reference)

| Color | iOS Light | iOS Dark |
|---|---|---|
| Red | `#FF3B30` | `#FF453A` |
| Orange | `#FF9500` | `#FF9F0A` |
| Yellow | `#FFCC00` | `#FFD60A` |
| Green | `#34C759` | `#30D158` |
| Mint | `#00C7BE` | `#63E6E2` |
| Teal | `#32ADE6` | `#40CBE0` |
| Cyan | `#32ADE6` | `#64D2FF` |
| Blue | `#007AFF` | `#0A84FF` |
| Indigo | `#5856D6` | `#5E5CE6` |
| Purple | `#AF52DE` | `#BF5AF2` |
| Pink | `#FF2D55` | `#FF375F` |
| Brown | `#A2845E` | `#AC8E68` |

---

## Semantic Surface Tokens

The **glass layer model** uses a stack of increasingly transparent surfaces:

```
surface-container-lowest  → deepest layer (base material)
surface-container-low     → glass shimmer (F9F9FB = near-white vibrancy)
surface-container          → standard grouped background (F2F2F7)
surface-container-high     → inset / secondary fill (E5E5EA)
surface-container-highest  → modal / opaque background (D1D1D6)
```

### Surface Token Map

| Token | Light | Purpose |
|---|---|---|
| `surface` | `#FFFFFF` | Card / panel / primary glass pane |
| `on-surface` | `#000000` | Primary label — highest emphasis text |
| `on-surface-variant` | `#6D6D72` | Secondary label — reduced emphasis |
| `surface-variant` | `#F2F2F7` | Grouped table background / base layer |
| `surface-container-low` | `#F9F9FB` | Glass shimmer fill (vibrancy simulation) |
| `surface-container` | `#F2F2F7` | Standard background |
| `surface-container-high` | `#E5E5EA` | Secondary fills, insets |

---

## Glass Simulation in Static Media

Since true glass blur (backdrop-filter, UIBlurEffect) is not possible in PPTX or draw.io,
simulate Liquid Glass using:

1. **White base** surface (`#FFFFFF`) — represents the card/glass pane
2. **Glass shimmer** fill (`#F9F9FB`) — off-white with very slight blue tint for "frosted" feel
3. **Subtle border** (`#E5E5EA` at 1px) — separates glass layers
4. **Large corner radius** (20–36px) — the squircle / superellipse curvature
5. **Light drop shadow** — blur 16px, opacity 10% — simulates depth / float

---

## Color Pairing Rules

Follow iOS semantic color pairings for guaranteed contrast:

```
primary         → on-primary          (White on System Blue)
primary-container → on-primary-container  (Deep blue on light blue)
surface         → on-surface          (Black on white)
surface-variant → on-surface-variant  (Gray on light gray)
error           → on-error            (White on System Red)
success         → on-success          (White on System Green)
```

---

## Accessibility

- System Blue `#007AFF` on white: contrast ratio **4.55:1** — WCAG AA ✅
- System Blue `#007AFF` on `#F2F2F7`: contrast ratio **4.40:1** — WCAG AA ✅ (close — use bold or larger text)
- `on-surface #000000` on white: **21:1** — WCAG AAA ✅
- `on-surface-variant #6D6D72` on white: **4.64:1** — WCAG AA ✅
