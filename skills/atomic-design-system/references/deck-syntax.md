# deck.md Syntax Reference

> **Maintenance rule — read this first:**
> This file is the canonical syntax reference for `deck.md` authoring.
> **Every time a new molecule, template, atom, or front-matter key is added to the design system,
> update the matching section here before closing the task.** This ensures any LLM can always
> produce correctly-structured `deck.md` files without needing a project example on disk.

---

## 1  File Structure

```markdown
---
theme: theme.css           # required — path to project theme.css
auto-agenda: true          # optional — false to disable agenda injection (default: true)
---

# Section Title            ← H1 = agenda section (groups slides)

## Slide Title             ← H2 = one physical slide
<!-- layout: <template-id> -->

Optional bare-text content (used by hero-title subtitle, etc.)

### Card Block Heading     ← H3 = one content zone inside the slide
```yaml
molecule: <molecule-id>
<key>: <value>
...
```​

### Second Card Block
```yaml
molecule: <molecule-id>
...
```​
```

### Rules

| Level | Meaning | Required |
|-------|---------|---------|
| `---` front matter | Theme path + global flags | Yes |
| `# H1` | Logical section / agenda entry | All content slides need a parent section |
| `## H2` | One physical slide | Yes per slide |
| `<!-- layout: id -->` | Template to use for this slide | Recommended; auto-selected otherwise |
| `### H3` | One card zone passed to the layout | One per column/slot |
| ` ```yaml ` block | Molecule props for that card zone | Required if zone has content |

### ⚠️ Key parser rules
- The YAML block opens with ` ```yaml ` and closes with ` ``` ` — exactly this fence language tag.
- The `molecule:` key **must be the first key** in the block.
- Properties are **flat** — do **not** wrap them under a `params:` key.
- Block content (text with colons) **must be quoted** — e.g. `title: "Phase 0: Mobilize"`.
- YAML-special characters (`—`, `&`, `>`) inside quoted strings are fine; bare values are not.

---

## 2  Available Layouts (Templates)

Use `<!-- layout: <id> -->` on the line immediately after the H2 heading.

| Template ID | Zones | Description |
|-------------|-------|-------------|
| `hero-title` | 0–1 (subtitle only) | Full-width cover / section-break slide. Title = H2 text; optional subtitle beneath. |
| `grid-2` | 2 | Two equal-width columns side-by-side. |
| `grid-3` | 2–4 | Three equal-width columns (adapts to 2 or 4 cards). |
| `grid-4` | 4 | Four equal-width columns. |
| `grid-1-2` | 2 | Narrow left column (1/3) + wide right column (2/3). |
| `grid-2-1` | 2 | Wide left column (2/3) + narrow right column (1/3). |
| `row-2` | 2 | Two equal-height rows stacked vertically. |
| `row-3` | 3 | Three equal-height rows stacked vertically. |
| `row-1-2` | 2 | Narrow top row + tall bottom row. |
| `row-2-1` | 2 | Tall top row + narrow bottom row. |
| `grid-row-2-2` | 4 | 2×2 grid (two rows, two columns). |
| `grid-row-3-2` | 6 | 3×2 grid (two rows, three columns). |
| `numbered-list` | 3–6 | Vertical numbered steps; each H3 = one step. |
| `comparison-2col` | 2 | Equal two-column comparison. |
| `data-insight` | 2–4 | Wide chart/viz left + insight text + KPIs right. |

### Hero-title subtitle syntax

```markdown
## My Cover Slide
<!-- layout: hero-title -->

subtitle: "Optional one-line subtitle shown below the title"
```

The bare `subtitle:` line (not inside a YAML fence) is the only content the hero-title layout reads.
Alternatively, place a single `### Subtitle` H3 with a `stacked-text` block if more content is needed.

---

## 3  Molecule Block Syntax (canonical form)

