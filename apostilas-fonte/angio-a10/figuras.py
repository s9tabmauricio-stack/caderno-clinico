"""Desenha as figuras SVG da apostila angio-a10 (rodar na pasta de trabalho)."""
import math
from pathlib import Path
from PIL import ImageFont

AQUI = Path(__file__).resolve().parent
ARQ = {'r': 'Inter-Regular.ttf', 'm': 'Inter-Medium.ttf', 's': 'Inter-SemiBold.ttf', 'b': 'Inter-Bold.ttf'}
_cache = {}


def larg(t, tam, p='r'):
    if p not in _cache:
        _cache[p] = ImageFont.truetype(str(AQUI / 'fonts' / ARQ[p]), 200)
    return _cache[p].getlength(t) * tam / 200


def quebra(t, tam, maxw, p='r'):
    linhas, atual = [], ''
    for pal in t.split():
        teste = (atual + ' ' + pal).strip()
        if larg(teste, tam, p) <= maxw or not atual:
            atual = teste
        else:
            linhas.append(atual)
            atual = pal
    if atual:
        linhas.append(atual)
    return linhas


FAM = {'r': 'font-family="Inter"', 'm': 'font-family="Inter Medium"',
       's': 'font-family="Inter SemiBold"', 'b': 'font-family="Inter" font-weight="700"'}
AZUL, MARINHO, TEXTO, SETA, BORDA, APOIO = '#0B5BD3', '#16315C', '#1F2933', '#8AA9DF', '#C3D8F8', '#F5F8FF'


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def txt(x, y, t, tam=8, p='r', cor=TEXTO, anc='start'):
    return f'<text x="{x:.1f}" y="{y:.1f}" {FAM[p]} font-size="{tam}" fill="{cor}" text-anchor="{anc}">{esc(t)}</text>'


def bloco(x, y, linhas, tam=8, p='r', cor=TEXTO, anc='start', alt=None):
    alt = alt or tam * 1.32
    return ''.join(txt(x, y + i * alt, l, tam, p, cor, anc) for i, l in enumerate(linhas))


def caixa(x, y, w, h, fundo='#FFFFFF', borda=BORDA, r=7, esp=1, traco=None):
    d = f' stroke-dasharray="{traco}"' if traco else ''
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fundo}" stroke="{borda}" stroke-width="{esp}"{d}/>'


def seta(x1, y1, x2, y2, cor=SETA, esp=1.4, ponta=5):
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - ponta * math.cos(ang), y2 - ponta * math.sin(ang)
    px, py = -math.sin(ang) * ponta * 0.6, math.cos(ang) * ponta * 0.6
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{cor}" stroke-width="{esp}"/>'
            f'<polygon points="{x2:.1f},{y2:.1f} {bx + px:.1f},{by + py:.1f} {bx - px:.1f},{by - py:.1f}" fill="{cor}"/>')


def circulo_num(cx, cy, n, r=7.5, fundo=AZUL):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fundo}"/>'
            + txt(cx, cy + 2.9, str(n), 8, 's', '#FFFFFF', 'middle'))


def svg(nome, h, corpo, w=478):
    (AQUI / nome).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}pt" height="{h}pt" viewBox="0 0 {w} {h}">{corpo}</svg>',
        encoding='utf-8')


