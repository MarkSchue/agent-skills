# Agent Skills

A collection of reusable skills for AI coding assistants. Skills are packaged
instructions and scripts that extend agent capabilities for specific workflows.

Skills follow the [skills.sh](https://skills.sh) format and are compatible with
GitHub Copilot, Claude Code, Cursor, Cline, and other agents.

## Available Skills

| Skill | Description |
|---|---|
| [`presentation-design`](skills/presentation-design/) | Presentation design system for building slide decks in `.pptx` and `.drawio` from a structured Markdown source file. Uses semantic CSS design tokens and an 8-step build pipeline. |

## Installation

```bash
# Install all skills
npx skills add MarkSchue/agent-skills

# Install a specific skill
npx skills add MarkSchue/agent-skills --skill presentation-design

# Install globally
npx skills add MarkSchue/agent-skills --skill presentation-design -g
```

## presentation-design

An 8-step build pipeline for producing `.pptx` and `.drawio` slide decks from a
structured Markdown source file. All visual values are resolved from a project
`theme.css` via semantic CSS design tokens — no hardcoded colours, fonts, or
spacing anywhere in the renderer library.

### Prerequisites

```bash
pip install -r skills/presentation-design/requirements.txt
```

### Quick start

```bash
# Scaffold a new project (creates presentation-definition.md + theme.css)
python skills/presentation-design/scripts/cli/scaffold_presentation.py MyDeck

# Build PPTX + draw.io
python skills/presentation-design/scripts/cli/build_presentation.py MyDeck/

# Build PPTX only
python skills/presentation-design/scripts/cli/build_presentation.py MyDeck/ --format pptx

# Build draw.io only
python skills/presentation-design/scripts/cli/build_presentation.py MyDeck/ --format drawio
```

### Theme customisation

All colours are defined once in the `.theme-colors` block of your `theme.css`.
Every other token references them via `var(--color-*)` — changing the palette
touches a single block and cascades everywhere.

```css
.theme-colors {
  --color-primary:   #1A1A2E;
  --color-secondary: #6B7280;
  --color-accent:    #3B82F6;
  /* ... see themes/base.css for the full token reference */
}
```

### Scripts reference

| Script | Purpose |
|---|---|
| `scripts/cli/scaffold_presentation.py <name>` | Create a new project folder with starter files |
| `scripts/cli/build_presentation.py <dir>` | Run the full 8-step build pipeline |
| `scripts/cli/extract_theme.py <source>` | Extract tokens from an existing file (planned) |
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
