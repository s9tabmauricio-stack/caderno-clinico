# gera os três SVG (largura 478pt) com os mesmos dados do PDF antigo
from PIL import ImageFont
R='/usr/share/fonts/opentype/inter/Inter-Regular.otf'; S='/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'; B='/usr/share/fonts/opentype/inter/Inter-Bold.otf'
def fnt(f,s): return ImageFont.truetype(f,s)
def wrap(txt,f,s,w):
    ft=fnt(f,s); out=[]; cur=''
    for p in txt.split(' '):
        t=(cur+' '+p).strip()
        if ft.getlength(t)<=w or not cur: cur=t
        else: out.append(cur); cur=p
    out.append(cur); return out
def esc(t): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
W=478
def head(h): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" font-family="Inter">'
def text(x,y,t,size=8.6,fill='#1F2933',anchor='start',weight='400',fam='Inter'):
    return f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{esc(t)}</text>'
def arrow(x,y1,y2):  # seta para baixo (polígono)
    return (f'<rect x="{x-0.7}" y="{y1}" width="1.4" height="{y2-y1-5}" fill="#8AA9DF"/>'
            f'<polygon points="{x-3.6},{y2-6} {x+3.6},{y2-6} {x},{y2}" fill="#8AA9DF"/>')
def box(x,y,w,h,fill='#FFFFFF',stroke='#C3D8F8',r=8): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'

# ---------- figura 1: ar que fica para trás (dois painéis lado a lado) ----------
def fig1():
    h=150; o=[head(h)]
    o.append(text(0,12,'O ar que fica para trás, ciclo a ciclo',10.5,'#16315C',weight='700'))
    o.append(text(0,25,'Inspiração ativa (1 tempo) e expiração passiva (2 tempos), com o desenho exagerado para mostrar a sobra.',8.3,'#6C6C70'))
    pw=(W-8)/2
    def painel(x0,titulo,desc,obstruido):
        y0=34; ph=h-y0
        r=[box(x0,y0,pw,ph,'#F5F8FF','#DCE6F8',9)]
        r.append(text(x0+11,y0+16,titulo,9.4,'#1F2933',weight='700'))
        for i,l in enumerate(wrap(desc,R,8.2,pw-22)): r.append(text(x0+11,y0+29+i*10.5,l,8.2,'#3A3A3C'))
        xa,xb=x0+12,x0+pw-12; bot=y0+ph-14; n=5
        cw=(xb-xa)/n; amp=46 if obstruido else 50
        ris=cw/3; sobra=4.6 if obstruido else 0
        pts=[]
        for i in range(n):
            xs=xa+i*cw; yb=bot-sobra*i
            pts+=[(xs,yb),(xs+ris,yb-amp)]
        pts.append((xb,bot-sobra*n))
        poly=' '.join(f'{x:.1f},{y:.1f}' for x,y in pts)
        r.append(f'<line x1="{xa}" y1="{bot}" x2="{xb}" y2="{bot}" stroke="#A9C4EE" stroke-width="0.8" stroke-dasharray="2 3"/>')
        if obstruido:
            area=f'{xa},{bot} '+' '.join(f'{xa+i*cw:.1f},{bot-sobra*i:.1f}' for i in range(n+1))+f' {xb},{bot}'
            r.append(f'<polygon points="{area}" fill="#CFE0FB"/>')
            r.append(text(xb-2,bot+11,'ar aprisionado: o volume residual sobe',8,'#16315C','end','700'))
        r.append(f'<polyline points="{poly}" fill="none" stroke="#0B5BD3" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>')
        return ''.join(r)
    o.append(painel(0,'Pulmão normal','Inspira 500 mL e solta 500 mL: sempre volta ao mesmo ponto.',False))
    o.append(painel(pw+8,'Pulmão obstruído','Inspira 499 mL e solta só 498 mL: a cada ciclo sobra um pouco.',True))
    o.append('</svg>'); open('fig-ar.svg','w').write(''.join(o))

# ---------- figura 2: graus ----------
def fig2():
    h=236; o=[head(h)]
    o.append(box(0,0,W,40,'#F5F8FF','#C3D8F8',9))
    o.append(text(W/2,16,'Condição para os quatro graus: índice de Tiffeneau abaixo de 0,70 depois do broncodilatador',8.6,'#1F2933','middle','700'))
    o.append(text(W/2,30,'O grau vem do volume expiratório forçado no primeiro segundo, em % do valor previsto',8.2,'#3A3A3C','middle'))
    dados=[('≥ 80%','Leve','Grau 1 (GOLD 1)',112,'#C3D8F8'),('50 a 79%','Moderada','Grau 2 (GOLD 2)',88,'#A6C1EE'),('30 a 49%','Grave','Grau 3 (GOLD 3)',64,'#86A8E3'),('< 30%','Muito grave','Grau 4 (GOLD 4)',36,'#6B90D6')]
    bw=100; gap=(W-4*bw)/3; base=196
    for i,(v,nm,gr,hh,c) in enumerate(dados):
        x=i*(bw+gap)
        o.append(f'<rect x="{x:.1f}" y="{base-hh}" width="{bw}" height="{hh}" rx="5" fill="{c}"/>')
        o.append(text(x+bw/2,base-hh-7,v,12,'#16315C','middle','700'))
        o.append(text(x+bw/2,base+13,nm,9,'#1F2933','middle','700'))
        o.append(text(x+bw/2,base+25,gr,8,'#6C6C70','middle'))
    o.append(f'<line x1="0" y1="{base}" x2="{W}" y2="{base}" stroke="#C3D8F8" stroke-width="1"/>')
    o.append('</svg>'); open('fig-graus.svg','w').write(''.join(o))

