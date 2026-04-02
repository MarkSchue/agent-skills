# Grid 2×1 Layout

Two rows, one column — two cards stacked vertically.

## Pictogram

```
┌─────────────────────────────────────────────────────────────────┐
│  [logo-primary]    [slide-title]          [logo-secondary]     │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                       Card 1                              │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                       Card 2                              │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  [footer-text]                              [page-number]      │
└─────────────────────────────────────────────────────────────────┘
```

## Purpose

Top/bottom split — image above text, header card above detail, or sequential content.

## Card Count

2

## Placement Map

| Slot | Position | Size |
|------|----------|------|
| 1 | Top half | 100% width × 50% body height |
| 2 | Bottom half | 100% width × 50% body height |

## Supported Overrides

All `.slide-base` tokens. Card gap via `--canvas-card-gap`.

## Limitations

- Cards beyond 2 are ignored.

## Example

```markdown
## Architecture Overview
### Diagram
```yaml
type: image-card
content:
  image: "diagrams/architecture.png"
  alt: "System architecture diagram"
```
### Description
```yaml
type: text-card
content:
  body: "The system uses a microservices architecture with event-driven communication."
```
```
