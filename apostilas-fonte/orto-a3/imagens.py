"""Recorta as imagens dos slides (slides.pptx) usadas na apostila orto-a3 e desenha por cima
as setas e os rótulos em português. Uso: python3 -I imagens.py (na pasta da aula)."""
import io, os
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, 'img')
os.makedirs(OUT, exist_ok=True)
AZUL = (11, 91, 211)
ESCURO = (31, 41, 51)
BRANCO = (255, 255, 255)


def fonte(peso, tam):
    return ImageFont.truetype(os.path.join(AQUI, 'fonts', f'Inter-{peso}.ttf'), tam)


def figuras():
    prs = Presentation(os.path.join(AQUI, 'slides.pptx'))
    achadas = {}
    for i, slide in enumerate(prs.slides, 1):
        k = 0
        def walk(shapes):
            for sh in shapes:
                if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
                    yield from walk(sh.shapes)
                else:
                    try:
                        sh.image
                    except Exception:
                        continue
                    yield sh
        for sh in walk(slide.shapes):
            k += 1
            im = Image.open(io.BytesIO(sh.image.blob)).convert('RGB')
            achadas[(i, k)] = (im, (sh.crop_left, sh.crop_top, sh.crop_right, sh.crop_bottom))
    return achadas


def recorte(im, l=0.0, t=0.0, r=0.0, b=0.0):
    w, h = im.size
    return im.crop((int(w * l), int(h * t), int(w * (1 - r)), int(h * (1 - b))))


def amplia(im, fator):
    return im.resize((im.width * fator, im.height * fator), Image.LANCZOS)


def seta(d, x0, y0, x1, y1, cor=BRANCO, larg=6, cab=22):
    import math
    ang = math.atan2(y1 - y0, x1 - x0)
    bx, by = x1 - cab * math.cos(ang), y1 - cab * math.sin(ang)
    d.line([(x0, y0), (bx, by)], fill=cor, width=larg)
    p = [(x1, y1),
         (bx + cab * 0.55 * math.sin(ang), by - cab * 0.55 * math.cos(ang)),
         (bx - cab * 0.55 * math.sin(ang), by + cab * 0.55 * math.cos(ang))]
    d.polygon(p, fill=cor)


def rotulo(d, x, y, texto, tam=30, fundo=AZUL, cor=BRANCO, ancora='la'):
    f = fonte('SemiBold', tam)
    linhas = texto.split('\n')
    larg = max(f.getlength(t) for t in linhas)
    alt = len(linhas) * tam * 1.25
    pad = tam * 0.45
    if ancora == 'ra':
        x = x - larg - 2 * pad
    d.rounded_rectangle([x, y, x + larg + 2 * pad, y + alt + 2 * pad - tam * 0.25], radius=tam * 0.4, fill=fundo)
    for n, t in enumerate(linhas):
        d.text((x + pad, y + pad + n * tam * 1.25), t, font=f, fill=cor)
    return x, y, x + larg + 2 * pad, y + alt + 2 * pad


def apara(im, margem=8, limiar=242):
    """Tira as bordas brancas em volta do desenho."""
    from PIL import ImageOps
    cinza = ImageOps.invert(im.convert('L')).point(lambda v: 255 if v > 255 - limiar else 0)
    caixa = cinza.getbbox()
    if not caixa:
        return im
    l, t, r, b = caixa
    return im.crop((max(0, l - margem), max(0, t - margem), min(im.width, r + margem), min(im.height, b + margem)))


def salva(im, nome, q=90):
    caminho = os.path.join(OUT, nome)
    if nome.endswith('.jpg'):
        im.save(caminho, quality=q)
    else:
        im.save(caminho, optimize=True)


