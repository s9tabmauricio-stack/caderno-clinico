"""Figuras da apostila orto-a5 (Patologias da coluna).

Gera os SVGs (trilha, fluxograma do colar, barras toracolombares, tronco,
hérnias, escada analgésica, curvas de proteína C reativa e hemossedimentação)
e as imagens de exame marcadas a partir dos recortes dos slides.
Uso: python3 figuras.py <pasta com os recortes c19.png, c42.png, c103m.png>
"""
import math
import os
import sys
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
W = 478
AZUL = "#0B5BD3"
MARINHO = "#16315C"
BORDA = "#C3D8F8"
APOIO = "#F5F8FF"
SETA = "#8AA9DF"
TXT = "#1F2933"
CINZA = "#6C6C70"
VERDE_F, VERDE_B, VERDE_T = "#E7F7EC", "#BFE5CB", "#1E7A34"

_cache = {}


def larg(t, peso, tam):
    k = (peso, tam)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(F[peso], tam * 10)
    return _cache[k].getlength(t) / 10


def quebra(t, peso, tam, maxw):
    linhas, atual = [], ""
    for p in t.split():
        teste = (atual + " " + p).strip()
        if larg(teste, peso, tam) <= maxw or not atual:
            atual = teste
        else:
            linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    return linhas


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def texto(x, y, t, peso="r", tam=8, cor=TXT, anc="start", extra=""):
    fam, w = FAM[peso]
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-weight="{w}" '
            f'font-size="{tam}" fill="{cor}" text-anchor="{anc}" {extra}>{esc(t)}</text>')


def bloco(x, y, w, linhas, peso="r", tam=8, cor=TXT, lh=None, anc="middle"):
    """linhas já quebradas; y = topo do bloco. Devolve (svg, altura)."""
    lh = lh or tam * 1.32
    out = []
    for i, l in enumerate(linhas):
        yy = y + tam * 0.95 + i * lh
        xx = x + w / 2 if anc == "middle" else x
        out.append(texto(xx, yy, l, peso, tam, cor, anc))
    return "".join(out), len(linhas) * lh


def caixa(x, y, w, h, fill="#FFFFFF", stroke=BORDA, rx=7, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def seta(x1, y1, x2, y2, cor=SETA, esp=1.6, cab=5):
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - cab * math.cos(ang), y2 - cab * math.sin(ang)
    px, py = -math.sin(ang), math.cos(ang)
    pts = f"{x2:.1f},{y2:.1f} {bx + px * cab * 0.6:.1f},{by + py * cab * 0.6:.1f} {bx - px * cab * 0.6:.1f},{by - py * cab * 0.6:.1f}"
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{cor}" stroke-width="{esp}"/>'
            f'<polygon points="{pts}" fill="{cor}"/>')


def salvar(nome, h, corpo):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{h:.0f}pt" '
           f'viewBox="0 0 {W} {h:.0f}">{corpo}</svg>')
    with open(os.path.join(AQUI, nome), "w", encoding="utf-8") as f:
        f.write(svg)


# ---------- 1. trilha ----------
def trilha():
    etapas = [("Anatomia", "01"), ("Fratura cervical", "02"), ("Fratura toracolombar", "03"),
              ("Nível da lesão e os dois choques", "04"), ("Dor lombar", "05"),
              ("Hérnia e tratamento", "06 e 07"), ("Cauda equina", "08"), ("Infecção e mal de Pott", "09 e 10")]
    n = len(etapas)
    passo = W / n
    out = [f'<line x1="{passo / 2:.1f}" y1="16" x2="{W - passo / 2:.1f}" y2="16" stroke="{BORDA}" stroke-width="2"/>']
    for i, (nome, cap) in enumerate(etapas):
        cx = passo / 2 + i * passo
        out.append(f'<circle cx="{cx:.1f}" cy="16" r="11" fill="{AZUL}"/>')
        out.append(texto(cx, 19.5, str(i + 1), "s", 9.5, "#FFFFFF", "middle"))
        ls = quebra(nome, "s", 7.6, passo - 6)
        s, h = bloco(cx - passo / 2, 33, passo, ls, "s", 7.6, MARINHO)
        out.append(s)
        out.append(texto(cx, 33 + h + 9, "cap. " + cap, "r", 6.8, CINZA, "middle"))
    salvar("trilha.svg", 84, "".join(out))


