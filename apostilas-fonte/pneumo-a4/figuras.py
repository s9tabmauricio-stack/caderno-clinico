import subprocess, html
from PIL import ImageFont
R=subprocess.check_output(['fc-match','-f','%{file}','Inter:weight=regular']).decode()
S=subprocess.check_output(['fc-match','-f','%{file}','Inter:weight=600']).decode()
def F(b,s): return ImageFont.truetype(S if b else R, s)
def wrap(t,b,s,w):
    f=F(b,s); out=[];cur=''
    for p in t.split(' '):
        n=(cur+' '+p).strip()
        if f.getlength(n)<=w or not cur: cur=n
        else: out.append(cur);cur=p
    out.append(cur); return out
W=478
class Svg:
    def __init__(s):s.e=[]
    def box(s,x,y,w,h,fill='#FFFFFF',stroke='#C3D8F8',dash=False,rx=9,sw=1.1):
        d=' stroke-dasharray="3 2.5"' if dash else ''
        s.e.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def text(s,x,y,t,b=False,sz=8.5,col='#1F2933',anchor='middle'):
        fam='Inter SemiBold' if b else 'Inter'
        s.e.append(f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{sz}" fill="{col}" text-anchor="{anchor}">{html.escape(t)}</text>')
    def para(s,x,y,t,b,sz,col,w,lh,anchor='middle'):
        for l in wrap(t,b,sz,w):
            s.text(x,y,l,b,sz,col,anchor); y+=lh
        return y
    def line(s,x1,y1,x2,y2,col='#0B5BD3',w=1.6):
        s.e.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}"/>')
    def arrow(s,x1,y1,x2,y2,col='#8AA9DF'):
        import math
        a=math.atan2(y2-y1,x2-x1); L=5.5; hw=3.2
        bx,by=x2-L*math.cos(a),y2-L*math.sin(a)
        s.line(x1,y1,bx,by,col,1.5)
        px,py=-math.sin(a)*hw,math.cos(a)*hw
        s.e.append(f'<polygon points="{x2},{y2} {bx+px},{by+py} {bx-px},{by-py}" fill="{col}"/>')
    def save(s,fn,h):
        open(fn,'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{h}pt" viewBox="0 0 {W} {h}">'+''.join(s.e)+'</svg>')

def cbox(s,x,y,w,h,title,sub,fill='#FFFFFF',stroke='#C3D8F8',dash=False,tcol='#16315C',tsz=9.4,ssz=7.6,scol='#4A4A4F'):
    s.box(x,y,w,h,fill,stroke,dash)
    tl=wrap(title,True,tsz,w-14); sl=wrap(sub,False,ssz,w-14) if sub else []
    th=len(tl)*tsz*1.25+len(sl)*ssz*1.3
    yy=y+(h-th)/2+tsz*1.0
    for l in tl: s.text(x+w/2,yy,l,True,tsz,tcol); yy+=tsz*1.25
    yy+=ssz*0.1
    for l in sl: s.text(x+w/2,yy,l,False,ssz,scol); yy+=ssz*1.3

