# Agent Skills Repository

This repository contains reusable skills for AI coding assistants following the
[skills.sh](https://skills.sh) format.

## How to use a skill

Read the individual `SKILL.md` inside the skill's directory. Each skill file
begins with YAML frontmatter (`name`, `description`, optional `metadata`) followed
by full instructions for the agent.

## Skills in this repository

- [`skills/atomic-design-system/SKILL.md`](skills/atomic-design-system/SKILL.md) —
  Headless slide deck design system. Produces `.pptx` and `.drawio` output from
  a structured Markdown source file using a six-phase assembly pipeline.

## When working on this repository

- Do **not** add hardcoded color, spacing, or font values to any component file
  inside `skills/atomic-design-system/scripts/`. All visual values must be read
  from the `RenderContext` API (`ctx.*`).
- The `scripts/lint.py` tool validates this constraint — run it before committing.
- Component Python files live in `scripts/rendering/`; layout logic lives in
  `scripts/rendering/templates/`.

## Molecule & Atom Python Authoring

When writing a new molecule renderer (`scripts/rendering/<name>.py`), follow
these rules so every card is per-instance customisable from `deck.md` without
touching the theme:

1. **Always pass `props` to every geometry helper.**
   ```python
   pad        = ctx.card_pad_px(w, h, props)
   header_h   = ctx.card_header_h(w, h, props)
   header_gap = ctx.card_header_gap(h, props)
   title_size = ctx.card_header_font_size(title, text_w, h, props)
   icon_sz    = ctx.icon_size(w, h, props)
   icon_r     = ctx.icon_radius(icon_sz, props)
   hdr_color  = ctx.card_line_color("header", ctx.color("line-default"), props)
   ftr_color  = ctx.card_line_color("footer", ctx.color("line-default"), props)
   ```
   `props` is the raw dict parsed from the molecule's YAML block in `deck.md`.
   Passing it is a no-op when no overrides are set — so the call is always safe.

2. **Priority chain (enforced by helpers):** per-card prop → CSS theme token → computed default.
   Never short-circuit this chain by reading `props` directly in the renderer body.
   Use `ctx._prop_value(props, "key-name", "key_name")` only when adding a *new*
   helper that does not yet exist in `context.py`.

3. **Do not inline geometry formulas.** If a molecule needs padding, header height,
   or icon size, use the centralised helpers above — never compute them inline.
   This ensures CSS tokens and per-card overrides both work transparently.

4. **Document every new overridable key** in `references/token-reference.md` under
   a "Card Instance Override Keys" section, and in the `context.py` module docstring.
