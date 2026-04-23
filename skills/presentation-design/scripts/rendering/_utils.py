"""
_utils.py — Shared rendering utilities.

Lightweight pure functions used by more than one card renderer.
"""

from __future__ import annotations

# Approximate character width as a fraction of font-size (em-based estimate).
# Used to compute how many characters fit in a given pixel width.
CHAR_WIDTH_RATIO: float = 0.48


def _is_icon_ligature(text: str) -> bool:
    """Return ``True`` when *text* looks like a Material Design icon ligature.

    Material icon ligatures are lowercase alphabetic strings, optionally
    containing underscores (e.g. ``"home"``, ``"add_box"``, ``"arrow_forward"``).
    """
    return bool(text and text.replace("_", "").isalpha() and text == text.lower())
