# Grid 3×2 Layout

Three rows, two columns — six cards in a 3×2 matrix.

## Pictogram

```
┌─────────────────────────────────────────────────────────────────┐
│  [logo-primary]    [slide-title]          [logo-secondary]     │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  ┌────────────────────────┐  ┌────────────────────────────┐    │
│  │        Card 1          │  │         Card 2             │    │
│  └────────────────────────┘  └────────────────────────────┘    │
│  ┌────────────────────────┐  ┌────────────────────────────┐    │
│  │        Card 3          │  │         Card 4             │    │
│  └────────────────────────┘  └────────────────────────────┘    │
│  ┌────────────────────────┐  ┌────────────────────────────┐    │
│  │        Card 5          │  │         Card 6             │    │
│  └────────────────────────┘  └────────────────────────────┘    │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  [footer-text]                              [page-number]      │
└─────────────────────────────────────────────────────────────────┘
```

## Purpose

Six items in a tall grid — team profiles, feature comparison, or categorized detail.

## Card Count

6

## Placement Map

| Slot | Position | Size |
|------|----------|------|
| 1 | Row 1, Col 1 | 50% width × 33% body height |
| 2 | Row 1, Col 2 | 50% width × 33% body height |
| 3 | Row 2, Col 1 | 50% width × 33% body height |
| 4 | Row 2, Col 2 | 50% width × 33% body height |
| 5 | Row 3, Col 1 | 50% width × 33% body height |
| 6 | Row 3, Col 2 | 50% width × 33% body height |

## Supported Overrides

All `.slide-base` tokens. Card gap via `--canvas-card-gap`.

## Limitations

- Cards beyond 6 are ignored.
- Compact vertical space per card.
