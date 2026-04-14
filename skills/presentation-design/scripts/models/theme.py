"""
Theme token models: ThemeTokens and supporting style structures.

ThemeTokens is the in-memory representation of a parsed CSS theme file.
It exposes a single ``resolve(namespace, property, overrides)`` method that
implements the 4-level override priority chain:

1. per-card / per-slide Markdown override
2. variant CSS class (e.g. ``.card--kpi``)
3. base CSS class (e.g. ``.card-base``)
4. Python fallback default
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


# ── Python fallback defaults ─────────────────────────────────────────────────
# Used when a token is not found in any CSS layer or override dict.
FALLBACK_DEFAULTS: dict[str, Any] = {
    # Canvas
    "canvas-width": 1280,
    "canvas-height": 720,
    "canvas-margin-top": 20,
    "canvas-margin-right": 20,
    "canvas-margin-bottom": 20,
    "canvas-margin-left": 20,
    "canvas-card-gap": 12,
    "canvas-background-color": "#FFFFFF",
    # Slide title
    "slide-title-font-size": 28,
    "slide-title-font-color": "#1A1A1A",
    "slide-title-font-weight": "bold",
    "slide-title-alignment": "left",
    # Slide subtitle
    "slide-subtitle-font-size": 18,
    "slide-subtitle-font-color": "#555555",
    "slide-subtitle-font-weight": "normal",
    # Divider
    "slide-divider-border-color": "#CCCCCC",
    "slide-divider-border-width": 1,
    # Footer
    "slide-footer-font-size": 10,
    "slide-footer-font-color": "#888888",
    "slide-footer-background-color": "transparent",
    # Page number
    "slide-page-number-font-size": 10,
    "slide-page-number-font-color": "#888888",
    # Card base
    "card-background": "#FFFFFF",
    "card-border-color": "#E0E0E0",
    "card-border-width": 1,
    "card-border-radius": 8,
    "card-padding": 16,
    "card-title-font-size": 16,
    "card-title-font-color": "#1A1A1A",
    "card-title-font-weight": "bold",
    "card-title-line-color": "#003087",
    "card-title-line-width": 2,
    # Text styles
    "text-h1-font-size": 36,
    "text-h1-font-color": "#1A1A1A",
    "text-h1-font-weight": "bold",
    "text-h2-font-size": 28,
    "text-h2-font-color": "#1A1A1A",
    "text-h2-font-weight": "bold",
    "text-body-font-size": 14,
    "text-body-font-color": "#333333",
    "text-body-font-weight": "normal",
    "text-caption-font-size": 11,
    "text-caption-font-color": "#888888",
    "text-label-font-size": 12,
    "text-label-font-color": "#555555",
    "text-quote-font-size": 16,
    "text-quote-font-color": "#333333",
    "text-footnote-font-size": 9,
    "text-footnote-font-color": "#AAAAAA",
}


@dataclass
class ThemeTokens:
    """In-memory CSS token store with multi-layer resolution.

    ``base_tokens``
        Tokens from ``.slide-base``, ``.card-base``, and text/image families.
    ``variant_tokens``
        Tokens from variant classes (``.card--kpi``, ``.card--chart``, …).
    """

    base_tokens: dict[str, Any] = field(default_factory=dict)
    variant_tokens: dict[str, dict[str, Any]] = field(default_factory=dict)

    # ── public API ────────────────────────────────────────────────────────

    def resolve(
        self,
        token_name: str,
        *,
        variant: str | None = None,
        overrides: dict[str, Any] | None = None,
    ) -> Any:
        """Resolve a token through the 4-level priority chain.

        Args:
            token_name: Fully-qualified token name (e.g. ``card-border-radius``).
            variant: Optional variant class name (e.g. ``card--kpi``).
            overrides: Per-card or per-slide Markdown overrides dict.

        Returns:
            The resolved value, or the Python fallback default.
        """
        # 1. Per-card / per-slide override
        if overrides:
            # Allow both dash-style and underscore-style keys
            if token_name in overrides:
                candidate = overrides[token_name]
                return self._resolve_var_reference(candidate, variant, overrides)
            underscore_key = token_name.replace("-", "_")
            if underscore_key in overrides:
                candidate = overrides[underscore_key]
                return self._resolve_var_reference(candidate, variant, overrides)

        # 2. Variant class token
        if variant and variant in self.variant_tokens:
            vt = self.variant_tokens[variant]
            if token_name in vt:
                return self._resolve_var_reference(vt[token_name], variant, overrides)

        # 3. Base class token
        if token_name in self.base_tokens:
            return self._resolve_var_reference(self.base_tokens[token_name], variant, overrides)

        # 4. Python fallback
        return FALLBACK_DEFAULTS.get(token_name)

    def set_base(self, token_name: str, value: Any) -> None:
        """Set a base-level token value."""
        self.base_tokens[token_name] = value

    def set_variant(self, variant: str, token_name: str, value: Any) -> None:
        """Set a variant-level token value."""
        if variant not in self.variant_tokens:
            self.variant_tokens[variant] = {}
        self.variant_tokens[variant][token_name] = value

    def _resolve_var_reference(
        self,
        value: Any,
        variant: str | None = None,
        overrides: dict[str, Any] | None = None,
    ) -> Any:
        """Resolve a one-level ``var(--token-name)`` reference in a token value."""
        if not isinstance(value, str):
            return value

        match = re.match(r"^var\(--(.+)\)$", value)
        if not match:
            return value

        ref = match.group(1)

        # First check overrides, allowing dash/underscore names.
        if overrides:
            if ref in overrides:
                return overrides[ref]
            override_key = ref.replace("-", "_")
            if override_key in overrides:
                return overrides[override_key]

        # Then variant token values.
        if variant and variant in self.variant_tokens:
            vt = self.variant_tokens[variant]
            if ref in vt:
                return vt[ref]

        # Then base token values.
        if ref in self.base_tokens:
            return self.base_tokens[ref]

        # Finally, Python fallback defaults.
        return FALLBACK_DEFAULTS.get(ref, value)
