#!/usr/bin/env python3
"""
extract_theme.py — Future: extract design tokens from PPTX or website screenshots.

This is a placeholder stub for future implementation.

Usage:
    python scripts/cli/extract_theme.py <source> --output <theme.css>
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract design tokens from a PPTX file or website (future feature)."
    )
    parser.add_argument("source", help="Source file or URL to extract tokens from.")
    parser.add_argument("--output", "-o", type=Path, default=Path("theme.css"))
    args = parser.parse_args()

    print(
        f"extract_theme: Not yet implemented.\n"
        f"  Source: {args.source}\n"
        f"  Output: {args.output}\n"
        f"  This feature is planned for a future release.",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
