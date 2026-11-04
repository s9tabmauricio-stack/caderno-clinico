"""Figuras da aula de Tabagismo. SVGs vetoriais, medidos com a fonte Inter."""
from pathlib import Path
from html import escape
from functools import lru_cache
import math
import xml.etree.ElementTree as ET
from PIL import ImageFont

BASE = Path(__file__).resolve().parent
OUT = BASE / 'fig'
OUT.mkdir(exist_ok=True)
W = 478
NAVY = '#16315C'
BLUE = '#0B5BD3'
TEXT = '#1F2933'
GRAY = '#5C6878'
BORDER = '#C3D8F8'
ARROW = '#8AA9DF'
PALE = '#F5F8FF'

@lru_cache(maxsize=32)
def font(size=9.5, bold=False):
    p = BASE / 'fonts' / ('Inter-SemiBold.ttf' if bold else 'Inter-Regular.ttf')
    return ImageFont.truetype(str(p), round(size * 4))

def measure(t, size=9.5, bold=False):
    return font(size, bold).getlength(t) / 4

def wrap(t, width, size=9.5, bold=False):
    lines = []
    for paragraph in t.split('\n'):
        line = ''
        for word in paragraph.split():
            candidate = (line + ' ' + word).strip()
            if line and measure(candidate, size, bold) > width:
                lines.append(line)
                line = word
            else:
                line = candidate
        lines.append(line)
    return lines

