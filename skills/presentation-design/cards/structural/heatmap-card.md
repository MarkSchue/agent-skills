# Heatmap Card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

A grid of **clusters** (business domains, departments, categories) each containing
**fact tiles** whose background colour encodes a 6-level heat value.  The visual
idiom is identical to a heat-map matrix used in application portfolio reviews,
risk assessments, and status dashboards.

---

## Layout

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  Card Title                                                                      â”‚
â”‚ â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€  â”‚
â”‚                                                                                  â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ â”‚
â”‚  â”‚â–ˆâ–ˆâ–ˆ HR â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ”‚  â”‚â–ˆâ–ˆâ–ˆ Information Technology â”‚  â”‚â–ˆâ–ˆâ–ˆ Manufacturing  â”‚
â”‚  â”‚ â”Œâ”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”â”‚  â”‚ â”Œâ”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”â”‚  â”‚ â”Œâ”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€ â”‚
â”‚  â”‚ â”‚ ERP  â”‚ â”‚ CRM  â”‚ â”‚ HCM  â”‚â”‚  â”‚ â”‚Jira  â”‚ â”‚ VPN  â”‚ â”‚ MES  â”‚â”‚  â”‚ â”‚ CAD  â”‚ â”‚ PLM  â”‚
â”‚  â”‚ â””â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”˜â”‚  â”‚ â””â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”˜â”‚  â”‚ â””â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€ â”‚
â”‚  â”‚ â”Œâ”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”         â”‚  â”‚ â”Œâ”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”         â”‚  â”‚ â”Œâ”€â”€â”€â”€â”€â”€â”        │
│  │ │Payrl │ │T&A   │         │  │ │LDAP  │ │ ITSM │         │  │ │ OEE  │        │
│  │ └──────┘ └──────┘         │  │ └──────┘ └──────┘         │  │ └──────┘        │
│  └──────────────────────────┘  └──────────────────────────┘  └────────────────── │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

- **███** — filled heading bar (cluster label; colour = `--card-heatmap-cluster-heading-bg`)
- Fact tiles are coloured by their `level` field using `--color-heat-{0..5}` tokens
- Clusters are equal-sized (height driven by the cluster with the most facts)
- Pagination: set `content.page` to `2`, `3`, … on subsequent slides to show more clusters

---

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `heatmap-card` |
| `content.clusters` | list | List of cluster objects (see Cluster Fields) |
| `content.clusters[].name` | string | Cluster heading label |
| `content.clusters[].facts` | list | List of fact objects inside this cluster |
| `content.clusters[].facts[].text` | string | Fact tile label text |

---

## Cluster Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✓ | Cluster heading displayed in the heading bar |
| `facts` | list | ✓ | List of fact objects (see Fact Fields below) |

---

## Fact Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | ✓ | Label displayed inside the fact tile |
| `level` | int | — | Heat level 0–5 (default: `0`); controls tile background colour |

### Heat Levels

| Level | Meaning | Default colour | Default text |
|-------|---------|---------------|--------------|
| `0` | Not applicable / no data | `#E5E7EB` (gray) | dark |
| `1` | Low / healthy | `#22C55E` (green) | dark |
| `2` | Low-medium | `#84CC16` (lime) | dark |
| `3` | Medium / notable | `#EAB308` (yellow) | dark |
| `4` | High / elevated | `#F97316` (orange) | white |
| `5` | Critical / maximum | `#EF4444` (red) | white |

Colours resolve from `--color-heat-{level}` tokens in `.theme-colors`.
Override them in your project `theme.css` to apply theme-specific ramps.

---

