# Apple Liquid Glass — Spacing

**Source:** https://developer.apple.com/design/human-interface-guidelines/layout  
**System:** 8pt grid

---

## The 8-Point Grid

Apple Liquid Glass uses an **8-point (8pt) base grid**. Every spacing value is a multiple of 8pt,
with 4pt used only for tight micro-spacing (icon-to-label gaps, dense list items).

```
4pt  = 0.5 × unit  → micro  (icon gap, tight inline spacing)
8pt  = 1 × unit    → compact (list item padding, small gaps)
16pt = 2 × units   → standard content padding  
24pt = 3 × units   → comfortable section gap
32pt = 4 × units   → generous inter-section padding
48pt = 6 × units   → major section separation, hero breathing room
```

---

## Semantic Spacing Tokens

| Token | Value | Use |
|---|---|---|
| `xs` | 4pt | Micro: icon-to-label, tag internal padding |
| `s` | 8pt | Compact: list row padding, inline gap |
| `m` | 16pt | Standard: card internal padding, column gap |
| `l` | 24pt | Comfortable: section padding, content margin |
| `xl` | 48pt | Spacious: major section, hero element gap |

---

## Layout Spacing Recommendations

### Card / Panel
```
Card internal padding:     m (16pt)
Card-to-card gap:          m (16pt)
Card header bottom margin: s (8pt)
Card body line-height:     1.47 × font-size
```

### Grid Layouts
```
Grid column gap:           l (24pt)
Grid row gap:              l (24pt)
Grid outer margin:         xl (48pt) or canvas.margin (80pt)
```

### Hero / Full-Slide
```
Hero content top margin:   xl (48pt)
Hero title bottom gap:     m (16pt)
Hero subtitle bottom gap:  l (24pt)
```

### Navigation Elements
```
Tab bar item padding:      s (8pt) vertical
Toolbar item spacing:      s (8pt)
Section header padding:    s (8pt) top, s (8pt) bottom
```

---

## Safe Areas and Insets

Apple Liquid Glass introduces **inset sheets** (modals inset from screen edges by 8pt on each side).
For PPTX / draw.io, simulate with:
- Canvas outer `margin: 80` (consistent across all presets)
- Card inner `padding: 28` (8pt grid: 24pt + 4pt safety margin)

---

## Comparison to Other Systems

| System | Grid | Base Unit | Standard Padding |
|---|---|---|---|
| Material Design 3 | 4dp | 4dp | 24dp |
| Carbon v11 | 8px | 8px | 16px |
| **Liquid Glass** | **8pt** | **8pt** | **16–24pt** |
