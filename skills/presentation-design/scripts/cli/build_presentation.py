#!/usr/bin/env python3
"""
build_presentation.py — Thin CLI wrapper.

Delegates to ``scripts.build_presentation`` so all 15 card types, numbering
sync, and pipeline improvements are always in effect from a single source of
truth.

Usage:
    python scripts/cli/build_presentation.py <project_dir> [--format pptx|drawio|both]
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure the skill root (parent of scripts/) is on sys.path
SKILL_DIR = Path(__file__).resolve().parent.parent.parent
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from scripts.build_presentation import main  # noqa: E402

if __name__ == "__main__":
    main()
