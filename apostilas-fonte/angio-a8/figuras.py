# Figuras da apostila angio-a8 (Angiologia · Aula 1 · Arterites e vasculites)
# Uso: python3 figuras.py  (na pasta da aula; precisa de fonts/ e, para os recortes, de slides.pdf)
import os
from PIL import ImageFont, Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
F = {w: os.path.join(AQUI, "fonts", f"Inter-{n}.ttf") for w, n in
     [(400, "Regular"), (500, "Medium"), (600, "SemiBold"), (700, "Bold")]}
_cache = {}


def font(w, s):
    k = (w, s)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(F[w], int(s * 10))
    return _cache[k]


def tw(t, w, s):
    return font(w, s).getlength(t) / 10.0


def wrap(t, w, s, maxw):
    out, cur = [], ""
    for p in t.split():
        c = (cur + " " + p).strip()
        if tw(c, w, s) <= maxw or not cur:
            cur = c
        else:
            out.append(cur)
            cur = p
    if cur:
        out.append(cur)
    return out


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


AZ, AZC, APOIO, SETA, TX, TIT, CINZA = "#0B5BD3", "#C3D8F8", "#F5F8FF", "#8AA9DF", "#1F2933", "#16315C", "#4F5B70"


def text(x, y, t, w=400, s=8, fill=TX, anchor="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter" font-weight="{w}" font-size="{s}" '
            f'fill="{fill}" text-anchor="{anchor}">{esc(t)}</text>')


def lines(x, y, ls, w=400, s=8, fill=TX, anchor="start", lh=None):
    lh = lh or s * 1.32
    return "".join(text(x, y + i * lh, l, w, s, fill, anchor) for i, l in enumerate(ls))


def rect(x, y, w, h, fill="#FFFFFF", stroke=AZC, rx=7, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def head(x, y, direc, size=5.5, fill=SETA):
    # ponta de seta com a ponta em (x, y)
    s = size
    if direc == "down":
        pts = [(x, y), (x - s, y - s * 1.3), (x + s, y - s * 1.3)]
    elif direc == "up":
        pts = [(x, y), (x - s, y + s * 1.3), (x + s, y + s * 1.3)]
    elif direc == "right":
        pts = [(x, y), (x - s * 1.3, y - s), (x - s * 1.3, y + s)]
    else:
        pts = [(x, y), (x + s * 1.3, y - s), (x + s * 1.3, y + s)]
    return '<polygon points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) + f'" fill="{fill}"/>'


def line(x1, y1, x2, y2, stroke=SETA, sw=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def svg(w, h, body, nome):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}pt" height="{h:.0f}pt" '
         f'viewBox="0 0 {w} {h:.0f}">' + body + "</svg>")
    with open(os.path.join(AQUI, nome), "w", encoding="utf-8") as f:
        f.write(s)


W = 478

# ---------------------------------------------------------------- trilha
def trilha():
    passos = [
        ("Vaso inflamado", "o que é vasculite e como dividir"),
        ("Suspeitar", "ferida sem história clássica"),
        ("Grande calibre", "temporal e Takayasu"),
        ("Médio calibre", "Buerger, poliarterite e Kawasaki"),
        ("Pequeno calibre", "Behçet e Wegener"),
        ("Além das clássicas", "eritema nodoso e leucocitoclástica"),
        ("Tratar", "o corticoide e as duas exceções"),
    ]
    n = len(passos)
    col = W / n
    cy, r = 16, 11
    b = []
    b.append(line(col / 2, cy, W - col / 2, cy, stroke=AZC, sw=3))
    maxy = 0
    for i, (t, d) in enumerate(passos):
        cx = col * i + col / 2
        ramo = i == 5
        if ramo:
            b.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="{r}" fill="#FFFFFF" stroke="{AZ}" stroke-width="1.6" stroke-dasharray="3 2"/>')
            b.append(text(cx, cy + 3.6, str(i + 1), 600, 10, AZ, "middle"))
        else:
            b.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="{r}" fill="{AZ}"/>')
            b.append(text(cx, cy + 3.6, str(i + 1), 600, 10, "#FFFFFF", "middle"))
        tl = wrap(t, 600, 8, col - 10)
        dl = wrap(d, 400, 7, col - 10)
        y = cy + r + 12
        b.append(lines(cx, y, tl, 600, 8, TIT, "middle", 10))
        y += len(tl) * 10 + 1
        b.append(lines(cx, y, dl, 400, 7, CINZA, "middle", 8.8))
        y += len(dl) * 8.8
        maxy = max(maxy, y)
    svg(W, maxy + 2, "".join(b), "trilha.svg")


