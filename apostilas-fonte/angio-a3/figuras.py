"""Desenha as figuras da apostila angio-a3 (SVG, largura 478pt).
Uso: python3 figuras.py  (na pasta da aula; usa fonts/ copiada pelo preparar.sh)
"""
import math
import os
from PIL import ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
F = {
    400: os.path.join(AQUI, "fonts", "Inter-Regular.ttf"),
    500: os.path.join(AQUI, "fonts", "Inter-Medium.ttf"),
    600: os.path.join(AQUI, "fonts", "Inter-SemiBold.ttf"),
    700: os.path.join(AQUI, "fonts", "Inter-Bold.ttf"),
}
_cache = {}
W = 478
AZUL_B = "#C3D8F8"   # borda das caixas
APOIO = "#F5F8FF"    # fundo de apoio
SETA = "#8AA9DF"
TXT = "#1F2933"
TIT = "#16315C"
AZUL = "#0B5BD3"


def font(peso, tam):
    k = (peso, tam)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(F[peso], tam)
    return _cache[k]


def larg(txt, peso, tam):
    return font(peso, tam).getlength(txt)


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


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def texto(x, y, s, peso=400, tam=8, cor=TXT, anc="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter" font-weight="{peso}" '
            f'font-size="{tam}" fill="{cor}" text-anchor="{anc}">{esc(s)}</text>')


def seta(x1, y1, x2, y2, cor=SETA, w=1.4, ponta=5.5):
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - ponta * math.cos(ang), y2 - ponta * math.sin(ang)
    px, py = -math.sin(ang), math.cos(ang)
    pts = [(x2, y2), (bx + px * ponta * 0.55, by + py * ponta * 0.55), (bx - px * ponta * 0.55, by - py * ponta * 0.55)]
    poly = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{cor}" stroke-width="{w}"/>'
            f'<polygon points="{poly}" fill="{cor}"/>')


def caixa_medida(w, titulo, corpo, tt=8.6, tc=7.8, pad=7):
    lt = quebra(titulo, 600, tt, w - 2 * pad) if titulo else []
    lc = quebra(corpo, 400, tc, w - 2 * pad) if corpo else []
    h = pad + len(lt) * tt * 1.3 + (3 if lt and lc else 0) + len(lc) * tc * 1.38 + pad - 2
    return lt, lc, h


def caixa(x, y, w, titulo, corpo, h=None, tt=8.6, tc=7.8, pad=7, borda=AZUL_B, fundo="#FFFFFF",
          bw=1, centro=False, cor_t=TIT, tracejada=False):
    lt, lc, hh = caixa_medida(w, titulo, corpo, tt, tc, pad)
    h = h or hh
    dash = ' stroke-dasharray="4 3"' if tracejada else ""
    out = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="7" fill="{fundo}" '
           f'stroke="{borda}" stroke-width="{bw}"{dash}/>']
    cy = y + pad + tt * 0.95
    ax = x + w / 2 if centro else x + pad
    anc = "middle" if centro else "start"
    for l in lt:
        out.append(texto(ax, cy, l, 600, tt, cor_t, anc))
        cy += tt * 1.3
    if lt and lc:
        cy += 3
    if lc:
        cy += tc * 0.05
    for l in lc:
        out.append(texto(ax, cy, l, 400, tc, TXT, anc))
        cy += tc * 1.38
    return "".join(out), h


def etiqueta(x, y, s, cor=AZUL):
    w = larg(s, 600, 7.4) + 8
    return (f'<rect x="{x - w / 2:.1f}" y="{y - 7:.1f}" width="{w:.1f}" height="11" rx="5.5" fill="#FFFFFF" '
            f'stroke="{AZUL_B}" stroke-width="0.8"/>' + texto(x, y + 1.2, s, 600, 7.4, cor, "middle"))


def salvar(nome, corpo, h):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{h:.0f}pt" '
           f'viewBox="0 0 {W} {h:.0f}">' + corpo + "</svg>")
    with open(os.path.join(AQUI, nome), "w", encoding="utf-8") as f:
        f.write(svg)
    print(nome, round(h))


def circulo_num(cx, cy, n, r=8, fundo=AZUL, cor="#FFFFFF"):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fundo}"/>'
            + texto(cx, cy + 3, str(n), 700, 8.2, cor, "middle"))


