"""
css_loader.py — CSS-based design-token & component-style loader
═══════════════════════════════════════════════════════════════════════════════
Replaces the former YAML-based design-config.yaml approach with a well-proven
CSS custom-properties file per design system.

Supports:
  • :root { --color-primary: #6750a4; }      ← design tokens
  • .kpi-card { background: var(--color-primary-container); }  ← component styles
  • @import "materialdesign3";               ← theme inheritance
  • var(--token, fallback)                   ← cascading resolution

Usage:
    from css_loader import StyleSheet

    css = StyleSheet.load("theme.css")
    css.color("primary")         # → "#6750a4"
    css.font_size("heading")     # → 32
    css.radius("radius-medium")  # → 12
    css.canvas()                 # → {"width": 1920, ...}
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any


# ── Paths ─────────────────────────────────────────────────────────────────────
SKILL_ROOT = Path(__file__).parent.parent
THEMES_DIR = SKILL_ROOT / "designthemes"


class StyleSheet:
    """Parsed CSS stylesheet providing design tokens and component-class styles."""

    def __init__(self) -> None:
        self._vars: dict[str, str] = {}       # --name → raw value
        self._resolved: dict[str, str] = {}   # --name → resolved value
        self._classes: dict[str, dict[str, str]] = {}  # selector → {prop: val}
        self.source_dir: Path | None = None   # directory of the first loaded file

    # ── Construction ──────────────────────────────────────────────────────────

    @classmethod
    def load(cls, *paths: Path | str) -> "StyleSheet":
        """Load and merge one or more CSS files.  Later files override earlier."""
        ss = cls()
        for p in paths:
            p = Path(p)
            if not p.exists():
                print(f"WARNING: stylesheet not found: {p}", file=sys.stderr)
                continue
            if ss.source_dir is None:
                ss.source_dir = p.parent
            text = p.read_text(encoding="utf-8")
            ss._parse(text, p.parent)
        ss._resolve_all()
        return ss

    # ── Parsing ───────────────────────────────────────────────────────────────

    def _parse(self, text: str, base_dir: Path) -> None:
        # Strip CSS comments
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)

        # Handle @import directives (before parsing rules)
        for m in re.finditer(r'@import\s+"([^"]+)"\s*;', text):
            ref = m.group(1)
            imp = self._resolve_import(ref, base_dir)
            if imp and imp.exists():
                imp_text = imp.read_text(encoding="utf-8")
                self._parse(imp_text, imp.parent)
            else:
                print(f"WARNING: @import \"{ref}\" could not be resolved", file=sys.stderr)

        # Remove @-rules (e.g. @import, @charset, @namespace) that are NOT
        # block-rules (i.e. those ending with ";" rather than "{ }").
        # Without this, their text contaminates the next rule-block's selector.
        text = re.sub(r"@[^{;]+;", "", text)

        # Parse rule blocks: selector { declarations }
        for m in re.finditer(r"([^{}@]+?)\s*\{([^{}]*)\}", text):
            selector = m.group(1).strip()
            body = m.group(2)
            props = self._parse_declarations(body)
            if selector == ":root":
                self._vars.update(props)
            else:
                self._classes.setdefault(selector, {}).update(props)

    @staticmethod
    def _parse_declarations(body: str) -> dict[str, str]:
        """Parse CSS declarations from a rule body."""
        props: dict[str, str] = {}
        for decl in body.split(";"):
            decl = decl.strip()
            if not decl or ":" not in decl:
                continue
            key, _, val = decl.partition(":")
            props[key.strip()] = val.strip()
        return props

    def _resolve_import(self, ref: str, base_dir: Path) -> Path | None:
        """Resolve an @import reference to an actual file path."""
        # 1. Direct relative path
        candidate = base_dir / ref
        if candidate.exists():
            return candidate
        # 2. With .css extension
        candidate = base_dir / f"{ref}.css"
        if candidate.exists():
            return candidate
        # 3. Look in designthemes/*/theme.css by directory name prefix
        if THEMES_DIR.is_dir():
            for theme_dir in sorted(THEMES_DIR.iterdir()):
                if not theme_dir.is_dir():
                    continue
                css_file = theme_dir / "theme.css"
                if css_file.exists() and theme_dir.name == ref:
                    return css_file
            # Partial match fallback (e.g. "material" → "materialdesign3")
            for theme_dir in sorted(THEMES_DIR.iterdir()):
                if not theme_dir.is_dir():
                    continue
                css_file = theme_dir / "theme.css"
                if css_file.exists() and theme_dir.name.startswith(ref):
                    return css_file
        return None

    # ── Variable resolution ───────────────────────────────────────────────────

    def _resolve_all(self) -> None:
        """Resolve var() references in :root custom properties."""
        self._resolved = dict(self._vars)
        for _ in range(10):  # handle chained vars
            changed = False
            for key, val in list(self._resolved.items()):
                new_val = self._subst(val)
                if new_val != val:
                    self._resolved[key] = new_val
                    changed = True
            if not changed:
                break

    def _subst(self, value: str) -> str:
        """Replace var(--name) / var(--name, fallback) with resolved values."""
        def _replacer(m: re.Match) -> str:
            var_name = m.group(1).strip()
            fallback = m.group(2)
            if var_name in self._resolved:
                return self._resolved[var_name]
            return fallback.strip() if fallback else m.group(0)
        return re.sub(
            r"var\(\s*(--[^,)]+?)(?:\s*,\s*([^)]+))?\s*\)", _replacer, value
        )

    # ═════════════════════════════════════════════════════════════════════════
    #  PUBLIC API — Design Token Accessors
    # ═════════════════════════════════════════════════════════════════════════

    def var(self, name: str, default: str = "") -> str:
        """Get a resolved CSS custom property.  *name* should start with '--'."""
        return self._resolved.get(name, default)

    # -- Colors ----------------------------------------------------------------

    def color(self, token: str) -> str:
        """Hex color for a design-system token.
        ``css.color("primary")`` → value of ``--color-primary``.
        """
        return self.var(f"--color-{token}", "#000000")

    # -- Typography ------------------------------------------------------------

    def font_family(self) -> str:
        raw = self.var("--font-family", "Roboto")
        # Strip CSS quotes: "Roboto", sans-serif → Roboto
        return raw.split(",")[0].strip().strip('"').strip("'")

    def font_size(self, role: str) -> int:
        raw = self.var(f"--font-{role}-size", "14")
        return int(float(raw.replace("px", "")))

    def font_weight(self, role: str) -> int:
        raw = self.var(f"--font-{role}-weight", "400")
        return int(float(raw))

    def font_bold(self, role: str) -> bool:
        return self.font_weight(role) >= 600

    def font_line_height(self, role: str) -> float:
        raw = self.var(f"--font-{role}-line-height", "1.5")
        return float(raw)

    # -- Borders / Radius ------------------------------------------------------

    def radius(self, key: str = "radius-medium") -> int:
        raw = self.var(f"--{key}", "12")
        return int(float(raw.replace("px", "")))

    # -- Spacing ---------------------------------------------------------------

    def spacing(self, name: str = "m") -> int:
        raw = self.var(f"--spacing-{name}", "16")
        return int(float(raw.replace("px", "")))

    # -- Canvas ----------------------------------------------------------------

    def canvas(self) -> dict[str, int]:
        return {
            "width":         int(self.var("--canvas-width", "960")),
            "height":        int(self.var("--canvas-height", "540")),
            "margin":        int(self.var("--canvas-margin", "40")),
            "padding":       int(self.var("--canvas-padding", "20")),
            "gutter":        int(self.var("--canvas-gutter", "24")),
            "baseline-grid": int(self.var("--canvas-baseline-grid", "4")),
        }

    # -- Slide Chrome ----------------------------------------------------------

    def chrome(self) -> dict:
        """Slide chrome config from --slide-* CSS custom properties.

        All chrome elements default to off — opt-in per theme or deck front-matter.
        """
        def _bool(name: str, default: bool) -> bool:
            v = self.var(name, "1" if default else "0")
            return v not in ("0", "false", "none", "")

        def _int(name: str, default: int) -> int:
            try:
                return int(float(self.var(name, str(default))))
            except (ValueError, TypeError):
                return default

        def _color(name: str, fallback_var: str, fallback: str) -> str:
            raw = self.var(name, "")
            return raw if raw else self.var(fallback_var, fallback)

        return {
            "accent_show":          _bool("--slide-accent-show",          False),
            "accent_height":        _int ("--slide-accent-height",        6),
            "accent_color":         _color("--slide-accent-color",        "--color-primary",            "#6750a4"),
            "header_height":        _int ("--slide-header-height",        56),
            "header_gap":           _int ("--slide-header-gap",           12),
            "title_align":          self.var("--slide-title-align",       "left"),
            "title_color":          _color("--slide-title-color",         "--color-on-surface",         "#1c1b1f"),
            "divider_show":         _bool("--slide-divider-show",         True),
            "divider_color":        _color("--slide-divider-color",       "--color-slide-divider",      "#cac4d0"),
            "footer_show":          _bool("--slide-footer-show",          False),
            "footer_height":        _int ("--slide-footer-height",        44),
            "footer_text":          self.var("--slide-footer-text",       ""),
            "footer_text_color":    _color("--slide-footer-text-color",   "--color-on-surface-variant", "#49454f"),
            "footer_text_align":    self.var("--slide-footer-text-align", "left"),
            "footer_divider_show":  _bool("--slide-footer-divider-show",  True),
            "footer_divider_color": _color("--slide-footer-divider-color","--color-border-subtle",      "#cac4d0"),
            "page_number_show":     _bool("--slide-page-number-show",     False),
            "page_number_format":   self.var("--slide-page-number-format","n"),
            "page_number_align":    self.var("--slide-page-number-align", "right"),
            "page_number_color":    _color("--slide-page-number-color",   "--color-on-surface-variant", "#49454f"),
            # ── Layout chrome ─────────────────────────────────────────────
            "slide_bg_color":         _color("--slide-bg-color",            "--color-surface",            "#fffbfe"),
            "slide_bg_image":         self.var("--slide-bg-image",          "none"),
            "content_area_bg_color":  self.var("--content-area-bg-color",   "transparent"),
            "content_area_bg_image":  self.var("--content-area-bg-image",   "none"),
            "content_block_bg_color": self.var("--content-block-bg-color",  "transparent"),
            "content_block_bg_image": self.var("--content-block-bg-image",  "none"),
            "divider_width":          self.var("--slide-divider-width",     "100%"),
            "divider_align":          self.var("--slide-divider-align",     "left"),
            "footer_divider_width":   self.var("--slide-footer-divider-width",  "100%"),
            "footer_divider_align":   self.var("--slide-footer-divider-align",  "left"),
            "content_area_padding":   _int ("--content-area-padding",       0),
            "content_block_padding":  _int ("--content-block-padding",      0),
            "content_block_gap":      _int ("--content-block-gap",          24),
            # ── Logos ──────────────────────────────────────────────────────
            "logo_primary_src":       self.var("--logo-primary-src",        "none"),
            "logo_primary_width":     _int ("--logo-primary-width",         120),
            "logo_primary_height":    _int ("--logo-primary-height",        40),
            "logo_secondary_src":     self.var("--logo-secondary-src",      "none"),
            "logo_secondary_width":   _int ("--logo-secondary-width",       80),
            "logo_secondary_height":  _int ("--logo-secondary-height",      30),
        }

    # -- Elevation -------------------------------------------------------------

    def elevation(self, level: str) -> dict[str, float]:
        return {
            "blur":     float(self.var(f"--elevation-{level}-blur", "0")),
            "distance": float(self.var(f"--elevation-{level}-distance", "0")),
            "angle":    float(self.var(f"--elevation-{level}-angle", "90")),
            "opacity":  float(self.var(f"--elevation-{level}-opacity", "0")),
        }

    # -- Component Class Styles ------------------------------------------------

    def class_style(self, selector: str, prop: str, default: str = "") -> str:
        """Resolved value for a property inside a class selector.

        ``css.class_style(".kpi-card", "background")`` → ``"#eaddff"``
        """
        cls_props = self._classes.get(selector, {})
        raw = cls_props.get(prop, default)
        return self._subst(raw) if raw else default

    def class_styles(self, selector: str) -> dict[str, str]:
        """All resolved properties for a class selector."""
        cls_props = self._classes.get(selector, {})
        return {k: self._subst(v) for k, v in cls_props.items()}

    # -- Backward Compat Bridge ({{theme.*}} placeholders) ---------------------

    def resolve(self, text: str) -> str:
        """Replace legacy ``{{theme.*}}`` placeholders using CSS tokens."""
        if not isinstance(text, str) or "{{" not in text:
            return text
        pattern = re.compile(r"\{\{([^}]+)\}\}")
        def _repl(m: re.Match) -> str:
            key = m.group(1).strip()
            css_var = _legacy_token_to_css_var(key)
            if css_var and css_var in self._resolved:
                return str(self._resolved[css_var])
            print(f"WARNING: unresolved token '{{{{{key}}}}}' — no CSS variable mapped",
                  file=sys.stderr)
            return m.group(0)
        return pattern.sub(_repl, text)

    def resolve_dict(self, obj: Any) -> Any:
        """Recursively resolve ``{{token}}`` placeholders."""
        if isinstance(obj, str):
            return self.resolve(obj)
        if isinstance(obj, dict):
            return {k: self.resolve_dict(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self.resolve_dict(i) for i in obj]
        return obj


# ── Legacy token → CSS var mapping ────────────────────────────────────────────

def _legacy_token_to_css_var(key: str) -> str | None:
    """Map ``theme.color.primary`` → ``--color-primary`` etc."""
    if key.startswith("theme.color."):
        return f"--color-{key[len('theme.color.'):]}"
    if key.startswith("colors."):
        return f"--color-{key[len('colors.'):]}"
    if key.startswith("theme.spacing.") or key.startswith("spacing."):
        name = key.split(".")[-1]
        return f"--spacing-{name}"
    if key.startswith("theme.borders.") or key.startswith("borders."):
        name = key.split(".")[-1]
        return f"--{name}"
    if key.startswith("theme.typography.") or key.startswith("typography."):
        parts = key.split(".")
        if len(parts) >= 3:
            role = parts[-2]
            prop = parts[-1]
            return f"--font-{role}-{prop}"
        if len(parts) == 2:
            return f"--font-{parts[-1]}"
    if key.startswith("canvas."):
        name = key.split(".")[-1]
        return f"--canvas-{name}"
    if key.startswith("elevation."):
        parts = key.split(".")
        if len(parts) >= 3:
            return f"--elevation-{parts[1]}-{parts[2]}"
    return None
