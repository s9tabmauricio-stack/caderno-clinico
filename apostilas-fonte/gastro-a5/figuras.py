# Desenha as figuras SVG da apostila gastro-a5 (trilha, fluxogramas, colangiocarcinoma).
# Rodar na pasta da aula: python3 figuras.py
from PIL import ImageFont
from xml.sax.saxutils import escape

F = {
    'r': 'fonts/Inter-Regular.ttf',
    'm': 'fonts/Inter-Medium.ttf',
    's': 'fonts/Inter-SemiBold.ttf',
    'b': 'fonts/Inter-Bold.ttf',
}
FAM = {'r': ("Inter", 400), 'm': ("Inter Medium", 500), 's': ("Inter SemiBold", 600), 'b': ("Inter", 700)}
_cache = {}

AZUL = '#0B5BD3'; MARINHO = '#16315C'; BORDA = '#C3D8F8'; APOIO = '#F5F8FF'
SETA = '#8AA9DF'; TEXTO = '#1F2933'; CINZA = '#6C6C70'; CLARO = '#E8F0FE'
W = 478


def font(k, size):
    key = (k, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(F[k], size)
    return _cache[key]


def width(t, k, size):
    return font(k, size).getlength(t)


def wrap(t, k, size, maxw):
    words, lines, cur = t.split(), [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if width(test, k, size) <= maxw:
            cur = test
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def text(x, y, t, k='r', size=8, color=TEXTO, anchor='start'):
    fam, wt = FAM[k]
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-weight="{wt}" '
            f'font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(t)}</text>')


def rect(x, y, w, h, fill='#FFFFFF', stroke=BORDA, rx=7, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def arrow_down(x, y1, y2, color=SETA):
    # haste + ponta
    return (f'<rect x="{x-0.9:.1f}" y="{y1:.1f}" width="1.8" height="{max(0, y2-y1-5):.1f}" fill="{color}"/>'
            f'<polygon points="{x-4:.1f},{y2-6:.1f} {x+4:.1f},{y2-6:.1f} {x:.1f},{y2:.1f}" fill="{color}"/>')


def arrow_right(x1, x2, y, color=SETA):
    return (f'<rect x="{x1:.1f}" y="{y-0.9:.1f}" width="{max(0, x2-x1-5):.1f}" height="1.8" fill="{color}"/>'
            f'<polygon points="{x2-6:.1f},{y-4:.1f} {x2-6:.1f},{y+4:.1f} {x2:.1f},{y:.1f}" fill="{color}"/>')


def line(x1, y1, x2, y2, color=SETA, w=1.8):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{w}"/>'


def box(x, y, w, title, body='', fill='#FFFFFF', stroke=BORDA, tsize=8.2, bsize=7.6,
        tcolor=MARINHO, pad=7, center=False, sw=1, dash=None, min_h=0):
    """Caixa com título (semibold) e corpo; devolve (svg, altura)."""
    inner = w - 2 * pad
    tl = wrap(title, 's', tsize, inner) if title else []
    bl = wrap(body, 'r', bsize, inner) if body else []
    lh_t, lh_b = tsize * 1.3, bsize * 1.38
    h = pad + len(tl) * lh_t + (2 if tl and bl else 0) + len(bl) * lh_b + pad - 2
    h = max(h, min_h)
    out = [rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, dash=dash)]
    # centraliza o bloco de texto na vertical quando min_h > altura natural
    nat = pad + len(tl) * lh_t + (2 if tl and bl else 0) + len(bl) * lh_b + pad - 2
    cy = y + pad + (h - nat) / 2
    ax = x + w / 2 if center else x + pad
    anc = 'middle' if center else 'start'
    for t in tl:
        cy += lh_t
        out.append(text(ax, cy - lh_t * 0.25, t, 's', tsize, tcolor, anc))
    if tl and bl:
        cy += 2
    for t in bl:
        cy += lh_b
        out.append(text(ax, cy - lh_b * 0.28, t, 'r', bsize, TEXTO, anc))
    return ''.join(out), h


def svg(h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{h:.0f}pt" '
            f'viewBox="0 0 {W} {h:.0f}">' + ''.join(body) + '</svg>')


def badge(cx, cy, n, r=8, fill=AZUL):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}"/>'
            + text(cx, cy + 3, str(n), 's', 8, '#FFFFFF', 'middle'))