# ---------- 2. fluxograma do colar ----------
def colar():
    out = []
    pad = 7
    tam = 8
    # topo
    t = "Politraumatizado: considere lesão cervical em todos. Colar cervical (e prancha) até examinar."
    ls = quebra(t, "s", 8.4, W - 40)
    h0 = len(ls) * 8.4 * 1.32 + 2 * pad
    out.append(caixa(0, 0, W, h0, APOIO, BORDA))
    s, _ = bloco(0, pad, W, ls, "s", 8.4, MARINHO)
    out.append(s)
    gap = 10
    cw = (W - 2 * gap) / 3
    xs = [i * (cw + gap) for i in range(3)]
    y1 = h0 + 16
    conds = ["Acordado e orientado, sem dor à palpação e sem déficit neurológico",
             "Confuso ou desorientado",
             "Dor cervical ou sintoma neurológico"]
    acoes = ["Tira o colar e a prancha, com movimentação em bloco",
             "Exame de imagem mantendo o colar",
             "Tomografia direto"]
    lc = [quebra(c, "s", tam, cw - 2 * pad) for c in conds]
    hc = max(len(l) for l in lc) * tam * 1.32 + 2 * pad
    for i in range(3):
        cx = xs[i] + cw / 2
        out.append(seta(cx, h0, cx, y1))
        out.append(caixa(xs[i], y1, cw, hc))
        s, _ = bloco(xs[i], y1 + pad, cw, lc[i], "s", tam, TXT)
        out.append(s)
    y2 = y1 + hc + 16
    la = [quebra(a, "r", tam, cw - 2 * pad) for a in acoes]
    ha = max(len(l) for l in la) * tam * 1.32 + 2 * pad
    # final convergente (colunas 2 e 3)
    y3 = y2 + ha + 16
    tf = "Tomografia normal e Glasgow 15: tira o colar, mesmo com dor"
    lf = quebra(tf, "s", tam, 2 * cw + gap - 2 * pad)
    hf = len(lf) * tam * 1.32 + 2 * pad
    base = y3 + hf
    for i in range(3):
        cx = xs[i] + cw / 2
        out.append(seta(cx, y1 + hc, cx, y2))
        if i == 0:
            out.append(caixa(xs[i], y2, cw, base - y2, VERDE_F, VERDE_B))
            hh = len(la[0]) * tam * 1.32
            s, _ = bloco(xs[i], y2 + (base - y2 - hh) / 2, cw, la[0], "s", tam, VERDE_T)
        else:
            out.append(caixa(xs[i], y2, cw, ha))
            s, _ = bloco(xs[i], y2 + pad, cw, la[i], "r", tam, TXT)
            out.append(seta(cx, y2 + ha, cx, y3))
        out.append(s)
    out.append(caixa(xs[1], y3, 2 * cw + gap, hf, VERDE_F, VERDE_B))
    s, _ = bloco(xs[1], y3 + pad, 2 * cw + gap, lf, "s", tam, VERDE_T)
    out.append(s)
    # nota
    yn = base + 10
    tn = ("Na dúvida, mantenha o colar. Tomografia normal e sintoma que persiste: ressonância (controversa no "
          "início) ou colar e reavaliação.")
    ln = quebra(tn, "r", 7.8, W - 2 * pad - 6)
    hn = len(ln) * 7.8 * 1.32 + 2 * 6
    out.append(caixa(0, yn, W, hn, APOIO, BORDA, dash="3 2"))
    s, _ = bloco(0, yn + 6, W, ln, "r", 7.8, CINZA)
    out.append(s)
    salvar("colar.svg", yn + hn + 1, "".join(out))


# ---------- 3. barras toracolombares ----------
def barras():
    dados = [("L1", 35, "1º"), ("T12", 18, "2º"), ("L2", 12, "3º"), ("T11", 10, "4º")]
    out = []
    x0, maxw = 64, 250
    for i, (niv, pct, ordem) in enumerate(dados):
        y = 6 + i * 25
        out.append(texto(0, y + 13, ordem, "r", 8, CINZA))
        out.append(texto(22, y + 13.5, niv, "s", 10, MARINHO))
        w = maxw * pct / 35
        out.append(f'<rect x="{x0}" y="{y + 2}" width="{w:.1f}" height="15" rx="4" fill="{AZUL if i == 0 else SETA}"/>')
        out.append(texto(x0 + w + 6, y + 13.5, f"{pct}%", "s", 9, TXT))
    # caixa lateral
    bx = 360
    out.append(caixa(bx, 4, W - bx, 98, APOIO, BORDA))
    ls = quebra("Transição toracolombar (T11 a L2): até 80% das fraturas toracolombares. É onde a coluna mais se mexe.",
                "r", 7.8, W - bx - 14)
    s, _ = bloco(bx, 13, W - bx, ls, "r", 7.8, TXT)
    out.append(s)
    salvar("barras.svg", 108, "".join(out))


