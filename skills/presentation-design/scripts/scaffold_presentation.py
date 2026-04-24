#!/usr/bin/env python3
"""
scaffold_presentation.py — Scaffold a new presentation project.

Usage:
    python scripts/scaffold_presentation.py <name> [--path <dir>] [--force]

Creates:
    <name>/
    ├── presentation-definition.md
    ├── theme.css
    ├── input/
    ├── output/
    │   └── .gitkeep
    └── assets/
        ├── images/
        ├── charts/
        ├── diagrams/
        └── logos/
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
# Sparse theme template — overrides only. Avoids copying the full base.css
# (which would shadow every token and prevent base.css updates from cascading
# into the deck).
THEME_TEMPLATE = SKILL_DIR / "examples" / "minimal-theme.css"

STARTER_DECK = """\
# My Presentation

## Title Slide
<!-- slide
layout: title-slide
-->

# Introduction

## Welcome
### Overview
```yaml
type: text-card
content:
  body: "Welcome to this presentation. Edit this file to add your content."
  bullets:
    - "Use # for sections (agenda entries)"
    - "Use ## for slide titles"
    - "Use ### for card titles with YAML content blocks"
```

# Key Findings

## Metrics Dashboard
### Revenue
```yaml
type: kpi-card
content:
  value: "$0"
  trend: "neutral"
  label: "Total Revenue"
```

### Growth
```yaml
type: kpi-card
content:
  value: "0%"
  trend: "neutral"
  label: "Year over Year"
```

# Next Steps

## Action Items
### Tasks
```yaml
type: text-card
content:
  body: "Replace this content with your action items."
  bullets:
    - "Action item 1"
    - "Action item 2"
    - "Action item 3"
```
"""


def scaffold(name: str, base_path: Path, force: bool = False) -> Path:
    """Create a new presentation project.

    Args:
        name: Project folder name.
        base_path: Parent directory for the project.
        force: If True, overwrite existing files.

    Returns:
        Path to the created project folder.
    """
    project = base_path / name
    if project.exists() and not force:
        print(f"Error: '{project}' already exists. Use --force to overwrite.", file=sys.stderr)
        sys.exit(1)

    # Create directories
    project.mkdir(parents=True, exist_ok=True)
    (project / "input").mkdir(exist_ok=True)
    (project / "output").mkdir(exist_ok=True)
    (project / "output" / ".gitkeep").touch()
    for sub in ("images", "charts", "diagrams", "logos"):
        (project / "assets" / sub).mkdir(parents=True, exist_ok=True)
        (project / "assets" / sub / ".gitkeep").touch()

    # Copy theme.css from the skill template
    dest_theme = project / "theme.css"
    if not dest_theme.exists() or force:
        if THEME_TEMPLATE.exists():
            shutil.copy2(THEME_TEMPLATE, dest_theme)
        else:
            dest_theme.write_text(
                "/* Theme overrides — customize tokens from base.css here */\n",
                encoding="utf-8",
            )

    # Write starter presentation-definition.md
    dest_deck = project / "presentation-definition.md"
    if not dest_deck.exists() or force:
        dest_deck.write_text(STARTER_DECK, encoding="utf-8")

    print(f"✓ Scaffolded presentation project at: {project}")
    print(f"  - Edit:   {dest_deck.name}")
    print(f"  - Theme:  {dest_theme.name}")
    print(f"  - Input:  input/  ← place source files here")
    print(f"  - Build:  python scripts/build_presentation.py {project}")
    return project


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a new presentation project."
    )
    parser.add_argument("name", help="Name of the presentation project folder.")
    parser.add_argument(
        "--path",
        type=Path,
        default=Path.cwd(),
        help="Parent directory (default: current directory).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files.",
    )
    args = parser.parse_args()
    scaffold(args.name, args.path.resolve(), args.force)


if __name__ == "__main__":
    main()
