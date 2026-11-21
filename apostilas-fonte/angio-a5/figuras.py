#!/usr/bin/env python3
"""Desenha as figuras SVG da apostila angio-a5 (Trauma vascular).

Rodar na pasta da aula: python3 figuras.py
Gera trilha.svg, guerras.svg, lesoes.svg, anastomoses.svg e fluxograma.svg.
Largura 478 pt (largura útil do cartão .figure); texto medido com a Inter da pasta fonts/.
"""
import math
import os
from xml.sax.saxutils import escape

from PIL import ImageFont

D = os.path.dirname(os.path.abspath(__file__))
ARQ = {'r': 'Inter-Regular.ttf', 'm': 'Inter-Medium.ttf', 's': 'Inter-SemiBold.ttf', 'b': 'Inter-Bold.ttf'}
PESO = {'r': 400, 'm': 500, 's': 600, 'b': 700}
_cache = {}

AZUL_BORDA = '#C3D8F8'
APOIO = '#F5F8FF'
SETA = '#8AA9DF'
TEXTO = '#1F2933'
TITULO = '#16315C'
DESTAQUE = '#0B5BD3'
CINZA = '#6C6C70'
VERDE_F, VERDE_B, VERDE_T = '#E7F7EC', '#BFE5CB', '#1E7A34'
LUMEN = '#DCE8FB'
PAREDE = '#16315C'
W = 478


def fonte(p, t):
    k = (p, t)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(os.path.join(D, 'fonts', ARQ[p]), t)
    return _cache[k]


def larg(txt, p, t):
    return fonte(p, round(t * 10)).getlength(txt) / 10


def quebra(txt, p, t, maxw):
    linhas, atual = [], ''
    for pal in txt.split():
        teste = (atual + ' ' + pal).strip()
        if larg(teste, p, t) <= maxw or not atual:
            atual = teste
        else:
            linhas.append(atual)
            atual = pal
    if atual:
        linhas.append(atual)
    return linhas


def T(x, y, txt, t, p='r', cor=TEXTO, ancora='start'):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter" font-weight="{PESO[p]}" '
            f'font-size="{t}" fill="{cor}" text-anchor="{ancora}">{escape(txt)}</text>')


def bloco(x, y, linhas, t, p='r', cor=TEXTO, ancora='start', lh=None):
    lh = lh or t * 1.32
    return ''.join(T(x, y + i * lh, l, t, p, cor, ancora) for i, l in enumerate(linhas))


def caixa(x, y, w, h, fill='#FFFFFF', stroke=AZUL_BORDA, r=7, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def seta(x1, y1, x2, y2, cor=SETA, sw=1.4, cab=5):
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - cab * math.cos(ang), y2 - cab * math.sin(ang)
    px, py = -math.sin(ang) * cab * 0.6, math.cos(ang) * cab * 0.6
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{cor}" stroke-width="{sw}"/>'
            f'<polygon points="{x2:.1f},{y2:.1f} {bx + px:.1f},{by + py:.1f} {bx - px:.1f},{by - py:.1f}" fill="{cor}"/>')


def linha(pts, cor=SETA, sw=1.4):
    p = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return f'<polyline points="{p}" fill="none" stroke="{cor}" stroke-width="{sw}"/>'


def salvar(nome, h, corpo):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{h:.0f}pt" '
           f'viewBox="0 0 {W} {h:.0f}"><g transform="translate(0.7 0.7) scale({(W - 1.4) / W:.5f})">{corpo}</g></svg>')
    with open(os.path.join(D, nome), 'w', encoding='utf-8') as f:
        f.write(svg)
    print(nome, W, 'x', round(h))


def selo(cx, cy, txt, cheio=True):
    if cheio:
        c = f'<circle cx="{cx}" cy="{cy}" r="8.5" fill="{DESTAQUE}"/>'
        return c + T(cx, cy + 2.6, txt, 7.2, 'b', '#FFFFFF', 'middle')
    c = f'<circle cx="{cx}" cy="{cy}" r="8.5" fill="#FFFFFF" stroke="{DESTAQUE}" stroke-width="1" stroke-dasharray="2 1.5"/>'
    return c + T(cx, cy + 2.6, txt, 7.2, 'b', DESTAQUE, 'middle')


