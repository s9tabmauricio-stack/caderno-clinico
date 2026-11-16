# Desenha as figuras SVG da apostila gastro-a6 (Doenças do fígado).
# Uso: python3 figuras.py  (na pasta de trabalho, com fonts/ copiada pelo preparar.sh)
import os
from PIL import ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = {
    'r': os.path.join(AQUI, 'fonts', 'Inter-Regular.ttf'),
    'm': os.path.join(AQUI, 'fonts', 'Inter-Medium.ttf'),
    's': os.path.join(AQUI, 'fonts', 'Inter-SemiBold.ttf'),
    'b': os.path.join(AQUI, 'fonts', 'Inter-Bold.ttf'),
}
FAMILIA = {'r': ('Inter', 400), 'm': ('Inter Medium', 500), 's': ('Inter SemiBold', 600), 'b': ('Inter', 700)}
_cache = {}

W = 478
BORDA = '#C3D8F8'
APOIO = '#F5F8FF'
SETA = '#8AA9DF'
TEXTO = '#1F2933'
TITULO = '#16315C'
AZUL = '#0B5BD3'
AZUL_CLARO = '#E8F0FE'


def fonte(peso, tam):
    k = (peso, tam)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(FONTES[peso], 100)
    return _cache[k]


def largura(txt, peso, tam):
    return fonte(peso, tam).getlength(txt) * tam / 100.0


def quebra(txt, peso, tam, maxw):
    linhas = []
    for par in txt.split('\n'):
        atual = ''
        for p in par.split(' '):
            t = (atual + ' ' + p).strip()
            if largura(t, peso, tam) <= maxw or not atual:
                atual = t
            else:
                linhas.append(atual)
                atual = p
        linhas.append(atual)
    return linhas


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def texto(x, y, t, peso='r', tam=8, cor=TEXTO, anc='start'):
    fam, w = FAMILIA[peso]
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-weight="{w}" '
            f'font-size="{tam}" fill="{cor}" text-anchor="{anc}">{esc(t)}</text>')


def caixa(x, y, w, h, fill='#FFFFFF', stroke=BORDA, r=7, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def seta_v(x, y1, y2, cor=SETA):
    # seta vertical de y1 até y2 (ponta em y2)
    p = 4.2
    return (f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{y2 - p:.1f}" stroke="{cor}" stroke-width="1.6"/>'
            f'<polygon points="{x - p:.1f},{y2 - p - 1:.1f} {x + p:.1f},{y2 - p - 1:.1f} {x:.1f},{y2:.1f}" fill="{cor}"/>')


def seta_h(x1, x2, y, cor=SETA):
    p = 4.2
    if x2 > x1:
        return (f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2 - p:.1f}" y2="{y:.1f}" stroke="{cor}" stroke-width="1.6"/>'
                f'<polygon points="{x2 - p - 1:.1f},{y - p:.1f} {x2 - p - 1:.1f},{y + p:.1f} {x2:.1f},{y:.1f}" fill="{cor}"/>')
    return (f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2 + p:.1f}" y2="{y:.1f}" stroke="{cor}" stroke-width="1.6"/>'
            f'<polygon points="{x2 + p + 1:.1f},{y - p:.1f} {x2 + p + 1:.1f},{y + p:.1f} {x2:.1f},{y:.1f}" fill="{cor}"/>')


def bloco(x, y, w, titulo=None, corpo=None, tt=8.6, tc=7.6, pad=7, alinhar='start', cor_t=TITULO):
    """Mede e devolve (lista de elementos de texto, altura) para um bloco com título e corpo."""
    els = []
    yy = y + pad
    larg = w - 2 * pad
    tx = x + pad if alinhar == 'start' else x + w / 2
    if titulo:
        for ln in quebra(titulo, 's', tt, larg):
            yy += tt * 1.0
            els.append(texto(tx, yy, ln, 's', tt, cor_t, alinhar))
            yy += tt * 0.28
    if corpo:
        if titulo:
            yy += 2.2
        for ln in quebra(corpo, 'r', tc, larg):
            yy += tc * 1.0
            els.append(texto(tx, yy, ln, 'r', tc, TEXTO, alinhar))
            yy += tc * 0.38
    return els, yy - y + pad - 1


def salvar(nome, h, corpo):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{h:.0f}pt" '
           f'viewBox="0 0 {W} {h:.0f}">' + ''.join(corpo) + '</svg>')
    with open(os.path.join(AQUI, nome), 'w', encoding='utf-8') as f:
        f.write(svg)
    print(nome, f'{W} x {h:.0f} pt')


