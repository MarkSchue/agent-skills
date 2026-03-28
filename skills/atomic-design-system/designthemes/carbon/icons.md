# Carbon Icons

**Source:** https://carbondesignsystem.com/elements/icons/library/

---

## Carbon Icons Library

Carbon Icons is IBM's open-source icon library. It provides flat, geometric,
pixel-aligned icons in a consistent visual language derived from IBM Design Language.

**Key characteristics:**
- Flat, single-weight line icons (no gradients, no shadows)
- Optimized for digital screens
- Available as SVG files and as packages for React, Angular, Vue, Svelte, and vanilla JS
- All icons are licensed under Apache 2.0

**GitHub:** https://github.com/carbon-design-system/carbon/tree/main/packages/icons

---

## Icon Sizing

Carbon icons use 4 fixed sizes — no scaling between them:

| Size | px | Use |
|---|---|---|
| **16px** | 16 | Compact UI — inline with text, table rows, labels |
| **20px** | 20 | Standard button icons, navigation |
| **24px** | 24 | **Default** — standalone icons, list items, sidebar |
| **32px** | 32 | Large action icons, empty states |

> Do not scale icons to other sizes (18px, 22px, etc.). The stroke weights
> are designed specifically for these 4 sizes on screen.

---

## Icon Grid

Every Carbon icon is drawn on a **32×32 unit grid** at the base, then
scaled to the 4 output sizes. The grid defines:

| Zone | Purpose |
|---|---|
| **Live area** | Inner 28×28 area — primary shapes go here |
| **Trim area** | 2px edge — must remain clear for optical balance |
| **Baseline shape** | Minimum distinguishable element at smallest size |

Key rules from the Carbon icon grid:
- Strokes: 2px at 32px grid → proportional at all sizes
- Curves use 45° angles and 90° angles primarily
- Negative (white) space within icons should feel balanced, not crowded

---

## Color Usage

Icons follow the same semantic token system as all Carbon color:

| Context | Token | Hex (White theme) |
|---|---|---|
| Primary icon | `$icon-primary` | `#161616` |
| Secondary / decorative | `$icon-secondary` | `#525252` |
| Interactive (link/button) | `$icon-interactive` | `#0f62fe` |
| On colored background | `$icon-on-color` | `#ffffff` |
| Disabled | `$icon-disabled` | `#c6c6c6` |
| Inverse | `$icon-inverse` | `#ffffff` |
| Error status | `$support-error` | `#da1e28` |
| Warning status | `$support-warning` | `#f1c21b` |
| Success status | `$support-success` | `#24a148` |
| Info status | `$support-info` | `#0043ce` |

> Never use decorative colors on icons that have functional meaning.
> Status icons (checkmark, warning, error X) must always use `$support-*` tokens.

---

## Icon Packages

```bash
# React
npm install @carbon/icons-react

# SVGs (all sizes)
npm install @carbon/icons

# Web components
npm install @carbon/web-components
```

### React Usage

```jsx
import { Add, CheckmarkFilled, Warning } from '@carbon/icons-react';

// Default 16px
<Add />

// Custom size
<Add size={24} />

// With aria label
<Warning size={20} aria-label="Warning" />

// Disabled appearance (via CSS class, not prop)
<CheckmarkFilled size={16} className="icon-disabled" />
```

---

## Naming Convention

Carbon icons follow a descriptive naming pattern:
- PascalCase in React (`<ArrowRight />`, `<ChevronDown />`)
- Kebab-case in SVG files (`arrow--right.svg`, `chevron--down.svg`)
- Size suffix in SVG folders (`/16/arrow--right.svg`, `/24/arrow--right.svg`)
- Filled variants get suffix: `CheckmarkFilled`, `WarningFilled`

---

## Common Icons Reference

| Name | Usage |
|---|---|
| `Add` / `Subtract` | Add / Remove items |
| `ArrowRight` | Directional navigation, CTA |
| `ChevronDown` / `ChevronRight` | Expand/collapse, nav |
| `Close` | Dismiss, close panel |
| `Menu` | Navigation hamburger |
| `Search` | Search field trigger |
| `Settings` | Configuration |
| `User` / `UserAvatar` | Account, profile |
| `Checkmark` / `CheckmarkFilled` | Success, complete |
| `Warning` / `WarningFilled` | Caution |
| `ErrorFilled` | Critical error |
| `InformationFilled` | Info tooltip |
| `Download` | Download action |
| `Upload` | Upload action |
| `Launch` | External link indicator |
| `Edit` | Inline edit |
| `TrashCan` | Delete |
| `Copy` | Copy to clipboard |

Full searchable library: https://carbondesignsystem.com/elements/icons/library/

---

## Icon Accessibility

1. **Decorative icons:** Add `aria-hidden="true"` — no label needed
2. **Standalone icon buttons:** Add visible or `aria-label`
3. **Icon + label pairs:** Icon is decorative; label carries the meaning
4. **Status icons:** Always pair with text for color-blind users

```jsx
// Decorative — hidden from screen readers
<CheckmarkFilled aria-hidden={true} />

// Standalone interactive — explicit label
<button aria-label="Close dialog"><Close size={20} aria-hidden={true} /></button>
```

---

## Icons in Presentations

For presentations and slides:

- Use 24px or 32px for body-level icons (visible at scale)
- Use 32px for callout icons, section markers
- Prefer `$icon-primary` on light backgrounds, `$icon-inverse` on dark
- Pair every icon with a text label — presentations are often printed/exported
- Do not resize icon SVGs to non-standard sizes — use 24px or 32px