# ------------------------------------------------------------------ trilha
def trilha():
    etapas = [
        ("A placa", "uma doença do corpo inteiro"),
        ("Onde ela se instala", "aortoilíaca, femoropoplítea e distal"),
        ("Claudicação e evolução", "da dor ao caminhar até a gangrena"),
        ("Exame e índice", "pulsos, Doppler e índice tornozelo-braquial"),
        ("Exames de imagem", "só para quem vai a procedimento"),
        ("Mudança de vida", "caminhada, cigarro, dieta e metas"),
        ("Remédios", "as três drogas e a escada do colesterol"),
        ("Cirurgia", "quando operar, TASC, WIfI e amputação"),
    ]
    gap = 18
    w = (W - 3 * gap) / 4
    out = []
    alturas = []
    for t, c in etapas:
        nt = len(quebra(t, 600, 8.6, w - 32))
        nc = len(quebra(c, 400, 7.6, w - 14))
        cy = max(16 + nt * 11, 27) + 3 + nc * 10.4
        alturas.append(cy)
    hb = max(alturas) - 2
    y1, y2 = 4, 4 + hb + 30
    pos = []
    for i, (t, c) in enumerate(etapas):
        lin, col = divmod(i, 4)
        x = col * (w + gap)
        y = y1 if lin == 0 else y2
        pos.append((x, y))
        r = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{hb:.1f}" rx="8" fill="#FFFFFF" stroke="{AZUL_B}" stroke-width="1"/>'
        out.append(r)
        out.append(circulo_num(x + 13, y + 13, i + 1))
        lt = quebra(t, 600, 8.6, w - 32)
        lc = quebra(c, 400, 7.6, w - 14)
        cy = y + 16
        for l in lt:
            out.append(texto(x + 25, cy, l, 600, 8.6, TIT))
            cy += 11
        cy = max(cy, y + 27) + 3
        for l in lc:
            out.append(texto(x + 7, cy, l, 400, 7.6, TXT))
            cy += 10.4
    for i in range(7):
        x, y = pos[i]
        if i == 3:
            # volta para a segunda linha
            sx = x + w / 2
            out.append(f'<polyline points="{sx:.1f},{y + hb:.1f} {sx:.1f},{y + hb + 14:.1f} {w / 2:.1f},{y + hb + 14:.1f}" '
                       f'fill="none" stroke="{SETA}" stroke-width="1.4"/>')
            out.append(seta(w / 2, y + hb + 14, w / 2, y2))
        else:
            out.append(seta(x + w + 2, y + hb / 2, x + w + gap - 2, y + hb / 2))
    salvar("trilha.svg", "".join(out), y2 + hb + 4)


