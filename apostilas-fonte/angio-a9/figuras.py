# Desenha as figuras da apostila angio-a9: trilha.svg, ulceras.svg e as imagens dos slides com rótulos.
# uso (na pasta de trabalho): python3 figuras.py <slides.pdf>
import os, sys
from PIL import ImageFont, Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
F = {k: os.path.join(AQUI, 'fonts', f'Inter-{k}.ttf') for k in ('Regular', 'Medium', 'SemiBold', 'Bold')}
FAM = {'Regular': 'Inter', 'Medium': 'Inter Medium', 'SemiBold': 'Inter SemiBold', 'Bold': 'Inter'}
_cache = {}

def larg(txt, peso, tam):
    k = (peso, tam)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(F[peso], int(tam * 20))
    return _cache[k].getlength(txt) / 20

def quebra(txt, peso, tam, w):
    linhas, atual = [], ''
    for p in txt.split():
        t = (atual + ' ' + p).strip()
        if larg(t, peso, tam) <= w or not atual:
            atual = t
        else:
            linhas.append(atual); atual = p
    if atual:
        linhas.append(atual)
    return linhas

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def texto(x, y, txt, peso='Regular', tam=8, cor='#1F2933', anc='start'):
    w = ' font-weight="700"' if peso == 'Bold' else ''
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FAM[peso]}"{w} font-size="{tam}" '
            f'fill="{cor}" text-anchor="{anc}">{esc(txt)}</text>')

def seta_v(x, y1, y2, cor='#8AA9DF'):
    # linha vertical com ponta para baixo (polígono)
    return (f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{y2-5:.1f}" stroke="{cor}" stroke-width="1.6"/>'
            f'<polygon points="{x-4:.1f},{y2-6:.1f} {x+4:.1f},{y2-6:.1f} {x:.1f},{y2:.1f}" fill="{cor}"/>')

def seta_h(x1, x2, y, cor='#8AA9DF'):
    return (f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2-5:.1f}" y2="{y:.1f}" stroke="{cor}" stroke-width="1.6"/>'
            f'<polygon points="{x2-6:.1f},{y-4:.1f} {x2-6:.1f},{y+4:.1f} {x2:.1f},{y:.1f}" fill="{cor}"/>')

def svg(w, h, corpo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}pt" height="{h:.1f}pt" '
            f'viewBox="0 0 {w} {h:.1f}">' + ''.join(corpo) + '</svg>')

# ---------------------------------------------------------------- trilha
def trilha():
    W = 478
    etapas = [
        ('Arteriopatias funcionais', 'artéria sã; frio e emoção disparam'),
        ('Fenômeno de Raynaud', 'branco, roxo, vermelho; primário ou secundário'),
        ('Tratar o Raynaud', 'fugir do frio, vasodilatador, simpatectomia'),
        ('Acrocianose', 'moça magra ou idoso cardiopata'),
        ('Livedo reticular', 'pele em rede; e a eritromelalgia'),
        ('Distrofia simpático-reflexa', 'depois de um trauma; pulso presente'),
        ('Ergotismo', 'remédio de enxaqueca; espasmo que imita êmbolo'),
        ('Úlceras', 'o lugar da ferida aponta a causa'),
    ]
    gap, bw = 18, (W - 3 * 18) / 4
    pad, tt, ts = 8, 8.6, 7.4
    caixas = []
    for i, (t, s) in enumerate(etapas):
        lt = quebra(t, 'SemiBold', tt, bw - 2 * pad - 18)
        ls = quebra(s, 'Regular', ts, bw - 2 * pad)
        caixas.append((lt, ls))
    def altura(c):
        lt, ls = c
        return pad + 4 + max(len(lt) * 10.5, 16) + 3 + len(ls) * 9.4 + pad
    h1 = max(altura(c) for c in caixas[:4])
    h2 = max(altura(c) for c in caixas[4:])
    y1, ygap = 4, 26
    y2 = y1 + h1 + ygap
    H = y2 + h2 + 4
    out = []
    for i, (lt, ls) in enumerate(caixas):
        lin, col = divmod(i, 4)
        x = col * (bw + gap)
        y = y1 if lin == 0 else y2
        h = h1 if lin == 0 else h2
        ramo = i == 7
        dash = ' stroke-dasharray="4 3"' if ramo else ''
        fundo = '#F5F8FF' if ramo else '#FFFFFF'
        out.append(f'<rect x="{x+0.8:.1f}" y="{y:.1f}" width="{bw-1.6:.1f}" height="{h:.1f}" rx="9" fill="{fundo}" stroke="#C3D8F8" stroke-width="1.2"{dash}/>')
        cx, cy = x + pad + 7, y + pad + 7
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="7.2" fill="#0B5BD3"/>')
        out.append(texto(cx, cy + 2.9, str(i + 1), 'SemiBold', 7.8, '#FFFFFF', 'middle'))
        ty = y + pad + 10.2
        for k, l in enumerate(lt):
            out.append(texto(x + pad + 18, ty + k * 10.5, l, 'SemiBold', tt, '#16315C'))
        sy = y + pad + 4 + max(len(lt) * 10.5, 16) + 3 + 7
        for k, l in enumerate(ls):
            out.append(texto(x + pad, sy + k * 9.4, l, 'Regular', ts, '#3A3A3C'))
        if col < 3 and i < 7:
            ya = y + h / 2
            out.append(seta_h(x + bw + 1, x + bw + gap - 1, ya))
    # retorno da linha 1 para a linha 2 (de 4 para 5)
    x4 = 3 * (bw + gap) + bw / 2
    x5 = bw / 2
    ym = y1 + h1 + ygap / 2
    out.append(f'<polyline points="{x4:.1f},{y1+h1+1:.1f} {x4:.1f},{ym:.1f} {x5:.1f},{ym:.1f}" fill="none" stroke="#8AA9DF" stroke-width="1.6"/>')
    out.append(seta_v(x5, ym, y2 - 1))
    # rótulo do ramo
    return svg(W, H, out)

