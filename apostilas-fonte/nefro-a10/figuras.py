# Figuras da apostila Nefrologia, Aula 10 (doença renal crônica).
# Gera os SVGs na mesma pasta: python3 figuras.py
import html
import os

from PIL import ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FONTES = {400: "Inter-Regular.ttf", 500: "Inter-Medium.ttf", 600: "Inter-SemiBold.ttf", 700: "Inter-Bold.ttf"}
_cache = {}
W = 478

AZUL_BORDA = "#C3D8F8"
APOIO = "#F5F8FF"
SETA = "#8AA9DF"
TEXTO = "#1F2933"
TITULO = "#16315C"
DESTAQUE = "#0B5BD3"
SEC = "#4F5B70"


def fonte(wt, size):
    k = (wt, size)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(os.path.join(BASE, "fonts", FONTES[wt]), int(size * 20))
    return _cache[k]


def tw(s, size, wt=400):
    return fonte(wt, size).getlength(s) / 20


def wrap(s, size, maxw, wt=400):
    out, cur = [], ""
    for p in s.split():
        t = (cur + " " + p).strip()
        if not cur or tw(t, size, wt) <= maxw:
            cur = t
        else:
            out.append(cur)
            cur = p
    if cur:
        out.append(cur)
    return out


class Svg:
    def __init__(self):
        self.el = []

    def rect(self, x, y, w, h, r=8, fill="#FFFFFF", stroke=AZUL_BORDA, sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" ry="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'
        )

    def circle(self, cx, cy, r, fill):
        self.el.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}"/>')

    def text(self, x, y, t, size=8, wt=400, fill=TEXTO, anchor="start"):
        self.el.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter" font-size="{size}" '
            f'font-weight="{wt}" fill="{fill}" text-anchor="{anchor}">{html.escape(t)}</text>'
        )

    def block(self, x, top, lines, size, wt=400, fill=TEXTO, anchor="start", lh=1.3):
        y = top + size * 0.92
        for ln in lines:
            self.text(x, y, ln, size, wt, fill, anchor)
            y += size * lh
        return top + len(lines) * size * lh

    def line(self, pts, stroke=SETA, sw=1.6):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.el.append(f'<polyline points="{p}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>')

    def head(self, x, y, d, s=6, fill=SETA):
        if d == "r":
            pts = [(x, y), (x - s, y - s * 0.6), (x - s, y + s * 0.6)]
        elif d == "l":
            pts = [(x, y), (x + s, y - s * 0.6), (x + s, y + s * 0.6)]
        elif d == "d":
            pts = [(x, y), (x - s * 0.6, y - s), (x + s * 0.6, y - s)]
        else:
            pts = [(x, y), (x - s * 0.6, y + s), (x + s * 0.6, y + s)]
        p = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
        self.el.append(f'<polygon points="{p}" fill="{fill}"/>')

    def arrow(self, pts, d):
        # pts: caminho; a ponta fica no último ponto, recuada para a linha não passar da ponta
        x, y = pts[-1]
        back = {"r": (-5, 0), "l": (5, 0), "d": (0, -5), "u": (0, 5)}[d]
        self.line(pts[:-1] + [(x + back[0], y + back[1])])
        self.head(x, y, d)

    def pill(self, x, y, t, size=7.2):
        w = tw(t, size, 500) + 12
        self.rect(x, y, w, size + 7, r=(size + 7) / 2, fill="#E8F0FE", stroke=AZUL_BORDA)
        self.text(x + 6, y + size + 2.2, t, size, 500, DESTAQUE)
        return w

    def save(self, nome, h):
        corpo = "\n".join(self.el)
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{h:.0f}pt" '
            f'viewBox="0 0 {W} {h:.0f}">\n{corpo}\n</svg>\n'
        )
        with open(os.path.join(BASE, nome), "w", encoding="utf-8") as f:
            f.write(svg)


