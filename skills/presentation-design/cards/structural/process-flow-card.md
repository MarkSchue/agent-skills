# Process Flow Card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

Horizontal sequence of N right-pointing chevron steps that visually connect
into a flow. Use for project phases, methodology stages (e.g. Discover â†’
Design â†’ Deliver), customer journeys, or any sequential narrative. The final
step may be flagged as `accent: true` to highlight the goal / end state.

## Layout

```
â”Œâ”€â”€â”  â”Œâ”€â”€â”  â”Œâ”€â”€â”  â”Œâ”€â”€â”
â”‚01â”‚â–¶ â”‚02â”‚â–¶ â”‚03â”‚â–¶ â”‚04â”‚â–¶
â””â”€â”€â”˜  â””â”€â”€â”˜  â””â”€â”€â”˜  â””â”€â”€â”˜
 step  step  step  step (accent)
```

Each chevron contains a step number, a heading, and optional body text.

## Required Fields (`content`)

| Field | Type | Description |
|-------|------|-------------|
| `steps` | list of dicts | Ordered list of process steps (typically 3â€“6). |

Each step supports:

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Step heading. |
| `body` | string | Optional descriptive sentence. |
| `accent` | bool | If true, fills the chevron with the accent colour and inverts text. |

## Supported Overrides (`style_overrides`)

Any token from `.card--process-flow` â€” see [`themes/base.css`](../../themes/base.css)
section 23. Common overrides:

- `card-process-flow-step-bg-color` / `step-accent-bg-color` â€” chevron fills.
- `card-process-flow-chevron-tip-pct` â€” tip width as fraction of card height
  (default `0.18`; smaller = squarer steps).
- `card-process-flow-step-number-visible` â€” hide the large numeric label.
- `card-process-flow-step-heading-font-size` / `step-body-font-size`.

## Example â€” Project methodology

```yaml
type: process-flow-card
title: "Our Engagement Methodology"
content:
  steps:
    - title: "Discover"
      body:  "Frame the problem and align stakeholders."
    - title: "Design"
      body:  "Architect target state and option set."
    - title: "Deliver"
      body:  "Build, integrate, and test the solution."
    - title: "Drive Value"
      body:  "Operate, measure, and continuously improve."
      accent: true
```

## Example â€” Customer journey (no step numbers)

```yaml
type: process-flow-card
title: "Customer Onboarding Journey"
content:
  steps:
    - title: "Awareness"
      body:  "Marketing touchpoint"
    - title: "Sign-up"
      body:  "Account creation"
    - title: "Activation"
      body:  "First success moment"
      accent: true
style_overrides:
  card_process_flow_step_number_visible: false
```