```markdown
### Column / Zone Heading
```yaml
molecule: <molecule-id>
<prop-key>: <value>
<list-prop>:
  - <item-key>: <value>
    <item-key>: <value>
```​
```

The H3 heading is the zone label visible in the template; the YAML block carries all card data.

---

## 4  Strategy Molecules

### 4.1  `stacked-text`  _(alias: `topic-card`)_

Stacked card with a title, repeated body rows, and an optional takeaway line.
Use for most content columns: overviews, summaries, bullet-style content.

```yaml
molecule: stacked-text
title: "Card Title"
items:
  - text: "Row one content"
  - text: "Row two content"
  - text: "Row three content"
takeaway: "Short bold conclusion line"
```

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `title` | string | — | Card heading |
| `items` | list of `{text}` | — | 1–8 rows |
| `takeaway` | string | — | Bold bottom line; aliases: `takeaway-line` |
| `text_align` | enum | `left` | `left` · `center` · `right`. Center suppresses chevrons (»»). |
| `card_bg` | enum | — | See §8 Card Background Overrides |
| `show_title_line` | bool | `true` | Divider below title |
| `title_line_width` | string/number | `100%` | e.g. `0.7` or `"70%"` |
| `title_line_align` | enum | `left` | `left` · `center` · `right` |
| `title_align` | enum | `left` | Title text alignment |

---

### 4.2  `timeline-panel`

Horizontal or vertical timeline of ordered milestones with date, label, description, and status.

```yaml
molecule: timeline-panel
orientation: horizontal
events:
  - date: "2023"
    label: "Series A"
    description: "$12M raised"
    status: success
  - date: "2025"
    label: "IPO"
    description: "Listed on XETRA"
    status: neutral
```

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `title` | string | — | Optional panel heading |
| `orientation` | enum | `horizontal` | `horizontal` · `vertical` |
| `events` | list of `{date, label, description, status}` | — | 2–8 items |
| `events[].status` | enum | `neutral` | `success` · `warning` · `error` · `primary` · `neutral` |

---

### 4.3  `objective-card`

OKR-style card with a strategic objective, quarter label, and key results with progress indicators.

```yaml
molecule: objective-card
objective: "Achieve market leadership in DACH region"
quarter: "Q3 2025"
key-results:
  - text: "Grow MRR to €5M"
    progress: 82
  - text: "Close 10 enterprise deals"
    progress: 60
  - text: "NPS above 50"
    progress: 100
```

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `objective` | string | — | The strategic objective statement |
| `quarter` | string | — | Badge label e.g. `"Q3 2025"` or `"Task 1"` |
| `key-results` | list of `{text, progress}` | — | 1–5 KRs; `progress` is 0–100 |

Progress badge variant is auto-derived: ≥80 % = success, 40–79 % = warning, <40 % = error.
Use `progress: 0` for "not started" (renders as empty / neutral).

---

### 4.4  `agenda-card`

Agenda/schedule card composing numbered, timed, or icon-labelled rows.
Primarily used by auto-generated agenda slides; can be placed manually.

```yaml
molecule: agenda-card
title: "Agenda"
entries:
  - label_type: number
    label: "01"
    title: "Welcome"
    description: "Introduction and context"
    highlight: false
  - label_type: number
    label: "02"
    title: "Deep Dive"
    description: "Technical walkthrough"
    highlight: true
  - label_type: time
    label: "14:00–15:30"
    title: "Workshop"
    description: "Hands-on session"
    highlight: false
```

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `title` | string | — | Card header title |
| `icon` | string | — | Header icon concept |
| `entries` | list of entry objects | — | Required |
| `entries[].label_type` | enum | `number` | `number` · `time` · `icon` |
| `entries[].label` | string | — | Ordinal, time range, or icon concept |
| `entries[].title` | string | — | Bold entry heading |
| `entries[].description` | string | — | 0–2 lines of body text |
| `entries[].highlight` | bool | `false` | Marks active row (primary-container tint) |
| `show-title` | bool | `true` | Show card title section |
| `show-dividers` | bool | `true` | Separator lines between entries |

