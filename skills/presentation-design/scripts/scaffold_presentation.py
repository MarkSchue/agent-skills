#!/usr/bin/env python3
"""
scaffold_presentation.py — Scaffold a new presentation project.

Usage:
    python scripts/scaffold_presentation.py <name> [--path <dir>] [--force] [--base <name>]
    python scripts/scaffold_presentation.py --list-bases

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
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
THEMES_DIR = SKILL_DIR / "themes"

if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

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

ASSET_SUBDIRS = ("images", "charts", "diagrams", "logos")


def _make_dirs(project: Path) -> None:
    project.mkdir(parents=True, exist_ok=True)
    for sub in ("input", "output"):
        (project / sub).mkdir(exist_ok=True)
        (project / sub / ".gitkeep").touch()
    for sub in ASSET_SUBDIRS:
        (project / "assets" / sub).mkdir(parents=True, exist_ok=True)
        (project / "assets" / sub / ".gitkeep").touch()


def _write_theme(dest: Path, base: str, force: bool) -> None:
    if dest.exists() and not force:
        return
    template = base_path_for(base, THEMES_DIR)
    marker = f"/* @base: {base} */\n"
    body = template.read_text(encoding="utf-8") if template.exists() else (
        f"/* Theme overrides — customize tokens from {base}_base.css here */\n"
    )
    dest.write_text(marker + body, encoding="utf-8")


def scaffold(name: str, base_path: Path, force: bool = False, base: str = DEFAULT_BASE) -> Path:
    """Create a new presentation project."""
    available = list_available_bases(THEMES_DIR)
    if base not in available:
        print(
            f"Error: unknown base '{base}'. Available: {', '.join(available) or '(none)'}",
            file=sys.stderr,
        )
        sys.exit(2)

    project = base_path / name
    if project.exists() and not force:
        print(f"Error: '{project}' already exists. Use --force to overwrite.", file=sys.stderr)
        sys.exit(1)

    _make_dirs(project)
    _write_theme(project / "theme.css", base, force)

    dest_deck = project / "presentation-definition.md"
    if not dest_deck.exists() or force:
        dest_deck.write_text(STARTER_DECK, encoding="utf-8")

    print(f"✓ Scaffolded presentation project at: {project}")
    print(f"  - Edit: {dest_deck.name}")
    print(f"  - Theme: theme.css (base: {base})")
    print(f"  - Build: python scripts/build_presentation.py {project}")
    return project


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a new presentation project.")
    parser.add_argument("name", nargs="?", help="Name of the presentation project folder.")
    parser.add_argument("--path", type=Path, default=Path.cwd(),
                        help="Parent directory (default: current directory).")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    parser.add_argument("--base", default=DEFAULT_BASE,
                        help=f"Base CSS to start from (default: {DEFAULT_BASE}).")
    parser.add_argument("--list-bases", action="store_true",
                        help="List available *_base.css files and exit.")
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