# ------------------------------------------------------------------ trilha
def trilha():
    etapas = [
        ('01', 'Conter o sangramento', 'compressão, torniquete, ligadura, anastomose'),
        ('02', 'O que as guerras ensinaram', 'tempo é vida, tempo é membro'),
        ('03', 'Mecanismo do trauma', 'tiro, faca, pancada, procedimento médico'),
        ('04', 'Lesões e síndromes', 'isquêmica, hemorrágica, tumoral'),
        ('05', 'Sinais maiores e menores', 'operar já ou investigar'),
        ('06', 'Exames', 'arteriografia é o padrão-ouro'),
        ('07', 'Conduta', 'exame positivo leva à cirurgia'),
        ('08', 'Endovascular', 'molas e stent recoberto'),
        ('09', 'Cirurgia aberta', 'controle proximal e distal'),
        ('10', 'Veias e compartimento', 'fasciotomia é ato médico'),
    ]
    gap, n = 13, 5
    bw = (W - (n - 1) * gap) / n
    inner = bw - 16
    tit = [quebra(e[1], 's', 8.8, inner) for e in etapas]
    sub = [quebra(e[2], 'r', 7.6, inner) for e in etapas]
    nt = max(len(t) for t in tit)
    ns = max(len(s) for s in sub)
    bh = 30 + nt * 11.2 + 3 + ns * 9.8 + 6
    y1, vao = 4, 30
    y2 = y1 + bh + vao
    out = []
    for i, (num, _, _) in enumerate(etapas):
        lin, col = divmod(i, n)
        x = col * (bw + gap)
        y = y1 if lin == 0 else y2
        ramo = num == '02'
        out.append(caixa(x, y, bw, bh, fill=APOIO if ramo else '#FFFFFF', dash='3 2' if ramo else None))
        out.append(selo(x + 15, y + 15, num, cheio=not ramo))
        if ramo:
            out.append(T(x + bw - 8, y + 17.5, 'ramo', 6.8, 'm', DESTAQUE, 'end'))
        out.append(bloco(x + 8, y + 37, tit[i], 8.8, 's', TITULO, lh=11.2))
        out.append(bloco(x + 8, y + 37 + nt * 11.2 + 3, sub[i], 7.6, 'r', CINZA, lh=9.8))
        if col < n - 1:
            out.append(seta(x + bw + 1.5, y + bh / 2, x + bw + gap - 1.5, y + bh / 2))
    # da etapa 05 (fim da linha 1) para a 06 (começo da linha 2)
    xa = 4 * (bw + gap) + bw / 2
    ym = y1 + bh + vao / 2
    out.append(linha([(xa, y1 + bh + 1.5), (xa, ym), (bw / 2, ym)]))
    out.append(seta(bw / 2, ym, bw / 2, y2 - 1.5))
    salvar('trilha.svg', y2 + bh + 4, ''.join(out))


