#!/usr/bin/env python3
"""Desenha as figuras da apostila angio-a2 (trilha, formas, aorta, decisao) em SVG.

Rodar na pasta de trabalho: python3 figuras.py
Mede o texto com a fonte Inter da pasta fonts/ (copiada pelo preparar.sh).
"""
import os
from PIL import ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = {400: "Inter-Regular.ttf", 500: "Inter-Medium.ttf", 600: "Inter-SemiBold.ttf", 700: "Inter-Bold.ttf"}
_cache = {}

AZUL_ESC = "#16315C"
AZUL = "#0B5BD3"
BORDA = "#C3D8F8"
APOIO = "#F5F8FF"
CLARO = "#E8F0FE"
SETA = "#8AA9DF"
TEXTO = "#1F2933"
CINZA = "#6C6C70"
W = 478


def fonte(peso, tam):
    k = (peso, tam)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(os.path.join(AQUI, "fonts", FONTES[peso]), tam * 10)
    return _cache[k]


def larg(txt, peso, tam):
    return fonte(peso, tam).getlength(txt) / 10


def quebra(txt, peso, tam, maxw):
    linhas, atual = [], ""
    for p in txt.split():
        t = (atual + " " + p).strip()
        if larg(t, peso, tam) <= maxw or not atual:
            atual = t
        else:
            linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    return linhas


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def texto(x, y, txt, peso=400, tam=8, cor=TEXTO, anc="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter" font-weight="{peso}" '
            f'font-size="{tam}" fill="{cor}" text-anchor="{anc}">{esc(txt)}</text>')


def bloco(x, y, linhas, peso=400, tam=8, cor=TEXTO, anc="start", entre=None):
    entre = entre or tam * 1.32
    return "".join(texto(x, y + i * entre, l, peso, tam, cor, anc) for i, l in enumerate(linhas))


def svg(nome, h, corpo):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{h}pt" '
         f'viewBox="0 0 {W} {h}">{corpo}</svg>')
    with open(os.path.join(AQUI, nome), "w", encoding="utf-8") as f:
        f.write(s)


def seta_baixo(x, y1, y2):
    return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2 - 5}" stroke="{SETA}" stroke-width="1.6"/>'
            f'<polygon points="{x - 4},{y2 - 6} {x + 4},{y2 - 6} {x},{y2}" fill="{SETA}"/>')


def seta_dir(x1, x2, y):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2 - 5}" y2="{y}" stroke="{SETA}" stroke-width="1.6"/>'
            f'<polygon points="{x2 - 6},{y - 4} {x2 - 6},{y + 4} {x2},{y}" fill="{SETA}"/>')


# ---------------------------------------------------------------- trilha
def trilha():
    etapas = [
        ("O que é aneurisma", "50% ou mais, localizado; parede e formato"),
        ("Viscerais: quando tratar", "romper × risco do procedimento"),
        ("Viscerais: como tratar", "molas, stent ou cirurgia aberta"),
        ("Aorta: quem tem", "idoso, homem, abaixo das renais"),
        ("Diagnóstico", "palpar com as duas mãos; imagem"),
        ("Quando operar", "5,5 cm, 5 cm na mulher, crescimento"),
        ("Como tratar a aorta", "clínico sempre; endovascular"),
    ]
    n = len(etapas)
    m = 35
    passo = (W - 2 * m) / (n - 1)
    cy = 20
    corpo = [f'<rect x="0" y="0" width="{W}" height="100" rx="10" fill="{APOIO}"/>',
             f'<line x1="{m}" y1="{cy}" x2="{W - m}" y2="{cy}" stroke="{SETA}" stroke-width="2.4"/>']
    for i, (tit, sub) in enumerate(etapas):
        cx = m + i * passo
        corpo.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="10.5" fill="{AZUL}"/>')
        corpo.append(texto(cx, cy + 3.4, str(i + 1), 700, 9.5, "#FFFFFF", "middle"))
        lt = quebra(tit, 600, 8.2, 62)
        corpo.append(bloco(cx, cy + 25, lt, 600, 8.2, AZUL_ESC, "middle", 10.4))
        ls = quebra(sub, 400, 7.2, 62)
        y0 = cy + 25 + len(lt) * 10.4 + 3
        corpo.append(bloco(cx, y0, ls, 400, 7.2, CINZA, "middle", 9.2))
    svg("trilha.svg", 100, "".join(corpo))


