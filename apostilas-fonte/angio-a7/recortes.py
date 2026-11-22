#!/usr/bin/env python3
"""Recorta as fotos dos slides usadas na apostila angio-a7 e desenha os selos numerados.

Rodar na pasta de trabalho, com o PDF dos slides ao lado: python3 -I recortes.py
Saída: slide-necrotizante.jpg (slide 7 da fonte) e slide-linfedema.jpg (slide 9).
Os selos (círculo azul-marinho com o número) são nossos; o texto do "O que olhar"
fica no HTML.
"""
from pathlib import Path

import pdfplumber
from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent
SLIDES = AQUI / "slides.pdf"
FONTE = AQUI / "fonts" / "Inter-SemiBold.ttf"
MARINHO = (22, 49, 92)

# nome: (página do PDF, caixa em pt, resolução, recorte em px (esq, topo, dir, base), selos)
FOTOS = {
    "slide-necrotizante.jpg": (7, (57, 590, 287, 719), 480, (10, 10, 1522, 720),
                               [(1, 150, 400), (2, 760, 250)]),
    "slide-linfedema.jpg": (9, (175, 390, 268, 483), 780, (6, 6, 1000, 930),
                            [(1, 700, 560), (2, 255, 520)]),
}


def selo(desenho, x, y, n, raio):
    desenho.ellipse((x - raio, y - raio, x + raio, y + raio), fill=MARINHO,
                    outline=(255, 255, 255), width=max(2, raio // 6))
    fonte = ImageFont.truetype(str(FONTE), int(raio * 1.25))
    desenho.text((x, y), str(n), font=fonte, fill=(255, 255, 255), anchor="mm")


def main():
    pdf = pdfplumber.open(SLIDES)
    for nome, (pag, caixa, res, corte, selos) in FOTOS.items():
        img = pdf.pages[pag - 1].crop(caixa).to_image(resolution=res).original.convert("RGB")
        img = img.crop(corte)
        raio = max(18, img.width // 34)
        desenho = ImageDraw.Draw(img)
        for n, x, y in selos:
            selo(desenho, x, y, n, raio)
        img.save(AQUI / nome, quality=86)
        print(nome, img.size)


if __name__ == "__main__":
    main()
