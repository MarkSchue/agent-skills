#!/usr/bin/env python3
"""sync_agenda.py — Sync the <!-- agenda --> block with # section headings.

Reads the current ``#`` section headings from a ``presentation-definition.md``
and updates the ``<!-- agenda ... -->`` comment block to match them.

Important: the agenda renderer matches sections to ``#`` headings **by position
(index)**, not by title.  The ``title`` field in the block is cosmetic only
(it is overridden at render time by the actual heading).  Only ``number`` and
``info`` are functionally significant.

Behaviour:
- ``title`` in every agenda entry is updated to match the ``#`` heading at the
  same position (keeps the block readable and self-documenting).
- ``number`` and ``info`` are preserved **by position** for sections that still
  exist at the same index.
- New sections appended at the end get auto-assigned sequential numbers and an
  empty ``info``.
- Sections removed from the file are dropped (last-in, first-out).
- All sections are renumbered sequentially (00, 01, 02 …) based on their
  final order so there are never gaps.
- Icon settings in the agenda block are always preserved.

Usage:
    python scripts/sync_agenda.py <presentation-definition.md>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

# ── Regex patterns ──────────────────────────────────────────────────────────

_RE_AGENDA_START = re.compile(r"^<!--\s*agenda\s*$")
_RE_AGENDA_END = re.compile(r"^-->\s*$")
_RE_H1 = re.compile(r"^#\s+(.+)$")

# ── Helpers ─────────────────────────────────────────────────────────────────


def _find_agenda_block(lines: list[str]) -> tuple[int, int]:
    """Return *(start_idx, end_idx)* of the ``<!-- agenda ... -->`` block.

    Both indices are inclusive line numbers inside *lines*.
    Returns ``(-1, -1)`` when absent.
    """
    for i, line in enumerate(lines):
        if _RE_AGENDA_START.match(line):
            j = i + 1
            while j < len(lines) and not _RE_AGENDA_END.match(lines[j]):
                j += 1
            return i, j
    return -1, -1


def _parse_agenda_config(lines: list[str], start: int, end: int) -> dict:
    """Parse the YAML inside the agenda block (lines[start+1 .. end-1])."""
    yaml_text = "\n".join(lines[start + 1 : end])
    try:
        data = yaml.safe_load(yaml_text)
        if isinstance(data, dict):
            return data
    except yaml.YAMLError:
        pass
    return {}


def _extract_section_titles(lines: list[str], agenda_start: int, agenda_end: int) -> list[str]:
    """Return ``# Heading`` titles from *lines*, skipping the agenda block.

    The very first ``#`` heading in the file is the deck/presentation title and
    is intentionally excluded — it is not an agenda section.
    """
    titles: list[str] = []
    first_seen = False
    for i, line in enumerate(lines):
        if agenda_start <= i <= agenda_end:
            continue
        m = _RE_H1.match(line)
        if m:
            if not first_seen:
                first_seen = True  # skip the deck title
                continue
            titles.append(m.group(1).strip())
    return titles


def _serialize_agenda_block(config: dict) -> list[str]:
    """Serialize *config* back to ``<!-- agenda ... -->`` lines (no trailing newline)."""
    out: list[str] = ["<!-- agenda"]

    icon = config.get("icon", {})
    out.append("icon:")
    out.append(f'  name: "{icon.get("name", "")}"')
    out.append(f'  visible: {str(icon.get("visible", False)).lower()}')
    out.append(f'  position: {icon.get("position", "right")}')
    color = icon.get("color", "")
    out.append(f'  color: "{color}"')

    out.append("sections:")
    for section in config.get("sections", []):
        out.append(f'  - title: "{section["title"]}"')
        out.append(f'    number: "{section["number"]}"')
        out.append(f'    info: "{section.get("info", "")}"')

    out.append("-->")
    return out


# ── Main sync logic ─────────────────────────────────────────────────────────


def sync_agenda(md_path: Path) -> bool:
    """Sync the agenda block in *md_path* and return ``True`` if the file changed."""
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    agenda_start, agenda_end = _find_agenda_block(lines)

    # Parse existing agenda config (may be absent)
    if agenda_start >= 0:
        existing_config = _parse_agenda_config(lines, agenda_start, agenda_end)
    else:
        existing_config = {}

    # Extract section titles (skipping the agenda block itself)
    safe_start = agenda_start if agenda_start >= 0 else 0
    safe_end = agenda_end if agenda_end >= 0 else 0
    current_titles = _extract_section_titles(lines, safe_start, safe_end)

    if not current_titles:
        print("No # section headings found — nothing to sync.")
        return False

    # Existing sections as an ordered list (position-indexed)
    existing_sections: list[dict] = list(existing_config.get("sections", []))
    old_count = len(existing_sections)
    new_count = len(current_titles)

    # Build merged section list matched **by position** (not by title).
    # - Titles are always updated to match the current # heading (cosmetic).
    # - number and info are preserved for positions that still exist.
    # - Extra positions at the end get new auto-numbered entries with empty info.
    new_sections: list[dict] = []
    for i, title in enumerate(current_titles):
        if i < old_count:
            # Position still exists — keep number/info, update title
            entry = dict(existing_sections[i])
            entry["title"] = title
        else:
            # Brand-new section appended beyond the old count
            entry = {"title": title, "number": "??", "info": ""}
        new_sections.append(entry)

    # Sequential renumbering (00, 01, 02 …) based on final position
    for i, section in enumerate(new_sections):
        section["number"] = f"{i:02d}"

    # Build updated config
    new_config: dict = {}
    if "icon" in existing_config:
        new_config["icon"] = existing_config["icon"]
    else:
        new_config["icon"] = {"name": "", "visible": False, "position": "right", "color": ""}
    new_config["sections"] = new_sections

    new_block_lines = _serialize_agenda_block(new_config)

    # Replace or prepend agenda block
    if agenda_start >= 0:
        updated_lines = lines[:agenda_start] + new_block_lines + lines[agenda_end + 1 :]
    else:
        updated_lines = new_block_lines + [""] + lines

    new_text = "\n".join(updated_lines)
    # Preserve trailing newline from original
    if text.endswith("\n") and not new_text.endswith("\n"):
        new_text += "\n"

    if new_text == text:
        print(f"Agenda already up to date in {md_path.name} ({len(new_sections)} sections).")
        return False

    md_path.write_text(new_text, encoding="utf-8")

    # Report changes
    if new_count > old_count:
        added = current_titles[old_count:]
        print(f"Agenda synced in {md_path.name} — {new_count} sections (+{len(added)} new).")
        print(f"  Added  : {', '.join(added)}")
    elif new_count < old_count:
        removed_count = old_count - new_count
        removed = [s.get("title", "?") for s in existing_sections[new_count:]]
        print(f"Agenda synced in {md_path.name} — {new_count} sections (-{removed_count} removed).")
        print(f"  Removed: {', '.join(removed)}")
    else:
        # Same count — only titles/numbers may have changed
        title_changes = [
            f'"{existing_sections[i].get("title", "")}" → "{current_titles[i]}"'
            for i in range(new_count)
            if existing_sections[i].get("title", "") != current_titles[i]
        ]
        if title_changes:
            print(f"Agenda synced in {md_path.name} — titles updated:")
            for change in title_changes:
                print(f"  {change}")
        else:
            print(f"Agenda already up to date in {md_path.name} ({new_count} sections).")

    return True


# ── Entry point ─────────────────────────────────────────────────────────────

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/sync_agenda.py <presentation-definition.md>")
        sys.exit(1)

    md_path = Path(sys.argv[1]).resolve()
    if not md_path.exists():
        print(f"Error: file not found — {md_path}")
        sys.exit(1)

    sync_agenda(md_path)


if __name__ == "__main__":
    main()
