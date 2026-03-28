# Template: row-3

```yaml
id: row-3
type: template
description: >
  Three equal-height rows stacked vertically, each spanning the full content width.
  Suited for listing three objectives, milestones, or focus areas with equal visual weight.
tags: [rows, three-row, stacked, vertical, objectives]
compatible_molecules: [mission-card, stacked-text, kpi-card]
```

## Layout Pictogram

```
┌──────────────────────────────────────────────────────────────────────────┐
│  SLIDE TITLE   ─────────────────────── [header divider]                 │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │                       BLOCK A  (row 1)                        │     │
│  └────────────────────────────────────────────────────────────────┘     │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │                       BLOCK B  (row 2)                        │     │
│  └────────────────────────────────────────────────────────────────┘     │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │                       BLOCK C  (row 3)                        │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                                                                          │
│  ─────── [footer divider]                       [page number]           │
└──────────────────────────────────────────────────────────────────────────┘
```

## Slot Specifications

| Slot | Accepts | Required | Height |
|------|---------|----------|--------|
| Block A | any molecule | yes | `(content_h − 2×gap) / 3` |
| Block B | any molecule | no | same |
| Block C | any molecule | no | same |

## CSS Token Reference

Same tokens as `row-2`. Row count is fixed at 3 by the layout slug.

## Example Usage

```markdown
# Strategic Pillars
<!-- layout: row-3 -->

## Reliability
```yaml
molecule: mission-card
title: Reliability
statement: "99.94 % uptime across all production services."
```

## Performance
```yaml
molecule: mission-card
title: Performance
statement: "Median query latency reduced to 48 ms."
```

## Adoption
```yaml
molecule: mission-card
title: Adoption
statement: "73 % platform adoption rate across business units."
```
```
