"""
numbering_normalizer.py — Dedicated class for resolving and renumbering
structured ID placeholders in a presentation-definition.md file.

Usage (programmatic)
--------------------

    from scripts.parsing.numbering_normalizer import NumberingNormalizer

    normalizer = NumberingNormalizer()
    result = normalizer.normalize(text)
    if result.changed:
        path.write_text(result.text, encoding="utf-8")
        for msg in result.log:
            print(msg)

Overview
--------
Placeholders
    Both ``%%`` and ``??`` are accepted as placeholder tokens.  ``??`` is a
    human-friendly variant that the user may type without consulting the docs.
    On the first run both are replaced by the correctly-computed sequence
    number; subsequent runs are fully idempotent.

Numbering config
    Pulled from the ``<!-- numbering … -->`` comment block at the top of the
    presentation-definition.md.  Example::

        <!-- numbering
        userstories:
          - "US-PH01-US%%"
          - "AC-PH01-US%%-AC%%"
        -->

    Each key is an arbitrary range name.  Each list item is a level pattern
    where ``%%`` (or ``??``) marks a counter slot.

Renumbering algorithm
    1. Normalize ``??`` → ``%%`` on lines that already match a pattern.
    2. Snapshot all currently-resolved IDs together with their label text.
    3. Run the sequential counter assignment (top-to-bottom, gap-free).
    4. Snapshot the new IDs + labels.
    5. Build a diff: ``{old_id: new_id}`` by matching labels across snapshots.
    6. Scan every non-definition line for occurrences of old IDs and replace.

Cross-reference detection
    A *definition line* is any line whose content contains a pattern match
    followed immediately by ``:``.  Every other line that contains an old ID
    is considered a cross-reference and is updated automatically.  All
    detected cross-references are reported in ``NormalizationResult.log``.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)

# ── Constants ────────────────────────────────────────────────────────────────

_PLACEHOLDER     = "%%"
_PLACEHOLDER_ALT = "??"          # human-typed alias, treated identically
_PAD             = 2             # zero-padding width  →  "01", "02", …
_NUMBERING_OPEN  = "<!-- numbering"
_NUMBERING_CLOSE = "-->"


# ── Internal data types ──────────────────────────────────────────────────────

class _LevelPattern(NamedTuple):
    raw_pattern: str            # e.g. "AC-PH01-US%%-AC%%"
    regex: re.Pattern           # matches both %%/??-placeholders and digits
    placeholder_count: int      # number of %% slots
    prefix_parts: list[str]     # segments split on %%


class _Range(NamedTuple):
    name: str
    levels: list[_LevelPattern]


@dataclass
class NormalizationResult:
    """Outcome of a single :meth:`NumberingNormalizer.normalize` call."""
    text: str                          # final (possibly rewritten) text
    changed: bool                      # True if any bytes differ from input
    replacements: int                  # total counter-slot substitutions
    cross_ref_updates: int             # cross-reference rewrite count
    log: list[str] = field(default_factory=list)   # human-readable change notes


# ── Helpers ──────────────────────────────────────────────────────────────────

def _compile_level_pattern(raw: str) -> _LevelPattern:
    """Build a _LevelPattern whose regex matches both placeholders and digits."""
    # Normalise: treat ?? identical to %%
    normalised = raw.replace(_PLACEHOLDER_ALT, _PLACEHOLDER)
    parts = normalised.split(_PLACEHOLDER)
    count = len(parts) - 1
    if count == 0:
        raise ValueError(
            f"Numbering pattern {raw!r} contains no placeholder (%% or ??)."
        )
    # Each placeholder slot becomes a capture group matching digits OR ?? OR %%
    regex_body = re.escape(parts[0])
    for part in parts[1:]:
        regex_body += r"(\d+|%%|\?\?)" + re.escape(part)
    return _LevelPattern(
        raw_pattern=normalised,
        regex=re.compile(regex_body),
        placeholder_count=count,
        prefix_parts=parts,
    )


def _build_replacement(lp: _LevelPattern, counters: list[int], level_idx: int) -> str:
    """Reconstruct the pattern string with current counter values."""
    parts = lp.prefix_parts
    result = parts[0]
    for slot_idx, sep in enumerate(parts[1:]):
        ctr_idx = min(slot_idx, level_idx)
        result += str(counters[ctr_idx]).zfill(_PAD)
        result += sep
    return result


def _is_inside_numbering_block(line: str, in_block: bool) -> tuple[bool, bool]:
    """Update *in_block* state; return (new_in_block, skip_this_line)."""
    stripped = line.strip()
    if not in_block:
        if stripped.startswith(_NUMBERING_OPEN):
            return True, True
        return False, False
    # Already inside
    if stripped == _NUMBERING_CLOSE or stripped.endswith(_NUMBERING_CLOSE):
        return False, True
    return True, True


# ── Core class ───────────────────────────────────────────────────────────────

class NumberingNormalizer:
    """Parse, renumber and cross-reference-patch a presentation-definition file.

    All state is local to each :meth:`normalize` call — instances are
    reusable and thread-safe (no mutable instance state).
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def normalize(self, text: str) -> NormalizationResult:
        """Resolve all numbering placeholders in *text*.

        Steps
        -----
        1. Extract the ``<!-- numbering -->`` config block.
        2. Normalize ``??`` → ``%%`` so the scanner finds them.
        3. Snapshot ID→label pairs before renumbering.
        4. Renumber sequentially (idempotent: re-running is a no-op when clean).
        5. Snapshot again and diff to find IDs that moved.
        6. Patch cross-references in non-definition lines.
        7. Return a :class:`NormalizationResult`.
        """
        block = self._extract_numbering_block(text)
        if block is None:
            return NormalizationResult(text=text, changed=False,
                                       replacements=0, cross_ref_updates=0,
                                       log=["No <!-- numbering --> block found."])

        try:
            ranges = self._build_ranges(block)
        except ValueError as exc:
            return NormalizationResult(text=text, changed=False,
                                       replacements=0, cross_ref_updates=0,
                                       log=[f"Numbering config error: {exc}"])

        if not ranges:
            return NormalizationResult(text=text, changed=False,
                                       replacements=0, cross_ref_updates=0,
                                       log=["Numbering block is empty."])

        log: list[str] = []

        # Step 2 — normalize ??, capture pre-state
        text_norm = self._normalize_placeholder_aliases(text, ranges)
        if text_norm != text:
            log.append(f"Normalized {text_norm.count(_PLACEHOLDER) - text.count(_PLACEHOLDER)} "
                       f"'??' placeholder(s) to '%%'.")

        # Step 3 — snapshot before (line_num → resolved_id)
        pre_snapshot = self._snapshot_line_ids(text_norm, ranges)

        # Step 4 — renumber
        text_renum, replacements = self._resolve_numbering(text_norm, ranges)
        if replacements:
            log.append(f"Renumbered {replacements} counter slot(s).")

        # Step 5 — snapshot after, build diff by line number
        post_snapshot = self._snapshot_line_ids(text_renum, ranges)
        id_mapping = self._build_id_mapping(pre_snapshot, post_snapshot)

        moved = {old: new for old, new in id_mapping.items() if old != new}
        if moved:
            for old_id, new_id in sorted(moved.items()):
                log.append(f"  Renumbered: {old_id} → {new_id}")

        # Step 6 — patch cross-references using the diff
        text_final, xref_count, xref_log = self._update_cross_references(
            text_renum, moved
        )
        if xref_count:
            log.append(f"Updated {xref_count} cross-reference(s):")
            log.extend(f"  {msg}" for msg in xref_log)

        changed = text_final != text
        return NormalizationResult(
            text=text_final,
            changed=changed,
            replacements=replacements,
            cross_ref_updates=xref_count,
            log=log,
        )

    # ------------------------------------------------------------------
    # Config extraction
    # ------------------------------------------------------------------

    def _extract_numbering_block(self, text: str) -> dict | None:
        """Return the parsed YAML dict from the ``<!-- numbering … -->`` block."""
        if yaml is None:
            raise RuntimeError(
                "PyYAML is required for numbering support. "
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
                    rest = stripped[len(_NUMBERING_OPEN):].strip()
                    if rest and not rest.startswith(_NUMBERING_CLOSE):
                        yaml_lines.append(rest)
                continue
            if stripped == _NUMBERING_CLOSE or stripped.endswith(_NUMBERING_CLOSE):
                break
            yaml_lines.append(line)
        if not yaml_lines:
            return None
        result = yaml.safe_load("\n".join(yaml_lines))
        if not isinstance(result, dict):
            raise ValueError(
                f"The <!-- numbering --> block must be a YAML mapping, "
                f"got {type(result).__name__}."
            )
        return result

    def _build_ranges(self, block: dict) -> list[_Range]:
        """Compile the numbering config into ``_Range`` objects."""
        ranges: list[_Range] = []
        for name, patterns in block.items():
            if not isinstance(patterns, list):
                raise ValueError(
                    f"Range '{name}' must be a list of pattern strings."
                )
            levels = [_compile_level_pattern(str(p)) for p in patterns]
            ranges.append(_Range(name=name, levels=levels))
        return ranges

    # ------------------------------------------------------------------
    # Placeholder alias normalisation
    # ------------------------------------------------------------------

    def _normalize_placeholder_aliases(self, text: str, ranges: list[_Range]) -> str:
        """Replace ``??`` with ``%%`` on lines that match a known pattern."""
        if _PLACEHOLDER_ALT not in text:
            return text

        lines = text.splitlines(keepends=True)
        result: list[str] = []
        in_block = False

        for line in lines:
            in_block, skip = _is_inside_numbering_block(line, in_block)
            if skip or _PLACEHOLDER_ALT not in line:
                result.append(line)
                continue

            new_line = line
            for rng in ranges:
                for lp in rng.levels:
                    # Build a variant of the regex that also matches ??
                    if lp.regex.search(new_line):
                        new_line = new_line.replace(_PLACEHOLDER_ALT, _PLACEHOLDER)
                        break
                if new_line != line:
                    break
            result.append(new_line)

        return "".join(result)

    # ------------------------------------------------------------------
    # Snapshot  (ID → label)
    # ------------------------------------------------------------------

    def _snapshot_line_ids(
        self, text: str, ranges: list[_Range]
    ) -> dict[int, str]:
        """Return ``{line_number: resolved_id}`` for every definition line.

        Uses the same most-specific-level-first rule as the renumberer so
        that ``US-PH01-US%%`` never matches inside an ``AC-PH01-US01-AC%%``
        line — only the most-specific level (AC) wins.
        """
        snapshot: dict[int, str] = {}
        lines = text.splitlines()
        in_block = False

        for lineno, line in enumerate(lines, start=1):
            in_block, skip = _is_inside_numbering_block(line, in_block)
            if skip:
                continue
            for rng in ranges:
                # Most-specific level first (highest index)
                for level_idx in range(len(rng.levels) - 1, -1, -1):
                    lp = rng.levels[level_idx]
                    m = lp.regex.search(line)
                    if m and all(
                        re.fullmatch(r"\d+", grp) for grp in m.groups()
                    ):
                        snapshot[lineno] = m.group(0)
                        break   # one level per line per range
        return snapshot

    # ------------------------------------------------------------------
    # Core renumbering
    # ------------------------------------------------------------------

    def _resolve_numbering(
        self, text: str, ranges: list[_Range]
    ) -> tuple[str, int]:
        """Scan top-to-bottom and replace every matching pattern sequentially.

        Returns ``(new_text, total_replacements)``.
        """
        lines = text.splitlines(keepends=True)
        counters: dict[str, list[int]] = {
            r.name: [0] * len(r.levels) for r in ranges
        }
        total = 0
        in_block = False
        result: list[str] = []

        for line in lines:
            in_block, skip = _is_inside_numbering_block(line, in_block)
            if skip:
                result.append(line)
                continue

            new_line = line
            for rng in ranges:
                ctrs = counters[rng.name]
                # Most-specific level first so "AC-%%-%%" wins over "AC-%%"
                for level_idx in range(len(rng.levels) - 1, -1, -1):
                    lp = rng.levels[level_idx]
                    if not lp.regex.search(new_line):
                        continue

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
                    total += count_box[0]
                    break   # only one level wins per line per range

            result.append(new_line)

        return "".join(result), total

    # ------------------------------------------------------------------
    # Cross-reference diff and patch
    # ------------------------------------------------------------------

    def _build_id_mapping(
        self,
        pre:  dict[int, str],   # {line_number: old_id}
        post: dict[int, str],   # {line_number: new_id}
    ) -> dict[str, str]:
        """Map each old_id to its new_id by matching on line number.

        Since renumbering never adds or removes lines, the same line number
        before and after renumbering corresponds to the same logical item.
        This avoids any fragility from duplicate or empty labels.
        """
        mapping: dict[str, str] = {}
        for lineno, old_id in pre.items():
            new_id = post.get(lineno)
            if new_id is not None:
                mapping[old_id] = new_id
        return mapping

    def _update_cross_references(
        self,
        text: str,
        moved: dict[str, str],          # {old_id: new_id} — only changed ones
    ) -> tuple[str, int, list[str]]:
        """Replace old IDs with new IDs on non-definition lines.

        Returns ``(patched_text, total_updates, log_messages)``.

        A *definition line* is identified by containing the old_id followed
        by ``:``.  Those lines are skipped (already renumbered in phase 4).
        """
        if not moved:
            return text, 0, []

        # Sort longest-first to avoid partial substitutions
        sorted_pairs = sorted(moved.items(), key=lambda kv: -len(kv[0]))

        lines = text.splitlines(keepends=True)
        result: list[str] = []
        xref_count = 0
        xref_log: list[str] = []
        in_block = False

        for lineno, line in enumerate(lines, start=1):
            in_block, skip = _is_inside_numbering_block(line, in_block)
            if skip:
                result.append(line)
                continue

            new_line = line
            for old_id, new_id in sorted_pairs:
                if old_id not in new_line:
                    continue
                # Skip definition lines (old_id immediately followed by ":")
                if re.search(re.escape(old_id) + r"\s*:", new_line):
                    continue
                # Replace all non-definition occurrences
                count_before = new_line.count(old_id)
                new_line = new_line.replace(old_id, new_id)
                replaced = count_before - new_line.count(old_id)
                if replaced > 0:
                    xref_count += replaced
                    xref_log.append(
                        f"Line {lineno}: {old_id} → {new_id} "
                        f"({replaced} occurrence(s))"
                    )

            result.append(new_line)

        return "".join(result), xref_count, xref_log


# ── Convenience function (for backward compat / sync_numbering wrapper) ──────

def normalize_file(path: Path) -> NormalizationResult:
    """Normalize *path* in-place.  Returns the result (no write if unchanged)."""
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    text = path.read_text(encoding="utf-8")
    result = NumberingNormalizer().normalize(text)
    if result.changed:
        path.write_text(result.text, encoding="utf-8")
    return result