# ---- linha do tempo
s=Svg(); 
X0,X1=8,470
s.text(X0,13,'Contando desde a internação',True,8.4,'#16315C','start')
# eixo de 0 a 462: 48h em 130; 5º dia em 300
a,b=8+0,8+170; c=8+320
y=22;h=40
s.box(a+2,y,b-a-6,h,'#F5F8FF','#C3D8F8',True); 
def two(x,w,t,sub,yy,hh,**k): cbox(s,x,yy,w,hh,t,sub,**k)
cbox(s,a+2,y,b-a-6,h,'Comunitária','provavelmente já internou com ela','#F5F8FF','#C3D8F8',True)
cbox(s,b+3,y,c-b-6,h,'Hospitalar precoce','até o 4º dia de internação','#E8F0FE')
cbox(s,c+3,y,X1-c-3,h,'Hospitalar tardia','a partir do 5º dia de internação','#E8F0FE')
for x in (a,b,c): s.line(x,y,x,y+h+2,'#0B5BD3',1.6)
s.text(a+3,y+h+14,'internação',False,7.8,'#0B5BD3','start')
s.text(b+3,y+h+14,'48 horas',False,7.8,'#0B5BD3','start')
s.text(c+3,y+h+14,'5º dia',False,7.8,'#0B5BD3','start')
y2=y+h+34
s.text(X0,y2,'Contando desde a intubação',True,8.4,'#16315C','start')
y2+=9;h2=50
cbox(s,a+2,y2,b-a-6,h2,'Ainda não é associada à ventilação','é comunitária ou hospitalar, conforme a internação','#F5F8FF','#C3D8F8',True,tsz=8.8,ssz=7.2)
cbox(s,b+3,y2,X1-b-3,h2,'Pneumonia associada à ventilação mecânica','o quadro começou com o paciente intubado há pelo menos 48 horas','#E8F0FE')
for x in (a,b): s.line(x,y2,x,y2+h2+2,'#0B5BD3',1.6)
s.text(a+3,y2+h2+14,'intubação orotraqueal',False,7.8,'#0B5BD3','start')
s.text(b+3,y2+h2+14,'48 horas',False,7.8,'#0B5BD3','start')
s.save('tempo.svg',int(y2+h2+22))

# ---- algoritmo
s=Svg(); cw=228; gx=22
cols=[(0,'Bacilos gram-negativos','Pseudomonas, Klebsiella, E. coli, Acinetobacter',
 'Algum fator de risco da lista do tipo de pneumonia? Na associada à ventilação, também: resistência local acima de 10% ou desconhecida.',
 ('Duas drogas','sem juntar dois betalactâmicos (sinergismo)'),('Uma droga','que também cubra o estafilococo sensível')),
 (cw+gx,'Cocos gram-positivos','Staphylococcus aureus (estafilococo)',
 'Estafilococo resistente à oxacilina acima do corte, ou taxa desconhecida? Hospitalar: 20%. Associada à ventilação: 10 a 20%.',
 ('Vancomicina ou linezolida','somar ao esquema'),('Não precisa de vancomicina','basta cobrir o estafilococo sensível'))]
y0=2
for x,t,sb,q,sim,nao in cols:
    cbox(s,x+2,y0,cw-4,26,t,sb,'#F5F8FF')
    s.arrow(x+cw/2,y0+27,x+cw/2,y0+37)
    # pergunta
    ql=wrap(q,False,8.2,cw-30)
    qh=len(ql)*11.2+8
    s.box(x+2,y0+38,cw-4,qh,'#FFFFFF','#C3D8F8')
    yy=y0+38+7+7
    for l in ql: s.text(x+cw/2,yy,l,False,8.2,'#1F2933'); yy+=11.2
    yb=y0+38+qh
    rb=yb+22; rh=50
    bw=(cw-4-8)/2
    s.arrow(x+cw/2-10,yb+2,x+2+bw/2+8,rb-1)
    s.arrow(x+cw/2+10,yb+2,x+2+bw+8+bw/2-8,rb-1)
    s.text(x+cw/2-52,yb+15,'Sim',True,7.6,'#0B5BD3','end')
    s.text(x+cw/2+52,yb+15,'Não',True,7.6,'#0B5BD3','start')
    for i,(tt,ss) in enumerate((sim,nao)):
        cbox(s,x+2+i*(bw+8),rb,bw,rh,tt,ss,'#E7F7EC','#BFE5CB',tcol='#1E7A34',tsz=8.8,ssz=7.4)
yend=rb+rh
sy=yend+6
s.box(2,sy,W-4,30,'#F5F8FF','#C3D8F8')
s.text(W/2,sy+13,'Somando as duas colunas: de 1 a 3 antibióticos',True,9.2,'#16315C')
s.text(W/2,sy+24,'As doses e as combinações estão nas tabelas da diretriz: não precisa decorar, precisa saber consultar.',False,7.6,'#4A4A4F')
s.save('algoritmo.svg',int(sy+31))
