"""
md_parser.py — Parse annotated Markdown to a structured slide plan
─────────────────────────────────────────────────────────────────────────────
Reads a Markdown file and returns a list of Slide objects describing:
  - slide title (H1)
  - layout hint (<!-- layout: grid-3 -->)
  - molecule hints (<!-- card: kpi-card, trend-card -->)
  - inline chart data blocks (```chart:bar ... ```)
  - body text for text atoms

Usage:
    from scripts.md_parser import parse_markdown

    slides = parse_markdown("path/to/deck.md")
    for slide in slides:
        print(slide.title, slide.template_hint, slide.molecule_hints)
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


# ── Data structures ───────────────────────────────────────────────────────────

@dataclass
class ChartBlock:
    chart_type: str         # bar | pie | gantt
    data: dict              # parsed YAML data from fenced block


@dataclass
class Slide:
    index: int
    title: str
    template_hint: str | None           # from <!-- layout: ... -->
    molecule_hints: list[str]           # from <!-- card: ... -->
    body_paragraphs: list[str]
    chart_blocks: list[ChartBlock]
    front_matter: dict                  # YAML front-matter from deck header (global)
    raw: str                            # raw source text of this slide section
    chrome_overrides: dict = field(default_factory=dict)  # from <!-- chrome --> block


# ── Parsing ───────────────────────────────────────────────────────────────────

_LAYOUT_COMMENT  = re.compile(r"<!--\s*layout:\s*([^\s>]+)\s*-->", re.IGNORECASE)
_CARD_COMMENT    = re.compile(r"<!--\s*card:\s*([^>]+)-->", re.IGNORECASE)
_CHROME_COMMENT  = re.compile(r"<!--\s*chrome\s*-->", re.IGNORECASE)
_CHART_FENCE     = re.compile(r"```chart:(\w+)\s*\n(.*?)```", re.DOTALL)
_H1              = re.compile(r"^#\s+(.+)$", re.MULTILINE)
_FRONT_MATTER    = re.compile(r"^---\n(.+?)\n---\n", re.DOTALL)


def parse_markdown(md_path: str | Path) -> list[Slide]:
    """Parse a Markdown file and return one Slide per H1 heading."""
    text = Path(md_path).read_text(encoding="utf-8")

    # Strip global front-matter
    global_front_matter: dict = {}
    fm_match = _FRONT_MATTER.match(text)
    if fm_match:
        try:
            global_front_matter = yaml.safe_load(fm_match.group(1)) or {}
        except yaml.YAMLError:
            pass
        text = text[fm_match.end():]

    # Split on H1 headings
    slide_texts = _split_on_h1(text)
    slides: list[Slide] = []

    for idx, (title, body) in enumerate(slide_texts):
        template_hint  = _extract_layout_hint(body)
        molecule_hints = _extract_molecule_hints(body)
        chart_blocks   = _extract_chart_blocks(body)
        body_paragraphs = _extract_body_paragraphs(body)

        chrome_overrides = _extract_chrome_overrides(body)

        slides.append(Slide(
            index            = idx,
            title            = title,
            template_hint    = template_hint,
            molecule_hints   = molecule_hints,
            body_paragraphs  = body_paragraphs,
            chart_blocks     = chart_blocks,
            front_matter     = global_front_matter,
            raw              = body,
            chrome_overrides = chrome_overrides,
        ))

    return slides


def _split_on_h1(text: str) -> list[tuple[str, str]]:
    """Split text on H1 headings; return list of (title, body) tuples."""
    parts: list[tuple[str, str]] = []
    lines = text.splitlines(keepends=True)
    current_title = "(untitled)"
    current_body: list[str] = []

    for line in lines:
        h1_match = re.match(r"^#\s+(.+)$", line.rstrip())
        if h1_match:
            # Only keep a preamble section if it has non-whitespace content
            body_text = "".join(current_body)
            if body_text.strip() or len(parts) > 0:
                parts.append((current_title, body_text))
            current_title = h1_match.group(1).strip()
            current_body = []
        else:
            current_body.append(line)

    if current_title or "".join(current_body).strip():
        parts.append((current_title, "".join(current_body)))

    return parts


def _extract_layout_hint(text: str) -> str | None:
    match = _LAYOUT_COMMENT.search(text)
    return match.group(1).strip() if match else None


def _extract_molecule_hints(text: str) -> list[str]:
    hints: list[str] = []
    for match in _CARD_COMMENT.finditer(text):
        items = [s.strip() for s in match.group(1).split(",") if s.strip()]
        hints.extend(items)
    return hints


def _extract_chart_blocks(text: str) -> list[ChartBlock]:
    blocks: list[ChartBlock] = []
    for match in _CHART_FENCE.finditer(text):
        chart_type = match.group(1).strip()
        data_raw   = match.group(2).strip()
        try:
            data = yaml.safe_load(data_raw) or {}
        except yaml.YAMLError:
            data = {"_raw": data_raw}
        blocks.append(ChartBlock(chart_type=chart_type, data=data))
    return blocks


def _extract_chrome_overrides(text: str) -> dict:
    """Extract per-slide chrome overrides from a <!-- chrome --> YAML block.

    Example in deck.md::

        <!-- chrome -->
        show_page_numbers: false
        footer_text: ""
    """
    m = _CHROME_COMMENT.search(text)
    if not m:
        return {}
    after = text[m.end():]
    yaml_lines: list[str] = []
    for line in after.splitlines():
        stripped = line.strip()
        if not stripped:
            if yaml_lines:
                break
            continue
        if stripped.startswith("<!--") or stripped.startswith("#"):
            if yaml_lines:
                break
            continue
        if re.match(r"^[\w_-]+\s*:", stripped):
            yaml_lines.append(stripped)
        else:
            if yaml_lines:
                break
    if not yaml_lines:
        return {}
    try:
        result = yaml.safe_load("\n".join(yaml_lines)) or {}
        return result if isinstance(result, dict) else {}
    except yaml.YAMLError:
        return {}


def _extract_body_paragraphs(text: str) -> list[str]:
    """Return non-empty paragraphs, excluding comment lines and fenced blocks."""
    # Remove chart blocks
    cleaned = _CHART_FENCE.sub("", text)
    # Remove HTML comments
    cleaned = re.sub(r"<!--.*?-->", "", cleaned, flags=re.DOTALL)
    # Remove H2 headings (section markers)
    cleaned = re.sub(r"^##.*$", "", cleaned, flags=re.MULTILINE)
    # Split into paragraphs
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", cleaned)]
    return [p for p in paragraphs if p]


# ── Markdown template generation ──────────────────────────────────────────────

def generate_md_template(ideas: list[str], registry: dict | None = None) -> str:
    """
    Generate a structured Markdown template from a list of rough slide ideas.

    ideas: list of brief descriptions like ["Company overview", "Q3 revenue results"]
    Returns: a Markdown string ready for user editing
    """
    lines: list[str] = ["---", "design-config: ./design-config.yaml", "---", ""]

    for i, idea in enumerate(ideas):
        lines.append(f"# {idea}")
        lines.append("<!-- layout: [TODO: choose template — hero-title | comparison-2col | grid-3 | numbered-list | data-insight] -->")
        lines.append("<!-- card: [TODO: choose molecules] -->")
        lines.append("")
        lines.append("[TODO: Add slide content here]")
        lines.append("")
        if i < len(ideas) - 1:
            lines.append("---")
            lines.append("")

    return "\n".join(lines)
