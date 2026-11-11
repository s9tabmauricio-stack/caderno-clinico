# Desenha as figuras da apostila nefro-a9 (Nefrologia, Aula 7.1).
# Uso: python3 figuras.py  (na pasta de trabalho; precisa da pasta fonts/ do preparar.sh)
from PIL import ImageFont
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
ARQ = {"r": "Inter-Regular.ttf", "m": "Inter-Medium.ttf", "s": "Inter-SemiBold.ttf", "b": "Inter-Bold.ttf"}
FAM = {"r": ('Inter', 400), "m": ('Inter Medium', 500), "s": ('Inter SemiBold', 600), "b": ('Inter', 700)}
_cache = {}

W = 478
AZUL_BORDA = "#C3D8F8"
APOIO = "#F5F8FF"
SETA = "#8AA9DF"
TEXTO = "#1F2933"
TITULO = "#16315C"
AZUL = "#0B5BD3"


def fonte(peso, tam):
    k = (peso, tam)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(os.path.join(AQUI, "fonts", ARQ[peso]), tam)
    return _cache[k]


def larg(txt, tam, peso="r"):
    return fonte(peso, tam).getlength(txt)


def quebra(txt, tam, maxw, peso="r"):
    # quebra em espaços; palavra com hífen pode quebrar depois do hífen
    pedacos = []
    for w in txt.split(" "):
        if larg(w, tam, peso) > maxw and "-" in w:
            a, b = w.split("-", 1)
            pedacos += [a + "-", "\x00" + b]
        else:
            pedacos.append(w)
    linhas, atual = [], ""
    for p in pedacos:
        cola = p.startswith("\x00")
        p = p.lstrip("\x00")
        teste = (atual + p) if cola else (atual + " " + p if atual else p)
        if larg(teste, tam, peso) <= maxw or not atual:
            atual = teste
        else:
            linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    return linhas


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def texto(x, y, linhas, tam, peso="r", cor=TEXTO, anc="start", lh=None):
    fam, wt = FAM[peso]
    lh = lh or tam * 1.32
    out = []
    for i, l in enumerate(linhas):
        out.append(f'<text x="{x:.1f}" y="{y + i * lh:.1f}" font-family="{fam}" font-weight="{wt}" '
                   f'font-size="{tam}" fill="{cor}" text-anchor="{anc}">{esc(l)}</text>')
    return "\n".join(out)


def caixa(x, y, w, h, fill="#FFFFFF", stroke=AZUL_BORDA, rx=8, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def seta_baixo(cx, y1, y2, cor=SETA):
    # haste + ponta, como polígono
    hw, ph, pw = 1.6, 6, 5.5
    return (f'<polygon points="{cx - hw:.1f},{y1:.1f} {cx + hw:.1f},{y1:.1f} {cx + hw:.1f},{y2 - ph:.1f} '
            f'{cx + pw:.1f},{y2 - ph:.1f} {cx:.1f},{y2:.1f} {cx - pw:.1f},{y2 - ph:.1f} {cx - hw:.1f},{y2 - ph:.1f}" fill="{cor}"/>')


def seta_esq(x1, x2, cy, cor=SETA):
    # de x1 (direita) para x2 (esquerda, ponta)
    hw, ph, pw = 1.4, 6, 5
    return (f'<polygon points="{x1:.1f},{cy - hw:.1f} {x2 + ph:.1f},{cy - hw:.1f} {x2 + ph:.1f},{cy - pw:.1f} '
            f'{x2:.1f},{cy:.1f} {x2 + ph:.1f},{cy + pw:.1f} {x2 + ph:.1f},{cy + hw:.1f} {x1:.1f},{cy + hw:.1f}" fill="{cor}"/>')


def seta_dir(x1, x2, cy, cor=SETA):
    hw, ph, pw = 1.6, 6, 5.5
    return (f'<polygon points="{x1:.1f},{cy - hw:.1f} {x2 - ph:.1f},{cy - hw:.1f} {x2 - ph:.1f},{cy - pw:.1f} '
            f'{x2:.1f},{cy:.1f} {x2 - ph:.1f},{cy + pw:.1f} {x2 - ph:.1f},{cy + hw:.1f} {x1:.1f},{cy + hw:.1f}" fill="{cor}"/>')


def salvar(nome, h, corpo):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h:.0f}" '
           f'viewBox="0 0 {W} {h:.0f}">\n{corpo}\n</svg>\n')
    with open(os.path.join(AQUI, nome), "w", encoding="utf-8") as f:
        f.write(svg)
    print(nome, W, "x", round(h))