# ---------------------------------------------------------------- 1. trilha
def trilha():
    etapas = [
        ("Definição", "lesão por 3 meses ou mais"),
        ("Classificação", "estágios G1 a G5 e A1 a A3"),
        ("Causas", "hipertensão e diabetes à frente"),
        ("Néfrons que sobram", "trabalham a mais e se gastam"),
        ("O que se acumula", "sódio, água, potássio, ácido, fósforo, ureia"),
        ("Síndrome urêmica", "o corpo inteiro sente"),
        ("Diagnóstico", "crônica ou aguda?"),
        ("Tratamento", "conservador, diálise, transplante"),
    ]
    n = len(etapas)
    x0, x1 = 26, W - 26
    xs = [x0 + i * (x1 - x0) / (n - 1) for i in range(n)]
    maxw = 108
    labs = []
    for (t, d) in etapas:
        tl = wrap(t, 8.8, maxw, 600)
        dl = wrap(d, 7.6, maxw)
        h = len(tl) * 8.8 * 1.22 + 2 + len(dl) * 7.6 * 1.3
        w = max([tw(s, 8.8, 600) for s in tl] + [tw(s, 7.6) for s in dl])
        labs.append((tl, dl, h, w))
    hmax = max(l[2] for l in labs)
    ly = 6 + hmax + 14
    total = ly + 14 + hmax + 6
    s = Svg()
    s.line([(xs[0], ly), (xs[-1], ly)], SETA, 2)
    for i, x in enumerate(xs):
        s.circle(x, ly, 9.5, DESTAQUE)
        s.text(x, ly + 3.2, str(i + 1), 8.4, 600, "#FFFFFF", "middle")
        tl, dl, h, w = labs[i]
        cx = min(max(x, w / 2 + 2), W - w / 2 - 2)
        top = ly - 14 - h if i % 2 == 0 else ly + 14
        y = s.block(cx, top, tl, 8.8, 600, TITULO, "middle", 1.22)
        s.block(cx, y + 2, dl, 7.6, 400, SEC, "middle")
    s.save("trilha.svg", total)


# ---------------------------------------------------------------- 2. matriz G x A
def matriz():
    linhas = [("G1", "90 ou mais"), ("G2", "60 a 89"), ("G3a", "45 a 59"), ("G3b", "30 a 44"), ("G4", "15 a 29"), ("G5", "menos de 15")]
    cols = [("A1", "até 30", "normal ou levemente aumentada"), ("A2", "30 a 300", "moderadamente aumentada"), ("A3", "acima de 300", "gravemente aumentada")]
    tons = ["#F3F7FF", "#E1ECFD", "#C9DBF9", "#A9C4EE", "#82A6E0", "#5A84CC", "#3461AE", "#16315C"]
    s = Svg()
    xl, x0 = 0, 122
    gap = 3
    cw = (W - x0 - 2 * gap) / 3
    s.text(xl, 9, "Taxa de filtração", 7.6, 600, SEC)
    s.text(xl, 19, "(mL/min/1,73 m²)", 7.2, 400, SEC)
    s.text(x0 + (W - x0) / 2, 9, "Albumina na urina (mg/g)", 7.6, 600, SEC, "middle")
    hy = 16
    hh = 36
    for j, (a, v, d) in enumerate(cols):
        x = x0 + j * (cw + gap)
        s.rect(x, hy, cw, hh, r=6, fill=APOIO, stroke=AZUL_BORDA)
        s.text(x + 8, hy + 14, a, 9.4, 700, TITULO)
        s.text(x + 8 + tw(a, 9.4, 700) + 5, hy + 14, v, 8.2, 600, DESTAQUE)
        s.block(x + 8, hy + 18, wrap(d, 7.2, cw - 14), 7.2, 400, SEC)
    rh = 25
    y0 = hy + hh + gap
    notas = {(3, 0): "risco moderado de ir para diálise", (3, 2): "risco muito elevado"}
    for i, (g, v) in enumerate(linhas):
        y = y0 + i * (rh + gap)
        s.rect(xl, y, x0 - gap - xl, rh, r=6, fill=APOIO, stroke=AZUL_BORDA)
        s.text(xl + 8, y + rh / 2 + 3.3, g, 9.4, 700, TITULO)
        s.text(xl + 40, y + rh / 2 + 3, v, 8.2, 400, TEXTO)
        for j in range(3):
            x = x0 + j * (cw + gap)
            t = tons[min(i + j + (1 if i == 5 else 0), 7)]
            s.rect(x, y, cw, rh, r=6, fill=t, stroke=t)
            if (i, j) in notas:
                cor = "#FFFFFF" if tons.index(t) >= 5 else TITULO
                ls = wrap(notas[(i, j)], 7.6, cw - 12, 600)
                top = y + (rh - len(ls) * 7.6 * 1.2) / 2
                s.block(x + cw / 2, top, ls, 7.6, 600, cor, "middle", 1.2)
    yb = y0 + 6 * (rh + gap) + 8
    s.text(x0, yb + 8, "menor risco", 7.4, 500, SEC)
    s.text(W, yb + 8, "maior risco", 7.4, 500, SEC, "end")
    bx0 = x0 + tw("menor risco", 7.4, 500) + 8
    bx1 = W - tw("maior risco", 7.4, 500) - 8
    sw = (bx1 - bx0) / len(tons)
    for k, t in enumerate(tons):
        s.rect(bx0 + k * sw, yb + 1, sw - 1, 9, r=2, fill=t, stroke=t)
    s.save("matriz.svg", yb + 14)


