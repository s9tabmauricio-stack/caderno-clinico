#!/usr/bin/env python3
"""Desenha as figuras SVG da apostila angio-a4 (Oclusão arterial aguda).
Uso: python3 figuras.py  (na pasta da apostila; usa fonts/ copiada pelo preparar.sh)
"""
import os
from PIL import ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = {
    400: os.path.join(AQUI, "fonts", "Inter-Regular.ttf"),
    500: os.path.join(AQUI, "fonts", "Inter-Medium.ttf"),
    600: os.path.join(AQUI, "fonts", "Inter-SemiBold.ttf"),
    700: os.path.join(AQUI, "fonts", "Inter-Bold.ttf"),
}
_cache = {}

W = 478
AZUL_BORDA = "#C3D8F8"
APOIO = "#F5F8FF"
SETA = "#8AA9DF"
TEXTO = "#1F2933"
TITULO = "#16315C"
AZUL = "#0B5BD3"
CINZA = "#6C6C70"


def fonte(peso, tam):
    k = (peso, tam)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(FONTES[peso], tam)
    return _cache[k]


def larg(txt, tam, peso=400):
    return fonte(peso, tam).getlength(txt)


def quebra(txt, tam, maxw, peso=400):
    linhas, atual = [], ""
    for p in txt.split():
        t = (atual + " " + p).strip()
        if larg(t, tam, peso) <= maxw or not atual:
            atual = t
        else:
            linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    return linhas


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def texto(x, y, t, tam, peso=400, cor=TEXTO, anc="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter" font-size="{tam}" '
            f'font-weight="{peso}" fill="{cor}" text-anchor="{anc}">{esc(t)}</text>')


def seta_v(x, y1, y2, cor=SETA):
    """seta vertical para baixo, de y1 até a ponta em y2"""
    return (f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{y2-5:.1f}" stroke="{cor}" stroke-width="1.6"/>'
            f'<polygon points="{x-4:.1f},{y2-6:.1f} {x+4:.1f},{y2-6:.1f} {x:.1f},{y2:.1f}" fill="{cor}"/>')


def seta_h(x1, x2, y, cor=SETA):
    return (f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2-5:.1f}" y2="{y:.1f}" stroke="{cor}" stroke-width="1.6"/>'
            f'<polygon points="{x2-6:.1f},{y-4:.1f} {x2-6:.1f},{y+4:.1f} {x2:.1f},{y:.1f}" fill="{cor}"/>')


def bloco_txt(titulo, corpo, w, tt=8.6, tc=7.8, pad=8):
    """devolve (linhas_titulo, linhas_corpo, altura)"""
    lt = quebra(titulo, tt, w - 2 * pad, 600) if titulo else []
    lc = quebra(corpo, tc, w - 2 * pad, 400) if corpo else []
    h = pad + len(lt) * (tt * 1.3) + (3 if lt and lc else 0) + len(lc) * (tc * 1.38) + pad - 2
    return lt, lc, h


def caixa(x, y, w, h, titulo, corpo, tt=8.6, tc=7.8, pad=8, tracejada=False, fundo="#FFFFFF", centro=False):
    lt, lc, _ = bloco_txt(titulo, corpo, w, tt, tc, pad)
    dash = ' stroke-dasharray="4 3"' if tracejada else ""
    s = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="7" fill="{fundo}" stroke="{AZUL_BORDA if not tracejada else SETA}" stroke-width="1.1"{dash}/>']
    cy = y + pad + tt * 0.95
    ax = x + w / 2 if centro else x + pad
    anc = "middle" if centro else "start"
    for l in lt:
        s.append(texto(ax, cy, l, tt, 600, TITULO, anc))
        cy += tt * 1.3
    if lt and lc:
        cy += 3
    if not lt:
        cy = y + pad + tc * 0.95
    for l in lc:
        s.append(texto(ax, cy, l, tc, 400, TEXTO, anc))
        cy += tc * 1.38
    return "".join(s)


def selo(cx, cy, n, r=7.5):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{AZUL}"/>'
            + texto(cx, cy + 2.9, str(n), 8, 600, "#FFFFFF", "middle"))


def svg(h, corpo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{h:.0f}pt" '
            f'viewBox="0 0 {W} {h:.0f}">' + "".join(corpo) + "</svg>\n")


def salvar(nome, h, corpo):
    with open(os.path.join(AQUI, nome), "w", encoding="utf-8") as f:
        f.write(svg(h, corpo))


