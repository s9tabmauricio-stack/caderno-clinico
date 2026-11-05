"""Figuras vetoriais originais. Executar na pasta da apostila, com Pillow instalado."""
from pathlib import Path
from html import escape
from PIL import ImageFont
import base64

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'fig'
OUT.mkdir(exist_ok=True)
FONT = ROOT / 'fonts' / 'Inter-Regular.ttf'
BOLD = ROOT / 'fonts' / 'Inter-SemiBold.ttf'
BLUE, NAVY, BORDER, INK, GRAY = '#0B5BD3', '#16315C', '#C3D8F8', '#1F2933', '#6C6C70'

def wrap(text, size, width, bold=False):
    f = ImageFont.truetype(str(BOLD if bold else FONT), size * 4)
    lines, line = [], ''
    for word in text.split():
        test = f'{line} {word}'.strip()
        if line and f.getlength(test) / 4 > width:
            lines.append(line); line = word
        else: line = test
    if line: lines.append(line)
    return lines

def text(x,y,s,size=10,color=INK,bold=False,anchor='start'):
    family='Inter SemiBold' if bold else 'Inter'
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(s)}</text>'

def para(x,y,s,width=130,size=9,color=INK,bold=False):
    return ''.join(text(x,y+i*size*1.5,l,size,color,bold) for i,l in enumerate(wrap(s,size,width,bold)))

def box(x,y,w,h,title,body,num=None):
    z=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="white" stroke="{BORDER}"/>'
    if num:
        z+=f'<circle cx="{x+17}" cy="{y+19}" r="10" fill="#E8F0FE"/>'+text(x+17,y+22.2,str(num),9,BLUE,True,'middle')
        z+=text(x+33,y+22,title,10,NAVY,True)
    else: z+=text(x+12,y+22,title,10,NAVY,True)
    return z+para(x+12,y+44,body,w-24,9)

def arrow(x1,y1,x2,y2):
    if x1==x2:
        return f'<path d="M{x1},{y1} L{x2},{y2-5}" stroke="#8AA9DF" stroke-width="1.4" fill="none"/><polygon points="{x2-3},{y2-6} {x2+3},{y2-6} {x2},{y2}" fill="#8AA9DF"/>'
    return f'<path d="M{x1},{y1} L{x2-5},{y2}" stroke="#8AA9DF" stroke-width="1.4" fill="none"/><polygon points="{x2-6},{y2-3} {x2-6},{y2+3} {x2},{y2}" fill="#8AA9DF"/>'

def save(name,h,s):
    (OUT/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="478" height="{h}" viewBox="0 0 478 {h}">{s}</svg>')

steps=[('A paciente','Mulher adulta e caminho da infecção'),('Os exames','Urina, cultura e antibiograma'),('A cistite','Reconhecer sintomas de bexiga'),('O tratamento','Escolher o esquema da cistite'),('O rim','Reconhecer infecção e gravidade'),('A conduta','Ambulatório, internação e drenagem'),('O risco','Identificar fatores complicadores'),('A gestação','Proteger a mãe e a gestação')]
s=''
for i,(t,b) in enumerate(steps):
    col,row=i%4,i//4;x,y=col*121,row*96
    s+=box(x,y,115,87,t,b,i+1)
    if col<3:s+=arrow(x+115,y+44,x+121,y+44)
save('trilha.svg',184,s)

s=box(0,0,149,120,'Exame de urina','Quais alterações aparecem? Leucócitos, hemácias, nitrito e outros parâmetros.',1)
s+=box(164,0,149,120,'Urocultura','Qual microrganismo cresceu? Identificação e contagem das colônias.',2)
s+=box(329,0,149,120,'Antibiograma','A quais antibióticos o microrganismo é sensível?',3)
s+=arrow(149,58,164,58)+arrow(313,58,329,58)
save('exames.svg',122,s)

s=box(0,0,149,121,'Sintomas urinários','Ardor e urgência: pensar na bexiga. Procurar dor lombar, febre e sintomas gerais.',1)
s+=box(164,0,149,121,'Suspeita renal','Investigar pielonefrite com avaliação clínica, cultura e exames apropriados.',2)
s+=box(329,0,149,121,'Definir o cuidado','Critério absoluto ou gestante com pielonefrite: internação. Sem gravidade: avaliar ambulatório.',3)
s+=arrow(149,60,164,60)+arrow(313,60,329,60)
s+='<rect x="0" y="132" width="478" height="55" rx="9" fill="#F5F8FF" stroke="#C3D8F8"/>'
s+=text(12,150,'Se não há indicação absoluta',9,NAVY,True)
s+=para(12,167,'Estabilidade, acesso ao medicamento e reavaliação possível sustentam a avaliação para tratamento ambulatorial.',454,9)
save('decisao.svg',189,s)

s=box(0,0,149,120,'Identificar','Sintomas e exames; colher cultura. Na abordagem da aula, não atrasar tratamento de infecção sintomática.',1)
s+=box(164,0,149,120,'Tratar e observar','Escolher fármaco compatível com a gestação. Sem resposta em 2–3 dias: reavaliar.',2)
s+=box(329,0,149,120,'Confirmar resposta','Controle de urocultura em uma semana, no esquema de acompanhamento da aula.',3)
s+=arrow(149,58,164,58)+arrow(313,58,329,58)
save('gestacao.svg',122,s)

image_path=OUT/'sistema-urinario.png'
if image_path.exists():
    b64=base64.b64encode(image_path.read_bytes()).decode()
    s=f'<image x="75" y="0" width="328" height="219" xlink:href="data:image/png;base64,{b64}"/>'
    s+=para(0,27,'Rim sem destaque inflamatório',100,9,NAVY,True)
    s+='<path d="M85,47 L140,47" stroke="#8AA9DF" fill="none"/>'
    s+=para(372,25,'Pielonefrite: rim e pelve renal',106,9,NAVY,True)
    s+='<path d="M373,48 L337,48" stroke="#8AA9DF" fill="none"/>'
    s+=text(25,115,'Ureteres',9,NAVY,True)
    s+='<path d="M88,112 L188,112 M88,112 L292,112" stroke="#8AA9DF" fill="none"/>'
    s+=para(353,166,'Cistite: mucosa da bexiga',120,9,NAVY,True)
    s+='<path d="M350,171 L286,171" stroke="#8AA9DF" fill="none"/>'
    s+=text(122,221,'Uretra feminina curta',9,NAVY,True)
    s+='<path d="M229,218 L237,204" stroke="#8AA9DF" fill="none"/>'
    save('anatomia.svg',232,s)

print('Figuras:', ', '.join(p.name for p in sorted(OUT.glob('*.svg'))))
