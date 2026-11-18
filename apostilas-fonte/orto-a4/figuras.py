"""Figuras da apostila orto-a4 (trilha, pelve, colo do fêmur). Rodar na pasta da aula: python3 figuras.py"""
from pathlib import Path
from PIL import ImageFont

AQUI = Path(__file__).resolve().parent
FONTES = {"r": "Inter-Regular.ttf", "m": "Inter-Medium.ttf", "s": "Inter-SemiBold.ttf", "b": "Inter-Bold.ttf"}
PESO = {"r": 400, "m": 500, "s": 600, "b": 700}
_cache = {}

AZUL = "#0B5BD3"; MARINHO = "#16315C"; TXT = "#1F2933"; CINZA = "#6C6C70"
BORDA = "#C3D8F8"; APOIO = "#F5F8FF"; SETA = "#8AA9DF"; CLARO = "#E8F0FE"
W = 478


def fonte(p, t):
    k = (p, t)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(str(AQUI / "fonts" / FONTES[p]), t)
    return _cache[k]


def larg(txt, p, t):
    return fonte(p, t).getlength(txt)


def quebra(txt, p, t, maxw):
    linhas, atual = [], ""
    for pal in txt.split():
        teste = (atual + " " + pal).strip()
        if larg(teste, p, t) <= maxw or not atual:
            atual = teste
        else:
            linhas.append(atual)
            atual = pal
    if atual:
        linhas.append(atual)
    return linhas


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def texto(x, y, s, p="r", t=8, cor=TXT, anc="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter" font-weight="{PESO[p]}" '
            f'font-size="{t}" fill="{cor}" text-anchor="{anc}">{esc(s)}</text>')


def caixa(x, y, w, h, fill="#FFFFFF", stroke=BORDA, sw=1, r=7, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def seta_baixo(x, y1, y2, cor=SETA):
    return (f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{y2 - 5:.1f}" stroke="{cor}" stroke-width="1.6"/>'
            f'<polygon points="{x - 4:.1f},{y2 - 6:.1f} {x + 4:.1f},{y2 - 6:.1f} {x:.1f},{y2:.1f}" fill="{cor}"/>')


def bloco(x, y, w, titulo, sub=None, pt=8.6, ps=7.7, pad=7, cor_t=MARINHO, cor_s=TXT, centro=False):
    """Devolve (elementos de texto, altura) de um título + subtítulo quebrados na largura w."""
    out, yy = [], y + pad + pt * 0.95
    lt = quebra(titulo, "s", pt, w - 2 * pad)
    ax = x + w / 2 if centro else x + pad
    anc = "middle" if centro else "start"
    for l in lt:
        out.append(texto(ax, yy, l, "s", pt, cor_t, anc))
        yy += pt * 1.3
    if sub:
        yy += 1
        for l in quebra(sub, "r", ps, w - 2 * pad):
            out.append(texto(ax, yy, l, "r", ps, cor_s, anc))
            yy += ps * 1.38
    h = yy - y - pt * 0.95 + pad - (ps * 0.4 if sub else pt * 0.35) + 2
    return out, h


def svg(nome, h, corpo):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{h:.0f}pt" '
         f'viewBox="0 0 {W} {h:.0f}">' + "".join(corpo) + "</svg>")
    (AQUI / nome).write_text(s, encoding="utf-8")
    print(nome, f"{W} x {h:.0f}")


