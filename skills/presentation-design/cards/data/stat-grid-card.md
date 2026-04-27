# Stat Grid Card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

"By the numbers" card â€” displays 2â€“6 large statistic tiles inside a single
card slot. Use as an executive overview / hero metrics card. Different from
`kpi-card` (which shows one metric per card).

## Layout

Auto-grid based on stat count:

| Stats | Grid |
|-------|------|
| 2     | 1Ã—2  |
| 3     | 1Ã—3  |
| 4     | 2Ã—2  |
| 5â€“6   | 2Ã—3  |

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
│  By the numbers                                       │
│  ─────────────────────────────                        │
│                                                       │
│      87%      │       3.2x      │      42M          │
│   adoption    │   productivity  │   data points     │
│  in 6 months  │     uplift      │   processed/day   │
│                                                       │
└──────────────────────────────────────────────────────┘
```

- Large bold **value** in primary colour (default).
- Small **label** under each value.
- Optional **sub** line for comparison / context (e.g. "vs Q2").
- Thin vertical separators between tiles in the same row.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `stat-grid-card` |
| `content.stats` | list | 2–6 stat objects (`value`, `label`, `sub`) |

## Stat Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `value` | string | Large headline number (e.g. `"$4.2M"`, `"87%"`) |
| `label` | string | Short descriptor under the value |
| `sub` | string | Optional smaller comparison / context line |

## Supported Overrides

All `.card-base` overrides plus `.card--stat-grid` tokens:

- `card-stat-grid-tile-gap-x` / `-tile-gap-y` — gaps between tiles
- `card-stat-grid-alignment` — `left | center | right`
- `card-stat-grid-tile-separator-visible` / `-color` / `-width`
- `card-stat-grid-value-font-size` / `-font-color` / `-font-weight`
- `card-stat-grid-label-font-size` / `-font-color` / `-font-weight`
- `card-stat-grid-sub-font-size` / `-font-color`

## Example

```yaml
type: stat-grid-card
content:
  stats:
    - value: "87%"
      label: "Agent adoption"
      sub: "in 6 months"
    - value: "3.2×"
      label: "Productivity uplift"
      sub: "vs baseline"
    - value: "42M"
      label: "Data points processed"
      sub: "per day"
  footer: "Source: internal pilot, Q3 2025"
```
