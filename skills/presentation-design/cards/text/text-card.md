# Text Card

General-purpose text card with heading, body text, and typography variants.

## Layout

```
┌─────────────────────────────────────────────────────┐
│  [text-label: card title]                           │
│  ─────────────────────────────── (header line)      │
│                                                     │
│  [text-h1: heading]                                 │
│  [text-h2: subheading]                              │
│                                                     │
│  [text-body: body paragraph / bullets]              │
│                                                     │
│  [text-caption: caption]                            │
│  [text-footnote: footnote]                          │
└─────────────────────────────────────────────────────┘
```

- Title sits at the top with an optional header line below it.
- Body area supports heading, subheading, body text, bullets, caption, and footnote.
- All text styles resolve from the `.text-*` token families.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `text-card` |
| `content.body` | string or list | Main body text or bullet list |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content.heading` | string | — | Heading text (uses `.text-h1`) |
| `content.subheading` | string | — | Subheading text (uses `.text-h2`) |
| `content.bullets` | list | — | Bullet list items |
| `content.caption` | string | — | Caption text below body |
| `content.footnote` | string | — | Footnote text at bottom |

## Supported Overrides

All `.card-base` overrides plus:
- No card-variant-specific overrides (text-card uses only base card tokens).

## Design Tokens Used

- `.card-base` — container, title, header line
- `.text-h1` — heading
- `.text-h2` — subheading
- `.text-body` — body paragraph
- `.text-caption` — caption
- `.text-footnote` — footnote

## Example

```yaml
type: text-card
content:
  heading: "Our Vision"
  body: "We believe in building products that matter."
  bullets:
    - "Customer-first approach"
    - "Data-driven decisions"
    - "Continuous improvement"
  caption: "Updated Q3 2025"
style_overrides:
  card_background: "#F8FAFC"
```
