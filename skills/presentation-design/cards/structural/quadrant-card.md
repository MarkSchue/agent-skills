# Quadrant Card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

A 2Ã—2 matrix card for SWOT, BCG growth-share, prioritisation grids,
Eisenhower boxes and similar consulting frameworks. Four labelled quadrants
in a 2Ã—2 grid with optional axis labels along the top and left edges.

## Layout

```
            X-axis low                    X-axis high
          â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
y high    │  Q1 (top-left)       │  Q2 (top-right)      │
          │                      │                      │
          ├──────────────────────┼──────────────────────┤
y low     │  Q3 (bottom-left)    │  Q4 (bottom-right)   │
          │                      │                      │
          └──────────────────────┴──────────────────────┘
```

Quadrant order is row-major: top-left → top-right → bottom-left → bottom-right.

## Required Fields (`content`)

| Field | Type | Description |
|-------|------|-------------|
| `quadrants` | list of 4 dicts | One entry per cell. Missing entries render as empty tiles. |

Each quadrant entry supports:

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Heading of the quadrant. |
| `body` | string | Body text (used when `items` is not provided). |
| `items` | list of strings | Bullet items rendered with `•`. Takes precedence over `body`. |
| `accent` | bool | If true, fills the tile with the accent colour and inverts text. |

## Optional Fields (`content`)

| Field | Type | Description |
|-------|------|-------------|
| `x_axis.low` / `x_axis.high` | string | Labels along the top edge (e.g. `"Low Effort"` / `"High Effort"`). |
| `y_axis.low` / `y_axis.high` | string | Labels along the left edge (e.g. `"Low Impact"` / `"High Impact"`). |

## Supported Overrides (`style_overrides`)

Any token from `.card--quadrant` — see [`themes/base.css`](../../themes/base.css)
section 22. Common overrides:

- `card-quadrant-tile-bg-color` / `tile-accent-bg-color` — tile colours.
- `card-quadrant-tile-border-width` — set to `1` for outlined tiles.
- `card-quadrant-quadrant-heading-font-size` / `quadrant-body-font-size`.
- `card-quadrant-axis-visible` — set to `false` to hide axis labels even
  when present in content.

## Example — Impact / Effort matrix

```yaml
type: quadrant-card
title: "Where to Invest in Agent Initiatives"
content:
  x_axis:
    low: "Low Effort"
    high: "High Effort"
  y_axis:
    low: "Low Impact"
    high: "High Impact"
  quadrants:
    - title: "Quick Wins"
      accent: true
      items:
        - "Internal copilot for finance reports"
        - "Email triage for HR"
    - title: "Major Bets"
      items:
        - "Autonomous procurement agents"
        - "Self-healing operations"
    - title: "Fill-Ins"
      body: "Useful but small. Schedule when capacity is free."
    - title: "Reconsider"
      body: "High effort, low impact. Park unless strategic value emerges."
```

## Example — SWOT

```yaml
type: quadrant-card
title: "Agent Adoption SWOT"
content:
  quadrants:
    - title: "Strengths"
      items: ["Mature data platform", "Skilled architects"]
    - title: "Weaknesses"
      items: ["No prompt registry", "Fragmented governance"]
    - title: "Opportunities"
      items: ["MCP standard maturing", "Vendor traction"]
    - title: "Threats"
      items: ["Shadow agents in BUs", "Regulatory uncertainty"]
```
