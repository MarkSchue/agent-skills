# Inheritance Model

This document describes the parallel Python class and CSS class inheritance
systems used by the presentation design skill.

---

## Python Class Hierarchy

### Card Renderers

```
BaseCardRenderer
├── TextCardRenderer
├── ImageCardRenderer
├── KpiCardRenderer
├── ChartCardRenderer
├── QuoteCardRenderer
├── AgendaCardRenderer
└── StackedTextCardRenderer
```

**BaseCardRenderer** provides:
- Card container rendering (background, border, radius, shadow)
- Title rendering (text, font, alignment, visibility)
- Header line rendering (color, width, alignment, visibility)
- **Footer area** — both independent components, active for every card type:
  - Footer line (`--card-footer-line-visible/color/width`) — renders whenever `true`, no text required
  - Footer text (`content.footer` in card YAML + `--card-footer-font-*` tokens)
- Body region geometry calculation (reserves space for footer before calling `render_body`)
- Token resolution through override chain

**Subclasses** override only:
- `render_body(ctx, x, y, w, h, content, props)` — type-specific content

### Layout Renderers

```
BaseLayoutRenderer
├── TitleSlideLayoutRenderer
└── GridLayoutRenderer
```

**BaseLayoutRenderer** provides:
- Canvas setup (dimensions, background)
- Slide chrome placement (title, subtitle, divider, logos, footer, page number)
- Card slot calculation
- Card dispatch to CardRenderers

**GridLayoutRenderer** handles all `grid-RxC` layouts through parameterized
rows/columns. No separate class per grid size.

---

## CSS Class Hierarchy

### Slide Level

```
.slide-base          ← all slide tokens (canvas, title, subtitle, divider,
                       logos, footer, page number)
```

No slide variant classes currently. Per-slide overrides are handled by
inline `<!-- slide ... -->` blocks in the Markdown.

### Card Level

```
.card-base              ← shared card tokens (background, border, title,
│                          header line, footer line, body)
├── .card--kpi          ← KPI-specific tokens (value size, trend colors)
├── .card--chart        ← chart-specific tokens (axis, grid, legend)
├── .card--quote        ← quote-specific tokens (mark, attribution)
├── .card--agenda       ← agenda-specific tokens (active/inactive, bullet)
└── .card--stacked-text ← stacked-text-specific tokens (heading, body, divider, gaps)
```

### Text Styles

```
.text-h1             ← Heading 1
.text-h2             ← Heading 2
.text-body           ← Body text
.text-caption        ← Caption text
.text-label          ← Label text
.text-quote          ← Quote text
.text-footnote       ← Footnote text
```

### Image Styles

```
.image-fullbleed     ← full-bleed (no border, flush)
.image-framed        ← framed (border, padding)
.image-circular      ← circular crop
```

---

## Token Resolution Chain

For every visual property, the renderer resolves the value through this chain:

```
1. Per-card YAML override    →  style_overrides.card-background
2. Per-slide YAML override   →  <!-- slide background: "#F0F4F8" -->
3. Card variant CSS class    →  .card--kpi { --card-kpi-value-font-size: 48 }
4. Base CSS class            →  .card-base { --card-background-color: #FFFFFF }
5. Python fallback           →  FALLBACK_TOKENS["card-background-color"] = "#FFFFFF"
```

The `ThemeLoader` merges all CSS layers. The `BaseCardRenderer.resolve_token()`
method checks per-card → per-slide → merged CSS → fallback in that order.

---

## Adding a New Card Type

1. Create `scripts/rendering/<name>_card.py` with a class extending `BaseCardRenderer`
2. Override `render_body()` with type-specific content rendering — the base handles title, header line, and **footer** automatically
3. Add variant CSS class `.card--<name>` in `themes/base.css` with type-specific tokens; include a commented-out `/* Footer overrides */` block (copy from another variant)
4. Register the card in `registry.yaml`
5. Create card spec at `cards/<category>/<name>-card.md`:
   - Include `content.footer` in the Optional Fields table
   - Include the "Footer tokens (shared with all card types)" sub-section in Supported Overrides
   - Show the footer zone in the `## Layout` pictogram
   - List `.card-base` footer in the `## Design Tokens Used` section
6. Add all new tokens to `references/token-reference.md`