# ---------------------------------------------------------------- trilha
def trilha():
    colunas = [
        ('Aneurisma de poplítea', [
            (1, 'Poplítea × aorta', 'trombosa em vez de romper'),
            (2, 'Clínica e exames', 'massa pulsátil, dedo azul, Doppler'),
            (3, 'Quando operar', 'sintoma, mais de 2 cm, trombo mural'),
            (4, 'Como operar', 'ponte com safena ou endoprótese')]),
        ('Hipertensão renovascular', [
            (5, 'Suspeita e causas', 'jovem hipertenso; aterosclerose ou displasia'),
            (6, 'Exames e conduta', 'Doppler; balão com ou sem stent')]),
        ('Isquemia intestinal', [
            (7, 'Isquemia aguda', 'êmbolo ou trombo; o tempo decide'),
            (8, 'Trombose venosa', 'anticoagulante'),
            (9, 'Isquemia crônica', 'come, dói: claudicação intestinal')]),
    ]
    gap, topo = 17, 4
    cw = (478 - 2 - 2 * gap) / 3
    hb, gb = 64, 14
    total = 4 * hb + 3 * gb
    out = []
    for ci, (titulo, passos) in enumerate(colunas):
        x = ci * (cw + gap) + 1
        out.append(caixa(x, topo, cw, 22, APOIO, BORDA, 11))
        out.append(txt(x + cw / 2, topo + 14.8, titulo, 8.8, 's', MARINHO, 'middle'))
        n = len(passos)
        h = (total - (n - 1) * gb) / n
        y = topo + 30
        if ci < 2:
            out.append(seta(x + cw + 2, topo + 11, x + cw + gap - 2, topo + 11))
        for i, (num, nome, desc) in enumerate(passos):
            out.append(caixa(x, y, cw, h))
            linhas = quebra(desc, 8.2, cw - 36)
            bloco_h = 12.5 + len(linhas) * 11
            y0 = y + (h - bloco_h) / 2 + 9
            out.append(circulo_num(x + 15, y0 - 3.2, num, 8.5))
            out.append(txt(x + 30, y0, nome, 9.4, 's', MARINHO))
            out.append(bloco(x + 30, y0 + 13, linhas, 8.2, 'r', '#4F5B70', alt=11))
            if i < n - 1:
                out.append(seta(x + cw / 2, y + h + 2, x + cw / 2, y + h + gb - 2))
            y += h + gb
    svg('trilha.svg', topo + 30 + total + 2, ''.join(out))


# ---------------------------------------------------------------- indicação (poplítea)
def indicacao():
    o = []
    W = 478
    # topo
    tw = 230
    o.append(caixa((W - tw) / 2, 2, tw, 24, APOIO, BORDA, 12))
    o.append(txt(W / 2, 17.5, 'Aneurisma de artéria poplítea', 9, 's', MARINHO, 'middle'))
    # ramos
    lx, lw = 1, 150
    rx, rw = 168, 309
    o.append(seta(W / 2 - 40, 26, lx + lw / 2, 44))
    o.append(seta(W / 2 + 40, 26, rx + rw / 2, 44))
    # esquerda: com sintoma
    o.append(caixa(lx, 44, lw, 22))
    o.append(txt(lx + lw / 2, 58.5, 'Com sintoma', 8.8, 's', MARINHO, 'middle'))
    l1 = quebra('Dor ou claudicação, dedos frios e roxos, oclusão aguda, compressão de nervo ou de veia', 7.8, lw - 16)
    hb = 14 + len(l1) * 10.3
    o.append(caixa(lx, 74, lw, 54))
    o.append(bloco(lx + 8, 74 + (54 - hb) / 2 + 12, l1, 7.8, 'r', '#3A3A3C', alt=10.3))
    o.append(seta(lx + lw / 2, 66, lx + lw / 2, 73))
    # direita: sem sintoma
    o.append(caixa(rx, 44, rw, 22))
    o.append(txt(rx + rw / 2, 58.5, 'Sem sintoma: basta um destes', 8.8, 's', MARINHO, 'middle'))
    crit = [('Mais de 2 cm', 'de diâmetro'),
            ('Trombo mural', 'com qualquer diâmetro (só vale para a poplítea)'),
            ('Saída ruim', 'poucas artérias abaixo do joelho')]
    cw3 = (rw - 2 * 7) / 3
    for i, (t, d) in enumerate(crit):
        cx = rx + i * (cw3 + 7)
        o.append(caixa(cx, 74, cw3, 54))
        o.append(seta(cx + cw3 / 2, 66, cx + cw3 / 2, 73))
        ld = quebra(d, 7.6, cw3 - 14)
        hb = 12 + len(ld) * 10
        y0 = 74 + (54 - hb) / 2 + 9
        o.append(txt(cx + cw3 / 2, y0, t, 8.6, 's', AZUL, 'middle'))
        o.append(bloco(cx + cw3 / 2, y0 + 12.5, ld, 7.6, 'r', '#3A3A3C', 'middle', alt=10))
    # condutas
    yb = 146
    o.append(seta(lx + lw / 2, 128, lx + lw / 2, yb - 1))
    o.append(caixa(lx, yb, lw, 40, '#E8F0FE', AZUL, 9, 1.2))
    o.append(txt(lx + lw / 2, yb + 16, 'Operar', 9.4, 's', AZUL, 'middle'))
    o.append(txt(lx + lw / 2, yb + 29, 'todos os sintomáticos', 7.8, 'r', '#3A3A3C', 'middle'))
    # direita: algum / nenhum
    hw = (rw - 7) / 2
    for i in range(3):
        cx = rx + i * (cw3 + 7) + cw3 / 2
        o.append(f'<line x1="{cx:.1f}" y1="128" x2="{cx:.1f}" y2="136" stroke="{SETA}" stroke-width="1.4"/>')
    o.append(f'<line x1="{rx + cw3 / 2:.1f}" y1="136" x2="{rx + rw - cw3 / 2:.1f}" y2="136" stroke="{SETA}" stroke-width="1.4"/>')
    o.append(seta(rx + hw / 2, 136, rx + hw / 2, yb - 1))
    o.append(seta(rx + hw + 7 + hw / 2, 136, rx + hw + 7 + hw / 2, yb - 1))
    o.append(caixa(rx, yb, hw, 40, '#E8F0FE', AZUL, 9, 1.2))
    o.append(txt(rx + hw / 2, yb + 16, 'Algum presente: operar', 9, 's', AZUL, 'middle'))
    o.append(txt(rx + hw / 2, yb + 29, 'cirurgia aberta ou endoprótese', 7.8, 'r', '#3A3A3C', 'middle'))
    o.append(caixa(rx + hw + 7, yb, hw, 40))
    o.append(txt(rx + hw + 7 + hw / 2, yb + 16, 'Nenhum: acompanhar', 9, 's', MARINHO, 'middle'))
    o.append(txt(rx + hw + 7 + hw / 2, yb + 29, 'tratamento clínico até haver indicação', 7.8, 'r', '#3A3A3C', 'middle'))
    svg('indicacao.svg', yb + 42, ''.join(o))


