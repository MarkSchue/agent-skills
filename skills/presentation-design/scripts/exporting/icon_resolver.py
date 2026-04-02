"""
IconResolver — Download, tint, and cache icon SVGs for exporters.

The renderer emits ``type: icon`` elements containing the icon ligature name,
the font-family (to identify which icon set is active), a colour, and a size.
This module converts those into real SVG files so exporters can embed actual
graphics instead of ligature text strings that only work in browsers.

Supported icon sets and their download URL templates:
  - Material Symbols Outlined  →  fonts.gstatic.com short-term release API
  - Material Icons Outlined    →  fonts.gstatic.com classic outlined API
  - Material Icons             →  fonts.gstatic.com classic filled API
  - Phosphor Icons             →  raw GitHub (phosphor-icons/core)
  - Fallback                   →  graceful None return; exporters use Unicode

The downloaded SVGs are tinted by injecting a ``fill`` attribute on the root
``<svg>`` element.  All paths without an explicit ``fill`` attribute inherit this
colour, which covers 100 % of the mono-colour icon families above.

Tinted SVGs are cached locally under ``<cache_dir>/<slug>/<name>_<color>.svg``
so network calls only happen once per icon+colour combination.
"""

from __future__ import annotations

import hashlib
import logging
import re
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# ── Optional PNG conversion (cairosvg) ───────────────────────────────────────
try:
    import cairosvg as _cairosvg  # type: ignore[import-untyped]
    _CAIROSVG_AVAILABLE = True
except ImportError:
    _CAIROSVG_AVAILABLE = False
    logger.debug("cairosvg not installed — SVG→PNG conversion unavailable (PPTX icons will use Unicode fallback)")

# ── URL templates ────────────────────────────────────────────────────────────
# Key: substring of --icon-font-family value (lower-cased)
# Value: URL template — ``{name}`` is replaced with the icon ligature name
_URL_TEMPLATES: list[tuple[str, str]] = [
    (
        "material symbols outlined",
        "https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsoutlined"
        "/{name}/default/24px.svg",
    ),
    (
        "material symbols",
        "https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsoutlined"
        "/{name}/default/24px.svg",
    ),
    (
        "material icons outlined",
        "https://fonts.gstatic.com/s/i/materialiconsoutlined/{name}/v12/24px.svg",
    ),
    (
        "material icons",
        "https://fonts.gstatic.com/s/i/materialicons/{name}/v12/24px.svg",
    ),
    (
        "phosphor",
        "https://raw.githubusercontent.com/phosphor-icons/core/main/assets/regular/{name}.svg",
    ),
]

# ET namespace registration so output doesn't get ns0: prefixes
ET.register_namespace("", "http://www.w3.org/2000/svg")


