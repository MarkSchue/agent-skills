"""layout_planner.py — deterministic slide layout feasibility and overflow splitting.

Prevents overcrowded slides by estimating a minimum viable width/height for each
content block, checking whether the requested template can satisfy those bounds,
and deterministically falling back to safer templates or continuation slides.

The planner is intentionally conservative:
1. Keep the authored template when it is feasible.
2. Otherwise try alternate single-slide templates for the same block count.
3. Otherwise split the slide into contiguous continuation slides.

The result is stable for the same input deck/theme and applies to both PPTX and
draw.io builders because it runs before rendering.
"""

from __future__ import annotations

from dataclasses import replace
from math import ceil

from md_parser import Slide
from rendering.molecules import MOLECULE_REGISTRY
from slide_helpers import _extract_section_blocks


_COLUMN_LAYOUTS: dict[str, tuple[int, ...]] = {
    "grid-2": (1, 1),
    "comparison-2col": (1, 1),
    "grid-3": (1, 1, 1),
    "grid-4": (1, 1, 1, 1),
    "grid-2-1": (2, 1),
    "grid-1-2": (1, 2),
    "grid-2-1-1": (2, 1, 1),
}

_ROW_LAYOUTS: dict[str, tuple[int, ...]] = {
    "row-2": (1, 1),
    "row-3": (1, 1, 1),
    "row-2-1": (2, 1),
    "row-1-2": (1, 2),
}

_GRID_ROW_LAYOUTS: dict[str, tuple[int, int]] = {
    "grid-row-2-2": (2, 2),
    "grid-row-3-2": (3, 2),
}

_CANDIDATES_BY_BLOCK_COUNT: dict[int, list[str]] = {
    1: ["hero-title"],
    2: ["grid-2-1", "grid-1-2", "grid-2", "row-2", "row-2-1", "row-1-2"],
    3: ["grid-2-1-1", "grid-3", "row-3", "grid-row-2-2"],
    4: ["grid-row-2-2", "grid-4", "row-3"],
}


def expand_overflow_slides(slides: list[Slide], ds) -> list[Slide]:
    """Return a new slide list with infeasible layouts split deterministically."""
    planner = _LayoutPlanner(ds)
    expanded: list[Slide] = []
    for slide in slides:
        expanded.extend(planner.plan_slide(slide))
    for idx, slide in enumerate(expanded):
        slide.index = idx
    return expanded


