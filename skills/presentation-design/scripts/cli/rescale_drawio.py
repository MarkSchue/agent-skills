"""
rescale_drawio.py  —  Transform a draw.io file to a new canvas size.

Usage:
    python rescale_drawio.py INPUT.drawio OUTPUT.drawio \
        --new-width 2304 --new-height 718 \
        [--strip-ids title_bg title_txt subtitle_txt]

Each page's mxGeometry is rescaled so that the old content area maps
linearly onto the new canvas.  Optionally, cells can be removed by id.

The old content area is determined by the old pageWidth / pageHeight;
if --old-content-y-start is given (e.g. 60 to skip a title bar in the
source design), y coordinates are shifted before scaling so that the
first content pixel maps to y=0 in the output.
"""

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input",  type=Path, help="Source .drawio file")
    p.add_argument("output", type=Path, help="Destination .drawio file")
    p.add_argument("--new-width",  type=float, required=True)
    p.add_argument("--new-height", type=float, required=True)
    p.add_argument("--old-content-y-start", type=float, default=0.0,
                   help="Y coordinate in the old design where real content begins "
                        "(everything above is treated as a title bar and stripped).")
    p.add_argument("--strip-ids", nargs="*", default=[],
                   help="Cell ids to remove from output (e.g. title_bg title_txt).")
    return p.parse_args()


def rescale_page(diagram_el: ET.Element,
                 new_w: float, new_h: float,
                 y_start: float,
                 strip_ids: set[str]) -> None:
    """Mutate a <diagram> element in-place."""
    model = diagram_el.find("mxGraphModel")
    if model is None:
        return

    old_w = float(model.get("pageWidth",  1280))
    old_h = float(model.get("pageHeight", 648))

    content_h = old_h - y_start          # height of content to map
    x_scale = new_w / old_w
    y_scale = new_h / content_h if content_h > 0 else 1.0

    # Update model-level attributes
    model.set("dx",         str(int(new_w)))
    model.set("dy",         str(int(new_h)))
    model.set("pageWidth",  str(int(new_w)))
    model.set("pageHeight", str(int(new_h)))

    root_el = model.find("root")
    if root_el is None:
        return

    to_remove: list[ET.Element] = []
    for cell in list(root_el):
        cell_id = cell.get("id", "")

        # Remove unwanted cells
        if cell_id in strip_ids:
            to_remove.append(cell)
            continue

        geo = cell.find("mxGeometry")
        if geo is None:
            continue

        # Read current geometry
        ox = float(geo.get("x", 0))
        oy = float(geo.get("y", 0))
        ow = float(geo.get("width",  0))
        oh = float(geo.get("height", 0))

        # Skip cells entirely above the content start
        if oy + oh <= y_start:
            to_remove.append(cell)
            continue

        # Clip cells that straddle y_start to start at y_start
        if oy < y_start:
            clip = y_start - oy
            oy  = y_start
            oh -= clip

        # Apply transform
        nx = round(ox * x_scale, 1)
        ny = round((oy - y_start) * y_scale, 1)
        nw = round(ow * x_scale, 1)
        nh = round(oh * y_scale, 1)

        # Clamp to canvas
        ny = max(0.0, ny)
        nh = min(nh, new_h - ny)

        geo.set("x",      str(nx))
        geo.set("y",      str(ny))
        geo.set("width",  str(nw))
        geo.set("height", str(nh))

    for cell in to_remove:
        root_el.remove(cell)


def main() -> None:
    args = parse_args()
    strip = set(args.strip_ids)

    tree = ET.parse(args.input)
    root = tree.getroot()

    for diagram in root.findall("diagram"):
        rescale_page(
            diagram,
            new_w=args.new_width,
            new_h=args.new_height,
            y_start=args.old_content_y_start,
            strip_ids=strip,
        )

    # Write with xml declaration and pretty-ish indentation
    ET.indent(tree, space="  ")
    tree.write(
        args.output,
        encoding="unicode",
        xml_declaration=False,
    )
    print(f"Written: {args.output}  ({int(args.new_width)}×{int(args.new_height)})")


if __name__ == "__main__":
    main()
