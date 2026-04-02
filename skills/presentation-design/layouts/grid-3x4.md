# Grid 3×4 Layout

Three rows, four columns — twelve cards in a 3×4 matrix. Maximum density layout.

## Pictogram

```
┌─────────────────────────────────────────────────────────────────┐
│  [logo-primary]    [slide-title]          [logo-secondary]     │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐      │
│  │  Card 1  │ │  Card 2  │ │  Card 3  │ │   Card 4     │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐      │
│  │  Card 5  │ │  Card 6  │ │  Card 7  │ │   Card 8     │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐      │
│  │  Card 9  │ │  Card 10 │ │  Card 11 │ │   Card 12    │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘      │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  [footer-text]                              [page-number]      │
└─────────────────────────────────────────────────────────────────┘
```

## Purpose

Maximum density — twelve items for large comparison grids or icon dashboards.

## Card Count

12

## Placement Map

| Slot | Position | Size |
|------|----------|------|
| 1 | Row 1, Col 1 | 25% width × 33% body height |
| 2 | Row 1, Col 2 | 25% width × 33% body height |
| 3 | Row 1, Col 3 | 25% width × 33% body height |
| 4 | Row 1, Col 4 | 25% width × 33% body height |
| 5 | Row 2, Col 1 | 25% width × 33% body height |
| 6 | Row 2, Col 2 | 25% width × 33% body height |
| 7 | Row 2, Col 3 | 25% width × 33% body height |
| 8 | Row 2, Col 4 | 25% width × 33% body height |
| 9 | Row 3, Col 1 | 25% width × 33% body height |
| 10 | Row 3, Col 2 | 25% width × 33% body height |
| 11 | Row 3, Col 3 | 25% width × 33% body height |
| 12 | Row 3, Col 4 | 25% width × 33% body height |

## Supported Overrides

All `.slide-base` tokens. Card gap via `--canvas-card-gap`.

## Limitations

- Cards beyond 12 are ignored.
- Extremely compact — only suitable for minimal content per card.