# ------------------------------------------------------------------ guerras
def guerras():
    eras = [
        ('Primeira Guerra', 'Mundial', ['Ligadura era o tratamento de escolha.',
                                        'A infecção desfazia a sutura do vaso.',
                                        'Muitos amputados, de muleta.']),
        ('Segunda Guerra', 'Mundial', ['2.471 lesões arteriais, 81 reparos e 78 suturas laterais.',
                                       'Amputação: mais de um terço; depois de ligadura, quase metade.',
                                       'Até o tratamento: 10 horas.']),
        ('Guerra', 'da Coreia', ['Anestesia melhor, resgate aéreo e postos avançados.',
                                 'Até o tratamento: 1 a 2 horas.',
                                 'Amputação: de 35% para 13%.']),
        ('Guerra', 'do Vietnã', ['Transporte aéreo em 95% dos feridos.',
                                 'Ainda muitas lesões vasculares, mas a amputação continuou baixa.']),
        ('Hoje:', 'trauma civil', ['Arma de fogo, trânsito e violência; atinge jovens.',
                                   'Mais iatrogenia (cateterismos).',
                                   'Primeiros artigos de tratamento endovascular: 1997.']),
    ]
    n, gap = len(eras), 9
    cw = (W - (n - 1) * gap) / n
    inner = cw - 19
    corpo = []
    for _, _, itens in eras:
        ls = []
        for it in itens:
            ls.append(quebra(it, 'r', 7.9, inner))
        corpo.append(ls)
    alt = [sum(len(l) for l in ls) * 10.3 + (len(ls) - 1) * 5 for ls in corpo]
    bh = max(alt) + 20
    eixo = 40
    out = [f'<line x1="2" y1="{eixo}" x2="{W - 2}" y2="{eixo}" stroke="{SETA}" stroke-width="1.6"/>']
    out.append(seta(W - 14, eixo, W - 1, eixo, cab=6))
    yb = eixo + 16
    for i, (a, b, _) in enumerate(eras):
        x = i * (cw + gap)
        cx = x + cw / 2
        out.append(T(cx, 13, a, 9, 's', TITULO, 'middle'))
        out.append(T(cx, 25.5, b, 9, 's', TITULO, 'middle'))
        out.append(f'<circle cx="{cx:.1f}" cy="{eixo}" r="4.5" fill="{DESTAQUE}" stroke="#FFFFFF" stroke-width="1.5"/>')
        out.append(f'<line x1="{cx:.1f}" y1="{eixo + 5}" x2="{cx:.1f}" y2="{yb}" stroke="{SETA}" stroke-width="1"/>')
        out.append(caixa(x, yb, cw, bh))
        yy = yb + 15
        for ls in corpo[i]:
            out.append(f'<circle cx="{x + 8.5:.1f}" cy="{yy - 2.6:.1f}" r="1.6" fill="{DESTAQUE}"/>')
            out.append(bloco(x + 13, yy, ls, 7.9, 'r', TEXTO, lh=10.3))
            yy += len(ls) * 10.3 + 5
    ya = yb + bh + 10
    ah = 30
    out.append(caixa(0, ya, W, ah, fill=APOIO, stroke=AZUL_BORDA))
    out.append(T(12, ya + 18.8, 'O que mudou o resultado:', 8.8, 's', TITULO))
    x0 = 12 + larg('O que mudou o resultado:', 's', 8.8) + 6
    out.append(T(x0, ya + 18.8, 'chegar rápido ao cirurgião e reconstruir o vaso em vez de amarrar.', 8.8, 'r', TEXTO))
    salvar('guerras.svg', ya + ah + 2, ''.join(out))


# ------------------------------------------------------------------ desenho de vasos
def tubo(x1, x2, cy, r=11, parede=PAREDE, lumen=LUMEN, sw=3):
    return (f'<rect x="{x1:.1f}" y="{cy - r:.1f}" width="{x2 - x1:.1f}" height="{2 * r:.1f}" fill="{lumen}"/>'
            f'<line x1="{x1:.1f}" y1="{cy - r:.1f}" x2="{x2:.1f}" y2="{cy - r:.1f}" stroke="{parede}" stroke-width="{sw}"/>'
            f'<line x1="{x1:.1f}" y1="{cy + r:.1f}" x2="{x2:.1f}" y2="{cy + r:.1f}" stroke="{parede}" stroke-width="{sw}"/>')


def fluxo(x1, x2, cy, cor=SETA):
    return seta(x1, cy, x2, cy, cor=cor, sw=1.2, cab=4.5)


def painel_texto(x, y, w, titulo, legenda):
    out = [T(x + w / 2, y, titulo, 9.2, 's', TITULO, 'middle')]
    ls = quebra(legenda, 'r', 8.0, w - 10)
    out.append(bloco(x + w / 2, y + 13, ls, 8.0, 'r', TEXTO, 'middle', lh=10.4))
    return ''.join(out), len(ls)


