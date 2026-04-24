# Gantt Chart Card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

Timeline card that renders a Gantt chart from structured YAML â€” no image needed.
Works at full-slide width (full-blown mode) and inside small card slots (condensed
mode, activated automatically when the slot width falls below
`--card-gantt-condensed-threshold`).

The card inherits the standard card chrome: title, header line, subtitle, footer.

## Layout

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  [card-title]                                                               â”‚
â”‚  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€  â”‚
â”‚                                                                             â”‚
â”‚  Task name                â”‚  0   1   2   3   4   5   6   7   8   9   10   â”‚
â”‚  â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”¼â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„â”„  â”‚
â”‚  â”€â”€ SECTION HEADER â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€   â”‚
â”‚  Task A                  â”‚  â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ                                   â”‚
â”‚  Task B                  â”‚          â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ                     â”‚
â”‚  Task C  (crit)          â”‚                 â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ(crit-red)                â”‚
â”‚  Milestone â—†             â”‚                          â—†                      â”‚
â”‚  Task D (progress)       â”‚  â–ˆâ–ˆâ–ˆâ–ˆâ–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘ (40%)                       â”‚
â”‚                                                                             â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

## Required Fields

```yaml
type: gantt-chart-card
content:
  sections:
    - tasks:
        - label: "My Task"
          start: 0
          duration: 3
```

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `unit` | `days\|weeks\|months` | `weeks` | Unit for all start/duration values |
| `title_col_label` | str | `Task` | Column header for the task-name column |
| `condensed` | bool | false | Force condensed mode regardless of box width |
| section `title` | str | â€” | Section header label; groups tasks visually |
| task `id` | str | â€” | Short identifier shown inside the bar |
| task `start` | int \| `"after:<id>"` | 0 | Offset from chart start, or dependency chain |
| task `duration` | int | 1 | Length in `unit` |
| task `progress` | int 0â€“100 | 0 | Completed fraction â€” shaded as progress overlay |
| task `color` | hex | token | Override bar fill colour |
| task `crit` | bool | false | Mark bar as critical (red fill) |
| task `milestone` | bool | false | Render as a diamond marker instead of a bar |
| `start_date` | `YYYY-MM-DD` \| `YYYY-MM` | â€” | Anchor chart dates so overlays can also be expressed as ISO dates |
| `overlays` | list | â€” | Named background spans (holidays, code-freeze, UAT, sprints, â€¦) rendered as shaded chart bands. |
| overlay `label` | str | â€” | Text shown in the header row above the band |
| overlay `start` | int \| ISO date | 0 | Band start offset / date (same rules as task `start`) |
| overlay `duration` | int | 1 | Band length in `unit` |
| overlay `color` | hex | token | Per-band fill colour â€” lets you colour-code overlay types |

## Supported Overrides

All `.card--gantt-chart` tokens via `style_overrides:` using
`card_gantt_*` key format.

## Design Tokens Used

| Token | Default | Role |
|-------|---------|------|
| `--card-gantt-label-col-pct` | 28 | % of body width for task names |
| `--card-gantt-condensed-threshold` | 320 | px â€” auto-condensed below this width |
| `--card-gantt-header-height` | 20 | axis tick-label row height |
| `--card-gantt-row-height` | 22 | task row height |
| `--card-gantt-section-height` | 18 | section header row height |
| `--card-gantt-grid-color` | `var(--color-border)` | grid line colour |
| `--card-gantt-section-fill` | `var(--color-surface-subtle)` | section bg |
| `--card-gantt-section-font-size` | 10 | section label size |
| `--card-gantt-section-font-color` | `var(--color-text-subtle)` | section text |
| `--card-gantt-label-font-size` | 10 | task label size |
| `--card-gantt-label-font-color` | `var(--color-text-default)` | task label colour |
| `--card-gantt-tick-font-size` | 9 | axis tick size |
| `--card-gantt-tick-font-color` | `var(--color-text-muted)` | axis tick colour |
| `--card-gantt-bar-color` | `var(--color-accent)` | default bar fill |
| `--card-gantt-bar-crit-color` | `var(--color-error)` | critical bar fill |
| `--card-gantt-bar-radius` | 3 | bar corner radius |
| `--card-gantt-bar-text-font-size` | 8 | bar label size |
| `--card-gantt-bar-text-font-color` | `var(--color-on-accent)` | bar label colour |
| `--card-gantt-progress-color` | `var(--color-primary)` | progress overlay fill |
| `--card-gantt-milestone-color` | `var(--color-warning)` | milestone marker fill |
| `--card-gantt-overlay-fill` | `#EFF6FF` | default overlay band fill |
| `--card-gantt-overlay-label-font-size` | 8 | band label size |
| `--card-gantt-overlay-label-color` | `var(--color-text-muted)` | band label colour |

## Example â€” Full-blown (full-slide)

```yaml
type: gantt-chart-card
title: "Q1 / Q2 Project Plan"
content:
  unit: weeks
  title_col_label: "Workstream"
  sections:
    - title: "Discovery"
      tasks:
        - id: "W1"
          label: "Stakeholder interviews"
          start: 0
          duration: 2
        - id: "W2"
          label: "AS-IS analysis"
          start: 1
          duration: 3
    - title: "Design"
      tasks:
        - id: "W3"
          label: "Architecture blueprint"
          start: "after:W2"
          duration: 4
          progress: 60
        - id: "W4"
          label: "Security review"
          start: "after:W3"
          duration: 2
          crit: true
    - title: "Milestones"
      tasks:
        - label: "Design freeze"
          start: 9
          duration: 0
          milestone: true
  start_date: "2026-01-03"
  overlays:
    - label: "New Year"
      start: "2026-01-01"
      duration: 1
      color: "#EFF6FF"
    - label: "Easter"
      start: "2026-04-07"
      duration: 1
      color: "#EFF6FF"
    - label: "Code Freeze"
      start: "2026-03-30"
      duration: 2
      color: "#FFF3E0"
    - label: "UAT"
      start: "2026-04-14"
      duration: 2
      color: "#FFF0F0"
```

## Example â€” Condensed (quarter-slide slot)

```yaml
type: gantt-chart-card
title: "Timeline"
content:
  unit: months
  condensed: true
  sections:
    - tasks:
        - label: "Phase 1"
          start: 0
          duration: 3
          color: "#003087"
        - label: "Phase 2"
          start: 3
          duration: 4
        - label: "Phase 3"
          start: 7
          duration: 3
```
