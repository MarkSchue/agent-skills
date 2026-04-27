# Section Divider Card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

A bold full-bleed chapter break used between sections of a deck. Shows an
oversized section number, a section title and an optional eyebrow + subtitle.
A much stronger visual break than an `agenda-card` highlight.

## Layout

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
│ │                                                  │
│ │                    EYEBROW                       │
│ │                                                  │
│ │   02       Section Title Goes Here               │
│ │            Optional subtitle / framing line      │
│ │                                                  │
└────────────────────────────────────────────────────┘
```

Use on a `grid-1x1` layout for full-bleed effect.

## Required Fields

None — all fields are optional. At minimum supply `number` or `title`.

## Optional Fields (`content`)

| Field | Type | Description |
|-------|------|-------------|
| `number` | string | Large section number, kept verbatim (`"02"`, `"III"`, `"#3"`). |
| `title` | string | Section title rendered large beside the number. |
| `subtitle` | string | Optional framing sentence below the title. |
| `eyebrow` | string | Small uppercase label above the title (e.g. `"Section"`, `"Part 02"`). |

## Supported Overrides (`style_overrides`)

Any token from the `.card--section-divider` block — see
[`themes/base.css`](../../themes/base.css) section 21. Common overrides:

- `card-section-divider-bg-color` — flip to `var(--color-primary)` for an
  inverted/dark treatment.
- `card-section-divider-number-font-color` / `title-font-color` /
  `subtitle-font-color` — must be inverted when using a dark background.
- `card-section-divider-number-font-size` / `title-font-size`.

## Example

```yaml
type: section-divider-card
content:
  eyebrow: "Part 02"
  number: "02"
  title: "Capabilities vs. Business Processes"
  subtitle: "Why capability becomes the durable EAM unit in the agent era"
```

### Inverted (dark) treatment

```yaml
type: section-divider-card
style_overrides:
  card-section-divider-bg-color: "#000099"
  card-section-divider-number-font-color: "#FFFFFF"
  card-section-divider-title-font-color: "#FFFFFF"
  card-section-divider-subtitle-font-color: "#CCCCFF"
  card-section-divider-eyebrow-font-color: "#80AAFF"
  card-section-divider-accent-color: "#FFFFFF"
content:
  eyebrow: "Section"
  number: "03"
  title: "What Needs to Be Tracked?"
```
