import zipfile, xml.etree.ElementTree as ET, os

dir_path = r'e:\FPGA\project\FPT\fpt26-harness\doc\这是其它优秀作品，需要你修改我的工程到达他们的水平'
NS = '{http://schemas.openxmlformats.org/drawingml/2006/main}t'

for f in sorted(os.listdir(dir_path)):
    if not f.endswith('.pptx') or f.startswith('~$'):
        continue
    full = os.path.join(dir_path, f)
    print(f'\n===== {f} =====')
    z = zipfile.ZipFile(full)
    slides = [s for s in z.namelist() if s.startswith('ppt/slides/slide') and s.endswith('.xml')]
    slides.sort(key=lambda x: int(x.replace('ppt/slides/slide','').replace('.xml','')))
    for s in slides[:25]:
        xml = z.read(s).decode('utf-8')
        texts = [t.text.strip() for t in ET.fromstring(xml).iter(NS) if t.text]
        line = ' '.join(texts)[:500]
        if line:
            print(f'  {s}: {line}')
    z.close()
