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
