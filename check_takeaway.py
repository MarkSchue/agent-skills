import xml.etree.ElementTree as ET

tree = ET.parse(r'C:\Users\mschuetten\OneDrive - mhp-group.com\ThyssenKrupp\tkSE\Anomalie\Anomalie Auswertung\output\presentation.drawio')
root = tree.getroot()

for cell in root.iter('mxCell'):
    val = cell.get('value', '')
    if 'Kombination' in val:
        geo = cell.find('mxGeometry')
        print('VALUE:', repr(val[:200]))
        print('STYLE:', cell.get('style','')[:200])
        if geo is not None:
            print('GEO: y={} h={} w={}'.format(geo.get('y'), geo.get('height'), geo.get('width')))


