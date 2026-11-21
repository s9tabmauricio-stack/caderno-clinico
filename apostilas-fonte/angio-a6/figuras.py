"""Figuras da apostila angio-a6 (Linfedema e lipedema). Rode na pasta da apostila: python3 figuras.py"""
import math
import os
from PIL import ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = {400: "Inter-Regular.ttf", 500: "Inter-Medium.ttf", 600: "Inter-SemiBold.ttf", 700: "Inter-Bold.ttf"}
_cache = {}

W = 478
BORDA = "#C3D8F8"
APOIO = "#F5F8FF"
SETA = "#8AA9DF"
TXT = "#1F2933"
TIT = "#16315C"
AZUL = "#0B5BD3"
CINZA = "#6C6C70"


def fonte(peso, tam):
    k = (peso, tam)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(os.path.join(AQUI, "fonts", FONTES[peso]), tam)
    return _cache[k]


def larg(txt, peso, tam):
    return fonte(peso, tam).getlength(txt)


def quebra(txt, peso, tam, maxw):
    linhas, atual = [], ""
    for p in txt.split():
        t = (atual + " " + p).strip()
        if larg(t, peso, tam) <= maxw or not atual:
            atual = t
        else:
            linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    return linhas


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def texto(x, y, t, peso=400, tam=8, cor=TXT, anc="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter" font-weight="{peso}" '
            f'font-size="{tam}" fill="{cor}" text-anchor="{anc}">{esc(t)}</text>')


def bloco(x, y, linhas, peso=400, tam=8, cor=TXT, anc="start", lh=None):
    lh = lh or tam * 1.3
    return "".join(texto(x, y + i * lh, l, peso, tam, cor, anc) for i, l in enumerate(linhas))


def caixa(x, y, w, h, fundo="#FFFFFF", borda=BORDA, r=8, tracejado=False, esp=1):
    d = ' stroke-dasharray="4 3"' if tracejado else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
            f'fill="{fundo}" stroke="{borda}" stroke-width="{esp}"{d}/>')


def ponta(x, y, ang, tam=6, cor=SETA):
    """Triângulo com a ponta em (x, y) apontando no ângulo ang (graus; 0 = direita, 90 = baixo)."""
    a = math.radians(ang)
    bx, by = x - tam * math.cos(a), y - tam * math.sin(a)
    px, py = -math.sin(a) * tam * 0.55, math.cos(a) * tam * 0.55
    return f'<polygon points="{x:.1f},{y:.1f} {bx+px:.1f},{by+py:.1f} {bx-px:.1f},{by-py:.1f}" fill="{cor}"/>'


def linha(pts, cor=SETA, esp=1.6, tracejado=False):
    d = ' stroke-dasharray="4 3"' if tracejado else ""
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline points="{p}" fill="none" stroke="{cor}" stroke-width="{esp}"{d}/>'


def seta(pts, cor=SETA, esp=1.6, tam=6, tracejado=False):
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    enc = pts[:-1] + [(x2 - (tam - 1) * math.cos(math.radians(ang)), y2 - (tam - 1) * math.sin(math.radians(ang)))]
    return linha(enc, cor, esp, tracejado) + ponta(x2, y2, ang, tam, cor)


def selo(cx, cy, n, r=7.5, fundo=AZUL):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fundo}"/>'
            + texto(cx, cy + 2.9, str(n), 600, 8, "#FFFFFF", "middle"))


def svg(h, corpo, nome):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{h}pt" viewBox="0 0 {W} {h}">'
         + corpo + "</svg>")
    with open(os.path.join(AQUI, nome), "w", encoding="utf-8") as f:
        f.write(s)


# ---------------------------------------------------------------- trilha da aula
def trilha():
    etapas = [
        ("A linfa", "filtra, reabsorve e o linfático tira o excesso"),
        ("A drenagem falha", "proteína parada, inflamação e erisipela"),
        ("Os tipos", "primário pela idade; secundário pela causa"),
        ("O quadro clínico", "frio, duro, cilíndrico, quase sem dor"),
        ("Lipedema", "o ramo do lado: doença da gordura"),
        ("Diagnóstico", "história e linfocintilografia"),
        ("Tratamento clínico", "quatro medidas somadas"),
        ("Cirurgia", "pouca derivação, alguma redução; neoplasias"),
    ]
    bw, gap, bh = 108, 15, 64
    corpo = []
    for i, (t, s) in enumerate(etapas):
        lin, col = divmod(i, 4)
        x = col * (bw + gap)
        y = 4 + lin * (bh + 34)
        ramo = i == 4
        corpo.append(caixa(x + 0.5, y, bw - 1, bh, "#FFFFFF", BORDA, 9, tracejado=ramo))
        corpo.append(selo(x + 15, y + 15, i + 1))
        tl = quebra(t, 600, 8.6, bw - 34)
        corpo.append(bloco(x + 28, y + 18, tl, 600, 8.6, TIT))
        sl = quebra(s, 400, 7.4, bw - 18)
        corpo.append(bloco(x + 9, y + 37 + (len(tl) - 1) * 10, sl, 400, 7.4, CINZA, lh=9.6))
        if col < 3:
            corpo.append(seta([(x + bw + 1.5, y + bh / 2), (x + bw + gap - 1.5, y + bh / 2)], tam=5.5))
    # ligação da etapa 4 para a 5
    x4 = 3 * (bw + gap) + bw / 2
    ymid = 4 + bh + 17
    corpo.append(seta([(x4, 4 + bh + 1), (x4, ymid), (bw / 2, ymid), (bw / 2, 4 + bh + 34 - 1)], tam=5.5))
    h = 4 + 2 * bh + 34 + 4
    svg(h, "".join(corpo), "trilha.svg")


