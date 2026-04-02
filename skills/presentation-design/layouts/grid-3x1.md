# Grid 3×1 Layout

Three rows, one column — three cards stacked vertically.

## Pictogram

```
┌─────────────────────────────────────────────────────────────────┐
│  [logo-primary]    [slide-title]          [logo-secondary]     │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                       Card 1                              │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                       Card 2                              │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                       Card 3                              │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  [footer-text]                              [page-number]      │
└─────────────────────────────────────────────────────────────────┘
```

## Purpose

Vertical list — three sequential items, timeline steps, or stacked content blocks.

## Card Count

3

## Placement Map

| Slot | Position | Size |
|------|----------|------|
| 1 | Top third | 100% width × 33% body height |
| 2 | Middle third | 100% width × 33% body height |
| 3 | Bottom third | 100% width × 33% body height |

## Supported Overrides

All `.slide-base` tokens. Card gap via `--canvas-card-gap`.

## Limitations

- Cards beyond 3 are ignored.
- Limited vertical space per card.
