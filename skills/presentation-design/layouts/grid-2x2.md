# Grid 2×2 Layout

Two rows, two columns — four equal-sized cards in a 2×2 matrix.

## Pictogram

```
┌─────────────────────────────────────────────────────────────────┐
│  [logo-primary]    [slide-title]          [logo-secondary]     │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  ┌────────────────────────┐  ┌────────────────────────────┐    │
│  │        Card 1          │  │         Card 2             │    │
│  │                        │  │                            │    │
│  └────────────────────────┘  └────────────────────────────┘    │
│  ┌────────────────────────┐  ┌────────────────────────────┐    │
│  │        Card 3          │  │         Card 4             │    │
│  │                        │  │                            │    │
│  └────────────────────────┘  └────────────────────────────┘    │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  [footer-text]                              [page-number]      │
└─────────────────────────────────────────────────────────────────┘
```

## Purpose

Quadrant view — four balanced content blocks, SWOT analysis, or 2×2 comparison matrix.

## Card Count

4

## Placement Map

| Slot | Position | Size |
|------|----------|------|
| 1 | Top-left | 50% width × 50% body height |
| 2 | Top-right | 50% width × 50% body height |
| 3 | Bottom-left | 50% width × 50% body height |
| 4 | Bottom-right | 50% width × 50% body height |

## Supported Overrides

All `.slide-base` tokens. Card gap via `--canvas-card-gap`.

## Limitations

- Cards beyond 4 are ignored.

## Example

```markdown
## SWOT Analysis
### Strengths
```yaml
type: text-card
content:
  body: "Strong brand recognition and loyal customer base."
```
### Weaknesses
```yaml
type: text-card
content:
  body: "Limited presence in APAC markets."
```
### Opportunities
```yaml
type: text-card
content:
  body: "Growing demand for sustainable products."
```
### Threats
```yaml
type: text-card
content:
  body: "Increasing regulatory requirements in EU."
```
```
