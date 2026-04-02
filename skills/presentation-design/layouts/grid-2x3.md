# Grid 2×3 Layout

Two rows, three columns — six cards in a 2×3 matrix.

## Pictogram

```
┌─────────────────────────────────────────────────────────────────┐
│  [logo-primary]    [slide-title]          [logo-secondary]     │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐      │
│  │   Card 1     │  │   Card 2     │  │    Card 3        │      │
│  │              │  │              │  │                  │      │
│  └──────────────┘  └──────────────┘  └──────────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐      │
│  │   Card 4     │  │   Card 5     │  │    Card 6        │      │
│  │              │  │              │  │                  │      │
│  └──────────────┘  └──────────────┘  └──────────────────┘      │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  [footer-text]                              [page-number]      │
└─────────────────────────────────────────────────────────────────┘
```

## Purpose

Six items — feature grid, team members, or categorized content.

## Card Count

6

## Placement Map

| Slot | Position | Size |
|------|----------|------|
| 1 | Row 1, Col 1 | 33% width × 50% body height |
| 2 | Row 1, Col 2 | 33% width × 50% body height |
| 3 | Row 1, Col 3 | 33% width × 50% body height |
| 4 | Row 2, Col 1 | 33% width × 50% body height |
| 5 | Row 2, Col 2 | 33% width × 50% body height |
| 6 | Row 2, Col 3 | 33% width × 50% body height |

## Supported Overrides

All `.slide-base` tokens. Card gap via `--canvas-card-gap`.

## Limitations

- Cards beyond 6 are ignored.
- Card body space is limited — best for short content.
