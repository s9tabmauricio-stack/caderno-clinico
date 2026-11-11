#!/usr/bin/env python3
"""Desenha as figuras SVG da apostila nefro-a8 (trilha, fisiopatologia, diagnóstico, infecção)."""
import os
from PIL import ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
F = {w: os.path.join(AQUI, "fonts", f"Inter-{n}.ttf") for w, n in
     ((400, "Regular"), (500, "Medium"), (600, "SemiBold"), (700, "Bold"))}
_cache = {}


def larg(txt, size, w=400):
    k = (size, w)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(F[w], size)
    return _cache[k].getlength(txt)


def quebra(txt, size, maxw, w=400):
    linhas, atual = [], ""
    for p in txt.split():
        t = (atual + " " + p).strip()
        if larg(t, size, w) <= maxw:
            atual = t
        else:
            linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    return linhas


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


W = 478
AZUL_B = "#C3D8F8"
APOIO = "#F5F8FF"
SETA = "#8AA9DF"
TXT = "#1F2933"
TIT = "#16315C"
AZ = "#0B5BD3"


class SVG:
    def __init__(self):
        self.el = []

    def rect(self, x, y, w, h, fill="#FFFFFF", stroke=AZUL_B, r=8, sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
                       f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, size=8.5, w=400, color=TXT, anchor="middle"):
        self.el.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter" font-size="{size}" '
                       f'font-weight="{w}" fill="{color}" text-anchor="{anchor}">{esc(s)}</text>')

    def bloco(self, x, y, w, linhas, size=8.5, peso=400, color=TXT, lh=1.32, anchor="middle"):
        """linhas = lista de (texto, peso, cor); devolve a altura usada."""
        yy = y
        for t, pw, cor in linhas:
            yy += size * lh
            xx = x + w / 2 if anchor == "middle" else x
            self.text(xx, yy - size * 0.32, t, size, pw, cor, anchor)
        return yy - y

    def seta_v(self, x, y1, y2):
        h = 5
        self.el.append(f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{y2 - h:.1f}" stroke="{SETA}" stroke-width="1.6"/>')
        self.el.append(f'<polygon points="{x - 4:.1f},{y2 - h - 1:.1f} {x + 4:.1f},{y2 - h - 1:.1f} {x:.1f},{y2:.1f}" fill="{SETA}"/>')

    def seta_h(self, x1, x2, y):
        h = 5
        self.el.append(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2 - h:.1f}" y2="{y:.1f}" stroke="{SETA}" stroke-width="1.6"/>')
        self.el.append(f'<polygon points="{x2 - h - 1:.1f},{y - 4:.1f} {x2 - h - 1:.1f},{y + 4:.1f} {x2:.1f},{y:.1f}" fill="{SETA}"/>')

    def caminho(self, pts):
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.el.append(f'<polyline points="{d}" fill="none" stroke="{SETA}" stroke-width="1.6"/>')

    def salvar(self, nome, h):
        corpo = "\n".join(self.el)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{h:.0f}pt" '
               f'viewBox="0 0 {W} {h:.0f}">\n{corpo}\n</svg>\n')
        with open(os.path.join(AQUI, nome), "w", encoding="utf-8") as f:
            f.write(svg)


def caixa_txt(s, x, y, w, titulo, texto, size=8.4, tsize=8.8, fill="#FFFFFF", stroke=AZUL_B,
              tcolor=TIT, pad=7, altura=None, dash=None):
    """Caixa com título (semibold) e texto; devolve altura."""
    linhas = []
    if titulo:
        linhas += [(t, 600, tcolor) for t in quebra(titulo, tsize, w - 2 * pad, 600)]
    corpo = [(t, 400, TXT) for t in quebra(texto, size, w - 2 * pad)] if texto else []
    h_t = len([l for l in linhas]) * tsize * 1.32
    h_c = len(corpo) * size * 1.36
    h = pad * 2 + h_t + h_c + (2 if titulo and texto else 0)
    if altura:
        h = max(h, altura)
    return h, linhas, corpo


