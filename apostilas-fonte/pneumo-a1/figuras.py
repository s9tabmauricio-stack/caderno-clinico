import sys; sys.path.insert(0,'/tmp/refazer')
from figlib import *
W=478
# ---------- espiral da morte ----------
def espiral():
    cw,g=109,14
    X=[i*(cw+g) for i in range(4)]
    sp=16
    r1=[Box('Trombo fecha um ramo','da artéria pulmonar',cw,seal=1,sealpad=sp,fill=SOFT),
        Box('Pressão sobe e o ventrículo direito dilata','a valva tricúspide vaza',cw,seal=2,sealpad=sp,fill=SOFT),
        Box('Parede tensa e inflamada','o ventrículo direito pede mais oxigênio',cw,seal=3,sealpad=sp,fill=SOFT),
        Box('Espaço morto','área ventilada sem sangue: hipoxemia',cw)]
    r2={0:Box('O que procurar','ventrículo direito dilatado, pressão caindo, lactato alto',cw,dash=True,fill='#FFFFFF'),
        2:Box('Coronárias recebem menos sangue','a isquemia piora e o ciclo se fecha',cw,seal=7,sealpad=sp,fill=SOFT),
        3:Box('Isquemia do ventrículo direito','ele começa a infartar e a contração cai',cw,seal=4,sealpad=sp,fill=SOFT)}
    r3={0:Box('Parada e óbito','se ninguém desobstrui o vaso a tempo',cw),
        2:Box('Débito cardíaco e pressão caem','síncope, hipotensão: choque obstrutivo',cw,seal=6,sealpad=sp,fill=SOFT),
        3:Box('Débito do ventrículo direito cai','chega pouco sangue ao ventrículo esquerdo',cw,seal=5,sealpad=sp,fill=SOFT)}
    h1=max(b.h for b in r1);h2=max(b.h for b in r2.values());h3=max(b.h for b in r3.values())
    y1=6;gap1=38;y2=y1+h1+gap1;gap2=32;y3=y2+h2+gap2;H=y3+h3+6
    o=''
    for i,b in enumerate(r1): o+=b.draw(X[i],y1,h1)
    for i in (0,1): o+=arrow(X[i]+cw+1,y1+h1/2,X[i+1]-1,y1+h1/2,4)
    o+=text(X[2]+cw+g/2,y1+h1/2+3,'+',11,600,BLUE)
    # colchete: caixas 3 e 4 -> caixa 4 da linha 2
    xa,xb=X[2]+cw/2,X[3]+cw/2
    ym=y1+h1+12
    o+=line([(xa,y1+h1),(xa,ym),(xb,ym)])+line([(xb,y1+h1),(xb,ym)])
    o+=text((xa+xb)/2,ym+10.5,'mais demanda, menos oferta',7,400,NAVY)
    o+=arrow(xb,ym,xb,y2-1,5)
    for i,b in r2.items(): o+=b.draw(X[i],y2,h2)
    for i,b in r3.items(): o+=b.draw(X[i],y3,h3)
    # setas: 7 -> 4 ; 4 -> 5 ; 5 -> 6 ; 6 -> 7 ; 6 -> parada
    o+=arrow(X[2]+cw+1,y2+h2/2,X[3]-1,y2+h2/2,4)
    o+=arrow(X[3]+cw/2,y2+h2,X[3]+cw/2,y3-1,5)
    o+=arrow(X[3]-1,y3+h3/2,X[2]+cw+1,y3+h3/2,4)
    o+=arrow(X[2]+cw/2,y3,X[2]+cw/2,y2+h2+1,5)
    o+=arrow(X[2]-1,y3+h3/2,X[0]+cw+1,y3+h3/2,5)
    # rótulo central
    cx=X[1]+cw/2+ (g/2)
    cyy=(y2+h2+y3)/2
    o+=text(cx,y2+h2/2-3,'espiral',9,700,BLUE)
    o+=text(cx,y2+h2/2+9,'da morte',9,700,BLUE)
    return svg(W,H,o)
