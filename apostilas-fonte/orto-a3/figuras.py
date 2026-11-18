"""Desenha as figuras em SVG da apostila orto-a3 (trilha, causas, salto, caminho do diagnóstico).
Uso: python3 -I figuras.py (na pasta da aula, com a pasta fonts/ copiada pelo preparar.sh)."""
import os
from PIL import ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
W = 478
AZUL, AZUL_CLARO, APOIO, SETA = '#0B5BD3', '#C3D8F8', '#F5F8FF', '#8AA9DF'
TEXTO, TITULO = '#1F2933', '#16315C'
FAM = {'Regular': 'Inter', 'Medium': 'Inter Medium', 'SemiBold': 'Inter SemiBold', 'Bold': 'Inter'}
_cache = {}


def mede(texto, peso, tam):
    chave = (peso, tam)
    if chave not in _cache:
        _cache[chave] = ImageFont.truetype(os.path.join(AQUI, 'fonts', f'Inter-{peso}.ttf'), int(tam * 20))
    return _cache[chave].getlength(texto) / 20


def quebra(texto, peso, tam, larg):
    linhas, atual = [], ''
    for p in texto.split():
        t = (atual + ' ' + p).strip()
        if mede(t, peso, tam) <= larg:
            atual = t
        else:
            linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    return linhas


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def texto(x, y, t, peso='Regular', tam=8, cor=TEXTO, ancora='start'):
    w = ' font-weight="700"' if peso == 'Bold' else ''
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FAM[peso]}"{w} font-size="{tam}" '
            f'fill="{cor}" text-anchor="{ancora}">{esc(t)}</text>')


def bloco(x, y, linhas, peso, tam, cor, ancora='start', entre=1.3):
    out = []
    for i, l in enumerate(linhas):
        out.append(texto(x, y + i * tam * entre, l, peso, tam, cor, ancora))
    return out


def seta_v(x, y0, y1, cor=SETA):
    return (f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1 - 5}" stroke="{cor}" stroke-width="1.6"/>'
            f'<polygon points="{x - 4},{y1 - 6} {x + 4},{y1 - 6} {x},{y1}" fill="{cor}"/>')


def seta_h(x0, x1, y, cor=SETA):
    return (f'<line x1="{x0}" y1="{y}" x2="{x1 - 5}" y2="{y}" stroke="{cor}" stroke-width="1.6"/>'
            f'<polygon points="{x1 - 6},{y - 4} {x1 - 6},{y + 4} {x1},{y}" fill="{cor}"/>')


def svg(nome, h, corpo):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{h}pt" viewBox="0 0 {W} {h}">'
         + ''.join(corpo) + '</svg>')
    open(os.path.join(AQUI, nome), 'w', encoding='utf-8').write(s)


def trilha():
    etapas = [('Anatomia', 'Músculo, tendão, êntese, bursa e bainha'),
              ('Causas', 'Reumáticas, metabólicas e por sobrecarga'),
              ('Diagnóstico', 'História, exame físico e imagem que combine'),
              ('Tratamento', 'Carga, dor e condições para cicatrizar'),
              ('Membro superior', 'Punho, cotovelo e ombro'),
              ('Membro inferior', 'Quadril, joelho e pé')]
    n = len(etapas)
    passo = (W - 20) / n
    larg = passo - 8
    corpo = [f'<rect x="0" y="0" width="{W}" height="112" rx="12" fill="{APOIO}"/>']
    yc = 26
    for i in range(n - 1):
        x0 = 10 + passo * i + passo / 2 + 13
        x1 = 10 + passo * (i + 1) + passo / 2 - 13
        corpo.append(seta_h(x0, x1, yc))
    for i, (t, d) in enumerate(etapas):
        cx = 10 + passo * i + passo / 2
        corpo.append(f'<circle cx="{cx:.1f}" cy="{yc}" r="11" fill="{AZUL}"/>')
        corpo.append(texto(cx, yc + 3.6, str(i + 1), 'SemiBold', 10, '#FFFFFF', 'middle'))
        lt = quebra(t, 'SemiBold', 8.6, larg)
        corpo += bloco(cx, yc + 26, lt, 'SemiBold', 8.6, TITULO, 'middle')
        ld = quebra(d, 'Regular', 7.6, larg)
        corpo += bloco(cx, yc + 28 + len(lt) * 8.6 * 1.3, ld, 'Regular', 7.6, TEXTO, 'middle')
    svg('trilha.svg', 112, corpo)


