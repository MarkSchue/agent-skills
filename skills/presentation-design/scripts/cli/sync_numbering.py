#!/usr/bin/env python3
"""
sync_numbering.py — CLI wrapper for the sync_numbering module.

Usage:
    python scripts/cli/sync_numbering.py <project_dir_or_md_file>

Resolves and renumbers all %%-based numbering placeholders in a
presentation-definition.md file.  Both bare placeholders and previously-
resolved numbers are replaced so the sequence is always gap-free.
"""

from __future__ import annotations

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SKILL_DIR))

from scripts.sync_numbering import _main  # noqa: E402 — path setup must come first

if __name__ == "__main__":
    _main()
