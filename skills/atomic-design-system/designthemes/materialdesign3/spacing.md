# Material Design 3 — Spacing & Layout

**Source:** https://m3.material.io/foundations/layout  
**Source:** https://m3.material.io/foundations/layout/applying-layout/window-size-classes

---

## Base Grid

M3 uses a **4dp base grid**. All spacing values must be multiples of 4dp.

```
4dp base unit → tokens at ×1, ×2, ×3, ×4, ×6, ×8, ×12, ×16, ×24, ×32
```

This differs from Material 2 which used an 8dp base grid. The 4dp grid allows
for finer control over component density and touch targets.

---

## Spacing Tokens

| Token | dp | px (1dp@hdpi) | Common use |
|---|---|---|---|
| `space-1` | 4 | 4 | Icon padding, tight insets |
| `space-2` | 8 | 8 | Badge padding, tight list items |
| `space-3` | 12 | 12 | Chip padding, badge internal |
| `space-4` | 16 | 16 | Standard content inset |
| `space-5` | 20 | 20 | Navigation item padding |
| `space-6` | 24 | 24 | Card padding, section margins |
| `space-7` | 32 | 32 | Large section gaps |
| `space-8` | 48 | 48 | Section separators |
| `space-9` | 64 | 64 | Major vertical rhythm |
| `space-10` | 128 | 128 | Layout-level separation |

**Semantic aliases:**

| Alias | Value | Role |
|---|---|---|
| `inset-compact` | 8dp | Dense component padding |
| `inset-default` | 16dp | Standard padding — use by default |
| `inset-relaxed` | 24dp | Spacious component padding |
| `gap-dense` | 8dp | Tight component gaps |
| `gap-default` | 16dp | Standard component gaps |
| `gap-loose` | 24dp | Spacious component gaps |

---

## Window Size Classes

Material Design 3 defines 5 window size classes for responsive layout:

| Class | Width Range | Typical Device |
|---|---|---|
| Compact | < 600dp | Phone portrait |
| Medium | 600–839dp | Tablet portrait, foldable unfolded |
| Expanded | 840–1199dp | Phone landscape, tablet landscape, desktop |
| Large | 1200–1599dp | Desktop |
| Extra-Large | 1600dp+ | Desktop, ultra-wide |

### Navigation by Window Size

| Window Class | Navigation Pattern |
|---|---|
| Compact | Navigation bar (bottom) |
| Medium | Navigation rail (side, collapsed) |
| Expanded | Navigation rail (side, expanded) or Navigation drawer |
| Large | Navigation drawer (persistent open) |
| Extra-Large | Navigation drawer + secondary panel |

---

## Layout Zones

| Zone | Role | Color |
|---|---|---|
| Body / Content area | Main content region | `surface` |
| Navigation area | Side nav, bottom bar | `surface-container` |
| App bar / Header | Top bar | `surface-container` |
| Modal / Overlay | Dialogs, sheets | `surface-container-high` |

The same zone always uses the same color token across all window size classes.
Do not change zone colors between compact and expanded layouts.

---

## Adaptive Layout Decisions (5 Questions)

When adapting to a larger window size class, ask:

1. **What should be revealed?** — Hidden navigation, secondary panels
2. **How should the screen be divided?** — Single pane (compact/medium) vs two panes (expanded+)
3. **What should be resized?** — Cards, feeds, list items
4. **What should be repositioned?** — Bottom actions → leading edge; tabs can be anchored center
5. **What should be swapped?** — Navigation bar → navigation rail → navigation drawer

---

## Component Spacing Guidelines

| Component | Internal padding | Notes |
|---|---|---|
| Card | 16dp all sides | 12dp for compact density |
| Button | 24dp horizontal, 10dp vertical | Label size: 14sp SemiBold |
| Text field | 16dp horizontal, 16dp vertical | |
| List item | 16dp horizontal, 8–12dp vertical | |
| Bottom navigation item | 16dp horizontal, 16dp vertical | |
| Navigation rail item | 12dp all sides | |
| Chip | 8dp vertical, 12dp horizontal | |
| FAB | 16dp all sides | |

---

## Slide / Presentation Sizing

For 1920×1080 presentations:

| System token | Recommended px |
|---|---|
| Canvas margin (edge inset) | 80px |
| Content gutter | 24px |
| Section padding | 24px |
| Card internal padding | 16–24px |
| Minimum touch target | 48×48dp (≈ 64px at presentation scale) |
