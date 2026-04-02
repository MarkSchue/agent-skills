# Grid 1×3 Layout

One row, three equal-width cards.

## Pictogram

```
┌─────────────────────────────────────────────────────────────────┐
│  [logo-primary]    [slide-title]          [logo-secondary]     │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐      │
│  │              │  │              │  │                  │      │
│  │   Card 1     │  │   Card 2     │  │    Card 3        │      │
│  │              │  │              │  │                  │      │
│  │              │  │              │  │                  │      │
│  └──────────────┘  └──────────────┘  └──────────────────┘      │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  [footer-text]                              [page-number]      │
└─────────────────────────────────────────────────────────────────┘
```

## Purpose

Three pillars, three KPIs, or a trio of related items.

## Card Count

3

## Placement Map

| Slot | Position | Size |
|------|----------|------|
| 1 | Left third | 33% width × 100% body height |
| 2 | Center third | 33% width × 100% body height |
| 3 | Right third | 33% width × 100% body height |

## Supported Overrides

All `.slide-base` tokens. Card gap via `--canvas-card-gap`.

## Limitations

- Cards beyond 3 are ignored.

## Example

```markdown
## Three Pillars
### Speed
```yaml
type: kpi-card
content:
  value: "2x"
  label: "Faster delivery"
```
### Quality
```yaml
type: kpi-card
content:
  value: "99.9%"
  label: "Uptime"
```
### Cost
```yaml
type: kpi-card
content:
  value: "-30%"
  label: "Infrastructure savings"
```
```
