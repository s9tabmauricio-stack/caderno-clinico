"""Figuras da apostila nefro-a7 (Hipertensão arterial). Gera os SVGs na pasta atual.

Uso: python3 figuras.py   (na pasta de trabalho, com a pasta fonts/ copiada pelo preparar.sh)
"""
from PIL import ImageFont
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
W = 478
AZUL_BORDA = "#C3D8F8"
APOIO = "#F5F8FF"
SETA = "#8AA9DF"
TXT = "#1F2933"
TIT = "#16315C"
AZUL = "#0B5BD3"
CINZA = "#6C6C70"
PESOS = {400: "Inter-Regular.ttf", 500: "Inter-Medium.ttf", 600: "Inter-SemiBold.ttf", 700: "Inter-Bold.ttf"}
_cache = {}


def fonte(peso, tam):
    k = (peso, tam)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(os.path.join(AQUI, "fonts", PESOS[peso]), tam)
    return _cache[k]


def largura(txt, tam, peso=400):
    return fonte(peso, tam).getlength(txt)


def quebrar(txt, maxw, tam, peso=400):
    linhas, atual = [], ""
    for p in txt.split():
        t = (atual + " " + p).strip()
        if largura(t, tam, peso) <= maxw or not atual:
            atual = t
        else:
            linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    return linhas


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class SVG:
    def __init__(self):
        self.el = []

    def rect(self, x, y, w, h, fill="#FFFFFF", stroke=AZUL_BORDA, rx=8, sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def texto(self, x, y, t, tam=8.5, peso=400, cor=TXT, anchor="start"):
        self.el.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter" font-size="{tam}" font-weight="{peso}" fill="{cor}" text-anchor="{anchor}">{esc(t)}</text>')

    def linhas(self, x, y, linhas, tam=8.5, peso=400, cor=TXT, anchor="start", lh=None):
        lh = lh or tam * 1.3
        for i, l in enumerate(linhas):
            self.texto(x, y + i * lh, l, tam, peso, cor, anchor)

    def linha(self, x1, y1, x2, y2, cor=SETA, sw=1.4, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{cor}" stroke-width="{sw}"{d}/>')

    def caminho(self, d, cor=SETA, sw=1.4):
        self.el.append(f'<path d="{d}" fill="none" stroke="{cor}" stroke-width="{sw}"/>')

    def ponta(self, x, y, dirx, diry, cor=SETA, t=5.5):
        # triângulo com a ponta em (x, y), apontando na direção (dirx, diry)
        import math
        n = math.hypot(dirx, diry)
        ux, uy = dirx / n, diry / n
        px, py = -uy, ux
        bx, by = x - ux * t, y - uy * t
        pts = [(x, y), (bx + px * t * 0.6, by + py * t * 0.6), (bx - px * t * 0.6, by - py * t * 0.6)]
        self.el.append('<polygon points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) + f'" fill="{cor}"/>')

    def seta(self, x1, y1, x2, y2, cor=SETA):
        import math
        n = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / n, (y2 - y1) / n
        self.linha(x1, y1, x2 - ux * 4, y2 - uy * 4, cor)
        self.ponta(x2, y2, ux, uy, cor)

    def circulo(self, cx, cy, r, num, fill=TIT):
        self.el.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}"/>')
        self.texto(cx, cy + 3.1, str(num), 8.2, 700, "#FFFFFF", "middle")

    def salvar(self, nome, h):
        corpo = "\n".join(self.el)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{h:.0f}pt" '
               f'viewBox="0 0 {W} {h:.0f}">\n{corpo}\n</svg>\n')
        with open(os.path.join(AQUI, nome), "w", encoding="utf-8") as f:
            f.write(svg)
        print(nome, f"{W}x{h:.0f}")


def caixa_texto(s, x, y, w, titulo, corpo, pad=8, tam_t=8.8, tam_c=7.9, fill="#FFFFFF", stroke=AZUL_BORDA, centro=False, sw=1):
    """Desenha caixa com título e corpo; devolve a altura."""
    lt = quebrar(titulo, w - 2 * pad, tam_t, 600) if titulo else []
    lc = quebrar(corpo, w - 2 * pad, tam_c, 400) if corpo else []
    h = pad + len(lt) * tam_t * 1.28 + (3 if lt and lc else 0) + len(lc) * tam_c * 1.36 + pad - 2
    return lt, lc, h


def desenhar_caixa(s, x, y, w, h, lt, lc, pad=8, tam_t=8.8, tam_c=7.9, fill="#FFFFFF", stroke=AZUL_BORDA, centro=False, sw=1, cor_t=TIT):
    s.rect(x, y, w, h, fill, stroke, 8, sw)
    anchor = "middle" if centro else "start"
    tx = x + w / 2 if centro else x + pad
    yy = y + pad + tam_t * 0.82
    s.linhas(tx, yy, lt, tam_t, 600, cor_t, anchor, tam_t * 1.28)
    yy += len(lt) * tam_t * 1.28 + (3 if lt and lc else 0)
    if lc:
        s.linhas(tx, yy + (tam_c * 0.82 - tam_t * 0.82), lc, tam_c, 400, TXT, anchor, tam_c * 1.36)


# ---------------------------------------------------------------- trilha
def trilha():
    s = SVG()
    passos = [
        ("Conceito", "Elevação persistente; os números do Brasil", "cap. 01"),
        ("Como a pressão é feita", "Débito × resistência; sal, simpático, renina", "cap. 02"),
        ("Fatores de risco", "Remédios, sono, álcool; primária × secundária", "cap. 03"),
        ("Classificação e órgão-alvo", "Estágios de 2025; albuminúria", "cap. 04"),
        ("Consulta e medida", "Anamnese, exame físico, técnica certa", "cap. 05 e 06"),
        ("Causas secundárias", "Quando suspeitar; exames", "cap. 07"),
        ("O rim na hipertensão", "Nefroesclerose benigna e maligna", "cap. 08"),
        ("Tratamento sem remédio", "Para todos, desde o primeiro dia", "cap. 09"),
    ]
    gap = 16
    bw = (W - 3 * gap) / 4
    pad = 8
    # altura comum
    dados = []
    hmax = 0
    for t, c, cap in passos:
        lt = quebrar(t, bw - 2 * pad, 8.6, 600)
        lc = quebrar(c, bw - 2 * pad, 7.6, 400)
        h = 24 + len(lt) * 11 + 3 + len(lc) * 10.3 + 16
        hmax = max(hmax, h)
        dados.append((lt, lc, cap))
    y1, y2 = 4, 4 + hmax + 30
    for i, (lt, lc, cap) in enumerate(dados):
        lin, col = divmod(i, 4)
        x = col * (bw + gap)
        y = y1 if lin == 0 else y2
        s.rect(x, y, bw, hmax, "#FFFFFF", AZUL_BORDA, 9)
        s.circulo(x + pad + 8, y + pad + 8, 8, i + 1)
        s.texto(x + bw - pad, y + pad + 11, cap, 6.8, 500, CINZA, "end")
        yy = y + 24 + 8.6 * 0.85
        s.linhas(x + pad, yy + 4, lt, 8.6, 600, TIT, lh=11)
        yy += len(lt) * 11 + 3
        s.linhas(x + pad, yy + 4, lc, 7.6, 400, TXT, lh=10.3)
        if col < 3:
            s.seta(x + bw + 2, y + hmax / 2, x + bw + gap - 2, y + hmax / 2)
    # volta da linha 1 para a linha 2
    xa = 3 * (bw + gap) + bw / 2
    xb = bw / 2
    ym = y1 + hmax + 15
    s.caminho(f"M{xa:.1f},{y1 + hmax + 2:.1f} L{xa:.1f},{ym:.1f} L{xb:.1f},{ym:.1f} L{xb:.1f},{y2 - 6:.1f}")
    s.ponta(xb, y2 - 2, 0, 1)
    s.salvar("trilha.svg", y2 + hmax + 4)


# ---------------------------------------------------------------- fórmula
def formula():
    s = SVG()
    cx = W / 2
    # nível 1
    w1, h1 = 170, 30
    s.rect(cx - w1 / 2, 2, w1, h1, APOIO, AZUL, 9, 1.4)
    s.texto(cx, 21, "Pressão arterial", 10, 700, TIT, "middle")
    # nível 2
    y2 = 62
    w2, h2 = 176, 30
    xs2 = [W * 0.25, W * 0.75]
    nomes2 = ["Débito cardíaco", "Resistência vascular periférica"]
    for x, n in zip(xs2, nomes2):
        s.linha(cx, 2 + h1, cx, 46)
        s.linha(x, 46, x, y2)
    s.linha(xs2[0], 46, xs2[1], 46)
    for x, n in zip(xs2, nomes2):
        s.rect(x - w2 / 2, y2, w2, h2, "#FFFFFF", AZUL_BORDA, 9)
        s.texto(x, y2 + 19, n, 9, 600, TIT, "middle")
    s.texto(cx, y2 + 20, "×", 13, 600, AZUL, "middle")
    s.texto(cx + 4, 42, "é o produto de", 7, 500, CINZA, "start")
    # nível 3
    y3 = 132
    leaf_w = 104
    xs3 = [W * 0.125, W * 0.375, W * 0.625, W * 0.875]
    folhas = ["Volume sistólico", "Frequência cardíaca", "Sistema constritor", "Sistema hormonal"]
    for i, par in enumerate([(0, 1), (2, 3)]):
        xp = xs2[i]
        s.linha(xp, y2 + h2, xp, y3 - 16)
        s.linha(xs3[par[0]], y3 - 16, xs3[par[1]], y3 - 16)
        for j in par:
            s.linha(xs3[j], y3 - 16, xs3[j], y3)
    s.texto(xs2[1] + 4, y2 + h2 + 10, "tônus das arteríolas", 7, 500, CINZA, "start")
    s.texto(xs2[0] + 4, y2 + h2 + 10, "é o produto de", 7, 500, CINZA, "start")
    for x, n in zip(xs3, folhas):
        s.rect(x - leaf_w / 2, y3, leaf_w, 28, "#FFFFFF", AZUL_BORDA, 9)
        s.texto(x, y3 + 17.5, n, 8.4, 600, TIT, "middle")
    s.texto(xs2[0], y3 + 18, "×", 12, 600, AZUL, "middle")
    s.texto(xs2[1], y3 + 18, "+", 12, 600, AZUL, "middle")
    # nível 4: remédios
    y4 = y3 + 28 + 26
    rem = [("Diurético", "baixa o volume"), ("Betabloqueador", "baixa a frequência"),
           ("Vasodilatador", "relaxa a arteríola"), ("Inibidor da enzima conversora", "freia a angiotensina")]
    hmax = 0
    pre = []
    for t, c in rem:
        lt = quebrar(t, leaf_w - 12, 8.2, 600)
        lc = quebrar(c, leaf_w - 12, 7.4, 400)
        h = 8 + len(lt) * 10.5 + 2 + len(lc) * 9.6 + 6
        hmax = max(hmax, h)
        pre.append((lt, lc))
    for x, (lt, lc) in zip(xs3, pre):
        s.seta(x, y4 - 2, x, y3 + 28 + 3)
        s.rect(x - leaf_w / 2, y4, leaf_w, hmax, APOIO, AZUL_BORDA, 9, 1)
        yy = y4 + 8 + 7
        s.linhas(x, yy, lt, 8.2, 600, AZUL, "middle", 10.5)
        yy += len(lt) * 10.5 + 2
        s.linhas(x, yy, lc, 7.4, 400, TXT, "middle", 9.6)
    s.salvar("formula.svg", y4 + hmax + 3)


# ---------------------------------------------------------------- pistas
def pistas():
    s = SVG()
    linhas = [
        ("Hipertensão com potássio baixo no sangue (e alto na urina)", "Hiperaldosteronismo primário"),
        ("Crises de pressão alta com dor de cabeça, suor, palpitação, palidez e pelos arrepiados", "Feocromocitoma"),
        ("Início súbito antes dos 30 ou depois dos 55 anos, sopro no abdome, edema agudo de pulmão sem explicação", "Estenose da artéria renal"),
        ("Inchaço, anemia, cansaço, ureia e creatinina altas, exame de urina alterado", "Doença renal parenquimatosa"),
        ("Ronco, sono picado, sono não reparador e sonolência de dia", "Apneia do sono"),
        ("Pressão dos braços diferente da pressão das pernas", "Coarctação da aorta"),
        ("Rosto em lua cheia, giba, barriga grande e pernas finas", "Síndrome de Cushing"),
        ("Magreza, intolerância ao calor, taquicardia e agitação", "Hipertireoidismo"),
        ("Cansaço, ganho de peso, queda de cabelo, pressão diastólica alta", "Hipotireoidismo"),
    ]
    xl, wl = 0, 300
    xr, wr = 336, W - 336
    pad = 8
    y = 18
    s.texto(xl + 2, 9, "Pista na consulta ou no exame", 7.2, 600, CINZA)
    s.texto(xr + 2, 9, "Pense em", 7.2, 600, CINZA)
    for p, c in linhas:
        lp = quebrar(p, wl - 2 * pad, 8, 400)
        lc = quebrar(c, wr - 2 * pad, 8.4, 600)
        h = max(len(lp) * 10.6, len(lc) * 11) + 2 * pad - 2
        s.rect(xl, y, wl, h, "#FFFFFF", AZUL_BORDA, 8)
        s.linhas(xl + pad, y + pad + 6.6 + (h - 2 * pad + 2 - len(lp) * 10.6) / 2, lp, 8, 400, TXT, lh=10.6)
        s.rect(xr, y, wr, h, APOIO, AZUL_BORDA, 8)
        s.linhas(xr + pad, y + pad + 7 + (h - 2 * pad + 2 - len(lc) * 11) / 2, lc, 8.4, 600, TIT, lh=11)
        s.seta(xl + wl + 4, y + h / 2, xr - 3, y + h / 2)
        y += h + 6
    s.salvar("pistas.svg", y - 3)


# ---------------------------------------------------------------- nefroesclerose
def nefroesclerose():
    s = SVG()
    gap = 14
    bw = (W - 3 * gap) / 4
    pad = 7
    topo = [
        ("Pressão alta por anos", "a pressão dentro do glomérulo sobe"),
        ("Arteríolas aferentes esclerosadas", "arterioloesclerose: envelhecem antes da hora"),
        ("Luz estreita, isquemia", "do glomérulo e do túbulo-interstício"),
        ("Glomérulo se perde", "esclerose focal, depois segmentar, depois global"),
    ]
    dados, hmax = [], 0
    for t, c in topo:
        lt = quebrar(t, bw - 2 * pad, 8.4, 600)
        lc = quebrar(c, bw - 2 * pad, 7.5, 400)
        h = pad + len(lt) * 10.8 + 3 + len(lc) * 10 + pad
        hmax = max(hmax, h)
        dados.append((lt, lc))
    y1 = 2
    for i, (lt, lc) in enumerate(dados):
        x = i * (bw + gap)
        s.rect(x, y1, bw, hmax, "#FFFFFF", AZUL_BORDA, 9)
        yy = y1 + pad + 7.2
        s.linhas(x + pad, yy, lt, 8.4, 600, TIT, lh=10.8)
        yy += len(lt) * 10.8 + 3
        s.linhas(x + pad, yy, lc, 7.5, 400, TXT, lh=10)
        if i < 3:
            s.seta(x + bw + 2, y1 + hmax / 2, x + bw + gap - 2, y1 + hmax / 2)
    # ciclo embaixo
    y2 = y1 + hmax + 34
    apoio_x, apoio_w = 0, 330
    ciclo = [("Sobram menos néfrons", "de 1 milhão, vão sendo perdidos"),
             ("Os que sobram trabalham a mais", "para dar conta da filtração"),
             ("Adoecem pelo esforço", "e o ciclo recomeça")]
    cw = (apoio_w - 16 - 2 * 14) / 3
    dados2, h2 = [], 0
    for t, c in ciclo:
        lt = quebrar(t, cw - 2 * pad, 8.2, 600)
        lc = quebrar(c, cw - 2 * pad, 7.4, 400)
        h = pad + len(lt) * 10.6 + 3 + len(lc) * 9.8 + pad
        h2 = max(h2, h)
        dados2.append((lt, lc))
    alt_apoio = 18 + h2 + 30
    s.rect(apoio_x, y2, apoio_w, alt_apoio, APOIO, AZUL_BORDA, 10)
    s.texto(apoio_x + 8, y2 + 12, "O ciclo que perpetua a lesão renal", 7.4, 600, CINZA)
    yb = y2 + 18
    for i, (lt, lc) in enumerate(dados2):
        x = apoio_x + 8 + i * (cw + 14)
        s.rect(x, yb, cw, h2, "#FFFFFF", AZUL_BORDA, 9)
        yy = yb + pad + 7
        s.linhas(x + pad, yy, lt, 8.2, 600, TIT, lh=10.6)
        yy += len(lt) * 10.6 + 3
        s.linhas(x + pad, yy, lc, 7.4, 400, TXT, lh=9.8)
        if i < 2:
            s.seta(x + cw + 2, yb + h2 / 2, x + cw + 12, yb + h2 / 2)
    # volta do 3 para o 1
    x1c = apoio_x + 8 + cw / 2
    x3c = apoio_x + 8 + 2 * (cw + 14) + cw / 2
    yv = yb + h2 + 14
    s.caminho(f"M{x3c:.1f},{yb + h2 + 2:.1f} L{x3c:.1f},{yv:.1f} L{x1c:.1f},{yv:.1f} L{x1c:.1f},{yb + h2 + 6:.1f}")
    s.ponta(x1c, yb + h2 + 2, 0, -1)
    # ligação do "glomérulo se perde" ao ciclo
    xg = 3 * (bw + gap) + bw / 2
    s.caminho(f"M{xg:.1f},{y1 + hmax + 2:.1f} L{xg:.1f},{y1 + hmax + 16:.1f} L{x1c:.1f},{y1 + hmax + 16:.1f} L{x1c:.1f},{y2 - 4:.1f}")
    s.ponta(x1c, y2 - 1, 0, 1)
    # freio
    fx = apoio_w + 14
    fw = W - fx
    lt = quebrar("Controle ideal da pressão", fw - 16, 8.8, 700)
    lc = quebrar("Freia o ciclo: menos glomérulos destruídos ao longo dos anos. É o foco do tratamento.", fw - 16, 7.8, 400)
    fh = alt_apoio
    s.rect(fx, y2, fw, fh, "#FFFFFF", AZUL, 10, 1.6)
    bloco = len(lt) * 11.5 + 4 + len(lc) * 10.4
    yy = y2 + (fh - bloco) / 2 + 8.5
    s.linhas(fx + 8, yy, lt, 8.8, 700, AZUL, lh=11.5)
    yy += len(lt) * 11.5 + 4
    s.linhas(fx + 8, yy, lc, 7.8, 400, TXT, lh=10.4)
    s.seta(fx - 2, y2 + fh / 2, apoio_w + 3, y2 + fh / 2, AZUL)
    s.salvar("nefroesclerose.svg", y2 + alt_apoio + 2)


# ---------------------------------------------------------------- início do tratamento
def inicio():
    s = SVG()
    pad = 9
    # topo
    lt = quebrar("Todo hipertenso: mudança de estilo de vida", W - 40, 9.6, 700)
    lc = quebrar("É tratamento, faz parte do protocolo do Ministério da Saúde e cabe ao médico prescrever.", W - 40, 8, 400)
    h0 = pad + len(lt) * 12 + 3 + len(lc) * 10.8 + pad - 1
    s.rect(0, 2, W, h0, APOIO, AZUL, 10, 1.4)
    yy = 2 + pad + 8
    s.linhas(W / 2, yy, lt, 9.6, 700, TIT, "middle", 12)
    yy += len(lt) * 12 + 3
    s.linhas(W / 2, yy, lc, 8, 400, TXT, "middle", 10.8)
    gap = 26
    cw = (W - gap) / 2
    xs = [0, cw + gap]
    colunas = [
        [("Pré-hipertensão ou estágio 1", "120 a 159 por 80 a 99 mmHg"),
         ("Só a mudança de estilo de vida", "acompanhar por 3 meses"),
         ("Em 3 meses não melhorou?", "pressão ainda acima de 140 mmHg"),
         ("Começa o remédio", "sem tirar a mudança de estilo de vida")],
        [("Estágios 2 e 3", "160 por 100 mmHg ou mais; a conduta só sem remédio fica para a pré-hipertensão e o estágio 1"),
         ("Remédio junto com a mudança de estilo de vida", "as classes de remédio são o assunto do seminário")],
    ]
    y = 2 + h0 + 22
    bases = []
    medidas = []
    for col in colunas:
        caixas = []
        for t, c in col:
            l1 = quebrar(t, cw - 2 * pad, 8.6, 600)
            l2 = quebrar(c, cw - 2 * pad, 7.7, 400)
            h = pad + len(l1) * 11 + 2 + len(l2) * 10.2 + pad - 2
            caixas.append((l1, l2, h))
        medidas.append(caixas)
    # alturas: as duas colunas terminam na mesma base
    gv = 18
    tot = [sum(c[2] for c in caixas) + gv * (len(caixas) - 1) for caixas in medidas]
    alvo = max(tot)
    for xi, caixas, t in zip(xs, medidas, tot):
        extra_gap = (alvo - t) / (len(caixas) - 1) if len(caixas) > 1 else 0
        yy0 = y
        s.seta(xi + cw / 2, 2 + h0 + 2, xi + cw / 2, y - 2)
        for i, (l1, l2, h) in enumerate(caixas):
            final = i == len(caixas) - 1
            s.rect(xi, yy0, cw, h, "#FFFFFF", AZUL if final else AZUL_BORDA, 9, 1.4 if final else 1)
            ty = yy0 + pad + 7
            s.linhas(xi + pad, ty, l1, 8.6, 600, AZUL if final else TIT, lh=11)
            ty += len(l1) * 11 + 2
            s.linhas(xi + pad, ty, l2, 7.7, 400, TXT, lh=10.2)
            if not final:
                g = gv + extra_gap
                s.seta(xi + cw / 2, yy0 + h + 2, xi + cw / 2, yy0 + h + g - 2)
                yy0 += h + g
            else:
                yy0 += h
        bases.append(yy0)
    s.salvar("inicio.svg", max(bases) + 2)


if __name__ == "__main__":
    trilha()
    formula()
    pistas()
    nefroesclerose()
    inicio()