# ---------------------------------------------------------------- microcirculação
def micro():
    c = []
    # capilar sanguíneo (faixa de cima)
    c.append(f'<rect x="20" y="22" width="438" height="26" rx="13" fill="#E8F0FE" stroke="{BORDA}"/>')
    c.append(seta([(150, 35), (330, 35)], cor=AZUL, tam=6))
    c.append(texto(240, 31, "sangue", 500, 7.2, AZUL, "middle"))
    c.append(texto(20, 14, "Lado arterial do capilar", 600, 8.6, TIT))
    c.append(texto(458, 14, "Lado venoso do capilar", 600, 8.6, TIT, "end"))
    # interstício
    c.append(caixa(20, 66, 438, 74, APOIO, BORDA, 10))
    c.append(texto(239, 80, "Espaço intersticial (entre as células)", 600, 8.2, TIT, "middle"))
    for cx in [140, 180, 220, 260, 300, 340]:
        c.append(f'<circle cx="{cx}" cy="105" r="10" fill="#FFFFFF" stroke="{BORDA}"/>')
    # setas de filtração e reabsorção
    for x in [44, 66]:
        c.append(seta([(x, 50), (x, 92)], tam=5.5))
    for x in [412, 434]:
        c.append(seta([(x, 92), (x, 50)], tam=5.5))
    c.append(bloco(78, 98, ["filtra"], 600, 8.2, AZUL))
    c.append(bloco(400, 98, ["reabsorve"], 600, 8.2, AZUL, "end"))
    c.append(bloco(239, 128, ["As células ficam coesas, com o líquido no lugar certo"], 400, 7.4, CINZA, "middle"))
    # linfático
    c.append(f'<rect x="120" y="170" width="338" height="22" rx="11" fill="#FFFFFF" stroke="{AZUL}" stroke-width="1.2"/>')
    c.append(seta([(250, 181), (400, 181)], cor=AZUL, tam=6))
    c.append(texto(325, 177.5, "linfa", 500, 7.2, AZUL, "middle"))
    for x in [180, 239, 298]:
        c.append(seta([(x, 142), (x, 168)], tam=5.5))
    c.append(bloco(20, 166, ["Linfático"], 600, 8.6, TIT))
    c.append(bloco(20, 178, ["recolhe o excesso,", "sempre um pouco a mais"], 400, 7.4, CINZA, lh=9.4))
    c.append(texto(239, 210, "Recolher um pouco a mais do que sobrou cria pressão negativa: o tecido fica firme, como um pacote a vácuo.", 500, 7.6, TXT, "middle"))
    svg(216, "".join(c), "micro.svg")


# ---------------------------------------------------------------- caminho da linfa
def trajeto():
    etapas = [
        ("Capilares linfáticos", "Recolhem o excesso de líquido, proteínas e corpos estranhos do tecido."),
        ("Coletores com válvulas", "Cada linfângio se contrai: a válvula de baixo fecha, a de cima abre e a linfa sobe."),
        ("Linfonodos inguinais", "Na virilha, a linfa passa pelo filtro que apresenta os antígenos aos linfócitos."),
        ("Cisterna do quilo", "Recebe a gordura absorvida do intestino: a linfa fica leitosa (quilosa)."),
        ("Ducto torácico", "Sobe pelo tórax levando a linfa do abdome, dos membros inferiores e do lado esquerdo do corpo."),
        ("Veia subclávia esquerda", "Recebe a linfa, com suas proteínas e gorduras, de volta ao sangue."),
    ]
    bw, bh, gap = 150, 30, 12
    xn = bw + 18
    c = []
    y = 6
    for i, (t, n) in enumerate(etapas):
        c.append(caixa(0.5, y, bw, bh, "#FFFFFF", BORDA, 8))
        c.append(selo(15, y + bh / 2, i + 1, r=7))
        c.append(texto(28, y + bh / 2 + 3, t, 600, 8.4, TIT))
        nl = quebra(n, 400, 8, W - xn - 2)
        ny = y + bh / 2 + 3 - (len(nl) - 1) * 5.2
        c.append(bloco(xn, ny, nl, 400, 8, TXT, lh=10.4))
        if i < len(etapas) - 1:
            c.append(seta([(bw / 2, y + bh + 1), (bw / 2, y + bh + gap - 1)], tam=5))
        y += bh + gap
    h = y - gap + 6
    svg(h, "".join(c), "trajeto.svg")