---

### 4.5  `mission-card`

Card for a mission or vision statement with optional icon.

```yaml
molecule: mission-card
title: "Our Mission"
statement: "We accelerate the world's transition to sustainable industrial processes."
icon-name: target
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `title` | string | Card heading |
| `statement` | string | Mission/vision text; up to 3 sentences |
| `icon-name` | string | Optional — icon concept (e.g. `target`, `compass`) |

---

### 4.6  `quote-card`

Pull-quote with large typographic quote marks and attribution.

```yaml
molecule: quote-card
quote: "This platform reduced our planning cycle from 6 weeks to 3 days."
name: "Maria Schneider"
title: "VP Operations, MegaCorp AG"
icon-name: user-avatar
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `quote` | string | The pull-quote text |
| `name` | string | Attributed person's name |
| `title` | string | Person's role or organization |
| `icon-name` | string | Portrait icon or company logo icon |

---

### 4.7  `roadmap-panel`

Now / Next / Later swim-lane roadmap.

```yaml
molecule: roadmap-panel
title: "Product Roadmap 2025"
lanes:
  - label: "Now"
    items:
      - text: "Mobile App v2.0"
        description: "iOS + Android release"
        status: primary
  - label: "Next"
    items:
      - text: "API v3"
        description: "GraphQL support"
        status: neutral
  - label: "Later"
    items:
      - text: "AI Insights"
        description: "Predictive analytics"
        status: neutral
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `title` | string | Panel heading |
| `lanes` | list of `{label, items[]}` | 2–4 swim-lanes |
| `lanes[].label` | string | Swim-lane heading (e.g. `Now`, `Next`, `Later`) |
| `lanes[].items[].text` | string | Item title |
| `lanes[].items[].description` | string | Short detail |
| `lanes[].items[].status` | enum | `primary` · `success` · `warning` · `neutral` |

---

## 5  Data Molecules

### 5.1  `kpi-card`

Single KPI with metric value, trend badge, and optional comparison period.

```yaml
molecule: kpi-card
label: "Annual Recurring Revenue"
value: "€12.4M"
change: "+18%"
trend: up
reference: "vs FY2023"
icon-name: currency
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `label` | string | KPI name |
| `value` | string | Formatted metric value |
| `change` | string | Delta e.g. `"+18%"` |
| `trend` | enum | `up` · `down` · `neutral` |
| `reference` | string | Comparison period label |
| `icon-name` | string | Icon representing the metric |

---

### 5.2  `trend-card`

Metric with sparkline bar chart and trend badge.

```yaml
molecule: trend-card
label: "Weekly Active Users"
value: "142K"
change: "+7%"
trend: up
unit: users
sparkline: [98, 105, 112, 118, 125, 131, 142]
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `label` | string | Metric name |
| `value` | string | Current value |
| `change` | string | Period-on-period delta |
| `trend` | enum | `up` · `down` · `neutral` |
| `unit` | string | Unit suffix |
| `sparkline` | list of numbers | 5–12 historical values (chronological) |

---

### 5.3  `comparison-card`

Two-option attribute comparison with optional recommended highlight.

```yaml
molecule: comparison-card
title: "Deployment Options"
left:
  label: "On-Premise"
  attributes:
    - "Full data control"
    - "Higher setup cost"
right:
  label: "Cloud SaaS"
  attributes:
    - "Instant deployment"
    - "Subscription pricing"
  badge: "Recommended"
recommended: right
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `title` | string | Panel heading |
| `left` | object `{label, attributes[], badge?}` | Left option |
| `right` | object `{label, attributes[], badge?}` | Right option |
| `recommended` | enum | `left` · `right` · `none` |

---

### 5.4  `chart-card`