# ---------------------------------------------------------------- trilha
def trilha():
    etapas = [
        ("Gravidade", "doença prévia, colateral e idade"),
        ("5 Ps e relógio", "nervo, músculo e pele"),
        ("Embolia ou trombose?", "o perfil na anamnese"),
        ("Fator tempo", "quando salvar a perna mata"),
        ("Diagnóstico e conduta", "não atrasar; heparina se longe"),
        ("Rutherford", "viável, ameaçado ou inviável"),
        ("Embolia: Fogarty", "artéria sadia: tirar o êmbolo com o balonete"),
        ("Reperfusão", "mau prognóstico e fasciotomia"),
        ("Trombose arterial", "artéria doente: cirurgia planejada, ponte ou endovascular"),
    ]
    s = []
    gap = 14
    bw = (W - 4 * gap) / 5
    pad = 8
    # linha 1: etapas 1 a 5
    alts = []
    for i in range(5):
        lt, lc, h = bloco_txt(etapas[i][0], etapas[i][1], bw - 12, 8.4, 7.3, pad)
        alts.append(h + 12)
    h1 = max(alts)
    y1 = 2
    for i in range(5):
        x = i * (bw + gap)
        s.append(f'<rect x="{x:.1f}" y="{y1}" width="{bw:.1f}" height="{h1:.1f}" rx="8" fill="#FFFFFF" stroke="{AZUL_BORDA}" stroke-width="1.1"/>')
        s.append(selo(x + 12, y1 + 12, i + 1))
        lt, lc, _ = bloco_txt(etapas[i][0], etapas[i][1], bw - 12, 8.4, 7.3, pad)
        cy = y1 + 30
        for l in lt:
            s.append(texto(x + pad, cy, l, 8.4, 600, TITULO)); cy += 8.4 * 1.3
        cy += 2
        for l in lc:
            s.append(texto(x + pad, cy, l, 7.3, 400, CINZA)); cy += 7.3 * 1.38
        if i < 4:
            s.append(seta_h(x + bw + 2, x + bw + gap - 2, y1 + h1 / 2))
    alts[:] = []
    # conector da etapa 5 para a 6
    x5c = 4 * (bw + gap) + bw / 2
    yb = y1 + h1
    ycanal = yb + 12
    y2 = ycanal + 12
    w6 = bw
    x6c = w6 / 2
    s.append(f'<polyline points="{x5c:.1f},{yb:.1f} {x5c:.1f},{ycanal:.1f} {x6c:.1f},{ycanal:.1f}" fill="none" stroke="{SETA}" stroke-width="1.6"/>')
    s.append(seta_v(x6c, ycanal, y2))
    # linha 2: etapa 6, ramo embolia (7, 8) e ramo trombose (9)
    xr = w6 + 54
    wr = (W - xr - gap) / 2
    lt6, lc6, h6 = bloco_txt(etapas[5][0], etapas[5][1], w6 - 12, 8.4, 7.3, pad)
    hs = []
    for k in (6, 7):
        hs.append(bloco_txt(etapas[k][0], etapas[k][1], wr - 12, 8.4, 7.3, pad)[2] + 12)
    h7 = max(hs)
    h9 = bloco_txt(etapas[8][0], etapas[8][1], W - xr - 12, 8.4, 7.3, pad)[2] + 12
    y9 = y2 + h7 + 12
    htot6 = y9 + h9 - y2
    # etapa 6 ocupa as duas faixas
    s.append(f'<rect x="0" y="{y2:.1f}" width="{w6:.1f}" height="{htot6:.1f}" rx="8" fill="#FFFFFF" stroke="{AZUL_BORDA}" stroke-width="1.1"/>')
    s.append(selo(12, y2 + 12, 6))
    cy = y2 + 30
    for l in lt6:
        s.append(texto(pad, cy, l, 8.4, 600, TITULO)); cy += 8.4 * 1.3
    cy += 2
    for l in lc6:
        s.append(texto(pad, cy, l, 7.3, 400, CINZA)); cy += 7.3 * 1.38

    def etapa(x, y, w, h, n, trac=False):
        lt, lc, _ = bloco_txt(etapas[n - 1][0], etapas[n - 1][1], w - 12, 8.4, 7.3, pad)
        dash = ' stroke-dasharray="4 3"' if trac else ""
        cor = SETA if trac else AZUL_BORDA
        out = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="8" fill="#FFFFFF" stroke="{cor}" stroke-width="1.1"{dash}/>',
               selo(x + 12, y + 12, n)]
        cy = y + 30
        for l in lt:
            out.append(texto(x + pad, cy, l, 8.4, 600, TITULO)); cy += 8.4 * 1.3
        cy += 2
        for l in lc:
            out.append(texto(x + pad, cy, l, 7.3, 400, CINZA)); cy += 7.3 * 1.38
        return "".join(out)

    s.append(etapa(xr, y2, wr, h7, 7))
    s.append(seta_h(xr + wr + 2, xr + wr + gap - 2, y2 + h7 / 2))
    s.append(etapa(xr + wr + gap, y2, wr, h7, 8))
    s.append(etapa(xr, y9, W - xr, h9, 9, trac=True))
    # ramos saindo da etapa 6
    ym7 = y2 + h7 / 2
    ym9 = y9 + h9 / 2
    xs = w6 + 2
    xm = w6 + 14
    s.append(f'<line x1="{xs:.1f}" y1="{(ym7+ym9)/2:.1f}" x2="{xm:.1f}" y2="{(ym7+ym9)/2:.1f}" stroke="{SETA}" stroke-width="1.6"/>')
    s.append(f'<line x1="{xm:.1f}" y1="{ym7:.1f}" x2="{xm:.1f}" y2="{ym9:.1f}" stroke="{SETA}" stroke-width="1.6"/>')
    s.append(seta_h(xm, xr - 2, ym7))
    s.append(seta_h(xm, xr - 2, ym9))
    s.append(texto(xm + 3, ym7 - 4, "embolia", 6.6, 500, CINZA))
    s.append(texto(xm + 3, ym9 - 4, "trombose", 6.6, 500, CINZA))
    salvar("trilha.svg", y9 + h9 + 2, s)