class IconResolver:
    """Download, colour-tint, and cache icon SVGs.

    Args:
        cache_dir: Directory where SVG files are cached.  Will be created on
                   first use.  Pass the project ``assets/icons/`` sub-folder.
    """

    def __init__(self, cache_dir: str | Path) -> None:
        self.cache_dir = Path(cache_dir)

    # ── public API ────────────────────────────────────────────────────────

    def resolve(self, name: str, font_family: str, color: str = "#000000") -> Optional[Path]:
        """Return a local path to a tinted SVG for *name*.

        Downloads the SVG on first call; returns the cached path on
        subsequent calls.  Returns ``None`` if the icon cannot be resolved
        (unknown family or download failure).

        Args:
            name: Icon ligature name (e.g. ``"campaign"``).
            font_family: CSS font-family string from the ``--icon-font-family`` token.
            color: Hex colour to tint the icon (e.g. ``"#3B82F6"``).

        Returns:
            Path to the local cached SVG, or ``None``.
        """
        if not name or not font_family:
            return None

        url_template = self._url_template(font_family)
        if url_template is None:
            logger.debug("No SVG URL template for font family %r", font_family)
            return None

        url = url_template.format(name=name)
        cache_path = self._cache_path(name, font_family, color)

        if cache_path.exists():
            return cache_path

        # Download
        svg_text = self._download(url)
        if svg_text is None:
            return None

        # Tint + save
        tinted = self._tint(svg_text, color)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(tinted, encoding="utf-8")
        logger.debug("Cached icon SVG: %s", cache_path)
        return cache_path

    def resolve_png(self, name: str, font_family: str, color: str = "#000000", size: int = 64) -> Optional[Path]:
        """Return a local path to a PNG version of the icon, converted from SVG.

        Uses :meth:`resolve` to obtain the SVG, then converts to PNG via
        ``cairosvg`` (must be installed).  Returns ``None`` if cairosvg is
        unavailable or conversion fails.

        Args:
            name: Icon ligature name.
            font_family: CSS font-family string.
            color: Hex colour to tint the icon.
            size: Output PNG dimensions in pixels (square).

        Returns:
            Path to a local PNG file, or ``None``.
        """
        if not _CAIROSVG_AVAILABLE:
            return None

        svg_path = self.resolve(name, font_family, color)
        if svg_path is None:
            return None

        color_hex = color.lstrip("#").lower()
        png_path = svg_path.with_name(f"{svg_path.stem}_{size}px.png")

        if png_path.exists():
            return png_path

        try:
            _cairosvg.svg2png(
                url=str(svg_path),
                write_to=str(png_path),
                output_width=size,
                output_height=size,
            )
            logger.debug("Cached icon PNG: %s", png_path)
            return png_path
        except Exception as exc:
            logger.warning("SVG→PNG conversion failed for %s: %s", name, exc)
            return None

    # ── private helpers ───────────────────────────────────────────────────

    def _url_template(self, font_family: str) -> Optional[str]:
        """Return the best-matching URL template for *font_family*."""
        ff_lower = font_family.lower()
        for key, template in _URL_TEMPLATES:
            if key in ff_lower:
                return template
        return None

    def _cache_path(self, name: str, font_family: str, color: str) -> Path:
        """Compute a deterministic cache file path."""
        # Sanitise font family to a filesystem-safe slug
        slug = re.sub(r"[^\w]", "_", font_family.lower()).strip("_")
        # Include color in filename so different tints are separate files
        color_hex = color.lstrip("#").lower()
        return self.cache_dir / slug / f"{name}_{color_hex}.svg"

    @staticmethod
    def _download(url: str) -> Optional[str]:
        """Fetch *url* and return the response body as a string."""
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "presentation-design-skill/1.0"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw = resp.read()
                return raw.decode("utf-8", errors="replace")
        except urllib.error.URLError as exc:
            logger.warning("Icon download failed for %s: %s", url, exc)
            return None
        except Exception as exc:  # noqa: BLE001
            logger.warning("Unexpected error downloading icon %s: %s", url, exc)
            return None

    @staticmethod
    def _tint(svg_text: str, color: str) -> str:
        """Inject *color* as the fill on the root ``<svg>`` element.

        All path/shape elements that don't set an explicit fill will inherit
        this colour, which covers every mono-colour icon family.
        """
        # Quick regex approach — avoids re-serialising the full XML tree
        # which can lose namespace declarations and comments.
        # Insert fill inside the opening <svg ...> tag before the first ">".
        def inject_fill(m: re.Match) -> str:
            tag_body = m.group(0)
            # If fill is already present, replace it
            if "fill=" in tag_body:
                tag_body = re.sub(r'fill="[^"]*"', f'fill="{color}"', tag_body)
                tag_body = re.sub(r"fill='[^']*'", f"fill='{color}'", tag_body)
            else:
                # Add fill attribute before the closing > or />
                tag_body = re.sub(r"(/?>)$", f' fill="{color}"\\1', tag_body)
            return tag_body

        # Match the opening <svg ...> tag (possibly multi-line)
        result = re.sub(
            r"<svg[^>]*>",
            inject_fill,
            svg_text,
            count=1,
            flags=re.DOTALL,
        )
        return result
