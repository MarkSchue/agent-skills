# Quote Card

Displays a quotation with attribution. Supports highlight/accent styling.

## Layout

```
┌─────────────────────────────────────────────────────┐
│  [text-label: card title]                           │
│  ─────────────────────────────── (header line)      │
│                                                     │
│  ┃  "Quote text goes here, spanning one or more     │
│  ┃   lines as needed for the full quotation."       │
│                                                     │
│              — [text-body: attribution]              │
│                [text-caption: role / org]            │
└─────────────────────────────────────────────────────┘
```

- Left accent bar drawn next to quote text.
- Quote text in italic or styled font.
- Attribution below, right-aligned or centered.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `quote-card` |
| `content.quote` | string | The quotation text |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content.attribution` | string | — | Speaker / author name |
| `content.role` | string | — | Role or organization |

## Supported Overrides

All `.card-base` overrides plus `.card--quote` tokens:
- `card_quote_accent_color` — left bar color
- `card_quote_accent_width` — left bar width in px
- `card_quote_font_size` — quote text size
- `card_quote_font_style` — `italic` or `normal`
- `card_quote_font_color` — quote text color

## Design Tokens Used

- `.card-base` — container, title, header line
- `.card--quote` — accent bar, quote text styling
- `.text-body` — attribution name
- `.text-caption` — role / org text

## Example

```yaml
type: quote-card
content:
  quote: "The best way to predict the future is to invent it."
  attribution: "Alan Kay"
  role: "Computer Scientist"
style_overrides:
  card_quote_accent_color: "#0066CC"
```