# ---------------------------------------------------------------- trilha
def trilha():
    passos = ["Bom remédio e estratégia", "Diuréticos", "Simpático: central, beta e alfa",
              "Canais de cálcio", "Renina-angiotensina", "Vasodilatadores diretos", "Cinco casos clínicos"]
    n = len(passos)
    x0, x1 = 36, W - 36
    xs = [x0 + i * (x1 - x0) / (n - 1) for i in range(n)]
    cy, r = 18, 12
    out = [f'<rect x="{x0:.1f}" y="{cy - 1.5:.1f}" width="{x1 - x0:.1f}" height="3" fill="{AZUL_BORDA}"/>']
    tam = 8.2
    yl = cy + r + 12
    maxl = 0
    for i, (x, p) in enumerate(zip(xs, passos)):
        cor = AZUL if i == n - 1 else TITULO
        out.append(f'<circle cx="{x:.1f}" cy="{cy}" r="{r}" fill="{cor}"/>')
        out.append(texto(x, cy + 3.6, [str(i + 1)], 10, "s", "#FFFFFF", "middle"))
        ls = quebra(p, tam, 64, "s")
        maxl = max(maxl, len(ls))
        out.append(texto(x, yl, ls, tam, "s", TITULO, "middle", lh=10.4))
    yb = yl + (maxl - 1) * 10.4 + 10
    # faixas de apoio, todas na mesma base
    tb = 7.8
    grupos = [(xs[0] - 32, xs[0] + 32, "o ponto de partida"),
              (xs[1] - 30, xs[5] + 30, "as classes, uma a uma: como agem, o efeito colateral típico e o cuidado na prescrição"),
              (xs[6] - 32, xs[6] + 32, "o efeito denuncia a classe")]
    alts = []
    for a, b, t in grupos:
        alts.append(len(quebra(t, tb, b - a - 10)))
    hb = max(alts) * 10 + 10
    for (a, b, t) in grupos:
        ls = quebra(t, tb, b - a - 10)
        out.append(caixa(a, yb, b - a, hb, APOIO, AZUL_BORDA, 7))
        ytxt = yb + (hb - (len(ls) - 1) * 10) / 2 + 2.6
        out.append(texto((a + b) / 2, ytxt, ls, tb, "r", TEXTO, "middle", lh=10))
    salvar("trilha.svg", yb + hb + 2, "\n".join(out))


# ---------------------------------------------------------------- pirâmide
def piramide():
    out = []
    niveis = [
        (300, "Depois, se precisar, acrescentar", "espironolactona · betabloqueador · alfabloqueador (alfa-1)", False),
        (424, "Para começar",
         "tiazídico · inibidor da enzima de conversão · bloqueador dos canais de cálcio · betabloqueador", False),
        (W, "Mudança de estilo de vida", "a base: não se fala em hipertensão arterial sem ela", True),
    ]
    y = 1
    for w, tit, corpo, base in niveis:
        x = (W - w) / 2
        ls = quebra(corpo, 8.6, w - 30)
        h = 16 + 12 + len(ls) * 11.4 + 2
        if base:
            out.append(caixa(x + 0.5, y, w - 1, h, TITULO, TITULO, 9))
            out.append(texto(W / 2, y + 18, [tit], 10.5, "s", "#FFFFFF", "middle"))
            out.append(texto(W / 2, y + 31, ls, 8.6, "r", "#DCE7FA", "middle", lh=11.4))
        else:
            out.append(caixa(x, y, w, h, "#FFFFFF", AZUL_BORDA, 9))
            out.append(texto(W / 2, y + 17, [tit], 9.4, "s", TITULO, "middle"))
            out.append(texto(W / 2, y + 30, ls, 8.6, "r", TEXTO, "middle", lh=11.4))
        y += h + 6
    salvar("piramide.svg", y - 6 + 2, "\n".join(out))