# ---------------------------------------------------------------- ciclo vicioso
def ciclo():
    c = []
    bw, bh = 172, 46
    xa, xb, y = 30, W - 30 - bw, 30
    c.append(caixa(xa, y, bw, bh, "#FFFFFF", BORDA, 10))
    c.append(caixa(xb, y, bw, bh, "#FFFFFF", BORDA, 10))
    c.append(texto(xa + bw / 2, y + 20, "Linfático danificado", 600, 8.8, TIT, "middle"))
    c.append(texto(xa + bw / 2, y + 33, "drena mal, a defesa local cai", 400, 7.6, CINZA, "middle"))
    c.append(texto(xb + bw / 2, y + 20, "Erisipela de repetição", 600, 8.8, TIT, "middle"))
    c.append(texto(xb + bw / 2, y + 33, "cada infecção destrói mais linfático", 400, 7.6, CINZA, "middle"))
    # arco de cima (esquerda -> direita) e de baixo (direita -> esquerda)
    x1, x2 = xa + bw / 2, xb + bw / 2
    c.append(f'<path d="M {x1} {y-2} C {x1+40} {y-26}, {x2-40} {y-26}, {x2-2} {y-5}" fill="none" stroke="{SETA}" stroke-width="1.6"/>')
    c.append(ponta(x2 + 1, y - 2, 40, 6))
    c.append(f'<path d="M {x2} {y+bh+2} C {x2-40} {y+bh+26}, {x1+40} {y+bh+26}, {x1+2} {y+bh+5}" fill="none" stroke="{SETA}" stroke-width="1.6"/>')
    c.append(ponta(x1 - 1, y + bh + 2, 220, 6))
    c.append(texto(W / 2, y + bh / 2 + 3, "ciclo vicioso", 600, 8.6, AZUL, "middle"))
    # resultado
    yr = y + bh + 34
    c.append(caixa(90, yr, W - 180, 30, APOIO, BORDA, 9))
    c.append(texto(W / 2, yr + 13, "Inflamação crônica", 600, 8.4, TIT, "middle"))
    c.append(texto(W / 2, yr + 24, "pele dura, cheia de verrucosidades, cronicamente inflamada", 400, 7.6, TXT, "middle"))
    svg(yr + 34, "".join(c), "ciclo.svg")


# ---------------------------------------------------------------- classificação
def tipos():
    c = []
    cw, gap = 148, 17
    xs = [0.5, cw + gap, 2 * (cw + gap)]
    # raiz
    rw = 150
    c.append(caixa(W / 2 - rw / 2, 2, rw, 26, "#E8F0FE", BORDA, 9))
    c.append(texto(W / 2, 18.5, "Linfedema", 600, 9.4, TIT, "middle"))
    # nível 2
    y2 = 50
    c.append(caixa(xs[0], y2, cw, 34, "#FFFFFF", BORDA, 9))
    c.append(texto(xs[0] + cw / 2, y2 + 14, "Primário", 600, 8.8, TIT, "middle"))
    c.append(texto(xs[0] + cw / 2, y2 + 26, "defeito do próprio sistema", 400, 7.4, CINZA, "middle"))
    sx = xs[1]
    sw = 2 * cw + gap
    c.append(caixa(sx, y2, sw, 34, "#FFFFFF", BORDA, 9))
    c.append(texto(sx + sw / 2, y2 + 14, "Secundário", 600, 8.8, TIT, "middle"))
    c.append(texto(sx + sw / 2, y2 + 26, "algo danificou um sistema que funcionava", 400, 7.4, CINZA, "middle"))
    c.append(seta([(W / 2, 29), (W / 2, 39), (xs[0] + cw / 2, 39), (xs[0] + cw / 2, y2 - 1)], tam=5))
    c.append(seta([(W / 2, 39), (sx + sw / 2, 39), (sx + sw / 2, y2 - 1)], tam=5))
    # nível 3: cabeçalhos dos secundários
    y3 = 104
    for x, t in [(xs[1], "Inflamatório"), (xs[2], "Não inflamatório")]:
        c.append(texto(x + cw / 2, y3 + 4, t, 600, 8.2, AZUL, "middle"))
    c.append(texto(xs[0] + cw / 2, y3 + 4, "Pela idade de início", 600, 8.2, AZUL, "middle"))
    for x in xs:
        c.append(seta([(x + cw / 2, y2 + 35), (x + cw / 2, y3 - 6)], tam=5))
    folhas = [
        [("Congênito", "já nasce com ele (síndrome de Turner, síndrome de Klippel-Trénaunay)"),
         ("Precoce", "começa antes dos 35 anos"),
         ("Tardio", "começa depois dos 35 anos; o mais visto")],
        [("Filariose", "Wuchereria bancrofti; elefantíase"),
         ("Pós-infeccioso", "erisipela de repetição, com porta de entrada nos pés")],
        [("Tumoral", "pouco frequente; em geral, doença avançada"),
         ("Pós-cirúrgico", "mastectomia com retirada dos linfonodos axilares; radioterapia"),
         ("Trauma", "acidentes")],
    ]
    # altura de cada folha, igualando a base das três colunas
    pads = []
    for col in folhas:
        hs = []
        for t, s in col:
            sl = quebra(s, 400, 7.4, cw - 16)
            hs.append(24 + len(sl) * 9.4)
        pads.append(hs)
    total = max(sum(hs) + 7 * (len(hs) - 1) for hs in pads)
    y0 = y3 + 12
    for ci, col in enumerate(folhas):
        hs = pads[ci]
        extra = (total - (sum(hs) + 7 * (len(hs) - 1))) / len(hs)
        y = y0
        for (t, s), hh in zip(col, hs):
            hh += extra
            c.append(caixa(xs[ci], y, cw, hh, "#FFFFFF", BORDA, 8))
            c.append(texto(xs[ci] + 8, y + 14, t, 600, 8.4, TIT))
            sl = quebra(s, 400, 7.4, cw - 16)
            c.append(bloco(xs[ci] + 8, y + 26, sl, 400, 7.4, TXT, lh=9.4))
            y += hh + 7
    svg(y0 + total + 3, "".join(c), "tipos.svg")