## Content Options

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content.cluster_columns` | int | 4 | Number of cluster columns per row (overrides CSS token) |
| `content.fact_columns` | int | 3 | Number of fact columns inside every cluster (overrides CSS token) |
| `content.page` | int | 1 | 1-based page; clusters are sliced into windows of `cluster_columns × rows_that_fit` |

---

## Style Overrides (per card)

Pass any `--card-heatmap-*` token (or a `.card-base` token) as a `style_overrides`
key using underscores (e.g. `card_heatmap_cluster_columns`):

| Override key | CSS token | Example value |
|---|---|---|
| `card_heatmap_cluster_columns` | `--card-heatmap-cluster-columns` | `3` |
| `card_heatmap_cluster_gap` | `--card-heatmap-cluster-gap` | `8` |
| `card_heatmap_cluster_padding` | `--card-heatmap-cluster-padding` | `8` |
| `card_heatmap_cluster_border_color` | `--card-heatmap-cluster-border-color` | `#374151` |
| `card_heatmap_cluster_border_width` | `--card-heatmap-cluster-border-width` | `0` |
| `card_heatmap_cluster_border_radius` | `--card-heatmap-cluster-border-radius` | `0` |
| `card_heatmap_cluster_heading_bg` | `--card-heatmap-cluster-heading-bg` | `var(--color-secondary)` |
| `card_heatmap_cluster_heading_font_color` | `--card-heatmap-cluster-heading-font-color` | `#FFFFFF` |
| `card_heatmap_cluster_heading_font_size` | `--card-heatmap-cluster-heading-font-size` | `12` |
| `card_heatmap_cluster_heading_height` | `--card-heatmap-cluster-heading-height` | `26` |
| `card_heatmap_cluster_heading_alignment` | `--card-heatmap-cluster-heading-alignment` | `center` |
| `card_heatmap_fact_columns` | `--card-heatmap-fact-columns` | `4` |
| `card_heatmap_fact_gap` | `--card-heatmap-fact-gap` | `4` |
| `card_heatmap_fact_height` | `--card-heatmap-fact-height` | `40` |
| `card_heatmap_fact_border_radius` | `--card-heatmap-fact-border-radius` | `0` |
| `card_heatmap_fact_font_size` | `--card-heatmap-fact-font-size` | `10` |
| `card_heatmap_fact_text_alignment` | `--card-heatmap-fact-text-alignment` | `left` |
| `card_heatmap_page` | `--card-heatmap-page` | `2` |

---

## Design Tokens Used

- `.card-base` — container, card title, header line, subtitle, footer
- `.card--heatmap` — all cluster and fact tile tokens (see above)
- `.theme-colors` — `--color-heat-{0..5}` and `--color-on-heat-{0..5}` (global heat scale)

---

## Pagination

All clusters are declared once in the card YAML.  The renderer automatically
divides them into pages.  To show additional clusters on a new slide, duplicate
the card YAML and set `content.page: 2` (or use `style_overrides.card_heatmap_page: 2`).

The number of clusters that fit on a single page is:
```
clusters_per_page = cluster_columns × cluster_rows_that_fit
```
where `cluster_rows_that_fit` is derived from available card body height and uniform
cluster height (itself driven by the cluster with the most facts).

---

## Example

```yaml
type: heatmap-card
title: Application Portfolio Heatmap
subtitle: "Heat = modernisation urgency (1 = low, 5 = critical)"
content:
  cluster_columns: 4
  fact_columns: 3
  clusters:
    - name: HR
      facts:
        - text: ERP Suite
          level: 3
        - text: Payroll Global
          level: 4
        - text: SAP SuccessFactors
          level: 1
        - text: HR Admin / HR Plan
          level: 5
        - text: Time Track
          level: 2
        - text: Training Management
          level: 0
    - name: Information Technology
      facts:
        - text: Atlassian Confluence
          level: 1
        - text: BYOD Directory
          level: 3
        - text: HP Service Desk
          level: 2
        - text: Issue Tracking
          level: 1
        - text: SAP LeanIX
          level: 4
        - text: SLA Tracking
          level: 5
        - text: VPN
          level: 0
    - name: Innovation
      facts:
        - text: HypeCollab
          level: 1
        - text: Idea Club
          level: 5
        - text: IdeaIT
          level: 2
        - text: OpenInno
          level: 3
    - name: Inventory
      facts:
        - text: BPM
          level: 2
        - text: ERP Suite
          level: 3
        - text: JIT Reporting
          level: 1
        - text: Stocky
          level: 4
        - text: WMS large
          level: 5
        - text: WMS special
          level: 0
```

---

## Example — Paginated (page 2)

```yaml
type: heatmap-card
title: Application Portfolio Heatmap (continued)
content:
  cluster_columns: 4
  fact_columns: 3
  page: 2
  clusters:
    # ... same cluster list as page 1 slide; renderer auto-selects page 2 window
```

---

## Example — Per-Card Token Override

```yaml
type: heatmap-card
title: Risk Heatmap
content:
  cluster_columns: 3
  clusters:
    - name: Finance
      facts:
        - text: ERP
          level: 4
        - text: Reporting
          level: 2
style_overrides:
  card_heatmap_cluster_heading_bg: var(--color-secondary)
  card_heatmap_cluster_border_width: 0
  card_heatmap_fact_height: 40
  card_heatmap_fact_font_size: 10
```
