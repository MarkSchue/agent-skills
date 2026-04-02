# Agent Skills Repository

This repository contains reusable skills for AI coding assistants following the
[skills.sh](https://skills.sh) format.

## How to use a skill

Read the individual `SKILL.md` inside the skill's directory. Each skill file
begins with YAML frontmatter (`name`, `description`, optional `metadata`) followed
by full instructions for the agent.

## Skills in this repository

- [`skills/presentation-design/SKILL.md`](skills/presentation-design/SKILL.md) —
  Presentation design system. Produces `.pptx` and `.drawio` output from a
  structured Markdown source file using an 8-step build pipeline driven by
  semantic CSS design tokens.

## When working on this repository

- Do **not** hardcode hex colour values anywhere in `scripts/rendering/`.
  All colours must be resolved from `ThemeTokens` via `theme.resolve("token-name")`.
- Colour tokens live exclusively in `.theme-colors` in `themes/base.css`;
  all other classes reference them via `var(--color-*)`.
- Do not rename existing tokens in `themes/base.css` — add new ones at the end
  of the relevant block instead.
- CLI entry points live in `scripts/cli/`; importable library code lives in
  `scripts/` sub-packages (`models/`, `parsing/`, `rendering/`, `exporting/`).
- **Keep exporters in sync:** `scripts/exporting/pptx_exporter.py` and
  `scripts/exporting/drawio_exporter.py` must always be kept in sync. Any new
  element type, coordinate formula, font-size unit conversion, or spacing
  calculation added to one exporter **must be immediately reflected in the other**.
  Both exporters share the same intermediate element dicts produced by the
  renderers; their visual output should match as closely as each target format
  allows.
