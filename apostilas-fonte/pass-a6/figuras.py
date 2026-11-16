"""Gera os esquemas da aula. Uso: python figuras.py /tmp/pass-a6/fonts."""
from pathlib import Path
from html import escape
import sys
from PIL import ImageFont

ROOT = Path(__file__).resolve().parent
FONTS = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "fonts"


def text(x, y, value, size=11, bold=False, anchor="middle", color="#1F2933"):
    family = "Inter-SemiBold.ttf" if bold else "Inter-Regular.ttf"
    font = ImageFont.truetype(str(FONTS / family), size * 4)
    assert font.getlength(value) / 4 < 468, value
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Inter" font-size="{size}" font-weight="{600 if bold else 400}" fill="{color}">{escape(value)}</text>'


def rect(x, y, w, h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="#FFFFFF" stroke="#C3D8F8"/>'


def arrow(x, y, length=16):
    return f'<path d="M{x} {y}v{length-3}" stroke="#8AA9DF" stroke-width="1.5"/><polygon points="{x-3},{y+length-4} {x+3},{y+length-4} {x},{y+length}" fill="#8AA9DF"/>'


def save(name, height, parts):
    (ROOT / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="478pt" height="{height}pt" viewBox="0 0 478 {height}"><rect width="478" height="{height}" rx="12" fill="#F5F8FF"/>' + ''.join(parts) + '</svg>')


labels = ["Estrutura", "Método", "Desfechos", "Resultados", "Crítica", "Metanálise", "Diretrizes"]
parts = []
for i, label in enumerate(labels):
    x = 5 + i * 67
    parts += [rect(x, 9, 64, 53), text(x+32, 28, f"0{i+1}", 12, True, color="#0B5BD3"), text(x+32, 48, label, 7)]
parts += [text(239, 83, "Da pergunta do estudo à recomendação clínica", 10, True, color="#16315C")]
save("trilha.svg", 98, parts)

stages = [
    ("10.521 pessoas", "entraram na fase inicial de tolerabilidade"),
    ("10.513 receberam enalapril", "8 receberam apenas sacubitril/valsartana"),
    ("9.419 receberam sacubitril/valsartana", "após a etapa com enalapril"),
    ("8.442 foram sorteadas", "43 excluídas por randomização inválida ou falhas dos centros"),
    ("8.399 na análise", "4.187: sacubitril/valsartana; 4.212: enalapril"),
]
parts=[]
for i,(title,sub) in enumerate(stages):
    y=6+i*42
    parts += [rect(10,y,458,34),text(239,y+15,title,10,True,color="#16315C"),text(239,y+28,sub,7)]
    if i<4:parts.append(arrow(239,y+34,7))
save("fluxo-ensaio.svg", 212, parts)

stages=[("1. Pergunta", "Qual população, comparação e desfecho?"),
        ("2. Busca", "Onde e até quando procurar estudos?"),
        ("3. Triagem", "Quais trabalhos cumprem os critérios?"),
        ("4. Extração", "Quais dados e medidas entram?"),
        ("5. Análise", "Como combinar as estimativas?"),
        ("6. Heterogeneidade", "Quanto os resultados variam?"),
        ("7. Gráfico de floresta", "Qual é o efeito e sua incerteza?"),
        ("8. Viés de publicação", "Quais resultados podem ter ficado ausentes?")]
parts=[]
for i,(title,sub) in enumerate(stages):
    col=i//4;row=i%4;x=8+col*237;y=8+row*50
    parts += [rect(x,y,225,38),text(x+112.5,y+15,title,10,True,color="#16315C"),text(x+112.5,y+30,sub,7.2)]
    if row<3:parts.append(arrow(x+112.5,y+38,10))
save("fluxo-metanalise.svg", 208, parts)
