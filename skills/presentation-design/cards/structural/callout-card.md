# Callout Card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

Consulting-style "key insight" / "key takeaway" box. Use to land a single
important sentence on a slide with maximum visual weight. Inspired by BCG
and McKinsey deck patterns.

## Layout

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  [card title]   (optional, base class)              â”‚
â”‚  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ (header line)              â”‚
â”‚  â–Œ                                                   â”‚
â”‚  â–Œ  KEY INSIGHT                                      â”‚
â”‚  â–Œ                                                   â”‚
â”‚  â–Œ  The capability becomes the new unit of           â”‚
â”‚  â–Œ  enterprise architecture in an agentic world.     â”‚
â”‚  â–Œ                                                   â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

- Thick coloured left accent bar runs the full body height.
- Optional small uppercase **eyebrow** label (e.g. "KEY INSIGHT", "SO WHAT?").
- Large bold **body** sentence is the actual takeaway.
- No bullets, no lists â€” one idea per card by design.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `callout-card` |
| `content.body` | string | The takeaway sentence (1â€“3 lines) |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content.eyebrow` | string | â€” | Small uppercase label above body (e.g. "KEY INSIGHT") |
| `content.footer` | string | â€” | Source / footnote (rendered by base) |

## Supported Overrides

All `.card-base` overrides plus `.card--callout` tokens:

- `card-callout-accent-color` â€” left bar colour (default `--color-primary`)
- `card-callout-accent-width` â€” bar thickness in px
- `card-callout-accent-gap` â€” gap between bar and text
- `card-callout-eyebrow-font-size` / `-font-color` / `-font-weight`
- `card-callout-eyebrow-letter-spacing` â€” `0` = none, `>0` adds hair spaces
- `card-callout-body-font-size` / `-font-color` / `-font-weight` / `-alignment`

## Example

```yaml
type: callout-card
content:
  eyebrow: "Key insight"
  body: "The capability becomes the new unit of enterprise architecture."
  footer: "Synthesis from interviews â€” Q3 2025"
style_overrides:
  card-callout-accent-color: "#000099"
  card-callout-body-font-size: 24
```