# ---------------------------------------------------------------- formas
def formas():
    pw = W / 5
    top, bot = 12, 132
    parede = f'stroke="{AZUL_ESC}" stroke-width="2.6" fill="none" stroke-linecap="round"'
    corpo = []
    paineis = [
        ("Vaso normal", "três camadas; calibre igual"),
        ("Fusiforme", "dilata por igual: pressão distribuída"),
        ("Sacular", "saco para um lado: pressão concentrada"),
        ("Pseudoaneurisma", "a parede rompeu: capa de coágulo"),
        ("Dissecção", "rasgo da íntima e da média: a luz falsa (escura) aperta a verdadeira"),
    ]
    for i, (tit, sub) in enumerate(paineis):
        cx = pw * i + pw / 2
        x0 = pw * i + 3
        corpo.append(f'<rect x="{x0:.1f}" y="2" width="{pw - 6:.1f}" height="192" rx="9" fill="{APOIO}"/>')
        r = 12
        L, R = cx - r, cx + r
        if i == 0:
            corpo.append(f'<rect x="{L:.1f}" y="{top}" width="{2 * r}" height="{bot - top}" fill="{CLARO}"/>')
            corpo.append(f'<line x1="{L:.1f}" y1="{top}" x2="{L:.1f}" y2="{bot}" {parede}/>')
            corpo.append(f'<line x1="{R:.1f}" y1="{top}" x2="{R:.1f}" y2="{bot}" {parede}/>')
        elif i == 1:
            b = 30
            esq = f"M{L:.1f},{top} L{L:.1f},38 C{L:.1f},52 {cx - b:.1f},55 {cx - b:.1f},72 C{cx - b:.1f},89 {L:.1f},92 {L:.1f},106 L{L:.1f},{bot}"
            dir_ = f"M{R:.1f},{top} L{R:.1f},38 C{R:.1f},52 {cx + b:.1f},55 {cx + b:.1f},72 C{cx + b:.1f},89 {R:.1f},92 {R:.1f},106 L{R:.1f},{bot}"
            fill = (f"M{L:.1f},{top} L{L:.1f},38 C{L:.1f},52 {cx - b:.1f},55 {cx - b:.1f},72 C{cx - b:.1f},89 {L:.1f},92 {L:.1f},106 L{L:.1f},{bot} "
                    f"L{R:.1f},{bot} L{R:.1f},106 C{R:.1f},92 {cx + b:.1f},89 {cx + b:.1f},72 C{cx + b:.1f},55 {R:.1f},52 {R:.1f},38 L{R:.1f},{top} Z")
            corpo.append(f'<path d="{fill}" fill="{CLARO}"/>')
            corpo.append(f'<path d="{esq}" {parede}/><path d="{dir_}" {parede}/>')
        elif i == 2:
            s = 30
            dir_ = f"M{R:.1f},{top} L{R:.1f},50 C{R + 4:.1f},40 {R + s:.1f},40 {R + s:.1f},66 C{R + s:.1f},92 {R + 4:.1f},92 {R:.1f},82 L{R:.1f},{bot}"
            fill = (f"M{L:.1f},{top} L{R:.1f},{top} L{R:.1f},50 C{R + 4:.1f},40 {R + s:.1f},40 {R + s:.1f},66 "
                    f"C{R + s:.1f},92 {R + 4:.1f},92 {R:.1f},82 L{R:.1f},{bot} L{L:.1f},{bot} Z")
            corpo.append(f'<path d="{fill}" fill="{CLARO}"/>')
            corpo.append(f'<line x1="{L:.1f}" y1="{top}" x2="{L:.1f}" y2="{bot}" {parede}/>')
            corpo.append(f'<path d="{dir_}" {parede}/>')
        elif i == 3:
            corpo.append(f'<ellipse cx="{R + 19:.1f}" cy="72" rx="20" ry="27" fill="{BORDA}" stroke="{SETA}" stroke-width="1.6" stroke-dasharray="3.5 2.5"/>')
            corpo.append(f'<rect x="{L:.1f}" y="{top}" width="{2 * r}" height="{bot - top}" fill="{CLARO}"/>')
            corpo.append(f'<rect x="{R - 1:.1f}" y="66" width="6" height="12" fill="{CLARO}"/>')
            corpo.append(f'<line x1="{L:.1f}" y1="{top}" x2="{L:.1f}" y2="{bot}" {parede}/>')
            corpo.append(f'<line x1="{R:.1f}" y1="{top}" x2="{R:.1f}" y2="65" {parede}/>')
            corpo.append(f'<line x1="{R:.1f}" y1="79" x2="{R:.1f}" y2="{bot}" {parede}/>')
        else:
            b = 19
            outer = (f"M{L:.1f},{top} L{L:.1f},34 C{L:.1f},46 {cx - b:.1f},48 {cx - b:.1f},64 L{cx - b:.1f},88 C{cx - b:.1f},104 {L:.1f},106 {L:.1f},116 L{L:.1f},{bot} "
                     f"L{R:.1f},{bot} L{R:.1f},116 C{R:.1f},106 {cx + b:.1f},104 {cx + b:.1f},88 L{cx + b:.1f},64 C{cx + b:.1f},48 {R:.1f},46 {R:.1f},34 L{R:.1f},{top} Z")
            corpo.append(f'<path d="{outer}" fill="{BORDA}"/>')
            flap = f"M{R - 2:.1f},30 C{cx - 4:.1f},44 {cx - 9:.1f},58 {cx - 10:.1f},76 C{cx - 10:.1f},96 {cx - 2:.1f},108 {R - 3:.1f},120"
            corpo.append(f'<path d="M{L:.1f},{top} L{R:.1f},{top} L{R:.1f},28 L{R - 2:.1f},30 C{cx - 4:.1f},44 {cx - 9:.1f},58 {cx - 10:.1f},76 C{cx - 10:.1f},96 {cx - 2:.1f},108 {R - 3:.1f},120 L{R:.1f},122 L{R:.1f},{bot} L{L:.1f},{bot} L{L:.1f},116 C{L:.1f},106 {cx - b:.1f},104 {cx - b:.1f},88 L{cx - b:.1f},64 C{cx - b:.1f},48 {L:.1f},46 {L:.1f},34 Z" fill="{CLARO}"/>')
            corpo.append(f'<path d="{flap}" stroke="{AZUL}" stroke-width="1.8" fill="none" stroke-linecap="round"/>')
            esq = f"M{L:.1f},{top} L{L:.1f},34 C{L:.1f},46 {cx - b:.1f},48 {cx - b:.1f},64 L{cx - b:.1f},88 C{cx - b:.1f},104 {L:.1f},106 {L:.1f},116 L{L:.1f},{bot}"
            dir_ = f"M{R:.1f},{top} L{R:.1f},34 C{R:.1f},46 {cx + b:.1f},48 {cx + b:.1f},64 L{cx + b:.1f},88 C{cx + b:.1f},104 {R:.1f},106 {R:.1f},116 L{R:.1f},{bot}"
            corpo.append(f'<path d="{esq}" {parede}/><path d="{dir_}" {parede}/>')
        if i == 3:
            corpo.append(texto(R + 19, 74.5, "coágulo", 500, 6.2, AZUL_ESC, "middle"))
        corpo.append(bloco(cx, 152, quebra(tit, 600, 8.6, pw - 12), 600, 8.6, AZUL_ESC, "middle"))
        corpo.append(bloco(cx, 165, quebra(sub, 400, 7.3, pw - 14), 400, 7.3, TEXTO, "middle", 9.4))
    svg("formas.svg", 196, "".join(corpo))