# ---------------------------------------------------------------- trilha
def trilha():
    etapas = [
        ("Método", "Dado-chave, cortar absurdas, cuidar do paciente."),
        ("Ferida e fratura exposta", "Imobilizar com curativo; tétano; lidocaína."),
        ("Pelve e choque", "Livro aberto e hipotensão: estabilizar a pelve."),
        ("Síndrome compartimental", "Dor desproporcional e ao esticar os dedos."),
        ("Fêmur da criança", "Aos 3 anos, gesso da pelve ao pé: 6 a 8 semanas."),
        ("Fêmur do idoso", "Perna curta e rodada para fora; operar sempre."),
        ("Osteoporose", "Bisfosfonato e, acima de tudo, estilo de vida."),
        ("Unidade Básica de Saúde", "Lombalgia sem imagem; canabidiol: informar."),
    ]
    gap = 18
    wc = (W - gap) / 2
    xt_rel, r = 25, 8.5
    wt = wc - xt_rel - 4
    # altura de cada linha (igual nas duas colunas)
    linhas = []
    for i in range(4):
        hs = []
        for col in (0, 1):
            t, s = etapas[col * 4 + i]
            hs.append(13 + len(quebra(s, "r", 7.8, wt)) * 10.2 + 5)
        linhas.append(max(hs))
    corpo, ys, y = [], [], 2
    for h in linhas:
        ys.append(y)
        y += h
    H = y
    for col in (0, 1):
        x0 = col * (wc + gap)
        cx = x0 + r + 1
        corpo.append(f'<line x1="{cx:.1f}" y1="{ys[0] + 11:.1f}" x2="{cx:.1f}" y2="{ys[-1] + 11:.1f}" stroke="{BORDA}" stroke-width="3"/>')
        for i in range(4):
            n = col * 4 + i + 1
            t, s = etapas[n - 1]
            yy = ys[i]
            corpo.append(f'<circle cx="{cx:.1f}" cy="{yy + 11:.1f}" r="{r}" fill="{MARINHO if n == 1 else AZUL}"/>')
            corpo.append(texto(cx, yy + 14, str(n), "s", 8.4, "#FFFFFF", "middle"))
            corpo.append(texto(x0 + xt_rel, yy + 13.5, t, "s", 9, MARINHO))
            for k, l in enumerate(quebra(s, "r", 7.8, wt)):
                corpo.append(texto(x0 + xt_rel, yy + 13.5 + 11.5 + k * 10.2, l, "r", 7.8, TXT))
    svg("trilha.svg", H, corpo)


# ---------------------------------------------------------------- pelve
def pelve():
    wm, xr, wr = 300, 314, W - 314
    corpo = []
    passos = [
        ("Atropelamento aos 22 anos: trauma de alta energia",
         "Bacia instável, hematoma no escroto, pressão 80 por 60, pulso 120.", "n"),
        ("Ultrassom FAST: sem líquido livre no abdome", "O sangue não está dentro da barriga.", "n"),
        ("Radiografia: sínfise aberta, pelve em livro aberto", "Cinta pélvica aplicada: fecha o anel.", "n"),
        ("Estabilização cirúrgica da pelve", "Fixador externo: rápido, com sedação leve ou anestesia local; o plexo venoso para de sangrar. Se nada der certo, depois: angiografia com embolização.", "ok"),
    ]
    y, pos = 16, []
    corpo.append(texto(0, 9, "O CAMINHO DO CASO", "s", 7.2, CINZA))
    corpo.append(texto(xr, 9, "FORA DE HORA", "s", 7.2, CINZA))
    for i, (t, s, tipo) in enumerate(passos):
        els, h = bloco(0, y, wm, t, s, pt=8.7 if tipo == "ok" else 8.3, ps=7.6, pad=7)
        if tipo == "ok":
            corpo.append(caixa(0, y, wm, h, fill=CLARO, stroke=AZUL, sw=1.6, r=8))
        else:
            corpo.append(caixa(0, y, wm, h))
        corpo += els
        pos.append((y, h))
        y += h
        if i < len(passos) - 1:
            gap = 21 if i == 2 or i == 3 else 14
            corpo.append(seta_baixo(wm / 2, y + 1, y + gap - 1))
            if i == 2:
                corpo.append(texto(wm / 2 + 8, y + 13.5, "continua hipotenso", "m", 7.6, AZUL))
            y += gap
    H = y + 2
    fora = [
        (1, "Laparotomia exploradora", "O FAST já afastou sangue na barriga; e é campo da cirurgia geral."),
        (2, "Tomografia de abdome e pelve", "Demora, e o paciente está instável."),
        (3, "Angiografia agora", "Demora e exige hospital terciário: fica para depois."),
    ]
    for idx, t, s in fora:
        y0, h0 = pos[idx]
        els, h = bloco(xr, 0, wr, t, s, pt=8.2, ps=7.5, pad=7, cor_t=CINZA, cor_s=CINZA)
        yy = y0 + (h0 - h) / 2
        els, h = bloco(xr, yy, wr, t, s, pt=8.2, ps=7.5, pad=7, cor_t=CINZA, cor_s=CINZA)
        corpo.append(caixa(xr, yy, wr, h, fill="#FFFFFF", stroke="#B9C3D3", dash="3 2.5"))
        corpo += els
        corpo.append(f'<line x1="{wm + 2}" y1="{y0 + h0 / 2:.1f}" x2="{xr - 2}" y2="{y0 + h0 / 2:.1f}" stroke="#B9C3D3" stroke-width="1" stroke-dasharray="2 2"/>')
    svg("pelve.svg", H, corpo)


