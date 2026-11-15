#!/usr/bin/env python3
"""Figuras da apostila gastro-a7 (intestino irritável, divertículos, diarreias, doença inflamatória intestinal, endometriose).

Rode na pasta de trabalho (com a pasta fonts/ do preparar.sh):  python3 figuras.py
"""
import os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(AQUI, "fonts")
F = {
    "r": os.path.join(FONTS, "Inter-Regular.ttf"),
    "m": os.path.join(FONTS, "Inter-Medium.ttf"),
    "s": os.path.join(FONTS, "Inter-SemiBold.ttf"),
    "b": os.path.join(FONTS, "Inter-Bold.ttf"),
}
FAM = {"r": ("Inter", 400), "m": ("Inter Medium", 500), "s": ("Inter SemiBold", 600), "b": ("Inter", 700)}
_cache = {}

BORDA = "#C3D8F8"; APOIO = "#F5F8FF"; SETA = "#8AA9DF"; TXT = "#1F2933"; TIT = "#16315C"; AZUL = "#0B5BD3"; CINZA = "#6C6C70"
W = 478


def font(k, size):
    key = (k, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(F[k], size)
    return _cache[key]


def larg(txt, k, size):
    return font(k, size).getlength(txt)


def quebra(txt, k, size, maxw):
    linhas, atual = [], ""
    for p in txt.split():
        t = (atual + " " + p).strip()
        if larg(t, k, size) <= maxw:
            atual = t
        else:
            if atual:
                linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    return linhas


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def texto(x, y, s, k="r", size=8, cor=TXT, anchor="start"):
    fam, peso = FAM[k]
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-weight="{peso}" '
            f'font-size="{size}" fill="{cor}" text-anchor="{anchor}">{esc(s)}</text>')


def bloco(x, y, linhas, k="r", size=8, cor=TXT, lh=None, anchor="start"):
    lh = lh or size * 1.32
    return "".join(texto(x, y + i * lh, l, k, size, cor, anchor) for i, l in enumerate(linhas))


def caixa(x, y, w, h, fill="#FFFFFF", stroke=BORDA, r=7, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def seta_v(x, y1, y2, cor=SETA):
    """seta vertical para baixo, desenhada como polígono"""
    return (f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{y2-5:.1f}" stroke="{cor}" stroke-width="1.6"/>'
            f'<polygon points="{x-4:.1f},{y2-6:.1f} {x+4:.1f},{y2-6:.1f} {x:.1f},{y2:.1f}" fill="{cor}"/>')


def seta_h(x1, x2, y, cor=SETA):
    return (f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2-5:.1f}" y2="{y:.1f}" stroke="{cor}" stroke-width="1.6"/>'
            f'<polygon points="{x2-6:.1f},{y-4:.1f} {x2-6:.1f},{y+4:.1f} {x2:.1f},{y:.1f}" fill="{cor}"/>')


def svg(nome, h, corpo):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{h:.0f}pt" '
         f'viewBox="0 0 {W} {h:.0f}">{corpo}</svg>')
    with open(os.path.join(AQUI, nome), "w", encoding="utf-8") as f:
        f.write(s)


# ---------------------------------------------------------------- trilha
def trilha():
    nos = [
        ("01", "O que é e como reconhecer"),
        ("02", "Alarme, exames e tratamento"),
        ("03", "O divertículo e os nomes"),
        ("04", "Diverticulite aguda"),
        ("05", "Aguda e crônica"),
        ("06", "Crohn e retocolite"),
        ("07", "Tratamento e riscos"),
        ("08", "Endometriose intestinal"),
        ("09", "Bônus de provas"),
    ]
    x0, passo, yc = 27, 53, 40
    xs = [x0 + i * passo for i in range(len(nos))]
    c = []
    grupos = [(0, 1, "Intestino irritável"), (2, 3, "Divertículos"), (4, 4, "Diarreias"),
              (5, 6, "Doença inflamatória"), (7, 7, "Pelve"), (8, 8, "Revisão")]
    for a, b, nome in grupos:
        xa, xb = xs[a] - 22, xs[b] + 22
        c.append(caixa(xa, 1, xb - xa, 18, fill=APOIO, stroke=BORDA, r=6))
        c.append(texto((xa + xb) / 2, 13.2, nome, "s", 7.2 if a == b else 7.6, TIT, "middle"))
    c.append(f'<line x1="{xs[0]:.1f}" y1="{yc}" x2="{xs[-1]:.1f}" y2="{yc}" stroke="{SETA}" stroke-width="2"/>')
    for x, (n, rot) in zip(xs, nos):
        c.append(f'<circle cx="{x:.1f}" cy="{yc}" r="10.5" fill="#FFFFFF" stroke="{AZUL}" stroke-width="1.6"/>')
        c.append(texto(x, yc + 3.2, n, "s", 8, AZUL, "middle"))
        ls = quebra(rot, "m", 7.2, 49)
        c.append(bloco(x, yc + 22, ls, "m", 7.2, TXT, 9.2, "middle"))
    svg("trilha.svg", 84, "".join(c))


