# Agent Skills

A collection of reusable skills for AI coding assistants. Skills are packaged
instructions and scripts that extend agent capabilities for specific workflows.

Skills follow the [skills.sh](https://skills.sh) format and are compatible with
GitHub Copilot, Claude Code, Cursor, Cline, and other agents.

## Available Skills

| Skill | Description |
|---|---|
| [`atomic-design-system`](skills/atomic-design-system/) | Headless presentation design system for building slide decks in draw.io and PowerPoint from a structured library of atoms, molecules, templates, and design tokens. |

## Installation

```bash
# Install all skills
npx skills add MarkSchue/agent-skills

# Install a specific skill
npx skills add MarkSchue/agent-skills --skill atomic-design-system

# Install globally
npx skills add MarkSchue/agent-skills --skill atomic-design-system -g
```

## atomic-design-system

A deterministic six-phase pipeline for producing `.pptx` and `.drawio` slide decks
from a structured Markdown source file. All visual values are resolved at build time
from a project `theme.css` via design tokens — no hardcoded colors, fonts, or spacing
anywhere in the component library.

### Prerequisites

```bash
pip install python-pptx pillow beautifulsoup4 cssutils requests pyyaml
```

### Quick start

```bash
# Initialise a new project (creates deck.md + theme.css scaffold)
python skills/atomic-design-system/scripts/scaffold_project.py MyDeck/

# Build PPTX
python skills/atomic-design-system/scripts/pptx_builder.py MyDeck/deck.md \
  --output MyDeck/output/deck.pptx

# Build draw.io
python skills/atomic-design-system/scripts/drawio_builder.py MyDeck/deck.md \
  --output MyDeck/output/deck.drawio

# Visual QA — renders every slide to a JPEG for review
python skills/atomic-design-system/scripts/qa_render.py MyDeck/output/deck.pptx \
  --output-dir MyDeck/output/qa/ --dpi 150
```

### Design themes

Three built-in design systems ship with the skill:

| Theme | Path |
|---|---|
| Material Design 3 | `designthemes/materialdesign3/theme.css` |
| IBM Carbon | `designthemes/carbon/theme.css` |
| Liquid Glass | `designthemes/liquidglass/theme.css` |

Copy a `theme.css` next to your `deck.md` to activate it. Override only
`--color-*` and `--font-family` tokens — structural tokens (radius, spacing,
elevation) are owned by the design system.

### Scripts reference

| Script | Purpose |
|---|---|
| `pptx_builder.py <md>` | Build PowerPoint output |
| `drawio_builder.py <md>` | Build draw.io output |
| `qa_render.py <pptx>` | Convert PPTX → per-slide JPEG for visual QA |
| `scaffold_project.py <dir>` | Initialise a new project directory |
| `visual_extractor.py <source>` | Extract design tokens from image / PPTX / URL |
| `lint.py` | Lint component files for hardcoded values |
| `preview_generator.py` | Regenerate preview PNGs for the registry |

## Contributing

1. Fork this repository
2. Add a new skill directory under `skills/<skill-name>/` with at minimum a `SKILL.md`
3. Open a pull request

## License

MIT
