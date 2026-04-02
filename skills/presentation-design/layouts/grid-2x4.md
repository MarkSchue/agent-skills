# Grid 2×4 Layout

Two rows, four columns — eight cards in a 2×4 matrix.

## Pictogram

```
┌─────────────────────────────────────────────────────────────────┐
│  [logo-primary]    [slide-title]          [logo-secondary]     │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐      │
│  │  Card 1  │ │  Card 2  │ │  Card 3  │ │   Card 4     │      │
│  │          │ │          │ │          │ │              │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐      │
│  │  Card 5  │ │  Card 6  │ │  Card 7  │ │   Card 8     │      │
│  │          │ │          │ │          │ │              │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘      │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  [footer-text]                              [page-number]      │
└─────────────────────────────────────────────────────────────────┘
```

## Purpose

Eight compact items — process steps, feature tiles, or dense comparison.

## Card Count

8

## Placement Map

| Slot | Position | Size |
|------|----------|------|
| 1 | Row 1, Col 1 | 25% width × 50% body height |
| 2 | Row 1, Col 2 | 25% width × 50% body height |
| 3 | Row 1, Col 3 | 25% width × 50% body height |
| 4 | Row 1, Col 4 | 25% width × 50% body height |
| 5 | Row 2, Col 1 | 25% width × 50% body height |
| 6 | Row 2, Col 2 | 25% width × 50% body height |
| 7 | Row 2, Col 3 | 25% width × 50% body height |
| 8 | Row 2, Col 4 | 25% width × 50% body height |

## Supported Overrides

All `.slide-base` tokens. Card gap via `--canvas-card-gap`.

## Limitations

- Cards beyond 8 are ignored.
- Very compact — best for KPIs, icons, or minimal text.
