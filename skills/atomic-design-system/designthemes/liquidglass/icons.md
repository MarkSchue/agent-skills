# Apple Liquid Glass — Icons

**Source:** https://developer.apple.com/sf-symbols/  
**Library:** SF Symbols 7 (released WWDC 2025)

---

## SF Symbols 7

SF Symbols is Apple's icon library with **6,000+ symbols** designed to integrate seamlessly
with the San Francisco typeface. Each symbol is:
- **Vector-based**: scales perfectly at any size
- **Typographically aligned**: optically sized and weight-matched to SF Pro
- **Semantically named**: consistent naming across platforms

---

## Symbol Rendering Modes

SF Symbols 7 supports 4 rendering modes:

| Mode | Description | Use |
|---|---|---|
| **Monochrome** | Single color, filled paths | Default — clean, simple |
| **Hierarchical** | One base color, layered opacity | Depth without color overload |
| **Palette** | 2–3 custom colors for layers | Brand color integration |
| **Multicolor** | System-defined semantic colors | Status icons, emojis |

---

## Weight Variants

SF Symbols match the weight of adjacent text. Use corresponding weights:

| Text Weight | Symbol Weight |
|---|---|
| Regular (400) | Regular |
| Medium (500) | Medium |
| Semibold (600) | Semibold |
| Bold (700) | Bold |

---

## Common Symbol Names (by category)

### Navigation & Interface
```
house                  → Home / Dashboard
chevron.right          → Forward / Navigate
arrow.left             → Back
magnifyingglass        → Search
xmark                  → Close / Dismiss
checkmark              → Confirm / Done
ellipsis               → More / Overflow menu
gearshape              → Settings / Configuration
```

### Data & Analytics
```
chart.bar.xaxis        → Bar chart
chart.line.uptrend.xyaxis → Trend / Growth
arrow.up.right         → Increase / Up
arrow.down.right       → Decrease / Down
number                 → KPI / Count
percent                → Percentage
```

### Team & People
```
person.fill            → Individual / Profile
person.2.fill          → Team / Duo
person.3.fill          → Group
person.crop.circle     → Avatar / User
briefcase.fill         → Work / Role
globe                  → Global / Region
```

### Strategy & Business
```
target                 → Goal / Mission
lightbulb.fill         → Idea / Innovation
flag.fill              → Milestone / Achievement
star.fill              → Rating / Priority
shield.fill            → Security / Trust
bolt.fill              → Speed / Performance
```

---

## Usage Guidelines for PPTX / Draw.io

Since SF Symbols are Apple-proprietary, in PPTX / draw.io contexts:
1. **Use built-in icon names** from the atomic design system's SVG library
2. SF Symbols-inspired naming convention maps to the system's icon registry
3. When an icon renders, the system looks up `icon-name:` from the SVG `/assets/icons/` folder

### Icon Badge (Liquid Glass style)
```
Badge shape:      circle (fully rounded — radius = height/2)
Badge background: primary (#007AFF)
Badge icon color: on-primary (#FFFFFF)
Badge size:       32–40px for molecule cards
```

---

## New in SF Symbols 7

- **Variadic animations**: symbols animate with spring physics matching Liquid Glass transitions
- **Symbol effects**: `.breathe`, `.rotate`, `.wiggle`, `.blink`, `.appear`, `.disappear`
- **Compositing layers**: foreground and background layers for Liquid Glass depth rendering
- **Concentric icon grid**: icon shapes now align concentrically with hardware form factors

> For the atomic design system, icon sizes should match the `label` or `heading-sub` token size
> for optical alignment with adjacent text.
