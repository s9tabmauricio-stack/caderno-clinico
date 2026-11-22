#!/usr/bin/env python3
"""Desenha as figuras SVG da apostila angio-a11 (rodar na pasta da aula: python3 figuras.py)."""
from PIL import ImageFont

FONT = {400: "fonts/Inter-Regular.ttf", 500: "fonts/Inter-Medium.ttf",
        600: "fonts/Inter-SemiBold.ttf", 700: "fonts/Inter-Bold.ttf"}
FAM = {400: "Inter", 500: "Inter Medium", 600: "Inter SemiBold", 700: "Inter"}
_cache = {}

AZUL_BORDA = "#C3D8F8"
APOIO = "#F5F8FF"
SETA = "#8AA9DF"
TXT = "#1F2933"
TIT = "#16315C"
AZUL = "#0B5BD3"
CINZA = "#6C6C70"
W = 478


def font(size, weight):
    k = (size, weight)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(FONT[weight], size)
    return _cache[k]


def tw(s, size, weight=400):
    return font(size, weight).getlength(s)


def wrap(s, size, maxw, weight=400):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if tw(t, size, weight) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size, weight=400, fill=TXT, anchor="start"):
    fw = 700 if weight == 700 else 400
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FAM[weight]}" font-weight="{fw}" '
            f'font-size="{size}" fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>')


def lines_block(x, y, lines, size, weight=400, fill=TXT, anchor="start", lh=1.3):
    out = []
    for i, ln in enumerate(lines):
        out.append(text(x, y + i * size * lh, ln, size, weight, fill, anchor))
    return out


