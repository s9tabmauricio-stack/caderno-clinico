# Gera as figuras da apostila pneumo-a5 em fig/ (SVG nossos + imagens com setas e rótulos)
import os, math, html
from PIL import Image, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(AQUI, 'fig'); os.makedirs(FIG, exist_ok=True)
FONTES = {400: '/usr/share/fonts/opentype/inter/Inter-Regular.otf', 500: '/usr/share/fonts/opentype/inter/Inter-Medium.otf',
          600: '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 700: '/usr/share/fonts/opentype/inter/Inter-Bold.otf'}
_f = {k: ImageFont.truetype(v, 100) for k, v in FONTES.items()}
NAVY, AZUL, CLARO, APOIO, SETA, TXT = '#16315C', '#0B5BD3', '#C3D8F8', '#F5F8FF', '#8AA9DF', '#1F2933'
ROXO, ROXO_F, ROXO_B = '#6E3AA7', '#F4EBFB', '#DEC7F1'

def tw(t, s, w=400): return _f[w].getlength(t) * s / 100
def wrap(t, s, maxw, w=400):
    out = []
    for par in t.split('\n'):
        linha = ''
        for p in par.split(' '):
            n = (linha + ' ' + p).strip()
            if tw(n, s, w) <= maxw or not linha: linha = n
            else: out.append(linha); linha = p
        out.append(linha)
    return out
def e(t): return html.escape(t, quote=True)

class SVG:
    def __init__(s, W, H): s.W, s.H, s.el = W, H, []
    def add(s, x): s.el.append(x)
    def rect(s, x, y, w, h, fill='#FFFFFF', stroke=None, sw=1, rx=6, dash=None, op=None):
        a = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
        if dash: a += f' stroke-dasharray="{dash}"'
        if op: a += f' fill-opacity="{op}"'
        s.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{a}/>')
    def text(s, x, y, t, size=8, w=400, fill=TXT, anchor='start', ls=None):
        a = f' letter-spacing="{ls}"' if ls else ''
        s.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}"{a}>{e(t)}</text>')
    def lines(s, x, y, ls, size=8, w=400, fill=TXT, anchor='start', lh=1.3):
        for i, l in enumerate(ls): s.text(x, y + i * size * lh, l, size, w, fill, anchor)
    def line(s, x1, y1, x2, y2, stroke=SETA, sw=1.2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        s.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d} stroke-linecap="round"/>')
    def circle(s, x, y, r, fill, stroke=None, sw=1):
        a = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
        s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}"{a}/>')
    def poly(s, pts, fill, stroke=None, sw=1):
        a = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ''
        s.add(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}"{a}/>')
    def path(s, d, fill='none', stroke=SETA, sw=1.2, dash=None):
        a = f' stroke-dasharray="{dash}"' if dash else ''
        s.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{a} stroke-linecap="round" stroke-linejoin="round"/>')
    def image(s, href, x, y, w, h):
        s.add(f'<image href="{href}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" preserveAspectRatio="none"/>')
    def save(s, nome):
        open(os.path.join(FIG, nome), 'w', encoding='utf-8').write(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{s.W}" height="{s.H:.0f}" viewBox="0 0 {s.W} {s.H:.0f}">\n' + '\n'.join(s.el) + '\n</svg>\n')

def seta_pts(x1, y1, x2, y2, w=1.5, hl=6.5, hw=5.2):
    d = math.hypot(x2 - x1, y2 - y1) or 1
    ux, uy = (x2 - x1) / d, (y2 - y1) / d; px, py = -uy, ux
    bx, by = x2 - ux * hl, y2 - uy * hl
    return [(x1 + px * w / 2, y1 + py * w / 2), (bx + px * w / 2, by + py * w / 2), (bx + px * hw, by + py * hw), (x2, y2),
            (bx - px * hw, by - py * hw), (bx - px * w / 2, by - py * w / 2), (x1 - px * w / 2, y1 - py * w / 2)]
def seta(s, x1, y1, x2, y2, cor=SETA, w=1.5, hl=6.5, hw=5.2):
    s.poly(seta_pts(x1, y1, x2, y2, w, hl, hw), cor)

def borda(cx, cy, w, h, tx, ty):
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0: return cx, cy
    k = min((w / 2) / abs(dx) if dx else 1e9, (h / 2) / abs(dy) if dy else 1e9)
    return cx + dx * k, cy + dy * k

def caixa(s, cx, cy, w, h, texto, estilo='b', size=7.6, peso=None, prova=False):
    st = {'b': ('#FFFFFF', CLARO, TXT, 400), 'h': ('#E8F0FE', CLARO, NAVY, 600), 'd': (NAVY, NAVY, '#FFFFFF', 600),
          'q': (APOIO, SETA, NAVY, 600), 'n': ('#FFFFFF', '#E3E3E8', '#4A4A4F', 400), 'p': (ROXO_F, ROXO_B, ROXO, 400)}[estilo]
    peso = peso or st[3]
    x, y = cx - w / 2, cy - h / 2
    s.rect(x, y, w, h, st[0], st[1], 1, 6, dash='3 2' if estilo in ('q', 'n', 'p') else None)
    ls = wrap(texto, size, w - 12, peso)
    lh = size * 1.28; y0 = cy - (len(ls) - 1) * lh / 2 + size * 0.35
    if prova:
        y0 += 5
        tag(s, x + 22, y - 1)
    s.lines(cx, y0, ls, size, peso, st[2], 'middle', 1.28)
    return (cx, cy, w, h)

def tag(s, cx, y):
    w = tw('PROVA', 5.6, 600) + 1.6 * 4 + 9
    s.rect(cx - w / 2, y - 5, w, 10, '#1F2933', rx=3)
    s.text(cx, y + 2.1, 'PROVA', 5.6, 600, '#FFFFFF', 'middle', ls='1.6')

def liga(s, a, b, lado_a='b', lado_b='t', rot=None, cor=SETA, dash=None):
    def pt(c, l):
        cx, cy, w, h = c
        return {'b': (cx, cy + h / 2), 't': (cx, cy - h / 2), 'l': (cx - w / 2, cy), 'r': (cx + w / 2, cy)}[l]
    x1, y1 = pt(a, lado_a); x2, y2 = pt(b, lado_b)
    if dash:
        s.line(x1, y1, x2 - (x2 - x1) * 0.02, y2 - 6 if lado_b == 't' else y2, cor, 1.2, dash)
        seta(s, x2 - (x2 - x1) * 0.001, y2 - 6.5 if lado_b == 't' else y2, x2, y2, cor)
    else:
        seta(s, x1, y1, x2, y2, cor)
    if rot:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        wv = tw(rot, 6.8, 600) + 8
        s.rect(mx - wv / 2, my - 6, wv, 11, '#FFFFFF', rx=4)
        s.text(mx, my + 2.3, rot, 6.8, 600, AZUL, 'middle')

# ---------------------------------------------------------------- imagens com setas
def prep(src, nome, maxw=1500, crop=None):
    im = Image.open(src).convert('RGB')
    if crop:
        W0, H0 = im.size; im = im.crop((int(crop[0] * W0), int(crop[1] * H0), int(crop[2] * W0), int(crop[3] * H0)))
    im.thumbnail((maxw, maxw * 2))
    ext = '.png' if src.endswith('.png') and 'imagens-gpt' in src else '.jpg'
    out = nome + ext
    if ext == '.jpg': im.save(os.path.join(FIG, out), quality=88)
    else: im.save(os.path.join(FIG, out), optimize=True)
    return out, im.size[0] / im.size[1]

def figura(nome, paineis, W=478, hmax=270, gap=10, pad=(0, 0, 0, 0), estilo='rx', size=7.2):
    """paineis: dict(src, tag, rot=[(texto, lx, ly, tx, ty, tipo)], maxw) em coordenadas 0-1 da imagem do painel."""
    pt, pr, pb, pl = pad
    imgs = [prep(p['src'], nome + f'-{i}', crop=p.get('crop')) for i, p in enumerate(paineis)]
    disp = W - pl - pr - gap * (len(paineis) - 1)
    h = min(hmax, disp / sum(ar for _, ar in imgs))
    tot = h * sum(ar for _, ar in imgs) + gap * (len(paineis) - 1)
    x = pl + (W - pl - pr - tot) / 2
    s = SVG(W, pt + h + pb)
    caixas = []
    for (href, ar), p in zip(imgs, paineis):
        w = h * ar
        s.image(href, x, pt, w, h)
        if p.get('tag'):
            s.rect(x + 4, pt + 4, 14, 14, NAVY, rx=4); s.text(x + 11, pt + 14.2, p['tag'], 8, 600, '#FFFFFF', 'middle')
        for r in p.get('rot', []):
            texto, lx, ly, tx, ty = r[:5]; tipo = r[5] if len(r) > 5 else 'n'
            c = p.get('crop')
            if c:
                lx, ly = (lx - c[0]) / (c[2] - c[0]), (ly - c[1]) / (c[3] - c[1])
                if tx is not None: tx, ty = (tx - c[0]) / (c[2] - c[0]), (ty - c[1]) / (c[3] - c[1])
            mw = r[6] if len(r) > 6 else 118
            ls = wrap(texto, size, mw, 600)
            bw = max(tw(l, size, 600) for l in ls) + 9; bh = len(ls) * size * 1.25 + 5
            if len(r) > 7 and r[7]: bw = max(bw, r[7][0] * w); bh = max(bh, r[7][1] * h)
            cx, cy = x + lx * w, pt + ly * h
            cx = min(max(cx, bw / 2 + 1), W - bw / 2 - 1); cy = min(max(cy, bh / 2 + 1), pt + h + pb - bh / 2 - 1)
            caixas.append((cx, cy, bw, bh, ls, tipo, None if tx is None else (x + tx * w, pt + ty * h)))
        x += w + gap
    # setas primeiro, caixas por cima
    for cx, cy, bw, bh, ls, tipo, alvo in caixas:
        if alvo is None: continue
        ax, ay = alvo
        sx, sy = borda(cx, cy, bw + 2, bh + 2, ax, ay)
        if estilo == 'rx':
            s.poly(seta_pts(sx, sy, ax, ay, 1.6, 6.5, 5), '#FFFFFF', '#FFFFFF', 2.2)
            s.poly(seta_pts(sx, sy, ax, ay, 1.6, 6.5, 5), '#0A84FF')
        else:
            cor = ROXO if tipo == 'p' else NAVY
            s.line(sx, sy, ax, ay, cor, 0.8); s.circle(ax, ay, 2, cor, '#FFFFFF', 0.8)
    for cx, cy, bw, bh, ls, tipo, alvo in caixas:
        fill, stroke, cor = ('#FFFFFF', CLARO, NAVY) if tipo != 'p' else (ROXO_F, ROXO_B, ROXO)
        if tipo == 't': fill, stroke, cor = ('#FFFFFF', '#FFFFFF', NAVY)
        s.rect(cx - bw / 2, cy - bh / 2, bw, bh, fill, stroke, 0.8, 3.5)
        s.lines(cx, cy - (len(ls) - 1) * size * 1.25 / 2 + size * 0.36, ls, size, 600, cor, 'middle', 1.25)
    s.save(nome + '.svg')
    return pt + h + pb

SL = os.path.join(AQUI, 'slides-img'); GP = os.path.join(AQUI, 'imagens-gpt')
def sl(n): return os.path.join(SL, n)
def gp(n): return os.path.join(GP, n)

# --- exames: radiografias, tomografias e ultrassom (slides)
figura('ex-parabola', [
    dict(src=sl('p11-rx-derrame-volumoso-parabola.png'), tag='A', rot=[
        ('1 · Borda curva do líquido', 0.36, 0.20, 0.715, 0.44),
        ('2 · Base toda branca: líquido', 0.66, 0.90, 0.76, 0.66)]),
    dict(src=sl('p12-rx-derrame-pequeno.png'), tag='B', rot=[
        ('3 · Seio apagado', 0.66, 0.66, 0.875, 0.905),
        ('4 · Seio pontudo', 0.28, 0.70, 0.095, 0.915)])])
figura('ex-decubito', [
    dict(src=sl('p13-rx-decubito-lateral-liquido-livre.png'), tag='A', rot=[
        ('1 · Lado de baixo: líquido junto à parede', 0.40, 0.20, 0.10, 0.42, 'n', 90),
        ('2 · Borda do pulmão', 0.50, 0.78, 0.25, 0.62, 'n', 80)]),
    dict(src=sl('p14a-rx-imagem-em-d-perfil.png'), tag='B', rot=[
        ('3 · Imagem em D', 0.72, 0.32, 0.455, 0.50)]),
    dict(src=sl('p14b-rx-imagem-em-d-pa.png'), tag='C', rot=[
        ('4 · Borda convexa: líquido preso', 0.62, 0.80, 0.32, 0.62, 'n', 90)])], hmax=230)
figura('ex-infra', [
    dict(src=sl('p15a-rx-infrapulmonar-pa.png'), tag='A', rot=[
        ('1 · Parece o diafragma: é o topo do líquido', 0.30, 0.52, 0.25, 0.685, 'n', 100),
        ('2 · Onde está o diafragma', 0.52, 0.95, 0.30, 0.805, 'n', 100),
        ('3 · Diafragma esquerdo: compare a altura', 0.76, 0.66, 0.75, 0.875, 'n', 90)]),
    dict(src=sl('p15b-rx-infrapulmonar-perfil.png'), tag='B', rot=[
        ('4 · Seio de trás apagado', 0.56, 0.86, 0.38, 0.70, 'n', 70)])], W=330, hmax=250, size=6.9)
figura('ex-intercisural', [
    dict(src=sl('p16a-rx-intercisural-lente.png'), tag='A', rot=[
        ('1 · Líquido em forma de lente na cissura', 0.50, 0.12, 0.50, 0.36, 'n', 90)]),
    dict(src=sl('p16b-rx-intercisural-pa.png'), tag='B', rot=[
        ('2 · Parece tumor: é líquido na cissura horizontal', 0.58, 0.12, 0.22, 0.60, 'n', 100)])], W=290, hmax=260)
figura('ex-tc-us', [
    dict(src=sl('p17a-tc-lojas-empiema.png'), tag='A', rot=[
        ('Frente', 0.50, 0.04, None, None, 't'), ('Costas', 0.50, 0.95, None, None, 't'),
        ('1 · Líquido preso na frente', 0.30, 0.20, 0.80, 0.33, 'n', 70),
        ('2 · Pleura grossa, realçada', 0.27, 0.78, 0.69, 0.71, 'n', 70)]),
    dict(src=sl('p17b-us-septos-lojas.png'), tag='B', rot=[
        ('Parede do tórax', 0.50, 0.07, None, None, 't'),
        ('3 · Líquido: preto', 0.25, 0.27, 0.22, 0.42),
        ('4 · Traves: lojas', 0.80, 0.30, 0.57, 0.53)])], hmax=210)
figura('ex-ptx-rx', [
    dict(src=sl('p36-rx-pneumotorax.png'), tag='A', rot=[
        ('1 · Linha pleural', 0.44, 0.88, 0.165, 0.62),
        ('2 · Só ar: sem trama', 0.50, 0.08, 0.21, 0.20),
        ('3 · Pulmão com trama', 0.62, 0.50, 0.30, 0.52, 'n', 70)]),
    dict(src=sl('p37-rx-pneumotorax-extenso.png'), tag='B', rot=[
        ('4 · Câmara de ar grande, sem trama', 0.785, 0.365, None, None, 'n', 140, (0.42, 0.085)),
        ('5 · Linha pleural', 0.63, 0.56, None, None, 'n', 140, (0.47, 0.09)),
        ('6 · Mediastino um pouco empurrado', 0.70, 0.86, 0.60, 0.70, 'n', 90)])], hmax=260)
figura('ex-ptx-tc', [
    dict(src=sl('p38-tc-pneumotorax.png'), tag='A', rot=[
        ('Frente', 0.30, 0.05, None, None, 't'),
        ('1 · Ar na frente do pulmão', 0.64, 0.10, 0.76, 0.25, 'n', 90),
        ('2 · Borda do pulmão', 0.50, 0.42, 0.68, 0.36, 'n', 70),
        ('3 · Provável dreno', 0.83, 0.72, 0.875, 0.515, 'n', 60)]),
    dict(src=sl('p39-tc-pneumotorax-enfisema-subcutaneo.png'), tag='B', rot=[
        ('4 · Ar sob a pele: enfisema subcutâneo', 0.20, 0.06, 0.16, 0.26, 'n', 90),
        ('5 · Pneumotórax', 0.28, 0.88, 0.33, 0.43, 'n', 80),
        ('6 · Ar no mediastino', 0.78, 0.16, 0.595, 0.31, 'n', 70)])], hmax=210)

# --- ilustrações do GPT, com rótulos nossos
figura('il-pleura', [dict(src=gp('img-pleura-anatomia.png'), rot=[
    ('Fissura horizontal', 0.13, 0.30, 0.15, 0.415),
    ('Fissura oblíqua', 0.10, 0.62, 0.15, 0.555),
    ('Seio costofrênico', -0.02, 1.03, 0.048, 0.84),
    ('Coração no mediastino, entre as duas cavidades', 0.40, 1.03, 0.34, 0.66, 'n', 200),
    ('Diafragma', 0.21, 0.895, 0.20, 0.80),
    ('Pulmão esquerdo: 2 lobos', 0.465, 0.30, 0.45, 0.40, 'n', 70),
    ('Costela', 0.585, 0.04, 0.68, 0.40),
    ('Pleura parietal', 0.73, 0.04, 0.752, 0.33),
    ('Líquido pleural', 0.91, 0.04, 0.78, 0.28),
    ('Pleura visceral', 0.74, 0.80, 0.798, 0.58),
    ('Pulmão (alvéolos)', 0.90, 0.84, 0.90, 0.68)])], estilo='il', hmax=250, pad=(0, 0, 20, 0))
figura('il-derrame-ptx', [dict(src=gp('img-derrame-e-pneumotorax.png'), crop=(0, 0.10, 1, 0.89), rot=[
    ('Derrame pleural', 0.25, 0.08, None, None, 't'),
    ('Pneumotórax', 0.75, 0.08, None, None, 't'),
    ('Líquido na base', 0.12, 0.95, 0.12, 0.72),
    ('Percussão: maciça', 0.33, 0.95, None, None, 'n'),
    ('Pulmão empurrado para cima', 0.12, 0.20, 0.16, 0.40, 'n', 80),
    ('Ar (sem vasos)', 0.58, 0.16, 0.60, 0.30),
    ('Borda do pulmão: linha pleural', 0.60, 0.95, 0.588, 0.62, 'n', 90),
    ('Percussão: timpânica', 0.83, 0.95, None, None, 'n')])], estilo='il', hmax=300)
figura('il-toracocentese', [dict(src=gp('img-toracocentese.png'), rot=[
    ('Costela', 0.615, 0.035, 0.775, 0.16),
    ('Vasos e nervo: na borda de baixo da costela de cima', 0.86, 0.06, 0.79, 0.268, 'p', 120),
    ('Ponto da punção: abaixo da ponta da escápula, na linha do meio dela', 0.36, 0.70, 0.330, 0.530, 'p', 105),
    ('Líquido do derrame', 0.935, 0.24, 0.85, 0.33, 'n', 60),
    ('Pleura visceral', 0.94, 0.60, 0.866, 0.56, 'n', 60),
    ('Pele e gordura', 0.60, 0.80, 0.69, 0.56),
    ('Agulha longe dos vasos, mais perto da costela de baixo', 0.81, 0.80, 0.80, 0.451, 'p', 110),
    ('Músculo entre as costelas', 0.66, 0.93, 0.745, 0.60, 'n', 80),
    ('Pleura parietal: anestesiar bem (dói)', 0.88, 0.93, 0.808, 0.64, 'n', 110),
    ('Frascos para os exames do líquido', 0.13, 0.72, 0.13, 0.85, 'n', 90)])], estilo='il', hmax=300)
figura('il-dreno', [dict(src=gp('img-dreno-selo-dagua.png'), rot=[
    ('Dreno de tórax entre as costelas', 0.20, 0.13, 0.322, 0.345, 'n', 90),
    ('Um frasco só', 0.20, 0.88, 0.40, 0.85),
    ('Frasco sempre abaixo do tórax', 0.20, 0.97, 0.37, 0.92, 'p', 140),
    ('Tubo do paciente: ponta embaixo da água (selo d\'água)', 0.61, 0.45, 0.738, 0.672, 'n', 85),
    ('Cerca de 2 cm abaixo da água', 0.61, 0.62, 0.738, 0.655, 'p', 75),
    ('Respiro: tubo curto, aberto', 0.92, 0.34, 0.80, 0.215, 'n', 70),
    ('Bolhas: o ar que sai do tórax', 0.92, 0.55, 0.768, 0.69, 'n', 70)])], estilo='il', hmax=258)
figura('il-bolhas', [dict(src=gp('img-bolhas-apicais.png'), crop=(0, 0, 1, 0.89), rot=[
    ('Antes: bolha rompida', 0.24, 0.035, None, None, 't'),
    ('Cirurgia por vídeo', 0.76, 0.035, None, None, 't'),
    ('Bolhas no ápice, sob a pleura', 0.10, 0.25, 0.25, 0.37, 'n', 80),
    ('Ar escapando para a pleura', 0.42, 0.14, 0.35, 0.29, 'n', 80),
    ('Pulmão', 0.24, 0.72, None, None, 'n'),
    ('Câmera', 0.60, 0.20, 0.66, 0.37),
    ('Grampeador abaixo das bolhas', 0.66, 0.66, 0.80, 0.47, 'n', 80),
    ('Parte retirada', 0.93, 0.22, 0.86, 0.36),
    ('Orifício pequeno entre as costelas', 0.55, 0.88, 0.575, 0.53, 'n', 90)])], estilo='il', hmax=250)

# ---------------------------------------------------------------- trilha da aula
def trilha():
    s = SVG(478, 136)
    nomes = ['Pleura normal', 'Por que junta líquido', 'Sintomas e exame físico', 'Imagem', 'Punção e Light',
             'Empiema e dreno', 'Tuberculose e câncer']
    y = 22; xs = [36 + i * 67.6 for i in range(7)]
    s.add(f'<rect x="{xs[0]:.1f}" y="{y - 2.5}" width="{xs[-1] - xs[0]:.1f}" height="5" rx="2.5" fill="{CLARO}"/>')
    # ramo do pneumotórax: sai entre as etapas 3 e 4
    bx = (xs[2] + xs[3]) / 2
    s.path(f'M{bx:.1f},{y} L{bx:.1f},{y + 80} L{bx + 26:.1f},{y + 80}', stroke=SETA, sw=1.6, dash='4 3')
    for i, x in enumerate(xs):
        s.circle(x, y, 11, AZUL); s.text(x, y + 3.6, str(i + 1), 9, 700, '#FFFFFF', 'middle')
        s.lines(x, y + 24, wrap(nomes[i], 7.6, 62, 600), 7.6, 600, NAVY, 'middle', 1.25)
    px = bx + 38
    s.circle(px, y + 80, 11, '#FFFFFF', AZUL, 1.6); s.text(px, y + 83.6, '8', 9, 700, AZUL, 'middle')
    s.text(px + 18, y + 77, 'Pneumotórax (ramo ao lado)', 8.4, 700, NAVY)
    s.lines(px + 18, y + 89, wrap('Ar em vez de líquido: mesmo exame físico, outra imagem, outro tratamento.', 7.4, 478 - px - 22), 7.4, 400, '#4A4A4F')
    s.save('trilha.svg')
trilha()

# ---------------------------------------------------------------- 02 pressões
def selo(s, x, y, n):
    s.circle(x, y, 7, AZUL); s.text(x, y + 2.6, str(n), 7.2, 700, '#FFFFFF', 'middle')
def pressoes():
    s = SVG(478, 244)
    cols = [(0, 154, 'Parede do tórax', 'capilar da pleura parietal'), (163, 152, 'Espaço pleural', 'onde o líquido fica'),
            (330, 148, 'Pulmão', 'capilar da pleura visceral')]
    for x, w, t, sub in cols:
        s.rect(x, 0, w, 198, APOIO if t != 'Espaço pleural' else '#E8F0FE', CLARO, 1, 9)
        s.text(x + w / 2, 15, t, 8.6, 700, NAVY, 'middle'); s.text(x + w / 2, 26, sub, 7, 400, '#6C6C70', 'middle')
    # linha 1: empurra para fora
    s.text(74, 48, '35', 15, 700, NAVY, 'middle'); s.lines(74, 66, ['empurra o líquido', 'para fora'], 7.2, 400, TXT, 'middle')
    seta(s, 112, 58, 205, 58, SETA, 2.2, 8, 6); selo(s, 128, 48, 1)
    s.lines(239, 55, ['entra líquido'], 7.2, 600, NAVY, 'middle')
    # linha 2: proteínas puxam de volta
    s.text(74, 116, '29', 15, 700, NAVY, 'middle'); s.lines(74, 128, ['as proteínas puxam', 'de volta'], 7.2, 400, TXT, 'middle')
    seta(s, 205, 120, 112, 120, SETA, 2.2, 8, 6); selo(s, 128, 110, 2)
    s.lines(239, 117, ['volta para o vaso'], 7.2, 600, NAVY, 'middle')
    # linha 3: linfa
    s.rect(12, 152, 124, 30, '#FFFFFF', CLARO, 1, 7)
    s.lines(74, 164, ['vaso linfático', 'leva o que sobra'], 7.2, 400, TXT, 'middle')
    seta(s, 205, 167, 138, 167, SETA, 2.2, 8, 6); selo(s, 152, 157, 3)
    s.lines(239, 164, ['sobram cerca de 6:', 'saem pela linfa'], 7.2, 600, NAVY, 'middle')
    # pulmão
    s.lines(404, 60, ['empurra 29', 'puxa 29'], 8, 600, NAVY, 'middle')
    seta(s, 368, 84, 300, 84, SETA, 1.8, 7, 5); seta(s, 300, 96, 368, 96, SETA, 1.8, 7, 5)
    s.text(404, 92, 'saldo: zero', 7.6, 700, NAVY, 'middle')
    selo(s, 404, 126, 4)
    s.lines(404, 144, ['inflamação abre a', 'membrana: passam', 'proteínas e células'], 7.2, 400, TXT, 'middle')
    s.lines(0, 214, wrap('Números do slide 4, em centímetros de água. Os selos marcam onde age cada mecanismo: 1 mais pressão no vaso, 2 menos proteína no sangue, 3 linfa entupida, 4 pleura inflamada.', 7.4, 478), 7.4, 400, '#6C6C70')
    s.save('pressoes.svg')
pressoes()

# ---------------------------------------------------------------- 06 fases
def fases():
    s = SVG(478, 160)
    titulos = [('1 · Exsudativa', 'Líquido ainda fino, junto com a pneumonia.'),
               ('2 · Fibrinopurulenta', 'Traves de fibrina e pus dividem o líquido em lojas.'),
               ('3 · Organização', 'Fibrose: pleura grossa que prende o pulmão (paquipleuris).')]
    for i in range(3):
        x = i * 164; w = 150
        s.rect(x, 30, w, 12, '#DCDCE2', rx=3)                      # parede
        s.line(x, 44, x + w, 44, '#9AA5B5', 1.4)                  # pleura parietal
        s.rect(x, 86, w, 26, CLARO, rx=3)                        # pulmão
        if i == 0:
            s.rect(x, 45, w, 40, '#E3EEFD', rx=0)
        elif i == 1:
            s.rect(x, 45, w, 40, '#E3EEFD', rx=0)
            for k in range(6):
                xx = x + 14 + k * 24
                s.path(f'M{xx},{45} C{xx + 8},{58} {xx - 6},{70} {xx + 4},{85}', stroke='#7F9CC9', sw=1.3)
            for (dx, dy) in [(22, 58), (60, 70), (98, 55), (128, 72), (44, 76)]:
                s.circle(x + dx, dy, 2.2, '#B9C3D3')
        else:
            s.rect(x, 45, w, 13, '#A9B8D0', rx=0); s.rect(x, 73, w, 13, '#A9B8D0', rx=0)
            s.rect(x, 58, w, 15, '#E3EEFD', rx=0)
            for k in range(5):
                s.line(x + 15 + k * 30, 58, x + 15 + k * 30, 73, '#7F9CC9', 1.3)
        s.line(x, 86, x + w, 86, NAVY, 1.4)                       # pleura visceral
        s.text(x + w / 2, 100, 'pulmão', 7, 400, NAVY, 'middle')
        s.text(x + 2, 126, titulos[i][0], 8.6, 700, NAVY)
        s.lines(x + 2, 138, wrap(titulos[i][1], 7.6, w - 4), 7.6, 400, TXT)
        if i < 2: seta(s, x + w + 2, 65, x + 162, 65, SETA, 1.6, 6, 4.5)
    # faixa: tratar até a fase 2
    s.path('M2,22 L2,14 L312,14 L312,22', stroke=AZUL, sw=1.2)
    s.text(157, 9, 'Tratar aqui, no máximo aqui', 7.8, 700, AZUL, 'middle')
    s.text(0, 40, '', 6)
    s.save('fases.svg')
fases()

# ---------------------------------------------------------------- 06 fluxograma do parapneumônico (PROVA)
def fluxo_pp():
    s = SVG(478, 372)
    L, M, R = 72, 238, 404
    a = caixa(s, 239, 14, 220, 26, 'Pneumonia com derrame pleural', 'h', 8.2)
    b = caixa(s, L, 66, 144, 44, 'Derrame menor que 10 mm (coluna menor que 1 cm, deitado de lado)', 'b', 7.4)
    c = caixa(s, R, 66, 148, 30, 'Derrame maior que 10 mm', 'b', 7.6)
    d = caixa(s, L, 130, 144, 44, 'Não punciona: trata a pneumonia e repete a radiografia', 'b', 7.4)
    e_ = caixa(s, R, 130, 148, 30, 'Toracocentese', 'h', 8.2)
    liga(s, a, b, 'b', 't'); liga(s, a, c, 'b', 't'); liga(s, b, d); liga(s, c, e_)
    liga(s, d, e_, 'r', 'l', 'cresceu')
    f = caixa(s, M, 214, 158, 64, 'Turvo ou pus · Gram ou cultura com bactéria · pH abaixo de 7,2', 'q', 7.8, prova=True)
    g = caixa(s, R, 214, 148, 64, 'Pouco líquido, claro, sem bactéria e pH de 7,2 ou mais', 'b', 7.4)
    liga(s, e_, f, 'b', 't', 'qualquer um'); liga(s, e_, g, 'b', 't', 'nenhum')
    h = caixa(s, M, 290, 158, 34, 'Drenagem fechada: dreno em selo d\'água', 'd', 7.8)
    i = caixa(s, R, 290, 148, 44, 'Esvazia, mantém o antibiótico e reavalia; voltou: nova punção', 'b', 7.2)
    liga(s, f, h); liga(s, g, i); liga(s, i, h, 'l', 'r', 'piorou')
    j = caixa(s, M, 350, 158, 38, 'Sem resposta: cirurgia (vídeo ou aberta, decorticação)', 'd', 7.4)
    liga(s, h, j)
    caixa(s, L, 290, 144, 34, 'Fibrinolítico: pouco usado aqui', 'n', 7.2)
    caixa(s, R, 350, 148, 30, 'Melhorou: segue o tratamento', 'n', 7.2)
    liga(s, i, (R, 350, 148, 30), 'b', 't')
    s.save('fluxo-parapneumonico.svg')
fluxo_pp()

# ---------------------------------------------------------------- 07 fluxograma do derrame neoplásico
def fluxo_neo():
    s = SVG(478, 290)
    L, M, R = 76, 239, 400
    a = caixa(s, M, 14, 230, 26, 'Câncer conhecido com derrame pleural', 'h', 8.2)
    b = caixa(s, M, 54, 230, 30, 'Toracocentese de alívio (guiada por ultrassom)', 'b', 7.6)
    c = caixa(s, M, 96, 200, 28, 'A falta de ar melhorou?', 'q', 8)
    liga(s, a, b); liga(s, b, c)
    d = caixa(s, L, 146, 150, 36, 'Não: procurar outra causa da falta de ar', 'b', 7.4)
    e_ = caixa(s, R, 146, 156, 36, 'Sim: o pulmão reexpandiu? (exame de imagem)', 'q', 7.6)
    liga(s, c, d, 'l', 't', 'não'); liga(s, c, e_, 'r', 't', 'sim')
    f = caixa(s, M, 200, 168, 36, 'Reexpandiu: quanto tempo de vida se espera?', 'q', 7.6)
    g = caixa(s, R + 2, 214, 152, 64, 'Não reexpandiu (slide): cateter pleural tunelizado se viver mais de 1 semana; se não, punções, oxigênio ou morfina', 'n', 6.9)
    liga(s, e_, f, 'b', 't', 'sim'); liga(s, e_, g, 'b', 't', 'não')
    h = caixa(s, L, 264, 150, 46, 'Pouco tempo (1 a 2 meses): toracocentese a cada 15 a 20 dias', 'b', 7.2)
    i = caixa(s, M + 10, 264, 150, 46, 'Bom tempo (1 a 2 anos): pleurodese com talco ou iodopovidona', 'd', 7.2)
    liga(s, f, h, 'b', 't'); liga(s, f, i, 'b', 't')
    s.save('fluxo-neoplasico.svg')
fluxo_neo()

# ---------------------------------------------------------------- 08 ponto P (PROVA)
def ponto_p():
    s = SVG(478, 196)
    x0, x1 = 6, 300
    s.text(x0, 10, 'Transdutor passando pela parede do tórax', 7.6, 600, '#6C6C70')
    s.rect(x0, 50, x1 - x0, 18, '#E9EAF0', rx=3)                 # parede
    for k in range(6):
        s.add(f'<ellipse cx="{x0 + 24 + k * 49}" cy="59" rx="15" ry="6" fill="#D1D5DE"/>')
    s.line(x0, 70, x1, 70, '#9AA5B5', 1.6)                        # pleura parietal
    pp = 170
    d = f'M{x0},{112} C{x0 + 70},{110} {pp - 50},{96} {pp},{72} L{x1},{72} L{x1},{150} L{x0},{150} Z'
    s.path(f'M{x0},71 L{x1},71 L{x1},72 L{pp},72 C{pp - 50},96 {x0 + 70},110 {x0},112 Z', fill='#F2F4F8', stroke='none')
    s.path(d, fill=CLARO, stroke='none')
    s.path(f'M{x0},{112} C{x0 + 70},{110} {pp - 50},{96} {pp},{72} L{x1},{72}', stroke=NAVY, sw=1.6)
    s.text(70, 90, 'ar', 8, 600, '#6C6C70', 'middle')
    s.text(150, 132, 'pulmão', 8, 600, NAVY, 'middle')
    for (x, l) in [(62, 'A'), (pp, 'B'), (250, 'C')]:
        s.rect(x - 13, 30, 26, 18, NAVY, rx=5); s.text(x, 43, l, 9, 700, '#FFFFFF', 'middle')
        s.line(x, 30, x, 18, NAVY, 1.4)
    seta(s, 96, 24, 214, 24, SETA, 1.4, 6, 4.5)
    s.line(pp, 72, pp, 160, AZUL, 1, '3 2'); s.text(pp, 170, 'ponto P', 8, 700, AZUL, 'middle')
    for k in range(3):                                           # marcas de deslizamento
        xx = 214 + k * 30
        seta(s, xx, 80, xx + 12, 80, AZUL, 1, 4, 3); seta(s, xx + 12, 84, xx, 84, AZUL, 1, 4, 3)
    s.text(254, 98, 'desliza', 7.4, 600, AZUL, 'middle')
    # cartões
    cards = [('A', 'Sem deslizamento', 'Há ar entre as pleuras: forte sinal de pneumotórax.'),
             ('B', 'Ponto P', 'O lugar onde o deslizamento volta a aparecer.'),
             ('C', 'Deslizamento normal', 'Pulmão encostado na parede, deslizando a cada respiração.')]
    y = 4
    for l, t, txt in cards:
        s.rect(314, y, 164, 44, '#FFFFFF', CLARO, 1, 7)
        s.rect(320, y + 7, 15, 15, NAVY, rx=4); s.text(327.5, y + 18, l, 8, 700, '#FFFFFF', 'middle')
        s.text(341, y + 17.5, t, 8.2, 700, NAVY)
        s.lines(320, y + 31, wrap(txt, 7.2, 152), 7.2, 400, TXT, 'start', 1.25)
        y += 50
    s.rect(314, y, 164, 36, '#1F2933', rx=7)
    s.lines(396, y + 14, ['Ausência de deslizamento', '+ ponto P = pneumotórax'], 7.8, 600, '#FFFFFF', 'middle', 1.3)
    s.save('ponto-p.svg')
ponto_p()

# ---------------------------------------------------------------- 08 tratamento do pneumotórax
def fluxo_ptx():
    s = SVG(478, 300)
    L, M, R = 76, 239, 400
    a = caixa(s, M, 14, 220, 26, 'Pneumotórax confirmado na imagem', 'h', 8.2)
    b = caixa(s, M, 60, 250, 30, 'O paciente está instável (insuficiência respiratória)?', 'q', 7.8)
    liga(s, a, b)
    c = caixa(s, L, 116, 150, 40, 'Sim: dreno sempre, qualquer tamanho', 'd', 7.6)
    d = caixa(s, R, 116, 156, 40, 'Não: depende do tamanho', 'q', 7.8)
    liga(s, b, c, 'l', 't', 'sim'); liga(s, b, d, 'r', 't', 'não')
    e_ = caixa(s, M, 184, 156, 66, 'Menos de 20% do hemitórax: observar com radiografias, oxigênio alto; aspiração por cateter (pouco usada)', 'b', 7.1)
    f = caixa(s, R, 184, 156, 54, 'Mais de 20%: drenagem fechada em um selo d\'água (um frasco)', 'd', 7.4)
    liga(s, d, e_, 'b', 't', 'pequeno'); liga(s, d, f, 'b', 't', 'grande')
    g = caixa(s, 318, 262, 316, 40, 'Qualquer dreno que não resolveu: chame o cirurgião (segundo dreno, aspiração contínua, dreno mais calibroso)', 'b', 7.2)
    liga(s, f, g, 'b', 't')
    caixa(s, L, 210, 150, 46, 'Bolhas no ápice de um jovem: cirurgia direto (vídeo com grampeador)', 'n', 7.1)
    s.save('fluxo-pneumotorax.svg')
fluxo_ptx()
print('figuras em', FIG, ':', len(os.listdir(FIG)))