# ---------------------------------------------------------------- calibre
def calibre():
    cols = [
        ("Grande calibre", "aorta e seus grandes ramos", 15,
         [("Arterite de Takayasu", "mulher jovem"),
          ("Arterite temporal", "de células gigantes ou de Horton; mulher idosa")]),
        ("Médio calibre", "artérias musculares: femorais, tibiais, coronárias, das vísceras", 10,
         [("Tromboangeíte obliterante", "doença de Buerger; homem jovem que fuma"),
          ("Poliarterite nodosa", "hepatite B; aneurismas nas vísceras"),
          ("Doença de Kawasaki", "criança; coronárias")]),
        ("Pequeno calibre", "arteríolas, capilares e vênulas: as mais difíceis de diagnosticar", 5.5,
         [("Granulomatose de Wegener", "c-ANCA; pulmão e mucosas"),
          ("Síndrome de Churg-Strauss", ""),
          ("Poliangeíte microscópica", ""),
          ("Vasculite por imunoglobulina A", ""),
          ("Crioglobulinemia", ""),
          ("Vasculite leucocitoclástica", ""),
          ("Doença de Behçet", "mucosas e olho")]),
    ]
    gap = 9
    cw = (W - 2 * gap) / 3
    pad = 8
    b = []
    # medir alturas
    blocos = []
    for (t, sub, raio, doencas) in cols:
        subl = wrap(sub, 400, 7.2, cw - 2 * pad)
        top = 10 + 34 + len(subl) * 9.2 + 6
        bx = []
        for nome, nota in doencas:
            nl = wrap(nome, 500, 8.2, cw - 2 * pad - 12)
            tl = wrap(nota, 400, 7, cw - 2 * pad - 12) if nota else []
            h = 7 + len(nl) * 10 + len(tl) * 8.8 + 5
            bx.append((nl, tl, h))
        blocos.append((subl, top, bx))
    H = max(top + sum(h + 5 for _, _, h in bx) for (_, top, bx) in blocos) + 4
    for i, ((t, sub, raio, doencas), (subl, top, bx)) in enumerate(zip(cols, blocos)):
        x = i * (cw + gap)
        b.append(rect(x, 0, cw, H, fill=APOIO, stroke="#DCE6F7", rx=10))
        # corte do vaso: anel proporcional ao calibre
        cx, cy = x + pad + 15, 24
        b.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="{raio}" fill="{AZC}" stroke="{AZ}" stroke-width="1"/>')
        b.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="{raio * 0.55:.1f}" fill="#FFFFFF"/>')
        b.append(text(x + pad + 36, 22, t, 600, 10, TIT))
        b.append(lines(x + pad, 10 + 34 + 2, subl, 400, 7.2, CINZA, lh=9.2))
        y = top
        for (nl, tl, h) in bx:
            b.append(rect(x + pad, y, cw - 2 * pad, h, rx=6))
            b.append(lines(x + pad + 6, y + 12.5, nl, 500, 8.2, TX, lh=10))
            if tl:
                b.append(lines(x + pad + 6, y + 12.5 + len(nl) * 10, tl, 400, 7, CINZA, lh=8.8))
            y += h + 5
    svg(W, H, "".join(b), "calibre.svg")