def rect(x, y, w, h, r=7, fill="#FFFFFF", stroke=AZUL_BORDA, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def arrow_h(x1, x2, y, color=SETA, head=5):
    """Seta horizontal de x1 a x2 (polígono, sem marker)."""
    d = 1 if x2 > x1 else -1
    xb = x2 - d * head
    return (f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{xb:.1f}" y2="{y:.1f}" stroke="{color}" stroke-width="1.6"/>'
            f'<polygon points="{x2:.1f},{y:.1f} {xb:.1f},{y - head * 0.75:.1f} {xb:.1f},{y + head * 0.75:.1f}" fill="{color}"/>')


def arrow_v(x, y1, y2, color=SETA, head=5):
    d = 1 if y2 > y1 else -1
    yb = y2 - d * head
    return (f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{yb:.1f}" stroke="{color}" stroke-width="1.6"/>'
            f'<polygon points="{x:.1f},{y2:.1f} {x - head * 0.75:.1f},{yb:.1f} {x + head * 0.75:.1f},{yb:.1f}" fill="{color}"/>')


def svg(h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{h}pt" viewBox="0 0 {W} {h}">\n'
            + "\n".join(body) + "\n</svg>\n")


def box_text(x, y, w, h, title, sub=None, tsize=8.4, ssize=7.4, fill="#FFFFFF", stroke=AZUL_BORDA,
             dash=None, tcolor=TIT, align="middle", pad=7):
    """Caixa com título (e subtítulo) centrados na vertical."""
    out = [rect(x, y, w, h, fill=fill, stroke=stroke, dash=dash)]
    tl = wrap(title, tsize, w - 2 * pad, 600)
    sl = wrap(sub, ssize, w - 2 * pad, 400) if sub else []
    th = len(tl) * tsize * 1.25 + (len(sl) * ssize * 1.3 + 2 if sl else 0)
    yy = y + (h - th) / 2 + tsize * 0.95
    cx = x + w / 2 if align == "middle" else x + pad
    out += lines_block(cx, yy, tl, tsize, 600, tcolor, align, 1.25)
    if sl:
        yy2 = yy + len(tl) * tsize * 1.25 + 1
        out += lines_block(cx, yy2, sl, ssize, 400, CINZA, align, 1.3)
    return out


# ---------------------------------------------------------------- trilha
def trilha():
    etapas = [
        ("Os vasos do cérebro", "Carótidas, vertebrais e polígono de Willis"),
        ("Placa e acidente vascular", "A placa instável solta êmbolos"),
        ("Sintomas e rastreamento", "Sinais de alarme e quem faz ultrassom"),
        ("Doppler", "Grau da estenose, aspecto da placa e velocidades"),
        ("Quem opera", "Sintoma, grau e risco do serviço"),
        ("O stent", "Pescoço hostil e filtro de proteção"),
        ("Tratamento clínico", "Hábitos, ácido acetilsalicílico e estatina"),
        ("Cirurgia e complicações", "Endarterectomia ou angioplastia"),
    ]
    bw, bh, gap = 104, 62, 20.67
    body = []
    for i, (t, s) in enumerate(etapas):
        row, col = divmod(i, 4)
        if row == 1:
            col = 3 - col  # serpentina
        x = col * (bw + gap)
        y = 6 + row * (bh + 30)
        body.append(rect(x, y, bw, bh, r=9))
        # selo numerado
        body.append(f'<circle cx="{x + 14:.1f}" cy="{y + 14:.1f}" r="8" fill="{AZUL}"/>')
        body.append(text(x + 14, y + 17.2, str(i + 1), 8.5, 600, "#FFFFFF", "middle"))
        tl = wrap(t, 8.4, bw - 30, 600)
        if len(tl) == 1:
            body.append(text(x + 27, y + 17.2, tl[0], 8.4, 600, TIT))
            yy = y + 31
        else:
            body += lines_block(x + 27, y + 13.5, tl, 8.4, 600, TIT, lh=1.2)
            yy = y + 13.5 + len(tl) * 8.4 * 1.2 + 4
        body += lines_block(x + 8, yy + 3, wrap(s, 7.3, bw - 16), 7.3, 400, CINZA, lh=1.3)
        # setas
        if i < 7:
            if i == 3:
                body.append(arrow_v(x + bw / 2, y + bh + 2, y + bh + 28))
            elif row == 0:
                body.append(arrow_h(x + bw + 2, x + bw + gap - 2, y + bh / 2))
            else:
                body.append(arrow_h(x - 2, x - gap + 2, y + bh / 2))
    h = 6 + 2 * bh + 30 + 6
    return svg(h, body)


# ---------------------------------------------------------------- anatomia
def anatomia():
    body = []
    top = 22
    rh, rg = 40, 8
    rows_y = [top + i * (rh + rg) for i in range(4)]
    H = rows_y[-1] + rh + 6
    # colunas
    c1x, c1w = 0, 50
    c2x, c2w = 63, 84
    c3x, c3w = 160, 84
    c4x, c4w = 257, 94
    c5x, c5w = 364, 114
    heads = [(c1x + c1w / 2, "Arco"), (c2x + c2w / 2, "Troncos"), (c3x + c3w / 2, "Ramos"),
             (c4x + c4w / 2, "No pescoço"), (c5x + c5w / 2, "Na base do cérebro")]
    for x, t in heads:
        body.append(text(x, 11, t.upper(), 6.6, 600, AZUL, "middle"))
    # c1 arco
    body.append(rect(c1x, rows_y[0], c1w, rows_y[3] + rh - rows_y[0], fill=APOIO))
    body += lines_block(c1x + c1w / 2, (rows_y[0] + rows_y[3] + rh) / 2 - 4, ["Arco da", "aorta"], 8.4, 600, TIT, "middle", 1.25)
    # c2
    yb_top, yb_bot = rows_y[0], rows_y[1] + rh
    body += box_text(c2x, yb_top, c2w, yb_bot - yb_top, "Tronco braquiocefálico", "só do lado direito; abre-se em dois, como um L")
    body += box_text(c2x, rows_y[2], c2w + c3w + 13, rh, "Carótida comum esquerda", "sai direto do arco")
    body += box_text(c2x, rows_y[3], c2w + c3w + 13, rh, "Subclávia esquerda", "manda para baixo a torácica interna")
    # c3
    body += box_text(c3x, rows_y[0], c3w, rh, "Subclávia direita")
    body += box_text(c3x, rows_y[1], c3w, rh, "Carótida comum direita")
    # c4
    body += box_text(c4x, rows_y[0], c4w, rh, "Vertebral direita", "dentro dos processos transversos")
    body += box_text(c4x, rows_y[1], c4w, rh, "Carótida interna direita", "depois da bifurcação")
    body += box_text(c4x, rows_y[2], c4w, rh, "Carótida interna esquerda", "depois da bifurcação")
    body += box_text(c4x, rows_y[3], c4w, rh, "Vertebral esquerda", "dentro dos processos transversos")
    # c5 Willis
    y5, h5 = rows_y[0], rows_y[3] + rh - rows_y[0]
    body.append(rect(c5x, y5, c5w, h5, fill=APOIO))
    body.append(text(c5x + 8, y5 + 15, "Polígono de Willis", 8.6, 600, TIT))
    itens = [
        ("Carótidas internas", "terminam nas cerebrais médias e dão as cerebrais anteriores"),
        ("Comunicantes", "uma anterior e duas posteriores fecham o anel"),
        ("Vertebrais", "juntam-se na basilar, que forma as cerebrais posteriores"),
    ]
    yy = y5 + 30
    for t, s in itens:
        body.append(text(c5x + 8, yy, t, 7.6, 600, AZUL))
        sl = wrap(s, 7.2, c5w - 16)
        body += lines_block(c5x + 8, yy + 10, sl, 7.2, 400, TXT, lh=1.3)
        yy += 10 + len(sl) * 7.2 * 1.3 + 9
    # setas
    mid = lambda i: rows_y[i] + rh / 2
    body.append(arrow_h(c1x + c1w + 1, c2x - 1, (yb_top + yb_bot) / 2))
    body.append(arrow_h(c1x + c1w + 1, c2x - 1, mid(2)))
    body.append(arrow_h(c1x + c1w + 1, c2x - 1, mid(3)))
    body.append(arrow_h(c2x + c2w + 1, c3x - 1, mid(0)))
    body.append(arrow_h(c2x + c2w + 1, c3x - 1, mid(1)))
    for i in range(4):
        body.append(arrow_h(c3x + c3w + 1, c4x - 1, mid(i)))
        body.append(arrow_h(c4x + c4w + 1, c5x - 1, mid(i)))
    return svg(H, body)


# ---------------------------------------------------------------- NASCET x ECST
def vaso(ox, oy):
    """Carótida comum -> bulbo -> interna, desenhada da esquerda para a direita; devolve elementos."""
    p = lambda x, y: f"{ox + x:.1f},{oy + y:.1f}"
    top = (f"M{p(0, 14)} L{p(55, 14)} C{p(66, 14)} {p(68, 4)} {p(80, 4)} L{p(140, 4)} "
           f"C{p(154, 4)} {p(156, 20)} {p(170, 20)} L{p(222, 20)}")
    bot = (f"M{p(0, 50)} L{p(55, 50)} C{p(66, 50)} {p(68, 60)} {p(80, 60)} L{p(140, 60)} "
           f"C{p(154, 60)} {p(156, 44)} {p(170, 44)} L{p(222, 44)}")
    fill = (f"M{p(0, 14)} L{p(55, 14)} C{p(66, 14)} {p(68, 4)} {p(80, 4)} L{p(140, 4)} "
            f"C{p(154, 4)} {p(156, 20)} {p(170, 20)} L{p(222, 20)} L{p(222, 44)} L{p(170, 44)} "
            f"C{p(156, 44)} {p(154, 60)} {p(140, 60)} L{p(80, 60)} C{p(68, 60)} {p(66, 50)} {p(55, 50)} "
            f"L{p(0, 50)} Z")
    placa = f"M{p(84, 4)} C{p(98, 4)} {p(100, 48)} {p(112, 48)} C{p(124, 48)} {p(126, 4)} {p(140, 4)} Z"
    return [f'<path d="{fill}" fill="#FFFFFF"/>',
            f'<path d="{placa}" fill="#C3D8F8" stroke="#8AA9DF" stroke-width="1"/>',
            f'<path d="{top}" fill="none" stroke="{TIT}" stroke-width="1.6"/>',
            f'<path d="{bot}" fill="none" stroke="{TIT}" stroke-width="1.6"/>']


def cota(x, y1, y2, color=AZUL):
    t = 3
    return (f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1.4"/>'
            f'<line x1="{x - t:.1f}" y1="{y1:.1f}" x2="{x + t:.1f}" y2="{y1:.1f}" stroke="{color}" stroke-width="1.4"/>'
            f'<line x1="{x - t:.1f}" y1="{y2:.1f}" x2="{x + t:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1.4"/>')


def selo(x, y, letra):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{AZUL}"/>'
            + text(x, y + 2.6, letra, 7.4, 600, "#FFFFFF", "middle"))


