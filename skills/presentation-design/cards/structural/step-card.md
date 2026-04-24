# step-card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

> Diagonal "stair" of 3-5 steps. Each step shows a circle (with optional
> icon), a heading and a body. Steps ascend from the bottom-left to the
> top-right of the card area, with optional dashed connector lines.

## When to use

- Methodology / engagement model walk-throughs.
- Maturity ladders and capability build-ups.
- Anything that is **sequential** AND has a sense of **upward
  progression** (process flow alone â†’ use `process-flow-card`).

## Content schema

```yaml
type: step-card
content:
  steps:
    - title: "Assess"
      body:  "Audit the agent landscape and governance gaps."
      icon:  "search"
    - title: "Design"
      body:  "Define factsheets, policy gates and the operating model."
      icon:  "draw"
    - title: "Build"
      body:  "Stand up registry, observability and HITL controls."
      icon:  "build"
    - title: "Operate"
      body:  "Continuous rationalisation and policy enforcement."
      icon:  "rocket_launch"
```

## Per-step keys

| key       | type   | required | description                          |
|-----------|--------|----------|--------------------------------------|
| `title`   | string | recommended | Short heading next to the circle.  |
| `body`    | string | optional | One-line description.                |
| `icon`    | string | optional | Material Symbols / Phosphor name.    |

## Tokens (variant `card--step`)

| token                                          | default                | purpose                              |
|------------------------------------------------|------------------------|--------------------------------------|
| `--card-step-step-circle-radius`               | `32`                   | px radius of each step circle        |
| `--card-step-step-circle-stroke-color`         | `var(--color-primary)` | circle outline                       |
| `--card-step-step-circle-stroke-width`         | `2.5`                  | px                                   |
| `--card-step-step-circle-fill-color`           | `var(--color-surface)` | circle interior                      |
| `--card-step-step-icon-color`                  | `var(--color-primary)` | icon glyph                           |
| `--card-step-step-icon-size`                   | `28`                   | px                                   |
| `--card-step-step-heading-font-size`           | `14`                   |                                      |
| `--card-step-step-heading-font-color`          | `var(--color-text-default)` |                                |
| `--card-step-step-heading-font-weight`         | `bold`                 |                                      |
| `--card-step-step-body-font-size`              | `11`                   |                                      |
| `--card-step-step-body-font-color`             | `var(--color-text-muted)` |                                   |
| `--card-step-step-text-gap`                    | `12`                   | px gap from circle to text           |
| `--card-step-step-connector-visible`           | `true`                 | draw connector lines                 |
| `--card-step-step-connector-color`             | `var(--color-border)`  |                                      |
| `--card-step-step-connector-width`             | `1.5`                  |                                      |
| `--card-step-step-connector-dashed`            | `true`                 |                                      |

## Notes

- Recommended layout: `grid-1x1`. The card needs the full canvas width
  to render the diagonal cleanly.
- Number of steps: 3, 4 or 5. With more, text overlap becomes likely.
- Icons fall back gracefully if the name is unknown â€” the circle still
  draws.
