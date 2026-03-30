"""
slide_helpers.py — Shared parsing and dispatch helpers
─────────────────────────────────────────────────────────────────────────────
Extracted from pptx_builder / drawio_builder so template layout classes and
both builders can import them without duplication.

Public API
──────────
    _parse_props(text)            → dict
    _extract_section_blocks(slide) → list[block]
    _blocks_from_body(slide)       → list[block]
    _merge_block_props(blocks)     → dict
    dispatch(ctx, molecule, props, body, x, y, w, h, slide, index)

Each ``block`` dict has keys: title, molecule, props, body.
"""

from __future__ import annotations

import re
import yaml
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from md_parser import Slide  # type: ignore[import]

from rendering.molecules import MOLECULE_REGISTRY  # type: ignore[import]


# ── Regex ─────────────────────────────────────────────────────────────────────

_CHART_FENCE_RE = re.compile(r"```chart:\w+\n.*?```", re.DOTALL)
_YAML_FENCE_RE  = re.compile(r"```(?:yaml)?\n(.*?)```", re.DOTALL)


# ── Prop parsing ──────────────────────────────────────────────────────────────

def _parse_props(text: str) -> dict:
    """Parse a YAML or colon-separated block into a flat dict."""
    try:
        parsed = yaml.safe_load(text)
        if isinstance(parsed, dict):
            return parsed
        if isinstance(parsed, list):
            result: dict = {}
            for item in parsed:
                if isinstance(item, dict):
                    result.update(item)
            return result
    except Exception:
        pass
    result = {}
    for line in text.splitlines():
        line = line.strip().lstrip("-").strip()
        if ":" in line:
            k, _, v = line.partition(":")
            result[k.strip()] = v.strip()
    return result


# ── Block extraction ──────────────────────────────────────────────────────────

def _extract_section_blocks(slide: "Slide") -> list:
    """Split a slide's raw markdown into a list of block dicts.

    If ``slide.synthetic_blocks`` is set (e.g. for agenda slides injected by
    ``agenda_injector``), those pre-built blocks are returned directly without
    any further parsing.

    The split delimiter adapts to ``slide.block_level``:
    - ``"h2"`` (legacy)  → split on ``##`` headings
    - ``"h3"`` (new)     → split on ``###`` headings
    """
    # ── Synthetic bypass ──────────────────────────────────────────────────────
    if getattr(slide, "synthetic_blocks", None) is not None:
        return slide.synthetic_blocks  # type: ignore[return-value]

    # ── Dynamic delimiter ─────────────────────────────────────────────────────
    block_level = getattr(slide, "block_level", "h2")
    delimiter   = r"^###\s+" if block_level == "h3" else r"^##\s+"

    blocks: list = []
    sections     = re.split(delimiter, slide.raw, flags=re.MULTILINE)
    section_mols = list(slide.molecule_hints)
    mol_index    = 0

    for sec in sections:
        if not sec.strip():
            continue
        # Skip header-only sections (only HTML comments / whitespace)
        content_only = re.sub(r"<!--.*?-->", "", sec, flags=re.DOTALL).strip()
        content_only = _CHART_FENCE_RE.sub("", content_only).strip()
        if not content_only:
            continue

        lines    = sec.splitlines()
        sec_body = "\n".join(lines[1:]).strip()
        mol_match = re.search(r"<!--\s*card:\s*([^>]+)-->", sec_body,
                               re.IGNORECASE)
        mol = (mol_match.group(1).strip() if mol_match else
               section_mols[mol_index] if mol_index < len(section_mols) else "")
        if mol_match or mol:
            mol_index += 1

        body_clean = re.sub(r"<!--.*?-->", "", sec_body, flags=re.DOTALL).strip()
        body_clean = _CHART_FENCE_RE.sub("", body_clean).strip()
        # Unwrap plain ```yaml ... ``` fences so the content is parsed as props
        body_clean = _YAML_FENCE_RE.sub(lambda m: m.group(1), body_clean).strip()
        # Strip trailing slide-separator (---) that leaks from raw slide body
        body_clean = re.sub(r"\s*^---\s*$", "", body_clean, flags=re.MULTILINE).strip()
        props = _parse_props(body_clean)
        # Fallback: molecule declared inside yaml block as ``molecule: kpi-card``
        if not mol and isinstance(props, dict) and props.get("molecule"):
            mol = str(props.pop("molecule")).strip()
            mol_index += 1
        elif isinstance(props, dict):
            props.pop("molecule", None)  # remove stray key if mol was already set
        blocks.append({"title": lines[0].strip(), "molecule": mol,
                       "props": props, "body": body_clean})
    return blocks


def _blocks_from_body(slide: "Slide") -> list:
    """Build a single block from the slide's flat body text (no ## sections)."""
    body  = "\n".join(slide.body_paragraphs)
    props = _parse_props(body)
    return [{"title": slide.title, "molecule": mol or "",
             "props": props, "body": body}
            for mol in (slide.molecule_hints or [""])]


def _merge_block_props(blocks: list) -> dict:
    """Merge all block props dicts into one, last writer wins."""
    merged: dict = {}
    for b in blocks:
        if isinstance(b.get("props"), dict):
            merged.update(b["props"])
    return merged


# ── Molecule dispatch ─────────────────────────────────────────────────────────

def dispatch(ctx, molecule: str, props: dict, body: str,
             x: int, y: int, w: int, h: int, slide, index: int) -> None:
    """Route a molecule slug to its renderer via MOLECULE_REGISTRY.

    Falls back to a placeholder rect for unknown slugs.
    """
    mol = molecule.lower().replace("_", "-")

    if mol == "chart-card":
        # Prefer a fenced ```chart:xxx``` block; fall back to inline props
        if slide.chart_blocks and index < len(slide.chart_blocks):
            chart = slide.chart_blocks[index]
            chart_type = chart.chart_type
            chart_data = chart.data
        elif props:
            chart_type = str(props.get("chart-type") or props.get("chart_type") or "bar")
            chart_data = dict(props)
            chart_data.pop("chart-type", None)
            chart_data.pop("chart_type", None)
        else:
            return
        MOLECULE_REGISTRY["chart-card"].render(ctx, chart_type, chart_data, x, y, w, h)
        return

    renderer = MOLECULE_REGISTRY.get(mol)
    if renderer:
        renderer.render(ctx, props, x, y, w, h, body=body)
    else:
        ctx.rect(x, y, w, h,
                 fill=ctx.color("bg-card"),
                 stroke=ctx.color("border-default"),
                 radius=ctx.rad(),
                 value=f"[{molecule}]")
