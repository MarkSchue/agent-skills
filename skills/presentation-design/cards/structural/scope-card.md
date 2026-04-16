# Scope Card

A visual grid of tiles that communicates the **in/out-of-scope** boundary of a project.
Each tile shows one topic with a status-coloured badge marker, a bold title, and an
optional body text. The grid adapts from 1 to 4 columns.

---

## Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Card Title                                                      │
│ ──────────────────────────────────────────────────────────────  │
│                                                                  │
│  ┌───────────────────────────┐  ┌───────────────────────────┐   │
│  │ ① Data Migration          │  │ ② Reporting               │   │
│  │   Move legacy records…    │  │   Standard reports only.  │   │
│  └───────────────────────────┘  └───────────────────────────┘   │
│                                                                  │
│  ┌───────────────────────────┐  ┌───────────────────────────┐   │
│  │ ✓ API Integration         │  │ ⊘ Mobile App              │   │
│  │   REST endpoints v2.      │  │   Out of current scope.   │   │
│  └───────────────────────────┘  └───────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

- **①** — number badge (marker: number, status: in-scope → accent colour)
- **✓** — checkmark icon badge (marker: check)
- **⊘** — muted badge (status: out-of-scope → text-muted colour)

---

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `scope-card` |
| `content.items` | list | List of scope items (see Item Fields below) |
| `content.items[].heading` | string | Item heading (displayed bold beside the badge) |

---

## Item Fields

| Field | Type | Required | Description |
|-------|------|----------|--------------|
| `heading` | string | ✓ | Bold item heading |
| `body` | string | — | Optional muted text below the heading |
| `status` | string | — | `in-scope` (default) · `out-of-scope` · `conditional` |
| `icon` | string | — | Material Symbols ligature used when `marker=icon` (e.g. `"storage"`) |

---

## Content Options

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content.layout_columns` | int | 2 | Number of tile columns (1–4); overrides CSS token |

---

## Style Overrides (per card)

Pass any `--card-scope-*` token (or a `.card-base` token) as a `style_overrides` key using
underscores and the base token name:

| Override key | CSS token | Example value |
|---|---|---|
| `card_columns` | `--card-scope-columns` | `3` |
| `card_item_gap` | `--card-scope-item-gap` | `8` |
| `card_item_marker` | `--card-scope-item-marker` | `check` |
| `card_check_icon_name` | `--card-scope-check-icon-name` | `task_alt` |
| `card_badge_size` | `--card-scope-badge-size` | `24` |
| `card_item_bg_color` | `--card-scope-item-bg-color` | `transparent` |
| `card_item_border_width` | `--card-scope-item-border-width` | `0` |
| `card_status_in_scope_color` | `--card-scope-status-in-scope-color` | `#10B981` |
| `card_status_label_visible` | `--card-scope-status-label-visible` | `true` |
| `card_heading_font_color` | `--card-heading-font-color` | `var(--color-primary)` |
| `card_body_font_color` | `--card-body-font-color` | `var(--color-text-muted)` |

---

## Design Tokens Used

- `.card-base` — container, card title, header line, footer
- `.card--scope` — all tile and badge tokens (see [token-reference.md](../references/token-reference.md))

---

## Marker Mode

Controlled by `--card-scope-item-marker` (or `style_overrides.card_item_marker`):

| Value | Behaviour |
|-------|-----------|
| `number` | Sequential number (1, 2, 3 …) inside a filled circle — **default** |
| `check` | Checkmark icon (from `--card-scope-check-icon-name`) inside a filled circle |
| `icon` | Per-item `icon` field used as icon name; falls back to `--card-scope-check-icon-name` |

The badge circle fill is always driven by the item `status` field.

---

## Status Values

| Value | Badge colour token | Meaning |
|-------|--------------------|---------|
| `in-scope` _(default)_ | `--card-scope-status-in-scope-color` | Topic is in scope |
| `out-of-scope` | `--card-scope-status-out-of-scope-color` | Explicitly excluded |
| `conditional` | `--card-scope-status-conditional-color` | Depends on conditions |

---

## Example

```yaml
type: scope-card
title: Project Scope Overview
content:
  layout_columns: 2
  items:
    - heading: Data Migration
      body: Move all legacy records to the new platform.
      status: in-scope
    - heading: Standard KPI Reports
      body: Standard KPI reports included; custom dashboards excluded.
      status: conditional
    - heading: API Integration
      body: REST endpoints for ERP and CRM systems.
      status: in-scope
    - heading: Mobile App
      body: Planned for Phase 2 only.
      status: out-of-scope
    - heading: User Training
      body: End-user onboarding workshops.
      status: in-scope
    - heading: Data Archiving
      body: Automated archiving of records older than 7 years.
      status: in-scope
```

---

## Example — Custom Icon Marker

```yaml
type: scope-card
title: Technical Scope
content:
  items:
    - heading: Cloud Infrastructure
      body: AWS multi-region deployment.
      status: in-scope
      icon: cloud
    - heading: On-Premises Servers
      status: out-of-scope
      icon: dns
    - heading: CI/CD Pipeline
      body: GitHub Actions workflows.
      status: in-scope
      icon: rocket_launch
style_overrides:
  card-item-marker: icon
  card-badge-size: 22
```

---

## Notes

- The number badge uses `type: ellipse` (circle) internally — the same primitive used by
  `numbered-text-card` and `timeline-card`.
- Setting `--card-scope-item-border-width: 0` and `--card-scope-item-bg-color: transparent`
  produces a minimal, border-free layout where tiles are separated by whitespace only.
- The `status-label-visible` token renders a small coloured status string at the bottom-right
  of each tile — useful when readers need an explicit legend.