# ---------------------------------------------------------------- trilha
def trilha():
    b = []
    etapas = [
        ('O pâncreas normal', 'neoplasia × displasia, anatomia, vasos'),
        ('Adenocarcinoma: quem tem', 'números, letalidade, fatores de risco'),
        ('Suspeita e diagnóstico', 'clínica, ultrassom, tomografia, CA 19-9'),
        ('Ressecabilidade e tratamento', '180°, Whipple, paliação'),
    ]
    ramos = [
        ('Tumor neuroendócrino', 'tamanho, Ki-67, tríade de Whipple'),
        ('Neoplasias císticas', 'intraductal, mucinosa, serosa, Frantz'),
        ('Colangiocarcinoma', 'intra-hepático, peri-hilar, distal'),
    ]
    gap = 14
    w4 = (W - 3 * gap) / 4
    y = 22
    b.append(text(0, 11, 'O CAMINHO PRINCIPAL: ADENOCARCINOMA DE PÂNCREAS', 's', 7, AZUL))
    hs = []
    for i, (t, s) in enumerate(etapas):
        _, h = box(0, 0, w4, t, s, pad=8)
        hs.append(h)
    H1 = max(hs) + 6
    for i, (t, s) in enumerate(etapas):
        x = i * (w4 + gap)
        sv, _ = box(x, y, w4, '', '', min_h=H1)
        b.append(sv)
        b.append(badge(x + 13, y + 13, i + 1))
        for j, ln in enumerate(wrap(t, 's', 8.2, w4 - 30)):
            b.append(text(x + 25, y + 16 + j * 10.5, ln, 's', 8.2, MARINHO))
        nt = len(wrap(t, 's', 8.2, w4 - 30))
        for j, ln in enumerate(wrap(s, 'r', 7.3, w4 - 14)):
            b.append(text(x + 7, y + 20 + nt * 10.5 + j * 9.8, ln, 'r', 7.3, CINZA))
        if i < 3:
            b.append(arrow_right(x + w4 + 2, x + w4 + gap - 1, y + H1 / 2))
    y2 = y + H1 + 30
    b.append(text(0, y2 - 9, 'AO LADO: OS OUTROS TUMORES DA REGIÃO', 's', 7, AZUL))
    w3 = (W - 2 * gap) / 3
    hs = [box(0, 0, w3, t, s, pad=8)[1] for t, s in ramos]
    H2 = max(hs) + 4
    for i, (t, s) in enumerate(ramos):
        x = i * (w3 + gap)
        b.append(rect(x, y2, w3, H2, fill=APOIO, stroke=SETA, dash='3 2'))
        b.append(badge(x + 13, y2 + 13, i + 5, fill=MARINHO))
        b.append(text(x + 25, y2 + 16, t, 's', 8.2, MARINHO))
        for j, ln in enumerate(wrap(s, 'r', 7.3, w3 - 14)):
            b.append(text(x + 7, y2 + 30 + j * 9.8, ln, 'r', 7.3, CINZA))
    return svg(y2 + H2 + 2, b)