# ---------------------------------------------------------------- sequência do intestino irritável
def cadeia(nome, passos, size=8, lh=10.6, pad=7):
    """caixas lado a lado ligadas por setas; a última em destaque"""
    n = len(passos)
    vao = 14
    w = (W - vao * (n - 1)) / n
    ls = [quebra(p, "m", size, w - 2 * pad) for p in passos]
    h = max(len(l) for l in ls) * lh + 2 * pad
    c = []
    for i, l in enumerate(ls):
        x = i * (w + vao)
        ult = i == n - 1
        c.append(caixa(x, 0, w, h, fill=APOIO if ult else "#FFFFFF", stroke=AZUL if ult else BORDA, sw=1.3 if ult else 1))
        y0 = h / 2 - (len(l) - 1) * lh / 2 + 2.8
        c.append(bloco(x + w / 2, y0, l, "s" if ult else "m", size, TIT if ult else TXT, lh, "middle"))
        if not ult:
            c.append(seta_h(x + w + 1.5, x + w + vao - 1.5, h / 2))
    svg(nome, h + 1, "".join(c))


# ---------------------------------------------------------------- conduta pela classificação de Hinchey
def hinchey():
    linhas = [
        ("0 e Ia", "Inflamação só em volta do cólon, sem abscesso", "Casa: dieta líquida ou pastosa e analgesia. Antibiótico só para idoso, imunossuprimido, gestante ou proteína C reativa muito alta"),
        ("Ib", "Abscesso pequeno ao lado do cólon, menor que 4 cm", "Internação e antibiótico na veia, sem drenar"),
        ("II", "Abscesso na pelve ou à distância, maior que 4 cm", "Drenagem pela pele guiada por tomografia e antibiótico na veia"),
        ("III", "Pus espalhado pela barriga (peritonite purulenta)", "Cirurgia de urgência: operação de Hartmann"),
        ("IV", "Fezes espalhadas pela barriga (peritonite fecal)", "Cirurgia de urgência: operação de Hartmann. É o grau que mais mata"),
    ]
    x1, w1 = 0, 46
    x2, w2 = 54, 168
    x3, w3 = 244, 234
    size, lh, pad = 8, 10.6, 7
    c = []
    topo = "Dor embaixo e à esquerda com febre: tomografia do abdome para confirmar e dar o grau"
    c.append(caixa(0, 0, W, 24, fill=APOIO, stroke=BORDA, r=6))
    c.append(texto(W / 2, 15.5, topo, "s", 8.2, TIT, "middle"))
    y = 24 + 8
    c.append(texto(x1 + w1 / 2, y + 7, "Grau", "s", 7.2, CINZA, "middle"))
    c.append(texto(x2 + pad, y + 7, "O que a tomografia mostra", "s", 7.2, CINZA))
    c.append(texto(x3 + pad, y + 7, "Conduta", "s", 7.2, CINZA))
    y += 13
    for i, (g, d, k) in enumerate(linhas):
        ld = quebra(d, "r", size, w2 - 2 * pad)
        lk = quebra(k, "m", size, w3 - 2 * pad)
        h = max(len(ld), len(lk)) * lh + 2 * pad - 1
        c.append(f'<rect x="{x1}" y="{y:.1f}" width="{w1}" height="{h:.1f}" rx="7" fill="{AZUL}"/>')
        c.append(texto(x1 + w1 / 2, y + h / 2 + 3.2, g, "s", 9, "#FFFFFF", "middle"))
        c.append(caixa(x2, y, w2, h))
        c.append(bloco(x2 + pad, y + h / 2 - (len(ld) - 1) * lh / 2 + 2.8, ld, "r", size, TXT, lh))
        c.append(caixa(x3, y, w3, h, fill=APOIO, stroke=AZUL, sw=1.2))
        c.append(bloco(x3 + pad, y + h / 2 - (len(lk) - 1) * lh / 2 + 2.8, lk, "m", size, TIT, lh))
        c.append(seta_h(x2 + w2 + 2, x3 - 2, y + h / 2))
        if i < len(linhas) - 1:
            c.append(seta_v(x1 + w1 / 2, y + h + 1, y + h + 9))
        y += h + 10
    y -= 10
    y += 8
    fim = "Passadas 6 semanas da crise: colonoscopia para confirmar a cura e afastar câncer"
    c.append(caixa(0, y, W, 24, stroke=BORDA, dash="3 2", r=6))
    c.append(texto(W / 2, y + 15.5, fim, "m", 8.2, TXT, "middle"))
    svg("hinchey.svg", y + 25, "".join(c))


