# Carbon Design Principles

**Source:** https://carbondesignsystem.com/ | IBM Design Language

---

## IBM Design Language Foundation

Carbon is the expression of **IBM Design Language** in digital products.
IBM's design language is governed by three core properties:

> **"Be essential. Be precise. Be human."**

These three words — not a corporate value statement, but design constraints —
drive every visual decision in Carbon, from the 8px grid to the choice of IBM Plex.

---

## 5 Core Design Principles

### 1. Token-First Thinking

No Hex values in design decisions. Every color, spacing, and type size is a
**semantic token** that carries intent, not a numeric value.

```
Wrong: bg = #f4f4f4, text = #161616
Right: bg = $layer-01, text = $text-primary
```

Tokens decouple design from implementation. When a theme changes, all tokens
update — no individual value hunts. This is how Carbon supports 4 themes with
a single component codebase.

**For presentations:** YAML design configs should only reference token names
(or the semantic aliases they are mapped to). Never hard-code hex values in
slide templates.

---

### 2. Theme Separation

Carbon's token layer cleanly separates **design intent** from **theme values**.

```
Component uses: $background, $text-primary, $border-subtle-01
Theme provides: (White) #ffffff, #161616, #c6c6c6
Theme provides: (Gray 100) #161616, #f4f4f4, #525252
```

Switching themes requires only a theme swap, not component changes.
Carbon supports: White, Gray 10, Gray 90, Gray 100 — all production-ready out-of-the-box.

---

### 3. Layering Model as Depth Language

Carbon does not use shadows to express depth (unlike MD3). Instead, **surface
layering using adjacent gray values** communicates hierarchy:

- Higher layers = lighter (light themes) or slightly lighter (dark themes)
- `$background` → `$layer-01` → `$layer-02` → `$layer-03`
- Each layer should be visually distinguishable but harmonious

This creates a **hierarchy without skeuomorphism** — no fake shadows, no blurs,
just systematic gray steps. The visual order is always clear because the
layering model is consistent and mathematical.

---

### 4. Productive Over Decorative

Carbon is built for work. Products that need to display and process data —
dashboards, configuration UIs, admin tools — cannot afford visual noise.

This shapes every decision:
- Motion is `productive` by default (fast, minimal, purposeful)
- Icons are flat, geometric (no gradients, fills as last resort)
- Type weights stop at SemiBold — no bold (700) allowed
- Color use is neutral-first — IBM Blue 60 is used **sparingly** as the action signal
- No decorative borders, no purely ornamental shapes

When something is expressive (hero, marketing), it is a **deliberate exception**
to the productive baseline — not the default mode.

---

### 5. Accessibility Is Non-Negotiable

Carbon targets **WCAG 2.1 AA minimum** across all components and themes, with
many components meeting AAA.

| Requirement | Carbon Standard |
|---|---|
| Body text contrast | ≥ 7:1 (`$text-primary`) |
| Large text / UI components | ≥ 4.5:1 |
| Focus ring | 2px `$focus` + 1px `$focus-inset` inset — always visible |
| Disabled states | Explicitly defined (not just grayed-out opacity) |
| Status colors | Always paired with text label — never color only |
| Reduced motion | All animations respect `prefers-reduced-motion` |

Accessibility is a **constraint, not a feature** — it shapes structure before
any visual design begins.

---

## Carbon vs. Other Systems

| | Carbon | Material Design 3 |
|---|---|---|
| **Owner** | IBM | Google |
| **Target** | Enterprise, data-rich products | Consumer apps, Android |
| **Tone** | Efficient, neutral, precise | Expressive, personal, adaptive |
| **Color model** | Token → theme (4 themes) | Dynamic color (tonal palette) |
| **Typography** | IBM Plex (sans/serif/mono) | Roboto / custom brand font |
| **Border radius** | 0 (default, sharp) | Continuous rounded scale |
| **Shadows** | Not used — layering model | Material elevation = shadow |
| **Motion** | Productive/Expressive + 6 durations | Expressive springs + legacy cubic |
| **Icons** | Flat SVG (4 sizes) | Variable font (Fill/Weight/Grade) |
| **Grid** | 8px mini unit, 2x Grid | 4dp baseline grid, adaptive layout |

---

## Key Design Conventions for Carbon Presentations

**Color:**
- Primary action = IBM Blue 60 (`#0f62fe` / `$interactive`)
- Use color sparingly — neutral content, colored emphasis
- Support colors (error/warning/success) must always be paired with text

**Type:**
- IBM Plex Sans is the **only** correct typeface for Carbon-style UI slides
- Use productive type set styles: heading-04/05/06 for titles, body-02 for content
- Never use more than 2 type sizes on a single slide

**Layout:**
- Obey the 8px mini unit — all dimensions must be multiples of 8 (or 4)
- Align to the 2x grid — 16-column structure for complex layouts
- Content area margins: 80px = 10 mini units

**Icons:**
- 24px or 32px for presentation-scale icons
- Color = `$icon-primary` on light, `$icon-inverse` on dark
- Always pair with text in slide context

---

## Anti-Patterns

| Wrong | Right |
|---|---|
| Using hex values directly | Use semantic token names |
| Shadows for depth | Use the layering model |
| Decorative rounded corners | Carbon corners are sharp or minimally rounded (4px max) |
| Bold text (700) | SemiBold (600) is the maximum weight |
| Color-only status indicators | Always pair status colors with text |
| Overusing Blue | Blue = one focal point per screen/slide |
| Mixing productive + expressive motion | Pick one style per component |
| Non-8px dimensions | Every layout value must be on the mini unit scale |