def lesoes():
    n, gap = 3, 10
    pw = (W - (n - 1) * gap) / n
    dh = 64
    legendas = [
        ('Secção parcial', 'Rasga só parte da parede: o vaso não consegue se retrair e se fechar, e sangra por mais tempo.'),
        ('Secção total (transecção)', 'Corta o vaso inteiro: as pontas se retraem e se contraem, e sangra por menos tempo.'),
        ('Lesão da íntima e dissecção', 'A camada de dentro descola, o sangue entra entre as camadas e o vaso entope: isquemia.'),
        ('Espasmo', 'O vaso se contrai sem romper: o pulso pode ficar mais fraco sem que haja rotura.'),
        ('Pseudoaneurisma', 'Hematoma que continua recebendo sangue pelo furo: em volta só há gordura e coágulo.'),
        ('Fístula arteriovenosa', 'O furo liga artéria e veia: frêmito e sopro, e a veia passa a pulsar.'),
    ]
    nl = max(len(quebra(l, 'r', 8.0, pw - 10)) for _, l in legendas)
    ph = dh + 14 + 13 + nl * 10.4 + 8
    out = []
    for i, (tit, leg) in enumerate(legendas):
        lin, col = divmod(i, n)
        x = col * (pw + gap)
        y = lin * (ph + gap)
        out.append(caixa(x, y, pw, ph, fill='#FFFFFF'))
        out.append(f'<rect x="{x + 6:.1f}" y="{y + 6:.1f}" width="{pw - 12:.1f}" height="{dh - 4:.1f}" rx="5" fill="{APOIO}"/>')
        cy = y + 6 + (dh - 4) / 2
        a, b = x + 16, x + pw - 16
        m = (a + b) / 2
        if i == 0:  # secção parcial
            out.append(tubo(a, b, cy + 6))
            out.append(f'<rect x="{m - 8:.1f}" y="{cy + 6 - 13:.1f}" width="16" height="5" fill="{APOIO}"/>')
            for dx, dy, r in [(-8, -14, 2.6), (0, -19, 3.2), (8, -14, 2.6), (-3, -26, 2.2), (5, -25, 2)]:
                out.append(f'<circle cx="{m + dx:.1f}" cy="{cy + 6 + dy:.1f}" r="{r}" fill="{SETA}"/>')
            out.append(fluxo(a + 6, m - 14, cy + 6))
        elif i == 1:  # transecção
            r = 11
            ga = 11
            out.append(f'<path d="M{a:.1f},{cy - r:.1f} L{m - ga - 6:.1f},{cy - r:.1f} Q{m - ga:.1f},{cy - r:.1f} {m - ga:.1f},{cy - 5:.1f} '
                       f'L{m - ga:.1f},{cy + 5:.1f} Q{m - ga:.1f},{cy + r:.1f} {m - ga - 6:.1f},{cy + r:.1f} L{a:.1f},{cy + r:.1f} Z" fill="{LUMEN}"/>')
            out.append(f'<path d="M{a:.1f},{cy - r:.1f} L{m - ga - 6:.1f},{cy - r:.1f} Q{m - ga:.1f},{cy - r:.1f} {m - ga:.1f},{cy - 4:.1f}" fill="none" stroke="{PAREDE}" stroke-width="3"/>')
            out.append(f'<path d="M{a:.1f},{cy + r:.1f} L{m - ga - 6:.1f},{cy + r:.1f} Q{m - ga:.1f},{cy + r:.1f} {m - ga:.1f},{cy + 4:.1f}" fill="none" stroke="{PAREDE}" stroke-width="3"/>')
            out.append(f'<path d="M{b:.1f},{cy - r:.1f} L{m + ga + 6:.1f},{cy - r:.1f} Q{m + ga:.1f},{cy - r:.1f} {m + ga:.1f},{cy - 5:.1f} '
                       f'L{m + ga:.1f},{cy + 5:.1f} Q{m + ga:.1f},{cy + r:.1f} {m + ga + 6:.1f},{cy + r:.1f} L{b:.1f},{cy + r:.1f} Z" fill="{LUMEN}"/>')
            out.append(f'<path d="M{b:.1f},{cy - r:.1f} L{m + ga + 6:.1f},{cy - r:.1f} Q{m + ga:.1f},{cy - r:.1f} {m + ga:.1f},{cy - 4:.1f}" fill="none" stroke="{PAREDE}" stroke-width="3"/>')
            out.append(f'<path d="M{b:.1f},{cy + r:.1f} L{m + ga + 6:.1f},{cy + r:.1f} Q{m + ga:.1f},{cy + r:.1f} {m + ga:.1f},{cy + 4:.1f}" fill="none" stroke="{PAREDE}" stroke-width="3"/>')
            out.append(seta(m - ga - 10, cy - 20, m - ga - 26, cy - 20, cor=SETA, sw=1.1, cab=4))
            out.append(seta(m + ga + 10, cy - 20, m + ga + 26, cy - 20, cor=SETA, sw=1.1, cab=4))
            out.append(fluxo(a + 6, m - ga - 12, cy))
        elif i == 2:  # íntima / dissecção
            out.append(tubo(a, b, cy))
            out.append(f'<path d="M{m - 22:.1f},{cy + 8:.1f} Q{m - 6:.1f},{cy + 8:.1f} {m + 4:.1f},{cy - 4:.1f}" fill="none" stroke="{PAREDE}" stroke-width="1.8"/>')
            out.append(f'<path d="M{m - 14:.1f},{cy + 9.5:.1f} Q{m + 2:.1f},{cy + 8:.1f} {m + 6:.1f},{cy - 2:.1f} L{m + 32:.1f},{cy - 2:.1f} '
                       f'Q{m + 40:.1f},{cy + 4:.1f} {m + 34:.1f},{cy + 9.5:.1f} Z" fill="#8AA9DF"/>')
            out.append(fluxo(a + 6, m - 26, cy - 2))
        elif i == 3:  # espasmo
            r1, r2 = 11, 5
            top = f'M{a:.1f},{cy - r1:.1f} L{m - 26:.1f},{cy - r1:.1f} C{m - 12:.1f},{cy - r1:.1f} {m - 12:.1f},{cy - r2:.1f} {m:.1f},{cy - r2:.1f} C{m + 12:.1f},{cy - r2:.1f} {m + 12:.1f},{cy - r1:.1f} {m + 26:.1f},{cy - r1:.1f} L{b:.1f},{cy - r1:.1f}'
            bot = f'M{a:.1f},{cy + r1:.1f} L{m - 26:.1f},{cy + r1:.1f} C{m - 12:.1f},{cy + r1:.1f} {m - 12:.1f},{cy + r2:.1f} {m:.1f},{cy + r2:.1f} C{m + 12:.1f},{cy + r2:.1f} {m + 12:.1f},{cy + r1:.1f} {m + 26:.1f},{cy + r1:.1f} L{b:.1f},{cy + r1:.1f}'
            fill = (f'M{a:.1f},{cy - r1:.1f} L{m - 26:.1f},{cy - r1:.1f} C{m - 12:.1f},{cy - r1:.1f} {m - 12:.1f},{cy - r2:.1f} {m:.1f},{cy - r2:.1f} '
                    f'C{m + 12:.1f},{cy - r2:.1f} {m + 12:.1f},{cy - r1:.1f} {m + 26:.1f},{cy - r1:.1f} L{b:.1f},{cy - r1:.1f} L{b:.1f},{cy + r1:.1f} '
                    f'L{m + 26:.1f},{cy + r1:.1f} C{m + 12:.1f},{cy + r1:.1f} {m + 12:.1f},{cy + r2:.1f} {m:.1f},{cy + r2:.1f} '
                    f'C{m - 12:.1f},{cy + r2:.1f} {m - 12:.1f},{cy + r1:.1f} {m - 26:.1f},{cy + r1:.1f} L{a:.1f},{cy + r1:.1f} Z')
            out.append(f'<path d="{fill}" fill="{LUMEN}"/>')
            out.append(f'<path d="{top}" fill="none" stroke="{PAREDE}" stroke-width="3"/>')
            out.append(f'<path d="{bot}" fill="none" stroke="{PAREDE}" stroke-width="3"/>')
            out.append(fluxo(a + 6, m - 30, cy))
        elif i == 4:  # pseudoaneurisma
            cyv = cy + 17
            out.append(f'<circle cx="{m:.1f}" cy="{cyv - 24:.1f}" r="14" fill="#C3D8F8" stroke="{SETA}" stroke-width="1.2" stroke-dasharray="3 2"/>')
            out.append(f'<circle cx="{m + 3:.1f}" cy="{cyv - 27:.1f}" r="6.5" fill="{SETA}"/>')
            out.append(tubo(a, b, cyv))
            out.append(f'<rect x="{m - 4:.1f}" y="{cyv - 13:.1f}" width="8" height="5" fill="#C3D8F8"/>')
            out.append(fluxo(a + 6, m - 12, cyv))
        else:  # fístula arteriovenosa
            ya, yv = cy - 13, cy + 15
            out.append(f'<rect x="{m - 4:.1f}" y="{ya:.1f}" width="8" height="{yv - ya:.1f}" fill="{LUMEN}"/>')
            out.append(f'<line x1="{m - 4:.1f}" y1="{ya + 8:.1f}" x2="{m - 4:.1f}" y2="{yv - 8:.1f}" stroke="{PAREDE}" stroke-width="1.6"/>')
            out.append(f'<line x1="{m + 4:.1f}" y1="{ya + 8:.1f}" x2="{m + 4:.1f}" y2="{yv - 8:.1f}" stroke="{PAREDE}" stroke-width="1.6"/>')
            out.append(tubo(a, b, ya, r=8, sw=2.6))
            out.append(tubo(a, b, yv, r=8, parede='#5E7FB8', sw=2.2))
            out.append(f'<rect x="{m - 2.6:.1f}" y="{ya + 6:.1f}" width="5.2" height="{yv - ya - 12:.1f}" fill="{LUMEN}"/>')
            out.append(T(a + 3, ya + 2.6, 'artéria', 6.6, 'm', TITULO))
            out.append(T(a + 3, yv + 2.6, 'veia', 6.6, 'm', TITULO))
            out.append(fluxo(m - 22, m - 8, ya))
            out.append(seta(m, ya + 4, m, yv - 3, cor=SETA, sw=1.1, cab=4))
            out.append(fluxo(m + 8, m + 26, yv))
        tx, _ = painel_texto(x, y + dh + 14, pw, tit, leg)
        out.append(tx)
    salvar('lesoes.svg', 2 * ph + gap + 1, ''.join(out))