# ------------------------------------------------------------------ artérias
def arterias():
    out = []
    cx = 232
    bw = 150
    bx = cx - bw / 2
    rows = [
        ("Aorta", "bifurca na altura do umbigo"),
        ("Ilíaca comum", ""),
        ("Ilíaca externa", ""),
        ("Femoral comum", "depois do ligamento inguinal"),
        ("Femoral superficial", ""),
        ("Canal dos adutores", "a artéria dobra em espiral: lugar preferido da placa"),
        ("Poplítea", ""),
    ]
    y = 6
    ys = []
    gapv = 15
    for i, (t, c) in enumerate(rows):
        destaque = i == 5
        s, h = caixa(bx, y, bw, t, c, tt=8.6, tc=7.4, pad=6, centro=True,
                     borda=AZUL if destaque else AZUL_B, bw=1.6 if destaque else 1,
                     fundo=APOIO if destaque else "#FFFFFF")
        out.append(s)
        ys.append((y, h))
        y += h + gapv
    for i in range(len(rows) - 1):
        y0, h0 = ys[i]
        out.append(seta(cx, y0 + h0 + 1, cx, ys[i + 1][0] - 1))
    # ligamento inguinal (tracejado) entre ilíaca externa e femoral comum
    yl = ys[3][0] - gapv / 2
    out.append(f'<line x1="{bx - 14:.1f}" y1="{yl:.1f}" x2="{bx + bw + 14:.1f}" y2="{yl:.1f}" stroke="{TIT}" stroke-width="0.9" stroke-dasharray="3 2.5"/>')
    out.append(texto(bx + bw + 18, yl + 2.6, "ligamento inguinal", 500, 7.2, TIT))
    # ramos laterais à direita
    rx = bx + bw + 30
    rw = W - rx - 2
    # ilíaca interna (sai da ilíaca comum, ao lado da externa)
    yi, hi = ys[2]
    s, h = caixa(rx, yi - 4, rw, "Ilíaca interna", "", tt=8.4, pad=6)
    out.append(s)
    out.append(seta(cx + 20, ys[1][0] + ys[1][1], rx - 1, yi - 4 + h / 2))
    # femoral profunda
    yf, hf = ys[4]
    s, h = caixa(rx, yf - 10, rw, "Femoral profunda", "circulação colateral rica: uma das artérias mais importantes da coxa",
                 tt=8.4, tc=7.3, pad=6, borda=AZUL, bw=1.4)
    out.append(s)
    out.append(seta(cx + 20, ys[3][0] + ys[3][1], rx - 1, yf - 10 + h / 2))
    # três artérias da perna
    yp, hp = ys[6]
    yb = yp + hp + 26
    nomes = [("Tibial anterior", ""), ("Tibial posterior", ""),
             ("Fibular", "uma das mais importantes da perna: a última a entregar os pontos")]
    g = 9
    x0 = bx
    tws = [80, 80]
    tws.append(W - x0 - 2 * g - 2 - sum(tws))
    hs = [caixa_medida(tws[k], t, c, tt=8.4, tc=7.2, pad=6)[2] for k, (t, c) in enumerate(nomes)]
    hm = max(hs)
    x = x0
    for k, (t, c) in enumerate(nomes):
        tw = tws[k]
        s, _ = caixa(x, yb, tw, t, c, h=hm, tt=8.4, tc=7.2, pad=6, centro=True,
                     borda=AZUL if k == 2 else AZUL_B, bw=1.4 if k == 2 else 1)
        out.append(s)
        out.append(seta(cx, yp + hp + 1, x + tw / 2, yb - 1))
        x += tw + g
    # faixas dos segmentos à esquerda
    sx = 4
    sw = bx - 26 - sx
    segs = [
        (ys[0][0], ys[2][0] + ys[2][1], "Aortoilíaco", "Síndrome de Leriche"),
        (ys[3][0], ys[6][0] + ys[6][1], "Femoropoplíteo", "o mais comum"),
        (yb, yb + hm, "Distal", "mais nos diabéticos"),
    ]
    for (a, b, t, c) in segs:
        out.append(f'<rect x="{sx:.1f}" y="{a:.1f}" width="{sw:.1f}" height="{b - a:.1f}" rx="7" fill="{APOIO}" stroke="{AZUL_B}" stroke-width="0.8"/>')
        bxr = bx - 14
        out.append(f'<polyline points="{bxr - 6:.1f},{a + 2:.1f} {bxr:.1f},{a + 2:.1f} {bxr:.1f},{b - 2:.1f} {bxr - 6:.1f},{b - 2:.1f}" fill="none" stroke="{SETA}" stroke-width="1.2"/>')
        m = (a + b) / 2
        lt = quebra(t, 600, 8.6, sw - 10)
        lc = quebra(c, 400, 7.4, sw - 10)
        tot = len(lt) * 11 + len(lc) * 10
        cy = m - tot / 2 + 8
        for l in lt:
            out.append(texto(sx + sw / 2, cy, l, 600, 8.6, TIT, "middle"))
            cy += 11
        for l in lc:
            out.append(texto(sx + sw / 2, cy, l, 400, 7.4, TXT, "middle"))
            cy += 10
    salvar("arterias.svg", "".join(out), yb + hm + 6)


