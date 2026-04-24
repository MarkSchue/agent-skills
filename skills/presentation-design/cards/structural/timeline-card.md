# Timeline Card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

Card that renders a timeline with milestone markers, optional entry icons, an arrowhead, and a goal block â€” all drawn from primitives (no images).

## Layout

### Horizontal (default)

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  [title]                                          [icon: â—]      â”‚
â”‚  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ (header line)       â”‚
â”‚                                                                  â”‚
â”‚        Q1              Q3               Q5                       â”‚
â”‚   [ðŸš€] Kickoff    [ðŸ”§] Build       [âœ“] Review                   â”‚
â”‚   Team formed     Feature sprint   QA & fixes                   â”‚
â”‚                                                                  â”‚
â”‚  â”€â”€â”€â”€â—â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â—â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â—â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¶  â”‚
â”‚                    Q2                  Q4             ðŸ Launch   â”‚
â”‚               [ðŸ“] Design         [ðŸš€] Deploy      Go-live!      â”‚
â”‚               Blueprint          CI/CD ready                     â”‚
â”‚                                                                  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

Markers sit on a horizontal spine line. Content alternates above/below (or all below if `alternate: false`). Optional arrowhead at the end. Optional goal block at the far right.

### Vertical

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  [title]                                                        â”‚
â”‚  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ (header line)                   â”‚
â”‚                                                                 â”‚
â”‚  â—â”€â”€ [ðŸš€] Kickoff                                               â”‚
â”‚  â”‚         Team formed                                          â”‚
â”‚  â—â”€â”€ [ðŸ“] Design                                                â”‚
â”‚  â”‚         Blueprint                                            â”‚
â”‚  â—â”€â”€ [ðŸ”§] Build                                                 â”‚
â”‚  â”‚         Feature sprint                                       â”‚
â”‚  â–¼                                                              â”‚
â”‚  â˜…â”€â”€ [ðŸ] Launch                                                â”‚
â”‚            Go-live!                                             â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

Milestones run top-to-bottom on a vertical spine. Content sits to the right of each marker. An optional downward arrow ends the spine. The goal is marked with the accent color fill.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `timeline-card` |
| `content.milestones` | list | One or more milestone objects (see below) |

### Milestone Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `marker` | string | `""` | Label inside the spine dot: date (`"Q1"`), calendar week (`"CW12"`), number (`"1"`), or icon ligature (`"check_circle"`) |
| `heading` | string | â€” | Entry title (bold) |
| `body` | string | â€” | Description text |
| `icon.name` | string | â€” | Material icon ligature shown beside the heading |
| `icon.color` | string | token | Icon color override |
| `accent` | bool | `false` | Highlight milestone with accent color |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content.orientation` | string | `horizontal` | `horizontal` \| `vertical` |
| `content.alternate` | bool | `true` | Alternate entries above/below in horizontal mode |
| `content.arrow` | bool | `true` | Show arrowhead at end of spine |
| `content.goal` | object | â€” | Terminal goal block (same fields as a milestone, always accent-styled) |
| `content.caption` | string | â€” | Attribution line at bottom |
| `content.footer` | string | â€” | Footer text (base class) |
| `subtitle` | string | â€” | Subtitle below the header line |
| `icon.name` | string | â€” | Card-level icon in the title row |

### Goal Fields (same as Milestone)

| Field | Type | Description |
|-------|------|-------------|
| `goal.heading` | string | Goal title |
| `goal.body` | string | Goal description |
| `goal.marker` | string | Marker label (e.g. `"ðŸ"` or `"flag"`) |
| `goal.icon.name` | string | Icon beside the goal heading |

## Design Tokens (`.card--timeline`)

| Token | Default | Description |
|-------|---------|-------------|
| `--card-timeline-spine-color` | border | Spine line color |
| `--card-timeline-spine-width` | `2` | Spine stroke width (px) |
| `--card-timeline-orientation` | `horizontal` | Default orientation |
| `--card-timeline-alternate` | `true` | Default alternation for horizontal |
| `--card-timeline-arrow` | `true` | Show arrowhead by default |
| `--card-timeline-arrow-size` | `10` | Arrowhead leg length (px) |
| `--card-timeline-connector-length` | `10` | Tick line from spine to content (px) |
| `--card-timeline-marker-size` | `28` | Spine dot diameter (px) |
| `--card-timeline-marker-fill` | accent | Default marker background |
| `--card-timeline-marker-stroke` | accent | Marker border color |
| `--card-timeline-marker-font-size` | `8` | Text inside marker (px) |
| `--card-timeline-marker-font-color` | `#FFFFFF` | Text color inside marker |
| `--card-timeline-accent-marker-fill` | warning | Highlighted milestone fill |
| `--card-timeline-goal-marker-fill` | accent-alt | Goal marker fill |
| `--card-timeline-heading-font-size` | `11` | Entry heading font size (px) |
| `--card-timeline-heading-font-color` | text-primary | Entry heading color |
| `--card-timeline-heading-font-weight` | `700` | Entry heading weight |
| `--card-timeline-body-font-size` | `9` | Entry body font size (px) |
| `--card-timeline-body-font-color` | text-muted | Entry body color |
| `--card-timeline-icon-size` | `13` | Icon beside heading (px) |
| `--card-timeline-icon-gap` | `3` | Gap between icon and heading |
| `--card-timeline-icon-color` | accent | Default icon color |
| `--card-timeline-caption-font-size` | `10` | Caption font size (px) |
| `--card-timeline-caption-font-color` | text-muted | Caption color |
| `--card-timeline-caption-alignment` | `center` | Caption alignment |