# ---------------------------------------------------------------- fluxo do adenocarcinoma
def fluxo_adeno():
    b = []
    y = 0
    full = [
        ('Suspeita clínica', 'Icterícia, perda de peso, dor epigástrica ou lombar. No posto, um ultrassom já levanta a suspeita: vesícula distendida, colédoco dilatado, massa na cabeça do pâncreas.'),
        ('Reunião multidisciplinar e estadiamento', 'Tomografia de abdome com protocolo pancreático (ou ressonância), tomografia de tórax e CA 19-9 de base. Se preciso: colangiorressonância, colangiopancreatografia endoscópica, ecoendoscopia, PET-CT.'),
    ]
    for t, s in full:
        sv, h = box(0, y, W, t, s, pad=8)
        b.append(sv)
        y += h
        b.append(arrow_down(W / 2, y + 1, y + 16))
        y += 17
    # pergunta: metástase?
    sv, h = box(W / 2 - 110, y, 220, 'Tem metástase à distância?', '', fill=CLARO, stroke=SETA, center=True, pad=7)
    b.append(sv)
    qy = y + h / 2
    # sim: à direita? usamos coluna da direita estreita
    y += h
    # ramo "sim" para a direita
    b.append(arrow_right(W / 2 + 111, W - 104, qy))
    b.append(text(W / 2 + 118, qy - 4, 'sim', 'm', 7.3, AZUL))
    sv2, h2 = box(W - 102, qy - 15, 102, 'Irressecável', 'paliação: prótese biliar, quimioterapia paliativa ou só cuidados paliativos', fill='#FFFFFF', stroke=AZUL, center=True, pad=6, tsize=7.8, bsize=7)
    b.append(sv2)
    b.append(arrow_down(W / 2, y + 1, y + 18))
    b.append(text(W / 2 + 5, y + 12, 'não', 'm', 7.3, AZUL))
    y += 19
    sv, h = box(0, y, W - 112, 'Contato do tumor com a artéria mesentérica superior ou o tronco celíaco', '', fill=CLARO, stroke=SETA, center=True, pad=7)
    b.append(sv)
    y += h
    gap = 12
    cw = (W - 2 * gap) / 3
    cols = [
        ('Sem contato arterial', 'Ressecável'),
        ('Contato de até 180°', 'Limítrofe (borderline)'),
        ('Contato acima de 180°', 'Localmente avançado'),
    ]
    # ramificação
    yb = y + 10
    b.append(line(W / 2, y, W / 2, yb))
    b.append(line(cw / 2, yb, W - cw / 2, yb))
    hs = []
    for i, (t, s) in enumerate(cols):
        hs.append(box(0, 0, cw, t, s, center=True)[1])
    H = max(hs)
    yc = yb + 14
    for i, (t, s) in enumerate(cols):
        x = i * (cw + gap)
        b.append(arrow_down(x + cw / 2, yb, yc))
        sv, _ = box(x, yc, cw, s, t, center=True, min_h=H, tsize=8.4, bsize=7.4)
        b.append(sv)
    y = yc + H
    conds = [
        'Sem fator de alto risco: cirurgia direto. Com alto risco (CA 19-9 muito alto, linfonodos aumentados, perda de peso excessiva, dor extrema, imagem duvidosa): biópsia e quimioterapia antes.',
        'Biópsia, quimioterapia neoadjuvante, nova tomografia e cirurgia se ficar possível. Veia (mesentérica superior ou porta) se reconstrói.',
        'Em geral irressecável. Conforme a equipe, ressecção em casos selecionados.',
    ]
    hs = [box(0, 0, cw, '', c, pad=7)[1] for c in conds]
    H = max(hs)
    yc = y + 16
    for i, c in enumerate(conds):
        x = i * (cw + gap)
        b.append(arrow_down(x + cw / 2, y + 1, yc))
        sv, _ = box(x, yc, cw, '', c, min_h=H, stroke=AZUL, pad=7)
        b.append(sv)
    y = yc + H
    # todos operados: adjuvância
    yb = y + 10
    b.append(line(cw / 2, y, cw / 2, yb))
    b.append(line(cw + gap + cw / 2, y, cw + gap + cw / 2, yb))
    b.append(line(cw / 2, yb, cw + gap + cw / 2, yb))
    mid = (cw / 2 + cw + gap + cw / 2) / 2
    b.append(arrow_down(mid, yb, yb + 14))
    sv, h = box(0, yb + 14, 2 * cw + gap, 'Depois da cirurgia', 'quase todos fazem quimioterapia adjuvante (biologia agressiva), salvo o muito idoso ou com muitas doenças.', pad=7, center=True)
    b.append(sv)
    return svg(yb + 14 + h + 1, b)


