"""
md_parser.py — Parse annotated Markdown to a structured slide plan
─────────────────────────────────────────────────────────────────────────────
Document hierarchy (new convention)
────────────────────────────────────
  # Section Name       ← H1 = agenda entry / logical section
  ## Slide Title       ← H2 = one physical slide
  ### Card Block       ← H3 = one card zone within a slide

Backward compatibility
──────────────────────
  If no H2 headings are found under any H1, the parser falls back to the
  legacy model where H1 = slide and H2 = card block.  This keeps existing
  deck.md files working without modification.

Usage:
    from scripts.md_parser import parse_markdown

    slides = parse_markdown("path/to/deck.md")
    for slide in slides:
        print(slide.title, slide.template_hint, slide.molecule_hints)
        print("section:", slide.section, "index:", slide.section_index)
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

    # ── Section / hierarchy fields (new hierarchy model) ─────────────────────
    section: str | None   = None   # H1 section title this slide belongs to
    section_index: int    = -1     # 0-based index of the section (-1 = no section)

    # ── Synthetic-slide fields (set by agenda_injector) ───────────────────────
    is_agenda_slide: bool           = False   # True for auto-generated agenda slides
    agenda_highlight_index: int     = -1      # which section is highlighted (-1 = none)
    synthetic_blocks: list | None   = None    # pre-built blocks; bypasses block extractor

    # ── Block level: "h2" (legacy) or "h3" (new hierarchy) ───────────────────
    block_level: str = "h2"   # h2 → split card blocks on ##; h3 → split on ###


# ── Regex constants ───────────────────────────────────────────────────────────

_LAYOUT_COMMENT  = re.compile(r"<!--\s*layout:\s*([^\s>]+)\s*-->", re.IGNORECASE)
_CARD_COMMENT    = re.compile(r"<!--\s*card:\s*([^>]+)-->", re.IGNORECASE)
_CHROME_COMMENT  = re.compile(r"<!--\s*chrome\s*-->", re.IGNORECASE)
_CHART_FENCE     = re.compile(r"```chart:(\w+)\s*\n(.*?)```", re.DOTALL)
_FRONT_MATTER    = re.compile(r"^---\n(.+?)\n---\n", re.DOTALL)
_NO_AGENDA       = re.compile(r"<!--\s*no-agenda\s*-->", re.IGNORECASE)


# ── Public API ────────────────────────────────────────────────────────────────

def parse_markdown(md_path: str | Path) -> list[Slide]:
    """Parse a Markdown file; return one Slide per H2 (new model) or H1 (legacy)."""
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

    if _has_h2_slides(text):
        return _parse_sections(text, global_front_matter)
    else:
        return _parse_legacy(text, global_front_matter)


# ── Hierarchy detection ───────────────────────────────────────────────────────

def _has_h2_slides(text: str) -> bool:
    """Return True when the document uses the new H1 / H2 / H3 hierarchy."""
    in_h1 = False
    for line in text.splitlines():
        stripped = line.rstrip()
        if re.match(r"^#(?!#)\s+\S", stripped):    # exactly H1
            in_h1 = True
        elif re.match(r"^##(?!#)\s+\S", stripped): # exactly H2
            if in_h1:
                return True
    return False


# ── New hierarchy parser: H1 = section, H2 = slide, H3 = card block ──────────

def _parse_sections(text: str, global_front_matter: dict) -> list[Slide]:
    """Parse the H1/H2/H3 hierarchy; return flat list of Slide objects."""
    slides: list[Slide] = []
    slide_idx = 0
    section_idx = -1
    current_section: str | None = None

    for sec_title, sec_body in _split_on_heading(text, level=1):
        sec_title_clean = sec_title.strip()
        # Detect <!-- no-agenda --> in the preamble of the section body (before the first ## slide)
        _preamble_end = re.search(r"^##(?!#)\s", sec_body, re.MULTILINE)
        _preamble     = sec_body[:_preamble_end.start()] if _preamble_end else sec_body
        no_agenda     = bool(_NO_AGENDA.search(_preamble))
        if sec_title_clean and not no_agenda:
            section_idx += 1
            current_section = sec_title_clean
        elif sec_title_clean and no_agenda:
            current_section = sec_title_clean  # keep name for display, but exclude from agenda

        effective_section_idx = -1 if no_agenda else section_idx

        h2_slides = _split_on_heading(sec_body, level=2)

        if not h2_slides:
            if sec_body.strip():
                slides.append(_make_slide(
                    idx=slide_idx,
                    title=current_section or sec_title,
                    body=sec_body,
                    global_fm=global_front_matter,
                    section=current_section,
                    section_index=effective_section_idx,
                    block_level="h3",
                ))
                slide_idx += 1
            continue

        for h2_title, h2_body in h2_slides:
            slides.append(_make_slide(
                idx=slide_idx,
                title=h2_title.strip() or current_section or "",
                body=h2_body,
                global_fm=global_front_matter,
                section=current_section,
                section_index=effective_section_idx,
                block_level="h3",
            ))
            slide_idx += 1

    return slides


def _split_on_heading(text: str, level: int) -> list[tuple[str, str]]:
    """Split *text* on exactly *level* hashes; return [(title, body), ...].

    A preamble before the first heading is returned with an empty title.
    """
    pattern = re.compile(r"^" + "#" * level + r"(?!#)\s+(.+)$", re.MULTILINE)
    parts: list[tuple[str, str]] = []
    last_end   = 0
    last_title = ""

    for m in pattern.finditer(text):
        fragment = text[last_end:m.start()]
        if fragment.strip() or parts:
            parts.append((last_title, fragment))
        last_title = m.group(1).strip()
        last_end   = m.end() + 1   # skip newline after heading

    remainder = text[last_end:]
    if remainder.strip() or last_title:
        parts.append((last_title, remainder))

    return parts


def _make_slide(idx: int, title: str, body: str, global_fm: dict,
                section: str | None, section_index: int,
                block_level: str = "h2") -> Slide:
    """Construct a Slide from parsed fields."""
    return Slide(
        index            = idx,
        title            = title,
        template_hint    = _extract_layout_hint(body),
        molecule_hints   = _extract_molecule_hints(body),
        body_paragraphs  = _extract_body_paragraphs(body),
        chart_blocks     = _extract_chart_blocks(body),
        front_matter     = global_fm,
        raw              = body,
        chrome_overrides = _extract_chrome_overrides(body),
        section          = section,
        section_index    = section_index,
        block_level      = block_level,
    )


# ── Legacy parser: H1 = slide, H2 = card block ───────────────────────────────

def _parse_legacy(text: str, global_front_matter: dict) -> list[Slide]:
    """Original parsing: H1 = slide, H2 = card block."""
    slides: list[Slide] = []

    for idx, (title, body) in enumerate(_split_on_h1(text)):
        slides.append(Slide(
            index            = idx,
            title            = title,
            template_hint    = _extract_layout_hint(body),
            molecule_hints   = _extract_molecule_hints(body),
            body_paragraphs  = _extract_body_paragraphs(body),
            chart_blocks     = _extract_chart_blocks(body),
            front_matter     = global_front_matter,
            raw              = body,
            chrome_overrides = _extract_chrome_overrides(body),
            block_level      = "h2",
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
            body_text = "".join(current_body)
            if body_text.strip() or parts:
                parts.append((current_title, body_text))
            current_title = h1_match.group(1).strip()
            current_body = []
        else:
            current_body.append(line)

    if current_title or "".join(current_body).strip():
        parts.append((current_title, "".join(current_body)))

    return parts


# ── Field extractors ──────────────────────────────────────────────────────────

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
        try:
            data = yaml.safe_load(match.group(2).strip()) or {}
        except yaml.YAMLError:
            data = {"_raw": match.group(2).strip()}
        blocks.append(ChartBlock(chart_type=chart_type, data=data))
    return blocks


def _extract_chrome_overrides(text: str) -> dict:
    """Extract per-slide chrome overrides from a <!-- chrome --> YAML block."""
    m = _CHROME_COMMENT.search(text)
    if not m:
        return {}
    yaml_lines: list[str] = []
    for line in text[m.end():].splitlines():
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
    cleaned = _CHART_FENCE.sub("", text)
    cleaned = re.sub(r"<!--.*?-->", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"^#{2,3}.*$", "", cleaned, flags=re.MULTILINE)
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", cleaned)]
    return [p for p in paragraphs if p]


# ── Markdown template generation ──────────────────────────────────────────────

def generate_md_template(ideas: list[str], registry: dict | None = None) -> str:
    """Generate a structured Markdown template from a list of rough slide ideas."""
    lines: list[str] = ["---", "design-config: ./design-config.yaml", "---", ""]

    for i, idea in enumerate(ideas):
        lines.append(f"# {idea}")
        lines.append("<!-- layout: [TODO: choose template] -->")
        lines.append("<!-- card: [TODO: choose molecules] -->")
        lines.append("")
        lines.append("[TODO: Add slide content here]")
        lines.append("")
        if i < len(ideas) - 1:
            lines.append("---")
            lines.append("")

    return "\n".join(lines)