# ---------------------------------------------------------------- 3. hiperfiltração
def nefrons():
    caixas = [
        ("Perda de néfrons", "Diabetes: glomeruloesclerose. Hipertensão: esclerose das arteríolas."),
        ("Os que sobram trabalham a mais", "Eliminam mais sódio, potássio e água: a homeostase se mantém."),
        ("Hipertrofia e hiperfiltração", "O excesso de trabalho lesa os próprios néfrons que sobram."),
        ("Esclerose de todos os glomérulos", "Anúria: o paciente vive de diálise."),
    ]
    s = Svg()
    gap = 20
    bw = (W - 3 * gap) / 4
    pad = 8
    conteudos = []
    for t, d in caixas:
        tl = wrap(t, 8.6, bw - 2 * pad, 600)
        dl = wrap(d, 7.8, bw - 2 * pad)
        conteudos.append((tl, dl, len(tl) * 8.6 * 1.22 + 4 + len(dl) * 7.8 * 1.3))
    bh = max(c[2] for c in conteudos) + 2 * pad + 2
    top = 34
    for i, (tl, dl, _) in enumerate(conteudos):
        x = i * (bw + gap)
        final = i == 3
        s.rect(x, top, bw, bh, r=9, fill=APOIO if final else "#FFFFFF", stroke=TITULO if final else AZUL_BORDA, sw=1.3 if final else 1)
        y = s.block(x + pad, top + pad, tl, 8.6, 600, TITULO, lh=1.22)
        s.block(x + pad, y + 4, dl, 7.8)
        if i < 3:
            s.arrow([(x + bw + 3, top + bh / 2), (x + bw + gap - 3, top + bh / 2)], "r")
    # volta do ciclo, por cima
    xa = bw / 2
    xc = 2 * (bw + gap) + bw / 2
    yv = 12
    s.arrow([(xc, top - 2), (xc, yv), (xa, yv), (xa, top - 3)], "d")
    rot = "o ciclo se repete: a cada volta, menos néfrons"
    lw = tw(rot, 7.6, 500) + 12
    s.rect((xa + xc) / 2 - lw / 2, yv - 7, lw, 14, r=7, fill="#FFFFFF", stroke="#FFFFFF")
    s.text((xa + xc) / 2, yv + 2.7, rot, 7.6, 500, SEC, "middle")
    s.save("nefrons.svg", top + bh + 2)


