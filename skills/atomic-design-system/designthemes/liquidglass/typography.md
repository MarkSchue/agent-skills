# Apple Liquid Glass — Typography

**Source:** https://developer.apple.com/design/human-interface-guidelines/typography  
**Font system:** San Francisco (SF Pro)

---

## The San Francisco Type System

Apple Liquid Glass uses the **San Francisco** typeface family, designed specifically for
Apple platforms. It is automatically anti-aliased, hinted, and optically adjusted for
device pixel densities.

### Family Variants

| Variant | Use |
|---|---|
| **SF Pro Display** | Headlines ≥ 20pt. Slightly wider letter-spacing, optimized for large sizes |
| **SF Pro Text** | Body text < 20pt. Tighter tracking, optimized for small sizes |
| **SF Pro Rounded** | Badges, pills, expressive UI elements. Matches the squircle curve of Liquid Glass |
| **SF Mono** | Code, monospaced content |
| **SF Compact** | watchOS displays and compact layouts |

> In PPTX / draw.io: use `"SF Pro Display"` for all headings (≥20pt)
> and `"SF Pro Text"` or `"SF Pro"` for body/caption.
> Fall back to `"Helvetica Neue"` if SF Pro is not installed.

---

## Dynamic Type Scale (Liquid Glass Baseline)

Apple defines a **Dynamic Type** scale with 11 pre-defined text styles:

| Style | Size | Weight | Line Height | Token |
|---|---|---|---|---|
| Large Title | **34pt** | Bold (700) | 41pt / 1.21 | `heading` |
| Title 1 | 28pt | Bold (700) | 34pt / 1.21 | — |
| Title 2 | **22pt** | Semibold (600) | 28pt / 1.27 | `heading-sub` |
| Title 3 | 20pt | Regular (400) | 25pt / 1.25 | — |
| Headline | 17pt | Semibold (600) | 22pt / 1.29 | — |
| Body | **17pt** | Regular (400) | 22pt / 1.29 | `body` |
| Callout | 16pt | Regular (400) | 21pt / 1.31 | — |
| Subheadline | **15pt** | Regular (400) | 20pt / 1.33 | `label` |
| Footnote | **13pt** | Regular (400) | 18pt / 1.38 | `caption` |
| Caption 1 | 12pt | Regular (400) | 16pt / 1.33 | — |
| Caption 2 | **11pt** | Regular (400) | 13pt / 1.18 | `annotation` |

---

## Presentation Scale (adapted for slide format)

For 1920×1080 slides, dynamic type values are scaled proportionally:

| Token | Size | Weight | Notes |
|---|---|---|---|
| `heading-display` | 56pt | 700 | Hero title — SF Pro Display Bold |
| `heading` | 34pt | 700 | Section header — Large Title |
| `heading-sub` | 22pt | 600 | Card header — Title 2 / Semibold |
| `body` | 17pt | 400 | Content — Body default |
| `label` | 15pt | 500 | Subheadline / medium weight |
| `caption` | 13pt | 400 | Footnote / caption |
| `annotation` | 11pt | 400 | Caption 2 — smallest readable size |

---

## Typography Rules

### 1. Optical Size Switching
SF Pro Display is used for text **≥ 20pt**. For smaller text, switch to SF Pro Text for
better legibility at small sizes. The font automatically handles this via optical sizing.

### 2. Weight Usage
- **Bold (700)**: Titles, CTAs, emphasis
- **Semibold (600)**: Card headers, navigation titles
- **Medium (500)**: Labels, subheadlines, metadata
- **Regular (400)**: Body, captions, all running text

### 3. Tracking (letter-spacing)
SF Pro applies variable tracking automatically. Do not manually add letter-spacing
to Display text — it will break the optical balance Apple builds into the letterforms.

### 4. Color
| Role | Color | Use |
|---|---|---|
| Primary text | `#000000` (`on-surface`) | Body, headings, high emphasis |
| Secondary text | `#6D6D72` (`on-surface-variant`) | Labels, captions, metadata |
| Tint / link | `#007AFF` (`primary`) | Interactive text, key figures |

---

## Fallback Fonts

For environments without SF Pro installed:

```yaml
font-family: "SF Pro Display, -apple-system, Helvetica Neue, Arial, sans-serif"
```

PPTX / draw.io will substitute `Helvetica Neue` as the closest match on non-Apple systems.
