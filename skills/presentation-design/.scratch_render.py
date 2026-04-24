import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from scripts.drawio_svg_renderer import DrawioSvgRenderer
from scripts.exporting.drawio_screenshot_exporter import _svg_to_png
from scripts.parsing.theme_loader import ThemeLoader

deck_dir = Path(r"C:\Users\mschuetten\OneDrive - mhp-group.com\CompetenceCenter\EAM\AI_EAM\ai_eam")
drawio = deck_dir / "output" / "presentation.drawio"
out_dir = deck_dir / "output" / "qa" / "drawio"
out_dir.mkdir(parents=True, exist_ok=True)
base_css = Path(__file__).parent / "themes" / "base.css"
deck_css = deck_dir / "theme.css"
loader = ThemeLoader()
theme = loader.load(base_css, deck_css)
import xml.etree.ElementTree as ET
tree = ET.parse(drawio); root = tree.getroot()
pages = [diag.get("name", "") for diag in root.iter("diagram")]
print(f"Total: {len(pages)}")
for idx in [int(a) for a in sys.argv[1:]]:
    name = pages[idx-1]
    safe = name.replace(" ", "_").replace("/", "_").replace(":", "")[:80]
    png = out_dir / f"slide-{idx:03d}-{safe}.png"
    renderer = DrawioSvgRenderer()
    mxg = renderer.extract_page(drawio, name)
    svg = renderer.render_to_svg(mxg, 1920, 1080)
    _svg_to_png(svg, png, 1920, 1080)
    print(f"  -> {png}")