# ---------------------------------------------------------------- aorta
def tubo(d, w=7):
    return (f'<path d="{d}" stroke="{AZUL_ESC}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" stroke="{CLARO}" stroke-width="{w - 3.2}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def aorta():
    H = 352
    cx = 239
    L, R = cx - 11, cx + 11
    corpo = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="10" fill="{APOIO}"/>']
    # faixa da aorta infrarrenal
    corpo.append(f'<rect x="{cx - 52}" y="126" width="104" height="146" rx="8" fill="#FFFFFF" stroke="{BORDA}" stroke-dasharray="4 3"/>')
    # lombares (atrás da aorta)
    for y in (140, 158, 248):
        corpo.append(f'<line x1="{L - 22}" y1="{y}" x2="{L}" y2="{y}" stroke="{SETA}" stroke-width="2.2" stroke-dasharray="3 2"/>')
        corpo.append(f'<line x1="{R}" y1="{y}" x2="{R + 22}" y2="{y}" stroke="{SETA}" stroke-width="2.2" stroke-dasharray="3 2"/>')
    # ilíacas
    corpo.append(tubo(f"M{cx - 5},268 L{cx - 38},334", 13))
    corpo.append(tubo(f"M{cx + 5},268 L{cx + 38},334", 13))
    # rins e renais
    corpo.append(f'<ellipse cx="{cx - 62}" cy="116" rx="12" ry="23" fill="#FFFFFF" stroke="{SETA}" stroke-width="1.4"/>')
    corpo.append(f'<ellipse cx="{cx + 62}" cy="116" rx="12" ry="23" fill="#FFFFFF" stroke="{SETA}" stroke-width="1.4"/>')
    corpo.append(tubo(f"M{cx},112 L{cx - 52},114", 7))
    corpo.append(tubo(f"M{cx},112 L{cx + 52},114", 7))
    # aorta com aneurisma infrarrenal
    b = 30
    contorno = (f"M{L},22 L{L},166 C{L},180 {cx - b},182 {cx - b},208 C{cx - b},236 {L},242 {L + 4},256 L{cx - 6},270 "
                f"L{cx + 6},270 L{R - 4},256 C{R},242 {cx + b},236 {cx + b},208 C{cx + b},182 {R},180 {R},166 L{R},22 Z")
    corpo.append(f'<path d="{contorno}" fill="{CLARO}" stroke="{AZUL_ESC}" stroke-width="2.4" stroke-linejoin="round"/>')
    # trombo mural sugerido
    corpo.append(f'<path d="M{cx - b + 4},208 C{cx - b + 4},188 {cx - 13},186 {cx - 10},200 L{cx - 10},222 C{cx - 12},234 {cx - b + 5},230 {cx - b + 4},208 Z" fill="{BORDA}"/>')
    # mesentérica inferior (sai do saco)
    corpo.append(tubo(f"M{cx + 20},198 C{cx + 40},204 {cx + 52},214 {cx + 60},238", 5.6))
    # mesentérica superior (anterior, desce)
    corpo.append(tubo(f"M{R - 3},80 C{R + 10},84 {R + 15},96 {R + 15},152", 6.4))
    # tronco celíaco (sai pela frente, à direita do desenho) e seus ramos
    corpo.append(tubo(f"M{cx + 30},53 C{cx + 12},40 {cx - 20},40 {cx - 66},44", 6.4))
    corpo.append(tubo(f"M{cx + 30},53 C{cx + 42},48 {cx + 48},56 {cx + 58},50 C{cx + 66},45 {cx + 72},52 {cx + 80},48", 6.4))
    corpo.append(tubo(f"M{R - 3},64 L{cx + 30},53", 7))
    # diafragma
    corpo.append(f'<path d="M{cx - 72},28 Q{cx},8 {cx + 72},28" stroke="{SETA}" stroke-width="3" fill="none" stroke-linecap="round"/>')

    def rot_esq(y, alvo, linhas):
        xs = 150
        corpo.append(f'<line x1="{xs + 4}" y1="{y - 3}" x2="{alvo[0]}" y2="{alvo[1]}" stroke="{SETA}" stroke-width="0.9"/>')
        corpo.append(f'<circle cx="{alvo[0]}" cy="{alvo[1]}" r="1.8" fill="{AZUL}"/>')
        corpo.append(bloco(xs, y, [linhas[0]], 600, 8, AZUL_ESC, "end"))
        if len(linhas) > 1:
            corpo.append(bloco(xs, y + 10, linhas[1:], 400, 7.2, CINZA, "end", 9.2))

    def rot_dir(y, alvo, linhas):
        xs = 328
        corpo.append(f'<line x1="{xs - 4}" y1="{y - 3}" x2="{alvo[0]}" y2="{alvo[1]}" stroke="{SETA}" stroke-width="0.9"/>')
        corpo.append(f'<circle cx="{alvo[0]}" cy="{alvo[1]}" r="1.8" fill="{AZUL}"/>')
        corpo.append(bloco(xs, y, [linhas[0]], 600, 8, AZUL_ESC, "start"))
        if len(linhas) > 1:
            corpo.append(bloco(xs, y + 10, linhas[1:], 400, 7.2, CINZA, "start", 9.2))

    rot_esq(16, (cx - 60, 21), ["Diafragma", "acima, aorta torácica"])
    rot_esq(52, (cx - 56, 44), ["Hepática comum", "fígado; dá a gastroduodenal"])
    rot_esq(96, (cx - 62, 100), ["Rim e artéria renal", "direita"])
    rot_esq(146, (cx - 20, 140), ["Colo e artérias lombares", "lombares: atrás da aorta,", "irrigam medula e costas"])
    rot_esq(214, (cx - 22, 210), ["Trombo mural", "parede do saco forrada", "de coágulo"])
    rot_esq(312, (cx - 30, 318), ["Ilíaca comum direita"])

    rot_dir(32, (cx + 74, 50), ["Esplênica", "baço"])
    rot_dir(70, (cx + 22, 57), ["Tronco celíaco", "colado no diafragma"])
    rot_dir(102, (cx + 26, 96), ["Mesentérica superior", "boa parte do intestino delgado"])
    rot_dir(130, (cx + 70, 124), ["Rim e artéria renal", "esquerda"])
    rot_dir(186, (cx + 28, 196), ["Aneurisma infrarrenal", "entre as renais e a", "bifurcação: o mais comum"])
    rot_dir(246, (cx + 58, 234), ["Mesentérica inferior"])
    rot_dir(312, (cx + 30, 318), ["Ilíaca comum esquerda"])
    svg("aorta.svg", H, "".join(corpo))


# ---------------------------------------------------------------- decisão
def decisao():
    qx, qw = 6, 236
    cxx, cw = 286, 186
    corpo = []
    y = 4
    topo = "Aneurisma de aorta abdominal encontrado"
    corpo.append(f'<rect x="{qx}" y="{y}" width="{qw}" height="26" rx="8" fill="{AZUL_ESC}"/>')
    corpo.append(texto(qx + qw / 2, y + 16.6, topo, 600, 8.6, "#FFFFFF", "middle"))
    y += 26
    perguntas = [
        ("Rompeu?", "Operar já, pelo caminho mais rápido (em geral, endoprótese)"),
        ("Dói, sem outra causa que explique a dor?", "Operar (eletiva; de preferência endovascular)"),
        ("5,5 cm ou mais no homem; 5,0 cm ou mais na mulher?", "Operar, com ou sem sintoma"),
        ("Cresceu 0,5 cm em 6 meses ou 1 cm em 1 ano?", "Operar (precisa de exame anterior para comparar)"),
        ("Formato sacular, com 3 cm ou mais?", "Considerar operar"),
    ]
    for q, c in perguntas:
        y += 14
        ql = quebra(q, 500, 8.4, qw - 20)
        cl = quebra(c, 600, 8.2, cw - 20)
        h = max(len(ql) * 11 + 14, len(cl) * 10.8 + 14, 34)
        corpo.append(seta_baixo(qx + qw / 2, y - 14, y))
        corpo.append(f'<rect x="{qx}" y="{y}" width="{qw}" height="{h}" rx="8" fill="#FFFFFF" stroke="{BORDA}" stroke-width="1.2"/>')
        corpo.append(bloco(qx + 10, y + h / 2 - (len(ql) - 1) * 5.5 + 3, ql, 500, 8.4, TEXTO, "start", 11))
        corpo.append(seta_dir(qx + qw, cxx, y + h / 2))
        corpo.append(texto((qx + qw + cxx) / 2, y + h / 2 - 4.5, "sim", 600, 7.4, AZUL, "middle"))
        corpo.append(f'<rect x="{cxx}" y="{y}" width="{cw}" height="{h}" rx="8" fill="{CLARO}" stroke="{AZUL}" stroke-width="1.2"/>')
        corpo.append(bloco(cxx + 10, y + h / 2 - (len(cl) - 1) * 5.4 + 3, cl, 600, 8.2, AZUL_ESC, "start", 10.8))
        corpo.append(texto(qx + qw / 2 + 6, y + h + 10, "não", 600, 7.4, AZUL, "start"))
        y += h
    y += 14
    corpo.append(seta_baixo(qx + qw / 2, y - 14, y))
    fim_t = "Sem indicação: tratamento clínico da aterosclerose e ultrassom"
    fim_l = ["Abaixo de 4 cm: ultrassom a cada 1 ano.",
             "De 4 a 5,4 cm: ultrassom a cada 6 meses."]
    hf = 44
    corpo.append(f'<rect x="{qx}" y="{y}" width="{W - 2 * qx}" height="{hf}" rx="8" fill="{APOIO}" stroke="{BORDA}" stroke-width="1.2"/>')
    corpo.append(texto(qx + 10, y + 16, fim_t, 600, 8.4, AZUL_ESC))
    corpo.append(texto(qx + 10, y + 31, fim_l[0] + "   " + fim_l[1], 400, 8.2, TEXTO))
    y += hf + 3
    svg("decisao.svg", round(y), "".join(corpo))


# ---------------------------------------------------------------- reparo endovascular
def evar():
    pw = W / 3
    H = 212
    corpo = []
    paineis = [
        ("1. Fios pelas femorais", "fio-guia e cateter sobem pelas femorais até a aorta"),
        ("2. Corpo principal", "liberado abaixo das renais; o ramo curto fica aberto no saco"),
        ("3. Segundo módulo", "pescado pela outra femoral: o saco fica sem fluxo"),
    ]
    for i, (tit, sub) in enumerate(paineis):
        x0 = pw * i
        cx = x0 + pw / 2
        corpo.append(f'<rect x="{x0 + 3:.1f}" y="2" width="{pw - 6:.1f}" height="{H - 4}" rx="9" fill="{APOIO}"/>')
        L, R = cx - 10, cx + 10
        b = 30
        # renais
        corpo.append(tubo(f"M{L - 18:.1f},26 L{R + 18:.1f},26", 6))
        # ilíacas
        corpo.append(tubo(f"M{cx - 7:.1f},118 L{cx - 30:.1f},162", 13))
        corpo.append(tubo(f"M{cx + 7:.1f},118 L{cx + 30:.1f},162", 13))
        saco = APOIO if i == 2 else CLARO
        contorno = (f"M{L:.1f},10 L{L:.1f},48 C{L:.1f},60 {cx - b:.1f},62 {cx - b:.1f},82 C{cx - b:.1f},104 {L:.1f},108 {L + 2:.1f},112 L{cx - 9:.1f},119 "
                    f"L{cx + 9:.1f},119 L{R - 2:.1f},112 C{R:.1f},108 {cx + b:.1f},104 {cx + b:.1f},82 C{cx + b:.1f},62 {R:.1f},60 {R:.1f},48 L{R:.1f},10 Z")
        corpo.append(f'<path d="{contorno}" fill="{saco}" stroke="{AZUL_ESC}" stroke-width="2.2" stroke-linejoin="round"'
                     + (' stroke-dasharray="0"' if i < 2 else '') + '/>')
        if i == 0:
            corpo.append(f'<path d="M{cx - 30:.1f},166 L{cx - 6:.1f},121 L{cx - 3:.1f},70 L{cx - 2:.1f},18" stroke="{AZUL_ESC}" stroke-width="1.1" fill="none"/>')
            corpo.append(f'<path d="M{cx + 30:.1f},166 L{cx + 6:.1f},121 L{cx + 4:.1f},92" stroke="{AZUL_ESC}" stroke-width="1.1" fill="none"/>')
        else:
            g = AZUL
            corpo.append(f'<path d="M{cx:.1f},31 L{cx:.1f},66" stroke="{g}" stroke-width="17" fill="none"/>')
            corpo.append(f'<path d="M{cx - 4:.1f},64 L{cx - 6:.1f},116 L{cx - 28:.1f},158" stroke="{g}" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
            corpo.append(f'<path d="M{cx + 4:.1f},64 L{cx + 6:.1f},86" stroke="{g}" stroke-width="8" fill="none"/>')
            for yy in (38, 46, 54):
                corpo.append(f'<line x1="{cx - 8:.1f}" y1="{yy}" x2="{cx + 8:.1f}" y2="{yy}" stroke="#FFFFFF" stroke-width="0.9" opacity="0.8"/>')
            if i == 2:
                corpo.append(f'<path d="M{cx + 6:.1f},84 L{cx + 6:.1f},116 L{cx + 28:.1f},158" stroke="{g}" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
                corpo.append(texto(cx - 21, 82, "sem", 500, 6, AZUL_ESC, "middle"))
                corpo.append(texto(cx - 21, 89.5, "fluxo", 500, 6, AZUL_ESC, "middle"))
            else:
                corpo.append(f'<path d="M{cx + 30:.1f},166 L{cx + 7:.1f},119 L{cx + 6:.1f},96" stroke="{AZUL_ESC}" stroke-width="1.1" fill="none"/>')
                corpo.append(f'<line x1="{cx + 11:.1f}" y1="84" x2="{cx + 36:.1f}" y2="70" stroke="{SETA}" stroke-width="0.9"/>')
                corpo.append(texto(cx + 38, 66, "ramo curto", 500, 6, AZUL_ESC, "start"))
                corpo.append(texto(cx + 38, 73.5, "aberto", 500, 6, AZUL_ESC, "start"))
        corpo.append(texto(L - 21, 20, "renal", 500, 6, CINZA, "middle"))
        corpo.append(bloco(cx, 180, quebra(tit, 600, 8.6, pw - 14), 600, 8.6, AZUL_ESC, "middle"))
        corpo.append(bloco(cx, 193, quebra(sub, 400, 7.3, pw - 18), 400, 7.3, TEXTO, "middle", 9.4))
    svg("evar.svg", H + 10, "".join(corpo))


if __name__ == "__main__":
    trilha()
    formas()
    aorta()
    decisao()
    evar()
    print("figuras: trilha.svg formas.svg aorta.svg decisao.svg evar.svg")
