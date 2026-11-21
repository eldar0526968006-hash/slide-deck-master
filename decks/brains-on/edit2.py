"""Round 2: drop slides 16/19/33, logos on 22, thank-you slide before sources, renumber."""
import re, sys, copy
from pptx import Presentation
from pptx.util import Pt, Emu
from lxml import etree
SRC, OUT, ICONS, LOGOS = sys.argv[1:5]
P = 12700; A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
prs = Presentation(SRC)
S = list(prs.slides)
def pt(v): return v / P
def txt(sh): return sh.text_frame.text if sh.has_text_frame else ''
def setx(sh, x=None, y=None, w=None, h=None):
    for k, v in (('left', x), ('top', y), ('width', w), ('height', h)):
        if v is not None: setattr(sh, k, Emu(int(v * P)))
def is_num(sh): return sh.has_text_frame and re.fullmatch(r'\d+', txt(sh).strip() or 'x') and pt(sh.top) > 500
def balance(s, target=272):
    body = [sh for sh in s.shapes if not is_num(sh) and not (pt(sh.top) > 470 and pt(sh.height) < 24)]
    top = min(pt(sh.top) for sh in body); bot = max(pt(sh.top + sh.height) for sh in body)
    d = target - (top + bot) / 2
    for sh in body: setx(sh, y=pt(sh.top) + d)
def textbox(s, text, x, y, w, h, font, sz, color, bold=False):
    tb = s.shapes.add_textbox(Emu(int(x*P)), Emu(int(y*P)), Emu(int(w*P)), Emu(int(h*P)))
    tf = tb.text_frame; tf.word_wrap = True
    for side in ('margin_left', 'margin_right', 'margin_top', 'margin_bottom'): setattr(tf, side, 0)
    p = tf.paragraphs[0]; ppr = p._p.get_or_add_pPr(); ppr.set('algn', 'ctr')
    if re.search('[֐-׿]', text): ppr.set('rtl', '1')
    r = p.add_run(); r.text = text; f = r.font; f.size = Pt(sz); f.bold = bold; f.name = font
    from pptx.dml.color import RGBColor; f.color.rgb = RGBColor.from_string(color)
    rpr = r._r.get_or_add_rPr()
    for tag in ('ea', 'cs'):
        e = etree.SubElement(rpr, f'{A}{tag}'); e.set('typeface', font)
    return tb

# --- slide 22: AI logos scattered around the title (seeded random, no overlaps) ---
import random, math
s22 = S[21]
title = [sh for sh in s22.shapes if 'כלי' in txt(sh)][0]
setx(title, y=262 - pt(title.height)/2)
order = ['chatgpt', 'gemini', 'claude', 'copilot', 'perplexity', 'grok',
         'qwen', 'suno', 'elevenlabs', 'kling', 'seedance', 'spiral']
TB = (175, 205, 785, 320)  # title glyph box, kept clear
def ok(b, placed):
    x0, y0, x1, y1 = b
    if x0 < 30 or x1 > 930 or y0 < 22 or y1 > 498: return False
    if not (x1 + 14 < TB[0] or x0 - 14 > TB[2] or y1 + 10 < TB[1] or y0 - 10 > TB[3]): return False
    return all(x1 + 16 < p[0] or x0 - 16 > p[2] or y1 + 16 < p[1] or y0 - 16 > p[3] for p in placed)
best = None
for seed in range(400):
    rnd = random.Random(seed); placed = []; slots = list(range(12)); rnd.shuffle(slots)
    for i, k in enumerate(order):
        for _ in range(60):
            ang = (slots[i] + 0.5) / 12 * 2 * math.pi + rnd.uniform(-0.17, 0.17)
            rx, ry = rnd.uniform(370, 425), rnd.uniform(185, 225)
            size = rnd.uniform(66, 88)
            cx, cy = 480 + rx * math.cos(ang), 262 + ry * math.sin(ang)
            b = (cx - size/2, cy - size/2, cx + size/2, cy + size/2)
            if ok(b, placed): placed.append(b); break
        else: break
    if len(placed) == 12:
        sizes = [p[2] - p[0] for p in placed]
        score = max(sizes) - min(sizes)  # prefer a calm spread of sizes
        if best is None or score < best[0]: best = (score, seed, placed)
_, seed, placed = best
rnd = random.Random(seed * 7 + 1)
for k, b in zip(order, placed):
    pic = s22.shapes.add_picture(f'{LOGOS}/{k}.png', Emu(int(b[0]*P)), Emu(int(b[1]*P)), Emu(int((b[2]-b[0])*P)), Emu(int((b[3]-b[1])*P)))
    pic.rotation = rnd.uniform(-9, 9)
print('logo seed', seed)

# --- slide 31: names move to the thank-you slide ---
s31 = S[30]
for sh in list(s31.shapes):
    if 'תודה' in txt(sh): sh._element.getparent().remove(sh._element)
balance(s31)

# --- new thank-you slide (orange bookend, mirrors slide 11) ---
s11 = S[10]
ty = prs.slides.add_slide(s11.slide_layout)
for ph in list(ty.placeholders): ph._element.getparent().remove(ph._element)
ty._element.cSld.insert(0, copy.deepcopy(s11._element.cSld.bg))
ty.shapes.add_picture(f'{ICONS}/smile-ink.png', Emu(int(430*P)), Emu(int(118*P)), Emu(int(100*P)), Emu(int(100*P)))
textbox(ty, 'תודה רבה', 80, 232, 800, 130, 'Karantina', 130, '1E130F', bold=True)
textbox(ty, 'אלדר ביכלר ועידו פינקלשטיין', 180, 398, 600, 34, 'Heebo', 24, '1E130F')
num11 = [sh for sh in s11.shapes if is_num(sh)][0]
ty.shapes._spTree.append(copy.deepcopy(num11._element))
ty.notes_slide.notes_text_frame.text = ('תודה רבה. מי שרוצה לבדוק לבד: בשקף הבא כל המקורות. '
                                        'שאלות?')

# --- reorder: thank-you before sources (old 32), then drop 16, 19, 33 ---
lst = prs.slides._sldIdLst; ids = list(lst)
new = ids[-1]; lst.remove(new); lst.insert(31, new)  # before old slide 32
for old in (33, 19, 16):
    sid = ids[old - 1]
    prs.part.drop_rel(sid.rId); lst.remove(sid)

# --- renumber ---
for i, s in enumerate(prs.slides, 1):
    for sh in s.shapes:
        if is_num(sh):
            runs = sh.text_frame.paragraphs[0].runs
            runs[0].text = str(i)
            for r in runs[1:]: r.text = ''
prs.save(OUT); print('slides:', len(prs.slides))
