# numbered-list-card

**Molecule slug:** `numbered-list-card`
**Domain:** strategy
**Category:** List / Process

A row-based list card with three horizontal zones per row: a **number / badge / icon** gutter
on the left, an optional **bold headline** in the centre, and **body text** on the right.
Horizontal dividers separate rows. The number type and all column proportions are fully
configurable.

## Design anatomy

```
┌──────────────────────────────────────────────────────────────────┐
│  [Optional title header]                                         │
│  01   Bold headline text    Body text wraps in the right column  │
│  ──────────────────────────────────────────────────────────────  │
│  02   Bold headline text    Body text wraps in the right column  │
│  ──────────────────────────────────────────────────────────────  │
│  03   (no headline = full   Body text using remaining width)     │
│  ──────────────────────────────────────────────────────────────  │
│  04   Bold headline text    Body text …                          │
└──────────────────────────────────────────────────────────────────┘
```

### Number zone variants

| `number-type` | Appearance |
|---|---|
| `number` | Plain colored text, zero-padded — **01 02 03** (default) |
| `badge`   | Filled circle / rounded-rect / square with number in centre |
| `icon`    | Icon rendered from the item's `icon` field |
| `none`    | Gutter hidden; headline and body fill the full row width |

## Parameters

| Parameter            | Type   | Default              | Description |
|----------------------|--------|----------------------|-------------|
| `title`              | string | —                    | Optional card header title |
| `items`              | list   | **required**         | Array of row objects (see below) |
| `number-type`        | enum   | `number`             | `number` · `badge` · `icon` · `none` |
| `number-color`       | color  | `primary`            | Plain number text color |
| `number-size`        | int    | auto                 | Explicit font-size in px for the number |
| `number-align`       | enum   | `left`               | `left` · `center` — alignment within the number column |
| `number-col-frac`    | float  | `0.10`               | Fraction of inner width for the number gutter (0–1) |
| `badge-fill`         | color  | `primary`            | Badge background color |
| `badge-text-color`   | color  | `on-primary`         | Text color inside the badge |
| `badge-shape`        | enum   | `rounded`            | `rounded` · `circle` · `square` |
| `badge-size`         | int    | auto                 | Explicit badge diameter in px |
| `headline-col-frac`  | float  | `0.30`               | Fraction of inner width for the headline column (0–1) |
| `headline-size`      | int    | auto                 | Explicit font-size in px for headlines |
| `headline-color`     | color  | `on-surface`         | Headline text color |
| `body-size`          | int    | auto                 | Explicit font-size in px for body text |
| `body-color`         | color  | `on-surface-variant` | Body text color |
| `show-dividers`      | bool   | `true`               | Draw horizontal dividers between rows |
| `divider-color`      | color  | `border-subtle`      | Row divider color |
| `row-valign`         | enum   | `middle`             | `middle` · `top` — vertical alignment of body text within its row |
| `column-gap`         | int    | spacing m (16)       | Gap in px between the three columns |
| `show-header`        | bool   | auto                 | Show/hide card title header block |
| `show-header-line`   | bool   | `true`               | Line below the title header |
| `bg-color`           | color  | `bg-card`            | Card background color override |

### Item object fields

| Field      | Type   | Required | Description |
|------------|--------|----------|-------------|
| `body`     | string | yes      | Main row text (right column) |
| `headline` | string | no       | Bold centre text; if no item has a headline the column is hidden |
| `number`   | string | no       | Override the auto-generated label (for `number` and `badge` types) |
| `icon`     | string | no       | Icon used when `number-type: icon` |
| `color`    | color  | no       | Per-item accent color (overrides `number-color` / `badge-fill`) |

## Examples

### Plain numbered list (matches screenshot)

```yaml
molecule: numbered-list-card
number-type: number
number-color: primary
items:
  - headline: Lorem ipsum dolor
    body: Lorem ipsum dolor sit amet, consetetur Lorem ipsum dolor sit amet, dolor sit amet,
  - headline: Lorem ipsum dolor
    body: Lorem ipsum dolor sit amet, consetetur Lorem ipsum dolor sit amet, dolor sit amet,
  - headline: Lorem ipsum dolor
    body: Lorem ipsum dolor sit amet, consetetur Lorem ipsum dolor sit amet, dolor sit amet,
```

### Badge variant with circle shape

```yaml
molecule: numbered-list-card
title: Key risk areas
number-type: badge
badge-shape: circle
badge-fill: primary
items:
  - headline: Market volatility
    body: Sudden shifts in end-market demand can affect forecast accuracy significantly.
    color: warning
  - headline: Regulatory change
    body: Upcoming frameworks in the EU may require product re-certification by Q2.
  - headline: Talent retention
    body: Attrition in senior engineering roles remains above industry average.
```

### Icon list — no headline column

```yaml
molecule: numbered-list-card
number-type: icon
items:
  - icon: check_circle
    body: Automated test coverage above 85 % across all critical paths
  - icon: check_circle
    body: Staging environment parity with production validated monthly
  - icon: warning
    body: Manual deployment steps still present for the payments service
    color: warning
```

### No gutter — body-only list

```yaml
molecule: numbered-list-card
number-type: none
show-dividers: true
items:
  - body: First consideration spanning across the full row width of the card
  - body: Second consideration with additional context and explanation
  - body: Third consideration listed here for completeness
```

## CSS design tokens

| Token                          | Description                    |
|--------------------------------|--------------------------------|
| `--color-primary`              | Default number / badge color   |
| `--color-on-primary`           | Default badge text color       |
| `--color-on-surface`           | Headline text color            |
| `--color-on-surface-variant`   | Body text color                |
| `--color-border-subtle`        | Row divider color              |