def nascet():
    body = []
    pw, gap = 233, 12
    H = 170
    for k in range(2):
        x0 = k * (pw + gap)
        body.append(rect(x0, 0, pw, H, r=10, fill=APOIO))
        if k == 0:
            t1, t2 = "Método norte-americano (NASCET)", "dá o número menor: subestima"
        else:
            t1, t2 = "Método europeu (ECST)", "dá o número maior: superestima"
        body.append(text(x0 + 10, 16, t1, 8.6, 600, TIT))
        body.append(text(x0 + 10, 27, t2, 7.4, 400, CINZA))
        ox, oy = x0 + 6, 42
        body += vaso(ox, oy)
        # luz que sobra (A) no ponto da placa: x=112, y 48..60
        body.append(cota(ox + 108, oy + 47, oy + 60))
        body.append(selo(ox + 108, oy + 74, "A"))
        if k == 0:
            body.append(cota(ox + 200, oy + 20, oy + 44))
            body.append(selo(ox + 200, oy + 56, "B"))
            legs = [("A", "luz que sobra no ponto da placa"),
                    ("B", "carótida interna sadia, acima da placa")]
            frase = "B é estreito, então a estenose parece menor."
        else:
            body.append(cota(ox + 117, oy + 4, oy + 60))
            body.append(selo(ox + 126, oy + 74, "C"))
            legs = [("A", "luz que sobra no ponto da placa"),
                    ("C", "diâmetro total do vaso no ponto da placa")]
            frase = "C é largo, então a estenose parece maior."
        yy = 132
        for letra, s in legs:
            body.append(selo(x0 + 16, yy - 2.6, letra))
            body.append(text(x0 + 27, yy, s, 7.5, 400, TXT))
            yy += 13
        body.append(text(x0 + 10, yy + 3, frase, 7.3, 400, CINZA))
    return svg(H, body)