def desenha_caixa(s, x, y, w, h, linhas, corpo, size=8.4, tsize=8.8, fill="#FFFFFF", stroke=AZUL_B,
                  pad=7, dash=None, valign="middle"):
    s.rect(x, y, w, h, fill=fill, stroke=stroke, dash=dash)
    h_t = len(linhas) * tsize * 1.32
    h_c = len(corpo) * size * 1.36
    tot = h_t + h_c + (2 if linhas and corpo else 0)
    yy = y + (h - tot) / 2 if valign == "middle" else y + pad
    for t, pw, cor in linhas:
        yy += tsize * 1.32
        s.text(x + w / 2, yy - tsize * 0.32, t, tsize, pw, cor)
    if linhas and corpo:
        yy += 2
    for t, pw, cor in corpo:
        yy += size * 1.36
        s.text(x + w / 2, yy - size * 0.34, t, size, pw, cor)


# ---------------------------------------------------------------- trilha
def trilha():
    s = SVG()
    etapas = [
        ("Glomérulo", "o açúcar abre o filtro e lesa as arteríolas"),
        ("Quem adoece", "epidemia, custo e risco de morte"),
        ("Três fases", "incipiente, clínica e doença renal crônica"),
        ("Fatores de risco", "glicose, pressão, proteína, sal, herança"),
        ("Diagnóstico", "microalbuminúria e o que confunde"),
        ("Metas e dieta", "pressão, cigarro, colesterol, proteína"),
        ("Remédios", "bloqueio da angiotensina, gliflozinas, finerenona"),
        ("Outras doenças", "infecção, Candida e bexiga neurogênica"),
    ]
    cols, gap = 4, 14
    bw = (W - gap * (cols - 1)) / cols
    pad = 7
    # altura comum
    alt = 0
    for t, d in etapas:
        n = len(quebra(d, 7.8, bw - 2 * pad))
        alt = max(alt, 24 + n * 7.8 * 1.36 + pad)
    y0, rowgap = 2, 18
    pos = []
    for i, (t, d) in enumerate(etapas):
        r, c = divmod(i, cols)
        x = c * (bw + gap)
        y = y0 + r * (alt + rowgap)
        pos.append((x, y))
        s.rect(x, y, bw, alt, fill="#FFFFFF", stroke=AZUL_B, r=9)
        # selo numerado
        s.el.append(f'<circle cx="{x + 14:.1f}" cy="{y + 14:.1f}" r="8" fill="{AZ}"/>')
        s.text(x + 14, y + 17.2, str(i + 1), 8.5, 600, "#FFFFFF")
        s.text(x + 27, y + 17.4, t, 8.8, 600, TIT, anchor="start")
        yy = y + 24
        for ln in quebra(d, 7.8, bw - 2 * pad):
            yy += 7.8 * 1.36
            s.text(x + pad, yy - 2.6, ln, 7.8, 400, "#3A3A3C", anchor="start")
    # setas na linha 1 e 2
    for i in range(len(etapas) - 1):
        if i == cols - 1:
            continue
        x, y = pos[i]
        s.seta_h(x + bw + 2, x + bw + gap - 1, y + alt / 2)
    # da 4 para a 5: desce pela direita e volta pela esquerda
    x4, y4 = pos[3]
    x5, y5 = pos[4]
    ymid = y4 + alt + rowgap / 2
    s.caminho([(x4 + bw / 2, y4 + alt + 1), (x4 + bw / 2, ymid), (x5 + bw / 2, ymid)])
    s.seta_v(x5 + bw / 2, ymid, y5 - 1)
    h = y0 + 2 * alt + rowgap + 2
    s.salvar("trilha.svg", h)


