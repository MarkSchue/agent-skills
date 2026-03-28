# Carbon Color System

**Source:** https://carbondesignsystem.com/elements/color/overview/

---

## 4 Themes

Carbon ships 4 production-ready themes built from IBM's neutral gray palette.
All themes share the same token names — only values change.

| Theme | Background | Usage |
|---|---|---|
| **White** | `#ffffff` | Default light — most IBM products |
| **Gray 10** | `#f4f4f4` | Alternate light — softer backdrop |
| **Gray 90** | `#262626` | Medium dark |
| **Gray 100** | `#161616` | Deep dark — maximum contrast |

---

## Token Architecture

Carbon colors are **semantic tokens** mapped from the IBM core palette.
Never use raw palette values (`#0f62fe`) directly — always use tokens (`$interactive`).

```
IBM Core Palette → Theme Mapping → Component Tokens
(Gray 100, Blue 60, ...)   ($text-primary, ...)   ($button-primary, ...)
```

---

## 10 Token Groups

### Background Group

| Token | White | Gray 10 | Gray 90 | Gray 100 |
|---|---|---|---|---|
| `$background` | `#ffffff` | `#f4f4f4` | `#262626` | `#161616` |
| `$background-hover` | `#e8e8e8` | `#e0e0e0` | `#333333` | `#2c2c2c` |
| `$background-active` | `#c6c6c6` | `#c6c6c6` | `#525252` | `#525252` |
| `$background-selected` | `#e0e0e0` | `#e0e0e0` | `#393939` | `#393939` |

### Layer Group (Layered Surfaces)

| Token | White | Gray 10 | Gray 90 | Gray 100 |
|---|---|---|---|---|
| `$layer-01` | `#f4f4f4` | `#ffffff` | `#353535` | `#262626` |
| `$layer-02` | `#ffffff` | `#f4f4f4` | `#3d3d3d` | `#393939` |
| `$layer-03` | `#f4f4f4` | `#ffffff` | `#525252` | `#525252` |

**Layering model:**
- Light themes: alternate White ↔ Gray 10 — each layer steps down
- Dark themes: each layer is one step lighter (higher z = lighter gray)
- Rule: layer content always has enough contrast against its backdrop

### Field Group

| Token | White | Gray 100 |
|---|---|---|
| `$field-01` | `#f4f4f4` | `#262626` |
| `$field-02` | `#ffffff` | `#393939` |
| `$field-hover-01` | `#e8e8e8` | `#333333` |

### Border Group

| Token | White | Gray 100 | Purpose |
|---|---|---|---|
| `$border-subtle-00` | `#e0e0e0` | `#393939` | Dividers on `$background` |
| `$border-subtle-01` | `#c6c6c6` | `#525252` | Dividers on `$layer-01` |
| `$border-strong-01` | `#8d8d8d` | `#6f6f6f` | Strong borders, boxes |
| `$border-interactive` | `#0f62fe` | `#4589ff` | Active input borders |
| `$border-inverse` | `#161616` | `#f4f4f4` | High-contrast border |

### Text Group

| Token | White | Gray 100 | Minimum contrast |
|---|---|---|---|
| `$text-primary` | `#161616` | `#f4f4f4` | ≥ 7:1 |
| `$text-secondary` | `#525252` | `#c6c6c6` | ≥ 4.5:1 |
| `$text-placeholder` | `#a8a8a8` | `#6f6f6f` | n/a |
| `$text-helper` | `#6f6f6f` | `#8d8d8d` | ≥ 4.5:1 |
| `$text-error` | `#da1e28` | `#ff8389` | ≥ 4.5:1 |
| `$text-disabled` | `#c6c6c6` | `#525252` | Not required |
| `$text-on-color` | `#ffffff` | `#ffffff` | ≥ 4.5:1 on blue bg |
| `$text-inverse` | `#ffffff` | `#161616` | ≥ 7:1 |

