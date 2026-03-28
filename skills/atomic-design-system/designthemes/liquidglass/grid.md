# Apple Liquid Glass — Layout Grid

**Source:** https://developer.apple.com/design/human-interface-guidelines/layout  
**Responsive:** Adapts to device size, window width, and orientation

---

## Adaptive Layout Model

Apple Liquid Glass uses an **adaptive, fluid layout** that responds to:
- Screen / window size (compact, regular, large)
- Orientation (portrait, landscape)
- System font size (Dynamic Type categories)
- Safe area insets (hardware cutouts, rounded corners)

For PPTX / draw.io slides (1920×1080), use the **large regular** breakpoint target.

---

## Breakpoints (UIKit / SwiftUI size classes)

| Class | Width | Typical Device |
|---|---|---|
| Compact | < 390pt | iPhone portrait |
| Regular | ≥ 390pt | iPad, iPhone landscape, Mac |
| Large | ≥ 1024pt | iPad Pro, Mac — **PPTX target** |

---

## Column Grid for Slides (1920×1080)

```
Outer margin:     80px  (canvas.margin)
Column padding:   28px  (canvas.padding — inner card edge)
Gutter:           24px  (canvas.gutter — column gap)

1-column:   1920 - 2×80 = 1760px content width
2-column:   (1760 - 24) / 2 = 868px per column
3-column:   (1760 - 2×24) / 3 = 570px per column
```

### Column Usage by Template

| Template | Columns | Notes |
|---|---|---|
| `hero-title` | 1 | Full-width hero, glass decoration |
| `comparison-2col` | 2 | Side-by-side 868px cards |
| `grid-3` | 3 | 570px cards — KPI, Profile |
| `data-insight` | 2 | 60/40 split: chart 1056px / insight 680px |
| `numbered-list` | 1 | Full-width list, optional 2-col variant |

---

## Concentric Radii

Apple Liquid Glass requires **concentric corner radii** — nested elements should have
smaller radii than their containers, maintaining a consistent visual relationship:

```
Sheet / hero container:   radius-large  (36)
Card / panel:             radius-medium (20)
Input / tag / button:     radius-sharp  (10)
Icon in card:             radius-sharp  (10) or fully circular (radius = height/2)
```

> This concentricity is a fundamental visual principle: outer containers are rounder,
> inner elements are less round but never sharper than expected visually.

---

## Safe Area Insets (Static Media Approximation)

For slides, all content should be 80px from the canvas edge (canvas.margin).
Decorative glass elements (hero blobs, shimmer layers) may extend to 60px (margin - 20).
Text and interactive content must stay within the 80px safe zone.