# ---------------------------------------------------------------- linha do tempo da diarreia
def diarreia_tempo():
    c = []
    ye = 30
    x0, x1 = 4, 474
    xa, xb = 150, 300     # 14 dias e 4 semanas
    c.append(f'<line x1="{x0}" y1="{ye}" x2="{x1-6}" y2="{ye}" stroke="{SETA}" stroke-width="2"/>')
    c.append(f'<polygon points="{x1-7},{ye-4.5} {x1-7},{ye+4.5} {x1},{ye}" fill="{SETA}"/>')
    for x, rot in ((xa, "14 dias"), (xb, "4 semanas")):
        c.append(f'<circle cx="{x}" cy="{ye}" r="5" fill="#FFFFFF" stroke="{AZUL}" stroke-width="1.6"/>')
        c.append(texto(x, ye - 11, rot, "s", 8.4, TIT, "middle"))
    c.append(texto(x0, ye - 11, "Começo", "s", 8.4, TIT, "start"))
    c.append(texto(x1, ye - 11, "tempo", "m", 7.4, CINZA, "end"))
    fases = [
        (x0, xa - 6 - x0, "Aguda: menos de 14 dias", "Vírus ou bactéria, quase sempre acaba sozinha. Hidratar e manter a comida, sem exames e sem antibiótico de rotina.", False),
        (xa + 6, xb - xa - 12, "Entre as duas", "Faixa sem nome na aula.", True),
        (xb + 6, x1 - xb - 6, "Crônica: mais de 4 semanas", "Nunca é banal: sempre investigar com exames de sangue, de fezes e de imagem.", False),
    ]
    yb = 44
    h = 0
    for x, w, t, d, cinza in fases:
        h = max(h, len(quebra(d, "r", 8, w - 16)) * 10.6 + 30)
    for x, w, t, d, cinza in fases:
        ls = quebra(d, "r", 8, w - 16)
        c.append(caixa(x, yb, w, h, fill="#F7F7FA" if cinza else "#FFFFFF", stroke="#E3E3E8" if cinza else BORDA))
        c.append(texto(x + 8, yb + 15, t, "s", 8.2, CINZA if cinza else AZUL))
        c.append(bloco(x + 8, yb + 28, ls, "r", 8, CINZA if cinza else TXT, 10.6))
    svg("diarreia-tempo.svg", yb + h + 1, "".join(c))


# ---------------------------------------------------------------- onde cada doença inflamatória pega
def crohn_rcu():
    """duas faixas do tubo digestivo: Crohn em saltos, retocolite contínua a partir do reto"""
    segs = [("Boca e esôfago", 62), ("Estômago", 50), ("Intestino delgado", 92), ("Íleo terminal e ceco", 84), ("Cólon", 110), ("Reto", 44), ("Ânus", 36)]
    x0 = 0
    c = []
    y = 12
    xs = []
    x = x0
    for nome, w in segs:
        xs.append((x, w))
        ls = quebra(nome, "m", 7, w - 4)
        c.append(bloco(x + w / 2, y - (len(ls) - 1) * 8.4, ls, "m", 7, CINZA, 8.4, "middle"))
        x += w
    tot = x
    def faixa(yy, titulo, cheios, nota):
        c.append(texto(0, yy - 5, titulo, "s", 8.4, TIT))
        for i, (xx, w) in enumerate(xs):
            c.append(f'<rect x="{xx+1:.1f}" y="{yy:.1f}" width="{w-2:.1f}" height="16" rx="4" fill="#FFFFFF" stroke="{BORDA}"/>')
        for (xx, w, forte) in cheios:
            c.append(f'<rect x="{xx:.1f}" y="{yy+2.5:.1f}" width="{w:.1f}" height="11" rx="3.5" fill="{AZUL if forte else "#8AA9DF"}"/>')
        c.append(texto(0, yy + 28, nota, "r", 7.8, TXT))
    # Crohn: manchas salteadas, a maior no íleo terminal e ceco
    cro = [(xs[0][0] + 20, 14, False), (xs[1][0] + 16, 16, False), (xs[2][0] + 14, 22, False), (xs[2][0] + 58, 16, False),
           (xs[3][0] + 8, 66, True), (xs[4][0] + 22, 20, False), (xs[4][0] + 70, 18, False), (xs[6][0] + 8, 20, False)]
    faixa(36, "Doença de Crohn", cro, "Da boca ao ânus, em saltos, com trechos sadios no meio. O ponto mais comum (azul forte) é a junção do íleo com o ceco.")
    # Retocolite: contínua do reto para cima
    rc = [(xs[4][0] + 30, xs[4][1] - 30 + xs[5][1] - 3, True)]
    faixa(92, "Retocolite ulcerativa", rc, "Só no cólon: começa sempre no reto e sobe sem pular nenhum trecho; pode tomar o cólon inteiro (pancolite).")
    svg("crohn-rcu.svg", 124, "".join(c))


if __name__ == "__main__":
    trilha()
    cadeia("sequencia-sii.svg", ["Disbiose (flora desequilibrada)", "Inflamação de baixo grau", "Intestino mais permeável", "Hipersensibilidade visceral", "Dor e mudança da evacuação"])
    hinchey()
    diarreia_tempo()
    crohn_rcu()
