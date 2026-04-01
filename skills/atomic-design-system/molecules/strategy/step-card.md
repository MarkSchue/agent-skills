# step-card

**Molecule slug:** `step-card`
**Domain:** strategy
**Category:** Process / Workflow

A numbered step layout with up to **5 equal columns**. Each column shows a large
number (or custom text / icon), a short colored accent line, a bold headline, and
body text below a full-width divider — ideal for process steps, how-it-works
sections, or phase overviews.

## Layout guidance

> **Column-width rule — always apply this when selecting a layout template.**
>
> | Steps | Recommended layout | Rationale |
> |---|---|---|
> | 1–3 | `grid-3` (equal columns) | Each step card occupies one equal column alongside other cards |
> | 4–5 | `grid-2-1-1` (wide left + 2 narrow) | The step card receives double width; narrow columns carry supporting cards (e.g. `numbered-list-card`, `stacked-text`) |
>
> With 4–5 steps, each step column is only ~¼ of the slide width in an equal
> grid — text wraps badly and numbers overflow. Giving the step-card a 2× wide
> slot (first column of `grid-2-1-1`) restores comfortable reading width per step.
>
> **Never** place a 4- or 5-step `step-card` in an equal `grid-3` or `grid-4` layout.

## Design anatomy

```
┌──────────────────────────────────────────────────────────────────┐
│  [Optional title header]                                         │
│  01            02            03            …                     │  ← large number
│  ─────         ─────         ─────                               │  ← accent line (colored)
│  Headline      Headline      Headline                            │  ← bold (wraps)
│  text          text          text                                │
├──────────────────────────────────────────────────────────────────┤  ← full-width divider
│  Body text     Body text     Body text                           │  ← regular weight
│  wraps…        wraps…        wraps…                              │
└──────────────────────────────────────────────────────────────────┘
```

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `accent-line-height` | int(px)/size token | Size/spacing value (px or token). |
| `accent-line-width` | int(px)/size token | Size/spacing value (px or token). |
| `active-color` | color-token | Color token name (theme color). |
| `active-step` | string | Value from props. |
| `body-color` | color-token | Color token name (theme color). |
| `default-color` | color-token | Color token name (theme color). |
| `divider-color` | color-token | Color token name (theme color). |
| `divider-position` | string | Value from props. |
| `done-color` | color-token | Color token name (theme color). |
| `headline-color` | color-token | Color token name (theme color). |
| `muted-color` | color-token | Color token name (theme color). |
| `number-size` | int(px)/size token | Size/spacing value (px or token). |
| `number-type` | string | Value from props. |
| `show-accent-line` | string | Value from props. |
| `steps` | string | List of data items. |
| `text_align/text-align` | enum | Alignment enum (left/center/right or top/middle/bottom). |
| `text_valign/text-valign` | enum | Alignment enum (left/center/right or top/middle/bottom). |
| `title` | string | Text string. |
## CSS design tokens

| Token                          | Description               | Default |
|--------------------------------|---------------------------|---------|
| `--color-step-active`          | Active step accent color  | `primary` |
| `--color-step-default`         | Default step accent color | `on-surface-variant` |
| `--color-step-divider`         | Horizontal divider color  | `border-subtle` |

## Example — 3 steps, auto-numbered, one active

```yaml
molecule: step-card
number-type: number
active-step: 3
steps:
  - headline: "Headline\nzwei Zeilen"
    body: "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt sadipscing elitr"
  - headline: "Headline\nzwei Zeilen"
    body: "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt sadipscing elitr"
  - headline: "Headline\nzwei Zeilen"
    body: "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt sadipscing elitr"
```

## Example — 4 steps with custom text labels and per-step status

```yaml
molecule: step-card
number-type: text
steps:
  - number: "A"
    headline: "Discover"
    body: "Identify requirements and stakeholders."
    status: done
  - number: "B"
    headline: "Design"
    body: "Blueprint the target architecture."
    status: done
  - number: "C"
    headline: "Build"
    body: "Implement core modules."
    status: active
  - number: "D"
    headline: "Launch"
    body: "Go-live and hypercare phase."
    status: muted
```

## Example — 5 steps with icons

```yaml
molecule: step-card
number-type: icon
active-step: 2
steps:
  - icon: "🔍"
    headline: "Assess"
    body: "Current state analysis"
  - icon: "🎯"
    headline: "Define"
    body: "Target picture and success metrics"
    status: active
  - icon: "🏗️"
    headline: "Build"
    body: "Core platform components"
  - icon: "🧪"
    headline: "Test"
    body: "Validation and UAT"
  - icon: "🚀"
    headline: "Deploy"
    body: "Cutover and hypercare"
```
