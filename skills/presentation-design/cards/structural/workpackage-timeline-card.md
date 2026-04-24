# workpackage-timeline-card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

> A horizontal project-phase timeline. Each **workpackage** sits above
> the bar with its title, body, person-day count and calendar week.
> **Cross-workpackages** span the full width below the bar (e.g.
> Project Management, Tech Lead). Ideal for project kick-off decks.

## When to use

- A "Project Timeline — Phase XX" overview slide.
- Anywhere you need to express **per-WP effort + calendar context +
  cross-cutting workpackages** in a single visual.

For a generic linear timeline without effort/cross-WPs, use
`timeline-card`. For a Gantt with bars and dependencies, use
`gantt-chart-card`.

## Content schema

```yaml
type: workpackage-timeline-card
content:
  workpackages:
    - { title: "Setup",                    body: "Setup of development project",            kw: "KW17", pt: 3   }
    - { title: "Functional Specification", body: "Definition of user stories…",             kw: "KW20", pt: 14  }
    - { title: "Technical Specification",  body: "Design and design decisions…",            kw: "KW21", pt: 10  }
    - { title: "Development",              body: "Development in 2-week sprints…",          kw: "KW30", pt: 112 }
    - { title: "Test",                     body: "User acceptance test, bug fixing…",       kw: "KW32", pt: 23  }
    - { title: "Training & Rollout",       body: "Training of end users…",                  kw: "KW34", pt: 8, end: true }
  cross_workpackages:
    - { title: "Project Management in agile approach",
        body:  "Preparation and conduction of all relevant events in an agile project.",
        pt:    18 }
    - { title: "Technical Lead",
        body:  "Preparation and conduction of all relevant architecture artifacts.",
        pt:    7  }
```

## Field reference

### Workpackage (`workpackages[]`)

| key     | type   | required | description                                              |
|---------|--------|----------|----------------------------------------------------------|
| `title` | string | required | Bold heading above the bar.                              |
| `body`  | string | optional | Description, wrapped to ~5 lines max.                    |
| `kw`    | string | optional | Calendar-week label below the bar (e.g. `"KW17"`).       |
| `pt`    | number | optional | Person-day count, rendered as `"X PT"` above the marker. |
| `end`   | bool   | optional | If `true`, this WP is rendered as the **end-arrow** (rightmost position) with the inline KW label after the arrow tip. Use on the last WP only. |

### Cross-workpackage (`cross_workpackages[]`)

| key     | type   | required | description                                       |
|---------|--------|----------|---------------------------------------------------|
| `title` | string | required | Bold heading.                                     |
| `body`  | string | optional | One-line description.                             |
| `pt`    | number | optional | PT total, right-aligned at the end of the row.    |

## Tokens (variant `card--workpackage-timeline`)

| token                                                       | default                  |
|-------------------------------------------------------------|--------------------------|
| `--card-workpackage-timeline-wp-heading-font-size`          | `12`                     |
| `--card-workpackage-timeline-wp-heading-font-color`         | `var(--color-text-default)` |
| `--card-workpackage-timeline-wp-heading-font-weight`        | `bold`                   |
| `--card-workpackage-timeline-wp-body-font-size`             | `10`                     |
| `--card-workpackage-timeline-wp-body-font-color`            | `var(--color-text-muted)`|
| `--card-workpackage-timeline-bar-height`                    | `6`                      |
| `--card-workpackage-timeline-bar-color-start`               | `var(--color-primary)`   |
| `--card-workpackage-timeline-bar-color-end`                 | `var(--color-accent)`    |
| `--card-workpackage-timeline-marker-font-size`              | `11`                     |
| `--card-workpackage-timeline-marker-color`                  | `var(--color-text-default)` |
| `--card-workpackage-timeline-kw-font-size`                  | `11`                     |
| `--card-workpackage-timeline-end-arrow-size`                | `10`                     |
| `--card-workpackage-timeline-end-arrow-color`               | `var(--color-accent)`    |
| `--card-workpackage-timeline-cross-heading-font-size`       | `12`                     |
| `--card-workpackage-timeline-cross-body-font-size`          | `10`                     |
| `--card-workpackage-timeline-cross-pt-font-size`            | `12`                     |
| `--card-workpackage-timeline-cross-row-gap`                 | `8`                      |

## Notes

- The bar is rendered as a series of 60 colour-interpolated rect slices
  to approximate a smooth gradient (no native gradient support in the
  shared element format).
- WP positions are evenly distributed across the bar. To control
  spacing, vary the number of WPs.
- The recommended layout is `grid-1x1`. The card needs the full slide
  width to look balanced.
