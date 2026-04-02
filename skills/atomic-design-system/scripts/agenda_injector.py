"""
agenda_injector.py — Auto-generate and inject agenda slides into a slide list
─────────────────────────────────────────────────────────────────────────────
Given a list of Slide objects produced by ``parse_markdown``, this module
inserts two kinds of synthetic agenda slides:

1. **Overview agenda** (inserted at position 1, after the cover slide):
   shows all sections with no highlight.

2. **Highlighted agenda** (inserted before the first slide of each section):
   shows all sections with the current section highlighted.

The agenda slide uses the ``grid-1-2`` layout template (1 narrow left column +
2 wide right columns).  The left column contains a ``stacked-text`` molecule
showing "Agenda" as a title.  The right column contains an ``agenda-card``
molecule with all section entries.

Usage::

    from scripts.md_parser import parse_markdown
    from scripts.agenda_injector import inject_agenda_slides

    slides = parse_markdown("deck.md")
    slides = inject_agenda_slides(slides)

To opt out of auto-injection, add ``auto-agenda: false`` to the deck front-matter.
"""

from __future__ import annotations

import io
import re
from pathlib import Path

import yaml

from md_parser import Slide, ChartBlock


# ── Public API ────────────────────────────────────────────────────────────────

def inject_agenda_slides(slides: list[Slide]) -> list[Slide]:
    """Return a new slide list with agenda slides automatically injected.

    Injection is skipped when:
    - There are fewer than 2 slides.
    - No section information is present (all ``section_index`` == -1).
    - Fewer than 2 distinct sections are present (no meaningful agenda).

    Previously-materialized ``# __agenda__`` slides (written back to deck.md
    by :func:`materialize_agenda_to_deck`) are filtered out before injection so
    they never appear twice.  Set ``auto-agenda: false`` in the deck
    front-matter to use those slides instead of auto-generating them.
    """
    # Remove previously-materialized __agenda__ slides
    slides = [s for s in slides if s.section != "__agenda__"]

    sections = collect_sections(slides)
    if len(sections) < 2:
        return slides   # nothing meaningful to inject

    global_fm = slides[0].front_matter if slides else {}

    # Map parser section_index → 0-based position in the sections list
    sec_idx_to_pos: dict[int, int] = {sec["index"]: pos for pos, sec in enumerate(sections)}

    result: list[Slide] = []

    # 0: always keep cover slide unchanged
    result.append(slides[0])

    # 1: insert overview agenda (no highlight)
    result.append(_make_agenda_slide(sections, highlight_index=-1, global_fm=global_fm))

    # track which sections we've already inserted a highlighted agenda for
    emitted_sections: set[int] = set()

    for slide in slides[1:]:      # skip cover which was already added
        sec_idx = slide.section_index

        # Insert a highlighted agenda before the first slide of each section
        if sec_idx >= 0 and sec_idx not in emitted_sections:
            emitted_sections.add(sec_idx)
            pos = sec_idx_to_pos.get(sec_idx)
            if pos is not None:
                result.append(_make_agenda_slide(
                    sections,
                    highlight_index=pos,
                    global_fm=global_fm,
                ))

        result.append(slide)

    # Re-index slides sequentially
    for i, s in enumerate(result):
        s.index = i

    return result


def collect_sections(slides: list[Slide]) -> list[dict]:
    """Return ordered list of unique section dicts from the slide list.

    Each dict has keys: ``index`` (0-based), ``title`` (str).
    Sections with ``section_index == -1`` are skipped (no section header).
    The synthetic ``__agenda__`` meta-section is also excluded.
    """
    seen: dict[int, str] = {}
    for slide in slides:
        if slide.section_index >= 0 and slide.section_index not in seen:
            if slide.section != "__agenda__":
                seen[slide.section_index] = slide.section or ""

    return [{"index": k, "title": v} for k, v in sorted(seen.items())]


# ── Slide builder ─────────────────────────────────────────────────────────────

def _make_agenda_slide(sections: list[dict], highlight_index: int,
                       global_fm: dict) -> Slide:
    """Build a synthetic Slide representing an agenda overview or divider.

    The slide title is always "Agenda".
    The left stacked-text block shows the active section name (highlighted
    agenda) or "Overview" (when no section is highlighted).
    """

    entries = [
        {
            "label_type": "number",
            "label": f"{i + 1:02d}",
            "title": sec["title"],
            "description": "",
            "highlight": (i == highlight_index),
        }
        for i, sec in enumerate(sections)
    ]

    left_title = sections[highlight_index]["title"] if highlight_index >= 0 else "Overview"

    left_block = {
        "title": left_title,
        "molecule": "stacked-text",
        "props": {"title": left_title},
        "body": "",
    }
    right_block = {
        "title": "",
        "molecule": "agenda-card",
        "props": {
            "entries": entries,
            "show-title": False,
        },
        "body": "",
    }

    return Slide(
        index                  = -1,          # will be re-indexed by inject_agenda_slides
        title                  = "Agenda",
        template_hint          = "grid-1-2",
        molecule_hints         = ["stacked-text", "agenda-card"],
        body_paragraphs        = [],
        chart_blocks           = [],
        front_matter           = global_fm,
        raw                    = "",
        chrome_overrides       = {},
        section                = None,
        section_index          = -1,
        is_agenda_slide        = True,
        agenda_highlight_index = highlight_index,
        synthetic_blocks       = [left_block, right_block],
        block_level            = "h2",
    )