def selo(cx, cy, n, r=8.5, fill=AZUL):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}"/>' +
            texto(cx, cy + 3.1, str(n), 'b', 8.4, '#FFFFFF', 'middle'))


# ------------------------------------------------------------------ 1. trilha
def trilha():
    etapas = [
        ('Fígado normal', 'anatomia, sangue da veia porta, regeneração'),
        ('Fibrose e cirrose', 'célula estrelada, cicatriz, hipertensão portal'),
        ('Avaliar', 'elastografia, biópsia, Child-Pugh e MELD'),
        ('Causas', 'vírus B e C, gordura, álcool, autoimune, esquistossomose'),
        ('Exame físico', 'sinais do estrógeno alto, cabeça de medusa, flapping'),
        ('Complicações', 'ascite e peritonite, varizes que sangram, encefalopatia'),
        ('Hepatocarcinoma', 'LI-RADS, estadiamento, critérios de Milão'),
        ('Rastreio e transplante', 'ultrassom semestral, quando encaminhar'),
    ]
    gap = 18
    bw = (W - 3 * gap) / 4
    els = []
    tits = [bloco(0, 0, bw - 31, t, None, tt=8.4, pad=0)[1] for t, _ in etapas]
    tit_lin = [max(tits[0:4]), max(tits[4:8])]
    cors = [bloco(0, 0, bw, None, c, tc=7.3, pad=7)[1] for _, c in etapas]
    bh = max(tit_lin[i // 4] + cors[i] + 12 for i in range(8))
    y1 = 2
    y2 = y1 + bh + 26
    for i, (t, c) in enumerate(etapas):
        lin, col = divmod(i, 4)
        x = col * (bw + gap)
        y = y1 if lin == 0 else y2
        els.append(caixa(x + 0.5, y, bw - 1, bh))
        els.append(selo(x + 13, y + 13, i + 1))
        tl, th = bloco(x + 26, y + 7.5, bw - 31, t, None, tt=8.4, pad=0)
        els += tl
        cl, _ = bloco(x, y + 9 + max(tit_lin[lin], 12), bw, None, c, tc=7.3, pad=7)
        els += cl
        if col < 3:
            els.append(seta_h(x + bw + 2, x + bw + gap - 2, y + bh / 2))
    # ligação da etapa 4 para a 5
    xa = 3 * (bw + gap) + bw / 2
    xb = bw / 2
    ym = y1 + bh + 13
    els.append(f'<path d="M{xa:.1f},{y1 + bh + 1:.1f} L{xa:.1f},{ym:.1f} L{xb:.1f},{ym:.1f}" '
               f'fill="none" stroke="{SETA}" stroke-width="1.6"/>')
    els.append(seta_v(xb, ym, y2 - 1))
    salvar('trilha.svg', y2 + bh + 2, els)


# ------------------------------------------- 2. consequências da hipertensão portal
def hipertensao():
    els = []
    topo_t = 'Hipertensão portal'
    topo_c = 'o fígado endurecido freia o sangue; a pressão na veia porta passa de 12 mmHg'
    tw = 360
    tx = (W - tw) / 2
    tl, th = bloco(tx, 0, tw, topo_t, topo_c, tt=9.4, tc=7.8, pad=8, alinhar='middle')
    els.append(caixa(tx, 0.5, tw, th, fill=AZUL_CLARO, stroke=AZUL))
    els += tl
    gap = 14
    cw = (W - 2 * gap) / 3
    cols = [
        [('Capilares do peritônio', 'a pressão alta empurra líquido para fora dos vasos'),
         ('Líquido no abdome', 'transudato: pouca proteína e poucas células'),
         ('Ascite', 'a complicação mais comum; infectada, vira peritonite')],
        [('Sangue desvia do fígado', 'abre caminhos colaterais para voltar ao coração'),
         ('Veias dilatadas', 'varizes do esôfago e do estômago, cabeça de medusa, hemorroidas'),
         ('Amônia chega ao cérebro', 'as toxinas do intestino escapam da limpeza do fígado: encefalopatia')],
        [('Veia esplênica', 'a pressão passa para a veia do baço'),
         ('Baço grande', 'esplenomegalia e hiperesplenismo: o baço sequestra células'),
         ('Sangue com menos células', 'anemia, leucopenia e plaquetopenia')],
    ]
    y0 = th + 22
    alturas = []
    for lin in range(3):
        alturas.append(max(bloco(0, 0, cw, *cols[c][lin], tt=8.4, tc=7.4)[1] for c in range(3)))
    vgap = 12
    for c in range(3):
        x = c * (cw + gap)
        cx = x + cw / 2
        y = y0
        for lin in range(3):
            h = alturas[lin]
            ultimo = lin == 2
            els.append(caixa(x, y, cw, h, fill=AZUL_CLARO if ultimo else '#FFFFFF',
                             stroke=AZUL if ultimo else BORDA))
            tl, _ = bloco(x, y, cw, *cols[c][lin], tt=8.4, tc=7.4)
            els += tl
            if lin < 2:
                els.append(seta_v(cx, y + h + 1, y + h + vgap - 1))
            y += h + vgap
    # ramos do topo
    yb = th + 1
    ym = yb + 10
    xs = [c * (cw + gap) + cw / 2 for c in range(3)]
    els.append(f'<line x1="{W / 2:.1f}" y1="{yb:.1f}" x2="{W / 2:.1f}" y2="{ym:.1f}" stroke="{SETA}" stroke-width="1.6"/>')
    els.append(f'<line x1="{xs[0]:.1f}" y1="{ym:.1f}" x2="{xs[2]:.1f}" y2="{ym:.1f}" stroke="{SETA}" stroke-width="1.6"/>')
    for x in xs:
        els.append(seta_v(x, ym, y0 - 1))
    total = y0 + sum(alturas) + 2 * vgap + 1
    salvar('hipertensao-portal.svg', total, els)


# --------------------------------------------------------- 3. evolução da doença
def evolucao():
    etapas = [
        ('Fígado saudável', 'esponja macia: o sangue passa livre'),
        ('Esteatose', 'gordura dentro dos hepatócitos'),
        ('Esteato-hepatite', 'a gordura inflama os hepatócitos'),
        ('Cirrose', 'fibrose difusa e nódulos; não volta'),
        ('Hepatocarcinoma', 'câncer que nasce no fígado doente'),
    ]
    gap = 16
    bw = (W - 4 * gap) / 5
    top = 34
    bh = max(bloco(0, 0, bw, t, c, tt=8.3, tc=7.3, pad=6)[1] for t, c in etapas)
    els = []
    for i, (t, c) in enumerate(etapas):
        x = i * (bw + gap)
        fim = i >= 3
        els.append(caixa(x, top, bw, bh, fill=AZUL_CLARO if fim else '#FFFFFF', stroke=AZUL if fim else BORDA))
        tl, _ = bloco(x, top, bw, t, c, tt=8.3, tc=7.3, pad=6)
        els += tl
        if i < 4:
            els.append(seta_h(x + bw + 1, x + bw + gap - 1, top + bh / 2))
    # arcos de volta (reversível) sobre as duas primeiras transições
    for i in (1, 2):
        xa = i * (bw + gap) + bw / 2
        xb = (i - 1) * (bw + gap) + bw / 2
        els.append(f'<path d="M{xa:.1f},{top - 2:.1f} C{xa:.1f},{top - 22:.1f} {xb:.1f},{top - 22:.1f} {xb + 3:.1f},{top - 6:.1f}" '
                   f'fill="none" stroke="{AZUL}" stroke-width="1.5"/>')
        els.append(f'<polygon points="{xb - 1:.1f},{top - 8:.1f} {xb + 7:.1f},{top - 9:.1f} {xb + 2:.1f},{top - 1:.1f}" fill="{AZUL}"/>')
        els.append(texto((xa + xb) / 2, top - 22, 'regride', 's', 7.4, AZUL, 'middle'))
    # cirrose: sem volta
    i = 3
    xa = i * (bw + gap) + bw / 2
    xb = (i - 1) * (bw + gap) + bw / 2
    els.append(f'<path d="M{xa:.1f},{top - 2:.1f} C{xa:.1f},{top - 22:.1f} {xb:.1f},{top - 22:.1f} {xb + 3:.1f},{top - 6:.1f}" '
               f'fill="none" stroke="{SETA}" stroke-width="1.4" stroke-dasharray="3 3"/>')
    xm = (xa + xb) / 2
    els.append(f'<line x1="{xm - 5:.1f}" y1="{top - 22:.1f}" x2="{xm + 5:.1f}" y2="{top - 12:.1f}" stroke="{TITULO}" stroke-width="1.8"/>')
    els.append(f'<line x1="{xm + 5:.1f}" y1="{top - 22:.1f}" x2="{xm - 5:.1f}" y2="{top - 12:.1f}" stroke="{TITULO}" stroke-width="1.8"/>')
    els.append(texto(xm + 9, top - 25, 'irreversível', 's', 7.4, TITULO, 'start'))
    # nota de rodapé da figura
    y = top + bh + 14
    nota = ('Vale para o álcool e para a gordura da síndrome metabólica. Sem a agressão (sem beber, perdendo peso), '
            'esteatose e esteato-hepatite regridem; a cirrose não, e ainda abre caminho para o câncer.')
    for ln in quebra(nota, 'r', 7.5, W - 4):
        els.append(texto(2, y, ln, 'r', 7.5, '#3A3A3C'))
        y += 10.5
    salvar('evolucao.svg', y - 4, els)


# ----------------------------------------------- 4. sangramento de varizes
def hda():
    els = []
    vgap = 15
    y = 1
    linhas_cheias = [
        ('Cirrótico sangrando por varizes', 'vomita sangue ou evacua sangue escuro; pode estar confuso e aspirar o vômito', True),
        ('1. Estabilizar como no trauma', 'reposição de volume se necessário, oxigênio e proteção da via aérea; sangue, plaquetas e fatores de coagulação que faltarem', False),
        ('2. Droga vasoativa e antibiótico', 'octreotide (no slide também terlipressina e somatostatina) para baixar a pressão nas varizes; antibiótico para evitar a peritonite e outras infecções', False),
    ]
    for t, c, dest in linhas_cheias:
        tl, h = bloco(0, y, W, t, c, tt=8.6, tc=7.5, pad=7, alinhar='middle')
        els.append(caixa(0.5, y, W - 1, h, fill=AZUL_CLARO if dest else '#FFFFFF', stroke=AZUL if dest else BORDA))
        els += tl
        y += h
        if t.startswith('2.'):
            els.append(f'<line x1="{W / 2:.1f}" y1="{y + 1:.1f}" x2="{W / 2:.1f}" y2="{y + vgap / 2:.1f}" stroke="{SETA}" stroke-width="1.6"/>')
        else:
            els.append(seta_v(W / 2, y + 1, y + vgap - 1))
        y += vgap
    # divisão estável / instável
    gap = 18
    lw = 290
    rw = W - lw - gap
    rx = lw + gap
    yl = y
    tl, h1 = bloco(0, yl, lw, '3. Estável: endoscopia', 'tratamento definitivo do ponto que sangra', tt=8.6, tc=7.5, pad=7, alinhar='middle')
    tr, h1r = bloco(rx, yl, rw, 'Instável ou sem controle', 'balão de Sengstaken-Blakemore na terapia intensiva, só por 24 a 48 horas', tt=8.6, tc=7.5, pad=7, alinhar='middle')
    hh = max(h1, h1r)
    els.append(caixa(0.5, yl, lw - 1, hh))
    els += tl
    els.append(caixa(rx, yl, rw - 0.5, hh))
    els += tr
    # ligação do passo 2 para os dois lados
    yv = y - vgap
    # a seta central já desce até y; desenha ramo para a direita
    els.append(f'<line x1="{W / 2:.1f}" y1="{yv + vgap / 2:.1f}" x2="{rx + rw / 2:.1f}" y2="{yv + vgap / 2:.1f}" stroke="{SETA}" stroke-width="1.6"/>')
    els.append(seta_v(rx + rw / 2, yv + vgap / 2, yl - 1))
    # remove a seta central (passa a ir para a esquerda)
    els.append(f'<line x1="{W / 2:.1f}" y1="{yv + vgap / 2:.1f}" x2="{lw / 2:.1f}" y2="{yv + vgap / 2:.1f}" stroke="{SETA}" stroke-width="1.6"/>')
    els.append(seta_v(lw / 2, yv + vgap / 2, yl - 1))
    y = yl + hh
    # linha seguinte
    y2 = y + vgap
    sw = (lw - 12) / 2
    a_t, a_c = 'Varizes do esôfago', 'ligadura elástica: o endoscopista laça a variz com um anel de borracha'
    b_t, b_c = 'Varizes do fundo gástrico', 'cianoacrilato: uma cola, como a de secagem rápida, que fecha a variz'
    c_t, c_c = 'Falharam endoscopia e balão', 'derivação portossistêmica intra-hepática transjugular: um stent liga a veia porta à veia hepática'
    ha = bloco(0, 0, sw, a_t, a_c, tt=8.3, tc=7.4)[1]
    hb = bloco(0, 0, sw, b_t, b_c, tt=8.3, tc=7.4)[1]
    hc = bloco(0, 0, rw, c_t, c_c, tt=8.3, tc=7.4)[1]
    h2 = max(ha, hb, hc)
    for x, w, t, c in [(0.5, sw, a_t, a_c), (sw + 12, sw, b_t, b_c), (rx, rw - 0.5, c_t, c_c)]:
        els.append(caixa(x, y2, w, h2))
        tl, _ = bloco(x, y2, w, t, c, tt=8.3, tc=7.4)
        els += tl
    ym = y + vgap / 2
    els.append(f'<line x1="{lw / 2:.1f}" y1="{y + 1:.1f}" x2="{lw / 2:.1f}" y2="{ym:.1f}" stroke="{SETA}" stroke-width="1.6"/>')
    els.append(f'<line x1="{sw / 2:.1f}" y1="{ym:.1f}" x2="{sw + 12 + sw / 2:.1f}" y2="{ym:.1f}" stroke="{SETA}" stroke-width="1.6"/>')
    els.append(seta_v(sw / 2, ym, y2 - 1))
    els.append(seta_v(sw + 12 + sw / 2, ym, y2 - 1))
    els.append(seta_v(rx + rw / 2, y + 1, y2 - 1))
    y = y2 + h2
    els.append(seta_v(lw / 2, y + 1, y + vgap - 1))
    y += vgap
    tl, h = bloco(0, y, W, 'Depois: evitar o próximo sangramento', 'quem tem varizes comprovadas na endoscopia recebe betabloqueador: carvedilol (ou propranolol)', tt=8.6, tc=7.5, pad=7, alinhar='middle')
    els.append(caixa(0.5, y, W - 1, h, fill=AZUL_CLARO, stroke=AZUL))
    els += tl
    salvar('hda.svg', y + h + 1, els)


# ------------------------------------------- 5. estadiamento e tratamento
def bclc():
    cols = [
        ('Inicial (0 e A)', 'nódulo único ou até 3 nódulos de até 3 cm; função do fígado preservada; paciente ativo',
         'Ressecção, transplante ou ablação', 'ressecção só sem hipertensão portal; transplante dentro dos critérios de Milão',
         'Intenção de cura: sobrevida em 5 anos de 40 a 70%'),
        ('Intermediário (B)', 'vários nódulos; função preservada; paciente ativo',
         'Quimioembolização', 'quimioterápico injetado pela artéria que nutre o nódulo',
         'Paliativo: sobrevida em 3 anos de 10 a 40%'),
        ('Avançado (C)', 'invasão da veia porta ou doença fora do fígado; função preservada',
         'Quimioterapia oral', 'sorafenibe',
         'Paliativo: sobrevida em 3 anos de 10 a 40%'),
        ('Terminal (D)', 'fígado em falência ou paciente acamado, sem condições',
         'Cuidados paliativos', 'controle de sintomas',
         'Sintomático: sobrevida em 1 ano abaixo de 20%'),
    ]
    gap = 10
    cw = (W - 3 * gap) / 4
    vgap = 14
    h1 = max(bloco(0, 0, cw, a, b, tt=8.3, tc=7.2)[1] for a, b, *_ in cols)
    h2 = max(bloco(0, 0, cw, c, d, tt=8.3, tc=7.2)[1] for _, _, c, d, _ in cols)
    h3 = max(bloco(0, 0, cw, None, e, tc=7.0)[1] for *_, e in cols)
    els = []
    y1 = 1
    for i, (a, b, c, d, e) in enumerate(cols):
        x = i * (cw + gap)
        els.append(caixa(x + 0.5, y1, cw - 1, h1))
        els += bloco(x, y1, cw, a, b, tt=8.3, tc=7.2)[0]
        y2 = y1 + h1 + vgap
        els.append(seta_v(x + cw / 2, y1 + h1 + 1, y2 - 1))
        els.append(caixa(x + 0.5, y2, cw - 1, h2, fill=AZUL_CLARO, stroke=AZUL))
        els += bloco(x, y2, cw, c, d, tt=8.3, tc=7.2)[0]
        y3 = y2 + h2 + 6
        els.append(caixa(x + 0.5, y3, cw - 1, h3, fill=APOIO, stroke=BORDA, dash='3 2'))
        els += bloco(x, y3, cw, None, e, tc=7.0)[0]
    salvar('bclc.svg', y1 + h1 + vgap + h2 + 6 + h3 + 1, els)


if __name__ == '__main__':
    trilha()
    hipertensao()
    evolucao()
    hda()
    bclc()