# ---------- 4. tronco e dermátomos ----------
def tronco():
    k = 0.78  # escala do desenho do corpo
    corpo_svg = []
    cx = 120
    corpo_svg.append(f'<circle cx="{cx}" cy="20" r="15" fill="#FFFFFF" stroke="{MARINHO}" stroke-width="1.6"/>')
    corpo_svg.append(f'<path d="M{cx - 7} 34 L{cx - 8} 44 M{cx + 7} 34 L{cx + 8} 44" stroke="{MARINHO}" stroke-width="1.6" fill="none"/>')
    corpo = (f"M{cx - 8} 44 Q{cx - 40} 44 {cx - 56} 52 L{cx - 70} 118 L{cx - 60} 120 L{cx - 50} 80 "
             f"L{cx - 48} 132 Q{cx - 50} 170 {cx - 44} 196 L{cx + 44} 196 Q{cx + 50} 170 {cx + 48} 132 "
             f"L{cx + 50} 80 L{cx + 60} 120 L{cx + 70} 118 L{cx + 56} 52 Q{cx + 40} 44 {cx + 8} 44 Z")
    corpo_svg.append(f'<path d="{corpo}" fill="#FFFFFF" stroke="{MARINHO}" stroke-width="1.6"/>')
    corpo_svg.append(f'<circle cx="{cx - 22}" cy="76" r="3" fill="{MARINHO}"/><circle cx="{cx + 22}" cy="76" r="3" fill="{MARINHO}"/>')
    corpo_svg.append(f'<path d="M{cx - 5} 96 L{cx} 103 L{cx + 5} 96" stroke="{MARINHO}" stroke-width="1.5" fill="none"/>')
    corpo_svg.append(f'<circle cx="{cx}" cy="136" r="3.5" fill="none" stroke="{MARINHO}" stroke-width="1.5"/>')
    corpo_svg.append(f'<path d="M{cx - 40} 166 L{cx - 10} 192 M{cx + 40} 166 L{cx + 10} 192" stroke="{MARINHO}" stroke-width="1.5" fill="none"/>')
    niveis = [("T4", "linha dos mamilos", 76), ("T7", "apêndice xifoide", 100),
              ("T10", "cicatriz umbilical", 136), ("T12", "virilha, a região inguinal (às vezes L1)", 180)]
    ox = 20
    out = [f'<g transform="translate({ox} 2) scale({k})">' + "".join(corpo_svg) + '</g>']
    xl = ox + (cx + 62) * k
    for niv, nome, y in niveis:
        yy = 2 + y * k
        out.append(f'<line x1="{ox + (cx - 60) * k:.1f}" y1="{yy:.1f}" x2="250" y2="{yy:.1f}" stroke="{SETA}" stroke-width="1" stroke-dasharray="3 2"/>')
        out.append(f'<rect x="252" y="{yy - 8.5:.1f}" width="34" height="17" rx="8.5" fill="{AZUL}"/>')
        out.append(texto(269, yy + 3.3, niv, "s", 9, "#FFFFFF", "middle"))
        out.append(texto(294, yy + 3.3, nome, "m", 8.6, TXT))
    salvar("tronco.svg", 2 + 198 * k, "".join(out))


