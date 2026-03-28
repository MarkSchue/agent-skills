"""
design_system_utils.py — Shared token resolution utilities
─────────────────────────────────────────────────────────────────────────────
Loads a CSS-based theme stylesheet (theme.css) for design tokens and
component styles.  Replaces the former YAML design-config.yaml approach.

Usage:
    from scripts.design_system_utils import DesignSystem

    ds = DesignSystem.load("path/to/theme.css")
    ds.color("primary")          # → "#6750a4"
    ds.canvas()                  # → {"width": 1920, ...}
    ds.resolve("{{theme.color.primary}}")  # legacy placeholder compat
"""

from __future__ import annotations
import sys
from pathlib import Path
from typing import Any

import yaml

# ── Paths ─────────────────────────────────────────────────────────────────────
SKILL_ROOT = Path(__file__).parent.parent
ASSETS     = SKILL_ROOT / "assets"
BRIDGES    = ASSETS / "theme-bridges"

# Import the CSS loader (lives in the same directory)
from css_loader import StyleSheet  # noqa: E402


# ── DesignSystem ──────────────────────────────────────────────────────────────
class DesignSystem:
    """Resolved design configuration backed by a CSS stylesheet."""

    def __init__(self, css: StyleSheet) -> None:
        self._css = css

    # ── Construction ──────────────────────────────────────────────────────────

    @classmethod
    def load(cls, config_path: str | Path | None = None) -> "DesignSystem":
        """Load a CSS theme stylesheet.

        Accepts a ``.css`` file path.  Falls back to the Material theme
        bundled in ``designthemes/materialdesign3/theme.css``.
        """
        config_path = Path(config_path) if config_path else None

        if config_path and config_path.exists():
            css = StyleSheet.load(config_path)
        else:
            fallback = SKILL_ROOT / "designthemes" / "materialdesign3" / "theme.css"
            css = StyleSheet.load(fallback)
        return cls(css)

    # ── Public API — same signatures as before so molecules stay unchanged ────

    @property
    def stylesheet(self) -> StyleSheet:
        """Direct access to the underlying StyleSheet for advanced queries."""
        return self._css

    def resolve(self, text: str) -> str:
        """Replace ``{{token}}`` placeholders in a string with resolved values."""
        return self._css.resolve(text)

    def resolve_dict(self, obj: Any) -> Any:
        """Recursively resolve tokens in a dict/list/str."""
        return self._css.resolve_dict(obj)

    def bridge(self) -> dict:
        """Return the theme-bridge dict with tokens resolved."""
        platform = self._css.var("--platform", "drawio")
        bridge_file = BRIDGES / f"{platform}.yaml"
        if not bridge_file.exists():
            bridge_file = BRIDGES / "drawio.yaml"
        if not bridge_file.exists():
            return {}
        raw = _load_yaml(bridge_file)
        return self.resolve_dict(raw)

    def platform(self) -> str:
        return self._css.var("--platform", "drawio")

    def canvas(self) -> dict:
        return self._css.canvas()

    def chrome(self) -> dict:
        """Slide chrome config — header accent, footer text, page numbers."""
        return self._css.chrome()

    def color(self, name: str) -> str:
        """Hex color for a named token — ``ds.color("primary")``."""
        value = self._css.color(name)
        if name == "slide-divider" and value == "#000000":
            # Older themes may not define slide-divider; fallback to border-subtle.
            return self._css.color("border-subtle")
        return value

    def spacing(self, name: str) -> int:
        """Spacing value in px — ``ds.spacing("m")``."""
        return self._css.spacing(name)

    def font_family(self) -> str:
        return self._css.font_family()

    def font_size(self, role: str) -> int:
        return self._css.font_size(role)

    def font_weight(self, role: str) -> int:
        return self._css.font_weight(role)

    def font_bold(self, role: str) -> bool:
        return self._css.font_bold(role)

    def radius(self, key: str = "radius-medium") -> int:
        return self._css.radius(key)


# ── Registry helpers ──────────────────────────────────────────────────────────

def load_registry(skill_root: Path | None = None) -> dict:
    """Load and return registry.yaml from the skill root."""
    root = Path(skill_root) if skill_root else SKILL_ROOT
    registry_path = root / "registry.yaml"
    if not registry_path.exists():
        raise FileNotFoundError(f"registry.yaml not found at {registry_path}")
    return _load_yaml(registry_path)


def find_element(registry: dict, element_id: str) -> dict | None:
    """Find a registry entry by id across atoms, molecules, templates."""
    for section in ("atoms", "molecules", "templates"):
        for entry in registry.get(section, []):
            if entry.get("id") == element_id:
                return {**entry, "_section": section}
    return None


def load_element_md(element_id: str, registry: dict, skill_root: Path | None = None) -> str:
    """Load the Markdown file for a registry element."""
    root = Path(skill_root) if skill_root else SKILL_ROOT
    entry = find_element(registry, element_id)
    if not entry:
        raise KeyError(f"Element '{element_id}' not found in registry")
    md_path = root / entry["file"]
    if not md_path.exists():
        raise FileNotFoundError(f"Element file not found: {md_path}")
    return md_path.read_text(encoding="utf-8")


# ── Internal helpers ──────────────────────────────────────────────────────────

def _load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}
