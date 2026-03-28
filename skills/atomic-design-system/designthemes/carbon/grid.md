# Carbon 2x Grid

**Source:** https://carbondesignsystem.com/elements/2x-grid/overview/

---

## What Is the 2x Grid?

The Carbon 2x Grid is a **scalable, multi-column grid** rooted in the **8px mini unit**.
Every dimension — column count, gutter, margin, component sizing — is a multiple of 8px
(or 4px for fine detail).

The name "2x" means the major structural units are always powers of 2 counted in 8px units:
8, 16, 32, 64, 128 … matching `$spacing-03` through `$spacing-10`.

---

## Mini Unit

The fundamental atom of the 2x Grid:

```
1 mini unit = 8px
```

The mini unit ensures all content aligns to an invisible baseline, giving
products the tight visual consistency IBM products are known for.

**Fixed sizing scale derived from mini unit:**

| Mini units | px |
|---|---|
| 1× | 8px |
| 2× | 16px |
| 3× | 24px |
| 4× | 32px |
| 6× | 48px |
| 8× | 64px |
| 10× | 80px |

---

## 5 Breakpoints

| Breakpoint | Name | Width | Columns | Gutter | Margin |
|---|---|---|---|---|---|
| `sm` | Small | 320px | 4 | 0 | 0 |
| `md` | Medium | 672px | 8 | 16px | 16px |
| `lg` | Large | 1056px | 16 | 16px | 16px |
| `xlg` | X-Large | 1312px | 16 | 16px | 16px |
| `max` | Max | 1584px | 16 | 24px | 16px |

> The margin is **not additive** — it is the space from the screen edge to the
> first column. On Small, the 4-column grid goes full width with no gutter,
> relying on component-level padding instead.

---

## Grid Types

### Fluid Grid
Columns **flex** proportionally as the viewport expands between breakpoints.
Content fills available space. Used for most page layouts.

```
| col col col col col col col col col col col col col col col col |
             (16 columns at lg — all fluid)
```

### Fixed Grid
Columns remain a **fixed width** at each breakpoint. Centered in viewport.
Used for max-width layouts (e.g. max breakpoint = 1584px max-width centered).

### Hybrid Grid
Most IBM products use a hybrid: fixed sidebar + fluid main content zone.

---

## Aspect Ratios

Carbon specifies standardized **aspect ratios** for cards, images, and tiles.
Always use a ratio from this list — never freeform:

| Ratio | Use |
|---|---|
| 1:1 | Square avatars, icons, tiles |
| 2:1 | Panoramic banners |
| 2:3 | Portrait cards |
| 3:2 | Landscape cards |
| 4:3 | Standard media, presentations |
| 16:9 | Video, widescreen slides |

---

## Grid Zones (Content Zones)

Carbon divides the grid into horizontal **zones** for complex layouts:

| Zone | Purpose |
|---|---|
| **Banner** | Full-width top band — logo, navigation |
| **Content area** | Main body — fluid or fixed grid content |
| **Aside** | Sidebar — typically 4 columns on lg |
| **Footer** | Full-width bottom band |

On presentation slides (1920×1080):
- Use an equivalent of 80px margin (10×8) on all four sides
- Internal content zone = 1760px wide (remaining after margins)
- Divide into virtual column grid as needed

---

## Slide Layout Guidance with Carbon Grid

For 1920×1080 slide canvases following Carbon 2x Grid:

| Element | Width / Spacing |
|---|---|
| Slide margin | 80px (10 mini units) |
| Content zone | 1760px wide |
| Section column width | 1760 ÷ 16 = 110px per column |
| Standard gutters | 16px (`$spacing-05`) |
| Large gap (2 sections) | 32px (`$spacing-07`) |
| Half-width split | ~848px each (8 col × 110px + 7 × 16px gutter) |

---

## Grid and Motion Alignment

When elements animate onto the grid (see [motion.md](./motion.md)), they should:
- Slide in along the **grid axis** (horizontal or vertical)
- Land precisely on a column edge
- Use `entrance-productive` easing for small movements
- Use `entrance-expressive` easing for hero/large panel motion

---

## Key Rules

1. **Every layout value must be on the mini unit scale** (multiple of 8, or 4 for fine spacing)
2. **Never use 12px+ gaps that are not in the spacing scale** — use the closest token
3. **Column spans must add up** — a 3-column + 5-column split on an 8-column breakpoint
4. **Margins are fixed** — only internal gutter and content widths are fluid
5. **Aspect ratios for tiles** — always from the approved list above