# ---------------------------------------------------------------- úlceras
def ulceras():
    W = 478
    gap = 12
    cw = (W - 2 * gap) / 3
    pad = 9
    out = []
    # topo
    tw = 300
    tx = (W - tw) / 2
    t1 = 'Ferida na perna ou no pé'
    t2 = quebra('Onde ela está e como é a pele ao redor?', 'Regular', 8.2, tw - 2 * pad)
    th = pad + 11 + len(t2) * 10.5 + pad - 2
    y = 2
    out.append(f'<rect x="{tx:.1f}" y="{y}" width="{tw}" height="{th:.1f}" rx="10" fill="#F5F8FF" stroke="#C3D8F8" stroke-width="1.2"/>')
    out.append(texto(W / 2, y + pad + 8.5, t1, 'SemiBold', 9.4, '#16315C', 'middle'))
    for k, l in enumerate(t2):
        out.append(texto(W / 2, y + pad + 21 + k * 10.5, l, 'Regular', 8.2, '#3A3A3C', 'middle'))
    ybar = y + th + 12
    out.append(f'<line x1="{W/2:.1f}" y1="{y+th:.1f}" x2="{W/2:.1f}" y2="{ybar:.1f}" stroke="#8AA9DF" stroke-width="1.6"/>')
    xs = [i * (cw + gap) + cw / 2 for i in range(3)]
    out.append(f'<line x1="{xs[0]:.1f}" y1="{ybar:.1f}" x2="{xs[2]:.1f}" y2="{ybar:.1f}" stroke="#8AA9DF" stroke-width="1.6"/>')
    cond = [
        ('Maléolo medial', ['Por dentro do tornozelo; raramente em outro ponto.',
                            'Pele ao redor com doença venosa: dermatite ocre, lipodermatoesclerose.']),
        ('Extremidade', ['Ponta do dedo, calcâneo ou tornozelo.',
                         'Falta de circulação (isquemia).']),
        ('Fora do lugar habitual', ['Joelho, bolsa escrotal, outros pontos.',
                                    'Pele ao redor sem sinais de doença venosa.',
                                    'Necrose e dor intensa.']),
    ]
    fim = [
        ('Úlcera venosa', 'Cerca de 80% das feridas. Bota de Unna.'),
        ('Úlcera arterial', 'Isquêmica, por falta de circulação.'),
        ('Pensar em vasculite', 'Há doença de base: pedir o parecer do reumatologista.'),
    ]
    yc = ybar + 18
    def bloco(lista, w):
        hs = []
        for par in lista:
            hs.append(quebra(par, 'Regular', 7.9, w))
        return hs
    cbs = [(c[0], bloco(c[1], cw - 2 * pad)) for c in cond]
    hc = max(pad + 12 + sum(len(b) * 9.8 + 3 for b in bl) + pad - 4 for _, bl in cbs)
    for i, (t, bl) in enumerate(cbs):
        x = i * (cw + gap)
        out.append(seta_v(xs[i], ybar, yc - 1))
        out.append(f'<rect x="{x+0.6:.1f}" y="{yc:.1f}" width="{cw-1.2:.1f}" height="{hc:.1f}" rx="10" fill="#FFFFFF" stroke="#C3D8F8" stroke-width="1.2"/>')
        out.append(texto(x + pad, yc + pad + 8.5, t, 'SemiBold', 9, '#16315C'))
        yy = yc + pad + 22
        for b in bl:
            for l in b:
                out.append(texto(x + pad, yy, l, 'Regular', 7.9, '#3A3A3C'))
                yy += 9.8
            yy += 3
    yf = yc + hc + 18
    fbs = [(t, quebra(s, 'Regular', 7.9, cw - 2 * pad)) for t, s in fim]
    hf = max(pad + 12 + len(b) * 9.8 + pad - 1 for _, b in fbs)
    for i, (t, b) in enumerate(fbs):
        x = i * (cw + gap)
        out.append(seta_v(xs[i], yc + hc, yf - 1))
        out.append(f'<rect x="{x+0.6:.1f}" y="{yf:.1f}" width="{cw-1.2:.1f}" height="{hf:.1f}" rx="10" fill="#E8F0FE" stroke="#0B5BD3" stroke-width="1.2"/>')
        out.append(texto(x + pad, yf + pad + 8.5, t, 'SemiBold', 9.2, '#0B5BD3'))
        for k, l in enumerate(b):
            out.append(texto(x + pad, yf + pad + 22 + k * 9.8, l, 'Regular', 7.9, '#1F2933'))
    H = yf + hf + 2
    return svg(W, H, out)