# ---------------------------------------------------------------- 4. trade-off
def tradeoff():
    nos = [
        ("1  Fósforo retido", "O rim deixa de eliminar o fósforo, entre as fases 3b e 4.", ["Dieta pobre em fósforo", "Sevelâmer"]),
        ("2  Fósforo prende o cálcio", "Os dois andam juntos no sangue; o cálcio livre cai: hipocalcemia.", ["Carbonato de cálcio"]),
        ("3  Paratireoide em alerta", "O cálcio baixo faz a paratireoide produzir mais paratormônio.", ["Cinacalcete", "Calcitriol"]),
        ("4  Cálcio sai do osso", "O cálcio do sangue normaliza, mas o fósforo continua alto e puxa mais cálcio.", []),
    ]
    s = Svg()
    gapx, gapy = 64, 30
    nw = (W - gapx) / 2
    pad = 9
    info = []
    for t, d, pills in nos:
        tl = wrap(t, 9, nw - 2 * pad, 600)
        dl = wrap(d, 7.9, nw - 2 * pad)
        h = len(tl) * 9 * 1.22 + 4 + len(dl) * 7.9 * 1.3 + (20 if pills else 0)
        info.append((tl, dl, pills, h))
    nh = max(i[3] for i in info) + 2 * pad
    pos = [(0, 0), (nw + gapx, 0), (nw + gapx, nh + gapy), (0, nh + gapy)]
    for k, ((tl, dl, pills, _), (x, y)) in enumerate(zip(info, pos)):
        s.rect(x, y, nw, nh, r=10)
        yy = s.block(x + pad, y + pad, tl, 9, 600, TITULO, lh=1.22)
        yy = s.block(x + pad, yy + 4, dl, 7.9)
        px = x + pad
        for p in pills:
            px += s.pill(px, y + nh - pad - 14.2, p) + 5
    # setas do ciclo
    s.arrow([(nw + 4, nh / 2), (nw + gapx - 4, nh / 2)], "r")
    s.arrow([(nw + gapx + nw / 2, nh + 3), (nw + gapx + nw / 2, nh + gapy - 3)], "d")
    s.arrow([(nw + gapx - 4, nh + gapy + nh / 2), (nw + 4, nh + gapy + nh / 2)], "l")
    s.arrow([(nw / 2, nh + gapy - 3), (nw / 2, nh + 3)], "u")
    cx, cy = W / 2, nh + gapy / 2
    s.block(cx, cy - 9, ["ciclo", "vicioso"], 8, 600, DESTAQUE, "middle", 1.2)
    s.save("tradeoff.svg", 2 * nh + gapy + 2)


# ---------------------------------------------------------------- 5. quando dialisar
def dialise():
    s = Svg()
    pad = 9
    tw_ = 300
    tx = (W - tw_) / 2
    tl = ["Doente renal crônico chegando ao fim do tratamento conservador"]
    tl = wrap(tl[0], 8.8, tw_ - 2 * pad, 600)
    th = len(tl) * 8.8 * 1.22 + 2 * pad
    s.rect(tx, 0, tw_, th, r=10, fill=APOIO, stroke=TITULO, sw=1.2)
    s.block(W / 2, pad, tl, 8.8, 600, TITULO, "middle", 1.22)
    gap = 26
    cw = (W - gap) / 2
    colx = [0, cw + gap]
    ys = th + 26
    # setas de saída
    for x in colx:
        s.arrow([(W / 2, th + 2), (W / 2, th + 10), (x + cw / 2, th + 10), (x + cw / 2, ys - 3)], "d")
    s.text(colx[0] + cw / 2 - 6, th + 21, "há perigo agora?", 7.4, 500, SEC, "end")
    s.text(colx[1] + cw / 2 + 6, th + 21, "sem urgência", 7.4, 500, SEC, "start")
    c1 = [
        ("Diálise de urgência quando há", ["hipervolemia ou edema que não responde ao diurético", "hiperpotassemia", "risco de vida: pericardite ou encefalopatia urêmica"]),
        ("Diálise eletiva", ["clearance de creatinina entre 9 e 14 mL/min", "no diabético, mais cedo: entre 15 e 20 mL/min"]),
    ]
    c2 = [
        ("Dialisar já", ["Foi o caso do paciente do início: anasarca, potássio de 6,8 mEq/L e coma por uremia."]),
        ("Programar com tempo", ["“Vamos programar a sua hemodiálise”: fazer a fístula e dar tempo de ela amadurecer.", "Reunião com médico, enfermeira, assistente social, nutricionista (papel primordial), família e paciente: hemodiálise ou diálise peritoneal?"]),
    ]

    def medir(t, itens, bullet):
        tl = wrap(t, 8.8, cw - 2 * pad, 600)
        bl = []
        for it in itens:
            ls = wrap(it, 7.9, cw - 2 * pad - (9 if bullet else 0))
            bl.append(ls)
        h = len(tl) * 8.8 * 1.22 + 4 + sum(len(b) * 7.9 * 1.3 + 2 for b in bl)
        return tl, bl, h

    def desenhar(x, y, h, tl, bl, bullet, fill="#FFFFFF"):
        s.rect(x, y, cw, h, r=10, fill=fill)
        yy = s.block(x + pad, y + pad, tl, 8.8, 600, TITULO, lh=1.22) + 4
        for b in bl:
            if bullet:
                s.circle(x + pad + 2.5, yy + 4.6, 1.8, DESTAQUE)
                yy = s.block(x + pad + 9, yy, b, 7.9) + 2
            else:
                yy = s.block(x + pad, yy, b, 7.9) + 2

    a1 = medir(c1[0][0], c1[0][1], True)
    b1 = medir(c1[1][0], c1[1][1], True)
    h1 = max(a1[2], b1[2]) + 2 * pad
    a2 = medir(c2[0][0], c2[0][1], False)
    b2 = medir(c2[1][0], c2[1][1], True)
    h2 = max(a2[2], b2[2]) + 2 * pad
    desenhar(colx[0], ys, h1, a1[0], a1[1], True)
    desenhar(colx[1], ys, h1, b1[0], b1[1], True)
    y2 = ys + h1 + 20
    for x in colx:
        s.arrow([(x + cw / 2, ys + h1 + 3), (x + cw / 2, y2 - 3)], "d")
    desenhar(colx[0], y2, h2, a2[0], a2[1], False, APOIO)
    desenhar(colx[1], y2, h2, b2[0], b2[1], True, APOIO)
    s.save("dialise.svg", y2 + h2 + 2)


