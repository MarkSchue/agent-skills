# Carbon Spacing

**Source:** https://carbondesignsystem.com/elements/spacing/overview/

---

## Foundation: The 8px Mini Unit

All Carbon spacing is based on an **8px mini unit** ≡ `spacing-03`.

Everything on a product page — margins, paddings, component heights, icon
sizes, grid gutters — should be a multiple of **8px**, or in cases of fine
detail, **4px** (half a mini unit).

```
1 mini unit = 8px
2 mini units = 16px → standard spacing
3 mini units = 24px → relaxed
4 mini units = 32px → section gap
```

---

## Spacing Scale

Carbon's scale has 13 steps covering 2px to 160px.

| Token | rem | px | Multiples of 8px | Semantic use |
|---|---|---|---|---|
| `$spacing-01` | 0.125 | **2px** | ¼× | Fine detail, icon gap nudge |
| `$spacing-02` | 0.250 | **4px** | ½× | Inline icon → label gap |
| `$spacing-03` | 0.500 | **8px** | 1× | 1 mini unit — smallest meaningful space |
| `$spacing-04` | 0.750 | **12px** | 1.5× | Tight padding (tags, chips) |
| `$spacing-05` | 1.000 | **16px** | 2× | **Standard inset / padding** |
| `$spacing-06` | 1.500 | **24px** | 3× | Comfortable inset / section gap |
| `$spacing-07` | 2.000 | **32px** | 4× | Large gap, between components |
| `$spacing-08` | 2.500 | **40px** | 5× | Component set dividers |
| `$spacing-09` | 3.000 | **48px** | 6× | Section spacer |
| `$spacing-10` | 4.000 | **64px** | 8× | Major section separator |
| `$spacing-11` | 5.000 | **80px** | 10× | Hero / page edge padding |
| `$spacing-12` | 6.000 | **96px** | 12× | Large margin blocks |
| `$spacing-13` | 10.000 | **160px** | 20× | Max spacing / layout bands |

---

## Design Principles

**1. Spatial consistency:** All space is from the scale. Never use arbitrary
values like 10px, 15px, or 22px.

**2. Density matches function:** Products dealing with dense data (dashboards,
tables) use smaller spacing (`$spacing-03`, `$spacing-04`). Editorial and
marketing pages use larger spacing (`$spacing-08`+).

**3. Component internal spacing:** Use `$spacing-03` to `$spacing-05` for
padding within a component. Use `$spacing-06`+ between components.

**4. Vertical rhythm:** Page sections should have consistent vertical gaps.
A baseline of `$spacing-09` (48px) between major slide sections works well.

---

## Spacing in the 2x Grid

The grid (see [grid.md](./grid.md)) uses spacing tokens for its gutter and margins:

| Value | Token | Breakpoints |
|---|---|---|
| 0px gutter | n/a | Small (320px) |
| 16px gutter | `$spacing-05` | Medium, Large, X-Large |
| 24px gutter | `$spacing-06` | Max (1584px+) |
| 16px margin | `$spacing-05` | All breakpoints |

---

## Stacking vs. Inline Spacing

| Pattern | Tokens | Direction |
|---|---|---|
| **Stacked** (vertical rhythm) | `$spacing-07`–`$spacing-10` | ↕ block margin |
| **Inset** (padding inside container) | `$spacing-04`–`$spacing-06` | ↔↕ padding |
| **Inline** (horizontal text gap) | `$spacing-02`–`$spacing-04` | ↔ inline margin |
| **Squished** (compact UI density) | `$spacing-02`–`$spacing-03` | ↕ reduced padding |

---

## Component Spacing Guidelines

### Buttons

| Context | Spacing |
|---|---|
| Button padding horizontal | `$spacing-06` (24px) |
| Button padding vertical | `$spacing-04` (12px) |
| Button group gap | `$spacing-03` (8px) |
| Icon button padding | `$spacing-04` (12px) all sides |

### Cards / Tiles

| Context | Spacing |
|---|---|
| Card padding | `$spacing-05` or `$spacing-06` |
| Card gap in grid | `$spacing-05` (matches gutter) |

### Lists and Data Tables

| Context | Spacing |
|---|---|
| Table row height (default) | 48px (`6×8`) |
| Table row height (compact) | 32px (`4×8`) |
| Table row height (spacious) | 64px (`8×8`) |
| List item padding | `$spacing-04`/`$spacing-05` |

### Form Elements

| Context | Spacing |
|---|---|
| Input height | 40px (`5×8`) |
| Input padding horizontal | `$spacing-05` (16px) |
| Form field gap | `$spacing-06` (24px) |
| Label → input gap | `$spacing-03` (8px) |

---

## Presentation Slide Spacing

Recommended spacing allocations on a 1920×1080 slide:

| Zone | Spacing |
|---|---|
| Page margin / bleed area | 80px (10×8) |
| Slide padding (content inset) | 48px (`$spacing-09`) |
| Between heading and body | 24px (`$spacing-06`) |
| Between content blocks | 40px (`$spacing-08`) |
| Between callout items | 16px (`$spacing-05`) |
| Caption / annotation offset | 8px (`$spacing-03`) |

---

## Spacing Anti-Patterns

| Wrong | Right |
|---|---|
| Arbitrary values (10px, 15px, 22px) | Use nearest 4px/8px step |
| Equal spacing everywhere | Dense content → smaller tokens; editorial → larger |
| Gaps between items that don't use the scale | Must be from the 13-step table above |
| Negative space ignored | Whitespace = structure — generous spacing improves hierarchy |