# ---------------------------------------------------------------- imagens dos slides
AZUL = (11, 91, 211)

def extrair(pdf_path):
    import pypdfium2 as pdfium, pypdfium2.raw as raw
    pdf = pdfium.PdfDocument(pdf_path)
    imgs = {}
    for n in (4, 10, 14, 15, 17, 19, 20):
        k = 0
        for obj in pdf[n - 1].get_objects(max_depth=3):
            if obj.type == raw.FPDF_PAGEOBJ_IMAGE:
                k += 1
                if k >= 2:
                    imgs[(n, k)] = obj.get_bitmap(render=False).to_pil().convert('RGB')
    return imgs

def rotulo(dr, xy, txt, tam, seta_para=None, anc='l'):
    f = ImageFont.truetype(F['SemiBold'], tam)
    x, y = xy
    w = f.getlength(txt); h = tam * 1.25
    px, py = tam * 0.55, tam * 0.35
    if anc == 'r':
        x = x - w - 2 * px
    if seta_para:
        sx, sy = seta_para
        cx, cy = x + (w + 2 * px) / 2, y + (h + 2 * py) / 2
        dr.line([(cx, cy), (sx, sy)], fill=AZUL, width=max(3, tam // 7))
        import math
        a = math.atan2(sy - cy, sx - cx)
        L, Wd = tam * 0.9, tam * 0.45
        p1 = (sx, sy)
        p2 = (sx - L * math.cos(a) + Wd * math.sin(a), sy - L * math.sin(a) - Wd * math.cos(a))
        p3 = (sx - L * math.cos(a) - Wd * math.sin(a), sy - L * math.sin(a) + Wd * math.cos(a))
        dr.polygon([p1, p2, p3], fill=AZUL)
    dr.rounded_rectangle([x, y, x + w + 2 * px, y + h + 2 * py], radius=tam * 0.45, fill=(255, 255, 255), outline=AZUL, width=max(2, tam // 10))
    dr.text((x + px, y + py), txt, font=f, fill=(22, 49, 92))

def imagens(pdf_path):
    im = extrair(pdf_path)
    im[(4, 2)].save(os.path.join(AQUI, 'sl04-cores.jpg'), quality=92)
    im[(10, 2)].save(os.path.join(AQUI, 'sl10-maos.jpg'), quality=92)
    im[(14, 2)].save(os.path.join(AQUI, 'sl14-video.jpg'), quality=92)
    im[(14, 3)].save(os.path.join(AQUI, 'sl14-lombar.jpg'), quality=92)
    im[(15, 2)].save(os.path.join(AQUI, 'sl15-dedos.jpg'), quality=90)
    im[(15, 3)].save(os.path.join(AQUI, 'sl15-mao.jpg'), quality=90)
    im[(17, 2)].save(os.path.join(AQUI, 'sl17-livedo.jpg'), quality=92)
    # pés: o esquerdo do paciente fica à direita da foto
    p = im[(19, 2)].copy()
    dr = ImageDraw.Draw(p)
    rotulo(dr, (930, 60), 'Pé esquerdo', 84, seta_para=(1000, 640))
    rotulo(dr, (60, 60), 'Pé direito', 84, seta_para=(600, 600))
    p.save(os.path.join(AQUI, 'sl19-pes.jpg'), quality=90)
    # angiografia: sem a legenda em inglês, ampliada para o rótulo
    a = im[(20, 2)]
    a = a.crop((0, 0, a.width, 370)).resize((a.width * 3, 370 * 3), Image.LANCZOS)
    dr = ImageDraw.Draw(a)
    rotulo(dr, (330, 760), 'Artéria fina, em espasmo', 46, seta_para=(395, 600))
    a.save(os.path.join(AQUI, 'sl20-angio.jpg'), quality=92)

if __name__ == '__main__':
    open(os.path.join(AQUI, 'trilha.svg'), 'w').write(trilha())
    open(os.path.join(AQUI, 'ulceras.svg'), 'w').write(ulceras())
    if len(sys.argv) > 1:
        imagens(sys.argv[1])
    print('ok')
