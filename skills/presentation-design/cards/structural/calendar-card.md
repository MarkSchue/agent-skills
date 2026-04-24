# calendar-card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

> A row of N consecutive month grids (Mon-Sun) with the ability to
> highlight contiguous date ranges as rounded coloured pills, plus an
> optional auto-generated legend. Use for project schedules, sprint
> plans, holiday calendars, release timelines.

## When to use

- Project phase / sprint plans where the **calendar context** matters
  (weekends, weeks).
- Holiday or blackout overviews.
- "Save the date" comms with multiple parallel tracks.

For pure timeline visuals without weekday context, use `timeline-card`
(linear) or `gantt-chart-card` (with bars and dependencies).

## Content schema

```yaml
type: calendar-card
content:
  # Either an explicit list of months …
  months:
    - "2025-04"
    - "2025-05"
    - "2025-06"
  # … or start + count:
  # start: "2025-04"
  # count: 3

  highlights:
    - { start: "2025-04-01", end: "2025-04-04", color: "#E5E54E", label: "Project Phase 1" }
    - { start: "2025-04-07", end: "2025-04-11", color: "#E5E54E", label: "Project Phase 1" }
    - { start: "2025-04-14", end: "2025-05-30", color: "#3344E5", label: "Project Phase 2" }
    - { start: "2025-06-11", end: "2025-06-13", color: "#1FBF7F", label: "Project Phase 3" }

  legend: true   # default — derive from highlights' unique labels
  # legend: [{label: "Phase 1", color: "#E5E54E"}, …]   # explicit override
  # legend: false  # hide
```

## Highlight keys

| key     | type    | required | description                                  |
|---------|---------|----------|----------------------------------------------|
| `start` | date    | required | ISO `YYYY-MM-DD`. Inclusive.                 |
| `end`   | date    | optional | ISO date, defaults to `start` (single day).  |
| `color` | hex str | optional | Pill fill. Falls back to `--color-primary`.  |
| `label` | string  | optional | Used in the legend (de-duplicated).          |

Multi-week or multi-month ranges are rendered as one pill **per
week-row**. Out-of-month days inside a week never get a pill.

## Tokens (variant `card--calendar`)

| token                                          | default                    | purpose                          |
|------------------------------------------------|----------------------------|----------------------------------|
| `--card-calendar-month-title-font-size`        | `14`                       | "APRIL 2025" header              |
| `--card-calendar-month-title-font-color`       | `var(--color-primary)`     |                                  |
| `--card-calendar-month-title-font-weight`      | `bold`                     |                                  |
| `--card-calendar-weekday-font-size`            | `10`                       | MO TU WE TH FR SA SU             |
| `--card-calendar-weekday-font-color`           | `var(--color-text-muted)`  |                                  |
| `--card-calendar-day-font-size`                | `11`                       |                                  |
| `--card-calendar-day-color`                    | `var(--color-text-default)`| in-month days                    |
| `--card-calendar-day-out-color`                | `var(--color-border)`      | days outside the month           |
| `--card-calendar-day-highlight-color`          | `#FFFFFF`                  | day numbers on top of pills      |
| `--card-calendar-cell-gap`                     | `2`                        | px between cells                 |
| `--card-calendar-month-gap`                    | `24`                       | px between month grids           |
| `--card-calendar-pill-padding-x`               | `4`                        | horizontal inset of pills        |
| `--card-calendar-pill-radius`                  | `auto`                     | px or `auto` (= `cell_h / 2`)    |
| `--card-calendar-legend-font-size`             | `11`                       |                                  |
| `--card-calendar-legend-font-color`            | `var(--color-text-default)`|                                  |
| `--card-calendar-legend-dot-radius`            | `7`                        | px                               |
| `--card-calendar-legend-gap`                   | `24`                       | reserved for future horizontal legend |

## Notes

- Recommended layout: `grid-1x1`. The card auto-distributes month grids
  across the card width.
- Cell width derives from card width (no manual sizing needed).
- Cell height derives from remaining vertical space after the legend
  reservation.
- The legend stacks vertically in the bottom-left of the card body.
- Multiple highlights with the **same `label`** are merged into a single
  legend entry (the colour of the **first** occurrence is used).