def main():
    F = figuras()
    # Capítulo 01: estrutura do músculo (slide 3) e junções (slide 4)
    salva(F[(3, 1)][0], 'musculo.jpg')
    salva(F[(4, 1)][0], 'juncoes.png')
    # bainha sinovial (slide 5), com o recorte que o slide usa
    im, c = F[(5, 2)]
    salva(recorte(im, c[0], c[1], c[2], 0.10), 'bainha.jpg')
    # Capítulo 02: mão com artrite reumatoide (slide 10, sem a legenda de baixo) e tibial posterior (slide 11)
    im, c = F[(10, 1)]
    salva(recorte(im, *c), 'mao-reumatoide.jpg')
    salva(F[(11, 1)][0], 'tibial-posterior.png')
    # Capítulo 03: ressonância do calcâneo (slide 16)
    salva(F[(16, 1)][0], 'ressonancia-calcaneo.jpg', 95)
    # Capítulo 05
    salva(F[(23, 1)][0], 'compartimentos-punho.jpg', 95)
    salva(apara(F[(25, 1)][0]), 'ortese-polegar.png')
    im, c = F[(28, 1)]
    salva(recorte(im, *c), 'ortese-cotovelo.png')
    salva(apara(F[(29, 1)][0]), 'bursas-cotovelo.png')
    salva(F[(30, 1)][0], 'bursite-olecraniana.jpg')
    # radiografia do cotovelo (slide 31): troca os rótulos em espanhol e tira o logotipo
    im = amplia(F[(31, 2)][0], 3)
    w, h = im.size
    d = ImageDraw.Draw(im)
    for (l, t, r, b) in [(0.69, 0.45, 0.90, 0.548), (0.21, 0.83, 0.43, 0.93)]:
        d.rectangle([w * l, h * t, w * r, h * b], fill=(0, 0, 0))
    # logotipo: cada linha recebe a cor do pixel logo à esquerda dele
    xl = int(w * 0.765)
    for y in range(int(h * 0.775), h):
        d.line([(xl, y), (w, y)], fill=im.getpixel((xl - 3, y)))
    rotulo(d, w * 0.985, h * 0.40, 'Calcificação na\ninserção do tríceps', tam=34, ancora='ra')
    rotulo(d, w * 0.095, h * 0.615, 'Olécrano', tam=38, fundo=ESCURO)
    rotulo(d, w * 0.03, h * 0.855, 'Bursa olecraniana aumentada', tam=34)
    salva(im, 'radiografia-cotovelo.jpg', 92)
    salva(F[(32, 2)][0], 'radiografia-ombro.jpg', 90)
    # Capítulo 06: bursas do quadril (slide 34), sem os rótulos em inglês, com margem para os nossos
    orig = F[(34, 1)][0].copy()
    W0, H0 = orig.size
    d0 = ImageDraw.Draw(orig)
    papel = orig.getpixel((int(W0 * 0.30), int(H0 * 0.47)))
    d0.rectangle([W0 * 0.18, H0 * 0.525, W0 * 0.222, H0 * 0.57], fill=papel)
    L, T, R, B = 0.185, 0.0, 0.20, 0.16
    im = amplia(recorte(orig, L, T, R, B), 2)
    marg = 360
    tela = Image.new('RGB', (im.width + marg, im.height), BRANCO)
    tela.paste(im, (marg, 0))
    d = ImageDraw.Draw(tela)
    def pos(fx, fy):
        return marg + (fx - L) * W0 * 2, fy * H0 * 2
    alvo_ilio = pos(0.226, 0.547)
    alvo_tro = pos(0.20, 0.70)
    x0, y0, x1, y1 = rotulo(d, 10, alvo_ilio[1] - 210, 'Bursa do\niliopsoas', tam=46)
    seta(d, x1 - 40, y1, alvo_ilio[0], alvo_ilio[1], cor=AZUL, larg=6, cab=24)
    x0, y0, x1, y1 = rotulo(d, 10, alvo_tro[1] - 30, 'Bursa\ntrocantérica', tam=46)
    seta(d, x1, (y0 + y1) / 2, alvo_tro[0] + 8, alvo_tro[1] + 20, cor=AZUL, larg=6, cab=24)
    salva(tela, 'bursas-quadril.jpg', 92)
    salva(apara(F[(36, 1)][0]), 'bursas-joelho.png')
    salva(F[(35, 1)][0], 'bursite-prepatelar.png')
    # radiografias do calcâneo (slide 38)
    im = amplia(F[(38, 1)][0], 3)
    w, h = im.size
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = rotulo(d, w * 0.03, h * 0.08, 'Calcificação na\ninserção do Aquiles', tam=30)
    seta(d, (x0 + x1) / 2 - 30, y1 + 6, w * 0.16, h * 0.45, larg=6, cab=24)
    salva(im, 'radiografia-aquiles.jpg', 92)
    im = amplia(F[(38, 2)][0], 2)
    w, h = im.size
    d = ImageDraw.Draw(im)
    rotulo(d, w * 0.30, h * 0.80, 'Esporão de calcâneo', tam=26)
    salva(im, 'radiografia-esporao.jpg', 92)


if __name__ == '__main__':
    main()