## Examples

### Horizontal roadmap (alternating, with goal)

```yaml
type: timeline-card
title: "Project Roadmap 2026"
icon:
  name: "route"
  visible: true
content:
  orientation: horizontal
  alternate: true
  arrow: true
  milestones:
    - marker: "Q1"
      icon:
        name: "groups"
      heading: "Kickoff"
      body: "Team alignment and scope"
    - marker: "Q2"
      icon:
        name: "architecture"
      heading: "Design"
      body: "Architecture blueprint"
    - marker: "Q3"
      icon:
        name: "build"
      heading: "Build"
      body: "Feature development"
    - marker: "Q4"
      icon:
        name: "rocket_launch"
      heading: "Deploy"
      body: "Staged rollout"
  goal:
    marker: "flag"
    heading: "Go-Live"
    body: "Full production launch"
    icon:
      name: "verified"
  caption: "Source: PMO Office"
```

### Vertical process flow (no alternation, no arrow)

```yaml
type: timeline-card
title: "Onboarding Process"
content:
  orientation: vertical
  arrow: true
  milestones:
    - marker: "1"
      icon:
        name: "person_add"
      heading: "Account created"
      body: "User receives welcome email"
    - marker: "2"
      icon:
        name: "settings"
      heading: "Profile setup"
      body: "Preferences and integrations"
    - marker: "3"
      icon:
        name: "school"
      heading: "Training"
      body: "Onboarding modules completed"
    - marker: "check_circle"
      accent: true
      heading: "Activated"
      body: "All features unlocked"
  goal:
    marker: "star"
    heading: "Champion"
    body: "Power user milestone reached"
    icon:
      name: "emoji_events"
```

### Per-card token override

```yaml
type: timeline-card
style_overrides:
  card-timeline-spine-color: "#003087"
  card-timeline-marker-fill: "#003087"
  card-timeline-marker-stroke: "#003087"
  card-timeline-goal-marker-fill: "#E2001A"
  card-heading-font-color: "#003087"
content:
  orientation: horizontal
  milestones:
    - marker: "Jan"
      heading: "Phase 1"
      body: "Initiation"
    - marker: "Mar"
      heading: "Phase 2"
      body: "Execution"
  goal:
    marker: "flag"
    heading: "Complete"
    body: "Project handover"
```
