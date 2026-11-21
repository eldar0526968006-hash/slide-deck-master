import re, sys
from pptx import Presentation
from pptx.util import Pt, Emu
from lxml import etree
from PIL import ImageFont
SRC, OUT, ICONS = sys.argv[1], sys.argv[2], sys.argv[3]
P = 12700
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
HEB = re.compile('[֐-׿]')
DARK = '170C14'
DARKS = {'140B12', '21101C'}
FONT = '/root/.fonts/Heebo[wght].ttf'
def tw(text, pt, bold):
    f = ImageFont.truetype(FONT, int(pt * 4)); f.set_variation_by_name('Bold' if bold else 'Regular')
    return f.getlength(text.replace('‏', '').replace('‎', '')) / 4
prs = Presentation(SRC)
def pt(v): return v / P
def txt(sh): return sh.text_frame.text if sh.has_text_frame else ''
def is_num(sh): return sh.has_text_frame and re.fullmatch(r'\d+', txt(sh).strip() or 'x') and pt(sh.top) > 500
def pill(sh):
    x = sh._element.xml
    return sh.has_text_frame and txt(sh).strip() and 'prst="roundRect"' in x and 'val 50000' in x
def icon(slide, name, dark, cx, top, size):
    return slide.shapes.add_picture(f'{ICONS}/{name}-{"dark" if dark else "light"}.png',
        Emu(int((cx - size/2)*P)), Emu(int(top*P)), Emu(int(size*P)), Emu(int(size*P)))
def setx(sh, x=None, y=None, w=None, h=None):
    if x is not None: sh.left = Emu(int(x*P))
    if y is not None: sh.top = Emu(int(y*P))
    if w is not None: sh.width = Emu(int(w*P))
    if h is not None: sh.height = Emu(int(h*P))
def center_x(sh): setx(sh, x=480 - pt(sh.width)/2)

