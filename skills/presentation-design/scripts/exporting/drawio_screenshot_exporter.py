"""
DrawioScreenshotExporter — Render each page of a .drawio file to a PNG.

Pipeline per slide:
  DrawioSvgRenderer.extract_page()
    → render_to_svg(canvas_width * scale, canvas_height * scale)
    → SVG→PNG via one of three backends (first available wins):
        1. Edge/Chrome headless --screenshot  (Windows, no DLL required)
        2. cairosvg                           (Linux, best quality)
        3. svglib + Pillow                    (fallback, needs reportlab)
    → output/qa/drawio/slide-001-Title.png
"""

from __future__ import annotations

import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

logger = logging.getLogger(__name__)

# ── SVG→PNG backend probing ──────────────────────────────────────────────────

def _probe_edge() -> str | None:
    """Return the path to the Edge (or Chrome) executable, or None."""
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    found = shutil.which("msedge") or shutil.which("google-chrome") or shutil.which("chromium-browser")
    return found


def _probe_cairosvg() -> bool:
    try:
        import cairosvg as _cs
        _cs.svg2png  # smoke-test (fails if libcairo DLL missing)
        return True
    except Exception:
        return False


def _probe_svglib() -> bool:
    try:
        from svglib.svglib import svg2rlg  # noqa: F401
        from reportlab.graphics import renderPM  # noqa: F401
        from PIL import Image  # noqa: F401
        return True
    except Exception:
        return False


_EDGE_EXE = _probe_edge()
_CAIROSVG_OK = _probe_cairosvg()
_SVGLIB_OK = _probe_svglib()

if _EDGE_EXE:
    logger.debug("draw.io screenshot backend: Edge/Chrome headless (%s)", _EDGE_EXE)
elif _CAIROSVG_OK:
    logger.debug("draw.io screenshot backend: cairosvg")
elif _SVGLIB_OK:
    logger.debug("draw.io screenshot backend: svglib+Pillow")
else:
    logger.debug("draw.io screenshot: no backend available")


# ── Conversion helpers ───────────────────────────────────────────────────────

def _safe_name(title: str) -> str:
    """Sanitise a slide title for use in a filename."""
    return re.sub(r"[^\w]+", "_", title).strip("_") or "Slide"


