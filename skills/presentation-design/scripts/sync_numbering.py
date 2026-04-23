"""
sync_numbering.py — Resolve and renumber %%-based numbering placeholders in
a presentation-definition.md file.

Runs BEFORE deck parsing on every build.  Both unresolved placeholders (``%%``)
and previously-resolved numbers are matched and renumbered from scratch so
that insertions, deletions, and reorderings always produce a consistent,
gap-free sequence.

## Numbering block syntax (top of presentation-definition.md)

    <!-- numbering
    userstories:
      - "US-PH01-%%"
      - "US-PH01-%%-AC%%"
    bugs:
      - "BUG-%%"
      - "BUG-%%-STEP%%"
    -->

Rules
-----
* Each key is a **range name** (arbitrary string, used only for logging).
* Each list item is a **level pattern** (index 0 = top level, 1 = first
  sub-level, …).
* ``%%`` is the counter placeholder.  In multi-``%%`` patterns the slots are
  filled left-to-right with ``counters[0], counters[1], …, counters[N]``.
* Numbers are zero-padded to 2 digits (``01``, ``02``, …).

## Match strategy

For each level pattern a regex is compiled where every ``%%`` becomes the
group ``(\\d+|%%)`` so that BOTH bare placeholders and previously-resolved
numbers are matched and replaced.

## Counter logic (top-to-bottom scan)

* Level-0 hit  → increment ``counters[0]``, reset ``counters[1+]`` to 0.
* Level-N hit  → increment ``counters[N]`` only;
                 ``counters[0..N-1]`` carry the current parent context.
* At most one level matches per line per range (the lowest-index that matches).

## Important exclusion

Lines inside the ``<!-- numbering … -->`` block itself are never modified.
"""
from __future__ import annotations

import logging
import re
import sys
from pathlib import Path
from typing import NamedTuple

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]

logger = logging.getLogger("sync_numbering")

# ── Constants ────────────────────────────────────────────────────────────────

_PLACEHOLDER = "%%"
_PAD = 2          # zero-padding width; e.g. 2 → "01"
_NUMBERING_OPEN  = "<!-- numbering"
_NUMBERING_CLOSE = "-->"


# ── Data structures ──────────────────────────────────────────────────────────

class _LevelPattern(NamedTuple):
    """A single level within a number range."""
    raw_pattern: str          # e.g. "US-PH01-%%-AC%%"
    regex: re.Pattern         # compiled: %% → (\d+|%%)
    placeholder_count: int    # number of %% slots in raw_pattern
    prefix_parts: list[str]   # split on %% → N+1 literal segments


class _Range(NamedTuple):
    name: str
    levels: list[_LevelPattern]


# ── Regex helpers ────────────────────────────────────────────────────────────

def _compile_level_pattern(raw: str) -> _LevelPattern:
    """Build a regex that matches both ``%%`` and resolved digit sequences."""
    parts = raw.split(_PLACEHOLDER)
    placeholder_count = len(parts) - 1
    if placeholder_count == 0:
        raise ValueError(
            f"Numbering pattern {raw!r} contains no '%%' placeholder."
        )
    # Build regex: escape literal parts, join with the wildcard group
    regex_body = re.escape(parts[0])
    for part in parts[1:]:
        regex_body += r"(\d+|%%)" + re.escape(part)
    return _LevelPattern(
        raw_pattern=raw,
        regex=re.compile(regex_body),
        placeholder_count=placeholder_count,
        prefix_parts=parts,
    )


# ── Block extraction ─────────────────────────────────────────────────────────

def extract_numbering_block(text: str) -> dict | None:
    """Return the parsed YAML dict from the ``<!-- numbering … -->`` block.

    Returns ``None`` if no such block is present or the block is empty.
    Raises ``ValueError`` on YAML parse errors.
    """
    if yaml is None:
        raise RuntimeError(
            "PyYAML is not installed — cannot parse the numbering block. "
            "Run: pip install pyyaml"
        )

    lines = text.splitlines()
    in_block = False
    yaml_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not in_block:
            if stripped.startswith(_NUMBERING_OPEN):
                in_block = True
                # Allow "<!-- numbering" on its own line or with trailing yaml
                rest = stripped[len(_NUMBERING_OPEN):].strip()
                if rest and not rest.startswith(_NUMBERING_CLOSE):
                    yaml_lines.append(rest)
            continue
        # Inside the block
        if stripped == _NUMBERING_CLOSE or stripped.endswith(_NUMBERING_CLOSE):
            break
        yaml_lines.append(line)

    if not yaml_lines:
        return None

    raw_yaml = "\n".join(yaml_lines)
    result = yaml.safe_load(raw_yaml)
    if not isinstance(result, dict):
        raise ValueError(
            f"The <!-- numbering --> block must contain a YAML mapping, "
            f"got {type(result).__name__}."
        )
    return result


