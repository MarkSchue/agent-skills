# Grid 1×2 Layout

One row, two equal-width cards side by side.

## Pictogram

```
┌─────────────────────────────────────────────────────────────────┐
│  [logo-primary]    [slide-title]          [logo-secondary]     │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  ┌────────────────────────┐  ┌────────────────────────────┐    │
│  │                        │  │                            │    │
│  │        Card 1          │  │         Card 2             │    │
│  │                        │  │                            │    │
│  │                        │  │                            │    │
│  └────────────────────────┘  └────────────────────────────┘    │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  [footer-text]                              [page-number]      │
└─────────────────────────────────────────────────────────────────┘
```

## Purpose

Comparison, before/after, or two complementary content blocks.

## Card Count

2

## Placement Map

| Slot | Position | Size |
|------|----------|------|
| 1 | Left half | 50% width × 100% body height |
| 2 | Right half | 50% width × 100% body height |

## Supported Overrides

All `.slide-base` tokens apply to the chrome. Card gap controlled by `--canvas-card-gap`.

## Limitations

- Cards beyond 2 are ignored.

## Example

```markdown
## Comparison
### Before
```yaml
type: text-card
content:
  body: "Manual process taking 3 days."
```
### After
```yaml
type: text-card
content:
  body: "Automated pipeline completing in 2 hours."
```
```
