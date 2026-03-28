#!/usr/bin/env python3
"""
qa_render.py — Convert a PPTX to individual slide JPEG images for visual QA.
=============================================================================

Usage
-----
    python scripts/qa_render.py <pptx_file> [options]

Options
-------
    --output-dir DIR   Folder to write images into (default: <pptx_dir>/qa/)
    --dpi N            Render resolution (default: 150)
    --slides N [N …]   Only convert specific slide numbers (1-based)

Output
------
    slide-01.jpg, slide-02.jpg, … in <output_dir>/

Requirements
------------
    LibreOffice (soffice) — PDF conversion
    Poppler (pdftoppm)    — PDF → JPEG

Install on Debian/Ubuntu:
    sudo apt install libreoffice poppler-utils

Both tools must be on PATH, or soffice must be available at the standard
LibreOffice install locations (macOS: /Applications/LibreOffice.app/...).
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


# ---------------------------------------------------------------------------
# Soffice resolver (handles macOS .app bundle path as well)
# ---------------------------------------------------------------------------

_SOFFICE_CANDIDATES = [
    "soffice",
    "/usr/bin/soffice",
    "/usr/lib/libreoffice/program/soffice",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "/opt/libreoffice/program/soffice",
]


def _find_soffice() -> str:
    for candidate in _SOFFICE_CANDIDATES:
        if shutil.which(candidate) or Path(candidate).is_file():
            return candidate
    raise FileNotFoundError(
        "LibreOffice (soffice) not found. Install it or add it to PATH.\n"
        "  Debian/Ubuntu: sudo apt install libreoffice\n"
        "  macOS:         brew install --cask libreoffice"
    )


def _find_pdftoppm() -> str:
    found = shutil.which("pdftoppm")
    if not found:
        raise FileNotFoundError(
            "pdftoppm not found. Install Poppler utils.\n"
            "  Debian/Ubuntu: sudo apt install poppler-utils\n"
            "  macOS:         brew install poppler"
        )
    return found


# ---------------------------------------------------------------------------
# Conversion steps
# ---------------------------------------------------------------------------

def _pptx_to_pdf(soffice: str, pptx_path: Path, work_dir: Path) -> Path:
    """Convert PPTX → PDF using LibreOffice headless."""
    cmd = [
        soffice,
        "--headless",
        "--convert-to", "pdf",
        "--outdir", str(work_dir),
        str(pptx_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("soffice stderr:", result.stderr, file=sys.stderr)
        raise RuntimeError(f"LibreOffice conversion failed (exit {result.returncode})")

    pdf_path = work_dir / (pptx_path.stem + ".pdf")
    if not pdf_path.exists():
        raise FileNotFoundError(
            f"Expected PDF not found: {pdf_path}\n"
            f"soffice output: {result.stdout}"
        )
    return pdf_path


def _pdf_to_jpegs(
    pdftoppm: str,
    pdf_path: Path,
    output_dir: Path,
    dpi: int,
    slides: list[int] | None,
) -> list[Path]:
    """Convert PDF → JPEG files using pdftoppm."""
    prefix = str(output_dir / "slide")
    cmd = [pdftoppm, "-jpeg", "-r", str(dpi)]

    if slides:
        # pdftoppm uses -f/-l for first/last page (1-based)
        # For arbitrary page sets, run individually
        paths: list[Path] = []
        for page in slides:
            page_cmd = cmd + ["-f", str(page), "-l", str(page),
                              str(pdf_path), prefix]
            subprocess.run(page_cmd, check=True, capture_output=True)
        # collect all generated files
        paths = sorted(output_dir.glob("slide-*.jpg"))
        return paths

    cmd += [str(pdf_path), prefix]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("pdftoppm stderr:", result.stderr, file=sys.stderr)
        raise RuntimeError(f"pdftoppm failed (exit {result.returncode})")

    return sorted(output_dir.glob("slide-*.jpg"))


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def render(
    pptx_path: str | Path,
    output_dir: str | Path | None = None,
    dpi: int = 150,
    slides: list[int] | None = None,
) -> list[Path]:
    """
    Convert *pptx_path* to JPEG slide images.

    Parameters
    ----------
    pptx_path  : path to the source .pptx file
    output_dir : destination folder (created if needed); defaults to
                 <pptx_dir>/qa/
    dpi        : render resolution (150 is fast; 200-300 for print QA)
    slides     : list of 1-based slide numbers to render; None = all

    Returns
    -------
    Sorted list of generated Path objects.
    """
    pptx_path = Path(pptx_path).resolve()
    if not pptx_path.exists():
        raise FileNotFoundError(f"PPTX not found: {pptx_path}")

    if output_dir is None:
        output_dir = pptx_path.parent / "qa"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    soffice  = _find_soffice()
    pdftoppm = _find_pdftoppm()

    with tempfile.TemporaryDirectory(prefix="qa_render_") as tmp:
        tmp_path = Path(tmp)
        print(f"[qa_render] Converting {pptx_path.name} → PDF …")
        pdf_path = _pptx_to_pdf(soffice, pptx_path, tmp_path)

        print(f"[qa_render] Rendering slides at {dpi} dpi …")
        images = _pdf_to_jpegs(pdftoppm, pdf_path, output_dir, dpi, slides)

    print(f"[qa_render] {len(images)} image(s) written to {output_dir}/")
    for img in images:
        print(f"  {img}")
    return images


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a PPTX to per-slide JPEG images for visual QA.",
    )
    parser.add_argument("pptx", help="Path to the .pptx file")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory (default: <pptx_dir>/qa/)")
    parser.add_argument("--dpi", type=int, default=150,
                        help="Render resolution in DPI (default: 150)")
    parser.add_argument("--slides", nargs="+", type=int, default=None,
                        metavar="N",
                        help="Only render these slide numbers (1-based)")
    args = parser.parse_args()

    try:
        render(
            pptx_path=args.pptx,
            output_dir=args.output_dir,
            dpi=args.dpi,
            slides=args.slides,
        )
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