# ---------------------------------------------------------------- colo do fêmur
def colo():
    corpo = []
    els, h = bloco(0, 0, W, "Fratura do colo do fêmur no idoso: operar sempre",
                   "Sem cirurgia, o idoso fica na cama, complica e a mortalidade chega a 50% no primeiro ano.",
                   pt=9.2, ps=7.9, pad=8, centro=True)
    corpo.append(caixa(0, 0, W, h, fill=APOIO, stroke=BORDA, r=8))
    corpo += els
    y = h
    corpo.append(seta_baixo(W / 2, y + 1, y + 15))
    y += 16
    corpo.append(texto(W / 2, y + 10, "O que decide: idade biológica e demanda funcional", "s", 8.4, AZUL, "middle"))
    y += 16
    gap = 10
    wc = (W - 2 * gap) / 3
    cols = [
        ("Ativo, lúcido e independente", "Idoso pela idade, jovem pela biologia.",
         "Artroplastia total do quadril", "Troca a cabeça do fêmur e o acetábulo. Funciona melhor a longo prazo."),
        ("Frágil, baixa demanda", "Anda pouco, só dentro de casa; sequela grave de acidente vascular cerebral ou demência.",
         "Hemiartroplastia", "Troca só a cabeça do fêmur. Mais rápida, sangra menos."),
        ("Menos de 60 anos ou fratura sem desvio", "Também o idoso de 60 a 65 anos muito hígido com fratura não desviada.",
         "Parafusos canulados", "Fixação. No idoso com desvio: risco de necrose da cabeça e de nova cirurgia."),
    ]
    # alturas iguais por linha
    h1 = max(bloco(0, 0, wc, a, b, pt=8.4, ps=7.6)[1] for a, b, _, _ in cols)
    h2 = max(bloco(0, 0, wc, c, d, pt=8.8, ps=7.6)[1] for _, _, c, d in cols)
    for i, (a, b, c, d) in enumerate(cols):
        x = i * (wc + gap)
        corpo.append(seta_baixo(x + wc / 2, y - 2, y + 10))
        y1 = y + 11
        corpo.append(caixa(x, y1, wc, h1))
        corpo += bloco(x, y1, wc, a, b, pt=8.4, ps=7.6)[0]
        corpo.append(seta_baixo(x + wc / 2, y1 + h1 + 1, y1 + h1 + 15))
        y2 = y1 + h1 + 16
        corpo.append(caixa(x, y2, wc, h2, fill=CLARO, stroke=AZUL, sw=1.4, r=8))
        corpo += bloco(x, y2, wc, c, d, pt=8.8, ps=7.6)[0]
    y = y + 11 + h1 + 16 + h2 + 12
    els, h = bloco(0, y, W, "Cortadas de cara: tração cutânea e gesso pelvipodálico",
                   "São tratamentos conservadores (o gesso é da criança).", pt=8.2, ps=7.5, pad=7,
                   cor_t=CINZA, cor_s=CINZA, centro=True)
    corpo.append(caixa(0, y, W, h, stroke="#B9C3D3", dash="3 2.5"))
    corpo += els
    svg("colo.svg", y + h + 1, corpo)


if __name__ == "__main__":
    trilha()
    pelve()
    colo()
