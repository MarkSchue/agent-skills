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

| Parameter            | Type   | Default              | Description |
|----------------------|--------|----------------------|-------------|
| `title`              | string | —                    | Optional card header title |
| `steps`              | list   | **required**         | Array of step objects (1–5 items) |
| `number-type`        | enum   | `number`             | `number` auto 01,02… · `text` (reads step `number`) · `icon` (reads step `icon`) · `none` |
| `active-step`        | int    | `0` (none)           | 1-based index — automatically highlights that column with `active-color` |
| `active-color`       | color  | `primary`            | Accent color for the active/highlighted step |
| `default-color`      | color  | `on-surface-variant` | Accent color for steps without a status |
| `done-color`         | color  | `success`            | Accent color for `status: done` steps |
| `muted-color`        | color  | `border-subtle`      | Accent color for `status: muted` steps |
| `number-size`        | int    | auto                 | Explicit font-size in px for the large number |
| `show-accent-line`   | bool   | `true`               | Draw the short colored bar under the number |
| `accent-line-width`  | float  | `0.35`               | Fraction of column width for the accent bar |
| `accent-line-height` | int    | `3`                  | Thickness of accent bar in px |
| `divider-position`   | float  | `0.52`               | 0..1 fraction of content height where the horizontal divider sits |
| `divider-color`      | color  | `border-subtle`      | Full-width divider line color |
| `headline-color`     | color  | `on-surface`         | Global override for all headline texts |
| `body-color`         | color  | `on-surface-variant` | Global override for all body texts |
| `show-header`        | bool   | auto                 | Show/hide card title header |
| `show-header-line`   | bool   | `true`               | Show/hide line below title header |
| `bg-color`           | color  | `bg-card`            | Card background override |

### Step object fields

| Field        | Type   | Required | Description |
|--------------|--------|----------|-------------|
| `headline`   | string | yes      | Bold step title |
| `body`       | string | no       | Supporting text shown in the lower zone |
| `number`     | string | no       | Custom label when `number-type: text` |
| `icon`       | string | no       | Icon description when `number-type: icon` |
| `badge`      | string | no       | Alias for `number` / `icon` |
| `status`     | enum   | no       | `active` · `done` · `muted` · `default` — controls accent color |
| `color`      | color  | no       | Per-step explicit color override (overrides status) |

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