Chart atom wrapper with title, period badge, and optional source note.
Embed a chart by placing a chart atom block inside.

```yaml
molecule: chart-card
title: "Revenue by Region"
period: "FY 2025"
chart-type: bar
data:
  - label: "DACH"
    value: 42
  - label: "APAC"
    value: 28
  - label: "Americas"
    value: 30
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `title` | string | Chart heading |
| `period` | string | Badge label for time range |
| `chart-type` | enum | `bar` · `pie` · `gantt` |
| `data` | list of `{label, value}` | Data points |

---

### 5.5  `data-insight-panel`

Wide panel with a chart and written insight bullets.

```yaml
molecule: data-insight-panel
title: "Market Share Trend"
chart-type: bar
data:
  - label: "Q1"
    value: 18
  - label: "Q2"
    value: 22
insights:
  - text: "Market share grew 4 pp in H1"
  - text: "APAC is the fastest-growing region"
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `title` | string | Panel heading |
| `chart-type` | enum | `bar` · `pie` |
| `data` | list of `{label, value}` | Chart data |
| `insights` | list of `{text}` | Bullet insights displayed to the right |

---

### 5.6  `waveform-card`

Split-layout card with amplitude waveform on the left and a large stat on the right.

```yaml
molecule: waveform-card
label: "Signal Intensity"
value: "84.5"
unit: dB
values: [0.2, 0.5, 0.8, 0.6, 0.9, 0.4, 0.7, 0.3, 0.8, 0.6]
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `label` | string | Metric label |
| `value` | string | Large display number |
| `unit` | string | Unit suffix |
| `values` | list of numbers | Normalized amplitudes 0.0–1.0 (5–30 values) |

---

### 5.7  `dot-chart-card`

Split-layout with lollipop / dot-line chart on the left and a stat on the right.

```yaml
molecule: dot-chart-card
label: "NPS Score"
value: "72"
unit: pts
data:
  - label: "Jan"
    value: 58
  - label: "Apr"
    value: 65
  - label: "Aug"
    value: 72
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `label` | string | Metric label |
| `value` | string | Large stat |
| `unit` | string | Unit suffix |
| `data` | list of `{label, value}` | Lollipop data points |

---

### 5.8  `stats-chart-panel`

Wide panel with icon-title header, stat column left, bar chart right.

```yaml
molecule: stats-chart-panel
title: "Monthly Performance"
icon-name: chart
stats:
  - label: "Revenue"
    value: "€4.2M"
  - label: "Deals closed"
    value: "38"
chart-data:
  - label: "Jan"
    value: 3.8
  - label: "Feb"
    value: 4.1
  - label: "Mar"
    value: 4.2
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `title` | string | Header title |
| `icon-name` | string | Header icon concept |
| `stats` | list of `{label, value}` | Left-column stat rows |
| `chart-data` | list of `{label, value}` | Bar chart data |

---

### 5.9  `daily-header-card`

Full-width display header card with large title and date/time footer row.

```yaml
molecule: daily-header-card
title: "Daily Operations Report"
date: "Monday, 30 March 2026"
time: "08:00 CET"
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `title` | string | Large display heading |
| `date` | string | Date label in footer |
| `time` | string | Time label in footer |

---

## 6  Team Molecules

### 6.1  `profile-card`

Person card with avatar icon, name, title, department badge, optional contact.

```yaml
molecule: profile-card
name: "Dr. Anna Müller"
title: "Chief Technology Officer"
department: "Engineering"
contact: "a.mueller@company.com"
icon-name: user
align: center
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `name` | string | Full name |
| `title` | string | Job title |
| `department` | string | Department badge label |
| `contact` | string | Email or social handle |
| `icon-name` | string | Avatar icon concept |
| `align` | enum | `center` · `left` |

---

### 6.2  `role-card`

Organizational role card with title, level badge, and responsibilities.

```yaml
molecule: role-card
title: "Solution Architect"
level: "L5 — Senior"
responsibilities:
  - text: "Design end-to-end integration patterns"
  - text: "Own technical delivery assurance"