### Link Group

| Token | White | Gray 100 |
|---|---|---|
| `$link-primary` | `#0f62fe` | `#78a9ff` |
| `$link-primary-hover` | `#0043ce` | `#a6c8ff` |
| `$link-secondary` | `#0043ce` | `#78a9ff` |
| `$link-visited` | `#8a3ffc` | `#be95ff` |
| `$link-inverse` | `#78a9ff` | `#0f62fe` |

### Icon Group

| Token | White | Gray 100 | Usage |
|---|---|---|---|
| `$icon-primary` | `#161616` | `#f4f4f4` | Primary icons |
| `$icon-secondary` | `#525252` | `#c6c6c6` | Decorative / secondary |
| `$icon-inverse` | `#ffffff` | `#161616` | Icons on colored backgrounds |
| `$icon-interactive` | `#0f62fe` | `#78a9ff` | Interactive icon buttons |
| `$icon-disabled` | `#c6c6c6` | `#525252` | Disabled state |

### Support Group (Status Colors)

| Status | White | Gray 100 | Palette ref |
|---|---|---|---|
| **Error** `$support-error` | `#da1e28` | `#ff8389` | Red 60 / Red 40 |
| **Warning** `$support-warning` | `#f1c21b` | `#f1c21b` | Yellow 30 (same) |
| **Success** `$support-success` | `#24a148` | `#42be65` | Green 50 / Green 40 |
| **Info** `$support-info` | `#0043ce` | `#4589ff` | Blue 70 / Blue 50 |

> Warning yellow is **identical in all themes** — it must always appear on a
> dark background. Use `$background` (not a white layer) behind `$support-warning`.

### Focus Group

| Token | White | Gray 100 |
|---|---|---|
| `$focus` | `#0f62fe` | `#ffffff` |
| `$focus-inset` | `#ffffff` | `#161616` |
| `$focus-inverse` | `#ffffff` | `#0f62fe` |

> Focus ring spec: **2px solid `$focus` + 1px offset `$focus-inset`**. Non-negotiable — meets WCAG 2.1.

### Skeleton Group

| Token | White | Gray 100 |
|---|---|---|
| `$skeleton-background` | `#e8e8e8` | `#333333` |
| `$skeleton-element` | `#e0e0e0` | `#393939` |

---

## Interaction State Logic

Carbon uses a step-based system from the IBM Gray palette:

| State | Behavior | Example (White theme) |
|---|---|---|
| **Hover** | Half step lighter or darker | Gray 10 → mix of Gray 10/0 |
| **Active** | Two steps (more extreme) | Gray 20 |
| **Selected** | One step | Add `$layer-selected` |
| **Focus** | 2px border, `$focus` color | Blue 60 ring |
| **Disabled** | Muted gray, no pointer | `text-disabled`, `icon-disabled` |

---

## Color Pairing Rules

1. **`$text-primary` on `$background`** — always ≥ 7:1 (WCAG AAA)
2. **`$text-secondary` on `$background`** — always ≥ 4.5:1 (WCAG AA)
3. **`$text-on-color` on `$button-primary`** — meets 4.5:1 with Blue 60
4. **Warning text** — only show `$support-warning` text on `$layer-02` or darker, never on white
5. **Link underline** — required in body copy; standalone links may use icon instead
6. **Never** place `$text-placeholder` as meaningful text — it's decorative only

---

## IBM Palette Reference

The full IBM design palette uses a numbered 100-scale per hue.
Carbon tokens always map from this palette:

```
Gray:    100=Darkest, 90, 80, 70, 60, 50, 40, 30, 20, 10=Lightest, White
Blue:    100, 90, 80, 70, 60=IBM Blue, 50, 40, 30, 20, 10
Red:     similar scale
Yellow:  similar scale (30 = Brand Yellow)
Green:   similar scale
```

Full palette: https://www.ibm.com/design/language/color
