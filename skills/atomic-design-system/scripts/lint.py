"""
lint.py — Validate the Atomic Design System library
─────────────────────────────────────────────────────────────────────────────
Checks:
  1. Every file in atoms/, molecules/**/, templates/ has a registry.yaml entry
  2. Every registry entry's file path exists on disk
  3. No atom/molecule/template file contains a literal hex color (#RRGGBB)
  4. All element IDs follow naming conventions
  5. All tags used in registry.yaml are in registry-tags.yaml vocabulary
  6. registry.yaml is under 50 KB

Usage:
    python scripts/lint.py [--root <path-to-skill>]

Exit code 0 = all clear.  Exit code 1 = one or more violations.
"""

from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

import yaml

# ── Constants ─────────────────────────────────────────────────────────────────
HEX_COLOR_PATTERN = re.compile(r"(?<!\w)#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})(?!\w)")
ATOM_NAME_PATTERN     = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)+$")  # <type>-<variant>
MOLECULE_NAME_PATTERN = re.compile(r"^[a-z]+(-[a-z]+)*(-(card|panel|grid))$")
TEMPLATE_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)+$")

MAX_REGISTRY_KB = 50

VIOLATIONS: list[str] = []
WARNINGS:   list[str] = []


def fail(msg: str) -> None:
    VIOLATIONS.append(msg)
    print(f"  ✗ {msg}", file=sys.stderr)


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    print(f"  ⚠ {msg}", file=sys.stderr)


def ok(msg: str) -> None:
    print(f"  ✓ {msg}")


# ── Loaders ───────────────────────────────────────────────────────────────────

def load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


# ── Checks ────────────────────────────────────────────────────────────────────

def check_registry_size(registry_path: Path) -> None:
    size_kb = registry_path.stat().st_size / 1024
    if size_kb > MAX_REGISTRY_KB:
        fail(f"registry.yaml is {size_kb:.1f} KB — exceeds {MAX_REGISTRY_KB} KB limit")
    else:
        ok(f"registry.yaml size: {size_kb:.1f} KB (within {MAX_REGISTRY_KB} KB limit)")


def check_registry_files_exist(registry: dict, root: Path) -> None:
    """Every file path in the registry must exist on disk."""
    for section in ("atoms", "molecules", "templates"):
        for entry in registry.get(section, []):
            entry_id = entry.get("id", "?")
            file_path = root / entry.get("file", "")
            if not file_path.exists():
                fail(f"[{section}] '{entry_id}': file not found: {entry.get('file')}")


def check_all_files_in_registry(registry: dict, root: Path) -> None:
    """Every .md file in atoms/, molecules/**/, templates/ must have a registry entry."""
    registered: set[str] = set()
    for section in ("atoms", "molecules", "templates"):
        for entry in registry.get(section, []):
            rel = entry.get("file", "")
            registered.add(rel)

    for pattern in ("atoms/*.md", "molecules/**/*.md", "templates/*.md"):
        for md_file in root.glob(pattern):
            rel = str(md_file.relative_to(root))
            if rel not in registered:
                warn(f"File '{rel}' has no registry entry — will be ignored by skill")


def check_no_hex_colors_in_elements(registry: dict, root: Path) -> None:
    """Atom, molecule, and template files must not contain literal hex colors."""
    for section in ("atoms", "molecules", "templates"):
        for entry in registry.get(section, []):
            entry_id = entry.get("id", "?")
            file_path = root / entry.get("file", "")
            if not file_path.exists():
                continue
            text = file_path.read_text(encoding="utf-8")
            matches = HEX_COLOR_PATTERN.findall(text)
            if matches:
                fail(f"[{section}] '{entry_id}': contains literal hex color(s): {matches[:3]}")


def check_naming_conventions(registry: dict) -> None:
    """IDs must follow naming patterns per section."""
    for entry in registry.get("atoms", []):
        eid = entry.get("id", "")
        if eid and not ATOM_NAME_PATTERN.match(eid):
            fail(f"[atom] '{eid}': ID does not match <type>-<variant> pattern")

    for entry in registry.get("molecules", []):
        eid = entry.get("id", "")
        if eid and not MOLECULE_NAME_PATTERN.match(eid):
            # Allow more flexible names; just warn
            warn(f"[molecule] '{eid}': ID doesn't end in -card, -panel, or -grid — check convention")

    for entry in registry.get("templates", []):
        eid = entry.get("id", "")
        if eid and not TEMPLATE_NAME_PATTERN.match(eid):
            warn(f"[template] '{eid}': ID may not follow <structure>-<role|count> pattern")


