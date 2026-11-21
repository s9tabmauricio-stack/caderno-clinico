#!/usr/bin/env python3
"""Desenha as figuras SVG da apostila angio-a7 (trilha, planos, tratamento).

Rodar na pasta de trabalho: python3 figuras.py
Mede o texto com a fonte Inter da pasta fonts/ (copiada pelo preparar.sh).
"""
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import ImageFont

AQUI = Path(__file__).resolve().parent
FONTES = {
    400: AQUI / "fonts" / "Inter-Regular.ttf",
    500: AQUI / "fonts" / "Inter-Medium.ttf",
    600: AQUI / "fonts" / "Inter-SemiBold.ttf",
    700: AQUI / "fonts" / "Inter-Bold.ttf",
}
_cache = {}

W = 478
BORDA = "#C3D8F8"
APOIO = "#F5F8FF"
CLARO = "#E8F0FE"
SETA = "#8AA9DF"
TXT = "#1F2933"
TIT = "#16315C"
AZUL = "#0B5BD3"
CINZA = "#6C6C70"


def fonte(peso, tam):
    chave = (peso, tam)
    if chave not in _cache:
        _cache[chave] = ImageFont.truetype(str(FONTES[peso]), tam * 10)
    return _cache[chave]


def largura(txt, peso, tam):
    return fonte(peso, tam).getlength(txt) / 10


def quebrar(txt, peso, tam, maxw):
    linhas, atual = [], ""
    for p in txt.split():
        teste = (atual + " " + p).strip()
        if largura(teste, peso, tam) <= maxw:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    return linhas


def texto(x, y, txt, peso=400, tam=8, cor=TXT, anchor="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter" font-weight="{peso}" '
            f'font-size="{tam}" fill="{cor}" text-anchor="{anchor}">{escape(txt)}</text>')


def caixa(x, y, w, h, fill="#FFFFFF", stroke=BORDA, r=7, dash=False):
    d = ' stroke-dasharray="3 2"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1"{d}/>')


def ponta(x, y, direcao="baixo", t=4.5):
    """Ponta de seta como polígono (sem marker). (x, y) = bico."""
    if direcao == "baixo":
        pts = [(x - t, y - t * 1.3), (x + t, y - t * 1.3), (x, y)]
    elif direcao == "direita":
        pts = [(x - t * 1.3, y - t), (x - t * 1.3, y + t), (x, y)]
    else:
        raise ValueError(direcao)
    s = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    return f'<polygon points="{s}" fill="{SETA}"/>'


def linha(pts, cor=SETA, w=1.4):
    s = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    return f'<polyline points="{s}" fill="none" stroke="{cor}" stroke-width="{w}"/>'


def salvar(nome, h, partes):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h:.0f}" '
           f'viewBox="0 0 {W} {h:.0f}">' + "".join(partes) + "</svg>")
    (AQUI / nome).write_text(svg, encoding="utf-8")


def selo(cx, cy, n, r=7.5):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{TIT}"/>'
            + texto(cx, cy + 2.9, str(n), 600, 8, "#FFFFFF", "middle"))


# ---------------------------------------------------------------- trilha
def trilha():
    etapas = [
        ("Os casos", "Infecção de pele que mutilou e matou gente saudável"),
        ("Os três nomes", "Linfangite, erisipela e celulite; 90% nas pernas"),
        ("O germe", "Na erisipela clássica, o estreptococo do grupo A"),
        ("A cilada", "Febre sem foco: examinar as pernas antes de liberar"),
        ("O exame", "Gânglio de Chomel, porta de entrada, tromboflebite, exames"),
        ("Complicações", "Necrose da pele, fasciíte, sepse, linfedema"),
        ("Tratamento", "Do leve ao grave; corticoide só depois"),
        ("Prevenção", "Fechar as portas de entrada: pés e sapatos"),
    ]
    gap, cols = 16, 4
    bw = (W - gap * (cols - 1)) / cols
    pad = 8
    tam_t, tam_s = 9, 7.6
    # altura comum
    alturas = []
    for t, s in etapas:
        n = len(quebrar(s, 400, tam_s, bw - 2 * pad))
        alturas.append(30 + n * 10.2 + 6)
    bh = max(alturas)
    row_gap = 26
    partes = []
    y0 = 1
    pos = []
    for i, (t, s) in enumerate(etapas):
        r, c = divmod(i, cols)
        x = c * (bw + gap)
        y = y0 + r * (bh + row_gap)
        pos.append((x, y))
        partes.append(caixa(x + 0.5, y, bw - 1, bh))
        partes.append(selo(x + pad + 7.5, y + pad + 7.5, i + 1))
        partes.append(texto(x + pad + 20, y + pad + 10.5, t, 600, tam_t, TIT))
        yy = y + 34
        for ln in quebrar(s, 400, tam_s, bw - 2 * pad):
            partes.append(texto(x + pad, yy, ln, 400, tam_s, TXT))
            yy += 10.2
        if c < cols - 1:
            ym = y + bh / 2
            partes.append(linha([(x + bw + 2, ym), (x + bw + gap - 3, ym)]))
            partes.append(ponta(x + bw + gap - 1, ym, "direita", 3.5))
    # da etapa 4 para a 5
    x4, y4 = pos[3]
    x5, y5 = pos[4]
    ymid = y4 + bh + row_gap / 2
    partes.append(linha([(x4 + bw / 2, y4 + bh + 1), (x4 + bw / 2, ymid),
                         (x5 + bw / 2, ymid), (x5 + bw / 2, y5 - 6)]))
    partes.append(ponta(x5 + bw / 2, y5 - 1, "baixo", 3.5))
    salvar("trilha.svg", y0 + 2 * bh + row_gap + 2, partes)