# ---------------------------------------------------------------- três técnicas (poplítea)
def tubo(x, y1, y2, meia=6, fundo='#DCE7FA', borda=SETA):
    return f'<rect x="{x - meia:.1f}" y="{y1:.1f}" width="{2 * meia:.1f}" height="{y2 - y1:.1f}" fill="{fundo}" stroke="{borda}" stroke-width="1"/>'


def rotulo(x, y, linhas, xl, yl, tam=7.4):
    """texto em x,y (start) com linha-guia até (xl, yl)"""
    return (f'<line x1="{x - 3:.1f}" y1="{y - 2.6:.1f}" x2="{xl:.1f}" y2="{yl:.1f}" stroke="#A9B8D0" stroke-width="0.7"/>'
            + bloco(x, y, linhas, tam, 'r', '#3A3A3C', alt=9.4))


def tecnicas():
    o = []
    pw = 478 / 3
    titulos = ['Ponte por acesso medial', 'Ressecção por acesso posterior', 'Endoprótese por punção']
    sub = ['amarra acima e abaixo e desvia', 'tira o aneurisma e interpõe veia', 'tubo coberto por dentro da artéria']
    topo, base = 42, 198
    meio = (topo + base) / 2
    for i in range(3):
        x0 = i * pw
        o.append(caixa(x0 + 2, 1, pw - 6, base + 10, APOIO, '#DCE6F7', 10))
        o.append(txt(x0 + 10, 16, titulos[i], 8.6, 's', MARINHO))
        o.append(txt(x0 + 10, 28, sub[i], 7.4, 'r', '#4F5B70'))
        ax = x0 + (52 if i == 2 else 40)
        if i == 0:
            o.append(tubo(ax, topo, base))
            o.append(f'<ellipse cx="{ax:.1f}" cy="{meio:.1f}" rx="19" ry="30" fill="#DCE7FA" stroke="{SETA}" stroke-width="1" stroke-dasharray="3 2"/>')
            for yl in (meio - 44, meio + 44):
                o.append(f'<rect x="{ax - 10:.1f}" y="{yl - 2:.1f}" width="20" height="4" rx="1.5" fill="{MARINHO}"/>')
            # ponte (veia) pela lateral
            o.append(f'<path d="M {ax + 6:.1f} {meio - 58:.1f} C {ax + 40:.1f} {meio - 50:.1f}, {ax + 40:.1f} {meio + 50:.1f}, {ax + 6:.1f} {meio + 58:.1f}" fill="none" stroke="{MARINHO}" stroke-width="4.2" stroke-linecap="round"/>')
            o.append(rotulo(x0 + 92, topo + 8, ['femoral distal'], ax + 8, topo + 6))
            o.append(rotulo(x0 + 92, meio - 40, ['ligadura'], ax + 11, meio - 44))
            o.append(rotulo(x0 + 92, meio - 4, ['veia safena', 'magna (ponte)'], ax + 31, meio - 6))
            o.append(rotulo(x0 + 92, meio + 34, ['aneurisma sem', 'fluxo, deixado'], ax + 16, meio + 16))
            o.append(rotulo(x0 + 92, base - 10, ['poplítea abaixo', 'do joelho'], ax + 8, base - 8))
        elif i == 1:
            o.append(tubo(ax, topo, meio - 40))
            o.append(tubo(ax, meio + 40, base))
            o.append(f'<ellipse cx="{ax:.1f}" cy="{meio:.1f}" rx="19" ry="30" fill="none" stroke="#A9B8D0" stroke-width="1" stroke-dasharray="3 2.5"/>')
            o.append(f'<rect x="{ax - 4.5:.1f}" y="{meio - 44:.1f}" width="9" height="88" rx="2" fill="{MARINHO}"/>')
            o.append(rotulo(x0 + 92, topo + 8, ['femoral distal'], ax + 8, topo + 6))
            o.append(rotulo(x0 + 92, meio - 22, ['aneurisma', 'retirado'], ax + 17, meio - 18))
            o.append(rotulo(x0 + 92, meio + 12, ['veia interposta', 'no lugar'], ax + 6, meio + 8))
            o.append(rotulo(x0 + 92, base - 10, ['poplítea abaixo', 'do joelho'], ax + 8, base - 8))
        else:
            o.append(tubo(ax, topo, base))
            o.append(f'<ellipse cx="{ax:.1f}" cy="{meio:.1f}" rx="19" ry="30" fill="#DCE7FA" stroke="{SETA}" stroke-width="1"/>')
            y1, y2 = meio - 62, meio + 62
            o.append(f'<rect x="{ax - 4.2:.1f}" y="{y1:.1f}" width="8.4" height="{y2 - y1:.1f}" fill="#FFFFFF" stroke="{MARINHO}" stroke-width="1.3"/>')
            zz = []
            yy = y1
            k = 0
            while yy < y2:
                zz.append(f'{ax - 4.2 if k % 2 == 0 else ax + 4.2:.1f},{yy:.1f}')
                yy += 5
                k += 1
            o.append(f'<polyline points="{" ".join(zz)}" fill="none" stroke="{AZUL}" stroke-width="0.8"/>')
            # chaves de 2 a 3 cm
            for (ya, yb_) in ((y1, meio - 30), (meio + 30, y2)):
                xk = ax - 14
                o.append(f'<path d="M {xk + 3:.1f} {ya:.1f} L {xk:.1f} {ya:.1f} L {xk:.1f} {yb_:.1f} L {xk + 3:.1f} {yb_:.1f}" fill="none" stroke="{AZUL}" stroke-width="1"/>')
            o.append(bloco(x0 + 10, meio - 49, ['2 a 3', 'cm'], 6.8, 's', AZUL, alt=8.4))
            o.append(bloco(x0 + 10, meio + 43, ['2 a 3', 'cm'], 6.8, 's', AZUL, alt=8.4))
            o.append(rotulo(x0 + 92, topo + 8, ['vem da femoral,', 'por punção', 'na virilha'], ax + 8, topo + 4))
            o.append(rotulo(x0 + 92, meio - 4, ['endoprótese:', 'nitinol coberto', 'de teflon'], ax + 5, meio - 6))
            o.append(rotulo(x0 + 92, base - 26, ['ancorada em', 'artéria sadia', 'acima e abaixo'], ax + 6, y2 - 4))
    svg('tecnicas.svg', base + 13, ''.join(o))