def check_tags_vocabulary(registry: dict, tags_path: Path) -> None:
    """All tags used in registry.yaml must be in registry-tags.yaml."""
    if not tags_path.exists():
        warn("registry-tags.yaml not found — skipping tag vocabulary check")
        return

    tags_data = load_yaml(tags_path)
    allowed: set[str] = set()
    for category_tags in (tags_data.get("categories") or {}).values():
        for t in (category_tags or []):
            allowed.add(str(t))

    for section in ("atoms", "molecules", "templates"):
        for entry in registry.get(section, []):
            entry_id = entry.get("id", "?")
            for tag in (entry.get("tags") or []):
                if tag not in allowed:
                    fail(f"[{section}] '{entry_id}': tag '{tag}' not in registry-tags.yaml vocabulary")


def check_required_atoms_exist(registry: dict) -> None:
    """required_atoms listed in molecules must all be atom IDs in the registry."""
    atom_ids = {e["id"] for e in registry.get("atoms", []) if "id" in e}
    for entry in registry.get("molecules", []):
        entry_id = entry.get("id", "?")
        for atom_id in (entry.get("required_atoms") or []):
            if atom_id not in atom_ids:
                fail(f"[molecule] '{entry_id}': required_atom '{atom_id}' not found in atoms registry")


def check_registry_structure(registry: dict) -> None:
    """Registry must have atoms, molecules, templates (in that order) and version field."""
    if registry.get("version") != 1:
        warn("registry.yaml: 'version: 1' expected at top level")
    for section in ("atoms", "molecules", "templates"):
        if section not in registry:
            fail(f"registry.yaml: missing top-level key '{section}'")


def check_entry_required_fields(registry: dict) -> None:
    """Each entry must have id, description (≤20 words), file, tags."""
    for section in ("atoms", "molecules", "templates"):
        for i, entry in enumerate(registry.get(section, [])):
            pos = f"[{section}][{i}]"
            if not entry.get("id"):
                fail(f"{pos}: missing 'id'")
            if not entry.get("file"):
                fail(f"{pos}: missing 'file'")
            desc = entry.get("description", "")
            if not desc:
                fail(f"{pos} '{entry.get('id','?')}': missing 'description'")
            elif len(desc.split()) > 20:
                warn(f"{pos} '{entry.get('id','?')}': description is {len(desc.split())} words (max 20)")
            if not entry.get("tags"):
                warn(f"{pos} '{entry.get('id','?')}': no 'tags' — reduces discoverability")


# ── Main ──────────────────────────────────────────────────────────────────────

def main(root: Path) -> int:
    registry_path = root / "registry.yaml"
    tags_path     = root / "registry-tags.yaml"

    if not registry_path.exists():
        print(f"✗ registry.yaml not found at {registry_path}", file=sys.stderr)
        return 1

    registry = load_yaml(registry_path)

    print("\n=== Atomic Design System Lint ===\n")

    print("[ registry structure ]")
    check_registry_structure(registry)

    print("\n[ registry size ]")
    check_registry_size(registry_path)

    print("\n[ required fields ]")
    check_entry_required_fields(registry)

    print("\n[ file existence ]")
    check_registry_files_exist(registry, root)

    print("\n[ orphaned files ]")
    check_all_files_in_registry(registry, root)

    print("\n[ hex color violations ]")
    check_no_hex_colors_in_elements(registry, root)

    print("\n[ naming conventions ]")
    check_naming_conventions(registry)

    print("\n[ tag vocabulary ]")
    check_tags_vocabulary(registry, tags_path)

    print("\n[ atom dependencies ]")
    check_required_atoms_exist(registry)

    print(f"\n=== Summary: {len(VIOLATIONS)} violation(s), {len(WARNINGS)} warning(s) ===\n")

    if VIOLATIONS:
        print("VIOLATIONS (must fix):")
        for v in VIOLATIONS:
            print(f"  ✗ {v}")
        return 1
    if WARNINGS:
        print("Warnings (should review):")
        for w in WARNINGS:
            print(f"  ⚠ {w}")
    print("Lint passed ✓")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lint the Atomic Design System library")
    parser.add_argument("--root", default=str(Path(__file__).parent.parent),
                        help="Path to the skill root directory")
    args = parser.parse_args()
    sys.exit(main(Path(args.root)))
