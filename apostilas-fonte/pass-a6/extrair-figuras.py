"""Extrai as imagens usadas na apostila, sem recriar os dados dos gráficos.

Uso: python extrair-figuras.py arquivo.pptx pasta-temporaria
Requer python-pptx, PyMuPDF, Pillow e LibreOffice. Não grava o PPTX no Git.
"""
from pathlib import Path
from io import BytesIO
import subprocess
import sys
import fitz
from PIL import Image
from pptx import Presentation

source = Path(sys.argv[1]).resolve()
temp = Path(sys.argv[2]).resolve()
temp.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parent
slides = Presentation(source).slides


def picture(slide, index=0):
    pictures = [shape for shape in slides[slide-1].shapes if shape.shape_type == 13]
    return Image.open(BytesIO(pictures[index].image.blob)).convert("RGB")


for number, filename in [(19, "curvas-ensaio.png"), (33, "metanalise-cirurgia.png"),
                         (36, "floresta-exemplo-a.png"), (37, "floresta-exemplo-b.png"),
                         (38, "floresta-exemplo-c.png")]:
    picture(number).save(root / filename, optimize=True)
curves = picture(19)
curves.crop((0, 0, 1624, 662)).save(root / "curvas-ensaio-ab.png", optimize=True)
curves.crop((0, 662, 1624, 1288)).save(root / "curvas-ensaio-cd.png", optimize=True)

subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(temp), str(source)], check=True)
with fitz.open(temp / (source.stem + ".pdf")) as doc:
    for number, filename, bounds in [
        (22, "subgrupos.png", (115, 100, 1410, 762)),
        (35, "vies-estudos.png", (60, 25, 1415, 835)),
        (40, "analise-combinada.png", (180, 25, 1390, 815)),
    ]:
        pix = doc[number-1].get_pixmap(matrix=fitz.Matrix(1.6, 1.6))
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        im.crop(bounds).save(root / filename, optimize=True)