# ---------- 5. hérnias ----------
def hernias():
    out = []
    n = 4
    cw = W / n
    nomes = [("Disco normal", "Núcleo no centro, ânulo inteiro."),
             ("Protrusa", "Só abaula: o ânulo não se rompe."),
             ("Extrusa", "O ânulo se rompe e o material sai; o corpo pode reabsorver."),
             ("Sequestrada", "Um fragmento solta e migra para longe do disco.")]
    for i in range(n):
        cx = cw * i + cw / 2
        cy = 42
        anel = f'<ellipse cx="{cx}" cy="{cy}" rx="44" ry="30" fill="{BORDA}" stroke="{MARINHO}" stroke-width="1.2"/>'
        nuc_cor = AZUL
        # canal (saco dural) atrás do disco
        canal = f'<ellipse cx="{cx}" cy="{cy + 50}" rx="17" ry="11" fill="{APOIO}" stroke="{SETA}" stroke-width="1.2"/>'
        out.append(canal)
        if i == 1:
            out.append(f'<ellipse cx="{cx}" cy="{cy + 22}" rx="22" ry="14" fill="{BORDA}" stroke="{MARINHO}" stroke-width="1.2"/>')
            out.append(anel.replace('stroke="#16315C"', 'stroke="#16315C"'))
            # apaga a costura entre o anel e o abaulamento
            out.append(f'<ellipse cx="{cx}" cy="{cy + 22}" rx="20.8" ry="12.8" fill="{BORDA}"/>')
            out.append(f'<ellipse cx="{cx}" cy="{cy + 8}" rx="19" ry="13" fill="{nuc_cor}"/>')
        else:
            out.append(anel)
            if i == 0:
                out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="19" ry="12" fill="{nuc_cor}"/>')
            elif i == 2:
                out.append(f'<ellipse cx="{cx}" cy="{cy + 4}" rx="18" ry="12" fill="{nuc_cor}"/>')
                out.append(f'<rect x="{cx - 6}" y="{cy + 8}" width="12" height="26" fill="{nuc_cor}"/>')
                out.append(f'<ellipse cx="{cx}" cy="{cy + 36}" rx="12" ry="7" fill="{nuc_cor}"/>')
            else:
                out.append(f'<ellipse cx="{cx}" cy="{cy + 2}" rx="17" ry="11" fill="{nuc_cor}"/>')
                out.append(f'<rect x="{cx - 5}" y="{cy + 24}" width="10" height="8" fill="#FFFFFF"/>')
                out.append(f'<ellipse cx="{cx + 26}" cy="{cy + 46}" rx="8" ry="6" fill="{nuc_cor}"/>')
        nome, desc = nomes[i]
        out.append(texto(cx, 124, nome, "s", 9, MARINHO, "middle"))
        ls = quebra(desc, "r", 7.6, cw - 10)
        s, _ = bloco(cx - cw / 2, 129, cw, ls, "r", 7.6, TXT)
        out.append(s)
    out.append(texto(4, 96, "canal", "r", 6.8, CINZA))
    out.append(texto(4, 9, "frente", "r", 6.8, CINZA))
    salvar("hernias.svg", 168, "".join(out))


# ---------- 6. escada analgésica ----------
def escada():
    out = []
    degraus = [
        ("Degrau 1", "Analgésicos não opioides", ""),
        ("Degrau 2", "Opioides fracos", "Tramadol, codeína"),
        ("Degrau 3", "Opioides fortes", "Morfina, metadona, buprenorfina, fentanil, oxicodona, tapentadol"),
        ("Degrau 4", "Procedimentos intervencionistas",
         "Bloqueios periféricos e centrais, bombas de infusão, radiofrequência pulsada e ablativa, "
         "analgesia controlada pelo paciente, infiltrações, neuroestimulação"),
    ]
    base = 236
    alturas = [62, 92, 132, 176]
    gap = 4
    cw = (W - 3 * gap) / 4
    fills = ["#FFFFFF", "#F5F8FF", "#E8F0FE", "#DCE7FB"]
    for i, (t, sub, ex) in enumerate(degraus):
        x = i * (cw + gap)
        h = alturas[i]
        y = base - h
        out.append(caixa(x, y, cw, h, fills[i], BORDA))
        out.append(texto(x + 8, y + 15, t, "s", 9.2, AZUL))
        ls = quebra(sub, "s", 8, cw - 14)
        s, hh = bloco(x + 8, y + 21, cw - 14, ls, "s", 8, MARINHO, anc="start")
        out.append(s)
        yy = y + 21 + hh + 2
        if ex:
            ls = quebra(ex, "r", 7.6, cw - 14)
            s, hh2 = bloco(x + 8, yy, cw - 14, ls, "r", 7.6, TXT, anc="start")
            out.append(s)
            yy += hh2 + 2
        out.append(texto(x + 8, base - 8, "com ou sem adjuvantes", "r", 6.9, CINZA))
    # setas diagonais na área livre
    out.append(seta(14, 150, 300, 40, AZUL, 1.6, 6))
    out.append(seta(318, 22, 32, 132, SETA, 1.6, 6))
    out.append(texto(118, 128, "Dor crônica: sobe os degraus", "s", 8, AZUL, "start",
                     'transform="rotate(-21 118 128)"'))
    out.append(texto(96, 86, "Dor aguda: desce os degraus", "s", 8, "#4F6FA8", "start",
                     'transform="rotate(-21 96 86)"'))
    salvar("escada.svg", base + 2, "".join(out))


