# Apple Liquid Glass — Design System

**Version:** WWDC 2025 / iOS 19 · iPadOS 19 · macOS Tahoe  
**Preset slug:** `liquidglass`  
**Source:** https://developer.apple.com/design/human-interface-guidelines/

---

## What is Liquid Glass?

Liquid Glass is Apple's dynamic material design system introduced at WWDC 2025.
It defines the visual language for all Apple platforms: iOS, iPadOS, macOS, tvOS, watchOS, and visionOS.

The core concept is a **translucent glass-like surface** that:
- Combines the optical properties of glass (refraction, blur, specular highlights)
- Floats above content as a distinct functional layer
- Adapts dynamically to background content through vibrancy and luminosity
- Uses **continuous corner radius** (superellipse / squircle geometry)

---

## Key Visual Properties

| Property | Value | Notes |
|---|---|---|
| Primary accent | `#007AFF` | System Blue (iOS) |
| Background | `#F2F2F7` | System grouped background |
| Card surface | `#FFFFFF` | White glass pane |
| Glass shimmer | `#F9F9FB` | Near-white vibrancy fill |
| Corner radius S | 10pt | Buttons, tags, inputs |
| Corner radius M | 20pt | Cards, panels |
| Corner radius L | 36pt | Modals, hero containers |
| Font | SF Pro Display / SF Pro Text | San Francisco type system |
| Spacing grid | 8pt | All spacing multiples of 8 |

---

## Files in this folder

| File | Purpose |
|---|---|
| `design-config.yaml` | Reference light-theme implementation |
| `design-config-dark.yaml` | Dark mode variant |
| `design-tokens.yaml` | Full token inventory |
| `colors.md` | Color roles and semantic mapping |
| `typography.md` | SF Pro type scale |
| `spacing.md` | 8pt grid and semantic aliases |
| `grid.md` | Layout grid and breakpoints |
| `motion.md` | Spring physics and timing curves |
| `icons.md` | SF Symbols 7 guidelines |
| `principles.md` | Design principles and philosophy |

---

## How this differs from Material and Carbon

| Aspect | Material Design 3 | Carbon v11 | Liquid Glass |
|---|---|---|---|
| Shapes | Rounded (4–28px) | Sharp (0–8px) | Super-rounded (10–36px) |
| Color | Warm purple tonal | IBM blue, flat | Cool system blue, glass |
| Surface | Tinted containers | Flat gray layers | Translucent white/glass |
| Elevation | Tonal color shift | Color steps | Shadow + vibrancy blur |
| Typography | Roboto | IBM Plex Sans | SF Pro |
| Spacing grid | 4dp | 8dp | 8pt |
| Depth model | 5 elevation levels | 4 layer levels | Glass pane layering |
