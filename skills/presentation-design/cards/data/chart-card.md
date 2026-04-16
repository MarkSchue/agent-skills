# Chart Card

Card that renders charts natively from data — no image dependency. Supports bar, line, pie, and combo (bar+line) chart types, all drawn from primitives so they work in both draw.io and PPTX output.

## Layout

```
┌─────────────────────────────────────────────────────┐
│  [text-label: card title]          [icon: ●]        │
│  ─────────────────────────────── (header line)      │
│  [text-caption: subtitle]                           │
│                                                     │
│  [legend — top (if position: top)]                  │
│                                                     │
│  y│  [chart area]          │[legend — right]        │
│   │  bars / lines / pie    │                        │
│   └──────────────────      │                        │
│       x-axis labels                                 │
│                                                     │
│  [legend — bottom (default)]                        │
│  [text-caption: source attribution]                 │
│                                                     │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  (footer line, opt.)      │
│  [text-caption: footer]      (optional, base class)  │
└─────────────────────────────────────────────────────┘
```

## Supported Chart Types

| `chart_type` | Description |
|---|---|
| `bar` | Vertical grouped or stacked bars |
| `line` | Lines with optional data-point markers |
| `pie` | Pie or donut chart |
| `combo` | Bars + line overlay (mixed per series) |

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `chart-card` |
| `content.chart_type` | string | `bar` \| `line` \| `pie` \| `combo` (default: `bar`) |
| `content.labels` | list | Category axis labels (one per data point) |
| `content.series` | list | One or more series objects (see below) |

### Series Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | string | `"Series N"` | Label shown in the legend |
| `values` | list of floats | — | One numeric value per label |
| `color` | string | palette | Hex color override (e.g. `"#E2001A"`) |
| `type` | string | — | `bar` or `line` — **combo only** |
| `marker` | string | `circle` | Marker shape on line series: `circle` \| `square` \| `none` |
| `dashed` | bool | `false` | Dashed stroke for line series |
| `width` | int | token | Stroke width in px for line series |

For **pie** charts with a single series, you may also use a `colors` list (one color per label):
```yaml
series:
  - name: "Share"
    values: [40, 30, 20, 10]
    colors: ["#3B82F6", "#EF4444", "#10B981", "#F59E0B"]
```

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content.stacked` | bool | `false` | Stack bars instead of grouping |
| `content.value_labels` | bool | `false` | Show data-value labels on bars/points |
| `content.inner_radius` | float 0–0.9 | `0` | Donut hole size (pie only); `0` = full pie |
| `content.caption` | string | — | Attribution / source line below chart |
| `content.x_axis.title` | string | — | X-axis title label |
| `content.x_axis.visible` | bool | `true` | Show/hide x-axis labels |
| `content.y_axis.title` | string | — | Y-axis title label |
| `content.y_axis.visible` | bool | `true` | Show/hide y-axis tick labels |
| `content.y_axis.min` | float | auto | Override y-axis minimum |
| `content.y_axis.max` | float | auto | Override y-axis maximum |
| `content.y_axis.step` | float | auto | Override tick step |
| `content.y_axis.format` | string | auto | Python format string for tick labels: `%`, `.1f`, `,.0f`, … |
| `content.legend.visible` | bool | `true` | Show/hide legend |
| `content.legend.position` | string | token | `bottom` \| `right` \| `top` \| `none` |
| `content.footer` | string | — | Footer text (base class handles rendering) |
| `subtitle` | string | — | Subtitle below the header line |
| `icon.name` | string | — | Icon ligature (e.g. `"bar_chart"`) |
| `icon.visible` | bool | `false` | Show/hide icon |
| `icon.position` | string | `right` | `left` \| `right` |
| `icon.color` | string | accent | Icon color |

## Design Tokens (`.card--chart`)

Override any token globally in your `theme.css` or per-card via `style_overrides`:

| Token | Default | Description |
|-------|---------|-------------|
| `--card-chart-axis-color` | text-muted | Axis spine and fallback tick-label color |
| `--card-chart-axis-font-size` | `9` | Tick-label font size (px) |
| `--card-chart-axis-font-color` | axis-color | Tick-label color |
| `--card-chart-axis-title-font-size` | `10` | Axis-title font size (px) |
| `--card-chart-axis-title-font-color` | text-muted | Axis-title color |
| `--card-chart-grid-color` | surface-raised | Horizontal grid-line color |
| `--card-chart-palette-1` … `-8` | built-in palette | Series color cycle |
| `--card-chart-line-width` | `2` | Default line stroke width (px) |
| `--card-chart-line-marker-size` | `5` | Data-point marker diameter (px) |
| `--card-chart-label-font-size` | `8` | Data-label font size (px) |
| `--card-chart-label-font-color` | `#FFFFFF` | Data-label color (inside bars) |
| `--card-chart-legend-font-size` | `10` | Legend text size (px) |
| `--card-chart-legend-font-color` | text-primary | Legend text color |
| `--card-chart-legend-position` | `bottom` | Default legend position |
| `--card-chart-caption-font-size` | `10` | Caption font size (px) |
| `--card-chart-caption-font-color` | text-muted | Caption color |
| `--card-chart-caption-alignment` | `center` | Caption alignment |
| `--card-chart-bg-color` | `#FFFFFF` | Background used for donut punch-out |

