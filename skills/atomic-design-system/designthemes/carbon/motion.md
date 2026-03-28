# Carbon Motion

**Source:** https://carbondesignsystem.com/elements/motion/overview/

---

## Two Motion Styles

Carbon defines two motion styles that reflect intent:

| Style | Character | When to Use |
|---|---|---|
| **Productive** | Fast, subtle, efficient | Utility interactions: state changes, data updates, status toggling |
| **Expressive** | Vibrant, dramatic, memorable | Significant moments: hero reveals, feature announcements, key calls-to-action |

Both styles use the same duration tokens — the difference lies in the **easing curve**.

---

## Easing Curves

Three easing types × two styles = 6 cubic-bezier curves.

### Standard Easing
Element remains visible throughout the animation (contained transition).

| Style | Curve | Use |
|---|---|---|
| Productive | `cubic-bezier(0.2, 0, 0.38, 0.9)` | Most UI transitions |
| Expressive | `cubic-bezier(0.4, 0.14, 0.3, 1)` | Featured card reveals |

### Entrance Easing
Element enters from off-screen or opacity 0. Decelerates to a stop.

| Style | Curve | Use |
|---|---|---|
| Productive | `cubic-bezier(0, 0, 0.38, 0.9)` | Dropdown menus, tooltips |
| Expressive | `cubic-bezier(0, 0, 0.3, 1)` | Hero panels sliding in |

### Exit Easing
Element leaves the screen or view. Accelerates out.

| Style | Curve | Use |
|---|---|---|
| Productive | `cubic-bezier(0.2, 0, 1, 0.9)` | Closing panels, dismissing |
| Expressive | `cubic-bezier(0.4, 0.14, 1, 1)` | Page-level dismissals |

---

## Duration Tokens

| Token | Duration | Use |
|---|---|---|
| `$duration-fast-01` | **70ms** | Micro-interactions: button press, toggle switch |
| `$duration-fast-02` | **110ms** | Micro-interactions: fade in/out, icon swap |
| `$duration-moderate-01` | **150ms** | Small expansion, short distance movement |
| `$duration-moderate-02` | **240ms** | Expansion, system communication, toast |
| `$duration-slow-01` | **400ms** | Large panel expansion, important notifications |
| `$duration-slow-02` | **700ms** | Background dimming, overlay fade |

---

## Duration Selection Rules

**Rule 1 — Size:** Larger elements move slower. Relationship:

$$\text{Duration} \propto \sqrt{\text{Distance or Scale}}$$

| Size | Productive | Expressive |
|---|---|---|
| Micro (button, icon) | 70–110ms | 110–150ms |
| Small (tooltip, dropdown) | 110–150ms | 150–240ms |
| Medium (modal, panel) | 240–400ms | 400–600ms |
| Large (page zone) | 400ms | 400–700ms |

**Rule 2 — Entrance vs Exit:** Exit should be **shorter** than Entrance.
If entrance = 400ms, exit ≤ 240ms. Users have seen the element — they don't
need a slow farewell.

**Rule 3 — No instantaneous state changes:** Even 70ms respects the user's
visual system. Never set `transition: none` for interactive components.

---

## Productive vs Expressive: Decision Guide

Ask these questions to choose a style:

```
Is this a utilitarian task (form submit, toggle, filter)?
  → Productive
  
Is this a significant moment (hero, feature highlight, onboarding step)?
  → Expressive
  
Is the user trying to complete a workflow right now?
  → Productive — stay out of their way
  
Is this a first impression or brand moment?
  → Expressive — make it memorable
```

---

## Motion Principles

1. **Purposeful** — Motion communicates function, not decoration. If removing
   the animation changes meaning, it should be there. If not — remove it.

2. **Productive first** — Most enterprise product interactions are productive.
   Expressive use is intentional and rare (< 10% of animations in a product UI).

3. **Consistent patterns** — Use the same easing curve for the same type of
   action everywhere. Never mix productive and expressive easing on the same
   component.

4. **Duration hierarchy** — Small things move faster. Large things move slower.
   Violating this breaks the user's natural physics model.

5. **Reduce motion accessible fallback** — When `prefers-reduced-motion` is
   active, use opacity-only transitions at `$duration-fast-01` (70ms) maximum
   or skip animation entirely.

---

## CSS Implementation Reference

```css
/* Productive standard */
.transition-productive {
  transition-timing-function: cubic-bezier(0.2, 0, 0.38, 0.9);
  transition-duration: 150ms; /* moderate-01 */
}

/* Expressive entrance */
.transition-expressive-entrance {
  transition-timing-function: cubic-bezier(0, 0, 0.3, 1);
  transition-duration: 400ms; /* slow-01 */
}

/* Exit is always faster than entrance */
.transition-exit {
  transition-timing-function: cubic-bezier(0.2, 0, 1, 0.9);
  transition-duration: 110ms; /* fast-02 */
}
```

---

## Slide Transition Patterns

| Pattern | Style | Easing | Duration |
|---|---|---|---|
| Title slide entrance | Expressive | `entrance-expressive` | 400ms |
| Section fade in | Productive | `entrance-productive` | 240ms |
| Content block reveal | Productive | `standard-productive` | 150ms |
| Callout highlight | Expressive | `standard-expressive` | 240ms |
| Slide-out exit | Productive | `exit-productive` | 110ms |
| Hero transition | Expressive | `entrance-expressive` | 700ms |