# ---------------------------------------------------------------- fluxo do cisto intraductal (Fukuoka)
def fluxo_ipmn():
    b = []
    y = 0
    sv, h = box(0, y, W, 'Cisto suspeito de neoplasia mucinosa papilífera intraductal', 'Ressonância com colangiorressonância, tomografia e, se preciso, ecoendoscopia; classificar o ducto acometido.', pad=6)
    b.append(sv); y += h
    b.append(arrow_down(150, y + 1, y + 12)); y += 13
    lw = 300
    rx = lw + 34
    rw = W - rx
    sv, h = box(0, y, lw, 'Tem estigma de alto risco?', 'Icterícia obstrutiva com cisto na cabeça; nódulo mural captante de 5 mm ou mais; ducto principal de 10 mm ou mais; citologia positiva.', fill=CLARO, stroke=SETA, pad=6)
    b.append(sv)
    qy = y + h / 2
    b.append(arrow_right(lw + 1, rx, qy)); b.append(text(lw + 8, qy - 4, 'sim', 'm', 7.3, AZUL))
    sv2, h2 = box(rx, qy - 14, rw, 'Cirurgia', 'ressecção direta', stroke=AZUL, center=True, pad=6)
    b.append(sv2)
    y += h
    b.append(arrow_down(150, y + 1, y + 14)); b.append(text(155, y + 10, 'não', 'm', 7.3, AZUL)); y += 15
    sv, h = box(0, y, lw, 'Tem característica preocupante?', 'Cisto de 3 cm ou mais; nódulo mural menor que 5 mm; parede espessa ou captante; ducto principal de 5 a 9 mm; crescimento rápido; linfonodo aumentado; pancreatite aguda.', fill=CLARO, stroke=SETA, pad=6)
    b.append(sv)
    qy = y + h / 2
    b.append(arrow_right(lw + 1, rx, qy)); b.append(text(lw + 8, qy - 4, 'sim', 'm', 7.3, AZUL))
    sv2, h2 = box(rx, qy - 22, rw, 'Ecoendoscopia com punção', 'citologia e antígeno carcinoembrionário no líquido do cisto', center=True, pad=6)
    b.append(sv2)
    ey = qy - 22 + h2
    y += h
    # coluna da direita: displasia de alto grau?
    b.append(arrow_down(rx + rw / 2, ey + 1, ey + 12))
    sv3, h3 = box(rx, ey + 12, rw, 'Displasia de alto grau ou câncer?', '', fill=CLARO, stroke=SETA, center=True, pad=6, tsize=7.8)
    b.append(sv3)
    dy = ey + 12 + h3
    # base comum das três caixas finais
    ybot = max(y + 14, dy + 14)
    b.append(arrow_down(150, y + 1, ybot)); b.append(text(155, y + 10, 'não', 'm', 7.3, AZUL))
    hw = (rw - 8) / 2
    b.append(arrow_down(rx + hw / 2, dy + 1, ybot)); b.append(text(rx + hw / 2 + 5, dy + 9, 'sim', 'm', 7.3, AZUL))
    b.append(arrow_down(rx + hw + 8 + hw / 2, dy + 1, ybot)); b.append(text(rx + hw + 8 + hw / 2 + 5, dy + 9, 'não', 'm', 7.3, AZUL))
    s2, a2 = box(rx + hw + 8, ybot, hw, 'Seguimento', 'imagem a cada 6 meses a 1 ano', stroke=AZUL, center=True, pad=6, tsize=7.8, bsize=7)
    s1, a1 = box(rx, ybot, hw, 'Cirurgia', '', stroke=AZUL, center=True, pad=6, tsize=7.8, min_h=a2)
    sv, h = box(0, ybot, lw, 'Seguimento com imagem', 'sem estigma e sem característica preocupante', stroke=AZUL, center=True, pad=6, min_h=a2)
    b.extend([s1, s2, sv])
    return svg(ybot + max(h, a2) + 1, b)