class _LayoutPlanner:
    def __init__(self, ds) -> None:
        self.ds = ds
        self.canvas = ds.canvas()
        self.chrome_defaults = ds.chrome()

    def plan_slide(self, slide: Slide) -> list[Slide]:
        if getattr(slide, "is_agenda_slide", False):
            return [slide]

        blocks = _extract_section_blocks(slide)
        if not blocks:
            return [slide]

        preferred = slide.template_hint or self._default_layout_for(len(blocks))
        if self._is_layout_feasible(slide, blocks, preferred):
            return [slide]

        single_layout = self._best_layout_for_blocks(slide, blocks, preferred)
        if single_layout is not None:
            if single_layout == preferred:
                return [slide]
            return [self._clone_slide(slide, blocks, single_layout, continuation_index=0)]

        pages: list[Slide] = []
        start = 0
        continuation = 0
        while start < len(blocks):
            best_end = None
            best_layout = None
            for end in range(len(blocks), start, -1):
                chunk = blocks[start:end]
                layout = self._best_layout_for_blocks(slide, chunk, preferred if start == 0 else None)
                if layout is not None:
                    best_end = end
                    best_layout = layout
                    break

            if best_end is None or best_layout is None:
                chunk = [blocks[start]]
                best_end = start + 1
                best_layout = "hero-title"

            chunk = blocks[start:best_end]
            pages.append(
                self._clone_slide(
                    slide,
                    chunk,
                    best_layout,
                    continuation_index=continuation,
                )
            )
            start = best_end
            continuation += 1

        return pages or [slide]

    def _clone_slide(self, slide: Slide, blocks: list, layout: str,
                     continuation_index: int) -> Slide:
        title = slide.title if continuation_index == 0 else f"{slide.title} (cont.)"
        return replace(
            slide,
            title=title,
            template_hint=layout,
            molecule_hints=[str(b.get("molecule", "") or "") for b in blocks],
            body_paragraphs=[],
            chart_blocks=[],
            raw="",
            synthetic_blocks=blocks,
        )

    def _default_layout_for(self, block_count: int) -> str:
        if block_count <= 1:
            return "hero-title"
        if block_count == 2:
            return "grid-2"
        if block_count == 3:
            return "grid-3"
        return "grid-row-2-2"

    def _best_layout_for_blocks(self, slide: Slide, blocks: list,
                                preferred: str | None) -> str | None:
        count = len(blocks)
        candidates: list[str] = []
        if preferred:
            candidates.append(preferred)
        for layout in _CANDIDATES_BY_BLOCK_COUNT.get(count, []):
            if layout not in candidates:
                candidates.append(layout)

        feasible: list[tuple[float, str]] = []
        for layout in candidates:
            score = self._layout_score(slide, blocks, layout, preferred)
            if score is not None:
                feasible.append((score, layout))

        if not feasible:
            return None
        feasible.sort(key=lambda item: (item[0], item[1]))
        return feasible[0][1]

    def _layout_score(self, slide: Slide, blocks: list,
                      layout: str, preferred: str | None) -> float | None:
        slots = self._slot_sizes(slide, layout, len(blocks))
        if not slots or len(blocks) > len(slots):
            return None

        requirements = [self._block_requirements(block) for block in blocks]
        width_slack = 0.0
        height_slack = 0.0
        for req, (slot_w, slot_h) in zip(requirements, slots):
            if slot_w < req["min_width"] or slot_h < req["min_height"]:
                return None
            width_slack += slot_w - req["min_width"]
            height_slack += slot_h - req["min_height"]

        deviation = 0.0 if preferred and layout == preferred else 10.0
        kind = self._layout_kind(layout)
        if preferred and kind != self._layout_kind(preferred):
            deviation += 5.0
        return deviation + width_slack / 1000.0 + height_slack / 2000.0

    def _is_layout_feasible(self, slide: Slide, blocks: list, layout: str) -> bool:
        return self._layout_score(slide, blocks, layout, layout) is not None

    @staticmethod
    def _layout_kind(layout: str | None) -> str:
        if not layout:
            return "unknown"
        if layout in _COLUMN_LAYOUTS:
            return "columns"
        if layout in _ROW_LAYOUTS:
            return "rows"
        if layout in _GRID_ROW_LAYOUTS:
            return "grid"
        if layout == "hero-title":
            return "hero"
        return "other"

    def _slot_sizes(self, slide: Slide, layout: str, block_count: int) -> list[tuple[int, int]]:
        chrome = self._resolve_chrome(slide)
        width = int(self.canvas.get("width", 1920))
        height = int(self.canvas.get("height", 1080))
        margin = int(self.canvas.get("margin", 80))
        gutter = int(self.canvas.get("gutter", 24))
        spacing_m = self.ds.spacing("m")
        gap = int(chrome.get("content_block_gap", gutter))
        cap_pad = int(chrome.get("content_area_padding", 0))
        blk_pad = int(chrome.get("content_block_padding", 0))

        accent_offset = int(chrome.get("accent_height", 0)) if chrome.get("accent_show") else 0
        header_h = int(chrome.get("header_height", 56))
        header_gap = int(chrome.get("header_gap", 12))
        footer_h = int(chrome.get("footer_height", 44)) if (chrome.get("footer_show") or chrome.get("page_number_show")) else 0
        content_y = margin + accent_offset + header_h + header_gap
        content_h = max(1, height - content_y - margin - footer_h)

        if layout == "hero-title":
            return [(width - 2 * margin, content_h - spacing_m)] if block_count == 1 else []

        if layout in _COLUMN_LAYOUTS:
            weights = _COLUMN_LAYOUTS[layout]
            if block_count > len(weights):
                return []
            if layout in ("grid-2", "comparison-2col", "grid-3", "grid-4"):
                cols = len(weights)
                card_w = (width - 2 * margin - (cols - 1) * gutter) // cols
                return [(card_w, content_h)] * min(block_count, cols)

            n = len(weights)
            cx_w = width - 2 * margin - 2 * cap_pad
            ch = content_h - 2 * cap_pad - 2 * blk_pad
            avail_w = cx_w - gap * (n - 1)
            col_widths: list[int] = []
            total_weight = sum(weights) or n
            for idx, wt in enumerate(weights):
                if idx < n - 1:
                    col_widths.append(max(1, int(avail_w * wt / total_weight)))
                else:
                    col_widths.append(max(1, avail_w - sum(col_widths)))
            return [(max(1, cw - 2 * blk_pad), max(1, ch)) for cw in col_widths[:block_count]]

        if layout in _ROW_LAYOUTS:
            weights = _ROW_LAYOUTS[layout]
            if block_count > len(weights):
                return []
            rows = len(weights)
            cw = width - 2 * margin - 2 * cap_pad - 2 * blk_pad
            ch_avail = content_h - 2 * cap_pad
            total_weight = sum(weights) or rows
            unit_h = (ch_avail - (total_weight - 1) * gap) / total_weight
            row_heights = [max(1, int(unit_h * wt + (wt - 1) * gap)) for wt in weights]
            if row_heights:
                assigned = sum(row_heights[:-1]) + gap * (rows - 1)
                row_heights[-1] = max(1, ch_avail - assigned)
            return [(max(1, cw), max(1, rh - 2 * blk_pad)) for rh in row_heights[:block_count]]

        if layout in _GRID_ROW_LAYOUTS:
            cols, rows = _GRID_ROW_LAYOUTS[layout]
            if block_count > cols * rows:
                return []
            cw = width - 2 * margin - 2 * cap_pad
            ch_avail = content_h - 2 * cap_pad
            cell_w = (cw - gap * (cols - 1)) // cols
            cell_h = (ch_avail - gap * (rows - 1)) // rows
            slot = (max(1, cell_w - 2 * blk_pad), max(1, cell_h - 2 * blk_pad))
            return [slot] * block_count

        return []

    def _resolve_chrome(self, slide: Slide) -> dict:
        chrome = dict(self.chrome_defaults)
        fm = slide.front_matter or {}
        if fm.get("page_number_format"):
            chrome["page_number_format"] = str(fm["page_number_format"])
        if "show_page_numbers" in fm:
            chrome["page_number_show"] = bool(fm["show_page_numbers"])
        if "show_footer" in fm:
            chrome["footer_show"] = bool(fm["show_footer"])
        if fm.get("footer_text"):
            chrome["footer_text"] = str(fm["footer_text"])
        for key, value in (slide.chrome_overrides or {}).items():
            chrome[key] = value
        return chrome

    def _block_requirements(self, block: dict) -> dict[str, int]:
        props = dict(block.get("props") or {})
        body = str(block.get("body", "") or "")
        molecule = str(block.get("molecule", "") or "").lower().replace("_", "-")
        renderer = MOLECULE_REGISTRY.get(molecule)
        if renderer and hasattr(renderer, "layout_requirements"):
            try:
                req = renderer.layout_requirements(self.ds, props, body=body)
                if isinstance(req, dict):
                    return {
                        "min_width": max(1, int(req.get("min_width", 320))),
                        "min_height": max(1, int(req.get("min_height", 220))),
                    }
            except Exception:
                pass

        text_len = self._text_density(props, body)
        list_count = self._list_density(props)
        base_w = max(320, self.ds.font_size("body") * 20)
        base_h = max(220, self.ds.font_size("body") * 10)
        min_width = base_w + ceil(text_len / 120) * self.ds.spacing("m") + max(0, list_count - 2) * self.ds.spacing("m")
        min_height = base_h + max(0, list_count - 2) * (self.ds.font_size("body") * 2)
        return {"min_width": min_width, "min_height": min_height}

    def _text_density(self, props: dict, body: str) -> int:
        def _walk(value) -> int:
            if value is None:
                return 0
            if isinstance(value, str):
                return len(value.strip())
            if isinstance(value, dict):
                return sum(_walk(v) for v in value.values())
            if isinstance(value, list):
                return sum(_walk(v) for v in value)
            return len(str(value))
        return _walk(props) + len(body.strip())

    @staticmethod
    def _list_density(props: dict) -> int:
        count = 0
        for key in ("items", "steps", "attributes", "rows", "columns", "entries"):
            value = props.get(key)
            if isinstance(value, list):
                count = max(count, len(value))
        return count