# ---------------------------------------------------------------- fluxograma do guideline
def decisao():
    body = []
    body += box_text(119, 0, 240, 30, "Placa na carótida medida no Doppler", tsize=8.8)
    cw, gap = 150, 14
    cols = [
        ("Com sintoma e estenose de 70% ou mais",
         ["Operar, em qualquer serviço",
          "A endarterectomia é a melhor indicação; o stent tem evidência de segurança"]),
        ("Sem sintoma, com estenose importante",
         ["Perguntar: é saudável? Deve viver mais de 5 anos? Há outro fator, como placa ulcerada?",
          "Se sim, endarterectomia ou stent; quanto menor a placa, mais o serviço precisa ter menos de 3% de acidente vascular"]),
        ("Sem sintoma e menos de 60%, ou artéria já ocluída",
         ["Tratamento clínico: não mexer no que está quieto",
          "Ultrassom a cada 6 meses; se a placa crescer ou der sintoma, vai para a cirurgia"]),
    ]
    # alturas: calcular para alinhar bases
    y_head = 52
    hh = 40
    ys = []
    hs = [0, 0]
    for _, passos in cols:
        for j, s in enumerate(passos):
            n = len(wrap(s, 7.8, cw - 16, 600 if j == 0 else 400))
            hs[j] = max(hs[j], n * 7.8 * 1.3 + 16)
    for i, (h, passos) in enumerate(cols):
        x = i * (cw + gap)
        cx = x + cw / 2
        body.append(arrow_v(cx, 31, y_head - 1) if i == 1 else "")
        body += box_text(x, y_head, cw, hh, h, tsize=8.2, fill=APOIO)
        y = y_head + hh + 16
        body.append(arrow_v(cx, y_head + hh + 1, y - 1))
        for j, s in enumerate(passos):
            h2 = hs[j]
            if j == 0:
                body += box_text(x, y, cw, h2, s, tsize=7.8)
            else:
                body.append(rect(x, y, cw, h2))
                ln = wrap(s, 7.6, cw - 16)
                th = len(ln) * 7.6 * 1.35
                body += lines_block(cx, y + (h2 - th) / 2 + 7.6, ln, 7.6, 400, TXT, "middle", 1.35)
            if j == 0:
                body.append(arrow_v(cx, y + h2 + 1, y + h2 + 15))
                y += h2 + 16
            else:
                y += h2
    # ramos da caixa de cima para as colunas laterais
    xl, xr = cw / 2, 2 * (cw + gap) + cw / 2
    body.append(f'<path d="M119,15 L{xl:.1f},15 L{xl:.1f},{y_head - 6:.1f}" fill="none" stroke="{SETA}" stroke-width="1.6"/>')
    body.append(f'<polygon points="{xl:.1f},{y_head - 1:.1f} {xl - 3.75:.1f},{y_head - 6:.1f} {xl + 3.75:.1f},{y_head - 6:.1f}" fill="{SETA}"/>')
    body.append(f'<path d="M359,15 L{xr:.1f},15 L{xr:.1f},{y_head - 6:.1f}" fill="none" stroke="{SETA}" stroke-width="1.6"/>')
    body.append(f'<polygon points="{xr:.1f},{y_head - 1:.1f} {xr - 3.75:.1f},{y_head - 6:.1f} {xr + 3.75:.1f},{y_head - 6:.1f}" fill="{SETA}"/>')
    H = y_head + hh + 16 + hs[0] + 16 + hs[1] + 2
    return svg(round(H), [b for b in body if b])


if __name__ == "__main__":
    for nome, fn in [("trilha", trilha), ("anatomia", anatomia), ("nascet-ecst", nascet), ("decisao", decisao)]:
        with open(f"{nome}.svg", "w", encoding="utf-8") as f:
            f.write(fn())
        print("ok", nome)
