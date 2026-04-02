# Grid 3×3 Layout

Three rows, three columns — nine cards in a 3×3 matrix.

## Pictogram

```
┌─────────────────────────────────────────────────────────────────┐
│  [logo-primary]    [slide-title]          [logo-secondary]     │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐      │
│  │   Card 1     │  │   Card 2     │  │    Card 3        │      │
│  └──────────────┘  └──────────────┘  └──────────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐      │
│  │   Card 4     │  │   Card 5     │  │    Card 6        │      │
│  └──────────────┘  └──────────────┘  └──────────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐      │
│  │   Card 7     │  │   Card 8     │  │    Card 9        │      │
│  └──────────────┘  └──────────────┘  └──────────────────┘      │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  [footer-text]                              [page-number]      │
└─────────────────────────────────────────────────────────────────┘
```

## Purpose

Dense grid — nine items for comprehensive comparison or feature matrix.

## Card Count

9

## Placement Map

| Slot | Position | Size |
|------|----------|------|
| 1 | Row 1, Col 1 | 33% width × 33% body height |
| 2 | Row 1, Col 2 | 33% width × 33% body height |
| 3 | Row 1, Col 3 | 33% width × 33% body height |
| 4 | Row 2, Col 1 | 33% width × 33% body height |
| 5 | Row 2, Col 2 | 33% width × 33% body height |
| 6 | Row 2, Col 3 | 33% width × 33% body height |
| 7 | Row 3, Col 1 | 33% width × 33% body height |
| 8 | Row 3, Col 2 | 33% width × 33% body height |
| 9 | Row 3, Col 3 | 33% width × 33% body height |

## Supported Overrides

All `.slide-base` tokens. Card gap via `--canvas-card-gap`.

## Limitations

- Cards beyond 9 are ignored.
- Very compact — best for icons, KPIs, or single-line labels.
