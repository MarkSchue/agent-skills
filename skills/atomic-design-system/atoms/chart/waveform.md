# Atom: chart-waveform

```yaml
id: chart-waveform
type: data-viz
description: Amplitude bar waveform from normalized values or auto-generated sample. Suitable for signal, audio, or any time-series amplitude data.
tags: [chart, waveform, amplitude, audio, signal, visualization, data-viz]
preview: previews/atoms/chart-waveform.png
```

## Data Input Schema
```yaml
data-input-schema:
  values:      list[number], required: false   # normalized 0.0–1.0 amplitudes; auto-generates 20-bar sample if omitted
  bar-count:   integer, required: false, default: 20
  auto:        boolean, required: false, default: false  # generate natural-looking sample waveform
  color-token: color-token, required: false, default: "on-primary"
```

## Layout Primitive
```
layout: fill-zone
zone-role: viz-left
```
Bars are drawn bottom-anchored, filling the full zone width and height.
Bar width = `(zone_w - 2) / bar_count * 0.7`; gap = remaining width / (bar_count - 1).
Centre bars taller, edge bars shorter — natural waveform taper if `auto: true`.

## Visual Properties
| Property | Token |
|---|---|
| Bar fill | `{{theme.color.on-primary}}` (overridable via `color-token`) |
| Background | transparent (inherits card bg) |
| Bar radius | 2px |
| Min bar height | 4px |
| Max bar height | zone_h × 0.88 |

## Parameters
| Parameter | Type | Required | Description |
|---|---|---|---|
| `auto` | boolean | no |
| `bar-count` | integer | no |
| `color-token` | color-token | no |
| `values` | list[float 0–1] | no |
## Auto-Generate Algorithm
When `auto: true` or no `values` provided, generate bars using:
```python
import math
n = bar_count  # default 20
vals = [0.15 + 0.70 * math.sin(math.pi * i / (n-1)) ** 1.5 * (0.8 + 0.2 * ((i*7) % 5) / 4) for i in range(n)]
# Centre peak ≈ 0.85, edges ≈ 0.15–0.25
```

## Renderer Notes
- Clip all bars to zone bounds — never overflow card padding
- No axis labels, no gridlines — purely decorative data-viz

## CSS Class Map

| Element | CSS Class / Utility Combo | Applied Properties |
|---------|--------------------------|-------------------|
| Bar element | `.waveform__bar` → `u-bg-primary` | `background`, `border-radius` |
