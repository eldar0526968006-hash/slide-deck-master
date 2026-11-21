from PIL import Image, ImageDraw, ImageFilter
import numpy as np
N=512; R=112
im1=Image.open('images/1.png').convert('RGB'); im2=Image.open('images/2.png').convert('RGB')
def rr(color, border=None):
    t=Image.new('RGBA',(N,N),(0,0,0,0)); d=ImageDraw.Draw(t)
    d.rounded_rectangle((0,0,N-1,N-1),R,fill=color, outline=border, width=4 if border else 0); return t
def sharpen(a):  # crisp up an upscaled alpha
    a=np.clip((a-0.18)/0.64,0,1); return a*a*(3-2*a)
def glyph(crop, mode, scale):
    a=np.asarray(crop).astype(float); L=a.mean(2)
    edge=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]); bg=np.median(edge,0); bL=bg.mean()
    if mode=='light': al=np.clip((L-bL)/(255-bL),0,1); col=np.ones_like(a)*255
    elif mode=='dark': al=np.clip((bL-L)/bL,0,1); col=np.zeros_like(a)
    else:
        al=np.clip(np.abs(a-bg).max(2)/120,0,1)
        col=np.clip((a-(1-al[...,None])*bg)/np.maximum(al[...,None],1e-3),0,255)
    h,w=L.shape; S=int(N*scale); k=S/max(h,w)
    A=Image.fromarray((al*255).astype('uint8')).resize((int(w*k),int(h*k)),Image.LANCZOS)
    A=Image.fromarray((sharpen(np.asarray(A)/255)*255).astype('uint8'))
    C=Image.fromarray(col.astype('uint8')).resize(A.size,Image.LANCZOS).convert('RGBA'); C.putalpha(A); return C
def comp(tile, g):
    tile.alpha_composite(g,((N-g.width)//2,(N-g.height)//2)); return tile
WHITE=(255,255,255,255); BORDER=(226,211,194,255)
out={}
out['chatgpt']=comp(rr((0,0,0,255)), glyph(im1.crop((352,18,424,90)),'light',.62))
out['grok']=comp(rr((0,0,0,255)), glyph(im1.crop((140,22,214,90)),'light',.62))
out['perplexity']=comp(rr((32,128,141,255) if False else (31,31,31,255)), glyph(im1.crop((44,30,90,78)),'light',.56))
out['claude']=comp(rr((217,119,87,255) if False else (204,155,122,255)), glyph(im1.crop((257,36,302,74)),'dark',.46))
out['gemini']=comp(rr(WHITE,BORDER), glyph(im2.crop((44,6,116,78)),'color',.64))
out['copilot']=comp(rr(WHITE,BORDER), glyph(im2.crop((152,6,222,78)),'color',.64))
el=Image.open('images/4.png').convert('RGB').crop((126,44,186,120)); out['elevenlabs']=comp(rr(WHITE,BORDER), glyph(el,'dark',.42))
qw=Image.open('images/5.png').convert('RGB').crop((78,143,309,372)); out['qwen']=comp(rr(WHITE,BORDER), glyph(qw,'color',.66))
su=Image.open('images/3.webp').convert('RGBA').resize((N,N),Image.LANCZOS)
m=Image.new('L',(N,N),0); ImageDraw.Draw(m).rounded_rectangle((0,0,N-1,N-1),R,fill=255); su.putalpha(m); out['suno']=su
order=['chatgpt','gemini','claude','copilot','perplexity','grok','qwen','suno','elevenlabs']
sheet=Image.new('RGBA',(len(order)*280,300),(255,243,232,255))
for i,k in enumerate(order):
    out[k].save(f'logos/{k}.png'); sheet.alpha_composite(out[k].resize((256,256),Image.LANCZOS),(i*280+12,22))
sheet.save('logos/sheet.png')
def square_tile(img):
    t=img.convert('RGBA').resize((N,N),Image.LANCZOS)
    m=Image.new('L',(N,N),0); ImageDraw.Draw(m).rounded_rectangle((0,0,N-1,N-1),R,fill=255); t.putalpha(m); return t
s6=Image.open('images/6.png'); w,h=s6.size; c=min(w,h); out['spiral']=square_tile(s6.crop(((w-c)//2,(h-c)//2,(w-c)//2+c,(h-c)//2+c)))
s7=Image.open('images/7.png').convert('RGB')
out['seedance']=square_tile(s7.crop((100,104,222,226)))
s8=Image.open('images/8.png'); w,h=s8.size; out['kling']=square_tile(s8.crop((6,6,w-6,h-6)))
order2=['spiral','seedance','kling']
sh=Image.new('RGBA',(3*280,300),(255,243,232,255))
for i,k in enumerate(order2):
    out[k].save(f'logos/{k}.png'); sh.alpha_composite(out[k].resize((256,256),Image.LANCZOS),(i*280+12,22))
sh.save('logos/sheet2.png')