# ---------------------------------------------------------------- fisiopatologia
def fisio():
    s = SVG()
    pad = 8
    # topo
    topo = ("Glicose em excesso filtrada pelo glomérulo", "")
    h, l, c = caixa_txt(s, 0, 0, 300, *topo, pad=6)
    x0 = (W - 300) / 2
    y = 2
    desenha_caixa(s, x0, y, 300, h, l, c)
    ytopo_fim = y + h
    colw, gap = 220, W - 2 * 220
    xl, xr = 0, W - colw
    esq = [("Glomérulo inflamado", "pelos polióis e pela própria glicose"),
           ("Os podócitos se abrem", "os poros do filtro ficam maiores"),
           ("Perda de proteína", "proteinúria (no começo, microalbuminúria)")]
    dir_ = [("Arteríolas do glomérulo lesadas", "o açúcar lesa a parede dos vasos pequenos"),
            ("Esclerose glomerular", "o glomérulo endurece e cicatriza"),
            ("Hipertensão", "a pressão arterial sobe")]
    # altura comum por linha
    yrow = ytopo_fim + 26
    # ramo: do topo desce e abre para os dois lados
    ym = ytopo_fim + 11
    s.caminho([(W / 2, ytopo_fim + 1), (W / 2, ym)])
    s.caminho([(xl + colw / 2, ym), (xr + colw / 2, ym)])
    s.seta_v(xl + colw / 2, ym, yrow - 1)
    s.seta_v(xr + colw / 2, ym, yrow - 1)
    for i in range(3):
        he, le, ce = caixa_txt(s, 0, 0, colw, *esq[i], pad=5)
        hd, ld, cd = caixa_txt(s, 0, 0, colw, *dir_[i], pad=5)
        hh = max(he, hd)
        desenha_caixa(s, xl, yrow, colw, hh, le, ce)
        desenha_caixa(s, xr, yrow, colw, hh, ld, cd)
        if i < 2:
            s.seta_v(xl + colw / 2, yrow + hh + 1, yrow + hh + 12)
            s.seta_v(xr + colw / 2, yrow + hh + 1, yrow + hh + 12)
            yrow += hh + 13
        else:
            yfim = yrow + hh
    # base: junta os dois
    yb = yfim + 24
    ym2 = yfim + 11
    s.caminho([(xl + colw / 2, yfim + 1), (xl + colw / 2, ym2), (xr + colw / 2, ym2), (xr + colw / 2, yfim + 1)])
    s.seta_v(W / 2, ym2, yb - 1)
    base = ("Proteinúria e hipertensão juntas",
            "a doença do diabetes é essencialmente vascular")
    hb, lb, cb = caixa_txt(s, 0, 0, 400, *base, pad=6)
    desenha_caixa(s, (W - 400) / 2, yb, 400, hb, lb, cb, fill=APOIO)
    s.salvar("fisio.svg", yb + hb + 2)


# ---------------------------------------------------------------- diagnóstico
def diag():
    s = SVG()
    y = 4
    topo = ("Paciente com diabetes", "pesquisar albumina na urina (microalbuminúria)")
    h, l, c = caixa_txt(s, 0, 0, 280, *topo)
    desenha_caixa(s, (W - 280) / 2, y, 280, h, l, c)
    yt = y + h
    colw = 222
    xl, xr = 0, W - colw
    ym = yt + 13
    s.caminho([(W / 2, yt + 1), (W / 2, ym)])
    s.caminho([(xl + colw / 2, ym), (xr + colw / 2, ym)])
    yrow = yt + 30
    s.seta_v(xl + colw / 2, ym, yrow - 1)
    s.seta_v(xr + colw / 2, ym, yrow - 1)
    e = ("Diabetes tipo 1", "primeiro exame a partir do 5º ano de doença")
    d = ("Diabetes tipo 2", "logo no diagnóstico: já chega com hipertensão e obesidade cedo")
    he, le, ce = caixa_txt(s, 0, 0, colw, *e)
    hd, ld, cd = caixa_txt(s, 0, 0, colw, *d)
    hh = max(he, hd)
    desenha_caixa(s, xl, yrow, colw, hh, le, ce)
    desenha_caixa(s, xr, yrow, colw, hh, ld, cd)
    yf = yrow + hh
    ym2 = yf + 13
    s.caminho([(xl + colw / 2, yf + 1), (xl + colw / 2, ym2), (xr + colw / 2, ym2), (xr + colw / 2, yf + 1)])
    y2 = yf + 30
    s.seta_v(W / 2, ym2, y2 - 1)
    mid = ("Repetir uma vez por ano", "nos dois tipos")
    h2, l2, c2 = caixa_txt(s, 0, 0, 280, *mid)
    desenha_caixa(s, (W - 280) / 2, y2, 280, h2, l2, c2)
    y3 = y2 + h2 + 18
    s.seta_v(W / 2, y2 + h2 + 1, y3 - 1)
    q = ("Albumina acima de 30 mg?", "")
    h3, l3, c3 = caixa_txt(s, 0, 0, 280, *q)
    desenha_caixa(s, (W - 280) / 2, y3, 280, h3, l3, c3, fill=APOIO)
    y4 = y3 + h3 + 18
    s.seta_v(W / 2, y3 + h3 + 1, y4 - 1)
    q4 = ("Antes de culpar o rim, afastar as outras causas",
          "infecção urinária, febre, hematúria, menstruação, gravidez, obesidade maciça, insuficiência cardíaca, exercício antes da coleta, mau controle metabólico")
    h4, l4, c4 = caixa_txt(s, 0, 0, 400, *q4)
    desenha_caixa(s, (W - 400) / 2, y4, 400, h4, l4, c4)
    y5 = y4 + h4 + 18
    s.seta_v(W / 2, y4 + h4 + 1, y5 - 1)
    q5 = ("Sem outra causa: nefropatia incipiente", "função renal ainda normal; é a hora de agir")
    h5, l5, c5 = caixa_txt(s, 0, 0, 300, *q5)
    desenha_caixa(s, (W - 300) / 2, y5, 300, h5, l5, c5)
    s.salvar("diag.svg", y5 + h5 + 4)


