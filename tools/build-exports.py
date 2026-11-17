"""Build <name>.pptx (slide images + speaker notes) and <name>.pdf from slide PNGs.
Usage: python3 tools/build-exports.py <deck.html> <pngdir> <outbase>"""
import html, re, sys, glob
from pptx import Presentation
from pptx.util import Emu
from PIL import Image

deck, pngdir, out = sys.argv[1:4]
src = open(deck, encoding='utf-8').read()
notes = [html.unescape(re.sub(r'<[^>]+>', '', n)).strip()
         for n in re.findall(r'<aside class="notes">(.*?)</aside>', src, re.S)]
pngs = sorted(glob.glob(f'{pngdir}/s*.png'))
if not pngs:
    sys.exit('no slide screenshots found')
prs = Presentation(); prs.slide_width = Emu(12192000); prs.slide_height = Emu(6858000)
imgs = []
for i, f in enumerate(pngs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.shapes.add_picture(f, 0, 0, prs.slide_width, prs.slide_height)
    if i < len(notes):
        s.notes_slide.notes_text_frame.text = notes[i]
    imgs.append(Image.open(f).convert('RGB'))
prs.save(out + '.pptx')
imgs[0].save(out + '.pdf', save_all=True, append_images=imgs[1:], resolution=144)
print(f'{len(pngs)} slides -> {out}.pptx, {out}.pdf')