# ---------- figura 3: algoritmo ----------
def fig3():
    colw=148; gap=17; xs=[0,colw+gap,2*(colw+gap)]
    o=[]
    def cx(i): return xs[i]+colw/2
    def caixa(x,y,w,tit,sub=None,verde=False,minh=0,titfs=9.2):
        tl=wrap(tit,S,titfs,w-16); sl=[]
        if sub:
            for s in sub: sl+=wrap(s,R,8,w-16)
        hh=max(minh, 12+len(tl)*12+(len(sl)*10.5+3 if sl else 0)+6)
        f,s_,tc=('#E7F7EC','#BFE5CB','#1E7A34') if verde else ('#FFFFFF','#C3D8F8','#16315C')
        r=[box(x,y,w,hh,f,s_,9)]
        yy=y+14
        for l in tl: r.append(text(x+w/2,yy,l,titfs,tc,'middle','600','Inter SemiBold')); yy+=12
        yy+=-1
        for l in sl: yy+=10.5; r.append(text(x+w/2,yy,l,8,'#1F2933','middle'))
        return ''.join(r),hh
    y=0
    # 1
    b,h1=caixa(0,y,W,'1. O paciente teve exacerbação?'); b=b.replace('fill="#FFFFFF"','fill="#F5F8FF"',1); o.append(b)
    ya=y+h1; yb=ya+18
    # setas Não (col 0-1 centro) e Sim (col 2)
    xn=(cx(0)+cx(1))/2; xsim=cx(2)
    o.append(arrow(xn,ya,yb)); o.append(text(xn+8,ya+16,'Não',8.2,'#1F2933','start','700'))
    o.append(arrow(xsim,ya,yb)); o.append(text(xsim+8,ya+16,'Sim',8.2,'#1F2933','start','700'))
    y=yb
    # 2: caixa dupla-coluna e grupo E
    w2=2*colw+gap
    b2,h2=caixa(0,y,w2,'2. Quanto sintoma ele tem?',['Escala de dispneia mMRC (0 a 4) ou questionário CAT (0 a 40)'])
    bE,hE=caixa(xs[2],y,colw,'Grupo E',['Exacerbador: já é E, ponto final'],minh=h2)
    h2=max(h2,hE); 
    b2,_=caixa(0,y,w2,'2. Quanto sintoma ele tem?',['Escala de dispneia mMRC (0 a 4) ou questionário CAT (0 a 40)'],minh=h2)
    bE,_=caixa(xs[2],y,colw,'Grupo E',['Exacerbador: já é E, ponto final'],minh=h2)
    o+= [b2,bE]
    ya=y+h2; yb=ya+26
    o.append(arrow(cx(0),ya,yb)); o.append(text(cx(0)+8,ya+18,'mMRC 0 ou 1',8.2,'#1F2933','start','700'))
    o.append(arrow(cx(1),ya,yb)); o.append(text(cx(1)+8,ya+18,'mMRC 2 ou mais',8.2,'#1F2933','start','700'))
    o.append(arrow(cx(2),ya,yb))
    y=yb
    # 3: A, B, contar eosinofilos
    cA=('Grupo A',['Pouco sintoma, sem exacerbação']); cB=('Grupo B',['Mais dispneia, sem exacerbação']); cC=('Contar eosinófilos',['No sangue, para decidir o corticoide inalatório'])
    hs=[caixa(xs[i],y,colw,*c)[1] for i,c in enumerate((cA,cB,cC))]; h3=max(hs)
    for i,c in enumerate((cA,cB,cC)): o.append(caixa(xs[i],y,colw,*c,minh=h3)[0])
    ya=y+h3; yb=ya+18
    for i in range(3): o.append(arrow(cx(i),ya,yb))
    y=yb
    f=[('Um broncodilatador',[]),('Dois broncodilatadores de longa ação',['Beta-2 agonista + antimuscarínico, juntos']),('Os mesmos dois de longa ação',['Com eosinófilos ≥ 300: considerar somar o corticoide inalatório (terapia tripla)'])]
    hs=[caixa(xs[i],y,colw,t,s,True)[1] for i,(t,s) in enumerate(f)]; h4=max(hs)
    for i,(t,s) in enumerate(f): o.append(caixa(xs[i],y,colw,t,s,True,minh=h4)[0])
    H=int(y+h4+2)
    open('fig-algoritmo.svg','w').write(head(H)+''.join(o)+'</svg>')
fig1(); fig2(); fig3()