class Figure:
    def __init__(self, height, title, desc):
        self.h = height
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="478pt" height="{height}pt" viewBox="0 0 478 {height}" role="img">',
                      f'<title>{escape(title)}</title><desc>{escape(desc)}</desc>']
        self.text_boxes = []

    def rect(self, x, y, w, h, fill='white', stroke=BORDER, radius=10):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')

    def line(self, x1, y1, x2, y2, stroke=ARROW, width=1.5, dash=''):
        dashed = f' stroke-dasharray="{dash}"' if dash else ''
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round"{dashed}/>')

    def path(self, d, stroke=ARROW, width=1.5, dash=''):
        dashed = f' stroke-dasharray="{dash}"' if dash else ''
        self.parts.append(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{dashed}/>')

    def arrow(self, x1, y1, x2, y2, stroke=ARROW, width=1.5, head=4):
        self.line(x1,y1,x2,y2,stroke,width)
        a = math.atan2(y2-y1,x2-x1)
        pts = [(x2,y2),(x2-head*math.cos(a)+head*.58*math.sin(a),y2-head*math.sin(a)-head*.58*math.cos(a)),(x2-head*math.cos(a)-head*.58*math.sin(a),y2-head*math.sin(a)+head*.58*math.cos(a))]
        self.parts.append('<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in pts)+f'" fill="{stroke}"/>')

    def circle(self, x,y,r,fill=BLUE):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>')

    def text(self, x, y, txt, size=9.5, bold=False, color=TEXT, anchor='start'):
        width = measure(txt,size,bold)
        left = x if anchor=='start' else x-width if anchor=='end' else x-width/2
        assert left >= -0.1 and left+width <= W+.1, (txt, left, width)
        assert y-size >= -1 and y+size*.25 <= self.h+1, (txt,y,self.h)
        self.text_boxes.append((left,y-size,left+width,y+size*.25,txt))
        family = 'Inter SemiBold' if bold else 'Inter'
        self.parts.append(f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(txt)}</text>')

    def para(self,x,y,txt,width,size=9.5,bold=False,color=TEXT,anchor='start',leading=1.5):
        lines = wrap(txt,width,size,bold)
        for i,t in enumerate(lines):
            self.text(x,y+i*size*leading,t,size,bold,color,anchor)
        return y + len(lines)*size*leading

    def save(self,name):
        s='\n'.join(self.parts+['</svg>'])+'\n'
        ET.fromstring(s)
        (OUT/name).write_text(s,encoding='utf-8')
        print(f'{name}: 478 × {self.h} pt; {len(self.text_boxes)} linhas de texto verificadas')


def trilha():
    f=Figure(132,'Trilha da aula','Oito etapas: dependência, avaliação, Dia D, medicação, acompanhamento, dispositivos, riscos e prevenção.')
    titles=['Entender a\ndependência','Abordar e\navaliar','Combinar\no Dia D','Individualizar\na medicação','Acompanhar\ne ajustar','Entender os\ndispositivos','Reconhecer\nos riscos','Prevenir e\ncompartilhar']
    bw=107.5
    for n,title in enumerate(titles):
        x=6+(n%4)*119.5
        y=4+(n//4)*76
        f.rect(x,y,bw,48)
        f.text(x+9,y+13,f'{n+1:02d}',8,True,BLUE)
        f.para(x+9,y+28,title,bw-18,8.7,True,NAVY,leading=1.35)
        if n%4!=3:
            f.arrow(x+bw+2,y+24,x+bw+10,y+24,head=3.5)
    f.path('M 472 28 L 476 28 L 476 66 L 2 66 L 2 104')
    f.arrow(2,104,5.5,104,head=3)
    f.save('trilha.svg')


def dependencia():
    f=Figure(152,'Três dimensões da dependência','As dependências física, psicológica e comportamental devem ser consideradas juntas.')
    data=[('Física','Nicotina e abstinência','O corpo pede reposição.'),('Psicológica','Emoções e contexto','Ansiedade, estresse e\nbusca de concentração.'),('Comportamental','Rotina e gatilhos','Café, carro e\npós-refeição.')]
    for i,(title,sub,body) in enumerate(data):
        x=2+i*160
        f.rect(x,3,154,96)
        f.text(x+12,25,title,10.4,True,NAVY)
        f.para(x+12,44,sub,130,8.7,True,BLUE,leading=1.4)
        f.para(x+12,65,body,130,9,False,leading=1.5)
        f.line(x+77,99,x+77,111)
    f.line(79,111,399,111)
    f.arrow(239,111,239,121,head=4)
    f.rect(53,123,372,26,fill=PALE)
    f.text(239,140,'O cuidado precisa alcançar as três dimensões.',9.5,True,NAVY,'middle')
    f.save('dependencia.svg')


def plano():
    f=Figure(146,'Do preparo ao acompanhamento','Marcar o Dia D entre sete e trinta dias, preparar mudanças de rotina e seguir acompanhando.')
    xs=[79,239,399]
    f.line(xs[0],25,xs[-1],25,width=2)
    labels=['Preparação','Dia D','Seguimento']
    for i,x in enumerate(xs):
        f.circle(x,25,11)
        f.text(x,28.5,str(i+1),9,True,'white','middle')
        f.text(x,12,labels[i],9.5,True,NAVY,'middle')
    data=[('7–30 dias antes','Marcar a data; identificar\ngatilhos; combinar mudanças.'),('Mudar a rotina','Retirar o cigarro dos\nhábitos do dia a dia.'),('Acompanhar','Rever fissura e dificuldades;\nreformular o plano se recair.')]
    for i,(title,body) in enumerate(data):
        x=2+i*160
        f.rect(x,46,154,82)
        f.text(x+12,66,title,9.5,True,BLUE)
        f.para(x+12,85,body,130,9,False,leading=1.5)
    f.text(239,143,'Plano construído com a pessoa, conforme sua rotina e necessidades.',8.5,False,GRAY,'middle')
    f.save('plano.svg')


def adesivos():
    f=Figure(130,'Exemplo de redução dos adesivos','Esquema de três meses apresentado pelo professor para o exemplo de vinte cigarros por dia.')
    for i,(dose,month) in enumerate([('21 mg','1º mês'),('14 mg','2º mês'),('7 mg','3º mês')]):
        x=7+i*162
        f.rect(x,3,140,78)
        f.text(x+70,23,month,9,True,NAVY,'middle')
        f.text(x+70,53,dose,22,True,BLUE,'middle')
        f.text(x+70,69,'um mês nesta etapa',8.2,False,GRAY,'middle')
        if i<2:
            f.arrow(x+144,42,x+157,42,head=4)
    f.rect(7,92,464,34,fill=PALE)
    f.text(239,106,'EXEMPLO · 20 cigarros/dia',8.5,True,NAVY,'middle')
    f.text(239,119,'Troca diária e alternância do local de aplicação.',8.7,False,TEXT,'middle')
    f.save('adesivos.svg')


def funcao():
    f=Figure(220,'Cessar muda o ritmo de perda','Esquema qualitativo: a função pulmonar já perdida não se recupera automaticamente, mas a cessação reduz o ritmo de perda futura.')
    f.text(9,12,'Função pulmonar',9,True,NAVY)
    f.line(37,25,37,153,stroke=GRAY,width=1)
    f.arrow(37,153,451,153,stroke=GRAY,width=1,head=4)
    f.text(451,168,'Idade / passagem do tempo',8.7,False,GRAY,'end')
    f.path('M 45 35 C 143 40 220 51 440 78',stroke=ARROW,width=2.4)
    f.path('M 45 35 C 100 44 158 61 215 80 C 294 106 360 126 440 146',stroke=NAVY,width=2.5)
    f.path('M 215 80 C 283 88 363 98 440 110',stroke=BLUE,width=2.5,dash='6 4')
    f.circle(215,80,3.5,BLUE)
    f.line(215,76,215,68,stroke=BLUE,width=1)
    f.text(215,61,'Cessação',8.8,True,BLUE,'middle')
    legend=[(10,183,ARROW,'Sem tabagismo',''),(169,183,NAVY,'Continua fumando',''),(333,183,BLUE,'Após cessar','6 4')]
    for x,y,col,label,dash in legend:
        f.line(x,y-3,x+22,y-3,col,2.2,dash)
        f.text(x+29,y,label,8.5,False,TEXT)
    f.rect(7,195,464,22,fill=PALE)
    f.text(239,210,'Esquema qualitativo, sem escala: cessar reduz a perda futura.',8.5,False,TEXT,'middle')
    f.save('funcao-pulmonar.svg')


def conta():
    f=Figure(158,'Como ler a concentração do pod','Exemplo da aula: cinco por cento, dez mililitros, dez dias. O resultado estima nicotina contida no líquido consumido, não dose absorvida.')
    steps=[('Concentração','5% × 10','50 mg/mL'),('Volume do refil','50 mg/mL × 10 mL','500 mg no líquido'),('Duração do refil','500 mg ÷ 10 dias','50 mg/dia no líquido')]
    for i,(title,eq,result) in enumerate(steps):
        x=2+i*160
        f.rect(x,3,154,93)
        f.text(x+12,23,title,9,True,NAVY)
        f.text(x+77,48,eq,9.1,True,BLUE,'middle')
        f.line(x+12,58,x+142,58,BORDER,1)
        f.para(x+77,76,result,130,9,True,TEXT,'middle',1.3)
        if i<2:
            f.arrow(x+155,47,x+159,47,head=3)
    f.rect(2,108,474,47,fill=PALE)
    f.text(239,126,'Conteúdo médio de nicotina no líquido consumido por dia.',9.3,True,NAVY,'middle')
    f.text(239,144,'A conta não determina quanto foi absorvido pelo organismo.',8.8,False,TEXT,'middle')
    f.save('conta-pod.svg')


if __name__=='__main__':
    for fn in (trilha,dependencia,plano,adesivos,funcao,conta):
        fn()
