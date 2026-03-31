"""
drawio_builder.py — Generate draw.io XML from a resolved slide plan
─────────────────────────────────────────────────────────────────────────────
Architecture:

    DrawioBuilder          ← thin orchestrator: scaffolds pages, delegates layout
        build()            ← public entry-point
        _build_page()      ← scaffold (background, title, divider) + TEMPLATE_REGISTRY lookup
        _background()      ← full-slide background rect
        _slide_title()     ← heading + divider rule, returns content_y
        _canvas()          ← returns (width, height, margin) from design system

    TEMPLATE_REGISTRY      ← maps layout slug → layout renderer (rendering/templates/)
        HeroTitleLayout    ← hero-title
        GridLayout         ← grid-3 / comparison-2col
        DataInsightLayout  ← data-insight
        NumberedListLayout ← numbered-list

    slide_helpers          ← shared parsing + dispatch (used by both builders)
        _extract_section_blocks()
        dispatch()

Usage:
    python scripts/drawio_builder.py deck.md [--stylesheet theme.css] [--output deck.drawio]

Requires: pyyaml
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).parent))
from design_system_utils import DesignSystem
from md_parser import parse_markdown, Slide
from agenda_injector import inject_agenda_slides, materialize_agenda_to_deck, strip_agenda_from_deck
from rendering.context import DrawioCtx
from rendering.templates import TEMPLATE_REGISTRY
from slide_helpers import _extract_section_blocks, dispatch


# ── DrawioBuilder ─────────────────────────────────────────────────────────────

class DrawioBuilder:
    """Thin orchestrator: scaffolds draw.io pages, delegates layout to TEMPLATE_REGISTRY."""

    def __init__(self, ds: DesignSystem) -> None:
        self.ds = ds

    # -- Public API ------------------------------------------------------------

    def build(self, slides: list, output_path: Path) -> None:
        """Build a complete .drawio file from *slides* and write to *output_path*."""
        total = len(slides)
        print(f"Building draw.io output: {total} slide(s) → {output_path}")
        mxfile = ET.Element("mxfile", host="atomic-design-system", type="device")
        for i, slide in enumerate(slides):
            diagram = self._build_page(slide, i, total=total)
            mxfile.append(diagram)
            print(f"  Page {i + 1}: {slide.title}")
        tree = ET.ElementTree(mxfile)
        ET.indent(tree, space="  ")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        tree.write(str(output_path), encoding="utf-8", xml_declaration=True)
        print(f"Wrote {output_path}")

    # -- Per-page rendering ----------------------------------------------------

    def _build_page(self, slide: Slide, page_index: int, total: int = 1):
        """Return an <diagram> element for a single slide."""
        ds              = self.ds
        width, height, margin = self._canvas()
        chrome          = self._resolve_chrome(slide)

        diagram = ET.Element("diagram",
                             name=f"Slide {page_index + 1}: {slide.title[:40]}")
        graph   = ET.SubElement(diagram, "mxGraphModel",
                                {"background": ds.color("surface"),
                                 "pageWidth":  str(width),
                                 "pageHeight": str(height)})
        root    = ET.SubElement(graph, "root")
        ET.SubElement(root, "mxCell", {"id": "0"})
        ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

        ctx       = DrawioCtx(root, ds)
        template  = slide.template_hint or "hero-title"
        page_num  = page_index + 1

        self._background(ctx, chrome, width, height)

        # Optional accent bar at very top of slide
        accent_offset = 0
        if chrome["accent_show"]:
            self._accent_bar(ctx, chrome, width)
            accent_offset = chrome["accent_height"]

        # Logos in the header area
        self._logos(ctx, chrome, width, margin, accent_offset)

        # Slide title → returns content_y
        title_y   = margin + accent_offset
        content_y = self._slide_title(ctx, slide.title, chrome,
                                      margin, title_y, width - 2 * margin)

        # Header divider line (width + alignment driven by CSS tokens)
        if chrome["divider_show"]:
            dx, dw = self._divider_span(width, margin, chrome["divider_width"],
                                        chrome["divider_align"])
            ctx.divider(dx, content_y - 4, dw, color=chrome["divider_color"])

        # Footer zone
        footer_h = 0
        if chrome["footer_show"] or chrome["page_number_show"]:
            footer_h = chrome["footer_height"]
            self._footer(ctx, chrome, slide, width, height, margin, page_num, total)

        content_h = height - content_y - margin - footer_h

        # Content-area background (optional fill between header and footer)
        self._content_bg(ctx, chrome, margin, content_y, width, content_h)

        blocks = _extract_section_blocks(slide)
        layout = TEMPLATE_REGISTRY.get(template, TEMPLATE_REGISTRY["hero-title"])
        layout.render(ctx, slide, blocks, margin, content_y, content_h,
                      width, height, dispatch)

        return diagram

    # -- Scaffold helpers ──────────────────────────────────────────────────────

    def _background(self, ctx: DrawioCtx, chrome: dict, width: int, height: int) -> None:
        """Fill the whole slide; uses --slide-bg-color (falls back to 'surface')."""
        bg = chrome.get("slide_bg_color") or ctx.color("surface")
        ctx.rect(0, 0, width, height, fill=bg)

    def _slide_title(self, ctx: DrawioCtx, title: str, chrome: dict,
                     x: int, y: int, w: int) -> int:
        """Render slide title; return content_y (Y after title + gap)."""
        h = chrome["header_height"]
        ctx.text(x, y, w, h, title,
                 size=ctx.font_size("heading"), bold=ctx.font_bold("heading"),
                 color=chrome["title_color"],
                 align=chrome["title_align"], valign="top")
        return y + h + chrome["header_gap"]

    def _canvas(self):
        c = self.ds.canvas()
        return (int(c.get("width", 1920)),
                int(c.get("height", 1080)),
                int(c.get("margin", 80)))

    def _accent_bar(self, ctx: DrawioCtx, chrome: dict, width: int) -> None:
        """Draw a thin accent stripe across the very top of the slide."""
        ctx.rect(0, 0, width, chrome["accent_height"],
                 fill=chrome["accent_color"], stroke=None)

    def _content_bg(self, ctx: DrawioCtx, chrome: dict,
                    margin: int, content_y: int, width: int, content_h: int) -> None:
        """Draw an optional background fill for the content area."""
        bg = chrome.get("content_area_bg_color", "transparent")
        if not ctx.is_transparent_fill(bg):
            ctx.rect(margin, content_y, width - 2 * margin, content_h, fill=bg)

    @staticmethod
    def _divider_span(slide_w: int, margin: int, width_token: str,
                      align_token: str) -> tuple[int, int]:
        """Compute (x, w) for a header or footer divider from CSS width/align tokens.

        *width_token*  e.g. ``"100%"``, ``"50%"`` or ``"480"`` (px).
        *align_token*  one of ``"left"`` | ``"center"`` | ``"right"``.
        Returns ``(start_x, span_w)``.
        """
        inner = slide_w - 2 * margin
        raw   = str(width_token).strip().lower()
        try:
            if raw.endswith("%"):
                ratio  = max(0.0, min(1.0, float(raw[:-1]) / 100.0))
                span_w = max(1, int(inner * ratio))
            else:
                val = float(raw)
                span_w = max(1, int(val if val <= inner else inner))
        except (ValueError, TypeError):
            span_w = inner
        align = str(align_token).strip().lower()
        if align == "center":
            start_x = margin + max(0, (inner - span_w) // 2)
        elif align == "right":
            start_x = margin + max(0, inner - span_w)
        else:
            start_x = margin
        return start_x, span_w

    def _logos(self, ctx: DrawioCtx, chrome: dict, width: int,
               margin: int, accent_offset: int = 0) -> None:
        """Render primary (left) and secondary (right) logos in the header area."""
        import base64
        from pathlib import Path as _Path

        logo_y = margin + accent_offset
        for side in ("primary", "secondary"):
            src = chrome.get(f"logo_{side}_src", "none")
            if not src or str(src).strip().lower() in ("none", "", "false", "0"):
                continue
            lw = chrome.get(f"logo_{side}_width",  120 if side == "primary" else 80)
            lh = chrome.get(f"logo_{side}_height", 40  if side == "primary" else 30)
            # Resolve file path relative to the CSS source directory
            src_path = _Path(src)
            if not src_path.is_absolute():
                css_dir = getattr(self.ds._css, "source_dir", None)
                if css_dir:
                    src_path = css_dir / src_path
            if not src_path.exists():
                continue
            lx = (margin if side == "primary"
                  else width - margin - lw)
            ly = logo_y + max(0, (chrome["header_height"] - lh) // 2)
            # Embed image as base64 data URI (same approach as draw_icon)
            suffix = src_path.suffix.lower()
            mime   = ("image/png"     if suffix == ".png"  else
                      "image/svg+xml" if suffix == ".svg"  else
                      "image/jpeg")
            b64      = base64.b64encode(src_path.read_bytes()).decode()
            data_uri = f"data:{mime};base64,{b64}"
            style    = (f"shape=image;imageAspect=1;aspect=fixed;"
                        f"image={data_uri};strokeColor=none;fillColor=none;")
            cell = ET.SubElement(ctx.root, "mxCell",
                                 {"id": ctx._new_id(), "parent": "1",
                                  "value": "", "style": style, "vertex": "1"})
            ET.SubElement(cell, "mxGeometry",
                          {"x": str(int(lx)), "y": str(int(ly)),
                           "width": str(int(lw)), "height": str(int(lh)),
                           "as": "geometry"})

    def _footer(self, ctx: DrawioCtx, chrome: dict, slide: Slide,
                width: int, height: int, margin: int,
                page_num: int, total: int) -> None:
        """Draw footer zone: optional divider, left text, right page number."""
        fh      = chrome["footer_height"]
        zone_y  = height - margin - fh
        text_y  = zone_y + 4
        text_h  = fh - 8
        font_sz = max(10, ctx.font_size("body") - 4)
        inner_w = width - 2 * margin

        if chrome["footer_divider_show"]:
            fdx, fdw = self._divider_span(width, margin,
                                          chrome.get("footer_divider_width", "100%"),
                                          chrome.get("footer_divider_align", "left"))
            ctx.divider(fdx, zone_y, fdw, color=chrome["footer_divider_color"])

        if chrome["page_number_show"]:
            num_text = self._format_page_number(page_num, total,
                                                chrome["page_number_format"])
            ctx.text(margin, text_y, inner_w, text_h, num_text,
                     size=font_sz, bold=False,
                     color=chrome["page_number_color"],
                     align=chrome["page_number_align"], valign="middle")

        footer_text = self._resolve_footer_text(chrome, slide)
        if footer_text and chrome["footer_show"]:
            text_w = (
                (inner_w * 2) // 3
                if chrome["page_number_show"] and chrome["page_number_align"] == "right"
                else inner_w
            )
            ctx.text(margin, text_y, text_w, text_h, footer_text,
                     size=font_sz, bold=False,
                     color=chrome["footer_text_color"],
                     align=chrome["footer_text_align"], valign="middle")

    @staticmethod
    def _format_page_number(page_num: int, total: int, fmt: str) -> str:
        fmt = str(fmt).strip()
        if "/" in fmt or "total" in fmt.lower():
            return f"{page_num} / {total}"
        return str(page_num)

    def _resolve_footer_text(self, chrome: dict, slide: Slide) -> str:
        """Footer text: per-slide override > deck front-matter > CSS token."""
        if slide.chrome_overrides.get("footer_text") is not None:
            return str(slide.chrome_overrides["footer_text"])
        if slide.front_matter.get("footer_text"):
            return str(slide.front_matter["footer_text"])
        return chrome.get("footer_text", "")

    def _resolve_chrome(self, slide: Slide) -> dict:
        """Merge CSS chrome defaults with deck front-matter and per-slide overrides."""
        chrome = dict(self.ds.chrome())
        fm = slide.front_matter or {}
        if fm.get("page_number_format"):
            chrome["page_number_format"] = str(fm["page_number_format"])
        if "show_page_numbers" in fm:
            chrome["page_number_show"] = bool(fm["show_page_numbers"])
        if "show_footer" in fm:
            chrome["footer_show"] = bool(fm["show_footer"])
        if fm.get("footer_text"):
            chrome["footer_text"] = str(fm["footer_text"])
        co = slide.chrome_overrides or {}
        for key in ("accent_show", "footer_show", "page_number_show",
                    "divider_show", "footer_divider_show"):
            if key in co:
                chrome[key] = bool(co[key])
        if co.get("footer_text") is not None:
            chrome["footer_text"] = str(co["footer_text"])
        if co.get("title_align"):
            chrome["title_align"] = str(co["title_align"])
        return chrome


# ── Convenience function (backwards-compatible) ───────────────────────────────

def _resolve_stylesheet(md_path: Path, stylesheet_path: Path | None) -> Path | None:
    """Resolve the CSS stylesheet to use for *md_path*.

    Resolution order:
    1. Explicit *stylesheet_path* argument (highest priority).
    2. ``theme:`` key in the deck's YAML front-matter.
    3. ``theme.css`` alongside the Markdown file (auto-detect).
    4. Fall through to ``None`` → DesignSystem uses the bundled default.
    """
    if stylesheet_path is not None:
        return stylesheet_path

    # Check front-matter for a theme: path
    try:
        text = md_path.read_text(encoding="utf-8")
        import re as _re
        fm_match = _re.match(r"^---\n(.+?)\n---\n", text, _re.DOTALL)
        if fm_match:
            import yaml as _yaml
            fm = _yaml.safe_load(fm_match.group(1)) or {}
            theme_val = fm.get("theme")
            if theme_val:
                candidate = (md_path.parent / theme_val).resolve()
                if candidate.exists():
                    return candidate
    except Exception:
        pass

    # Auto-detect theme.css in the same directory as the deck
    sibling = md_path.parent / "theme.css"
    if sibling.exists():
        return sibling

    return None


def build_drawio(md_path: Path, stylesheet_path, output_path: Path) -> None:
    """Build a .drawio file from Markdown + CSS stylesheet."""
    css    = _resolve_stylesheet(md_path, Path(stylesheet_path) if stylesheet_path else None)
    if css:
        print(f"Using stylesheet: {css}")
    else:
        print("WARNING: no project theme.css found — falling back to materialdesign3 default",
              file=__import__('sys').stderr)
    ds     = DesignSystem.load(css)
    slides = parse_markdown(md_path)
    if slides and slides[0].front_matter.get("auto-agenda", True):
        slides = inject_agenda_slides(slides)
        strip_agenda_from_deck(md_path)   # keep source clean; slides are injected at build time
    DrawioBuilder(ds).build(slides, output_path)


# ── CLI entrypoint ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build draw.io from Markdown")
    parser.add_argument("md_file",         help="Input Markdown file")
    parser.add_argument("--stylesheet",    help="CSS theme stylesheet path (theme.css)",
                        default=None)
    parser.add_argument("--output",        help="Output .drawio path",
                        default=None)
    args = parser.parse_args()

    md  = Path(args.md_file)
    css = Path(args.stylesheet) if args.stylesheet else None
    out = Path(args.output) if args.output else md.with_suffix(".drawio")
    build_drawio(md, css, out)