for n, s in enumerate(prs.slides, 1):
    el = s._element
    bg = el.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}bg')
    bgc = bg.find(f'.//{A}srgbClr').get('val') if bg is not None and bg.find(f'.//{A}srgbClr') is not None else None
    dark = bgc in DARKS or n == 1
    # 1. colours
    for c in el.iter(f'{A}srgbClr'):
        v = c.get('val')
        if v in DARKS: v = DARK
        elif dark and v in {'5A4E43', '6B5C4E', '7A6D60', '9C8F80'}: v = 'A89A8B'
        elif dark and v == 'DCC6AE': v = 'CFC3B4'
        elif not dark and v == '6B5C4E': v = '5A4E43'
        elif not dark and v in {'9C8F80', 'A89A8B'} and bgc == 'FFF3E8': v = '7A6D60'
        c.set('val', v)
    # 2. runs / paragraphs
    for p in el.iter(f'{A}p'):
        t = ''.join(x.text or '' for x in p.iter(f'{A}t'))
        if HEB.search(t):
            ppr = p.find(f'{A}pPr')
            if ppr is None: ppr = etree.SubElement(p, f'{A}pPr'); p.insert(0, ppr)
            ppr.set('rtl', '1')
        for r in p.findall(f'{A}r'):
            rpr = r.find(f'{A}rPr'); rt = r.findtext(f'{A}t') or ''
            if rpr is None: continue
            if rpr.get('sz') and int(rpr.get('sz')) < 1200: rpr.set('sz', '1200')
            lat = rpr.find(f'{A}latin')
            if lat is not None and lat.get('typeface') == 'Anton' and HEB.search(rt):
                for tag in ('latin', 'ea', 'cs'):
                    e = rpr.find(f'{A}{tag}')
                    if e is not None: e.set('typeface', 'Karantina')
                rpr.set('b', '1'); rpr.set('sz', str(int(int(rpr.get('sz')) * 1.3)))
    # 3. pills: one height + one padding per size class, rows re-centred
    rows = {}
    for sh in s.shapes:
        if pill(sh):
            r0 = sh.text_frame.paragraphs[0].runs[0]
            sz = r0.font.size.pt if r0.font.size else 18
            if sz < 16:  # stray small pill (slide 12) -> standard
                for r in sh.text_frame.paragraphs[0].runs: r.font.size = Pt(18)
                sz = 18
            rows.setdefault(round(pt(sh.top + sh.height/2) / 6), []).append((sh, sz, bool(r0.font.bold)))
    for key, items in rows.items():
        cy = sum(pt(sh.top + sh.height/2) for sh, _, _ in items) / len(items)
        H = 40 if max(i[1] for i in items) >= 18 else 34
        for sh, sz, b in items:
            w = tw(txt(sh), sz, b) + 2 * (20 if H == 40 else 16)
            ccx = pt(sh.left + sh.width/2)
            setx(sh, w=w, h=H, y=cy - H/2, x=ccx - w/2)
        items.sort(key=lambda i: i[0].left)
        gaps=[pt(b[0].left)-pt(a[0].left+a[0].width) for a,b in zip(items,items[1:])]
        if n != 12 and len(items) > 1 and max(gaps) < 40:  # only true pill rows; labels in separate cards stay put
            gap = 10; total = sum(pt(i[0].width) for i in items) + gap*(len(items)-1)
            x = 480 - total/2
            for sh, _, _ in items: setx(sh, x=x); x += pt(sh.width) + gap
    shapes = list(s.shapes)
    T = lambda pat: [sh for sh in shapes if sh.has_text_frame and re.search(pat, txt(sh))]
    # 4. slide-specific
    if n == 7:
        sh = T('מסנן')[0]
        for p in sh.text_frame.paragraphs: p._p.find(f'{A}pPr').set('algn', 'ctr')
        center_x(sh)
    if n == 10:
        for sh in T('^0'): setx(sh, y=pt(sh.top) + 22)
    if n == 20:
        sh = T('לא הצליחו')[0]; setx(sh, w=660); center_x(sh)
    if n == 21:
        sh = T('במחקר של MIT')[0]; setx(sh, w=560, h=70); center_x(sh)
    if n == 16:
        setx(T('ההבדל')[0], y=345)
    if n == 31:
        for sh in T('תודה'):
            for r in sh.text_frame.paragraphs[0].runs:
                r.text = re.sub(r'\s*·\s*(‏)?\s*$', r'\1', r.text)
    if n == 17:
        cards = sorted([sh for sh in shapes if not sh.has_text_frame or not txt(sh).strip()
                        if pt(sh.width) > 200], key=lambda c: c.left)
        for card, ic in zip(cards, ['spark', 'nav', 'phone']):
            cx0, cx1 = pt(card.left), pt(card.left + card.width)
            inner = sorted([sh for sh in shapes if sh.has_text_frame and txt(sh).strip()
                            and cx0 < pt(sh.left + sh.width/2) < cx1 and 170 < pt(sh.top) < 470], key=lambda q: q.top)
            T0 = 168
            icon(s, ic, False, (cx0+cx1)/2, T0 + 24, 34)
            name, giv, v1, took, v2 = inner
            for sh, y in ((name, T0+64), (giv, T0+120), (v1, T0+144), (took, T0+180), (v2, T0+204)):
                if txt(sh).strip() == '?':
                    for r in sh.text_frame.paragraphs[0].runs: r.font.size = Pt(30)
                    ls = sh.text_frame.paragraphs[0]._p.find(f'{A}pPr/{A}lnSpc')
                    if ls is not None: ls.getparent().remove(ls)
                    setx(sh, y=y-4, h=34)
                else: setx(sh, y=y)
            setx(card, y=T0, h=244)
    if n == 23:
        for letter, ic in (('א', 'userplus'), ('ב', 'flag'), ('ג', 'home')):
            sh = [q for q in shapes if q.has_text_frame and txt(q).strip() == letter][0]
            icon(s, ic, True, pt(sh.left + sh.width/2), pt(sh.top) + 4, 40)
            sh._element.getparent().remove(sh._element)
    if n == 24:
        cards = [sh for sh in shapes if (not sh.has_text_frame or not txt(sh).strip()) and 100 < pt(sh.width) < 130]
        mapping = {'1': 'grid', '2': 'check', '3': 'chat', '4': 'hammer', '5': 'easel', '6': 'pen'}
        for card in cards:
            cx0, cx1 = pt(card.left), pt(card.left + card.width)
            inner = [sh for sh in shapes if sh is not card and cx0 <= pt(sh.left) and pt(sh.left + sh.width) <= cx1 and 200 < pt(sh.top) < 380]
            num = [sh for sh in inner if sh.has_text_frame and re.fullmatch(r'\d', txt(sh).strip())][0]
            for sh in inner: setx(sh, y=pt(sh.top) + 36)
            setx(card, y=pt(card.top) - 6, h=pt(card.height) + 42)
            icon(s, mapping[txt(num).strip()], False, (cx0+cx1)/2, pt(card.top) + 16, 28)
        setx(T('מתחיל בכם')[0], y=446)
    # 5. vertical balance: centre the content block between 24pt and 500pt
    if n not in (1, 2, 12):
        body = [sh for sh in s.shapes if not is_num(sh) and not (pt(sh.width) >= 950 and pt(sh.height) >= 500)
                and not (pt(sh.top) > 470 and pt(sh.height) < 24)]  # footer source lines stay anchored
        top = min(pt(sh.top) for sh in body); bot = max(pt(sh.top + sh.height) for sh in body)
        d = 272 - (top + bot)/2
        if abs(d) > 6:
            for sh in body: setx(sh, y=pt(sh.top) + d)
prs.save(OUT)
print('saved', OUT)
