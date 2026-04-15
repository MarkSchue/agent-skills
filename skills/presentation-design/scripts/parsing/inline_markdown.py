"""
inline_markdown — parse inline **bold** and *italic* markdown within text strings.

Supported syntax (MD-compatible):
  ``**text**``       → bold
  ``*text*``         → italic
  ``***text***``     → bold + italic

Public API:
  ``parse_inline(text)``  → list of run dicts  ({"text", "bold", "italic"})
  ``strip_inline(text)``  → plain text without markers  (used for layout sizing)
  ``text_and_runs(text)`` → partial element-dict fragment (convenience wrapper)
"""

from __future__ import annotations

import re

# Ordered longest-first so *** is tested before ** before *.
_INLINE_RE = re.compile(
    r"\*\*\*(.*?)\*\*\*"   # bold + italic
    r"|\*\*(.*?)\*\*"       # bold
    r"|\*(.*?)\*",          # italic
    re.DOTALL,
)


def parse_inline(text: str) -> list[dict]:
    """Parse inline ``**bold**`` / ``*italic*`` markdown into a list of run dicts.

    Each run is a dict with keys ``text`` (str), ``bold`` (bool), ``italic`` (bool).
    Returns a single un-decorated run when *text* contains no markup.
    """
    if not text or "*" not in text:
        return [{"text": text, "bold": False, "italic": False}]

    runs: list[dict] = []
    last = 0
    for m in _INLINE_RE.finditer(text):
        if m.start() > last:
            runs.append({"text": text[last : m.start()], "bold": False, "italic": False})
        if m.group(1) is not None:      # ***bold+italic***
            runs.append({"text": m.group(1), "bold": True, "italic": True})
        elif m.group(2) is not None:    # **bold**
            runs.append({"text": m.group(2), "bold": True, "italic": False})
        else:                           # *italic*
            runs.append({"text": m.group(3), "bold": False, "italic": True})
        last = m.end()

    if last < len(text):
        runs.append({"text": text[last:], "bold": False, "italic": False})

    return runs or [{"text": text, "bold": False, "italic": False}]


def strip_inline(text: str) -> str:
    """Return *text* with all inline markdown markers removed.

    Used by renderers to obtain a plain string for layout-width estimation
    while the original marked-up text is kept for the exporter via ``runs``.
    """
    if not text or "*" not in text:
        return text
    return _INLINE_RE.sub(lambda m: m.group(1) or m.group(2) or m.group(3), text)


def text_and_runs(text: str) -> dict:
    """Return a partial element-dict fragment for a text element.

    Sets ``"text"`` to the plain (marker-stripped) version of *text* so that
    exporters always have a safe fallback, and adds ``"runs"`` only when *text*
    contains actual bold/italic markup.

    Usage in renderers::

        box.add({
            "type": "text",
            "x": x, "y": y, "w": w, "h": h,
            **text_and_runs(heading_text),
            "font_size": h_size,
            "font_color": h_color,
            ...
        })
    """
    if not text or "*" not in text:
        return {"text": text}
    runs = parse_inline(text)
    plain = strip_inline(text)
    if any(r["bold"] or r["italic"] for r in runs):
        return {"text": plain, "runs": runs}
    return {"text": plain}