# ------------------------------------------------------------------ escada de Rutherford
def escada():
    out = []
    graus = [
        ("0", "Sem sintoma"),
        ("1", "Claudicação leve"),
        ("2", "Claudicação moderada"),
        ("3", "Claudicação grave"),
        ("4", "Dor em repouso"),
        ("5", "Lesão trófica menor"),
        ("6", "Lesão trófica maior: gangrena"),
    ]
    cores = ["#EEF3FD", "#DCE7FB", "#C3D8F8", "#A9C4EE", "#6F9BE0", "#3B78D8", "#0B5BD3"]
    g = 5
    cw = (W - 6 * g) / 7
    base = 118
    hmin, hmax = 26, 108
    for i, (n, nome) in enumerate(graus):
        x = i * (cw + g)
        h = hmin + (hmax - hmin) * i / 6
        y = base - h
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{h:.1f}" rx="6" fill="{cores[i]}" stroke="{AZUL_B}" stroke-width="0.8"/>')
        cor_n = "#FFFFFF" if i >= 4 else TIT
        out.append(texto(x + cw / 2, y + 19, n, 700, 15, cor_n, "middle"))
        cy = base + 12
        for l in quebra(nome, 500, 7.6, cw - 2):
            out.append(texto(x + cw / 2, cy, l, 500, 7.6, TXT, "middle"))
            cy += 9.8
    # grupos
    yg = base + 46
    grupos = [(1, 3, "Claudicação"), (4, 4, "Dor em repouso"), (5, 6, "Lesão trófica")]
    for a, b, t in grupos:
        x1 = a * (cw + g) + 2
        x2 = b * (cw + g) + cw - 2
        out.append(f'<polyline points="{x1:.1f},{yg - 6:.1f} {x1:.1f},{yg:.1f} {x2:.1f},{yg:.1f} {x2:.1f},{yg - 6:.1f}" fill="none" stroke="{SETA}" stroke-width="1.2"/>')
        out.append(texto((x1 + x2) / 2, yg + 12, t, 600, 8.4, TIT, "middle"))
    salvar("escada.svg", "".join(out), yg + 18)


# ------------------------------------------------------------------ ondas do Doppler
def ondas():
    out = []

    def gauss(t, c, s):
        return math.exp(-((t - c) ** 2) / (2 * s * s))

    def tri(t):
        return 1.0 * gauss(t, 10, 2.0) - 0.36 * gauss(t, 16.5, 2.2) + 0.17 * gauss(t, 24, 2.6)

    def bi(t):
        return 0.95 * gauss(t, 10, 2.4) - 0.30 * gauss(t, 17.5, 2.8)

    def mono(t):
        return 0.42 * gauss(t, 15, 5.5) + 0.10

    paineis = [
        (tri, "Trifásica", "normal na artéria periférica"),
        (bi, "Bifásica", "ateromatose; artéria envelhecida, que perdeu a mobilidade"),
        (mono, "Monofásica", "obstrução; nunca normal numa artéria periférica"),
    ]
    g = 12
    pw = (W - 2 * g) / 3
    top, alt = 6, 92
    zero = top + 58
    amp = 46
    for i, (f, t, c) in enumerate(paineis):
        x0 = i * (pw + g)
        out.append(f'<rect x="{x0:.1f}" y="{top:.1f}" width="{pw:.1f}" height="{alt:.1f}" rx="8" fill="{APOIO}" stroke="{AZUL_B}" stroke-width="0.8"/>')
        out.append(f'<line x1="{x0 + 8:.1f}" y1="{zero:.1f}" x2="{x0 + pw - 8:.1f}" y2="{zero:.1f}" stroke="{SETA}" stroke-width="0.8" stroke-dasharray="3 2.5"/>')
        pts = []
        L = 34.0
        n = 260
        for k in range(n + 1):
            tt = k / n * 2 * L
            v = f(tt % L)
            px = x0 + 10 + (pw - 20) * k / n
            py = zero - amp * v
            pts.append(f"{px:.1f},{py:.1f}")
        out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{AZUL}" stroke-width="1.6" stroke-linejoin="round"/>')
        cy = top + alt + 13
        out.append(texto(x0 + pw / 2, cy, t, 600, 8.8, TIT, "middle"))
        cy += 11
        for l in quebra(c, 400, 7.6, pw - 6):
            out.append(texto(x0 + pw / 2, cy, l, 400, 7.6, TXT, "middle"))
            cy += 10
    out.append(texto(4, top + 10, "", 400, 7, TXT))
    salvar("ondas.svg", "".join(out), top + alt + 13 + 11 + 22)


