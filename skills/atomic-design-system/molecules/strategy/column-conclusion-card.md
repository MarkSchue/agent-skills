# column-conclusion-card

**Molecule slug:** `column-conclusion-card`
**Domain:** strategy
**Category:** Summary / Insight

A metric-column layout with **2–5 equal columns** and an optional full-width conclusion
section below a decorated divider. Each column can independently show an icon, a large
value with unit, a bold headline, and body text — all centred (or left/right) as a unit.
Use it for key-number summaries, section recaps, or before/after comparisons.

## Design anatomy

```
┌──────────────────────────────────────────────────────────────────┐
│  [Optional title header]                                         │
│                                                                  │
│   [icon]        [icon]        [icon]         ← optional          │
│   87 %          12.4 M        +3             ← large, primary    │
│   Bold          Bold          Bold           ← headline (bold)   │
│   Headline      Headline      Headline                           │
│   Supporting    Supporting    Supporting      ← body (muted)     │
│   body text     body text     body text                          │
│                                                                  │
│  ─────────────────────[∨]─────────────────────  ← divider+chev  │
│       Lorem ipsum dolor sit amet — conclusion text               │
└──────────────────────────────────────────────────────────────────┘
```

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `chevron-color` | color-token | Color token name (theme color). |
| `col_valign/col-valign` | enum | Alignment enum (left/center/right or top/middle/bottom). |
| `column-gap` | int(px)/size token | Size/spacing value (px or token). |
| `columns` | list | List of data items. |
| `takeaway` | string | Full-width summary text below the columns. **Canonical.** Alias: `conclusion`. |
| `conclusion-align` | enum | Alignment enum (left/center/right or top/middle/bottom). |
| `conclusion-bold` | string | Value from props. |
| `conclusion-color` | color-token | Color token name (theme color). |
| `conclusion-size` | int(px)/size token | Size/spacing value (px or token). |
| `divider-color` | color-token | Color token name (theme color). |
| `icon-color` | color-token | Color token name (theme color). |
| `icon-size` | int(px)/size token | Size/spacing value (px or token). |
| `show-chevron` | bool | Boolean toggle (true/false). |
| `show-divider` | bool | Value from props. |
| `text-align` | enum | Alignment enum (left/center/right or top/middle/bottom). |
| `title` | string | Text string. |
| `value-color` | color-token | Color token name (theme color). |
| `value-size` | int(px)/size token | Size/spacing value (px or token). |
## Example — 3 columns with metrics and conclusion

```yaml
molecule: column-conclusion-card
title: Results at a Glance
text-align: center
value-color: primary
takeaway: Together these improvements deliver a step-change in customer satisfaction and operational efficiency.
show-chevron: true
columns:
  - icon: star
    value: "87"
    value-unit: "%"
    headline: Customer\nSatisfaction
    body: Up from 71 % in Q3, driven by faster resolution times
  - icon: trending_up
    value: "12.4"
    value-unit: M €
    headline: Revenue\nImpact
    body: Incremental ARR attributed to the new service tier
  - icon: schedule
    value: "−3"
    value-unit: days
    headline: Time to\nResolution
    color: success
    body: Median resolution cycle reduced across all priority levels
```

## Example — 2 columns, no icons, left-aligned text

```yaml
molecule: column-conclusion-card
text-align: left
show-chevron: false
takeaway: Addressing the gap in SMB onboarding unlocks the largest near-term growth lever.
conclusion-align: center
columns:
  - value: "62"
    value-unit: "%"
    headline: Current state
    body: Share of new SMB accounts that complete onboarding within 14 days
  - value: "89"
    value-unit: "%"
    headline: Target state
    color: primary
    body: Benchmark from top-quartile SaaS peers
```

## CSS design tokens

| Token                        | Description                        | Default via theme |
|------------------------------|------------------------------------|-------------------|
| `--color-primary`            | Default metric value color         | theme primary     |
| `--color-on-surface`         | Headline and conclusion text       | dark              |
| `--color-on-surface-variant` | Body text and icon default         | medium grey       |
| `--color-border-subtle`      | Conclusion divider line            | light grey        |
