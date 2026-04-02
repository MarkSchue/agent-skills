# Grid 1×4 Layout

One row, four equal-width cards.

## Pictogram

```
┌─────────────────────────────────────────────────────────────────┐
│  [logo-primary]    [slide-title]          [logo-secondary]     │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐      │
│  │          │ │          │ │          │ │              │      │
│  │  Card 1  │ │  Card 2  │ │  Card 3  │ │   Card 4     │      │
│  │          │ │          │ │          │ │              │      │
│  │          │ │          │ │          │ │              │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘      │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  [footer-text]                              [page-number]      │
└─────────────────────────────────────────────────────────────────┘
```

## Purpose

Four KPIs in a row, four-step process, or compact comparison of four items.

## Card Count

4

## Placement Map

| Slot | Position | Size |
|------|----------|------|
| 1 | Column 1 | 25% width × 100% body height |
| 2 | Column 2 | 25% width × 100% body height |
| 3 | Column 3 | 25% width × 100% body height |
| 4 | Column 4 | 25% width × 100% body height |

## Supported Overrides

All `.slide-base` tokens. Card gap via `--canvas-card-gap`.

## Limitations

- Cards beyond 4 are ignored.
- Narrow cards — best suited for KPIs or short text.

## Example

```markdown
## Q3 Metrics
### Revenue
```yaml
type: kpi-card
content:
  value: "$4.2M"
  trend: "up"
```
### Users
```yaml
type: kpi-card
content:
  value: "12.5K"
  trend: "up"
```
### Churn
```yaml
type: kpi-card
content:
  value: "2.1%"
  trend: "down"
```
### NPS
```yaml
type: kpi-card
content:
  value: "72"
  trend: "neutral"
```
```
