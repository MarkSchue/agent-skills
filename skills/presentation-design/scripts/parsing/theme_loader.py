"""
ThemeLoader — Parse CSS theme files into ThemeTokens.

Reads a CSS file containing ``.slide-base``, ``.card-base``, variant classes,
text families, and image families, then populates a ``ThemeTokens`` instance.

Only custom-property-like declarations are extracted.  The parser processes
lines of the form::

    --token-name: value;      /* optional comment */

and stores them keyed by the token name (without the leading ``--``).
"""

from __future__ import annotations

import re
from pathlib import Path

from scripts.models.theme import ThemeTokens

# ── regex helpers ────────────────────────────────────────────────────────────

_RE_SELECTOR = re.compile(r"^\s*\.([\w-]+)\s*\{")
_RE_PROPERTY = re.compile(
    r"^\s*--([a-zA-Z0-9_-]+)\s*:\s*(.+?)\s*;", re.DOTALL
)
_RE_BLOCK_END = re.compile(r"^\s*\}")

# Base-level selectors whose tokens go into ``ThemeTokens.base_tokens``
_BASE_SELECTORS = frozenset(
    {
        "slide-base",
        "card-base",
        "text-h1",
        "text-h2",
        "text-body",
        "text-caption",
        "text-label",
        "text-quote",
        "text-footnote",
        "image-fullbleed",
        "image-framed",
        "image-circular",
    }
)


class ThemeLoader:
    """Load CSS theme tokens from disk into a ``ThemeTokens`` model."""

    def load(self, *paths: str | Path) -> ThemeTokens:
        """Load one or more CSS files and merge into a single ``ThemeTokens``.

        Files are loaded in order — later files override earlier ones for
        duplicate token names, which enables the
        ``base.css → default-theme.css → user-theme.css`` layering.

        Args:
            *paths: File paths to CSS theme files.

        Returns:
            Populated ``ThemeTokens`` instance.
        """
        tokens = ThemeTokens()
        for path in paths:
            self._parse_file(Path(path), tokens)
        return tokens

    # ── private ──────────────────────────────────────────────────────────

    def _parse_file(self, path: Path, tokens: ThemeTokens) -> None:
        """Parse a single CSS file and merge into *tokens*."""
        text = path.read_text(encoding="utf-8")
        current_selector: str | None = None

        for line in text.splitlines():
            # Detect selector start
            m = _RE_SELECTOR.match(line)
            if m:
                current_selector = m.group(1)
                continue

            # Detect block end
            if _RE_BLOCK_END.match(line):
                current_selector = None
                continue

            # Extract property
            if current_selector is not None:
                m = _RE_PROPERTY.match(line)
                if m:
                    token_name = m.group(1)
                    raw_value = m.group(2).strip()
                    value = self._coerce_value(raw_value)

                    if current_selector in _BASE_SELECTORS:
                        tokens.set_base(token_name, value)
                    else:
                        tokens.set_variant(current_selector, token_name, value)

    @staticmethod
    def _coerce_value(raw: str) -> int | float | bool | str:
        """Attempt to coerce a CSS token value to a native Python type."""
        # Strip surrounding quotes
        if (raw.startswith('"') and raw.endswith('"')) or (
            raw.startswith("'") and raw.endswith("'")
        ):
            return raw[1:-1]

        # Strip trailing comment (e.g.  "12  /* title size */")
        comment_idx = raw.find("/*")
        if comment_idx != -1:
            raw = raw[:comment_idx].strip()

        # Bool
        if raw.lower() in ("true", "yes"):
            return True
        if raw.lower() in ("false", "no"):
            return False

        # Numeric (with optional px/pt suffix)
        numeric = re.sub(r"(px|pt|em|rem|%)$", "", raw)
        try:
            return int(numeric)
        except ValueError:
            pass
        try:
            return float(numeric)
        except ValueError:
            pass

        return raw
