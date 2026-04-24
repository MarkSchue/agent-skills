#!/usr/bin/env python3
"""
qa_screenshots.py — Generate QA PNG screenshots from both .drawio and .pptx outputs.

Usage:
    python scripts/cli/qa_screenshots.py <project_dir> [options]

Output:
    output/qa/drawio/slide-001-Title.png  …  (one per slide, from draw.io)
    output/qa/pptx/slide-001-Title.png    …  (one per slide, from PPTX)

The output/qa/ folder is wiped before each run so there are never stale images.

Options:
    --scale INT         Resolution multiplier (default: 2 → 2× HiDPI).
    --backend BACKEND   PPTX rendering backend: auto | powerpoint | libreoffice
                        (default: auto — tries PowerPoint first, then LibreOffice).
    --drawio-only       Only generate draw.io screenshots.
    --pptx-only         Only generate PPTX screenshots.
    -v, --verbose       Enable verbose logging.
"""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from pathlib import Path

# Ensure skill root is on sys.path so sibling packages resolve
SKILL_DIR = Path(__file__).resolve().parent.parent.parent
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from scripts.exporting.drawio_screenshot_exporter import DrawioScreenshotExporter
from scripts.exporting.pptx_screenshot_exporter import PptxScreenshotExporter

logger = logging.getLogger("qa_screenshots")


def run_qa(
    project_dir: Path,
    *,
    scale: int = 2,
    backend: str = "auto",
    drawio_only: bool = False,
    pptx_only: bool = False,
) -> list[Path]:
    """Wipe output/qa/ and regenerate PNG screenshots for both output formats.

    Args:
        project_dir:  Path to the presentation project folder.
        scale:        PNG resolution multiplier (default 2 for HiDPI).
        backend:      PPTX backend: ``"auto"`` | ``"powerpoint"`` | ``"libreoffice"``.
        drawio_only:  Only export draw.io screenshots.
        pptx_only:    Only export PPTX screenshots.

    Returns:
        Flat list of all generated PNG paths.
    """
    output_dir = project_dir / "output"
    qa_dir = output_dir / "qa"

    # ── Wipe and recreate qa/ ────────────────────────────────────────────
    # Scope the wipe to only the subfolder(s) that will be regenerated.
    def _wipe(target: Path) -> None:
        if not target.exists():
            return
        try:
            shutil.rmtree(target)
            logger.info("Removed stale QA folder: %s", target)
        except PermissionError:
            # OneDrive or antivirus may hold a lock; delete individual files instead
            logger.debug("rmtree failed (permission); falling back to per-file delete")
            for f in target.rglob("*.png"):
                try:
                    f.unlink()
                except OSError as e:
                    logger.warning("Could not delete %s: %s", f.name, e)

    drawio_qa = qa_dir / "drawio"
    pptx_qa = qa_dir / "pptx"

    if pptx_only:
        _wipe(pptx_qa)
    elif drawio_only:
        _wipe(drawio_qa)
    else:
        _wipe(qa_dir)

    if not pptx_only:
        drawio_qa.mkdir(parents=True, exist_ok=True)
    if not drawio_only:
        pptx_qa.mkdir(parents=True, exist_ok=True)

    generated: list[Path] = []

    # ── draw.io screenshots ──────────────────────────────────────────────
    if not pptx_only:
        drawio_path = output_dir / "presentation.drawio"
        if not drawio_path.exists():
            logger.warning(
                "draw.io output not found at %s — skipping draw.io screenshots. "
                "Run build first (--format drawio or --format both).",
                drawio_path,
            )
        else:
            # Derive canvas size from theme if possible; fall back to defaults
            canvas_w, canvas_h = _canvas_size_from_theme(project_dir)
            exporter = DrawioScreenshotExporter(
                canvas_width=canvas_w,
                canvas_height=canvas_h,
                scale=scale,
            )
            try:
                pngs = exporter.export(drawio_path, drawio_qa)
                generated.extend(pngs)
                logger.info("draw.io QA: %d slides rendered → %s", len(pngs), drawio_qa)
            except RuntimeError as exc:
                logger.error("draw.io screenshot export failed: %s", exc)

    # ── PPTX screenshots ─────────────────────────────────────────────────
    if not drawio_only:
        pptx_path = output_dir / "presentation.pptx"
        if not pptx_path.exists():
            logger.warning(
                "PPTX output not found at %s — skipping PPTX screenshots. "
                "Run build first (--format pptx or --format both).",
                pptx_path,
            )
        else:
            exporter_pptx = PptxScreenshotExporter(scale=scale, backend=backend)
            try:
                pngs = exporter_pptx.export(pptx_path, pptx_qa)
                generated.extend(pngs)
                logger.info("PPTX QA:   %d slides rendered → %s", len(pngs), pptx_qa)
            except RuntimeError as exc:
                logger.error("PPTX screenshot export failed: %s", exc)

    # ── Manifest ─────────────────────────────────────────────────────────
    if generated:
        print("\n--- QA Screenshot Manifest ---")
        for p in generated:
            print(str(p))
        print(f"--- {len(generated)} PNG(s) generated in {qa_dir} ---\n")
    else:
        print("No QA screenshots were generated. Check warnings above.")

    return generated


def _canvas_size_from_theme(project_dir: Path) -> tuple[int, int]:
    """Read canvas-width/height tokens from the project theme (best-effort)."""
    try:
        from scripts.models.theme import ThemeTokens
        from scripts.parsing.theme_loader import ThemeLoader
        from scripts.parsing.base_resolver import resolve_base_files

        themes_dir = SKILL_DIR / "themes"
        theme_css = project_dir / "theme.css"
        files = resolve_base_files(themes_dir, theme_css)
        if theme_css.exists():
            files.append(theme_css)
        loader = ThemeLoader()
        theme = loader.load(*files)
        w = int(theme.resolve("canvas-width") or 1280)
        h = int(theme.resolve("canvas-height") or 720)
        return w, h
    except Exception as exc:  # noqa: BLE001
        logger.debug("Could not read canvas size from theme (%s); using defaults", exc)
        return 1280, 720


# ── CLI ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate QA PNG screenshots from .drawio and .pptx outputs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Output is written to output/qa/drawio/ and output/qa/pptx/ inside\n"
            "the project directory. The qa/ folder is always wiped before each run."
        ),
    )
    parser.add_argument(
        "project_dir",
        type=Path,
        help="Path to the presentation project folder.",
    )
    parser.add_argument(
        "--scale",
        type=int,
        default=2,
        metavar="N",
        help="Resolution multiplier (default: 2 → 2× HiDPI).",
    )
    parser.add_argument(
        "--backend",
        choices=["auto", "powerpoint", "libreoffice"],
        default="auto",
        help="PPTX rendering backend (default: auto).",
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--drawio-only",
        action="store_true",
        help="Only generate draw.io screenshots.",
    )
    mode.add_argument(
        "--pptx-only",
        action="store_true",
        help="Only generate PPTX screenshots.",
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging.",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    run_qa(
        args.project_dir.resolve(),
        scale=args.scale,
        backend=args.backend,
        drawio_only=args.drawio_only,
        pptx_only=args.pptx_only,
    )


if __name__ == "__main__":
    main()
