import xml.etree.ElementTree as ET

path = "C:/Users/mschuetten/OneDrive - mhp-group.com/CompetenceCenter/EAM/AI_EAM/ai_eam/output/presentation.drawio"
tree = ET.parse(path)
root = tree.getroot()

for i, d in enumerate(root.findall("diagram")):
    print(f"{i}: {d.get('name')}")

print()

# Page 7: Strategic Layer
page7 = root.findall("diagram")[7]
print(f"Page 7: {page7.get('name')}")
mx_root = page7.find("mxGraphModel/root")
for cell in mx_root.findall("mxCell"):
    geo = cell.find("mxGeometry")
    if geo is not None and geo.get("width"):
        val = (cell.get("value","") or "")[:40]
        style = (cell.get("style","") or "")[:45]
        print(f"  id={cell.get('id')} x={geo.get('x')} y={geo.get('y')} w={geo.get('width')} h={geo.get('height')} val='{val}' style='{style}'")