# ---------------------------------------------------------------- doença arterial: fases × tromboangeíte
def daop():
    b = []
    b.append(text(0, 9, "Doença arterial obstrutiva periférica: o caminho de sempre, em meses ou anos", 600, 8.2, TIT))
    bw, g, y0, bh = 132, 41, 18, 42
    fases = [("1", "Dor para caminhar", "passa quando para"),
             ("2", "Dor em repouso", "à noite, na cama"),
             ("3", "Lesão trófica", "ferida, necrose")]
    for i, (n, t, d) in enumerate(fases):
        x = i * (bw + g)
        dest = i == 2
        b.append(rect(x, y0, bw, bh, stroke=AZ if dest else AZC, sw=1.6 if dest else 1, rx=8))
        b.append(f'<circle cx="{x + 15:.1f}" cy="{y0 + bh / 2}" r="8" fill="{AZ}"/>')
        b.append(text(x + 15, y0 + bh / 2 + 3.2, n, 600, 8.5, "#FFFFFF", "middle"))
        b.append(text(x + 29, y0 + 18, t, 600, 8.6, TX))
        b.append(text(x + 29, y0 + 30, d, 400, 7.4, CINZA))
        if i < 2:
            xa = x + bw + 5
            b.append(line(xa, y0 + bh / 2, xa + g - 14, y0 + bh / 2))
            b.append(head(xa + g - 8, y0 + bh / 2, "right"))
    # tromboangeíte
    ty, th = 92, 40
    b.append(rect(0, ty, 190, th, fill=APOIO, stroke=AZC, rx=8))
    b.append(text(10, ty + 16, "Tromboangeíte obliterante", 600, 8.6, TIT))
    b.append(text(10, ty + 29, "homem até 50 anos, que fuma muito", 400, 7.4, CINZA))
    x3 = 2 * (bw + g) + bw / 2
    yl = ty + th / 2
    b.append(line(190, yl, x3, yl))
    b.append(line(x3, yl + 1, x3, y0 + bh + 9))
    b.append(head(x3, y0 + bh + 3, "up"))
    b.append(text(202, yl - 6, "pula as fases: chega com ferida e dor dia e noite", 500, 7.6, AZ))
    b.append(text(x3 - 7, y0 + bh + 22, "Rutherford 5 e 6", 600, 7.4, AZ, "end"))
    svg(W, ty + th + 2, "".join(b), "daop.svg")