reports-to: "VP Engineering"
icon-name: architect
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `title` | string | Role title |
| `level` | string | Seniority / level badge |
| `responsibilities` | list of `{text}` | Duty bullets |
| `reports-to` | string | Reporting line |
| `icon-name` | string | Icon concept |

---

### 6.3  `contact-card`

Business-card style with name, role, company, email, URL, and channels.

```yaml
molecule: contact-card
name: "Markus Lang"
role: "Enterprise Architect"
company: "LAPP Group"
email: "m.lang@lapp.com"
url: "lapp.com"
icon-name: user
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `name` | string | Full name |
| `role` | string | Job title |
| `company` | string | Company name |
| `email` | string | Email address |
| `url` | string | Website |
| `icon-name` | string | Avatar icon |

---

### 6.4  `location-card`

Office or site card with city, address, headcount, timezone, key contact.

```yaml
molecule: location-card
city: "Stuttgart"
address: "Oskar-Lapp-Str. 2, 70565 Stuttgart"
headcount: 1200
timezone: "UTC+1"
contact: "contact@lapp.com"
icon-name: location
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `city` | string | City / site name |
| `address` | string | Street address |
| `headcount` | number | People at site |
| `timezone` | string | Timezone label |
| `contact` | string | Key contact email |
| `icon-name` | string | Location icon |

---

### 6.5  `team-grid-panel`

Grid panel composing multiple profile entries in 2- or 3-column layout.

```yaml
molecule: team-grid-panel
title: "Leadership Team"
columns: 3
members:
  - name: "Anna Müller"
    title: "CTO"
    icon-name: user
  - name: "Ben Schneider"
    title: "CFO"
    icon-name: user
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `title` | string | Panel heading |
| `columns` | number | `2` or `3` |
| `members` | list — same shape as `profile-card` | Each member card |

---

### 6.6  `header-list-card`

Card with header strip (avatar · name · detail), a labeled two-column item list, and optional CTA.

```yaml
molecule: header-list-card
name: "Sarah Chen"
detail: "Available · Mon–Fri"
icon-name: user
items:
  - label: "Focus"
    value: "SAP Integration"
  - label: "Rate"
    value: "€1,200/day"
cta-label: "Book a call"
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `name` | string | Header strip name |
| `detail` | string | Subtitle / availability |
| `icon-name` | string | Avatar icon |
| `items` | list of `{label, value}` | Two-column item rows |
| `cta-label` | string | Optional call-to-action button text |

---

## 7  Agenda Auto-generation

When the deck uses H1 / H2 / H3 hierarchy and has ≥ 2 H1 sections, the builder automatically
injects agenda slides:

1. **Overview agenda** (no section highlighted) → slide 2 (after cover).
2. **Section agenda** (current section highlighted) → before the first slide of each section.

Slide order: `cover → overview-agenda → [section1-agenda] → section1-slides → [section2-agenda] → …`

Each agenda slide uses `grid-1-2`:
- Left (`stacked-text`): section name
- Right (`agenda-card`): all sections, one highlighted

**Disable auto-agenda:**

```markdown
---
theme: theme.css
auto-agenda: false
---
```

**Manually edit agenda:** After first build, `deck.md` receives a materialized `# __agenda__` block
at the top. Edit entries there and set `auto-agenda: false` to prevent regeneration from overwriting.

---

## 8  Card Background Overrides

Add `card_bg:` to any molecule block to change the card surface:

```yaml
molecule: stacked-text
title: "Featured Item"
card_bg: featured
items:
  - text: "Stands out with vivid primary fill"
```