def _build_ranges(block: dict) -> list[_Range]:
    """Validate and compile the numbering config into ``_Range`` objects."""
    ranges: list[_Range] = []
    for range_name, level_patterns in block.items():
        if not isinstance(level_patterns, list):
            raise ValueError(
                f"Numbering range '{range_name}' must be a list of patterns, "
                f"got {type(level_patterns).__name__}."
            )
        levels: list[_LevelPattern] = []
        for raw in level_patterns:
            if not isinstance(raw, str):
                raise ValueError(
                    f"Pattern in range '{range_name}' must be a string, got {raw!r}."
                )
            levels.append(_compile_level_pattern(raw))
        ranges.append(_Range(name=range_name, levels=levels))
    return ranges


# ── Core resolver ────────────────────────────────────────────────────────────

def resolve_numbering(text: str, ranges: list[_Range]) -> tuple[str, int]:
    """Scan *text* top-to-bottom and replace every matching pattern.

    Returns
    -------
    (new_text, total_replacements)
        ``new_text`` has all matching occurrences replaced with sequential
        numbers.  ``total_replacements`` is the count of substitutions made.
    """
    lines = text.splitlines(keepends=True)

    # Per-range counter array, all start at 0
    counters: dict[str, list[int]] = {
        r.name: [0] * len(r.levels) for r in ranges
    }

    total_replacements = 0
    in_numbering_block = False
    result_lines: list[str] = []

    for line in lines:
        stripped = line.strip()

        # Track whether we are inside the <!-- numbering … --> block itself
        if not in_numbering_block:
            if stripped.startswith(_NUMBERING_OPEN):
                in_numbering_block = True
                result_lines.append(line)
                continue
        else:
            result_lines.append(line)
            if stripped == _NUMBERING_CLOSE or stripped.endswith(_NUMBERING_CLOSE):
                in_numbering_block = False
            continue

        # Process content lines
        new_line = line
        for rng in ranges:
            ctrs = counters[rng.name]
            # Check from most specific (highest index) to least specific (level 0)
            # so "REQ-%%-AC%%" wins over the shorter "REQ-%%" on the same line.
            for level_idx in range(len(rng.levels) - 1, -1, -1):
                lp = rng.levels[level_idx]
                if not lp.regex.search(new_line):
                    continue

                # Replace ALL occurrences of this level pattern on the line,
                # incrementing the counter for each hit.
                count_box = [0]

                def _replacer(
                    m,
                    _ctrs=ctrs,
                    _li=level_idx,
                    _lp=lp,
                    _cb=count_box,
                ):
                    if _li == 0:
                        _ctrs[0] += 1
                        for k in range(1, len(_ctrs)):
                            _ctrs[k] = 0
                    else:
                        _ctrs[_li] += 1
                    _cb[0] += 1
                    return _build_replacement(_lp, _ctrs, _li)

                new_line = lp.regex.sub(_replacer, new_line)
                total_replacements += count_box[0]
                break  # only one level wins per line per range

        result_lines.append(new_line)

    return "".join(result_lines), total_replacements


def _build_replacement(
    lp: _LevelPattern, counters: list[int], level_idx: int
) -> str:
    """Reconstruct the pattern string with counters substituted for ``%%``."""
    parts = lp.prefix_parts
    # Number of %% slots = len(parts) - 1
    # Slots 0..level_idx-1 carry parent counters; slot level_idx is the leaf.
    # Any extra slots beyond level_idx (shouldn't happen in a well-formed
    # config) fall back to the leaf counter.
    result = parts[0]
    for slot_idx, sep in enumerate(parts[1:]):
        ctr_idx = min(slot_idx, level_idx)
        result += str(counters[ctr_idx]).zfill(_PAD)
        result += sep
    return result


# ── Public API ───────────────────────────────────────────────────────────────

def sync(deck_path: Path) -> bool:
    """Read *deck_path*, resolve all numbering placeholders, write back.

    Returns ``True`` if the file was modified, ``False`` if nothing changed
    (i.e. all numbers were already correct — re-entrant / idempotent when
    content has not changed).

    Raises ``FileNotFoundError`` if *deck_path* does not exist.
    Raises ``ValueError`` on malformed numbering block or patterns.
    """
    if not deck_path.exists():
        raise FileNotFoundError(f"Deck not found: {deck_path}")

    text = deck_path.read_text(encoding="utf-8")

    block = extract_numbering_block(text)
    if block is None:
        logger.debug("No <!-- numbering --> block found in %s — skipping.", deck_path.name)
        return False

    ranges = _build_ranges(block)
    if not ranges:
        logger.debug("Numbering block in %s is empty — skipping.", deck_path.name)
        return False

    new_text, count = resolve_numbering(text, ranges)

    if new_text == text:
        logger.debug("Numbering in %s already up-to-date (%d ranges scanned).", deck_path.name, len(ranges))
        return False

    deck_path.write_text(new_text, encoding="utf-8")
    logger.info(
        "Numbering sync: %d replacement(s) across %d range(s) in %s.",
        count, len(ranges), deck_path.name,
    )
    return True


# ── Standalone CLI ───────────────────────────────────────────────────────────

def _main() -> None:
    import argparse

    ap = argparse.ArgumentParser(
        description=(
            "Resolve and renumber %%-based numbering placeholders in a "
            "presentation-definition.md file."
        )
    )
    ap.add_argument(
        "path",
        type=Path,
        help=(
            "Path to a presentation project folder OR directly to a "
            "presentation-definition.md file."
        ),
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