# ---------------------------------------------------------------- túbulo
def nefron():
    gap = 18
    cw = (W - 2 * gap) / 3
    xs = [i * (cw + gap) for i in range(3)]
    cab = ["Glomérulo e túbulo proximal", "Alça de Henle (ramo espesso)", "Túbulo distal e ducto coletor"]
    colunas = [
        [("Manitol", "soro injetável; trauma de crânio (edema cerebral)", "w"),
         ("Acetazolamida", "inibe a anidrase carbônica; glaucoma", "w"),
         ("Glifozinas", "dapagliflozina, empagliflozina, canagliflozina", "w")],
        [("Diuréticos de alça", "furosemida, bumetanida, ácido etacrínico, piretanida", "w"),
         ("Os mais potentes e rápidos", "inativam o cotransportador de sódio, potássio e dois cloretos", "a"),
         ("Furosemida", "a que existe na Unidade Básica de Saúde", "w")],
        [("Espoliadores de potássio", "benzotiazídicos (hidroclorotiazida, da farmácia básica) e sulfamídicos (clortalidona, indapamida)", "w"),
         ("Poupadores de potássio", "espironolactona (a mais famosa), triantereno, amilorida", "w")],
    ]
    out = []
    hc = 34
    for i, x in enumerate(xs):
        ls = quebra(cab[i], 8.8, cw - 16, "s")
        out.append(caixa(x + 0.5, 1, cw - 1, hc, TITULO, TITULO, 8))
        ytxt = 1 + (hc - (len(ls) - 1) * 11) / 2 + 3
        out.append(texto(x + cw / 2, ytxt, ls, 8.8, "s", "#FFFFFF", "middle", lh=11))
        if i < 2:
            out.append(seta_dir(x + cw + 2, x + cw + gap - 2, 1 + hc / 2))
    # caixas das colunas
    y0 = 1 + hc + 12
    medidas = []
    for col in colunas:
        blocos = []
        for tit, corpo, tipo in col:
            lt = quebra(tit, 8.8, cw - 18, "s")
            lc = quebra(corpo, 8, cw - 18)
            h = 9 + len(lt) * 11 + len(lc) * 10.4 + 7
            blocos.append((lt, lc, h, tipo))
        medidas.append(blocos)
    alturas = [sum(b[2] for b in bl) + 7 * (len(bl) - 1) for bl in medidas]
    hmax = max(alturas)
    for i, bl in enumerate(medidas):
        x = xs[i]
        y = y0
        extra = hmax - alturas[i]
        for j, (lt, lc, h, tipo) in enumerate(bl):
            if j == len(bl) - 1:
                h += extra  # última caixa de cada coluna termina na mesma base
            fill = APOIO if tipo == "a" else "#FFFFFF"
            out.append(caixa(x + 0.5, y, cw - 1, h, fill, AZUL_BORDA, 8))
            out.append(texto(x + 9, y + 15, lt, 8.8, "s", TITULO, lh=11))
            out.append(texto(x + 9, y + 15 + len(lt) * 11 + 0.5, lc, 8, "r", TEXTO, lh=10.4))
            y += h + 7
        # seta da coluna de cabeçalho para as caixas
        out.append(seta_baixo(x + cw / 2, 1 + hc + 1, y0 - 1))
    salvar("nefron.svg", y0 + hmax + 2, "\n".join(out))


