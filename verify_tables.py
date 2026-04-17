import zipfile, re

pptx = r"C:\Users\mschuetten\OneDrive - mhp-group.com\Workspace\lapp_derisking\slides\decoupling\output\presentation.pptx"
with zipfile.ZipFile(pptx) as z:
    slides = sorted(
        [f for f in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", f)],
        key=lambda s: int(re.search(r"\d+", s).group())
    )
    print("Total slides:", len(slides))

    # Check bullet chars
    for sname in slides:
        xml = z.read(sname).decode()
        chars = re.findall(r'buChar char="(.+?)"', xml)
        if chars:
            print(sname, "bullet chars:", list(set(chars)))
            break

    # Show row distributions for all slides with tables
    for sname in slides:
        xml = z.read(sname).decode()
        rows = [int(x) // 9525 for x in re.findall(r"<a:tr h=\"([0-9]+)\"", xml)]
        if rows:
            print(f"{sname}: rows={rows}  total={sum(rows)}px")