# ---------- 7. curvas PCR × VHS ----------
def curvas():
    out = []
    x0, y0, x1 = 30, 128, 470
    out.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{CINZA}" stroke-width="1"/>')
    out.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="10" stroke="{CINZA}" stroke-width="1"/>')
    out.append(texto(x1, y0 + 13, "tempo", "r", 7.4, CINZA, "end"))
    out.append(texto(x0 + 4, 14, "nível no sangue", "r", 7.4, CINZA))
    for xm, rot in [(40, "começa a infecção"), (250, "infecção controlada")]:
        out.append(f'<line x1="{xm}" y1="{y0}" x2="{xm}" y2="{y0 + 4}" stroke="{CINZA}"/>')
        out.append(texto(xm, y0 + 13, rot, "r", 7.4, CINZA, "start" if xm < 100 else "middle"))
    pcr = f"M40 {y0 - 2} C70 {y0 - 2} 80 42 110 40 C150 38 170 {y0 - 6} 250 {y0 - 4}"
    vhs = f"M40 {y0 - 2} C120 {y0 - 4} 170 64 240 60 C320 56 360 {y0 - 8} 450 {y0 - 4}"
    out.append(f'<path d="{pcr}" fill="none" stroke="{AZUL}" stroke-width="2.4"/>')
    out.append(f'<path d="{vhs}" fill="none" stroke="{SETA}" stroke-width="2.4" stroke-dasharray="6 3"/>')
    lx = 290
    out.append(f'<line x1="{lx}" y1="12" x2="{lx + 22}" y2="12" stroke="{AZUL}" stroke-width="2.4"/>')
    out.append(texto(lx + 28, 15, "Proteína C reativa:", "s", 8.2, AZUL))
    out.append(texto(lx + 28, 26, "primeira a subir, primeira a cair", "r", 7.6, TXT))
    out.append(f'<line x1="{lx}" y1="38" x2="{lx + 22}" y2="38" stroke="{SETA}" stroke-width="2.4" stroke-dasharray="6 3"/>')
    out.append(texto(lx + 28, 41, "Hemossedimentação:", "s", 8.2, "#4F6FA8"))
    out.append(texto(lx + 28, 52, "última a subir, última a cair", "r", 7.6, TXT))
    salvar("curvas.svg", y0 + 18, "".join(out))


# ---------- 8. imagens de exame marcadas ----------
def marcar(origem, destino, marcas, escala=1.0):
    im = Image.open(origem).convert("RGB")
    if escala != 1.0:
        im = im.resize((int(im.width * escala), int(im.height * escala)), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    r = max(16, int(im.width * 0.03))
    fonte = ImageFont.truetype(F["s"], int(r * 1.25))
    for num, (mx, my), alvo in marcas:
        mx, my = mx * escala, my * escala
        if alvo:
            ax, ay = alvo[0] * escala, alvo[1] * escala
            ang = math.atan2(ay - my, ax - mx)
            sx, sy = mx + r * math.cos(ang), my + r * math.sin(ang)
            cab = r * 0.9
            bx, by = ax - cab * math.cos(ang), ay - cab * math.sin(ang)
            px, py = -math.sin(ang), math.cos(ang)
            for cor, esp in (("#FFFFFF", 9), (AZUL, 5)):
                d.line([(sx, sy), (bx, by)], fill=cor, width=esp)
            tri = [(ax, ay), (bx + px * cab * 0.6, by + py * cab * 0.6), (bx - px * cab * 0.6, by - py * cab * 0.6)]
            d.polygon(tri, fill=AZUL, outline="#FFFFFF")
        d.ellipse([mx - r - 3, my - r - 3, mx + r + 3, my + r + 3], fill="#FFFFFF")
        d.ellipse([mx - r, my - r, mx + r, my + r], fill=AZUL)
        d.text((mx, my), str(num), font=fonte, fill="#FFFFFF", anchor="mm")
    im.save(os.path.join(AQUI, destino), optimize=True)


def exames(pasta):
    marcar(os.path.join(pasta, "c19.png"), "exame-cervical.png",
           [(1, (620, 240), (480, 335)), (2, (640, 800), (588, 712))])
    marcar(os.path.join(pasta, "c42.png"), "exame-tomografia.png",
           [(1, (70, 610), (178, 610)), (2, (470, 520), (352, 590))])
    marcar(os.path.join(pasta, "c103m.png"), "exame-pott.png",
           [(1, (50, 560), (150, 440)), (2, (620, 170), (360, 320))])


if __name__ == "__main__":
    trilha(); colar(); barras(); tronco(); hernias(); escada(); curvas()
    if len(sys.argv) > 1:
        exames(sys.argv[1])
    print("figuras prontas")
