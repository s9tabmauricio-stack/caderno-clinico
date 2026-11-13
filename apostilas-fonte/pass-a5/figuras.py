#!/usr/bin/env python3
"""Esquemas originais da aula; SVGs regeneráveis, sem imagens externas."""
from pathlib import Path
from html import escape
from PIL import ImageFont

ROOT = Path(__file__).resolve().parent
FONT = Path('/tmp/pass-a5/fonts/Inter-Regular.ttf')
if not FONT.exists():
    FONT = ROOT.parent / 'ferramentas/fonts/Inter-Regular.ttf'

def text(x, y, value, size=10, color='#1F2933', anchor='start', weight=400):
    return f'<text x="{x}" y="{y}" font-family="Inter, sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{color}">{escape(value)}</text>'

def wrap(value, width, size):
    font = ImageFont.truetype(str(FONT), size)
    lines, current = [], ''
    for word in value.split():
        candidate = (current + ' ' + word).strip()
        if current and font.getlength(candidate) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    return lines + [current]

def save(name, height, parts):
    (ROOT / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="478" height="{height}" viewBox="0 0 478 {height}">' + ''.join(parts) + '</svg>')

def rect(x,y,w,h,fill='#FFFFFF',stroke='#C3D8F8',r=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'

parts = []
labels = ['Definir o desfecho','Montar a tabela','Calcular o risco','Comparar grupos','Medir a redução','Benefício e dano','Razão de chances']
for i, label in enumerate(labels):
    x = i * 68
    parts += [rect(x+1, 2, 64, 69), text(x+9, 20, f'0{i+1}', 9, '#0B5BD3', weight=600)]
    for j,line in enumerate(wrap(label, 51, 8)):
        parts.append(text(x+8, 38+j*11, line, 8, '#16315C'))
    if i < 6:
        parts.append(f'<polygon points="{x+66},33 {x+69},36 {x+66},39" fill="#8AA9DF"/>')
save('trilha.svg', 75, parts)

parts = [text(1,15,'O mesmo benefício, visto de duas formas',12,'#16315C',weight=600)]
for y,label,events in [(49,'Placebo',20),(92,'Medicação',10)]:
    parts += [text(1,y,label,10),rect(96,y-14,290,20,'#EDF1F6','#EDF1F6',4),rect(96,y-14,290*events/100,20,'#0B5BD3','#0B5BD3',4),text(477,y,f'{events} em 100',10,'#16315C','end')]
parts += [text(96,128,'10 eventos a menos por 100 pessoas: 10 pontos percentuais',9,'#16315C'),text(96,147,'10 a menos entre os 20 eventos do controle: redução de 50%',9,'#16315C')]
save('reducao.svg',158,parts)

parts = [text(1,15,'Multiplicação cruzada: o “peixinho”',12,'#16315C',weight=600)]
for x,y,label in [(168,62,'A'),(264,62,'B'),(168,118,'C'),(264,118,'D')]:
    parts += [rect(x,y-25,54,38),text(x+27,y,label,16,'#0B5BD3','middle',600)]
parts += [text(1,58,'Expostos',9),text(1,114,'Não expostos',9),text(195,31,'Com evento',9,'#16315C','middle'),text(291,31,'Sem evento',9,'#16315C','middle')]
parts += ['<path d="M 225 68 L 257 93 M 257 68 L 225 93" stroke="#8AA9DF" stroke-width="2" fill="none"/>',text(477,77,'A × D',14,'#16315C','end',600),'<line x1="411" y1="85" x2="477" y2="85" stroke="#16315C"/>',text(477,106,'B × C',14,'#16315C','end',600),text(1,157,'Mantenha a mesma ordem das linhas e colunas em toda a conta.',9)]
save('peixinho.svg',164,parts)
