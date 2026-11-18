#!/usr/bin/env python3
"""Figuras da apostila orto-a6.

Uso: python3 figuras.py <slides.pdf>
  - recorta as imagens dos slides (pdftoppm a 200 dpi) e desenha as setas;
  - desenha trilha.svg e principios.svg (texto medido com a fonte Inter da pasta fonts/).
O slides.pdf sai do slides.pptx original (soffice --headless --convert-to pdf).
"""
import os
import subprocess
import sys
import tempfile
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(AQUI, "fonts")
DPI = 200

# ---------------------------------------------------------------- imagens dos slides
# nome: (slide, [caixas em polegadas (x, y, largura, altura)])
RECORTES = {
    "img-entorse": (5, [(1.26, 1.98, 5.74, 4.45)]),
    "img-luxacao": (10, [(2.89, 3.11, 8.79, 4.06)]),
    "img-fratura": (12, [(7.0, 0.83, 5.95, 4.69)]),
    "img-femur": (30, [(1.55, 2.17, 10.71, 4.28)]),
    "img-ac": (60, [(0.33, 0.22, 10.8, 6.47)]),
    "img-colles": (84, [(6.48, 0.7, 4.9, 6.09)]),
    "img-torus": (90, [(2.82, 0.82, 6.47, 6.15)]),
    "img-pelve": (104, [(0.7, 1.45, 11.93, 4.61)]),
    "img-quinto": (132, [(0.72, 1.41, 4.74, 5.09)]),
}
IMOB = {  # grade de fotos das imobilizações
    "img-imob-tracao": (19, (6.93, 3.86, 4.34, 3.3)),
    "img-imob-velpeau": (20, (6.53, 1.63, 5.21, 5.21)),
    "img-imob-colar": (21, (3.49, 3.79, 3.17, 3.17)),
    "img-imob-colar2": (21, (7.46, 3.95, 3.17, 3.17)),
    "img-imob-putti": (22, (7.27, 1.44, 4.62, 4.62)),
    "img-imob-brace": (23, (8.19, 0.62, 3.9, 6.25)),
    "img-imob-robofoot": (24, (7.06, 1.98, 4.03, 4.03)),
    "img-imob-jones": (25, (7.72, 1.98, 4.36, 4.5)),
    "img-imob-tala": (26, (6.67, 1.71, 5.1, 4.58)),
    "img-imob-gesso": (27, (7.16, 3.23, 5.09, 3.73)),
    "img-imob-metalica": (28, (7.8, 1.8, 3.39, 3.27)),
    "img-imob-esparadrapo": (29, (7.26, 3.38, 5.16, 3.1)),
}
# setas (no recorte, em pixels a 200 dpi): (ponta, cauda)
SETAS = {
    "img-torus": [((1138, 812), (1272, 742))],
    "img-quinto": [((828, 700), (936, 846))],
}


def pagina(pdf, n, cache):
    if n not in cache:
        base = os.path.join(cache["_dir"], f"s{n}")
        subprocess.run(["pdftoppm", "-r", str(DPI), "-png", "-f", str(n), "-l", str(n),
                        "-singlefile", pdf, base], check=True)
        cache[n] = Image.open(base + ".png").convert("RGB")
    return cache[n]


def recorte(im, caixa):
    x, y, w, h = caixa
    b = (int(x * DPI), int(y * DPI), int((x + w) * DPI), int((y + h) * DPI))
    b = (max(0, b[0]), max(0, b[1]), min(im.width, b[2]), min(im.height, b[3]))
    return im.crop(b)


def seta(d, ponta, cauda, cor=(76, 154, 255), borda=(255, 255, 255)):
    import math
    (x1, y1), (x0, y0) = ponta, cauda
    ang = math.atan2(y1 - y0, x1 - x0)
    comp = math.hypot(x1 - x0, y1 - y0)
    larg, cab, abre = 9, 34, 22

    def pt(dist, lado):
        return (x0 + dist * math.cos(ang) - lado * math.sin(ang),
                y0 + dist * math.sin(ang) + lado * math.cos(ang))
    poly = [pt(0, -larg / 2), pt(comp - cab, -larg / 2), pt(comp - cab, -abre / 2 - larg / 2),
            pt(comp, 0), pt(comp - cab, abre / 2 + larg / 2), pt(comp - cab, larg / 2), pt(0, larg / 2)]
    d.polygon(poly, fill=cor, outline=borda, width=3)


def salvar(im, nome, maxw=1100):
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(os.path.join(AQUI, nome + ".jpg"), quality=86)