def _svg_to_png_edge(svg_str: str, out_path: Path, width: int, height: int) -> None:
    """Render SVG to PNG using Edge/Chrome headless --screenshot."""
    tmp_svg = None
    try:
        with tempfile.NamedTemporaryFile(
            suffix=".svg", delete=False, mode="w", encoding="utf-8", prefix="drawio_qa_"
        ) as tmp:
            tmp.write(svg_str)
            tmp_svg = tmp.name

        svg_url = "file:///" + tmp_svg.replace("\\", "/")
        cmd = [
            _EDGE_EXE,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-software-rasterizer",
            f"--screenshot={str(out_path.resolve())}",
            f"--window-size={width},{height}",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            svg_url,
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        if result.returncode != 0:
            raise RuntimeError(
                f"Edge headless exited {result.returncode}: {result.stderr.decode(errors='replace')}"
            )
        if not out_path.exists():
            raise RuntimeError("Edge headless did not produce a screenshot file.")
    finally:
        if tmp_svg and os.path.exists(tmp_svg):
            try:
                os.unlink(tmp_svg)
            except OSError:
                pass


def _svg_to_png_cairo(svg_str: str, out_path: Path, width: int, height: int) -> None:
    import cairosvg
    cairosvg.svg2png(
        bytestring=svg_str.encode("utf-8"),
        write_to=str(out_path),
        output_width=width,
        output_height=height,
    )


def _svg_to_png_svglib(svg_str: str, out_path: Path, width: int, height: int) -> None:
    import io
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM
    from PIL import Image

    with tempfile.NamedTemporaryFile(suffix=".svg", delete=False, mode="w", encoding="utf-8") as tmp:
        tmp.write(svg_str)
        tmp_path = tmp.name
    try:
        drawing = svg2rlg(tmp_path)
        if drawing is None:
            raise RuntimeError("svglib could not parse SVG")
        buf = io.BytesIO()
        renderPM.drawToFile(drawing, buf, fmt="PNG")
        buf.seek(0)
        img = Image.open(buf)
        img = img.resize((width, height), Image.LANCZOS)
        img.save(str(out_path), "PNG")
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def _svg_to_png(svg_str: str, out_path: Path, width: int, height: int) -> None:
    """Convert SVG string to PNG using the best available backend."""
    if _EDGE_EXE:
        _svg_to_png_edge(svg_str, out_path, width, height)
    elif _CAIROSVG_OK:
        _svg_to_png_cairo(svg_str, out_path, width, height)
    elif _SVGLIB_OK:
        _svg_to_png_svglib(svg_str, out_path, width, height)
    else:
        raise RuntimeError(
            "No SVG→PNG backend available for draw.io screenshots.\n"
            "  • Windows: Edge is normally available at the default install path\n"
            "  • Linux: install cairosvg (pip install cairosvg) or svglib+pillow"
        )


class DrawioScreenshotExporter:
    """Render all pages of a ``.drawio`` file to PNG images.

    Args:
        canvas_width:  Slide canvas width in pixels (matches theme token).
        canvas_height: Slide canvas height in pixels (matches theme token).
        scale:         Output resolution multiplier (default 2 → 2× HiDPI).
    """

    def __init__(
        self,
        canvas_width: int = 1280,
        canvas_height: int = 720,
        scale: int = 2,
    ) -> None:
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.scale = scale

    def export(self, drawio_path: Path, out_dir: Path) -> list[Path]:
        """Render every page of *drawio_path* to PNG files in *out_dir*.

        Args:
            drawio_path: Path to the ``.drawio`` source file.
            out_dir:     Destination directory (created if absent).

        Returns:
            List of paths to the generated PNG files, in slide order.

        Raises:
            RuntimeError: If no SVG→PNG backend is available.
        """
        if not _EDGE_EXE and not _CAIROSVG_OK and not _SVGLIB_OK:
            raise RuntimeError(
                "No SVG→PNG backend available for draw.io screenshots.\n"
                "  • Windows: Edge is normally available at the default install path\n"
                "  • Linux: install cairosvg (pip install cairosvg) or svglib+pillow"
            )

        from scripts.drawio_svg_renderer import DrawioSvgRenderer  # local import

        out_dir.mkdir(parents=True, exist_ok=True)
        renderer = DrawioSvgRenderer()

        pages = self._list_pages(drawio_path)
        if not pages:
            logger.warning("No readable pages found in %s", drawio_path)
            return []

        # Pass scaled dimensions so the SVG <width>/<height> match the PNG output size.
        # Edge headless renders the SVG at its declared size; this ensures the
        # screenshot is exactly canvas_width*scale × canvas_height*scale pixels.
        out_w = self.canvas_width * self.scale
        out_h = self.canvas_height * self.scale
        generated: list[Path] = []

        for idx, page_name in enumerate(pages, start=1):
            safe = _safe_name(page_name)
            png_path = out_dir / f"slide-{idx:03d}-{safe}.png"

            try:
                model = renderer.extract_page(drawio_path, page_name)
                svg_str = renderer.render_to_svg(model, out_w, out_h)
                _svg_to_png(svg_str, png_path, out_w, out_h)
                logger.info("QA drawio  → %s", png_path.name)
                generated.append(png_path)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Failed to render page '%s': %s", page_name, exc)

        return generated

    # ── helpers ──────────────────────────────────────────────────────────

    @staticmethod
    def _list_pages(drawio_path: Path) -> list[str]:
        """Return the ordered list of page names from a ``.drawio`` file.

        Our exporter writes plain (uncompressed) XML, so a simple ET parse
        is sufficient.  Falls back gracefully if a page has no name.
        """
        try:
            tree = ET.parse(drawio_path)
            root = tree.getroot()
        except ET.ParseError as exc:
            logger.error("Cannot parse %s: %s", drawio_path, exc)
            return []

        # Standard mxfile: <diagram name="..."> children
        diagrams = root.findall("diagram")
        if diagrams:
            names: list[str] = []
            for i, d in enumerate(diagrams):
                name = d.get("name") or f"Slide {i + 1}"
                names.append(name)
            return names

        # Legacy: root IS the mxGraphModel
        if root.tag == "mxGraphModel":
            return ["Slide 1"]

        return []