| `card_bg` value | Token | Typical use |
|----------------|-------|------------|
| _(omitted)_ | `--color-bg-card` | Default harmonized surface |
| `clean` | `--color-bg-card-clean` | Minimal / near-white feel |
| `filled` | `--color-bg-card-filled` | Accented / primary-container |
| `alt` | `--color-bg-card-alt` | Secondary-container variant |
| `featured` | `--color-bg-card-featured` | Vivid hero / primary color |

---

## 9  Common Per-card Overrides

These keys apply to most card molecules (check individual molecule docs for support):

| Key | Type | Effect |
|-----|------|--------|
| `card_bg` | enum | Card surface color (see §8) |
| `text_align` | enum | `left` · `center` · `right` — global text alignment |
| `title_align` | enum | Title alignment only |
| `show_title_line` | bool | Show/hide divider below card title |
| `title_line_width` | string/number | Width of title divider (`"70%"` or `0.7`) |
| `title_line_align` | enum | `left` · `center` · `right` |

---

## 10  Full Deck Example

```markdown
---
theme: theme.css
---

# Program Overview

## Project Cover
<!-- layout: hero-title -->

subtitle: "Delivering the future — Q2 2026"

## Objectives & Scope
<!-- layout: grid-2 -->

### Objectives
```yaml
molecule: stacked-text
title: Objectives
items:
  - text: "Reduce operating cost by 20%"
  - text: "Migrate all on-premise workloads to cloud"
  - text: "Achieve ISO 27001 certification"
takeaway: Cost · Cloud · Compliance
```​

### Scope
```yaml
molecule: stacked-text
title: Scope
items:
  - text: "IN: All production SAP systems"
  - text: "IN: Data center consolidation"
  - text: "OUT: End-user device management"
```​

# Roadmap

## Delivery Phases
<!-- layout: grid-1-2 -->

### Overview
```yaml
molecule: stacked-text
title: Five Phases
items:
  - text: "Phase 0 — Mobilize (4 wks)"
  - text: "Phase 1 — Baseline (8 wks)"
  - text: "Phase 2 — Architecture (6 wks)"
  - text: "Phase 3 — Transition planning (10 wks)"
  - text: "Phase 4 — Execution waves"
takeaway: 28 weeks to production decision
```​

### Timeline
```yaml
molecule: timeline-panel
orientation: horizontal
events:
  - date: "Wk 1–4"
    label: "Phase 0"
    description: "Mobilize"
    status: success
  - date: "Wk 5–12"
    label: "Phase 1"
    description: "Baseline"
    status: neutral
  - date: "Wk 13–18"
    label: "Phase 2"
    description: "Architecture"
    status: neutral
```​

# Target State & Next Steps

## Definition of Done
<!-- layout: grid-3 -->

### Baseline
```yaml
molecule: objective-card
objective: Current state fully documented
quarter: Task 1
key-results:
  - text: "Module/process inventory complete"
    progress: 0
  - text: "Interface catalog published"
    progress: 0
```​

### Architecture
```yaml
molecule: objective-card
objective: Target architecture decided and documented
quarter: Task 2
key-results:
  - text: "Option selected by steering board"
    progress: 0
  - text: "Blueprint signed off"
    progress: 0
```​

### Roadmap
```yaml
molecule: objective-card
objective: Execution roadmap at budget level of detail
quarter: Task 3
key-results:
  - text: "Wave plan with milestones"
    progress: 0
  - text: "RAID log established"
    progress: 0
```​

## Next Steps
<!-- layout: numbered-list -->

### Step 1
```yaml
molecule: stacked-text
title: Confirm scope
items:
  - text: "Agree system perimeter with architecture board"
```​

### Step 2
```yaml
molecule: stacked-text
title: Kick off discovery
items:
  - text: "Schedule stakeholder interviews for all domains"
```​
```

---

## 11  Changelog

| Date | Change | Element |
|------|--------|---------|
| 2026-03-30 | File created | All molecules and templates as of v1.0.0 |

_Add a row here each time a new molecule, template, or front-matter key is introduced._