# ---------------------------------------------------------------- renina-angiotensina
def raa():
    lw = 196           # coluna da cascata
    rx0 = 236          # coluna dos bloqueios
    rw = W - rx0
    cascata = ["Renina", "Angiotensina I", "Angiotensina II",
               "Receptor da angiotensina II nas células do vaso",
               "Vaso contrai; aldosterona segura sódio e água e elimina potássio"]
    rotulos_seta = [None, "enzima de conversão (uma cininase)", None, None]
    notas = {  # índice: (alvo, título, texto) ; alvo "b" = caixa, "s" = seta abaixo da caixa
        0: ("b", "Alisquireno", "inibe a renina direto: forma menos angiotensina"),
        1: ("s", "Inibidor da enzima de conversão",
            "bloqueia a passagem de I para II; as cininas (bradicinina) se acumulam: tosse seca e, no pior caso, angioedema"),
        3: ("b", "Bloqueador do receptor",
            "a angiotensina II se forma, mas não age no vaso; não acumula cinina: sem tosse"),
        4: ("b", "Nos dois bloqueios",
            "a pressão cai e a aldosterona fica inibida: o potássio sobe (hiperpotassemia)"),
    }
    out = []
    y = 1
    pos = []
    gap_seta = 26
    for i, c in enumerate(cascata):
        ls = quebra(c, 8.8, lw - 20, "s" if i < 4 else "m")
        h = 12 + len(ls) * 11.2 + 4
        pos.append((y, h))
        y += h + (gap_seta if i < len(cascata) - 1 else 0)
    # notas podem ser mais altas que o espaço: calcular altura de cada nota
    out_notas = []
    for i, (yb, hb) in enumerate(pos):
        if i not in notas:
            continue
        alvo, tit, corpo = notas[i]
        lt = quebra(tit, 8.8, rw - 18, "s")
        lc = quebra(corpo, 8, rw - 18)
        hn = 9 + len(lt) * 11 + len(lc) * 10.4 + 6
        if alvo == "b":
            cy = yb + hb / 2
        else:
            cy = yb + hb + gap_seta / 2
        out_notas.append((i, cy, hn, lt, lc, alvo))
    # ajusta para não sobrepor
    ajust = []
    ultimo = -99
    for i, cy, hn, lt, lc, alvo in out_notas:
        top = max(cy - hn / 2, ultimo + 6, 1)
        ajust.append((i, cy, top, hn, lt, lc, alvo))
        ultimo = top + hn
    for i, (yb, hb) in enumerate(pos):
        ls = quebra(cascata[i], 8.8, lw - 20, "s" if i < 4 else "m")
        fill = "#FFFFFF" if i < 4 else APOIO
        out.append(caixa(0.5, yb, lw, hb, fill, AZUL_BORDA, 8))
        out.append(texto(lw / 2, yb + 15.5, ls, 8.8, "s" if i < 4 else "m", TITULO if i < 4 else TEXTO, "middle", lh=11.2))
        if i < len(pos) - 1:
            out.append(seta_baixo(30 if rotulos_seta[i] else lw / 2, yb + hb + 2, yb + hb + gap_seta - 2))
            if rotulos_seta[i]:
                lr = quebra(rotulos_seta[i], 7.8, lw - 50, "m")
                y1 = yb + hb + gap_seta / 2 - (len(lr) - 1) * 9.4 / 2 + 2.8
                out.append(texto(44, y1, lr, 7.8, "m", TITULO, lh=9.4))
    for i, cy, top, hn, lt, lc, alvo in ajust:
        out.append(caixa(rx0, top, rw - 0.5, hn, "#FFFFFF", AZUL_BORDA, 8))
        out.append(f'<rect x="{rx0:.1f}" y="{top + 6:.1f}" width="3" height="{hn - 12:.1f}" rx="1.5" fill="{TITULO}"/>')
        out.append(texto(rx0 + 11, top + 15, lt, 8.8, "s", TITULO, lh=11))
        out.append(texto(rx0 + 11, top + 15 + len(lt) * 11 + 0.5, lc, 8, "r", TEXTO, lh=10.4))
        ly = min(max(cy, top + 10), top + hn - 10)
        alvo_x = lw + 2
        out.append(seta_esq(rx0 - 2, alvo_x, ly))
    h = max(pos[-1][0] + pos[-1][1], ajust[-1][2] + ajust[-1][3]) + 2
    salvar("raa.svg", h, "\n".join(out))


# ---------------------------------------------------------------- canais de cálcio
def bcc():
    out = []
    y = 1
    for t in ["Bloqueia a entrada de cálcio nas células musculares lisas dos vasos",
              "O vaso não contrai e fica dilatado: vasodilatação"]:
        out.append(caixa(0.5, y, W - 1, 26, "#FFFFFF", AZUL_BORDA, 8))
        out.append(texto(W / 2, y + 16.5, [t], 9, "s", TITULO, "middle"))
        y += 26
        out.append(seta_baixo(W / 2, y + 2, y + 16))
        y += 18
    # ramo em três
    gap = 12
    cw = (W - 2 * gap) / 3
    fins = [("A resistência vascular periférica cai", "a pressão baixa"),
            ("O retorno venoso diminui", "edema bimaleolar, em volta dos tornozelos"),
            ("O rosto também dilata", "rubor facial: duas manchinhas vermelhas")]
    # barra que distribui
    xs = [i * (cw + gap) for i in range(3)]
    out[-1] = seta_baixo(W / 2, y - 16, y - 8)
    out.append(f'<rect x="{xs[0] + cw / 2 - 1.6:.1f}" y="{y - 9.6:.1f}" width="{xs[2] - xs[0] + 3.2:.1f}" height="3.2" fill="{SETA}"/>')
    for x in xs:
        out.append(seta_baixo(x + cw / 2, y - 8, y + 2))
    y += 3
    hs = []
    for t, c in fins:
        lt = quebra(t, 8.8, cw - 18, "s")
        lc = quebra(c, 8, cw - 18)
        hs.append((lt, lc, 10 + len(lt) * 11 + len(lc) * 10.4 + 6))
    h = max(x[2] for x in hs)
    for x, (lt, lc, _) in zip(xs, hs):
        out.append(caixa(x + 0.5, y, cw - 1, h, APOIO, AZUL_BORDA, 8))
        out.append(texto(x + 9, y + 15, lt, 8.8, "s", TITULO, lh=11))
        out.append(texto(x + 9, y + 15 + len(lt) * 11 + 0.5, lc, 8, "r", TEXTO, lh=10.4))
    salvar("bcc.svg", y + h + 2, "\n".join(out))