# ---------------------------------------------------------------- 6. mapa mental
def mapa_mental():
    ramos = [
        ("Classificar", ["3 meses de lesão", "estágios G1 a G5", "albuminúria A1 a A3"]),
        ("Saber as causas", ["hipertensão 32%", "diabetes 31%", "glomerulonefrite 9%", "policística 4%", "outras 24%"]),
        ("Como o corpo se defende", ["néfrons que sobram trabalham a mais", "hiperfiltração", "trade-off do fósforo"]),
        ("Tratamento conservador", ["menos sal, exercício", "proteína 0,6 a 0,8 g/kg", "potássio: duas águas", "anemia, fósforo, cálcio"]),
    ]
    s = Svg()
    gap = 8
    cw = (W - 3 * gap) / 4
    pad = 8
    info = []
    for t, itens in ramos:
        tl = wrap(t, 8.6, cw - 2 * pad, 600)
        bl = [wrap(i, 7.5, cw - 2 * pad - 8) for i in itens]
        h = len(tl) * 8.6 * 1.22 + 5 + sum(len(b) * 7.5 * 1.3 + 2 for b in bl)
        info.append((tl, bl, h))
    ch = max(i[2] for i in info) + 2 * pad + 17
    pill_h = 22
    ytop = pill_h + 18
    cx = W / 2
    rot = "Doença renal crônica"
    lw = tw(rot, 9.4, 600) + 26
    ybar = pill_h + 8
    s.line([(cx, pill_h), (cx, ybar)], SETA, 1.6)
    xs = [k * (cw + gap) + cw / 2 for k in range(4)]
    s.line([(xs[0], ybar), (xs[-1], ybar)], SETA, 1.6)
    for x in xs:
        s.arrow([(x, ybar), (x, ytop - 2)], "d")
    s.rect(cx - lw / 2, 0, lw, pill_h, r=pill_h / 2, fill=TITULO, stroke=TITULO)
    s.text(cx, pill_h / 2 + 3.3, rot, 9.4, 600, "#FFFFFF", "middle")
    for k, (tl, bl, _) in enumerate(info):
        x = k * (cw + gap)
        s.rect(x, ytop, cw, ch, r=10)
        s.circle(x + pad + 6.5, ytop + pad + 6.5, 6.5, DESTAQUE)
        s.text(x + pad + 6.5, ytop + pad + 9.2, str(k + 1), 7.4, 600, "#FFFFFF", "middle")
        yy = s.block(x + pad, ytop + pad + 17, tl, 8.6, 600, TITULO, lh=1.22) + 4
        for b in bl:
            s.circle(x + pad + 2.3, yy + 4.4, 1.7, DESTAQUE)
            yy = s.block(x + pad + 8, yy, b, 7.5) + 2
    s.save("mapa-mental.svg", ytop + ch + 1)


if __name__ == "__main__":
    trilha()
    matriz()
    nefrons()
    tradeoff()
    dialise()
    mapa_mental()
    print("ok")