# ---------------------------------------------------------------- planos
def planos():
    bx, bw = 26, 158          # bloco do corte
    camadas = [               # nome, altura, preenchimento
        ("Epiderme", 14, CLARO),
        ("Derme e linfáticos", 46, APOIO),
        ("Tecido subcutâneo", 50, "#FFFFFF"),
        ("Fáscia", 13, BORDA),
        ("Músculo", 58, CLARO),
    ]
    top = 10
    partes = []
    y = top
    centros = {}
    for nome, h, fill in camadas:
        partes.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="{h}" fill="{fill}" '
                      f'stroke="{BORDA}" stroke-width="1"/>')
        centros[nome] = y + h / 2
        if nome == "Derme e linfáticos":
            for i in range(5):
                cx = bx + 96 + (i % 3) * 18
                cy = y + 12 + (i // 3) * 20 + (i % 2) * 4
                partes.append(f'<ellipse cx="{cx}" cy="{cy}" rx="5" ry="3.2" fill="#FFFFFF" '
                              f'stroke="{SETA}" stroke-width="1"/>')
        if nome == "Tecido subcutâneo":
            for i in range(7):
                cx = bx + 92 + (i % 4) * 16 + (i // 4) * 8
                cy = y + 13 + (i // 4) * 22
                partes.append(f'<circle cx="{cx}" cy="{cy}" r="6.5" fill="none" '
                              f'stroke="{BORDA}" stroke-width="1"/>')
        if nome == "Músculo":
            for k in range(1, 6):
                yy = y + k * h / 6
                partes.append(f'<line x1="{bx + 80}" y1="{yy:.1f}" x2="{bx + bw - 6}" y2="{yy:.1f}" '
                              f'stroke="{BORDA}" stroke-width="1"/>')
        ty = y + h / 2 + 2.8
        partes.append(texto(bx + 7, ty, nome, 500, 7.4, TIT))
        y += h
    fundo = y
    # circulação
    cy0 = fundo + 12
    ch = 24
    partes.append(caixa(bx, cy0, bw, ch, fill="#FFFFFF", dash=True, r=6))
    partes.append(texto(bx + 7, cy0 + ch / 2 + 2.8, "Circulação", 500, 7.4, TIT))
    centros["Circulação"] = cy0 + ch / 2
    total = cy0 + ch
    # seta lateral: mais fundo, mais grave
    partes.append(linha([(10, top + 4), (10, total - 8)]))
    partes.append(ponta(10, total - 2, "baixo", 3.5))
    meio = (top + total) / 2
    partes.append(f'<text x="0" y="0" font-family="Inter" font-weight="500" font-size="7.2" '
                  f'fill="{CINZA}" text-anchor="middle" transform="translate(5.5 {meio:.1f}) rotate(-90)">'
                  f'mais fundo, mais grave</text>')
    # quadros à direita
    qx = 212
    qw = W - qx - 1
    pad = 8
    quadros = [
        ("Derme e linfáticos", "Pele: erisipela",
         "Começa na derme e nos linfáticos. Se a pele necrosa, é a erisipela necrotizante."),
        ("Fáscia", "Fáscia: fasciíte necrotizante",
         "A fáscia vira uma coisa liquefeita; os capilares trombosam e o corte não sangra."),
        ("Músculo", "Músculo",
         "No caso da jovem de 20 anos, o músculo estava liquefeito: ela perdeu o compartimento anterior da perna."),
        ("Circulação", "Circulação: sepse",
         "Na fasciíte, chega rápido, conforme a imunidade do paciente: na jovem, em 24 a 48 horas."),
    ]
    ultimo_fim = 0
    for alvo, tit, corpo in quadros:
        lns = quebrar(corpo, 400, 7.8, qw - 2 * pad)
        h = 22 + len(lns) * 10.4 + 3
        y = centros[alvo] - h / 2
        y = max(y, ultimo_fim + 6, 1)
        partes.append(caixa(qx, y, qw, h))
        partes.append(texto(qx + pad, y + 14, tit, 600, 8.6, TIT))
        yy = y + 26
        for ln in lns:
            partes.append(texto(qx + pad, yy, ln, 400, 7.8, TXT))
            yy += 10.4
        # conector
        cy = centros[alvo]
        alvo_y = min(max(cy, y + 8), y + h - 8)
        partes.append(linha([(bx + bw + 2, cy), (qx - 8, alvo_y)], w=1.1))
        partes.append(ponta(qx - 2, alvo_y, "direita", 3.2))
        ultimo_fim = y + h
    salvar("planos.svg", max(total, ultimo_fim) + 2, partes)


# ---------------------------------------------------------------- tratamento
def tratamento():
    gap = 12
    cw = (W - 2 * gap) / 3
    pad = 8
    partes = []
    # topo
    th = 26
    partes.append(caixa(0.5, 0.5, W - 1, th, fill=APOIO))
    partes.append(texto(W / 2, 17, "Erisipela: como o paciente está?", 600, 9, TIT, "middle"))
    colunas = [
        ("Leve", ["Trata em casa",
                  "Amoxicilina com clavulanato, ou cefalexina (cefalosporina de primeira geração)",
                  "A maior parte das erisipelas se resolve com antibiótico simples"]),
        ("Moderado", ["Interna na unidade de pronto atendimento",
                      "Penicilina cristalina, 2 a 4 milhões de unidades de 4 em 4 horas, ou oxacilina",
                      "Evoluiu mal? Amplia o espectro, como no grave"]),
        ("Grave", ["Amplia o espectro",
                   "Ceftriaxona ou ciprofloxacino, com clindamicina",
                   "Sem melhora: piperacilina com tazobactam; acima dela, vancomicina ou linezolida"]),
    ]
    y_cab = th + 18
    cab_h = 22
    tam = 7.9
    lh = 10.4
    # alturas de cada caixa
    caixas_col = []
    for nome, itens in colunas:
        hs = []
        for j, it in enumerate(itens):
            peso = 600 if j == 0 else 400
            n = len(quebrar(it, peso, tam, cw - 2 * pad))
            hs.append(12 + n * lh)
        caixas_col.append(hs)
    seta_v = 14
    alturas_tot = [sum(hs) + seta_v * (len(hs) - 1) for hs in caixas_col]
    base = y_cab + cab_h + seta_v + max(alturas_tot)
    for c, (nome, itens) in enumerate(colunas):
        x = c * (cw + gap)
        xm = x + cw / 2
        # seta do topo
        partes.append(linha([(xm, th + 1), (xm, y_cab - 5)]))
        partes.append(ponta(xm, y_cab - 1, "baixo", 3.5))
        partes.append(caixa(x + 0.5, y_cab, cw - 1, cab_h, fill=CLARO))
        partes.append(texto(xm, y_cab + 14.5, nome, 600, 9.2, TIT, "middle"))
        y = y_cab + cab_h + seta_v
        partes.append(linha([(xm, y_cab + cab_h + 1), (xm, y - 5)]))
        partes.append(ponta(xm, y - 1, "baixo", 3.5))
        hs = caixas_col[c]
        for j, it in enumerate(itens):
            h = hs[j]
            if j == len(itens) - 1:
                h = base - y          # última caixa estica até a base comum
            peso = 600 if j == 0 else 400
            cor = TIT if j == 0 else TXT
            partes.append(caixa(x + 0.5, y, cw - 1, h))
            yy = y + 6 + lh - 2.4
            for ln in quebrar(it, peso, tam, cw - 2 * pad):
                partes.append(texto(x + pad, yy, ln, peso, tam, cor))
                yy += lh
            if j < len(itens) - 1:
                partes.append(linha([(xm, y + h + 1), (xm, y + h + seta_v - 5)]))
                partes.append(ponta(xm, y + h + seta_v - 1, "baixo", 3.5))
            y += h + seta_v
    # rodapé: depois da infecção controlada
    yb = base + seta_v
    for c in range(3):
        xm = c * (cw + gap) + cw / 2
        partes.append(linha([(xm, base + 1), (xm, yb - 5)]))
        partes.append(ponta(xm, yb - 1, "baixo", 3.5))
    msg = ("Infecção controlada, mas a perna segue vermelha, inchada e dolorida: corticoide. "
           "Depois, tratar a micose e a frieira (fluconazol).")
    lns = quebrar(msg, 400, 8, W - 2 * pad - 4)
    bh = 22 + len(lns) * lh
    partes.append(caixa(0.5, yb, W - 1, bh, fill=APOIO))
    partes.append(texto(pad + 2, yb + 14, "Depois do antibiótico", 600, 8.6, TIT))
    yy = yb + 26
    for ln in lns:
        partes.append(texto(pad + 2, yy, ln, 400, 8, TXT))
        yy += lh
    salvar("tratamento.svg", yb + bh + 1, partes)


if __name__ == "__main__":
    trilha()
    planos()
    tratamento()
    print("ok: trilha.svg, planos.svg, tratamento.svg")