# ------------------------------------------------------------------ anastomoses
def anastomoses():
    n, gap = 3, 10
    pw = (W - (n - 1) * gap) / n
    dh = 70
    legendas = [
        ('Término-terminal', 'Boca a boca: a ponta de um vaso costurada na ponta do outro.'),
        ('Término-lateral', 'A ponta de um vaso costurada num corte na lateral do outro: o fluxo original continua.'),
        ('Triangulação de Carrel', 'Três pontos a 120 graus, puxados, abrem a boca em triângulo: a parede de trás não colaba.'),
    ]
    nl = max(len(quebra(l, 'r', 8.0, pw - 10)) for _, l in legendas)
    ph = dh + 14 + 13 + nl * 10.4 + 8
    out = []
    for i, (tit, leg) in enumerate(legendas):
        x = i * (pw + gap)
        y = 0
        out.append(caixa(x, y, pw, ph, fill='#FFFFFF'))
        out.append(f'<rect x="{x + 6:.1f}" y="{y + 6:.1f}" width="{pw - 12:.1f}" height="{dh - 4:.1f}" rx="5" fill="{APOIO}"/>')
        cy = y + 6 + (dh - 4) / 2
        a, b = x + 16, x + pw - 16
        m = (a + b) / 2
        if i == 0:
            out.append(tubo(a, m, cy))
            out.append(tubo(m, b, cy, parede='#3D63A8'))
            for k in range(-2, 3):
                yy = cy + k * 4.6
                out.append(f'<line x1="{m - 3:.1f}" y1="{yy - 1.5:.1f}" x2="{m + 3:.1f}" y2="{yy + 1.5:.1f}" stroke="{DESTAQUE}" stroke-width="1"/>')
            out.append(f'<line x1="{m:.1f}" y1="{cy - 13:.1f}" x2="{m:.1f}" y2="{cy + 13:.1f}" stroke="{DESTAQUE}" stroke-width="1" stroke-dasharray="2 1.5"/>')
            out.append(fluxo(a + 6, a + 28, cy))
            out.append(fluxo(b - 28, b - 6, cy))
        elif i == 1:
            cyv = cy + 14
            out.append(tubo(a, b, cyv))
            # enxerto oblíquo chegando à lateral de cima
            ang = math.radians(35)
            L = 44
            jx, jy = m + 6, cyv - 11
            dx, dy = math.cos(ang), math.sin(ang)
            nx, ny = -dy, dx
            r = 8
            sx, sy = jx - L * dx, jy - L * dy
            p1 = (sx + nx * r, sy + ny * r)
            p2 = (sx - nx * r, sy - ny * r)
            q1 = (jx + 9, jy)
            q2 = (jx - 13, jy)
            out.append(f'<polygon points="{p1[0]:.1f},{p1[1]:.1f} {q2[0]:.1f},{q2[1]:.1f} {q1[0]:.1f},{q1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{LUMEN}"/>')
            out.append(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{q2[0]:.1f}" y2="{q2[1]:.1f}" stroke="#3D63A8" stroke-width="2.6"/>')
            out.append(f'<line x1="{p2[0]:.1f}" y1="{p2[1]:.1f}" x2="{q1[0]:.1f}" y2="{q1[1]:.1f}" stroke="#3D63A8" stroke-width="2.6"/>')
            out.append(f'<rect x="{q2[0] + 1.5:.1f}" y="{jy - 1.6:.1f}" width="{q1[0] - q2[0] - 3:.1f}" height="3.2" fill="{LUMEN}"/>')
            out.append(fluxo(a + 6, a + 30, cyv))
            out.append(fluxo(b - 30, b - 6, cyv))
            out.append(seta(jx - 4, jy - 4, jx - 4 - 22 * dx, jy - 4 - 22 * dy, cor=SETA, sw=1.1, cab=4))
        else:
            cx1 = x + pw * 0.27
            cx2 = x + pw * 0.73
            R = 17
            out.append(f'<circle cx="{cx1:.1f}" cy="{cy:.1f}" r="{R}" fill="{LUMEN}" stroke="{PAREDE}" stroke-width="2.6"/>')
            pts = []
            for k in range(3):
                t = math.radians(-90 + k * 120)
                px, py = cx1 + R * math.cos(t), cy + R * math.sin(t)
                out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.6" fill="{DESTAQUE}"/>')
            out.append(seta(cx1 + R + 7, cy, cx2 - R - 7, cy, cor=SETA, sw=1.3, cab=5))
            tri = []
            for k in range(3):
                t = math.radians(-90 + k * 120)
                tri.append((cx2 + (R + 1) * math.cos(t), cy + (R + 1) * math.sin(t)))
            ptxt = ' '.join(f'{px:.1f},{py:.1f}' for px, py in tri)
            out.append(f'<polygon points="{ptxt}" fill="{LUMEN}" stroke="{PAREDE}" stroke-width="2.6" stroke-linejoin="round"/>')
            for k, (px, py) in enumerate(tri):
                t = math.radians(-90 + k * 120)
                ex, ey = px + 9 * math.cos(t), py + 9 * math.sin(t)
                out.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{DESTAQUE}" stroke-width="1.2"/>')
                out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.6" fill="{DESTAQUE}"/>')
        tx, _ = painel_texto(x, y + dh + 14, pw, tit, leg)
        out.append(tx)
    salvar('anastomoses.svg', ph + 1, ''.join(out))


# ------------------------------------------------------------------ fluxograma
def fluxograma():
    out = []
    gap = 12
    cw = (W - 2 * gap) / 3
    def cx_col(i):
        return i * (cw + gap) + cw / 2

    def no(x, y, w, txt, p='m', t=8.2, fill='#FFFFFF', stroke=AZUL_BORDA, cor=TEXTO, pad=8):
        ls = quebra(txt, p, t, w - 2 * pad)
        h = len(ls) * t * 1.3 + 2 * pad - 2
        return h, ls, (x, y, w, fill, stroke, cor, p, t, pad)

    def desenha(h, ls, args):
        x, y, w, fill, stroke, cor, p, t, pad = args
        s = caixa(x, y, w, h, fill=fill, stroke=stroke)
        y0 = y + (h - len(ls) * t * 1.3) / 2 + t * 0.98
        s += bloco(x + w / 2, y0, ls, t, p, cor, 'middle', lh=t * 1.3)
        return s

    # topo
    tw_ = 250
    y = 2
    h, ls, a = no((W - tw_) / 2, y, tw_, 'Suspeita de trauma vascular', 's', 9.4, stroke=DESTAQUE, cor=TITULO)
    out.append(desenha(h, ls, a))
    y += h
    out.append(seta(W / 2, y + 1.5, W / 2, y + 15))
    y += 16
    h, ls, a = no((W - tw_) / 2, y, tw_, 'Ressuscitação volêmica e exame dos sinais', 'm', 8.8)
    out.append(desenha(h, ls, a))
    y += h
    # ramificação para 3 colunas
    yb = y + 12
    out.append(f'<line x1="{W / 2:.1f}" y1="{y + 1.5:.1f}" x2="{W / 2:.1f}" y2="{yb:.1f}" stroke="{SETA}" stroke-width="1.4"/>')
    out.append(f'<line x1="{cx_col(0):.1f}" y1="{yb:.1f}" x2="{cx_col(2):.1f}" y2="{yb:.1f}" stroke="{SETA}" stroke-width="1.4"/>')
    y = yb + 14
    for i in range(3):
        out.append(seta(cx_col(i), yb, cx_col(i), y - 1.5))
    nivel1 = ['Sinais maiores', 'Sinais menores e índice tornozelo-braço bom',
              'Sinais menores e índice tornozelo-braço ruim']
    nos1 = [no(i * (cw + gap), y, cw, t, 's', 9.0, stroke=DESTAQUE, cor=TITULO) for i, t in enumerate(nivel1)]
    h1 = max(n[0] for n in nos1)
    for h, ls, a in nos1:
        out.append(desenha(h1, ls, a))
    y += h1
    nivel2 = [None, 'Observar ou fazer eco-Doppler (duplex), menos invasivo', 'Arteriografia ou eco-Doppler']
    y2 = y + 16
    nos2 = [no(i * (cw + gap), y2, cw, t, 'm', 8.6) if t else None for i, t in enumerate(nivel2)]
    h2 = max(n[0] for n in nos2 if n)
    for i, n_ in enumerate(nos2):
        if n_:
            out.append(seta(cx_col(i), y + 1.5, cx_col(i), y2 - 1.5))
            h, ls, a = n_
            out.append(desenha(h2, ls, a))
    y3 = y2 + h2 + 16
    # finais
    fh = 46
    sub = (cw - 6) / 2
    # coluna 1: seta longa até a cirurgia
    out.append(seta(cx_col(0), y + 1.5, cx_col(0), y3 - 1.5))
    finais = {
        0: [('Cirurgia', '')],
        1: [('Seguimento clínico', 'se nada aparecer'), ('Cirurgia', 'se positivo ou piorou')],
        2: [('Seguimento clínico', 'se negativo'), ('Cirurgia', 'se positivo')],
    }
    for i in range(3):
        x0 = i * (cw + gap)
        itens = finais[i]
        if len(itens) == 1:
            out.append(caixa(x0, y3, cw, fh, fill=VERDE_F, stroke=VERDE_B))
            out.append(T(x0 + cw / 2, y3 + fh / 2 + 3.4, itens[0][0], 10, 's', VERDE_T, 'middle'))
        else:
            yv = y2 + h2
            for k, (t1, t2) in enumerate(itens):
                xx = x0 + k * (sub + 6)
                out.append(seta(cx_col(i), yv + 1.5, xx + sub / 2, y3 - 1.5))
                out.append(caixa(xx, y3, sub, fh, fill=VERDE_F, stroke=VERDE_B))
                l1 = quebra(t1, 's', 8.3, sub - 8)
                l2 = quebra(t2, 'r', 7.4, sub - 8)
                tot = len(l1) * 10.2 + len(l2) * 9.2
                yy = y3 + (fh - tot) / 2 + 7.6
                out.append(bloco(xx + sub / 2, yy, l1, 8.3, 's', VERDE_T, 'middle', lh=10.2))
                out.append(bloco(xx + sub / 2, yy + len(l1) * 10.2, l2, 7.4, 'r', VERDE_T, 'middle', lh=9.2))
    y = y3 + fh + 10
    ah = 30
    out.append(caixa(0, y, W, ah, fill=APOIO))
    t1 = 'Positivo é cirurgia:'
    out.append(T(12, y + 18.8, t1, 8.8, 's', TITULO))
    out.append(T(12 + larg(t1, 's', 8.8) + 5, y + 18.8,
                 'em qualquer etapa, ou se o paciente piorar: cirurgia aberta ou endovascular.', 8.8, 'r', TEXTO))
    salvar('fluxograma.svg', y + ah + 2, ''.join(out))


if __name__ == '__main__':
    trilha()
    guerras()
    lesoes()
    anastomoses()
    fluxograma()