## Examples

### Bar chart

```yaml
type: chart-card
title: "Revenue by Quarter"
content:
  chart_type: bar
  labels: ["Q1", "Q2", "Q3", "Q4"]
  y_axis:
    title: "EUR (k)"
    max: 500
  series:
    - name: "2023"
      values: [280, 340, 310, 420]
      color: "#3B82F6"
    - name: "2024"
      values: [310, 380, 360, 470]
      color: "#10B981"
  legend:
    position: bottom
  caption: "Source: Finance"
```

### Stacked bar

```yaml
type: chart-card
title: "Cost Breakdown"
content:
  chart_type: bar
  stacked: true
  labels: ["Jan", "Feb", "Mar", "Apr"]
  series:
    - name: "Fixed"
      values: [100, 100, 100, 100]
    - name: "Variable"
      values: [40, 55, 48, 62]
    - name: "One-off"
      values: [0, 200, 0, 30]
  value_labels: true
```

### Line chart

```yaml
type: chart-card
title: "Monthly Active Users"
content:
  chart_type: line
  labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
  y_axis:
    min: 0
    format: ",.0f"
  series:
    - name: "Users"
      values: [1200, 1400, 1350, 1600, 1750, 1900]
      color: "#3B82F6"
      marker: circle
    - name: "Target"
      values: [1300, 1500, 1500, 1700, 1800, 2000]
      color: "#9CA3AF"
      dashed: true
      marker: none
```

### Pie / donut chart

```yaml
type: chart-card
title: "Market Share"
content:
  chart_type: pie
  inner_radius: 0.55      # 0 = full pie, >0 = donut
  labels: ["Product A", "Product B", "Product C", "Other"]
  series:
    - name: "Share"
      values: [42, 28, 18, 12]
  value_labels: true
  legend:
    position: right
```

### Combo chart (bar + line)

```yaml
type: chart-card
title: "Revenue vs. Growth Rate"
content:
  chart_type: combo
  labels: ["Q1", "Q2", "Q3", "Q4"]
  series:
    - name: "Revenue (k€)"
      type: bar
      values: [280, 340, 310, 420]
      color: "#3B82F6"
    - name: "Growth %"
      type: line
      values: [5, 21, -9, 35]
      color: "#EF4444"
      marker: circle
  y_axis:
    title: "EUR (k) / %"
```

### Per-card token override

```yaml
type: chart-card
title: "Customer Satisfaction"
style_overrides:
  card-chart-legend-position: right
  card-chart-palette-1: "#E2001A"
  card-chart-palette-2: "#003087"
content:
  chart_type: bar
  labels: ["Jan", "Feb", "Mar"]
  series:
    - name: "Score"
      values: [7.2, 7.8, 8.1]
```

