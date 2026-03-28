# Material Design 3 — Iconography

**Source:** https://fonts.google.com/icons  
**Source:** https://m3.material.io/styles/icons

---

## Material Symbols

Material Design 3 uses **Material Symbols** — a variable icon font hosted on
Google Fonts. Material Symbols replaces Material Icons (the previous system) with
full variable font control.

**Font family:** `Material Symbols Outlined` / `Material Symbols Rounded` / `Material Symbols Sharp`

---

## Variable Font Axes

Material Symbols supports 4 variable axes, each adjustable for expressive and
contextual control:

| Axis | CSS property | Range | Default | Effect |
|---|---|---|---|---|
| **Fill** | `font-variation-settings: 'FILL' N` | 0–1 | 0 | 0 = outline only; 1 = filled solid |
| **Weight** | `'wght' N` | 100–700 | 400 | Stroke thickness |
| **Grade** | `'GRAD' N` | -25–200 | 0 | Fine weight adjustment (negative = thinner) |
| **Optical size** | `'opsz' N` | 20–48 | 24 | Adjusts detail level for size context |

---

## Recommended Icon Sizes

| Context | Size | `opsz` setting |
|---|---|---|
| Micro / annotation | 16dp | 20 |
| Standard UI icon | 24dp | 24 (default) |
| Navigation item | 24dp | 24 |
| Toolbar / app bar | 24dp | 24 |
| Cards, list items | 24–32dp | 24 |
| Hero / feature icon | 48dp | 48 |

Always match `opsz` to the rendered size. At small sizes, icons become
too detailed without adjusting `opsz` to 20.

---

## Style Variants

| Variant | Description | Best for |
|---|---|---|
| **Outlined** (default) | Stroke-based icons | General UI, navigation |
| **Rounded** | Softer rounded terminals | Consumer products, playful UI |
| **Sharp** | Crisp 90° terminals | Utilitarian, data products |

Consistency: use the same variant throughout a product. Do not mix variants.

---

## Color Rules for Icons

| Context | Color token | Notes |
|---|---|---|
| Standard icon | `on-surface` | Default for primary icons |
| Secondary / hint icon | `on-surface-variant` | Lower-emphasis icons |
| Icon on filled button | `on-primary` | Match the button's fill color context |
| Icon in container | `on-{container}` | Always use the `on-` counterpart |
| Error icon | `error` | Use alongside error text |
| Disabled icon | `on-surface` at 38% opacity | |
| Active / selected icon | `primary` | Navigation, toggles |

---

## Importing via Google Fonts

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
```

```css
.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
```

```html
<span class="material-symbols-outlined">home</span>
```

---

## Icon Naming Conventions

Material Symbols uses snake_case names: `arrow_back`, `account_circle`,
`close`, `check`, `expand_more`, `visibility`.

Category references:
- **Action:** `add`, `create`, `delete`, `edit`, `settings`, `search`
- **Navigation:** `arrow_back`, `menu`, `close`, `chevron_right`
- **Communication:** `email`, `message`, `notifications`
- **Data:** `bar_chart`, `pie_chart`, `trending_up`, `analytics`
- **UI state:** `check_circle`, `error`, `warning`, `info`

Full icon library: https://fonts.google.com/icons

---

## Usage in Presentation Slides

For draw.io and PPTX output, use SVG exports from the Google Fonts icon viewer or
the Material Symbols npm package (`@material-symbols/svg-400`).

Recommended approach:
1. Download SVG from https://fonts.google.com/icons
2. Set fill color via `ctx.color("on-surface")` at render time
3. Size icons at 24–32px for card icons, 16px for annotation icons
4. Store downloaded SVGs in `assets/icons/material/`

---

## Icon Grid and Padding

Material icons are designed on a 24×24dp grid with the following interior zones:

```
24dp outer box
├── 4dp live area margin (on all sides)
└── 20dp "trim box" (actual icon artwork)
    ├── 2dp safe zone margin
    └── 16dp active content area
```

Always render icons at their intended size. Scaling should be proportional.
Avoid rendering at odd sizes (e.g., 23px) that cause sub-pixel blurring.
