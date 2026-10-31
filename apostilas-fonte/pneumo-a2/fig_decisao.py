from PIL import ImageFont
from xml.sax.saxutils import escape
REG='/usr/share/fonts/opentype/inter/Inter-Regular.otf'
SEMI='/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
W=478
def F(p,s): return ImageFont.truetype(p,s*10)  # medir em 10x para precisão
fr, fs = F(REG,8), F(SEMI,9)
def width(f,t): return f.getlength(t)/10
def wrap(t,f,maxw):
    out=[];cur=''
    for w in t.split():
        x=(cur+' '+w).strip()
        if width(f,x)<=maxw: cur=x
        else: out.append(cur);cur=w
    out.append(cur);return out
LH=10.9
els=[]
def rect(x,y,w,h,fill='#FFFFFF',stroke='#C3D8F8',rx=9):
    els.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>')
def text(x,y,t,fam,size,fill='#1F2933'):
    els.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" fill="{fill}">{escape(t)}</text>')
def arrow(x,y1,y2):
    els.append(f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{y2-4:.1f}" stroke="#8AA9DF" stroke-width="1.6"/>')
    els.append(f'<polygon points="{x-3.6:.1f},{y2-5:.1f} {x+3.6:.1f},{y2-5:.1f} {x:.1f},{y2:.1f}" fill="#8AA9DF"/>')
def line(x1,y1,x2,y2):
    els.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#8AA9DF" stroke-width="1.6"/>')
def box_h(title,body,w,pad=9,left=0):
    lines=wrap(body,fr,w-2*pad-left)
    return pad+11+len(lines)*LH+pad-1, lines
def step(y,n,title,body):
    h,lines=box_h(title,body,W,pad=7,left=26)
    rect(0.6,y,W-1.2,h)
    els.append(f'<circle cx="17" cy="{y+14:.1f}" r="8.5" fill="#E8F0FE" stroke="#C3D8F8" stroke-width="1.2"/>')
    els.append(f'<text x="17" y="{y+17.2:.1f}" text-anchor="middle" font-family="Inter SemiBold" font-size="8.5" fill="#0B5BD3">{n}</text>')
    text(34,y+14,title,'Inter SemiBold',9,'#16315C')
    for i,l in enumerate(lines): text(34,y+14+LH*(i+1)+1,l,'Inter',8)
    return h
GAP=11
y=0.6
h=step(y,1,'É pneumonia?','Clínica (sintomas respiratórios agudos, febre, dor pleurítica, achados focais), imagem com opacidade nova e contexto fora do hospital.');yc=y;y+=h;arrow(W/2,y,y+GAP);y+=GAP
h=step(y,2,'Quem é esse paciente?','Comorbidades, antibiótico ou internação nos últimos 90 dias, isolamento prévio de germe resistente, alergias, deglutição e suporte em casa.');y+=h;arrow(W/2,y,y+GAP);y+=GAP
h=step(y,3,'Onde tratar e qual a gravidade?','CURB-65 com julgamento clínico. Um critério maior ou três menores definem a pneumonia grave.');y+=h
# ramificação
G=10; cw=(W-1.2-2*G)/3; xs=[0.6+i*(cw+G) for i in range(3)]; cx=[x+cw/2 for x in xs]
ybr=y+7
line(W/2,y,W/2,ybr); line(cx[0],ybr,cx[2],ybr)
for c in cx: arrow(c,ybr,ybr+GAP+2)
y=ybr+GAP+2
cols=[
 [('Em casa','CURB-65 de 0 a 1 e nenhum outro motivo para internar.'),('Exames','Oximetria e radiografia. Sem exames de sangue nem cultura de rotina.'),('Antibiótico','Sem comorbidade: amoxicilina, doxiciclina ou macrolídeo. Com comorbidade: combinação ou fluoroquinolona.')],
 [('Na enfermaria','CURB-65 de 2 ou mais, ou hipoxemia, comorbidade descompensada ou falta de suporte.'),('Exames','Exames laboratoriais conforme a avaliação e culturas.'),('Antibiótico','Betalactâmico com macrolídeo, ou fluoroquinolona respiratória sozinha.')],
 [('Na terapia intensiva','Pneumonia grave: um critério maior ou três menores.'),('Exames','Investigação ampliada: hemoculturas e testes virais.'),('Antibiótico','Antibiótico e manejo de pneumonia grave; considerar corticoide, nunca na influenza.')],
]
for r in range(3):
    hs=[box_h(c[r][0],c[r][1],cw,pad=6)[0] for c in cols]; hm=max(hs)
    for i,c in enumerate(cols):
        t,b=c[r]; _,lines=box_h(t,b,cw,pad=6)
        rect(xs[i],y,cw,hm); text(xs[i]+8,y+13,t,'Inter SemiBold',9,'#16315C')
        for k,l in enumerate(lines): text(xs[i]+8,y+13+LH*(k+1)+1,l,'Inter',8)
    y+=hm
    if r<2:
        for cc in cx: arrow(cc,y,y+GAP)
        y+=GAP
# junção
yj=y+7
for cc in cx: line(cc,y,cc,yj)
line(cx[0],yj,cx[2],yj); line(W/2,yj,W/2,yj+GAP-1)
els.append(f'<polygon points="{W/2-3.6:.1f},{yj+GAP-5:.1f} {W/2+3.6:.1f},{yj+GAP-5:.1f} {W/2:.1f},{yj+GAP:.1f}" fill="#8AA9DF"/>')
y=yj+GAP
h=step(y,4,'Reavaliar em 48 a 72 horas','Estável: encerrar com 3 a 5 dias (grave: 5 dias ou mais). Não estável: rever o diagnóstico, a gravidade, o agente, a resistência e se o remédio foi usado direito.')
y+=h
H=y+1
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H:.1f}" viewBox="0 0 {W} {H:.1f}">'+''.join(els)+'</svg>'
open('caminho-decisao.svg','w',encoding='utf-8').write(svg)
print('altura',H)