def causas():
    cols = [('Reumáticas', 'autoimunes',
             'Artrite reumatoide, lúpus e espondilite anquilosante. O corpo ataca a membrana sinovial da articulação e do tendão.'),
            ('Metabólicas', 'microcirculação',
             'Diabetes e tabaco estragam os vasos da ponta da circulação, que são os únicos que o tendão tem.'),
            ('Traumáticas e degenerativas', 'as mais frequentes',
             'Sobrecarga e uso excessivo: esporte, trabalho, salto alto e também a falta de músculo.')]
    gap = 12
    larg = (W - 2 * gap) / 3
    pad = 9
    alturas = []
    blocos = []
    for t, s, d in cols:
        lt = quebra(t, 'SemiBold', 9.4, larg - 2 * pad)
        ld = quebra(d, 'Regular', 8.2, larg - 2 * pad)
        blocos.append((lt, s, ld))
        alturas.append(14 + len(lt) * 12.2 + 12 + 6 + len(ld) * 10.7 + 6)
    hcol = max(alturas)
    corpo = []
    for i, (lt, s, ld) in enumerate(blocos):
        x = i * (larg + gap)
        corpo.append(f'<rect x="{x:.1f}" y="1" width="{larg:.1f}" height="{hcol:.1f}" rx="10" fill="#FFFFFF" stroke="{AZUL_CLARO}" stroke-width="1"/>')
        y = 16
        corpo += bloco(x + pad, y, lt, 'SemiBold', 9.4, TITULO, entre=1.3)
        y += len(lt) * 12.2
        corpo.append(texto(x + pad, y + 1, s.upper(), 'SemiBold', 6.6, AZUL))
        y += 16
        corpo += bloco(x + pad, y, ld, 'Regular', 8.2, TEXTO, entre=1.3)
        corpo.append(seta_v(x + larg / 2, hcol + 2, hcol + 20))
    yb = hcol + 21
    hb = 34
    corpo.append(f'<rect x="0" y="{yb:.1f}" width="{W}" height="{hb}" rx="10" fill="{APOIO}" stroke="{AZUL_CLARO}" stroke-width="1"/>')
    corpo.append(texto(W / 2, yb + 14, 'Tendão, êntese, bursa ou bainha adoecem', 'SemiBold', 9.4, TITULO, 'middle'))
    corpo.append(texto(W / 2, yb + 26, 'dor, inflamação, calcificação ou ruptura', 'Regular', 8.2, TEXTO, 'middle'))
    yd = yb + hb + 10
    corpo.append(f'<rect x="60" y="{yd:.1f}" width="{W - 120}" height="22" rx="10" fill="#FFFFFF" stroke="{SETA}" stroke-width="1" stroke-dasharray="4 3"/>')
    corpo.append(texto(W / 2, yd + 14.5, 'Nenhuma causa achada? Idiopático: o que ainda não se explicou', 'Medium', 8.2, TITULO, 'middle'))
    svg('causas.svg', round(yd + 24), corpo)


def salto():
    linhas = [('Salto de 2 cm', 50, None, '50%', '50%'),
              ('Salto de 4 cm', 57, None, '57%', '43%'),
              ('Salto de 6 cm', 75, None, '75%', '25%'),
              ('Salto de 10 cm', 90, 10, '90 a 100%', '0 a 10%')]
    x0, xb = 0, 86
    lb = W - xb
    corpo = [texto(xb, 10, 'ANTEPÉ (FRENTE DO PÉ)', 'SemiBold', 6.8, AZUL),
             texto(W, 10, 'RETROPÉ (CALCANHAR)', 'SemiBold', 6.8, TITULO, 'end')]
    y = 18
    for nome, a, extra, ta, tr in linhas:
        corpo.append(texto(x0, y + 13, nome, 'Medium', 8.4, TITULO))
        wa = lb * a / 100
        corpo.append(f'<rect x="{xb}" y="{y}" width="{lb}" height="19" rx="5" fill="{AZUL_CLARO}"/>')
        corpo.append(f'<rect x="{xb}" y="{y}" width="{wa:.1f}" height="19" rx="5" fill="{AZUL}"/>')
        if extra:
            corpo.append(f'<rect x="{xb + wa - 5:.1f}" y="{y}" width="{lb * extra / 100 + 5:.1f}" height="19" rx="5" fill="{SETA}"/>')
            corpo.append(f'<rect x="{xb + wa - 5:.1f}" y="{y}" width="6" height="19" fill="{AZUL}"/>')
        corpo.append(texto(xb + 7, y + 13, ta, 'SemiBold', 8.4, '#FFFFFF'))
        if not extra:
            corpo.append(texto(xb + lb - 7, y + 13, tr, 'SemiBold', 8.4, TITULO, 'end'))
        else:
            corpo.append(texto(xb + lb - 4, y + 32, 'retropé: 0 a 10%', 'Medium', 7.4, TITULO, 'end'))
        y += 27
    svg('salto.svg', y + 14, corpo)


def diagnostico():
    passos = [('História', 'Tipo de dor, doenças, remédios e hábitos'),
              ('Exame físico', 'Dirigido à estrutura suspeita'),
              ('Imagem', 'Raio-X, ultrassom ou ressonância'),
              ('Correlação', 'A imagem explica a queixa?'),
              ('Diagnóstico', 'O trabalho do médico'),
              ('Recomendação', 'Quem escolhe é o paciente')]
    n = len(passos)
    gap = 11
    larg = (W - gap * (n - 1)) / n
    pad = 6
    blocos = []
    for t, d in passos:
        lt = quebra(t, 'SemiBold', 8.6, larg - 2 * pad)
        ld = quebra(d, 'Regular', 7.6, larg - 2 * pad)
        blocos.append((lt, ld))
    h = max(14 + len(lt) * 11.2 + 3 + len(ld) * 9.9 for lt, ld in blocos) + 6
    corpo = []
    for i, (lt, ld) in enumerate(blocos):
        x = i * (larg + gap)
        fundo = APOIO if i in (3,) else '#FFFFFF'
        corpo.append(f'<rect x="{x:.1f}" y="1" width="{larg:.1f}" height="{h:.1f}" rx="9" fill="{fundo}" stroke="{AZUL_CLARO}" stroke-width="1"/>')
        y = 15
        corpo += bloco(x + larg / 2, y, lt, 'SemiBold', 8.6, TITULO, 'middle')
        y += len(lt) * 11.2 + 3
        corpo += bloco(x + larg / 2, y, ld, 'Regular', 7.6, TEXTO, 'middle')
        if i < n - 1:
            corpo.append(seta_h(x + larg + 1, x + larg + gap - 0.5, h / 2 + 1))
    svg('diagnostico.svg', round(h + 3), corpo)


if __name__ == '__main__':
    trilha()
    causas()
    salto()
    diagnostico()
