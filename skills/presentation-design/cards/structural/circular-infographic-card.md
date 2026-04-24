# circular-infographic-card
<!-- inheritance-note v1 -->
> **Inherits from `BaseCardRenderer`.** This card automatically gets the
> base chrome — container background/border/radius, title + header line,
> optional footer text and footer line — plus the 4-level token resolution
> chain (card override → slide override → variant CSS → base CSS). The
> renderer overrides only `render_body`; suppress unwanted chrome via
> tokens (e.g. `--card-title-visible: false`, `--card-padding: 0`).

> Concentric ring infographic with an inner and an outer ring. Each ring
> is divided into N equal angular segments (different colours). One
> segment per ring may be marked `highlighted: true`, which bumps it
> outward to draw the eye.

## When to use

- Capability wheels / framework wheels (e.g. inner pillars + outer
  practices).
- Any "X powers Y" relationship where the inner concept is the
  foundation for the outer cycle.
- Process wheels where a particular phase needs to be the focus.

## Content schema

```yaml
type: circular-infographic-card
content:
  inner_ring:
    segments:
      - { label: "Strategy" }
      - { label: "People"   }
      - { label: "Process", highlighted: true }
      - { label: "Tech"     }
  outer_ring:
    segments:
      - { label: "Discover" }
      - { label: "Define"   }
      - { label: "Design"   }
      - { label: "Build"    }
      - { label: "Operate", highlighted: true }
      - { label: "Govern"   }
```

## Per-segment keys

| key           | type    | required | description                              |
|---------------|---------|----------|------------------------------------------|
| `label`       | string  | optional | Label drawn at the segment mid-radius.   |
| `color`       | hex str | optional | Override segment fill (else palette).    |
| `highlighted` | bool    | optional | If true, segment outer radius bumps out. |

## Tokens (variant `card--circular-infographic`)

| token                                                       | default                       | purpose                                    |
|-------------------------------------------------------------|-------------------------------|--------------------------------------------|
| `--card-circular-infographic-outer-radius-pct`              | `0.95`                        | of `min(box.w, box.h)/2`                   |
| `--card-circular-infographic-inner-radius-pct`              | `0.55`                        | inner ring **outer** radius                |
| `--card-circular-infographic-inner-hole-pct`                | `0.35`                        | inner ring **inner** radius / its outer    |
| `--card-circular-infographic-ring-gap`                      | `6`                           | px between inner and outer rings           |
| `--card-circular-infographic-highlight-bump`                | `14`                          | px outward bump for highlighted segments   |
| `--card-circular-infographic-segment-stroke-color`          | `var(--color-surface)`        | divider lines between segments             |
| `--card-circular-infographic-segment-stroke-width`          | `2`                           |                                            |
| `--card-circular-infographic-label-font-size`               | `11`                          |                                            |
| `--card-circular-infographic-label-font-color`              | `#FFFFFF`                     |                                            |
| `--card-circular-infographic-label-font-weight`             | `bold`                        |                                            |
| `--card-circular-infographic-palette`                       | primary + 7 tints/shades      | semicolon-separated hex list (fallback colours) |

## Notes

- Recommended layout: `grid-1x1`. The wheel auto-centres in the body.
- Number of segments per ring can differ (e.g. inner=4, outer=6).
- Labels are skipped automatically when a segment angle is < 12Â°.
- The `style: arrow` flag on a ring is reserved (currently behaves like
  `donut`); a future revision will add chevron-tipped segments.