# ---------------------------------------------------------------- sinal de Martorell
def martorell():
    b = []
    pw, g, H = 229, 20, 236
    jl = 108  # linha articular
    for i in range(2):
        x0 = i * (pw + g)
        b.append(rect(x0, 0, pw, H, fill=APOIO, stroke="#DCE6F7", rx=10))
        b.append(text(x0 + 12, 18, "Normal" if i == 0 else "Sinal de Martorell", 600, 9.5, TIT))
        b.append(line(x0 + 10, jl, x0 + pw - 10, jl, stroke="#9AA5B5", sw=1, dash="4 3"))
        if i == 0:
            b.append(text(x0 + pw - 12, jl - 5, "linha articular do joelho", 400, 7, CINZA, "end"))
    # normal
    cx = 70
    b.append(f'<path d="M{cx},30 L{cx},{jl + 18}" stroke="{AZ}" stroke-width="9" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M{cx},{jl + 18} C{cx - 4},{jl + 40} {cx - 18},{jl + 70} {cx - 26},{H - 14}" stroke="{AZ}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M{cx},{jl + 18} L{cx + 6},{jl + 62}" stroke="{AZ}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M{cx + 6},{jl + 62} C{cx + 8},{jl + 85} {cx + 4},{jl + 105} {cx + 2},{H - 14}" stroke="{AZ}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M{cx + 6},{jl + 62} C{cx + 14},{jl + 85} {cx + 24},{jl + 105} {cx + 30},{H - 14}" stroke="{AZ}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    # rótulos normal
    def rot(x1, y1, x2, y2, ls):
        o = line(x1, y1, x2, y2, stroke="#7D8DA6", sw=0.8)
        o += f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="1.8" fill="#7D8DA6"/>'
        o += lines(x2 + 3, y2 + 3, ls, 400, 7.4, TX, lh=9)
        return o
    b.append(rot(cx + 5, 62, 100, 62, ["artéria poplítea"]))
    b.append(line(cx - 9, jl + 52, 42, jl + 52, stroke="#7D8DA6", sw=0.8))
    b.append(f'<circle cx="{cx - 9}" cy="{jl + 52}" r="1.8" fill="#7D8DA6"/>')
    b.append(lines(10, jl + 49, ["tibial", "anterior"], 400, 7.4, TX, lh=9))
    b.append(rot(cx + 6, jl + 50, 100, jl + 46, ["tronco tibiofibular"]))
    b.append(rot(cx + 22, jl + 100, 112, jl + 104, ["tibial posterior", "e fibular"]))
    # martorell
    mx = pw + g + 70
    b.append(f'<path d="M{mx},30 L{mx},{jl - 4}" stroke="{AZ}" stroke-width="9" fill="none" stroke-linecap="round"/>')
    raizes = [
        (-10, 0.9, -34, 70, -30, 112), (-6, 0.9, -20, 46, -48, 98), (-3, 1.1, -8, 60, -14, 120),
        (0, 1.2, 4, 40, -2, 104), (3, 1.0, 14, 62, 10, 122), (6, 1.0, 22, 40, 34, 96),
        (9, 0.9, 36, 64, 42, 118), (-12, 0.8, -40, 30, -54, 60), (12, 0.8, 40, 26, 52, 58),
    ]
    for (dx, sw, c1x, c1y, ex, ey) in raizes:
        sx, sy = mx + dx * 0.4, jl - 8
        b.append(f'<path d="M{sx:.1f},{sy} C{mx + c1x * 0.5:.1f},{jl + c1y * 0.4:.1f} {mx + c1x:.1f},{jl + c1y * 0.7:.1f} {mx + ex:.1f},{jl + ey:.1f}" '
                 f'stroke="{AZ}" stroke-width="{sw}" fill="none" stroke-linecap="round"/>')
    b.append(rot(mx + 5, 62, mx + 30, 62, ["artéria poplítea"]))
    b.append(rot(mx + 3, jl - 6, mx + 62, jl + 22, ["termina na linha articular"]))
    b.append(rot(mx + 36, jl + 70, mx + 72, jl + 70, ["colaterais finas, em", "raiz de árvore, que não", "salvam a perna"]))
    svg(W, H, "".join(b), "martorell.svg")


# ---------------------------------------------------------------- tratamento
def tratamento():
    b = []
    gap = 10
    w1 = 206
    w2 = (W - w1 - 2 * gap) / 2
    xs = [0, w1 + gap, w1 + w2 + 2 * gap]
    ws = [w1, w2, w2]
    # caixa do topo
    tw_ = 210
    tx = (W - tw_) / 2
    b.append(rect(tx, 0, tw_, 26, fill=APOIO, stroke=AZC, rx=8))
    b.append(text(W / 2, 16.5, "Vasculite com o diagnóstico feito", 600, 8.8, TIT, "middle"))
    # ramos
    ybar = 38
    b.append(line(W / 2, 26, W / 2, ybar))
    cxs = [xs[i] + ws[i] / 2 for i in range(3)]
    b.append(line(cxs[0], ybar, cxs[2], ybar))
    for c in cxs:
        b.append(line(c, ybar, c, 52))
        b.append(head(c, 58, "down"))
    rotulos = ["A regra", "Exceção", "Exceção"]
    quem = [
        "Arterite temporal, arterite de Takayasu, poliarterite nodosa, doença de Behçet, granulomatose de Wegener e vasculite leucocitoclástica",
        "Doença de Kawasaki",
        "Tromboangeíte obliterante (doença de Buerger)",
    ]
    conduta = [("Corticoide, o carro-chefe", "nos casos graves, outros imunossupressores"),
               ("Ácido acetilsalicílico", "o tratamento de base"),
               ("Parar de fumar", "mais analgésico; às vezes vasodilatador e ponte")]
    y2 = 60
    ql = [wrap(q, 400, 7.8, ws[i] - 16) for i, q in enumerate(quem)]
    h2 = 20 + max(len(q) for q in ql) * 10 + 4
    cl = [wrap(c[1], 400, 7.4, ws[i] - 16) for i, c in enumerate(conduta)]
    tl = [wrap(c[0], 600, 9, ws[i] - 16) for i, c in enumerate(conduta)]
    h3 = 12 + max(len(t) for t in tl) * 11 + max(len(c) for c in cl) * 9.4 + 6
    y3 = y2 + h2 + 18
    for i in range(3):
        x, w = xs[i], ws[i]
        b.append(rect(x, y2, w, h2, rx=8))
        b.append(text(x + 8, y2 + 12, rotulos[i].upper(), 600, 6.8, AZ))
        b.append(lines(x + 8, y2 + 24, ql[i], 400, 7.8, TX, lh=10))
        c = x + w / 2
        b.append(line(c, y2 + h2, c, y3 - 6))
        b.append(head(c, y3, "down"))
        b.append(rect(x, y3, w, h3, fill=AZ, stroke=AZ, rx=8))
        b.append(lines(x + 8, y3 + 15, tl[i], 600, 9, "#FFFFFF", lh=11))
        b.append(lines(x + 8, y3 + 15 + len(tl[i]) * 11, cl[i], 400, 7.4, "#E3ECFB", lh=9.4))
    svg(W, y3 + h3 + 1, "".join(b), "tratamento.svg")


# ---------------------------------------------------------------- recortes dos slides com rótulos
def recortes():
    slides = os.path.join(AQUI, "slides.pdf")
    if not os.path.exists(slides):
        print("sem slides.pdf: recortes não refeitos")
        return
    import pypdfium2 as pdfium
    pdf = pdfium.PdfDocument(slides)

    def pagina(n):
        return pdf[n - 1].render(scale=3).to_pil().convert("RGB")

    def rotular(im, larg_pt, itens):
        # itens: (texto, (x, y) da caixa, [(x, y) alvos])
        esc_ = im.width / larg_pt  # px por pt
        s = round(8.0 * esc_)
        f = ImageFont.truetype(F[600], s)
        d = ImageDraw.Draw(im)
        lw = max(2, round(1.1 * esc_))
        for (t, (bx, by), alvos) in itens:
            w = f.getlength(t)
            px, py = round(0.6 * s), round(0.38 * s)
            caixa = (bx, by, bx + w + 2 * px, by + s + 2 * py)
            cxm, cym = (caixa[0] + caixa[2]) / 2, (caixa[1] + caixa[3]) / 2
            for (ax, ay) in alvos:
                ox = caixa[2] if ax > caixa[2] else (caixa[0] if ax < caixa[0] else cxm)
                oy = caixa[3] if ay > caixa[3] else (caixa[1] if ay < caixa[1] else cym)
                d.line([(ox, oy), (ax, ay)], fill="#FFFFFF", width=lw + 4)
                d.line([(ox, oy), (ax, ay)], fill=AZ, width=lw)
                rr = round(0.45 * s)
                d.ellipse([ax - rr, ay - rr, ax + rr, ay + rr], fill="#FFFFFF", outline=AZ, width=lw)
            d.rounded_rectangle(caixa, radius=round(0.55 * s), fill="#FFFFFF", outline=AZ, width=lw)
            d.text((bx + px, by + py - round(0.12 * s)), t, font=f, fill=TIT)
        return im

    def salvar(im, nome):
        im.save(os.path.join(AQUI, nome), quality=88)

    # slide 13: artéria temporal (foto C)
    im = pagina(13).crop((285, 170, 1020, 1170))
    rotular(im, 175, [("artéria temporal", (40, 600), [(338, 405)])])
    salvar(im, "img-temporal.jpg")
    # slide 20: angiografia do arco da aorta
    im = pagina(20).crop((78, 276, 1730, 1188))
    rotular(im, 380, [("ramos do arco estreitados (setas)", (30, 30), [(700, 300), (900, 230)]),
                      ("arco da aorta", (30, 820), [(640, 760)])])
    salvar(im, "img-takayasu.jpg")
    # slide 31: Kawasaki
    im = pagina(31).crop((316, 190, 1598, 962))
    rotular(im, 230, [("olhos vermelhos, sem secreção", (400, 150), [(300, 75), (880, 70)]),
                      ("bochecha vermelha", (20, 600), [(170, 440)]),
                      ("lábios vermelhos", (850, 640), [(790, 700)])])
    salvar(im, "img-kawasaki.jpg")
    # slide 35: pernas com vasculite leucocitoclástica
    im = pagina(35).crop((63, 107, 1715, 1208))
    rotular(im, 380, [("manchas arroxeadas e pequenas úlceras", (520, 960), [(560, 520), (1120, 700)])])
    salvar(im, "img-leuco.jpg")
    # slide 46: pulmão com necrose
    im = pagina(46).crop((352, 312, 1684, 1285))
    rotular(im, 230, [("nódulo com cavidade", (20, 20), [(348, 268)]),
                      ("áreas de necrose", (20, 880), [(640, 640), (1000, 430)])])
    salvar(im, "img-pulmao.jpg")


if __name__ == "__main__":
    trilha()
    calibre()
    daop()
    martorell()
    tratamento()
    recortes()
    print("figuras prontas")