# ---------------------------------------------------------------- artéria renal: aterosclerótica × displasia
def renal():
    o = []
    pw = 231
    titulos = [('Aterosclerótica', 'cerca de 90% · idoso'), ('Displasia fibromuscular', 'cerca de 10% · mulher jovem')]
    for i in range(2):
        x0 = i * (pw + 14) + 1
        o.append(caixa(x0, 1, pw, 150, APOIO, '#DCE6F7', 10))
        o.append(txt(x0 + 10, 17, titulos[i][0], 8.8, 's', MARINHO))
        o.append(txt(x0 + pw - 10, 17, titulos[i][1], 7.4, 'r', '#4F5B70', 'end'))
        # aorta
        ax1, ax2 = x0 + 14, x0 + 42
        o.append(f'<rect x="{ax1}" y="28" width="{ax2 - ax1}" height="112" rx="3" fill="#DCE7FA" stroke="{SETA}" stroke-width="1"/>')
        o.append(txt((ax1 + ax2) / 2, 136, 'aorta', 6.8, 'm', '#4F5B70', 'middle'))
        cy = 70
        # rim
        kx = x0 + pw - 34
        o.append(f'<ellipse cx="{kx:.1f}" cy="{cy:.1f}" rx="20" ry="31" fill="#E8F0FE" stroke="{SETA}" stroke-width="1"/>')
        o.append(txt(kx, cy + 46, 'rim', 6.8, 'm', '#4F5B70', 'middle'))
        xa, xb = ax2, kx - 17
        pts_top, pts_bot = [], []
        n = 120
        for k in range(n + 1):
            x = xa + (xb - xa) * k / n
            t = (x - xa) / (xb - xa)
            if i == 0:
                h = 5.5 - 3.6 * math.exp(-((x - (xa + 7)) / 5.5) ** 2)
            else:
                h = 5.5
                if t > 0.32:
                    h = 5.2 + 2.6 * math.sin((x - (xa + (xb - xa) * 0.32)) / 11.5 * 2 * math.pi - math.pi / 2)
            pts_top.append(f'{x:.1f},{cy - h:.1f}')
            pts_bot.append(f'{x:.1f},{cy + h:.1f}')
        o.append(f'<polygon points="{" ".join(pts_top + pts_bot[::-1])}" fill="#DCE7FA" stroke="{SETA}" stroke-width="1"/>')
        if i == 0:
            # placa vindo da parede da aorta para o óstio
            o.append(f'<path d="M {ax2 - 5:.1f} {cy - 12:.1f} Q {ax2 + 4:.1f} {cy - 8:.1f} {ax2 + 12:.1f} {cy - 2.4:.1f} L {ax2 + 12:.1f} {cy - 1.8:.1f} Q {ax2 + 2:.1f} {cy - 3:.1f} {ax2 - 5:.1f} {cy - 6:.1f} Z" fill="{MARINHO}"/>')
            o.append(f'<path d="M {ax2 - 5:.1f} {cy + 12:.1f} Q {ax2 + 4:.1f} {cy + 8:.1f} {ax2 + 12:.1f} {cy + 2.4:.1f} L {ax2 + 12:.1f} {cy + 1.8:.1f} Q {ax2 + 2:.1f} {cy + 3:.1f} {ax2 - 5:.1f} {cy + 6:.1f} Z" fill="{MARINHO}"/>')
            o.append(f'<line x1="{ax2 + 8:.1f}" y1="{cy + 9:.1f}" x2="{ax2 + 22:.1f}" y2="{cy + 34:.1f}" stroke="#A9B8D0" stroke-width="0.7"/>')
            o.append(bloco(ax2 + 24, cy + 37, ['placa da aorta entra no óstio', 'e para ali: o resto da artéria', 'é normal'], 7.4, 'r', '#3A3A3C', alt=9.4))
        else:
            xm = xa + (xb - xa) * 0.12
            o.append(f'<line x1="{xm:.1f}" y1="{cy + 7:.1f}" x2="{xm + 6:.1f}" y2="{cy + 34:.1f}" stroke="#A9B8D0" stroke-width="0.7"/>')
            o.append(bloco(xm + 8, cy + 37, ['origem poupada'], 7.4, 'r', '#3A3A3C'))
            xc = xa + (xb - xa) * 0.62
            o.append(f'<line x1="{xc:.1f}" y1="{cy - 9:.1f}" x2="{xc - 10:.1f}" y2="{cy - 25:.1f}" stroke="#A9B8D0" stroke-width="0.7"/>')
            o.append(bloco(xc - 70, cy - 28, ['meio e fim em colar de contas'], 7.4, 'r', '#3A3A3C'))
            o.append(bloco(xm + 8, cy + 50, ['doença da camada média'], 7.4, 'r', '#3A3A3C'))
    svg('renal.svg', 153, ''.join(o))


