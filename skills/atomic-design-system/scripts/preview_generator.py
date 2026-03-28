"""
preview_generator.py — Generate PNG preview thumbnails for all elements
─────────────────────────────────────────────────────────────────────────────
Creates placeholder PNG thumbnails in previews/atoms/, previews/molecules/,
previews/templates/. Real thumbnails are grey boxes with the element ID text.

Usage:
    python scripts/preview_generator.py [element-id]
    python scripts/preview_generator.py              # regenerate all

Requires: pyyaml, Pillow
    pip install Pillow
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

# Local imports
sys.path.insert(0, str(Path(__file__).parent))
from design_system_utils import DesignSystem, load_registry

SKILL_ROOT = Path(__file__).parent.parent
PREVIEWS   = SKILL_ROOT / "previews"

PREVIEW_SIZES = {
    "atoms":     (320, 200),
    "molecules": (400, 280),
    "templates": (640, 360),
}


def _check_pillow() -> bool:
    try:
        from PIL import Image  # noqa: F401
        return True
    except ImportError:
        print("ERROR: Pillow not installed. Run: pip install Pillow", file=sys.stderr)
        return False


def generate_preview(element_id: str, section: str, ds: DesignSystem) -> Path | None:
    """Generate a placeholder PNG thumbnail for one element."""
    if not _check_pillow():
        return None

    from PIL import Image, ImageDraw, ImageFont

    size = PREVIEW_SIZES.get(section, (320, 200))
    out_dir = PREVIEWS / section
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{element_id}.png"

    # Colors from active theme
    bg_hex      = ds.color("surface")
    border_hex  = ds.color("neutral")
    text_hex    = ds.color("on-surface")
    accent_hex  = ds.color("primary")

    def hex_to_rgb(h: str) -> tuple[int, int, int]:
        h = h.lstrip("#")
        if len(h) == 3:
            h = h[0]*2 + h[1]*2 + h[2]*2
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    img  = Image.new("RGB", size, hex_to_rgb(bg_hex))
    draw = ImageDraw.Draw(img)

    # Border
    draw.rectangle([1, 1, size[0]-2, size[1]-2], outline=hex_to_rgb(border_hex), width=1)

    # Accent top bar (10px)
    draw.rectangle([0, 0, size[0]-1, 9], fill=hex_to_rgb(accent_hex))

    # Element ID text
    try:
        # Try to use a nicer font; fall back to default if unavailable
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except (IOError, OSError):
        font = ImageFont.load_default()
        small_font = font

    # Center the element ID
    text_w = draw.textlength(element_id, font=font)
    x = (size[0] - text_w) / 2
    y = (size[1] - 40) / 2
    draw.text((x, y), element_id, fill=hex_to_rgb(text_hex), font=font)

    # Section label
    section_label = section.upper()
    label_w = draw.textlength(section_label, font=small_font)
    draw.text(((size[0] - label_w) / 2, y + 28), section_label,
              fill=hex_to_rgb(border_hex), font=small_font)

    img.save(str(out_path))
    return out_path


def generate_all(ds: DesignSystem) -> None:
    registry = load_registry()
    section_map = {
        "atoms":     "atoms",
        "molecules": "molecules",
        "templates": "templates",
    }
    total = 0
    for section, folder in section_map.items():
        for entry in registry.get(section, []):
            element_id = entry.get("id", "?")
            out = generate_preview(element_id, folder, ds)
            if out:
                print(f"  Generated: {out.relative_to(SKILL_ROOT)}")
                total += 1
    print(f"\n{total} preview(s) generated in {PREVIEWS.relative_to(SKILL_ROOT)}/")


def generate_one(element_id: str, ds: DesignSystem) -> None:
    registry = load_registry()
    for section in ("atoms", "molecules", "templates"):
        for entry in registry.get(section, []):
            if entry.get("id") == element_id:
                out = generate_preview(element_id, section, ds)
                if out:
                    print(f"Generated: {out}")
                return
    print(f"ERROR: element '{element_id}' not found in registry", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate preview thumbnails")
    parser.add_argument("element_id", nargs="?", default=None,
                        help="Element ID to regenerate (omit to regenerate all)")
    parser.add_argument("--design-config", default=None,
                        help="Path to design-config.yaml (defaults to neutral theme)")
    args = parser.parse_args()

    cfg = Path(args.design_config) if args.design_config else None
    ds  = DesignSystem.load(cfg)

    if args.element_id:
        generate_one(args.element_id, ds)
    else:
        generate_all(ds)
