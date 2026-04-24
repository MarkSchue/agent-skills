"""
base_resolver.py — Resolve which base CSS file a presentation should use.

Convention
----------
The skill's ``themes/`` directory contains one or more ``<name>_base.css``
files. ``standard_base.css`` is the canonical, fully-populated token set
and is **always** loaded as the foundation. A presentation may opt into a
different *additional* base by placing a marker comment at the top of its
``theme.css``::

    /* @base: boston */

The resolver loads:

    1. ``themes/standard_base.css``   (always — completeness floor)
    2. ``themes/<name>_base.css``     (only if @base marker present and != standard)
    3. ``<project>/theme.css``        (project overrides — handled by caller)

This means an alternative base only needs to declare the tokens that
actually differ from standard.
"""

from __future__ import annotations

import re
from pathlib import Path

_BASE_MARKER_RE = re.compile(
    r"/\*\s*@base\s*:\s*([a-zA-Z0-9_-]+)\s*\*/", re.IGNORECASE
)
_BASE_FILE_SUFFIX = "_base.css"
DEFAULT_BASE = "standard"


def list_available_bases(themes_dir: Path) -> list[str]:
    """Return the list of available base names found in *themes_dir*.

    Each ``<name>_base.css`` becomes ``<name>``. Result is sorted with
    ``standard`` first if present.
    """
    if not themes_dir.is_dir():
        return []
    names = [
        p.stem.removesuffix("_base")
        for p in themes_dir.glob(f"*{_BASE_FILE_SUFFIX}")
    ]
    names = sorted(set(names))
    if DEFAULT_BASE in names:
        names.remove(DEFAULT_BASE)
        names.insert(0, DEFAULT_BASE)
    return names


def base_path_for(name: str, themes_dir: Path) -> Path:
    """Return the CSS path for base *name* (without checking existence)."""
    return themes_dir / f"{name}{_BASE_FILE_SUFFIX}"


def read_base_marker(theme_css_path: Path) -> str | None:
    """Return the base name declared by the ``/* @base: <name> */`` marker
    in *theme_css_path*, or ``None`` if no marker is present (or file
    missing).

    Only the first 30 lines are inspected — the marker is expected at the
    top of the file.
    """
    if not theme_css_path or not theme_css_path.exists():
        return None
    try:
        head = "\n".join(
            theme_css_path.read_text(encoding="utf-8").splitlines()[:30]
        )
    except OSError:
        return None
    m = _BASE_MARKER_RE.search(head)
    return m.group(1).lower() if m else None


def resolve_base_files(
    themes_dir: Path, theme_css_path: Path | None
) -> list[Path]:
    """Return the list of base CSS files to load **before** the project's
    own ``theme.css``.

    Order:
        1. ``themes/standard_base.css`` (always, if present)
        2. ``themes/<chosen>_base.css`` (only if marker selects a non-standard
           base that exists)

    Args:
        themes_dir:     The skill's ``themes/`` directory.
        theme_css_path: The project's ``theme.css`` (may be ``None`` or absent).

    Returns:
        Ordered list of existing CSS file paths.
    """
    files: list[Path] = []
    standard = base_path_for(DEFAULT_BASE, themes_dir)
    if standard.exists():
        files.append(standard)

    chosen = read_base_marker(theme_css_path) if theme_css_path else None
    if chosen and chosen != DEFAULT_BASE:
        alt = base_path_for(chosen, themes_dir)
        if alt.exists():
            files.append(alt)
        # If marker points at a missing base, silently fall back to standard
        # (caller may log).
    return files
