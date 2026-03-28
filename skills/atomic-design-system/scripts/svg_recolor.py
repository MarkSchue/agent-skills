"""
svg_recolor.py — Recolor SVG fills/strokes using theme token values
─────────────────────────────────────────────────────────────────────────────
Rewrites fill and stroke attributes in an SVG string, mapping original colors
to resolved design token values. The source SVG is never modified.

Usage:
    from scripts.svg_recolor import recolor_svg

    svg_text = open("atoms/svg/chart-bar.svg").read()
    color_map = {"#007bff": "#0f62fe", "#6c757d": "#8d8d8d"}
    output_svg = recolor_svg(svg_text, color_map)
"""

from __future__ import annotations
import re
from pathlib import Path


def recolor_svg(svg_text: str, color_map: dict[str, str]) -> str:
    """Replace fill and stroke colors in SVG text using color_map.

    color_map: {original_hex → replacement_hex}
    Colors are matched case-insensitively.  Values not in color_map are unchanged.
    """
    if not color_map:
        return svg_text

    # Normalize keys to lowercase for matching
    norm_map = {k.lower(): v for k, v in color_map.items()}

    def replace_color(match: re.Match) -> str:
        attr  = match.group(1)   # fill | stroke
        color = match.group(2).lower()
        replacement = norm_map.get(color, match.group(2))
        return f'{attr}="{replacement}"'

    # Match fill="#..." and stroke="#..."
    pattern = re.compile(r'(fill|stroke)="(#[0-9a-fA-F]{3,6})"', re.IGNORECASE)
    output  = pattern.sub(replace_color, svg_text)

    # Also handle CSS-style fill/stroke in style attributes
    def replace_style_color(match: re.Match) -> str:
        prop  = match.group(1)
        color = match.group(2).lower()
        replacement = norm_map.get(color, match.group(2))
        return f"{prop}:{replacement}"

    style_pattern = re.compile(r'(fill|stroke):(#[0-9a-fA-F]{3,6})', re.IGNORECASE)
    output = style_pattern.sub(replace_style_color, output)

    return output


def extract_colors_from_svg(svg_text: str) -> list[str]:
    """Return a sorted list of all unique hex colors present in an SVG."""
    pattern = re.compile(r"(?:fill|stroke)[=:][\"']?(#[0-9a-fA-F]{3,6})", re.IGNORECASE)
    colors  = {m.group(1).lower() for m in pattern.finditer(svg_text)
               if m.group(1).lower() not in ("#none", "#000", "#000000", "#fff", "#ffffff")}
    return sorted(colors)


def build_color_map_from_atom_md(atom_md: str, design_system) -> dict[str, str]:
    """
    Parse an atom file's 'atom-color-map' block and build a fill→token→hex mapping.

    Atom files may include a YAML block like:
        atom-color-map:
          "#4589ff": primary
          "#878d96": neutral

    This function parses that block and resolves token names to hex values.
    """
    import yaml, re as _re
    block_pattern = _re.compile(r"atom-color-map:\s*\n((?:\s{2,}.+\n?)+)", _re.MULTILINE)
    match = block_pattern.search(atom_md)
    if not match:
        return {}

    try:
        raw: dict = yaml.safe_load("atom-color-map:\n" + match.group(1)) or {}
        color_map_yaml = raw.get("atom-color-map", {}) or {}
    except yaml.YAMLError:
        return {}

    result = {}
    for orig_hex, token_name in color_map_yaml.items():
        if isinstance(token_name, str):
            resolved = design_system.color(token_name)
            if resolved:
                result[str(orig_hex)] = resolved
    return result


def recolor_svg_file(svg_path: Path, color_map: dict[str, str],
                     output_path: Path | None = None) -> str:
    """Recolor an SVG file and optionally write to output_path. Returns recolored text."""
    original = svg_path.read_text(encoding="utf-8")
    recolored = recolor_svg(original, color_map)
    if output_path:
        output_path.write_text(recolored, encoding="utf-8")
    return recolored
