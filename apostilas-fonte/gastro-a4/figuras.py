#!/usr/bin/env python3
"""Figuras da apostila gastro-a4 (Pâncreas, pancreatite aguda e crônica).

Rode na pasta de trabalho:  python3 figuras.py
Gera os SVGs (trilha, fisiopatologia, investigação da causa, linha do tempo da
crônica, diagnóstico da crônica) e recorta as imagens dos slides (slides.pdf,
via pdftoppm) com rótulos desenhados por nós.
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
        ("01", "Caso: icterícia obstrutiva"),
        ("02", "Anatomia e enzimas"),
        ("03", "Causas e mecanismo"),
        ("04", "Quadro e diagnóstico"),
        ("05", "Tomografia e gravidade"),
        ("06", "Tratamento e coleções"),
        ("07", "Quadro e diagnóstico"),
        ("08", "Causas e quatro casos"),
        ("09", "Tratamento"),
    ]
    x0, passo, yc = 27, 53, 40
    xs = [x0 + i * passo for i in range(len(nos))]
    c = []
    grupos = [(0, 0, "O caso"), (1, 1, "A base"), (2, 5, "Pancreatite aguda"), (6, 8, "Pancreatite crônica")]
    for a, b, nome in grupos:
        xa, xb = xs[a] - 22, xs[b] + 22
        c.append(caixa(xa, 1, xb - xa, 18, fill=APOIO, stroke=BORDA, r=6))
        c.append(texto((xa + xb) / 2, 13.2, nome, "s", 7.6, TIT, "middle"))
    c.append(f'<line x1="{xs[0]:.1f}" y1="{yc}" x2="{xs[-1]:.1f}" y2="{yc}" stroke="{SETA}" stroke-width="2"/>')
    for x, (n, rot) in zip(xs, nos):
        c.append(f'<circle cx="{x:.1f}" cy="{yc}" r="10.5" fill="#FFFFFF" stroke="{AZUL}" stroke-width="1.6"/>')
        c.append(texto(x, yc + 3.2, n, "s", 8, AZUL, "middle"))
        ls = quebra(rot, "m", 7.2, 49)
        c.append(bloco(x, yc + 22, ls, "m", 7.2, TXT, 9.2, "middle"))
    svg("trilha.svg", 74, "".join(c))


# ---------------------------------------------------------------- fisiopatologia
def fisiopatologia():
    col_w, gap = 229, 20
    xl, xr = 0, col_w + gap
    esq = [
        "As células acinares liberam as proteases desligadas (pró-enzimas). Amilase e lipase já saem ativas.",
        "No duodeno, a enteropeptidase do intestino transforma o tripsinogênio em tripsina.",
        "A tripsina liga as outras: pró-elastase em elastase, quimotripsinogênio em quimotripsina, pró-carboxipeptidase em carboxipeptidase.",
        "As proteínas da comida são digeridas dentro do intestino. O pâncreas fica protegido.",
    ]
    dir_ = [
        "Gatilho: cálculo no fim do colédoco, álcool, triglicerídeos ou cálcio altos, remédio, tumor.",
        "O tripsinogênio vira tripsina dentro das células do pâncreas, em quantidade que vence as defesas.",
        "A tripsina liga as outras enzimas em série: o pâncreas começa a digerir a si mesmo.",
        "Inflamação local. Se for intensa: resposta inflamatória sistêmica, pulmão inflamado, choque e insuficiência renal.",
    ]
    size, lh, pad = 8, 10.8, 7
    alt = []
    for a, b in zip(esq, dir_):
        la = quebra(a, "r", size, col_w - 2 * pad)
        lb = quebra(b, "r", size, col_w - 2 * pad)
        alt.append((la, lb, max(len(la), len(lb)) * lh + 2 * pad - 2))
    c = []
    y = 0
    for x, tit in ((xl, "Normal: as enzimas ligam no intestino"), (xr, "Pancreatite: as enzimas ligam no pâncreas")):
        c.append(caixa(x, y, col_w, 22, fill=APOIO, stroke=BORDA, r=6))
        c.append(texto(x + col_w / 2, y + 14.5, tit, "s", 8.2, TIT, "middle"))
    y = 22 + 14
    for i, (la, lb, h) in enumerate(alt):
        for x, ls in ((xl, la), (xr, lb)):
            forte = (i == len(alt) - 1 and x == xr)
            c.append(caixa(x, y, col_w, h, stroke=AZUL if forte else BORDA, sw=1.3 if forte else 1))
            c.append(bloco(x + pad, y + pad + 7.5, ls, "r", size, TXT, lh))
        if i < len(alt) - 1:
            for x in (xl, xr):
                c.append(seta_v(x + col_w / 2, y + h + 1, y + h + 13))
        y += h + 14
    svg("fisiopatologia.svg", y - 13, "".join(c))


# ---------------------------------------------------------------- investigação da causa
def investigacao():
    xl, wl = 0, 262
    xr, wr = 318, 160
    passos = [
        ("Ultrassom: tem pedra na vesícula?", "Pancreatite biliar"),
        ("História: álcool, remédios, trauma ou procedimento na via biliar (como a colangiopancreatografia na véspera)?", "A causa está na história"),
        ("Exames: triglicerídeos e cálcio estão altos?", "Hipertrigliceridemia ou hipercalcemia"),
        ("Nada disso e mais de 40 anos?", "Pensar em tumor obstruindo o ducto pancreático"),
    ]
    size, lh, pad = 8.2, 11, 8
    c = []
    y = 0
    for i, (q, r) in enumerate(passos):
        lq = quebra(q, "m", size, wl - 2 * pad)
        lr = quebra(r, "s", size, wr - 2 * pad)
        h = max(len(lq), len(lr)) * lh + 2 * pad - 1
        c.append(caixa(xl, y, wl, h))
        c.append(bloco(xl + pad, y + pad + 8, lq, "m", size, TXT, lh))
        c.append(caixa(xr, y, wr, h, fill=APOIO, stroke=AZUL, sw=1.2))
        c.append(bloco(xr + pad, y + h / 2 - (len(lr) - 1) * lh / 2 + 3, lr, "s", size, TIT, lh))
        c.append(seta_h(xl + wl + 2, xr - 2, y + h / 2))
        c.append(texto((xl + wl + xr) / 2, y + h / 2 - 5, "sim", "s", 7.4, AZUL, "middle"))
        if i < len(passos) - 1:
            c.append(seta_v(xl + 40, y + h + 1, y + h + 17))
            c.append(texto(xl + 48, y + h + 12, "não", "s", 7.4, CINZA))
        y += h + 18
    svg("investigacao.svg", y - 17, "".join(c))


# ---------------------------------------------------------------- linha do tempo da crônica
def linha_tempo():
    c = []
    y_eixo = 44
    x0, x1 = 6, 472
    c.append(f'<line x1="{x0}" y1="{y_eixo}" x2="{x1-6}" y2="{y_eixo}" stroke="{SETA}" stroke-width="2"/>')
    c.append(f'<polygon points="{x1-7},{y_eixo-4.5} {x1-7},{y_eixo+4.5} {x1},{y_eixo}" fill="{SETA}"/>')
    marcos = [(20, "Início: crises de dor", "start"), (300, "Cerca de 10 anos depois", "middle")]
    for x, rot, anc in marcos:
        c.append(f'<circle cx="{x}" cy="{y_eixo}" r="5" fill="#FFFFFF" stroke="{AZUL}" stroke-width="1.6"/>')
        c.append(texto(x - 6 if anc == "start" else x, y_eixo - 12, rot, "s", 8, TIT, anc))
    c.append(texto(x1, y_eixo + 15, "anos", "m", 7.4, CINZA, "end"))
    # faixas de fase
    fases = [
        (6, 270, "Fase de dor", "Crises de 1 a 7 dias, com intervalos sem dor. Álcool e comida gordurosa disparam a crise; o paciente passa a ter medo de comer."),
        (282, 190, "Fase de perda da função", "Esteatorreia e diabetes, quando já se perdeu mais de 90% do parênquima."),
    ]
    yb = 66
    hs = []
    for x, w, t, d in fases:
        ls = quebra(d, "r", 8, w - 16)
        hs.append(len(ls))
    h = max(hs) * 10.8 + 30
    for (x, w, t, d) in fases:
        ls = quebra(d, "r", 8, w - 16)
        c.append(caixa(x, yb, w, h))
        c.append(texto(x + 8, yb + 15, t, "s", 8.2, AZUL))
        c.append(bloco(x + 8, yb + 28, ls, "r", 8, TXT, 10.8))
    svg("linha-tempo.svg", yb + h + 1, "".join(c))


# ---------------------------------------------------------------- diagnóstico da crônica
def diagnostico_cronica():
    xl, wl = 0, 268
    xr, wr = 326, 152
    size, lh, pad = 8.2, 11, 8
    c = []
    topo = "Suspeita: dor típica, diarreia com gordura ou diabetes, crises repetidas de pancreatite aguda, história familiar ou alteração genética conhecida"
    lt = quebra(topo, "m", size, wl - 2 * pad)
    ht = len(lt) * lh + 2 * pad - 1
    c.append(caixa(xl, 0, wl, ht, fill=APOIO))
    c.append(bloco(xl + pad, pad + 8, lt, "m", size, TIT, lh))
    y = ht + 18
    c.append(seta_v(xl + wl / 2, ht + 1, y - 1))
    passos = [
        ("Tomografia (ou ressonância): primeira escolha", "inconclusiva"),
        ("Ecoendoscopia: vê alterações mais precoces", "não compatível"),
        ("Teste genético; se positivo, histologia do pâncreas", None),
    ]
    ys = []
    for i, (p, nao) in enumerate(passos):
        lp = quebra(p, "m", size, wl - 2 * pad)
        h = len(lp) * lh + 2 * pad - 1
        c.append(caixa(xl, y, wl, h))
        c.append(bloco(xl + pad, y + pad + 8, lp, "m", size, TXT, lh))
        ys.append((y, h))
        if nao:
            c.append(seta_v(xl + wl / 2, y + h + 1, y + h + 19))
            c.append(texto(xl + wl / 2 + 8, y + h + 13, nao, "s", 7.4, CINZA))
            y += h + 20
        else:
            y += h
    # caixa de resultado alta, à direita
    ytop, ybot = ys[0][0], ys[-1][0] + ys[-1][1]
    c.append(caixa(xr, ytop, wr, ybot - ytop, fill=APOIO, stroke=AZUL, sw=1.3))
    lr = quebra("Compatível com pancreatite crônica", "s", 9, wr - 20)
    c.append(bloco(xr + wr / 2, (ytop + ybot) / 2 - (len(lr) - 1) * 6 + 3, lr, "s", 9, TIT, 12, "middle"))
    for (yy, hh) in ys:
        c.append(seta_h(xl + wl + 2, xr - 2, yy + hh / 2))
        c.append(texto((xl + wl + xr) / 2, yy + hh / 2 - 5, "compatível", "s", 6.8, AZUL, "middle"))
    # saída final
    y += 18
    c.append(seta_v(xl + wl / 2, ybot + 1, y - 1))
    c.append(texto(xl + wl / 2 + 8, ybot + 12, "negativos", "s", 7.4, CINZA))
    lf = ["Pensar em outro diagnóstico"]
    c.append(caixa(xl, y, wl, 26, stroke=BORDA, dash="3 2"))
    c.append(bloco(xl + pad, y + 16.5, lf, "m", size, TXT, lh))
    svg("diagnostico-cronica.svg", y + 27, "".join(c))


# ---------------------------------------------------------------- hipóteses do caso
def hipoteses():
    cols = ["Sangue", "Endoscopia", "Ultrassom", "Ressonância"]
    # estados: s = segue, b = pouco provável, f = descartada, c = confirmada, "" = sem exame novo
    linhas = [
        ("Hepatite aguda", ["b", "b", "b", "b"]),
        ("Pancreatite aguda", ["b", "b", "b", "b"]),
        ("Câncer gástrico com metástase", ["s", "f", "", ""]),
        ("Câncer de papila", ["s", "f", "", ""]),
        ("Cirrose", ["s", "s", "f", ""]),
        ("Tumor alto (hilo, vesícula)", ["s", "s", "f", ""]),
        ("Pancreatite crônica", ["s", "s", "s", "f"]),
        ("Tumor periampular", ["s", "s", "s", "f"]),
        ("Coledocolitíase", ["s", "s", "s", "c"]),
        ("Dispepsia (refluxo, gastrite)", ["s", "c", "", ""]),
    ]
    xl, x0, cw, lh, top = 0, 170, 77, 14.5, 24
    c = []
    c.append(caixa(x0 - 4, 0, cw * 4 + 8, top + lh * len(linhas) + 4, fill=APOIO, stroke=BORDA, r=6))
    for j, nome in enumerate(cols):
        c.append(texto(x0 + cw * j + cw / 2, 15, nome, "s", 7.8, TIT, "middle"))
    for i, (h, est) in enumerate(linhas):
        y = top + lh * i + lh / 2
        if i:
            c.append(f'<line x1="{xl}" y1="{y - lh/2:.1f}" x2="{x0 + cw*4 + 4}" y2="{y - lh/2:.1f}" stroke="#E3E3E8" stroke-width="0.7"/>')
        c.append(texto(xl, y + 3, h, "m", 7.8, TXT))
        for j, e in enumerate(est):
            cx = x0 + cw * j + cw / 2
            if e == "s":
                c.append(f'<circle cx="{cx:.1f}" cy="{y:.1f}" r="3.6" fill="#A9C4EE"/>')
            elif e == "b":
                c.append(f'<circle cx="{cx:.1f}" cy="{y:.1f}" r="3.4" fill="#FFFFFF" stroke="#A9C4EE" stroke-width="1.3"/>')
            elif e == "f":
                c.append(f'<line x1="{cx-6:.1f}" y1="{y:.1f}" x2="{cx+6:.1f}" y2="{y:.1f}" stroke="#8E8E93" stroke-width="1.6"/>')
                c.append(texto(cx + 9, y + 2.6, "fora", "m", 6.6, "#8E8E93"))
            elif e == "c":
                c.append(f'<rect x="{cx-17:.1f}" y="{y-5.5:.1f}" width="34" height="11" rx="5.5" fill="{AZUL}"/>')
                c.append(texto(cx, y + 2.6, "confirma", "s", 6.4, "#FFFFFF", "middle"))
    yl = top + lh * len(linhas) + 18
    c.append(f'<circle cx="{x0+2}" cy="{yl-2.6}" r="3.6" fill="#A9C4EE"/>')
    c.append(texto(x0 + 10, yl, "segue na lista", "r", 7.2, CINZA))
    c.append(f'<circle cx="{x0+92}" cy="{yl-2.6}" r="3.4" fill="#FFFFFF" stroke="#A9C4EE" stroke-width="1.3"/>')
    c.append(texto(x0 + 100, yl, "pouco provável", "r", 7.2, CINZA))
    c.append(f'<line x1="{x0+180}" y1="{yl-2.6}" x2="{x0+192}" y2="{yl-2.6}" stroke="#8E8E93" stroke-width="1.6"/>')
    c.append(texto(x0 + 197, yl, "descartada", "r", 7.2, CINZA))
    c.append(texto(xl, yl, "Hipótese", "s", 7.2, TIT))
    svg("hipoteses.svg", yl + 4, "".join(c))


# ---------------------------------------------------------------- imagens dos slides
def pagina(n, dpi=200):
    tmp = tempfile.mkdtemp()
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-f", str(n), "-l", str(n),
                    os.path.join(AQUI, "slides.pdf"), os.path.join(tmp, "p")], check=True)
    arq = [a for a in os.listdir(tmp) if a.endswith(".png")][0]
    return Image.open(os.path.join(tmp, arq)).convert("RGB")


def recorta(im, caixa110):
    k = im.width / 1100.0
    x0, y0, x1, y1 = caixa110
    return im.crop((int(x0 * k), int(y0 * k), int(x1 * k), int(y1 * k)))


def rotulo(d, xy, txt, size=34, cor=(11, 91, 211), fundo=(255, 255, 255), pad=10, k="s"):
    f = font(k, size)
    x, y = xy
    w = f.getlength(txt)
    d.rounded_rectangle([x - pad, y - pad + 2, x + w + pad, y + size + pad - 2], radius=12, fill=fundo, outline=(195, 216, 248), width=3)
    d.text((x, y), txt, font=f, fill=cor)


def lado_a_lado(ims, altura, gap=24, faixa=0, fundo=(255, 255, 255)):
    rs = [im.resize((int(im.width * altura / im.height), altura), Image.LANCZOS) for im in ims]
    w = sum(r.width for r in rs) + gap * (len(rs) - 1)
    tela = Image.new("RGB", (w, altura + faixa), fundo)
    x = 0
    pos = []
    for r in rs:
        tela.paste(r, (x, 0))
        pos.append((x, r.width))
        x += r.width + gap
    return tela, pos


def imagens():
    # anatomia (slide 3): rótulos do slide + cabeça, corpo e cauda desenhados por nós
    im = recorta(pagina(3), (30, 45, 1100, 800))
    d = ImageDraw.Draw(im)
    k = im.width / 1070
    fundo = im.getpixel((int(20 * k), int(20 * k)))
    # os rótulos do slide são redesenhados maiores, para continuarem legíveis com a figura menor
    rotulos = [((130, 50, 330, 78), ["Ducto colédoco"]),
               ((652, 380, 920, 408), ["Incisura do pâncreas"]),
               ((590, 552, 856, 622), ["Ducto pancreático", "principal (de Wirsung)"]),
               ((136, 686, 432, 750), ["Ducto pancreático", "acessório (de Santorini)"])]
    fm = font("m", 50)
    for (x0, y0, x1, y1), linhas in rotulos:
        d.rectangle([int(x0 * k) - 6, int(y0 * k) - 6, int(x1 * k) + 6, int(y1 * k) + 6], fill=fundo)
        for i, t in enumerate(linhas):
            d.text((int(x0 * k), int(y0 * k) - 4 + i * 60), t, font=fm, fill=(31, 41, 51))
    rotulo(d, (int(270 * k), int(560 * k)), "Cabeça", 62)
    rotulo(d, (int(520 * k), int(150 * k)), "Corpo", 62)
    rotulo(d, (int(900 * k), int(250 * k)), "Cauda", 62)
    im.save(os.path.join(AQUI, "anatomia.jpg"), quality=88)

    # Cullen e Grey-Turner (slide 22)
    p = pagina(22)
    a = recorta(p, (30, 83, 525, 482))
    b = recorta(p, (543, 190, 1070, 665))
    tela, pos = lado_a_lado([a, b], 700, gap=26, faixa=90)
    d = ImageDraw.Draw(tela)
    f = font("s", 40)
    for (x, w), t in zip(pos, ["Cullen: em volta do umbigo", "Grey-Turner: nos flancos"]):
        d.text((x + w / 2 - f.getlength(t) / 2, 724), t, font=f, fill=(22, 49, 92))
    tela.save(os.path.join(AQUI, "cullen-grey-turner.jpg"), quality=86)

    # complicações locais (slides 30, 31, 32): os nomes ficam no "O que olhar", na mesma ordem
    ims = [recorta(pagina(30), (262, 140, 1030, 735)),
           recorta(pagina(31), (412, 160, 1056, 693)),
           recorta(pagina(32), (305, 134, 1045, 691))]
    tela, pos = lado_a_lado(ims, 640, gap=22, faixa=0)
    tela.save(os.path.join(AQUI, "complicacoes-locais.jpg"), quality=86)

    # pancreatite crônica: tomografia (slide 64) e colangiorressonância (slide 67)
    a = recorta(pagina(64), (55, 22, 1054, 803))
    ka = a.width / 999.0  # cobre a legenda em inglês da figura original
    ImageDraw.Draw(a).rectangle([int(680 * ka), int(684 * ka), a.width, a.height], fill=(0, 0, 0))
    b = recorta(pagina(67), (588, 308, 1090, 770))
    tela, pos = lado_a_lado([a, b], 700, gap=24, faixa=96)
    d = ImageDraw.Draw(tela)
    for (x, w), t in zip(pos, ["Tomografia", "Colangiorressonância"]):
        ff = font("s", 40)
        d.text((x + w / 2 - ff.getlength(t) / 2, 724), t, font=ff, fill=(22, 49, 92))
    tela.save(os.path.join(AQUI, "cronica-imagem.jpg"), quality=86)

    # ilhota de Langerhans entre os ácinos (detalhe do slide 4)
    ilhota = recorta(pagina(4), (490, 392, 1100, 732))
    ki = ilhota.width / 610.0  # apaga a pontinha do texto azul do slide que entra no recorte
    ImageDraw.Draw(ilhota).rectangle([0, int(225 * ki), int(20 * ki), int(280 * ki)], fill=(255, 255, 255))
    ilhota.save(os.path.join(AQUI, "ilhota.jpg"), quality=88)

    # posição genupeitoral (slide 19), sem a legenda do livro
    recorta(pagina(19), (375, 197, 1058, 563)).save(os.path.join(AQUI, "genupeitoral.jpg"), quality=86)


if __name__ == "__main__":
    trilha(); hipoteses(); fisiopatologia(); investigacao(); linha_tempo(); diagnostico_cronica(); imagens()
    print("figuras prontas")