# ---------------------------------------------------------------- relógio da isquemia
def relogio():
    s = []
    cols = [
        ("2 h", "Nervo", "Começa a formigar a perna: parestesia. Com 2 a 3 horas, o nervo já está comprometido."),
        ("12 h", "Músculo", "O músculo fica rígido."),
        ("24 h", "Pele", "A pele começa a fazer flictenas e bolhas."),
    ]
    gap = 12
    cw = (W - 2 * gap) / 3
    # eixo do tempo
    ya = 16
    s.append(texto(0, 8, "Oclusão", 7.2, 500, CINZA))
    s.append(texto(W, 8, "tempo de isquemia", 7.2, 500, CINZA, "end"))
    s.append(f'<line x1="2" y1="{ya}" x2="{W-8}" y2="{ya}" stroke="{SETA}" stroke-width="2.2"/>')
    s.append(f'<polygon points="{W-9},{ya-5} {W-9},{ya+5} {W},{ya}" fill="{SETA}"/>')
    s.append(f'<circle cx="3" cy="{ya}" r="3.5" fill="{SETA}"/>')
    hmax = 0
    for i, (t, tit, corpo) in enumerate(cols):
        lc = quebra(corpo, 8.2, cw - 20, 400)
        h = 12 + 16 + 8 + 13 + len(lc) * 8.2 * 1.42 + 6
        hmax = max(hmax, h)
    yc = ya + 18
    for i, (t, tit, corpo) in enumerate(cols):
        x = i * (cw + gap)
        cx = x + cw / 2
        s.append(f'<circle cx="{cx:.1f}" cy="{ya}" r="5" fill="{AZUL}"/>')
        s.append(f'<line x1="{cx:.1f}" y1="{ya+5}" x2="{cx:.1f}" y2="{yc}" stroke="{SETA}" stroke-width="1.2"/>')
        s.append(f'<rect x="{x:.1f}" y="{yc}" width="{cw:.1f}" height="{hmax:.1f}" rx="8" fill="#FFFFFF" stroke="{AZUL_BORDA}" stroke-width="1.1"/>')
        s.append(texto(x + 10, yc + 24, t, 16, 700, TITULO))
        s.append(texto(x + 10 + larg(t, 16, 700) + 7, yc + 23, tit, 10, 600, AZUL))
        cy = yc + 42
        for l in quebra(corpo, 8.2, cw - 20, 400):
            s.append(texto(x + 10, cy, l, 8.2, 400, TEXTO)); cy += 8.2 * 1.42
    # caixa de apoio
    yb = yc + hmax + 10
    nota = ("Ordem de resistência à isquemia: o nervo é o primeiro a sofrer e a pele, a última. "
            "Se a pele já morreu, o músculo embaixo dela está ainda pior.")
    ln = quebra(nota, 8.2, W - 24, 400)
    hb = 10 + len(ln) * 8.2 * 1.42 + 6
    s.append(f'<rect x="0" y="{yb:.1f}" width="{W}" height="{hb:.1f}" rx="8" fill="{APOIO}" stroke="{AZUL_BORDA}" stroke-width="1"/>')
    cy = yb + 16
    for l in ln:
        s.append(texto(12, cy, l, 8.2, 400, TEXTO)); cy += 8.2 * 1.42
    salvar("relogio.svg", yb + hb + 1, s)


