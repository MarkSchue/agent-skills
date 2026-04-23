# Deck Syntax — Presentation Definition Format

This document defines the structured Markdown syntax for `presentation-definition.md`.

---

## Structure Hierarchy

```
# Section Title          → agenda entry + section grouping
## Slide Title           → one slide
<!-- DONE -->            → (optional) freeze this slide
<!-- slide ... -->       → (optional) per-slide overrides
### Card Title           → one card on the slide
```yaml
type: card-type
content: ...
style_overrides: ...
```​
```

---

## Sections — `#`

Each `#` heading creates a **section** and an **agenda entry**. Sections group
slides logically and drive the automatic agenda injection system.

```markdown
# Introduction
# Key Results
# Next Steps
```

---

## Slides — `##`

Each `##` heading creates a **slide**. The heading text becomes the slide title.

```markdown
## Welcome to the Team
## Q3 Revenue Summary
```

### Frozen slides — `<!-- DONE -->`

Place `<!-- DONE -->` on the line immediately below `##` to mark a slide as
frozen. The renderer will never modify frozen slides.

```markdown
## Final Approved Slide
<!-- DONE -->
### Revenue Chart
...
```

### Per-slide overrides — `<!-- slide ... -->`

Place a YAML comment block below `##` (after `<!-- DONE -->` if present) to
override slide-level CSS tokens for this specific slide.

```markdown
## Custom Background Slide
<!-- slide
background: "#F0F4F8"
title-color: "#003087"
hide-footer: true
hide-page-number: false
-->
### Card Title
...
```

Supported per-slide override keys:
| Key | Type | Description |
|-----|------|-------------|
| `background` | string | Slide background color (hex) |
| `background-image` | string | Path to background image |
| `title-color` | string | Slide title font color |
| `title-size` | int | Slide title font size (px) |
| `title-alignment` | string | left \| center \| right |
| `hide-footer` | bool | Hide footer text |
| `hide-page-number` | bool | Hide page number |
| `hide-divider` | bool | Hide title divider line |
| `hide-logo-primary` | bool | Hide primary logo |
| `hide-logo-secondary` | bool | Hide secondary logo |

---

## Cards — `###`

Each `###` heading creates a **card** on the current slide. The heading text
becomes the card title.

Below the heading, include a fenced YAML code block with the card definition:

```markdown
### Our Mission
```yaml
type: text-card
content:
  heading: "Building the Future"
  body: "We are committed to innovation and excellence."
  bullets:
    - "Customer-first approach"
    - "Data-driven decisions"
style_overrides:
  card-background: "#F8FAFC"
  header-line-color: "#3B82F6"
```​
```

### Card YAML schema

Every card YAML block normalizes to this schema:

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `type` | yes | string | Card type identifier (e.g. `text-card`) |
| `content` | yes | object | Card-specific content fields |
| `subtitle` | no | string | Subtitle text displayed below the header line |
| `icon` | no | object | Title icon config: `{ name, position, color, size, visible }` |
| `style_overrides` | no | object | Per-card CSS token overrides |
| `asset_refs` | no | list | Relative paths to assets used by this card |

### Body ↔ Bullets — universal content principle

Every card type that accepts a `body` text field also accepts a `bullets` list
as a **drop-in replacement**.  The two can coexist in the YAML, but `bullets`
takes precedence over `body` when both are present.

```yaml
# prose body (any card type)
content:
  heading: "Key Insight"
  body: "A single paragraph of explanation."

# bullet list (same card type — no change to `type` needed)
content:
  heading: "Key Insight"
  bullets:
    - "First supporting point"
    - "Second supporting point"
    - "Third supporting point"
```

Bullet appearance is controlled globally via CSS tokens:

| Token | Default | Purpose |
|---|---|---|
| `--card-bullet-style` | `square` | Bullet character: `disc` `circle` `square` `dash` `arrow` `none` |
| `--card-bullet-color` | inherits body color | Bullet marker colour |
| `--card-bullet-size` | inherits body font-size | Bullet marker size (px) |
| `--card-body-bullet-indent` | `16` | Hanging-indent in px for wrapped lines |

### Per-card override keys