# ------------------------------------------------------------------ decisão
def decisao():
    out = []
    # topo
    tw = 270
    tx = (W - tw) / 2
    s, th = caixa(tx, 4, tw, "Paciente com doença arterial obstrutiva periférica",
                  "A pergunta que decide: o sintoma é importante?", centro=True, borda=AZUL, bw=1.4)
    out.append(s)
    ytop = 4 + th
    lw = 160
    rx = lw + 36
    rw = W - rx
    y1 = ytop + 30
    # colunas
    L = [
        ("Sem sintoma importante", "Sem sintoma, pouco sintoma ou claudicação que não limita (andar 200 metros não é limitante)"),
        ("Tratamento clínico", "Caminhada todos os dias, parar de fumar, dieta, os três remédios e o LDL na meta."),
        ("Melhorou?", "Andava 200 metros e passou a andar 400: segue no tratamento clínico, sem operar."),
    ]
    R1 = ("Sintoma importante", "Dor em repouso, lesão trófica ou claudicação limitante: não chega ao portão, não consegue trabalhar")
    R2 = ("Classificação WIfI", "Ferida profunda, isquemia crítica e infecção com sepse?")
    # medir e alinhar
    hL0 = caixa_medida(lw, *L[0])[2]
    hR1 = caixa_medida(rw, *R1)[2]
    h1 = max(hL0, hR1)
    s, _ = caixa(0, y1, lw, L[0][0], L[0][1], h=h1)
    out.append(s)
    s, _ = caixa(rx, y1, rw, R1[0], R1[1], h=h1)
    out.append(s)
    out.append(seta(tx + 40, ytop + 1, lw / 2, y1 - 1))
    out.append(seta(tx + tw - 40, ytop + 1, rx + rw / 2, y1 - 1))
    out.append(etiqueta((tx + 40 + lw / 2) / 2 - 6, (ytop + y1) / 2, "Não"))
    out.append(etiqueta((tx + tw - 40 + rx + rw / 2) / 2 + 6, (ytop + y1) / 2, "Sim"))
    # coluna esquerda
    y = y1 + h1 + 16
    yl = []
    for t, c in L[1:]:
        s, h = caixa(0, y, lw, t, c)
        out.append(s)
        out.append(seta(lw / 2, y - 15, lw / 2, y - 1))
        yl.append((y, h))
        y += h + 16
    fimL = y - 16
    # coluna direita
    y2 = y1 + h1 + 16
    s, h2 = caixa(rx, y2, rw, R2[0], R2[1])
    out.append(s)
    out.append(seta(rx + rw / 2, y2 - 15, rx + rw / 2, y2 - 1))
    y3 = y2 + h2 + 26
    aw = 80
    hA = caixa_medida(aw, "Amputação", "salva a vida do paciente")[2]
    tasw = rw - aw - 12
    hT = caixa_medida(tasw, "Classificação TASC", "decide o caminho da cirurgia")[2]
    h3 = max(hA, hT)
    s, _ = caixa(rx, y3, aw, "Amputação", "salva a vida do paciente", h=h3, borda=AZUL, bw=1.4)
    out.append(s)
    tx2 = rx + aw + 12
    s, _ = caixa(tx2, y3, tasw, "Classificação TASC", "decide o caminho da cirurgia", h=h3)
    out.append(s)
    out.append(seta(rx + rw / 2 - 30, y2 + h2 + 1, rx + aw / 2, y3 - 1))
    out.append(seta(rx + rw / 2 + 30, y2 + h2 + 1, tx2 + tasw / 2, y3 - 1))
    out.append(etiqueta(rx + aw / 2 + 22, y2 + h2 + 12, "Sim"))
    out.append(etiqueta(tx2 + tasw / 2 - 2, y2 + h2 + 12, "Não"))
    y4 = y3 + h3 + 18
    sw2 = (tasw - 8) / 2
    E = ("A e B: lesão curta", "endovascular, por dentro do vaso")
    A = ("C e D: lesão longa", "cirurgia aberta: ponte, de preferência com safena")
    hE = max(caixa_medida(sw2, *E, tc=7.4)[2], caixa_medida(sw2, *A, tc=7.4)[2])
    for k, (t, c) in enumerate([E, A]):
        x = tx2 + k * (sw2 + 8)
        s, _ = caixa(x, y4, sw2, t, c, h=hE, tc=7.4)
        out.append(s)
        out.append(seta(tx2 + tasw / 2, y3 + h3 + 1, x + sw2 / 2, y4 - 1))
    fimR = y4 + hE
    # piorou: seta tracejada da esquerda para a direita
    yp, hp = yl[0]
    ym = yp + hp / 2
    out.append(f'<line x1="{lw + 1:.1f}" y1="{ym:.1f}" x2="{rx - 7:.1f}" y2="{ym:.1f}" stroke="{SETA}" stroke-width="1.3" stroke-dasharray="3 2.5"/>')
    out.append(seta(rx - 8, ym, rx - 1, ym))
    out.append(texto((lw + rx) / 2, ym - 4, "piorou", 600, 7, AZUL, "middle"))
    salvar("decisao.svg", "".join(out), max(fimL, fimR) + 4)


if __name__ == "__main__":
    trilha()
    arterias()
    escada()
    ondas()
    decisao()