# ---------------------------------------------------------------- cateter de Fogarty
def fogarty():
    s = []
    gap = 12
    pw = (W - gap) / 2
    ph = 100
    legendas = [
        "Incisão transversal na artéria sadia",
        "O cateter passa desinsuflado além do êmbolo",
        "Insufla o balonete depois do êmbolo",
        "Puxa insuflado: o êmbolo sai pela incisão",
    ]
    PAREDE = SETA
    COAG = "#4F5B70"
    CAT = TITULO

    def coagulo(x0, x1, yt, yb):
        # massa irregular ocupando a luz
        mid = (yt + yb) / 2
        return (f'<path d="M{x0},{mid} C{x0},{yt+1} {x0+8},{yt+0.5} {x0+14},{yt+1.2} '
                f'S{x1-10},{yt+0.4} {x1-4},{yt+1.5} C{x1+2},{yt+4} {x1+3},{yb-4} {x1-3},{yb-1.2} '
                f'S{x0+12},{yb-0.4} {x0+6},{yb-1} C{x0+1},{yb-3} {x0-1},{mid+3} {x0},{mid} Z" fill="{COAG}"/>')

    for i in range(4):
        ox = (i % 2) * (pw + gap)
        oy = (i // 2) * (ph + 10)
        s.append(f'<rect x="{ox:.1f}" y="{oy:.1f}" width="{pw:.1f}" height="{ph}" rx="8" fill="#FFFFFF" stroke="{AZUL_BORDA}" stroke-width="1.1"/>')
        yt, yb = oy + 34, oy + 58
        ax0, ax1 = ox + 10, ox + pw - 10
        inc0, inc1 = ox + 40, ox + 50
        # luz da artéria
        s.append(f'<rect x="{ax0:.1f}" y="{yt}" width="{ax1-ax0:.1f}" height="{yb-yt}" fill="{APOIO}"/>')
        # paredes (a de cima com a abertura da incisão)
        s.append(f'<line x1="{ax0:.1f}" y1="{yt}" x2="{inc0:.1f}" y2="{yt}" stroke="{PAREDE}" stroke-width="3"/>')
        s.append(f'<line x1="{inc1:.1f}" y1="{yt}" x2="{ax1:.1f}" y2="{yt}" stroke="{PAREDE}" stroke-width="3"/>')
        s.append(f'<line x1="{ax0:.1f}" y1="{yb}" x2="{ax1:.1f}" y2="{yb}" stroke="{PAREDE}" stroke-width="3"/>')
        # lábios da incisão
        s.append(f'<circle cx="{inc0:.1f}" cy="{yt}" r="1.5" fill="{PAREDE}"/><circle cx="{inc1:.1f}" cy="{yt}" r="1.5" fill="{PAREDE}"/>')
        mid = (yt + yb) / 2
        if i < 3:
            s.append(coagulo(ox + 108, ox + 158, yt + 1.5, yb - 1.5))
        if i == 0:
            s.append(texto(ox + 133, yb + 14, "êmbolo", 7.4, 500, CINZA, "middle"))
            s.append(texto(ox + 45, yt - 10, "incisão transversal", 7.4, 500, CINZA, "start"))
        if i in (1, 2):
            # cateter entrando pela incisão e correndo no centro da luz
            tip = ox + 190
            s.append(f'<path d="M{inc0-6:.1f},{oy+8} C{inc0+2:.1f},{yt-8} {inc0+6:.1f},{mid-2} {inc0+20:.1f},{mid} L{tip:.1f},{mid}" '
                     f'fill="none" stroke="{CAT}" stroke-width="1.8"/>')
            if i == 1:
                s.append(f'<ellipse cx="{tip+4:.1f}" cy="{mid}" rx="6" ry="2.6" fill="{AZUL_BORDA}" stroke="{AZUL}" stroke-width="1"/>')
                s.append(texto(tip + 4, yb + 14, "balonete vazio", 7.4, 500, CINZA, "middle"))
            else:
                s.append(f'<ellipse cx="{tip+4:.1f}" cy="{mid}" rx="10" ry="{(yb-yt)/2-1.5:.1f}" fill="{AZUL_BORDA}" stroke="{AZUL}" stroke-width="1.2"/>')
                s.append(texto(tip + 4, yb + 14, "balonete cheio", 7.4, 500, CINZA, "middle"))
        if i == 3:
            bx = ox + 86
            s.append(f'<path d="M{inc0-6:.1f},{oy+8} C{inc0+2:.1f},{yt-8} {inc0+6:.1f},{mid-2} {inc0+20:.1f},{mid} L{bx:.1f},{mid}" '
                     f'fill="none" stroke="{CAT}" stroke-width="1.8"/>')
            # êmbolo empurrado à frente do balonete, saindo pela incisão
            s.append(coagulo(ox + 52, ox + 74, yt + 1.5, yb - 1.5))
            s.append(f'<ellipse cx="{inc0+4:.1f}" cy="{yt-9}" rx="7" ry="4.2" fill="{COAG}"/>')
            s.append(f'<ellipse cx="{inc0+14:.1f}" cy="{yt-16}" rx="5" ry="3.2" fill="{COAG}"/>')
            s.append(f'<ellipse cx="{bx+6:.1f}" cy="{mid}" rx="10" ry="{(yb-yt)/2-1.5:.1f}" fill="{AZUL_BORDA}" stroke="{AZUL}" stroke-width="1.2"/>')
            x1, x2 = ox + 160, ox + 112
            s.append(f'<line x1="{x1:.1f}" y1="{mid}" x2="{x2+5:.1f}" y2="{mid}" stroke="{SETA}" stroke-width="1.6"/>'
                     f'<polygon points="{x2+6:.1f},{mid-4} {x2+6:.1f},{mid+4} {x2:.1f},{mid}" fill="{SETA}"/>')
            s.append(texto(ox + 130, yb + 14, "sentido da tração", 7.4, 500, CINZA, "middle"))
        # selo e legenda
        s.append(selo(ox + 14, oy + ph - 14, i + 1))
        s.append(texto(ox + 27, oy + ph - 11, legendas[i], 8.2, 600, TITULO))
    salvar("fogarty.svg", 2 * ph + 10 + 1, s)


# ---------------------------------------------------------------- decisão
def decisao():
    s = []
    pad = 8
    tt, tc = 8.6, 7.8
    y = 1
    # linha A
    a_t = "Membro pálido, com dor, parestesia, paralisia e sem pulso"
    a_c = "Os 5 Ps: oclusão arterial aguda."
    _, _, ha = bloco_txt(a_t, a_c, W, tt, tc, pad)
    s.append(caixa(0, y, W, ha, a_t, a_c, tt, tc, pad, centro=True))
    y += ha
    s.append(seta_v(W / 2, y + 2, y + 14)); y += 14
    b_t = "Quanto tempo de evolução? Viável, ameaçado ou inviável?"
    b_c = "Classificação de Rutherford e exames de sangue (creatinina, potássio, enzimas musculares, gasometria)."
    _, _, hb = bloco_txt(b_t, b_c, W, tt, tc, pad)
    s.append(caixa(0, y, W, hb, b_t, b_c, tt, tc, pad, centro=True))
    y += hb
    lw, gap = 316, 16
    rw = W - lw - gap
    rx = lw + gap
    lc_x, rc_x = lw / 2, rx + rw / 2
    # bifurcação
    yj = y + 9
    s.append(f'<line x1="{W/2:.1f}" y1="{y+1:.1f}" x2="{W/2:.1f}" y2="{yj:.1f}" stroke="{SETA}" stroke-width="1.6"/>')
    s.append(f'<line x1="{lc_x:.1f}" y1="{yj:.1f}" x2="{rc_x:.1f}" y2="{yj:.1f}" stroke="{SETA}" stroke-width="1.6"/>')
    s.append(seta_v(lc_x, yj, yj + 11))
    s.append(seta_v(rc_x, yj, yj + 11))
    y = yj + 11
    # linha C
    c1_t, c1_c = "Viável ou ameaçado", "Classes I, IIa e IIb: ainda dá para salvar o membro."
    c2_t, c2_c = "Inviável", "Classe III, rigor mortis; ou muitas horas, com rigidez, creatinina, potássio e enzimas altos e acidose."
    h1 = bloco_txt(c1_t, c1_c, lw, tt, tc, pad)[2]
    h2 = bloco_txt(c2_t, c2_c, rw, tt, tc, pad)[2]
    s.append(caixa(0, y, lw, h1, c1_t, c1_c, tt, tc, pad))
    s.append(caixa(rx, y, rw, h2, c2_t, c2_c, tt, tc, pad))
    yr = y + h2  # base da caixa da direita
    y += h1
    s.append(seta_v(lc_x, y + 2, y + 14)); y += 14
    d_t = "Centro cirúrgico já, sem esperar exame de fora"
    d_c = "Angiografia na mesa. Centro cirúrgico longe: heparina, algodão, não elevar o membro, sem vasodilatador, enquanto transfere."
    hd = bloco_txt(d_t, d_c, lw, tt, tc, pad)[2]
    s.append(caixa(0, y, lw, hd, d_t, d_c, tt, tc, pad))
    y += hd
    ew = (lw - 12) / 2
    e1x, e2x = 0, ew + 12
    yj2 = y + 8
    s.append(f'<line x1="{lc_x:.1f}" y1="{y+1:.1f}" x2="{lc_x:.1f}" y2="{yj2:.1f}" stroke="{SETA}" stroke-width="1.6"/>')
    s.append(f'<line x1="{ew/2:.1f}" y1="{yj2:.1f}" x2="{e2x+ew/2:.1f}" y2="{yj2:.1f}" stroke="{SETA}" stroke-width="1.6"/>')
    s.append(seta_v(ew / 2, yj2, yj2 + 11))
    s.append(seta_v(e2x + ew / 2, yj2, yj2 + 11))
    y = yj2 + 11
    e1_t, e1_c = "Embolia: artéria sadia", "Fogarty por incisão transversal; angiografia para conferir."
    e2_t, e2_c = "Trombose: artéria com placa", "Cirurgia planejada: ponte com a safena ou endovascular."
    he = max(bloco_txt(e1_t, e1_c, ew, tt, tc, pad)[2], bloco_txt(e2_t, e2_c, ew, tt, tc, pad)[2])
    s.append(caixa(e1x, y, ew, he, e1_t, e1_c, tt, tc, pad))
    s.append(caixa(e2x, y, ew, he, e2_t, e2_c, tt, tc, pad))
    y += he
    yj3 = y + 8
    s.append(f'<line x1="{ew/2:.1f}" y1="{y+1:.1f}" x2="{ew/2:.1f}" y2="{yj3:.1f}" stroke="{SETA}" stroke-width="1.6"/>')
    s.append(f'<line x1="{e2x+ew/2:.1f}" y1="{y+1:.1f}" x2="{e2x+ew/2:.1f}" y2="{yj3:.1f}" stroke="{SETA}" stroke-width="1.6"/>')
    s.append(f'<line x1="{ew/2:.1f}" y1="{yj3:.1f}" x2="{e2x+ew/2:.1f}" y2="{yj3:.1f}" stroke="{SETA}" stroke-width="1.6"/>')
    s.append(seta_v(lc_x, yj3, yj3 + 11))
    y = yj3 + 11
    f_t = "Depois de revascularizar: vigiar a reperfusão"
    f_c = "Dor fora da proporção, parestesia, perna dura: fasciotomia."
    hf = bloco_txt(f_t, f_c, lw, tt, tc, pad)[2]
    g_t, g_c = "Amputação", "Revascularizar mataria o paciente."
    hg = bloco_txt(g_t, g_c, rw, tt, tc, pad)[2]
    hfg = max(hf, hg)
    s.append(caixa(0, y, lw, hfg, f_t, f_c, tt, tc, pad))
    s.append(caixa(rx, y, rw, hfg, g_t, g_c, tt, tc, pad))
    s.append(seta_v(rc_x, yr + 2, y))
    salvar("decisao.svg", y + hfg + 1, s)


if __name__ == "__main__":
    trilha()
    relogio()
    fogarty()
    decisao()
    print("figuras: trilha.svg relogio.svg fogarty.svg decisao.svg")
