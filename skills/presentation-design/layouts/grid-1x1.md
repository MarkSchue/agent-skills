# Grid 1×1 Layout

Single card occupying the full body area of the slide.

## Pictogram

```
┌─────────────────────────────────────────────────────────────────┐
│  [logo-primary]    [slide-title]          [logo-secondary]     │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                                                           │  │
│  │                       Card 1                              │  │
│  │                                                           │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  [footer-text]                              [page-number]      │
└─────────────────────────────────────────────────────────────────┘
```

## Purpose

Hero content — a single text block, large image, or KPI that needs maximum visual weight.

## Card Count

1

## Placement Map

| Slot | Position | Size |
|------|----------|------|
| 1 | Full body | 100% width × 100% body height |

## Supported Overrides

All `.slide-base` tokens apply to the chrome.

## Limitations

- Only renders the first card; additional cards are ignored.

## Example

```markdown
## Key Insight
### Main Point
```yaml
type: text-card
content:
  body: "Our platform now serves 2M daily active users."
```
```
