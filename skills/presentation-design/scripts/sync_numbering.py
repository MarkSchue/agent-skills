"""
sync_numbering.py — Thin CLI / build-pipeline wrapper around
:class:`scripts.parsing.numbering_normalizer.NumberingNormalizer`.

All numbering logic lives in that dedicated class.  This module exposes:

* ``sync(deck_path)`` — called by ``build_presentation.py`` before parsing.
* ``_main()``         — standalone CLI entry point.

Placeholder support
-------------------
Both ``%%`` and ``??`` are accepted as placeholder tokens.  The normalizer
converts ``??`` to ``%%`` transparently on every run.

Cross-reference patching
------------------------
After renumbering, any non-definition line that still references a moved ID
is automatically updated and reported in the build log.
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

# Ensure the skill root (parent of scripts/) is on sys.path so that
# "scripts.parsing.numbering_normalizer" resolves when run directly.
_SKILL_DIR = Path(__file__).resolve().parent.parent
if str(_SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(_SKILL_DIR))

from scripts.parsing.numbering_normalizer import NumberingNormalizer, normalize_file

logger = logging.getLogger("sync_numbering")


# ── Public API (backward-compatible) ────────────────────────────────────────

def sync(deck_path: Path) -> bool:
    """Resolve and renumber placeholders in *deck_path*, write back if changed.

    Returns ``True`` if the file was modified, ``False`` if already up-to-date.
    Raises ``FileNotFoundError`` if *deck_path* does not exist.
    """
    result = normalize_file(deck_path)
    for msg in result.log:
        if result.changed:
            logger.info("%s", msg)
        else:
            logger.debug("%s", msg)
    return result.changed


# ── Standalone CLI ───────────────────────────────────────────────────────────

def _main() -> None:
    import argparse

    ap = argparse.ArgumentParser(
        description=(
            "Resolve and renumber placeholders (%% / ??) in a "
            "presentation-definition.md file."
        )
    )
    ap.add_argument(
        "path",
        type=Path,
        help="Path to a presentation project folder or a definition .md file.",
    )
    ap.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging.",
    )
    args = ap.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
    )

    target: Path = args.path
    if target.is_dir():
        deck_path = target / "presentation-definition.md"
        if not deck_path.exists():
            deck_path = target / "deck.md"
    else:
        deck_path = target

    if not deck_path.exists():
        logger.error("File not found: %s", deck_path)
        sys.exit(1)

    changed = sync(deck_path)
    if changed:
        print(f"✓ Numbering updated in {deck_path}")
    else:
        print(f"  Numbering already up-to-date in {deck_path}")


if __name__ == "__main__":
    _main()
