# Figuras da apostila de Angiologia · Aula 2 · Pé diabético
# uso: python3 figuras.py  (gera frentes.svg e conduta.svg na pasta atual)
import os, html, math, glob
from PIL import ImageFont

def achar(nome):
    for pasta in (os.path.expanduser('~/.fonts'), os.path.expanduser('~/.local/share/fonts'),
                  r'C:\Windows\Fonts', os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\Fonts'),
                  '/usr/share/fonts'):
        achados = glob.glob(os.path.join(pasta, '**', nome), recursive=True)
        if achados:
            return achados[0]
    raise SystemExit('fonte não encontrada: ' + nome)

R = achar('Inter-Regular.ttf')
S = achar('Inter-SemiBold.ttf')
def F(b, s): return ImageFont.truetype(S if b else R, round(s * 10))   # medido em 10x: o PIL arredonda tamanhos fracionários
def wrap(t, b, s, w):
    f = F(b, s); out = []; cur = ''
    for p in t.split(' '):
        n = (cur + ' ' + p).strip()
        if f.getlength(n) / 10 <= w or not cur: cur = n
        else: out.append(cur); cur = p
    out.append(cur); return out

W = 478
AZUL_T = '#16315C'; TXT = '#4A4A4F'; SETA = '#8AA9DF'; BORDA = '#C3D8F8'; APOIO = '#F5F8FF'