# ---------------------------------------------------------------- caso 4
def caso4():
    out = []
    gap = 14
    cw = (W - gap) / 2
    def bloco(x, y, w, tit, corpo, fill="#FFFFFF", escuro=False, centro=False):
        lt = quebra(tit, 8.8, w - 20, "s")
        lc = quebra(corpo, 8, w - 20) if corpo else []
        h = 10 + len(lt) * 11 + len(lc) * 10.4 + 6
        return (lt, lc, h)
    def desenha(x, y, w, h, lt, lc, fill="#FFFFFF", escuro=False):
        out.append(caixa(x + 0.5, y, w - 1, h, TITULO if escuro else fill, TITULO if escuro else AZUL_BORDA, 8))
        ct = "#FFFFFF" if escuro else TITULO
        cc = "#DCE7FA" if escuro else TEXTO
        out.append(texto(x + w / 2, y + 15, lt, 8.8, "s", ct, "middle", lh=11))
        out.append(texto(x + w / 2, y + 15 + len(lt) * 11 + 0.5, lc, 8, "r", cc, "middle", lh=10.4))
    y = 1
    # linha A
    a1 = bloco(0, y, cw, "Remédio de casa", "enalapril, inibidor da enzima de conversão, há 10 anos")
    a2 = bloco(0, y, cw, "Remédio novo", "losartana, bloqueador do receptor, prescrita sem saber do outro")
    h = max(a1[2], a2[2])
    desenha(0, y, cw, h, a1[0], a1[1]); desenha(cw + gap, y, cw, h, a2[0], a2[1])
    y += h
    # convergir
    out.append(seta_baixo(cw / 2, y + 2, y + 10, SETA)[:-0] if False else "")
    for cx in (cw / 2, cw + gap + cw / 2):
        out.append(f'<rect x="{cx - 1.6:.1f}" y="{y + 2:.1f}" width="3.2" height="8" fill="{SETA}"/>')
    out.append(f'<rect x="{cw / 2 - 1.6:.1f}" y="{y + 8.4:.1f}" width="{cw + gap + 3.2:.1f}" height="3.2" fill="{SETA}"/>')
    out.append(seta_baixo(W / 2, y + 10, y + 20))
    y += 20
    b = bloco(0, y, W, "Os dois juntos: duplo bloqueio", "um dia um, um dia outro ou, muito provavelmente, os dois ao mesmo tempo")
    desenha(0, y, W, b[2], b[0], b[1], APOIO)
    y += b[2]
    # dividir
    out.append(f'<rect x="{W / 2 - 1.6:.1f}" y="{y + 2:.1f}" width="3.2" height="7" fill="{SETA}"/>')
    out.append(f'<rect x="{cw / 2 - 1.6:.1f}" y="{y + 7.6:.1f}" width="{cw + gap + 3.2:.1f}" height="3.2" fill="{SETA}"/>')
    for cx in (cw / 2, cw + gap + cw / 2):
        out.append(seta_baixo(cx, y + 9, y + 20))
    y += 20
    c1 = bloco(0, y, cw, "A pressão cai", "dois hipotensores somados")
    c2 = bloco(0, y, cw, "O potássio sobe", "a aldosterona fica inibida pelos dois: hiperpotassemia")
    h = max(c1[2], c2[2])
    desenha(0, y, cw, h, c1[0], c1[1]); desenha(cw + gap, y, cw, h, c2[0], c2[1])
    y += h
    for cx in (cw / 2, cw + gap + cw / 2):
        out.append(f'<rect x="{cx - 1.6:.1f}" y="{y + 2:.1f}" width="3.2" height="8" fill="{SETA}"/>')
    out.append(f'<rect x="{cw / 2 - 1.6:.1f}" y="{y + 8.4:.1f}" width="{cw + gap + 3.2:.1f}" height="3.2" fill="{SETA}"/>')
    out.append(seta_baixo(W / 2, y + 10, y + 20))
    y += 20
    d = bloco(0, y, W, "Fraqueza, mal-estar e cãibras; exames muito alterados",
              "ambulância de urgência, terapia intensiva e remédio para baixar o potássio")
    desenha(0, y, W, d[2], d[0], d[1], escuro=True)
    y += d[2]
    salvar("caso4.svg", y + 2, "\n".join(x for x in out if x))


if __name__ == "__main__":
    trilha()
    piramide()
    nefron()
    raa()
    bcc()
    caso4()
