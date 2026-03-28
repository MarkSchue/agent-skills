# Atom: chart-gantt

```yaml
id: chart-gantt
type: data-viz
description: Horizontal timeline Gantt chart with labeled tasks and start/end dates.
tags: [chart, timeline, project, gantt, schedule]
preview: previews/atoms/chart-gantt.png
svg-source: atoms/svg/chart-gantt.svg
```

## Visual Properties

| Property | Token |
|---|---|
| Task bar fill | `{{theme.color.primary}}` |
| Milestone marker | `{{theme.color.accent}}` |
| Row separator | `{{theme.shape.divider}}` |
| Axis / grid lines | `{{theme.shape.thin-line}}` |
| Label text | `{{theme.color.on-surface}}` |
| Background | `{{theme.color.surface}}` |
| Today marker | `{{theme.color.error}}` |

## Data Input Schema

```yaml
data-input-schema:
  tasks:
    type: list[object]
    required: true
    items:
      name:      {type: string, required: true}
      start:     {type: date, required: true,  format: "YYYY-MM-DD"}
      end:       {type: date, required: true,  format: "YYYY-MM-DD"}
      progress:  {type: number, required: false, min: 0, max: 100}  # % complete
      type:      {type: enum[task, milestone], required: false, default: task}
      color-token: {type: color-token, required: false}  # override for this row
  show-today:
    type: boolean
    required: false
    default: true
  date-format:
    type: string
    required: false
    default: "MMM YYYY"
```

## Behavior

- Timeline axis is auto-scaled to span from the earliest start to the latest end date.
- Tasks are rendered as horizontal bars; milestones as diamond markers.
- `progress` value shades the completed portion in a lighter tint of `primary`.
- If `show-today` is true and today falls within the timeline range, a vertical marker is shown.
- Maximum tasks rendered without truncation: 10. If more, paginate or compress to fit.

## Example Fenced Block in Markdown

```chart:gantt
tasks:
  - name: "Discovery"
    start: "2025-01-06"
    end:   "2025-01-17"
    progress: 100
  - name: "Design"
    start: "2025-01-20"
    end:   "2025-02-14"
    progress: 60
  - name: "Build"
    start: "2025-02-17"
    end:   "2025-03-28"
    progress: 0
show-today: true
```

## Notes

- SVG source `atoms/svg/chart-gantt.svg` is a placeholder recolored at assembly.
- Date parsing accepts ISO 8601 dates; other formats must be declared via `date-format`.
