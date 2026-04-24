#!/usr/bin/env python3
"""
scaffold_presentation.py — Scaffold a new presentation project.

Usage:
    python scripts/cli/scaffold_presentation.py <name> [--path <dir>] [--force]

Creates:
    <name>/
    ├── presentation-definition.md
    ├── theme.css
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

SKILL_DIR = Path(__file__).resolve().parent.parent.parent
THEMES_DIR = SKILL_DIR / "themes"

# Allow running as a plain script (`python scripts/cli/scaffold_presentation.py`)
# without an active package install.
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

# Imported lazily so the file remains importable when the package layout
# changes during dev.
from scripts.parsing.base_resolver import (  # noqa: E402
    DEFAULT_BASE,
    base_path_for,
    list_available_bases,
)

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


def scaffold(name: str, base_path: Path, force: bool = False, base: str = DEFAULT_BASE) -> Path:
    """Create a new presentation project.

    Args:
        name:       Project folder name.
        base_path:  Parent directory for the project.
        force:      If True, overwrite existing files.
        base:       Name of the base CSS to start from (e.g. ``standard``,
                    ``boston``). The selection is recorded as a
                    ``/* @base: <name> */`` marker at the top of
                    ``theme.css`` so subsequent builds know which base
                    to fall back to.

    Returns:
        Path to the created project folder.
    """
    available = list_available_bases(THEMES_DIR)
    if base not in available:
        print(
            f"Error: unknown base '{base}'. Available: {', '.join(available) or '(none)'}",
            file=sys.stderr,
        )
        sys.exit(2)
    theme_template = base_path_for(base, THEMES_DIR)
    project = base_path / name
    if project.exists() and not force:
        print(f"Error: '{project}' already exists. Use --force to overwrite.", file=sys.stderr)
        sys.exit(1)

    # Create directories
    project.mkdir(parents=True, exist_ok=True)
    (project / "output").mkdir(exist_ok=True)
    (project / "output" / ".gitkeep").touch()
    (project / "input").mkdir(exist_ok=True)
    (project / "input" / ".gitkeep").touch()
    for sub in ("images", "charts", "diagrams", "logos"):
        (project / "assets" / sub).mkdir(parents=True, exist_ok=True)
        (project / "assets" / sub / ".gitkeep").touch()

    # Copy theme.css from the chosen base, prepended with a @base marker
    dest_theme = project / "theme.css"
    if not dest_theme.exists() or force:
        marker = f"/* @base: {base} */\n"
        if theme_template.exists():
            body = theme_template.read_text(encoding="utf-8")
            dest_theme.write_text(marker + body, encoding="utf-8")
        else:
            dest_theme.write_text(
                marker
                + f"/* Theme overrides \u2014 customize tokens from {base}_base.css here */\n",
                encoding="utf-8",
            )

    # Write starter presentation-definition.md
    dest_deck = project / "presentation-definition.md"
    if not dest_deck.exists() or force:
        dest_deck.write_text(STARTER_DECK, encoding="utf-8")

    print(f"✓ Scaffolded presentation project at: {project}")
    print(f"  - Edit: {dest_deck.name}")
    print(f"  - Theme: {dest_theme.name}")
    print(f"  - Build: python scripts/cli/build_presentation.py {project}")
    return project


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a new presentation project."
    )
    parser.add_argument("name", nargs="?", help="Name of the presentation project folder.")
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
    parser.add_argument(
        "--base",
        default=DEFAULT_BASE,
        help=(
            f"Base CSS to start from (default: {DEFAULT_BASE}). "
            "Use --list-bases to see available options."
        ),
    )
    parser.add_argument(
        "--list-bases",
        action="store_true",
        help="List available *_base.css files and exit.",
    )
    args = parser.parse_args()
    if args.list_bases:
        for n in list_available_bases(THEMES_DIR):
            print(n)
        return
    if not args.name:
        parser.error("name is required (unless --list-bases is given)")
    scaffold(args.name, args.path.resolve(), args.force, base=args.base)


if __name__ == "__main__":
    main()