# ---------------------------------------------------------------- onde nasce o colangiocarcinoma
def tubo(d, w=9):
    return (f'<path d="{d}" fill="none" stroke="{SETA}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{CLARO}" stroke-width="{w-3.2}" stroke-linecap="round" stroke-linejoin="round"/>')


def tumor(d, w=12):
    return f'<path d="{d}" fill="none" stroke="{MARINHO}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" opacity="0.88"/>'


def colangio_local():
    b = []
    k = 0.72  # desenho reduzido; rótulos em tamanho normal
    H = round(236 * k) + 2
    g = []
    # fígado (contorno simples) e pâncreas/duodeno
    g.append('<path d="M18,40 C30,10 120,4 190,14 C230,20 250,34 240,56 C228,84 170,92 120,96 C80,100 30,96 20,74 C14,62 14,50 18,40 Z" '
             f'fill="{APOIO}" stroke="{BORDA}" stroke-width="1.2"/>')
    g.append('<path d="M120,196 C150,186 200,184 240,192 C255,196 252,212 236,214 C200,218 160,216 126,214 Z" '
             f'fill="#FFFFFF" stroke="{BORDA}" stroke-width="1.2"/>')
    g.append('<path d="M108,170 C96,190 96,214 108,230" fill="none" stroke="#DCE6F7" stroke-width="16" stroke-linecap="round"/>')
    for d in ['M130,82 C110,70 90,60 64,52', 'M88,62 C80,50 70,44 58,40', 'M130,82 C150,66 172,56 200,48',
              'M172,58 C182,46 194,40 210,34', 'M104,70 C100,58 96,50 90,42', 'M156,64 C160,52 166,44 174,38']:
        g.append(tubo(d, 6))
    g.append(tubo('M130,82 C130,110 128,140 120,170 C116,184 112,196 108,206'))
    g.append(tubo('M128,128 C118,132 108,138 98,146', 7))
    g.append('<path d="M98,146 C80,150 64,166 70,180 C76,192 96,186 104,170 C108,160 104,150 98,146 Z" '
             f'fill="#FFFFFF" stroke="{SETA}" stroke-width="1.2"/>')
    g.append(tumor('M84,58 C80,54 76,50 70,46', 6))
    g.append(tumor('M124,78 L136,78', 9))
    g.append(tumor('M114,186 C112,192 111,196 110,200', 9))
    b.append(f'<g transform="scale({k})">' + ''.join(g) + '</g>')
    for x, y, t in [(40, 34, 'fígado'), (196, 208, 'pâncreas'), (70, 226, 'duodeno'), (40, 160, 'vesícula')]:
        b.append(text(x * k, y * k, t, 'm', 7.3, CINZA, 'middle' if t == 'pâncreas' else 'start'))
    zonas = [
        (36, 70, 22, 'Intra-hepático', 'cerca de 10%', 'dentro do fígado, nos ductos periféricos'),
        (76, 110, 72, 'Peri-hilar (tumor de Klatskin)', '65%: o mais comum', 'na confluência dos ductos hepáticos direito e esquerdo'),
        (150, 208, 128, 'Distal', 'cerca de 25%', 'no colédoco, perto do pâncreas e da ampola'),
    ]
    xb = 230
    for y1, y2, my, t, p, s in zonas:
        y1, y2 = y1 * k - 2, y2 * k + 2
        b.append(f'<path d="M{xb},{y1:.1f} h6 v{y2-y1:.1f} h-6" fill="none" stroke="{AZUL}" stroke-width="1.3"/>')
        bm = (y1 + y2) / 2
        cx = xb + 20
        b.append(line(xb + 6, bm, cx - 4, my, AZUL, 1.1))
        b.append(text(cx, my - 6, t, 's', 8.4, MARINHO))
        b.append(text(cx, my + 5, p, 's', 8, AZUL))
        for j, ln in enumerate(wrap(s, 'r', 7.4, W - cx)):
            b.append(text(cx, my + 15.5 + j * 9.6, ln, 'r', 7.4, TEXTO))
    return svg(H, b)


