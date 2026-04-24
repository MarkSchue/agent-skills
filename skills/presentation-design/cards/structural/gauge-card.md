# gauge-card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

> Row of 2-5 donut gauges, each showing a percentage with a heading and
> optional body text. KPI / dashboard pattern.

## When to use

- Programme / portfolio dashboards.
- "Where we stand" status updates.
- Comparing multiple percentage metrics side-by-side.

## Content schema

```yaml
type: gauge-card
content:
  gauges:
    - value: 84
      heading: "Agent Coverage"
      body:    "of deployed agents catalogued"
    - value: 67
      heading: "Policy Enforcement"
      body:    "of decisions gated at runtime"
    - value: 92
      heading: "HITL Compliance"
      body:    "of high-risk actions reviewed"
    - value: 38
      heading: "Cost Reduction"
      body:    "vs. ungoverned baseline"
      color:   "#E5546A"
```

## Per-gauge keys

| key       | type    | required | description                            |
|-----------|---------|----------|----------------------------------------|
| `value`   | number  | required | 0-100. Clamped to range.               |
| `heading` | string  | recommended | Label below the ring.                |
| `body`    | string  | optional | Sub-label below the heading.           |
| `color`   | hex str | optional | Override the foreground arc colour.    |
| `icon`    | string  | optional | Reserved (not yet rendered).           |

## Tokens (variant `card--gauge`)

| token                                | default                       | purpose                          |
|--------------------------------------|-------------------------------|----------------------------------|
| `--card-gauge-ring-radius`           | `64`                          | max px radius                    |
| `--card-gauge-ring-thickness`        | `0.22`                        | fraction of radius (0..1)        |
| `--card-gauge-ring-bg-color`         | `var(--color-surface-sunken)` | unfilled track                   |
| `--card-gauge-ring-fg-color`         | `var(--color-primary)`        | filled portion (per-gauge override via `color`) |
| `--card-gauge-value-font-size`       | derived from radius           | % label                          |
| `--card-gauge-value-font-color`      | `var(--color-primary)`        |                                  |
| `--card-gauge-value-font-weight`     | `bold`                        |                                  |
| `--card-gauge-value-suffix`          | `%`                           | unit string                      |
| `--card-gauge-heading-font-size`     | `14`                          |                                  |
| `--card-gauge-heading-font-color`    | `var(--color-text-default)`   |                                  |
| `--card-gauge-heading-font-weight`   | `bold`                        |                                  |
| `--card-gauge-body-font-size`        | `11`                          |                                  |
| `--card-gauge-body-font-color`       | `var(--color-text-muted)`     |                                  |
| `--card-gauge-gauge-gap`             | `16`                          | px between gauges                |

## Notes

- Recommended layout: `grid-1x1`. The card auto-distributes the gauges
  along the card's full width.
- Ring radius is auto-shrunk to fit the slot, but never below 28 px.
- The fill arc starts at 12 o'clock and sweeps clockwise.
