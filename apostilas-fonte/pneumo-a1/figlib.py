from PIL import ImageFont
import html
R='/usr/share/fonts/opentype/inter/Inter-Regular.otf'
S='/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
B='/usr/share/fonts/opentype/inter/Inter-Bold.otf'
_c={}
def font(p,sz):
    k=(p,sz)
    if k not in _c: _c[k]=ImageFont.truetype(p,int(sz*20))
    return _c[k]
def tw(t,p,sz): return font(p,sz).getlength(t)/20
def wrap(t,p,sz,maxw):
    out=[];cur=''
    for w in t.split(' '):
        c=(cur+' '+w).strip()
        if tw(c,p,sz)<=maxw or not cur: cur=c
        else: out.append(cur);cur=w
    if cur: out.append(cur)
    return out
INK='#1F2933';NAVY='#16315C';BLUE='#0B5BD3';LINE='#C3D8F8';SOFT='#F5F8FF';ARR='#8AA9DF'
def esc(t): return html.escape(t,quote=False)
def text(x,y,t,sz,w=400,fill=INK,anchor='middle'):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter" font-size="{sz}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}">{esc(t)}</text>'
def arrow(x1,y1,x2,y2,head=5):
    # reta horizontal ou vertical, ponta como polígono
    import math
    dx,dy=x2-x1,y2-y1;L=math.hypot(dx,dy);ux,uy=dx/L,dy/L
    bx,by=x2-ux*head,y2-uy*head
    px,py=-uy,ux
    s=f'<path d="M{x1:.1f} {y1:.1f}L{bx+ux*0.5:.1f} {by+uy*0.5:.1f}" stroke="{ARR}" stroke-width="1.3" fill="none"/>'
    s+=f'<polygon points="{x2:.1f},{y2:.1f} {bx+px*head*0.62:.1f},{by+py*head*0.62:.1f} {bx-px*head*0.62:.1f},{by-py*head*0.62:.1f}" fill="{ARR}"/>'
    return s
def line(pts):
    d='M'+'L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)
    return f'<path d="{d}" stroke="{ARR}" stroke-width="1.3" fill="none" stroke-linejoin="round"/>'
def rect(x,y,w,h,fill='#FFFFFF',stroke=LINE,r=7,dash=False,sw=1.1):
    d=' stroke-dasharray="3 2.4"' if dash else ''
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'
def seal(cx,cy,n):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="7" fill="{BLUE}"/>'+text(cx,cy+2.9,str(n),8,600,'#FFFFFF'))
class Box:
    def __init__(s,title,body='',w=100,tsz=7.8,bsz=7,seal=None,fill='#FFFFFF',stroke=LINE,dash=False,pad=7,sealpad=0,tcol=NAVY,tw_=600):
        s.title,s.body,s.w,s.tsz,s.bsz,s.seal,s.fill,s.stroke,s.dash,s.pad=title,body,w,tsz,bsz,seal,fill,stroke,dash,pad
        s.sealpad=sealpad;s.tcol=tcol;s.tw_=tw_
        iw=w-2*pad-sealpad
        s.tl=wrap(title,S if tw_>=600 else R,tsz,iw) if title else []
        s.bl=wrap(body,R,bsz,iw) if body else []
        s.th=len(s.tl)*tsz*1.22;s.bh=len(s.bl)*bsz*1.28
        s.h=s.th+s.bh+(3 if s.tl and s.bl else 0)+2*7
    def draw(s,x,y,h=None):
        h=h or s.h
        o=rect(x,y,s.w,h,s.fill,s.stroke,dash=s.dash)
        cx=x+s.w/2+s.sealpad/2
        cy=y+(h-(s.th+s.bh+(3 if s.tl and s.bl else 0)))/2
        for l in s.tl:
            cy+=s.tsz*0.98; o+=text(cx,cy,l,s.tsz,s.tw_,s.tcol); cy+=s.tsz*0.24
        if s.tl and s.bl: cy+=3
        for l in s.bl:
            cy+=s.bsz*1.0; o+=text(cx,cy,l,s.bsz,400,INK); cy+=s.bsz*0.28
        if s.seal: o+=seal(x+pad_seal(s),y+h/2,s.seal)
        return o
def pad_seal(b): return 6+7+1
def svg(w,h,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}pt" height="{h:.1f}pt" viewBox="0 0 {w} {h:.1f}">{body}</svg>'