class Svg:
    def __init__(s): s.e = []
    def box(s, x, y, w, h, fill='#FFFFFF', stroke=BORDA, dash=False, rx=9, sw=1.1):
        d = ' stroke-dasharray="3 2.5"' if dash else ''
        s.e.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def text(s, x, y, t, b=False, sz=8.5, col='#1F2933', anchor='middle'):
        fam = 'Inter SemiBold' if b else 'Inter'
        s.e.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{sz}" fill="{col}" text-anchor="{anchor}">{html.escape(t)}</text>')
    def line(s, x1, y1, x2, y2, col=SETA, w=1.5):
        s.e.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}"/>')
    def arrow(s, x1, y1, x2, y2, col=SETA):
        a = math.atan2(y2 - y1, x2 - x1); L = 5.5; hw = 3.2
        bx, by = x2 - L * math.cos(a), y2 - L * math.sin(a)
        s.line(x1, y1, bx, by, col, 1.5)
        px, py = -math.sin(a) * hw, math.cos(a) * hw
        s.e.append(f'<polygon points="{x2:.1f},{y2:.1f} {bx+px:.1f},{by+py:.1f} {bx-px:.1f},{by-py:.1f}" fill="{col}"/>')
    def save(s, fn, h):
        open(fn, 'w', encoding='utf-8').write(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{h}pt" viewBox="0 0 {W} {h}">' + ''.join(s.e) + '</svg>')

def altura(w, title, sub, tsz, ssz):
    tl = wrap(title, True, tsz, w - 20) if title else []
    sl = wrap(sub, False, ssz, w - 20) if sub else []
    return len(tl) * tsz * 1.25 + len(sl) * ssz * 1.32

def cbox(s, x, y, w, h, title, sub, fill='#FFFFFF', stroke=BORDA, dash=False, tcol=AZUL_T, tsz=9.2, ssz=7.6, scol=TXT):
    s.box(x, y, w, h, fill, stroke, dash)
    tl = wrap(title, True, tsz, w - 20) if title else []
    sl = wrap(sub, False, ssz, w - 20) if sub else []
    th = altura(w, title, sub, tsz, ssz)
    yy = y + (h - th) / 2 + (tsz if tl else ssz) * 0.95
    for l in tl: s.text(x + w / 2, yy, l, True, tsz, tcol); yy += tsz * 1.25
    if tl and sl: yy += ssz * 0.08
    for l in sl: s.text(x + w / 2, yy, l, False, ssz, scol); yy += ssz * 1.32

# ---------------------------------------------------------------- 1. as quatro frentes
s = Svg()
gx = 8; cw = (W - 4 - 3 * gx) / 4
cols = [
    ('Neuropatia', 'sensitiva e autonômica',
     'Não sente dor, calor nem frio; o pé não sua, resseca e racha',
     'Machuca, não dói e continua pisando em cima'),
    ('Deformidade', 'da neuropatia motora',
     'Dedos em garra e em martelo, poucos pontos de apoio',
     'Calo nos pontos de pressão; embaixo dele, a úlcera afunda'),
    ('Doença arterial', 'aterosclerose acelerada',
     'Doença distal, muitas vezes sem queixa de claudicação',
     'Sem oxigênio nem antibiótico, a ferida não fecha'),
    ('Infecção', 'germes da própria pele',
     'Entra pela ferida, desce aos tendões e chega ao osso',
     'Osteomielite e sepse: o foco precisa sair'),
]
y = 2
h1 = 32
h2 = max(altura(cw, '', c[2], 9, 7.9) for c in cols) + 16
h3 = max(altura(cw, '', c[3], 9, 7.9) for c in cols) + 16
xs = [2 + i * (cw + gx) for i in range(4)]
for x, (t, sub, a, b) in zip(xs, cols):
    cbox(s, x, y, cw, h1, t, sub, APOIO, tsz=9.4, ssz=7.3)
    s.arrow(x + cw / 2, y + h1 + 1, x + cw / 2, y + h1 + 13)
    cbox(s, x, y + h1 + 14, cw, h2, '', a, ssz=7.9, scol='#1F2933')
    s.arrow(x + cw / 2, y + h1 + 14 + h2 + 1, x + cw / 2, y + h1 + 14 + h2 + 13)
    cbox(s, x, y + h1 + 28 + h2, cw, h3, '', b, ssz=7.9, scol='#1F2933')
yb = y + h1 + 28 + h2 + h3
yu = yb + 20
for x in xs:
    s.arrow(x + cw / 2, yb + 1, W / 2 + (x + cw / 2 - W / 2) * 0.35, yu - 1)
hu = 34
cbox(s, 2, yu, W - 4, hu, 'Úlcera que não cicatriza e infecciona',
     'as quatro frentes se somam no mesmo pé', '#E8F0FE', tsz=9.6, ssz=7.6)
s.arrow(W / 2, yu + hu + 1, W / 2, yu + hu + 13)
ya = yu + hu + 14
cbox(s, 2, ya, W - 4, 30, 'Amputação', 'cerca de 1 milhão de pessoas com diabetes por ano no mundo', '#E8F0FE', tcol=AZUL_T, tsz=9.6, ssz=7.6)
yp = ya + 30 + 10
hp = 34
s.box(2, yp, W - 4, hp, APOIO, BORDA, True)
s.text(W / 2, yp + 13.5, 'O que freia cada frente', True, 8.4, AZUL_T)
s.text(W / 2, yp + 26, 'controle da glicemia · autoexame diário · palmilha e calçado sob medida · revascularizar a isquemia · tratar cedo a infecção', False, 7.5, TXT)
s.save('frentes.svg', int(yp + hp + 2))

# ---------------------------------------------------------------- 2. conduta pela circulação
s = Svg()
gx = 10; cw = (W - 4 - 2 * gx) / 3
xs = [2 + i * (cw + gx) for i in range(3)]
y0 = 2; h0 = 34
cbox(s, 2, y0, W - 4, h0, 'Pé diabético com úlcera ou infecção',
     'olhar a cor e a temperatura, palpar os pulsos e medir o índice tornozelo-braquial', APOIO, tsz=9.6, ssz=7.6)
y1 = y0 + h0 + 22; h1 = 40
cbox(s, xs[0], y1, cw, h1, 'Boa perfusão', 'tem pulso, ou índice de 0,9 ou mais')
wr = xs[2] + cw - xs[1]
cbox(s, xs[1], y1, wr, h1, 'Comprometimento arterial importante', 'sem pulso, ou índice abaixo de 0,9')
s.arrow(W / 2 - 40, y0 + h0 + 1, xs[0] + cw / 2, y1 - 1)
s.arrow(W / 2 + 40, y0 + h0 + 1, xs[1] + wr / 2, y1 - 1)
y2 = y1 + h1 + 22; h2 = 46
cbox(s, xs[1], y2, cw, h2, 'Claudicação intermitente', 'dor ao andar, sem risco iminente para a perna')
cbox(s, xs[2], y2, cw, h2, 'Dor isquêmica de repouso', 'dói parado; depois do banho a perna esfria e empalidece')
s.arrow(xs[1] + wr / 2 - 30, y1 + h1 + 1, xs[1] + cw / 2, y2 - 1)
s.arrow(xs[1] + wr / 2 + 30, y1 + h1 + 1, xs[2] + cw / 2, y2 - 1)
y3 = y2 + h2 + 22; h3 = 58
G = dict(fill='#E7F7EC', stroke='#BFE5CB', tcol='#1E7A34', tsz=9.2, ssz=7.6)
cbox(s, xs[0], y3, cw, h3, 'Tratamento habitual', 'cuidar da úlcera e tratar a infecção', **G)
cbox(s, xs[1], y3, cw, h3, 'Ambulatório de cirurgia vascular', 'encaminhar para acompanhar e avaliar', **G)
cbox(s, xs[2], y3, cw, h3, 'Internar com urgência', 'revascularizar, desbridar a necrose e amputar o que não for viável', **G)
s.arrow(xs[0] + cw / 2, y1 + h1 + 1, xs[0] + cw / 2, y3 - 1)
s.arrow(xs[1] + cw / 2, y2 + h2 + 1, xs[1] + cw / 2, y3 - 1)
s.arrow(xs[2] + cw / 2, y2 + h2 + 1, xs[2] + cw / 2, y3 - 1)
s.save('conduta.svg', int(y3 + h3 + 2))
print('frentes.svg e conduta.svg gerados')