# ---------------------------------------------------------------- infecção com gliflozina
def infec():
    s = SVG()
    VB, VD, VT = "#E7F7EC", "#BFE5CB", "#1E7A34"
    y = 2
    topo = ("Infecção em quem usa gliflozina", "")
    h, l, c = caixa_txt(s, 0, 0, 280, *topo, pad=5)
    desenha_caixa(s, (W - 280) / 2, y, 280, h, l, c)
    yt = y + h
    colw = 226
    xl, xr = 0, W - colw
    ym = yt + 9
    s.caminho([(W / 2, yt + 1), (W / 2, ym)])
    s.caminho([(xl + colw / 2, ym), (xr + colw / 2, ym)])
    yrow = yt + 20
    s.seta_v(xl + colw / 2, ym, yrow - 1)
    s.seta_v(xr + colw / 2, ym, yrow - 1)
    e = ("Localizada", "balanopostite por fungo ou infecção urinária com pouca repercussão")
    d = ("Sinais de infecção sistêmica", "febre, taquicardia, enchimento capilar diminuído, palidez")
    he, le, ce = caixa_txt(s, 0, 0, colw, *e, pad=5)
    hd, ld, cd = caixa_txt(s, 0, 0, colw, *d, pad=5)
    hh = max(he, hd)
    desenha_caixa(s, xl, yrow, colw, hh, le, ce)
    desenha_caixa(s, xr, yrow, colw, hh, ld, cd)
    yf = yrow + hh
    y2 = yf + 12
    s.seta_v(xl + colw / 2, yf + 1, y2 - 1)
    s.seta_v(xr + colw / 2, yf + 1, y2 - 1)
    e2 = ("Pode manter o remédio", "e tratar a infecção")
    d2 = ("Suspende por 7 dias", "trata a infecção e depois retoma o remédio")
    he, le, ce = caixa_txt(s, 0, 0, colw, *e2, tcolor=VT, pad=5)
    hd, ld, cd = caixa_txt(s, 0, 0, colw, *d2, tcolor=VT, pad=5)
    hh = max(he, hd)
    desenha_caixa(s, xl, y2, colw, hh, le, ce, fill=VB, stroke=VD)
    desenha_caixa(s, xr, y2, colw, hh, ld, cd, fill=VB, stroke=VD)
    s.salvar("infec.svg", y2 + hh + 2)


# ---------------------------------------------------------------- bexiga neurogênica
def bexiga():
    s = SVG()
    etapas = [("Bexiga neurogênica", "a musculatura não elimina toda a urina"),
              ("Estase", "a bexiga fica distendida e sobra urina dentro dela"),
              ("Infecção urinária", "a urina parada facilita a infecção"),
              ("Piora da função renal", "uma das causas de o rim piorar")]
    n, gap = len(etapas), 16
    bw = (W - gap * (n - 1)) / n
    alt = 0
    medidas = []
    for t, d in etapas:
        h, l, c = caixa_txt(s, 0, 0, bw, t, d, pad=6)
        medidas.append((l, c))
        alt = max(alt, h)
    y = 2
    for i, (l, c) in enumerate(medidas):
        x = i * (bw + gap)
        desenha_caixa(s, x, y, bw, alt, l, c, fill=APOIO if i == n - 1 else "#FFFFFF")
        if i < n - 1:
            s.seta_h(x + bw + 2, x + bw + gap - 1, y + alt / 2)
    s.salvar("bexiga.svg", y + alt + 2)


if __name__ == "__main__":
    bexiga()
    trilha()
    fisio()
    diag()
    infec()
    print("ok")