# ---------- algoritmo do paciente estável ----------
def algoritmo():
    cw,g=136,35
    X=[i*(cw+g) for i in range(3)]
    C=[x+cw/2 for x in X]
    o='';y=6
    top=Box('Suspeita de embolia pulmonar em paciente estável','',270,tsz=8.4,fill='#E8F0FE',stroke=ARR)
    o+=top.draw((W-270)/2,y,top.h); y+=top.h
    o+=arrow(W/2,y,W/2,y+16,5); y+=16
    hist=Box('','História, exame físico e escore de Wells (ou de Genebra): qual a probabilidade antes do exame?',340,bsz=7.6)
    o+=hist.draw((W-340)/2,y,hist.h); y+=hist.h
    yb=y+13
    o+=line([(W/2,y),(W/2,yb)]) ; o+=line([(C[0],yb),(C[2],yb)])
    pr=[Box('Probabilidade baixa','',cw,tsz=8,fill='#E8F0FE'),Box('Probabilidade moderada','',cw,tsz=8,fill='#E8F0FE'),Box('Probabilidade alta','',cw,tsz=8,fill='#E8F0FE')]
    ypr=yb+14
    for i in range(3):
        o+=arrow(C[i],yb,C[i],ypr-1,5); o+=pr[i].draw(X[i],ypr,pr[i].h)
    y=ypr+pr[0].h
    r=[Box('Critérios PERC','oito perguntas: alguma resposta é sim?',cw),
       Box('Dímero D + critérios YEARS','o resultado define o ponto de corte',cw),
       Box('Direto para a imagem','sem dímero D: só faria perder horas',cw)]
    yr=y+18; hr=max(b.h for b in r)
    for i in range(3):
        o+=arrow(C[i],y,C[i],yr-1,5); o+=r[i].draw(X[i],yr,hr)
    # PERC -> dímero
    o+=arrow(X[0]+cw+1,yr+hr/2,X[1]-1,yr+hr/2,5)
    o+=text(X[0]+cw+g/2,yr+hr/2-4,'alguma',7,400,NAVY)
    o+=text(X[0]+cw+g/2,yr+hr/2+11,'sim',7,400,NAVY)
    f=[Box('Nada mais a pedir','probabilidade muito baixa, menor que 1%',cw,fill='#E8F0FE',stroke=ARR),
       Box('Embolia afastada','sem exame de imagem; procure outra causa',cw,fill='#E8F0FE',stroke=ARR),
       Box('Angiotomografia','confirma ou afasta a embolia',cw,fill='#E8F0FE',stroke=ARR)]
    yf=yr+hr+44; hf=max(b.h for b in f)
    for i in range(3): o+=f[i].draw(X[i],yf,hf)
    # setas finais
    o+=arrow(C[0],yr+hr,C[0],yf-1,5); o+=text(C[0]+5,yr+hr+25,'todas não',7,400,NAVY,'start')
    o+=arrow(C[1],yr+hr,C[1],yf-1,5); o+=text(C[1]-5,yr+hr+25,'abaixo do corte',7,400,NAVY,'end')
    ye=yr+hr+22; xe=C[1]+50
    o+=line([(xe,yr+hr),(xe,ye),(C[2],ye)])
    o+=text((xe+C[2])/2,ye-4,'acima do corte',7,400,NAVY)
    o+=arrow(C[2],yr+hr,C[2],yf-1,5)
    H=yf+hf+6
    return svg(W,H,o)
# ---------- escada de A a E ----------
def escada():
    n=5;g=9.5;cw=(W-4*g)/n
    cols=[('A','','Assintomática','embolia achada por acaso, em exame pedido por outro motivo','#F5F8FF'),
          ('B','B1 · B2','Sintomática, baixa gravidade','PESI simplificado igual a zero; o número depende de ser subsegmentar ou não','#E8F0FE'),
          ('C','C1 · C2 · C3','PESI simplificado de 1 ou mais','C1: ventrículo direito e biomarcadores normais. C2: um alterado. C3: os dois alterados','#DCE8FD'),
          ('D','D1 · D2','Falência começando','hipotensão transitória ou choque normotensivo (pressão normal, perfusão ruim)','#CFE0FB'),
          ('E','E1 · E2','Falência instalada','hipotensão persistente; choque refratário ou parada cardiorrespiratória','#C3D8F8')]
    pad=8;iw=cw-2*pad
    need=[]
    for L,num,t,b,_ in cols:
        tl=wrap(t,S,8.4,iw);bl=wrap(b,R,7.6,iw)
        need.append(pad+24+len(tl)*10.3+4+len(bl)*9.9+pad)
    base=[110,132,158,184,208]
    hs=[max(a,b) for a,b in zip(need,base)]
    # garante degraus crescentes
    for i in range(1,n): hs[i]=max(hs[i],hs[i-1]+22)
    top=30;H=top+hs[-1]+6
    o=text(0,13,'quanto maior a letra e o número, maior o risco de morrer',7.4,400,NAVY,'start')
    wcap=tw('quanto maior a letra e o número, maior o risco de morrer',R,7.4)
    o+=arrow(wcap+8,10.5,W-2,10.5,6)
    for i,(L,num,t,b,fill) in enumerate(cols):
        x=i*(cw+g);y=H-6-hs[i]
        o+=rect(x,y,cw,hs[i],fill,LINE,r=8)
        o+=text(x+pad,y+pad+17,L,20,700,NAVY,'start')
        if num: o+=text(x+cw-pad,y+pad+16,num,7,600,BLUE,'end')
        yy=y+pad+24+8
        for l in wrap(t,S,8.4,iw): o+=text(x+pad,yy,l,8.4,600,NAVY,'start'); yy+=10.3
        yy+=4+0.5
        for l in wrap(b,R,7.6,iw): o+=text(x+pad,yy,l,7.6,400,INK,'start'); yy+=9.9
    return svg(W,H,o)
open('/tmp/refazer/pneumo-a1/fig-espiral.svg','w').write(espiral())
open('/tmp/refazer/pneumo-a1/fig-algoritmo.svg','w').write(algoritmo())
open('/tmp/refazer/pneumo-a1/fig-escada.svg','w').write(escada())
print('ok')