# ---------------------------------------------------------------- Bismuth-Corlette
def bismuth():
    b = []
    tipos = [
        ('Tipo I', 'abaixo da confluência, no ducto hepático comum', 'I'),
        ('Tipo II', 'atinge a confluência', 'II'),
        ('Tipo IIIa', 'confluência + ducto hepático direito', 'IIIa'),
        ('Tipo IIIb', 'confluência + ducto hepático esquerdo', 'IIIb'),
        ('Tipo IV', 'confluência + os dois ductos, ou multicêntrico', 'IV'),
    ]
    pw = W / 5
    for i, (t, s, k) in enumerate(tipos):
        x0 = i * pw
        cx = x0 + pw / 2
        b.append(rect(x0 + 2, 0, pw - 4, 178, fill=APOIO, stroke=BORDA))
        b.append(text(cx, 15, t, 's', 9, MARINHO, 'middle'))
        cy = 72
        rd = f'M{cx},{cy} L{cx-22},{cy-22} L{cx-30},{cy-34}'
        ld = f'M{cx},{cy} L{cx+22},{cy-22} L{cx+30},{cy-34}'
        b.append(tubo(rd)); b.append(tubo(ld))
        b.append(tubo(f'M{cx},{cy} L{cx},{cy+60}'))
        b.append(tubo(f'M{cx},{cy+38} L{cx-14},{cy+46}', 7))
        if k == 'I':
            b.append(tumor(f'M{cx},{cy+14} L{cx},{cy+32}'))
        else:
            b.append(tumor(f'M{cx},{cy+18} L{cx},{cy} L{cx-6},{cy-6} M{cx},{cy} L{cx+6},{cy-6}'))
        if k in ('IIIa', 'IV'):
            b.append(tumor(f'M{cx},{cy} L{cx-22},{cy-22} L{cx-27},{cy-29}'))
        if k in ('IIIb', 'IV'):
            b.append(tumor(f'M{cx},{cy} L{cx+22},{cy-22} L{cx+27},{cy-29}'))
        b.append(text(cx - 36, cy - 44, 'direito', 'r', 6.6, CINZA, 'start'))
        b.append(text(cx + 36, cy - 44, 'esquerdo', 'r', 6.6, CINZA, 'end'))
        for j, ln in enumerate(wrap(s, 'r', 7.4, pw - 14)):
            b.append(text(cx, 148 + j * 9.6, ln, 'r', 7.4, TEXTO, 'middle'))
    # legenda
    b.append(f'<rect x="2" y="188" width="16" height="7" rx="3.5" fill="{MARINHO}" opacity="0.88"/>')
    b.append(text(24, 195, 'tumor', 'r', 7.4, TEXTO))
    b.append(f'<rect x="64" y="188" width="16" height="7" rx="3.5" fill="{CLARO}" stroke="{SETA}" stroke-width="1.6"/>')
    b.append(text(86, 195, 'via biliar livre (vista de frente: o ducto direito fica à esquerda; o ramo curto é o ducto cístico)', 'r', 7.4, TEXTO))
    return svg(200, b)


if __name__ == '__main__':
    for nome, fn in [('trilha', trilha), ('fluxo-adeno', fluxo_adeno), ('fluxo-ipmn', fluxo_ipmn),
                     ('colangio-local', colangio_local), ('bismuth', bismuth)]:
        with open(f'{nome}.svg', 'w', encoding='utf-8') as f:
            f.write(fn())
        print('ok', nome)
