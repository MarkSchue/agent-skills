# Pyramid Card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

Hierarchical pyramid (stacked-trapezoid) for strategic hierarchy, Maslow
needs, value pyramids, capability ladders or any "foundation → apex"
narrative. Layers stack bottom-up by default (the FIRST layer in `layers`
is the widest base; the LAST is the narrowest apex).

## Layout

```
                  ▲                    ┌─ Apex
                ▲▲▲▲                   │
              ▲▲▲▲▲▲▲▲                 │
            ▲▲▲▲▲▲▲▲▲▲▲▲               │
          ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲             ▼  Base
```

Labels sit to the right of the pyramid by default with leader lines
connecting to each layer. Set `card-pyramid-layer-label-position: inline`
to centre labels inside the layers instead.

## Required Fields (`content`)

| Field | Type | Description |
|-------|------|-------------|
| `layers` | list of dicts | Layers from base → apex (typically 3–5). |

Each layer supports:

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Layer heading. |
| `body` | string | Optional descriptive sentence. |
| `accent` | bool | If true, fills the layer with the accent colour and inverts text. |

## Optional Fields (`content`)

| Field | Type | Description |
|-------|------|-------------|
| `direction` | string | `"bottom-up"` (default — first listed = base) or `"top-down"` (first listed = apex). |

## Supported Overrides (`style_overrides`)

Any token from `.card--pyramid` — see [`themes/base.css`](../../themes/base.css)
section 24. Common overrides:

- `card-pyramid-layer-bg-color` / `layer-accent-bg-color` — layer fills.
- `card-pyramid-layer-label-position` — `right` (with leader lines) or `inline`.
- `card-pyramid-layer-gap` — px between layers (default `4`).
- `card-pyramid-label-line-color` / `label-line-width` — leader-line styling.

## Example — Strategic hierarchy

```yaml
type: pyramid-card
title: "EAM Maturity Pyramid"
content:
  layers:
    - title: "Foundation"
      body:  "Centralised system inventory & ownership"
    - title: "Capability"
      body:  "Documented integrations & automated quality gates"
    - title: "Insight"
      body:  "Metrics, trends and architectural KPIs"
      accent: true
    - title: "Strategy"
      body:  "Continuous portfolio rationalisation"
```

## Example — Inline labels

```yaml
type: pyramid-card
title: "Maslow's Hierarchy of Needs"
content:
  layers:
    - title: "Physiological"
    - title: "Safety"
    - title: "Belonging"
    - title: "Esteem"
    - title: "Self-actualisation"
      accent: true
style_overrides:
  card_pyramid_layer_label_position: inline
```