# ---------------------------------------------------------------- colaterais mesentéricas
def arco(x1, x2, ytopo, fundo, cor=SETA, esp=1.5, traco=None):
    d = f' stroke-dasharray="{traco}"' if traco else ''
    return (f'<path d="M {x1:.1f} {ytopo:.1f} C {x1:.1f} {fundo:.1f}, {x2:.1f} {fundo:.1f}, {x2:.1f} {ytopo:.1f}" '
            f'fill="none" stroke="{cor}" stroke-width="{esp}"{d}/>')


def colaterais():
    o = []
    # aorta horizontal (esquema)
    o.append(f'<rect x="10" y="6" width="370" height="13" rx="6" fill="#DCE7FA" stroke="{SETA}" stroke-width="1"/>')
    o.append(txt(18, 15.6, 'Aorta abdominal (esquema)', 7.2, 'm', MARINHO))
    caixas = [(1, 'Tronco celíaco', 'ramos gastroduodenais'),
              (2, 'Mesentérica superior', 'jejuno, íleo e parte do intestino grosso'),
              (3, 'Mesentérica inferior', 'ramos marginais junto ao intestino grosso'),
              (0, 'Ilíaca interna', 'vasos pélvicos')]
    bw, gap, by, bh = 104, 16, 40, 48
    centros = []
    for k, (n, nome, desc) in enumerate(caixas):
        x = 4 + k * (bw + gap)
        cx = x + bw / 2
        centros.append(cx)
        if k < 3:
            o.append(f'<rect x="{cx - 3:.1f}" y="19" width="6" height="{by - 19}" fill="#DCE7FA" stroke="{SETA}" stroke-width="0.8"/>')
        else:
            o.append(f'<path d="M 372 15 C 400 15, {cx:.1f} 18, {cx:.1f} {by:.1f}" fill="none" stroke="{SETA}" stroke-width="1.2" stroke-dasharray="3 2"/>')
        o.append(caixa(x, by, bw, bh, '#FFFFFF', BORDA, 8))
        o.append(txt(cx, by + 15, nome, 8.2, 's', MARINHO, 'middle'))
        ld = quebra(desc, 7, bw - 12)
        o.append(bloco(cx, by + 27, ld, 7, 'r', '#4F5B70', 'middle', alt=9))
    yb = by + bh
    c1, c2, c3, c4 = centros
    # pancreaticoduodenais: celíaco–superior
    o.append(arco(c1 + 6, c2 - 6, yb, yb + 46, SETA, 1.6))
    o.append(bloco((c1 + c2) / 2, yb + 50, ['Arcadas', 'pancreaticoduodenais'], 7.6, 's', AZUL, 'middle', alt=9.6))
    # Riolan (central) e Drummond (marginal, junto ao cólon): superior–inferior
    o.append(arco(c2 + 10, c3 - 10, yb, yb + 46, AZUL, 2))
    o.append(txt((c2 + c3) / 2, yb + 19, 'Arcada de Riolan', 7.6, 's', AZUL, 'middle'))
    o.append(arco(c2 - 2, c3 + 2, yb, yb + 104, SETA, 1.6, '4 2.5'))
    o.append(bloco((c2 + c3) / 2, yb + 95, ['Arcadas marginais', 'de Drummond'], 7.6, 's', AZUL, 'middle', alt=9.6))
    # inferior–ilíaca interna
    o.append(arco(c3 + 12, c4 - 6, yb, yb + 46, SETA, 1.6))
    o.append(bloco((c3 + c4) / 2 + 8, yb + 50, ['Ramos pélvicos'], 7.6, 's', AZUL, 'middle'))
    # notas
    o.append(bloco(8, yb + 84, ['Riolan: liga direto a superior', 'à inferior (a arcada maior).'], 7.2, 'r', '#3A3A3C', alt=9.2))
    o.append(bloco(334, yb + 84, ['Drummond: marginais, bem', 'perto do intestino grosso.'], 7.2, 'r', '#3A3A3C', alt=9.2))
    svg('colaterais.svg', yb + 108, ''.join(o))


if __name__ == '__main__':
    trilha()
    indicacao()
    tecnicas()
    renal()
    colaterais()
    print('figuras prontas')