| Key | Type | Description |
|-----|------|-------------|
| `card-background` | string | Card background color |
| `card-border-color` | string | Card border color |
| `card-border-radius` | int | Card border radius (px) |
| `card-padding` | int | Card inner padding (px) |
| `title-visible` | bool | Show/hide card title |
| `title-alignment` | string | left \| center \| right |
| `header-line-visible` | bool | Show/hide header divider |
| `header-line-color` | string | Header divider color |
| `header-line-width` | int | Header divider thickness (px) |
| `footer-line-visible` | bool | Show/hide footer divider line |
| `footer-font-size` | int | Footer font size (px) |
| `footer-font-color` | string | Footer text color |
| `footer-font-weight` | string | `normal` \| `bold` |
| `footer-font-style` | string | `normal` \| `italic` |
| `footer-alignment` | string | `left` \| `center` \| `right` |
| `footer-margin-top` | int | Space above footer text (px) |
| `footer-line-color` | string | Footer divider color |
| `footer-line-width` | int | Footer divider thickness (px) |
| `subtitle-visible` | bool | Show/hide subtitle below header line |
| `subtitle-font-color` | string | Subtitle text color |
| `subtitle-font-size` | int | Subtitle font size (px) |
| `subtitle-font-style` | string | `normal` \| `italic` |
| `subtitle-alignment` | string | `left` \| `center` \| `right` |
| `icon-visible` | bool | Show/hide icon next to card title |
| `icon-name` | string | Icon ligature or Unicode codepoint (e.g. `"bar_chart"`) |
| `icon-position` | string | `left` \| `right` |
| `icon-color` | string | Icon foreground color |
| `icon-size` | int | Icon size in px |
| `icon-background-color` | string | Icon badge background color |

---

## Inline text formatting

Any plain text field that accepts user content (`body`, `bullets` items, `heading`, `title`, `subtitle`, `footer`) supports inline **bold** and *italic* markdown:

| Markdown | Rendered as |
|----------|-------------|
| `**word**` | bold word |
| `*word*` | italic word |
| `***word***` | bold + italic word |

The markers are stripped for layout-width estimation, and the styled runs are passed to both the PPTX (via `python-pptx` text runs) and draw.io (via HTML `<b>`/`<i>` tags) exporters.

**Example:**

```yaml
type: text-card
content:
  body: "Results were **very positive** — a *significant* improvement over last year."
  bullets:
    - "Cost reduced by **18%** in Q1"
    - "Lead time *halved* through automation"
```

---

## Layout selection

The layout for each slide is determined automatically by the number of `###`
cards on the slide:
- 0 cards → `title-slide`
- 1 card → `grid-1x1`
- 2 cards → `grid-1x2`
- 3 cards → `grid-1x3`
- 4 cards → `grid-2x2`
- 6 cards → `grid-2x3`

Override the auto-selected layout with a `<!-- layout: grid-3x3 -->` comment
below the `##` heading.

---

## Complete example

```markdown
# Introduction

## Welcome
### Greeting
```yaml
type: text-card
content:
  heading: "Hello, World"
  body: "Welcome to our presentation."
```​

# Key Metrics

## Revenue Dashboard
### Q3 Revenue
```yaml
type: kpi-card
content:
  value: "$4.2M"
  trend: "up"
  label: "vs Q2"
```​

### Customer Growth
```yaml
type: kpi-card
content:
  value: "12,500"
  trend: "up"
  label: "Active users"
```​
```

---

## Numbering Ranges

The numbering system lets you maintain consistent, sequential codes (user stories,
bug IDs, requirements, etc.) without keeping them in sync by hand.  Every build
the codes are resolved from scratch, so insertions, deletions, and reorderings
always produce a gap-free sequence.

### Block syntax

Place a `<!-- numbering … -->` comment block **anywhere in the file** (convention:
top of the file, before the first `#` section). The block contains a YAML mapping
of range names to an ordered list of level patterns:

```markdown
<!-- numbering
userstories:
  - "US-PH01-%%"
  - "US-PH01-%%-AC%%"
bugs:
  - "BUG-%%"
  - "BUG-%%-STEP%%"
-->
```

* **Range name** (`userstories`, `bugs`, …) — arbitrary label used in log output.
* **Level patterns** — list index 0 is the *top-level* pattern, index 1 is the
  first *sub-level*, and so on.
* `%%` is the counter placeholder.  It is zero-padded to 2 digits (`01`, `02`, …).
* Patterns with multiple `%%` slots fill them left-to-right:
  `US-PH01-%%-AC%%` with counters `[3, 2]` → `US-PH01-03-AC02`.

### Counter rules

| Event | Effect |
|-------|--------|
| Level-0 match | `counters[0]` += 1, sub-counters reset to 0 |
| Level-N match | `counters[N]` += 1, parent counters unchanged |
| At most one level per line per range | First matching level wins |

### Renumber on every build

Both bare placeholders (`%%`) **and** previously-resolved codes (e.g. `US-PH01-03`)
are matched by the same regex so the file is always renumbered from scratch.
This means:

* Adding a story in the middle shifts all subsequent numbers correctly.
* Removing a story closes the gap automatically.
* Running the build twice in a row leaves the file unchanged (idempotent when
  nothing has moved).

### Example

Given a `<!-- numbering -->` block declaring:

```yaml
userstories:
  - "US-%%"
  - "US-%%-AC%%"
```

And this content (after the first build):

```markdown
Deliver US-01 by end of sprint.
Acceptance criteria: US-01-AC01, US-01-AC02.
Second story: US-02.
```

If you insert a new story before `US-02` and re-run the build, it becomes `US-02`
and the old `US-02` (now third) becomes `US-03` automatically.