# ── Deck materializer ─────────────────────────────────────────────────────────

_AGENDA_SECTION_RE = re.compile(
    r"^# __agenda__.*?(?=^# (?!__agenda__)|\Z)",
    re.MULTILINE | re.DOTALL,
)


def strip_agenda_from_deck(md_path: Path) -> None:
    """Remove any ``# __agenda__`` section from deck.md without writing a new one.

    Called when ``auto-agenda: true`` so the source file stays clean — agenda
    slides are injected purely at build time from the ``#`` section headers.
    """
    text = Path(md_path).read_text(encoding="utf-8")
    stripped = _AGENDA_SECTION_RE.sub("", text).lstrip("\n")
    if stripped != text:
        Path(md_path).write_text(stripped, encoding="utf-8")
        print(f"Removed stale __agenda__ block from {md_path}")


def materialize_agenda_to_deck(md_path: Path, slides_after_injection: list[Slide]) -> None:
    """Write (or overwrite) the ``# __agenda__`` section at the top of deck.md.

    The section contains editable Markdown blocks for every injected agenda
    slide.  It is placed right after the YAML front-matter (if present) and
    before the first real ``#`` section.

    When ``auto-agenda: false`` is set in the front-matter the parser uses
    these blocks instead of auto-generating them, so the user can freely
    customise titles, entries, and card props without touching the injector.

    The section is always re-generated on each build so it stays in sync with
    the current section list.  User customisations should be applied with
    ``auto-agenda: false`` to prevent overwriting.
    """
    text = Path(md_path).read_text(encoding="utf-8")

    # Collect all agenda slides from the injected list
    agenda_slides = [s for s in slides_after_injection if getattr(s, "is_agenda_slide", False)]
    if not agenda_slides:
        return

    # Build the __agenda__ section text
    buf = io.StringIO()
    buf.write("# __agenda__\n")
    buf.write("<!-- auto-generated on every build — to customise, set  auto-agenda: false"
              "  in the front-matter and edit this section directly -->\n\n")

    for slide in agenda_slides:
        hl_idx     = getattr(slide, "agenda_highlight_index", -1)
        # Derive left block title from synthetic_blocks
        blocks     = getattr(slide, "synthetic_blocks", []) or []
        left_title = blocks[0].get("props", {}).get("title", "Overview") if blocks else "Overview"
        right_props: dict = blocks[1].get("props", {}) if len(blocks) > 1 else {}
        entries: list     = right_props.get("entries", [])

        buf.write(f"## Agenda\n")
        buf.write("<!-- layout: grid-1-2 -->\n")
        buf.write(f"### {left_title}\n")
        buf.write("molecule: stacked-text\n")
        buf.write(f"title: {left_title}\n\n")
        buf.write("### Agenda Topics\n")
        buf.write("molecule: agenda-card\n")
        buf.write("show-title: false\n")
        # Dump entries inline as readable YAML
        if entries:
            buf.write("entries:\n")
            for entry in entries:
                e_yaml = yaml.dump(
                    [entry],
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                ).strip()
                # Indent the list item block by 2 spaces
                for line in e_yaml.splitlines():
                    buf.write(f"  {line}\n")
        buf.write("\n---\n\n")

    agenda_block = buf.getvalue()

    # Remove any existing __agenda__ section
    text_stripped = _AGENDA_SECTION_RE.sub("", text).lstrip("\n")

    # Find insertion point: after YAML front-matter (---...---), before first #
    fm_end = 0
    if text_stripped.startswith("---"):
        closing = text_stripped.find("\n---", 3)
        if closing != -1:
            fm_end = closing + 4   # skip past the closing ---\n

    new_text = (
        text_stripped[:fm_end].rstrip("\n")
        + ("\n\n" if fm_end else "")
        + agenda_block
        + text_stripped[fm_end:].lstrip("\n")
    )

    Path(md_path).write_text(new_text, encoding="utf-8")
    print(f"Materialized {len(agenda_slides)} agenda slide(s) → {md_path}")