def imagens(pdf):
    with tempfile.TemporaryDirectory() as tmp:
        cache = {"_dir": tmp}
        for nome, (n, caixas) in RECORTES.items():
            im = recorte(pagina(pdf, n, cache), caixas[0])
            d = ImageDraw.Draw(im)
            for ponta, cauda in SETAS.get(nome, []):
                seta(d, ponta, cauda)
            salvar(im, nome)
        for nome, (n, caixa) in IMOB.items():
            im = recorte(pagina(pdf, n, cache), caixa)
            # encaixa num quadro 4:3 branco, para a grade ficar alinhada
            W, H = 480, 360
            esc = min(W / im.width, H / im.height)
            im = im.resize((int(im.width * esc), int(im.height * esc)), Image.LANCZOS)
            quadro = Image.new("RGB", (W, H), "white")
            quadro.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
            salvar(quadro, nome)


# ---------------------------------------------------------------- SVG
def fonte(peso, tam):
    return ImageFont.truetype(os.path.join(FONTS, f"Inter-{peso}.ttf"), tam * 10)


def mede(txt, peso, tam):
    return fonte(peso, tam).getlength(txt) / 10


def quebra(txt, peso, tam, larg):
    linhas, atual = [], ""
    for p in txt.split():
        t = (atual + " " + p).strip()
        if mede(t, peso, tam) <= larg or not atual:
            atual = t
        else:
            linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    return linhas


FAM = {"Regular": "Inter", "Medium": "Inter Medium", "SemiBold": "Inter SemiBold", "Bold": "Inter"}


def texto(x, y, linhas, peso, tam, cor, anc="start", entre=1.3):
    out = []
    w = ' font-weight="700"' if peso == "Bold" else ""
    for i, l in enumerate(linhas):
        l = l.replace("&", "&amp;")
        out.append(f'<text x="{x:.1f}" y="{y + i * tam * entre:.1f}" font-family="{FAM[peso]}"{w} '
                   f'font-size="{tam}" fill="{cor}" text-anchor="{anc}">{l}</text>')
    return "\n".join(out)


def seta_svg(x0, y0, x1, y1, cor="#8AA9DF"):
    """seta reta horizontal ou vertical, desenhada como polígono."""
    import math
    ang = math.atan2(y1 - y0, x1 - x0)
    comp = math.hypot(x1 - x0, y1 - y0)
    larg, cab, abre = 1.6, 5.5, 7

    def pt(dist, lado):
        return (x0 + dist * math.cos(ang) - lado * math.sin(ang),
                y0 + dist * math.sin(ang) + lado * math.cos(ang))
    pts = [pt(0, -larg / 2), pt(comp - cab, -larg / 2), pt(comp - cab, -abre / 2), pt(comp, 0),
           pt(comp - cab, abre / 2), pt(comp - cab, larg / 2), pt(0, larg / 2)]
    return '<polygon points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) + f'" fill="{cor}"/>'


def altura(w, num, titulo, sub):
    h = 37 if num else 16
    h += len(quebra(titulo, "SemiBold", 8.6, w - 16)) * 8.6 * 1.25 + 2
    if sub:
        h += (len(quebra(sub, "Regular", 7.6, w - 16)) - 1) * 7.6 * 1.32 + 7.6
    return h + 9


def caixa(x, y, w, h, num, titulo, sub, destaque=False):
    out = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="7" '
           f'fill="#FFFFFF" stroke="{"#0B5BD3" if destaque else "#C3D8F8"}" stroke-width="1"/>']
    tx = x + 8
    if num:
        out.append(f'<circle cx="{x + 15:.1f}" cy="{y + 15:.1f}" r="8" fill="#0B5BD3"/>')
        out.append(texto(x + 15, y + 18.2, [str(num)], "SemiBold", 8.5, "#FFFFFF", "middle"))
        ty = y + 37
    else:
        ty = y + 16
    lt = quebra(titulo, "SemiBold", 8.6, w - 16)
    out.append(texto(tx, ty, lt, "SemiBold", 8.6, "#16315C"))
    ty += len(lt) * 8.6 * 1.25 + 2
    if sub:
        out.append(texto(tx, ty, quebra(sub, "Regular", 7.6, w - 16), "Regular", 7.6, "#3A3A3C", entre=1.32))
    return "\n".join(out)


def svg(nome, w, h, corpo):
    with open(os.path.join(AQUI, nome), "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}pt" height="{h}pt" '
                f'viewBox="0 0 {w} {h}">\n{corpo}\n</svg>\n')