# ---------------------------------------------------------------- terapia física complexa
def tfc():
    c = []
    lx, rx = 96, W - 2
    c.append(texto(lx + 4, 8, "pé (periferia)", 600, 7.4, CINZA))
    c.append(texto(rx - 4, 8, "virilha (centro)", 600, 7.4, CINZA, "end"))

    def estrada(y, titulo, sub):
        tl = quebra(titulo, 600, 8.6, 88)
        y0 = y - 2 - (len(tl) - 1) * 5.5
        c.append(bloco(0, y0, tl, 600, 8.6, TIT, lh=11))
        c.append(bloco(0, y0 + 11 * len(tl), quebra(sub, 400, 7.2, 88), 400, 7.2, CINZA, lh=9))
        c.append(f'<rect x="{lx}" y="{y-12}" width="{rx-lx}" height="24" rx="12" fill="{APOIO}" stroke="{BORDA}"/>')

    def pedagio(y, aberto):
        px = rx - 96
        if aberto:
            c.append(f'<rect x="{px}" y="{y-15}" width="30" height="30" rx="3" fill="#FFFFFF" stroke="{AZUL}" stroke-width="1.2" stroke-dasharray="3 2"/>')
        else:
            c.append(f'<rect x="{px}" y="{y-15}" width="30" height="30" rx="3" fill="#DCDCE2" stroke="#8E8E93" stroke-width="1"/>')
        return px

    y1 = 36
    estrada(y1, "Drenagem estética", "massagem que empurra o líquido de baixo para cima")
    px = pedagio(y1, False)
    c.append(texto(px + 15, y1 + 3, "fechado", 600, 6.6, "#4F5B70", "middle"))
    c.append(seta([(lx + 14, y1), (px - 3, y1)], tam=6))
    c.append(texto(lx + 10, y1 + 25, "Empurra a partir do pé e o líquido para no bloqueio: não passa.", 500, 7.4, TXT))
    y2 = 92
    estrada(y2, "Terapia física complexa", "abre o centro primeiro, depois traz a periferia")
    px = pedagio(y2, True)
    c.append(selo(px + 15, y2, 1, r=7))
    c.append(seta([(px + 33, y2), (rx - 12, y2)], cor=AZUL, tam=6))
    c.append(seta([(lx + 14, y2), (px - 4, y2)], tam=6))
    c.append(selo((lx + px) / 2, y2, 2, r=7))
    c.append(texto(lx + 10, y2 + 25, "2  depois, traz o líquido do pé", 500, 7.4, TXT))
    c.append(texto(rx - 4, y2 + 25, "1  primeiro, abre o pedágio: linfonodos e coletores do centro", 500, 7.4, TXT, "end"))
    svg(y2 + 30, "".join(c), "tfc.svg")


if __name__ == "__main__":
    trilha(); micro(); trajeto(); ciclo(); tipos(); tfc()
    print("figuras prontas")
