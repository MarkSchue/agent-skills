#!/usr/bin/env python3
"""Thin CLI wrapper — delegates to ``scripts.extract_theme``."""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent.parent
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from scripts.extract_theme import main  # noqa: E402

if __name__ == "__main__":
    main()