def trilha():
    W = 478
    passos1 = [
        ("Princípios", "imobilizar e tirar a dor"),
        ("Partes moles", "contusão, entorse, músculo"),
        ("Luxação e fratura", "emergência ou urgência"),
        ("Imobilizações", "tala, gesso, órteses"),
        ("Cirurgia", "osteossíntese e prótese"),
        ("Politrauma", "fratura exposta"),
    ]
    passos2 = [
        ("Radiografia: coluna", "duas incidências, sempre"),
        ("Radiografia: membro superior", "ombro, antebraço, punho"),
        ("Radiografia: membro inferior", "pelve, quadril, joelho, pé"),
    ]
    out = []
    g = 10
    y1 = 16
    out.append(texto(0, 10, ["TRATAR O TRAUMA"], "SemiBold", 7.2, "#6C6C70"))
    bw = (W - 5 * g) / 6
    h1 = max(altura(bw, 1, t, sub) for t, sub in passos1)
    for i, (t, s) in enumerate(passos1):
        x = i * (bw + g)
        out.append(caixa(x, y1, bw, h1, i + 1, t, s))
        if i < 5:
            out.append(seta_svg(x + bw + 1.5, y1 + h1 / 2, x + bw + g - 1.5, y1 + h1 / 2))
    y2 = y1 + h1 + 26
    out.append(seta_svg(W / 2, y1 + h1 + 3, W / 2, y2 - 12))
    out.append(texto(0, y2 - 6, ["LER A RADIOGRAFIA DE CADA REGIÃO"], "SemiBold", 7.2, "#6C6C70"))
    bw2 = (W - 2 * g) / 3
    h2 = max(altura(bw2, 1, t, sub) for t, sub in passos2)
    for i, (t, s) in enumerate(passos2):
        x = i * (bw2 + g)
        out.append(caixa(x, y2, bw2, h2, i + 7, t, s))
        if i < 2:
            out.append(seta_svg(x + bw2 + 1.5, y2 + h2 / 2, x + bw2 + g - 1.5, y2 + h2 / 2))
    svg("trilha.svg", W, int(y2 + h2 + 2), "\n".join(out))


def principios():
    W = 478
    out = []
    g = 14
    bw = (W - 3 * g) / 4
    p = [("Diagnóstico inicial", "o que aconteceu e onde dói"),
         ("Imobilizar", "proteger a lesão e aliviar"),
         ("Analgesia", "remédio, gelo"),
         ("Rever o diagnóstico", "exame mais apurado, se precisar")]
    h = max(altura(bw, 1, t, sb) for t, sb in p)
    for i, (t, s) in enumerate(p):
        x = i * (bw + g)
        out.append(caixa(x, 0, bw, h, i + 1, t, s))
        if i < 3:
            out.append(seta_svg(x + bw + 2, h / 2, x + bw + g - 2, h / 2))
    # segunda linha: definitivo (com dois caminhos) e reabilitação
    y = h + 26
    out.append(seta_svg(W - bw / 2, h + 3, W - bw / 2, y - 3))
    # definitivo à direita, reabilitação à esquerda (o caminho volta)
    dw = 2 * bw + g
    dx = W - dw
    hh = 82
    out.append(f'<rect x="{dx:.1f}" y="{y:.1f}" width="{dw:.1f}" height="{hh}" rx="7" fill="#FFFFFF" stroke="#C3D8F8"/>')
    out.append(f'<circle cx="{dx + 15:.1f}" cy="{y + 15:.1f}" r="8" fill="#0B5BD3"/>')
    out.append(texto(dx + 15, y + 18.2, ["5"], "SemiBold", 8.5, "#FFFFFF", "middle"))
    out.append(texto(dx + 29, y + 18, ["Tratamento definitivo"], "SemiBold", 8.6, "#16315C"))
    pw = (dw - 16 - 10) / 2
    for j, (t, s) in enumerate([("Conservador", "tala, gesso, órtese"), ("Cirúrgico", "osteossíntese, prótese, fixador")]):
        px = dx + 8 + j * (pw + 10)
        out.append(f'<rect x="{px:.1f}" y="{y + 28:.1f}" width="{pw:.1f}" height="46" rx="6" fill="#F5F8FF" stroke="#C3D8F8"/>')
        out.append(texto(px + pw / 2, y + 42, [t], "SemiBold", 8, "#0B5BD3", "middle"))
        out.append(texto(px + pw / 2, y + 54, quebra(s, "Regular", 7.2, pw - 12), "Regular", 7.2, "#3A3A3C", "middle"))
    out.append(seta_svg(dx - 2, y + hh / 2, dx - g + 2, y + hh / 2))
    rw = dx - g
    out.append(f'<rect x="0" y="{y:.1f}" width="{rw:.1f}" height="{hh}" rx="7" fill="#FFFFFF" stroke="#0B5BD3"/>')
    out.append(texto(10, y + 18, ["Objetivo: reabilitação"], "SemiBold", 8.6, "#16315C"))
    out.append(texto(10, y + 33, quebra("física, psicológica e laboral: voltar a trabalhar, ao esporte, ao que fazia antes",
                                         "Regular", 7.8, rw - 20), "Regular", 7.8, "#3A3A3C", entre=1.32))
    svg("principios.svg", W, int(y + hh + 2), "\n".join(out))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        imagens(sys.argv[1])
    trilha()
    principios()
    print("figuras prontas")
