# arquivo: checar.py
# uso: python3 checar.py "Disciplina - Aula N - Professor - Tema.pdf" apostila.html
# Checagem automática antes de entregar: fontes, rodapé, marcadores do PDF, marcadores {{ }}
# esquecidos, siglas e datas (dia da semana) no texto. Salva o texto do PDF em texto.txt
# (para comparar com a fonte) e as páginas em espelho na pasta paginas/ (para olhar com Read).
import os, re, sys, html, datetime, pdfplumber, pypdfium2 as pdfium
from PIL import Image
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.utils import decode_text

pdf_path, html_path = sys.argv[1], sys.argv[2]
avisos = []
pdf = pdfplumber.open(pdf_path)
pags = pdf.pages

# 1. fontes: só Inter (o Inter-Oblique sintético das citações é esperado)
fontes = sorted({re.sub(r'^[A-Z]{6}\+', '', c['fontname']) for p in pags for c in p.chars})
print('Fontes:', ', '.join(fontes))
fora = [f for f in fontes if not f.lower().startswith('inter')]
if fora:
    avisos.append('fonte fora do padrão: ' + ', '.join(fora))

# 2. rodapé: nenhum na capa, um em cada página seguinte, sempre numa linha só
for i, p in enumerate(pags, 1):
    rod = [c for c in p.chars if c['top'] > 795 and c['x0'] < p.width * 0.75]
    if i == 1:
        if rod:
            avisos.append('a capa tem rodapé')
        continue
    if not rod:
        avisos.append(f'página {i} sem rodapé')
        continue
    tops = sorted(c['top'] for c in rod)
    if sum(1 for a, b in zip(tops, tops[1:]) if b - a > 4):
        avisos.append(f'rodapé em mais de uma linha na página {i}: encurte o título curto')
if len(pags) > 1:
    print('Rodapé:', (pags[1].crop((0, 795, pags[1].width, pags[1].height)).extract_text() or '').strip())

# 3. marcadores do PDF (sem "PROVA" no nome)
with open(pdf_path, 'rb') as f:
    try:
        marc = [(n, decode_text(t) if isinstance(t, bytes) else str(t))
                for n, t, *_ in PDFDocument(PDFParser(f)).get_outlines()]
    except Exception:
        marc = []
print('Marcadores:', ' | '.join(('  ' * (n - 1)) + t for n, t in marc) or 'nenhum')
if any('PROVA' in t for _, t in marc):
    avisos.append('marcador com "PROVA" no nome: use data-bm no h3')

# 4. texto do PDF em texto.txt + marcadores {{ }} esquecidos
texto = ''.join(f'\n=== página {i} ===\n' + (p.extract_text() or '') for i, p in enumerate(pags, 1))
open('texto.txt', 'w', encoding='utf-8').write(texto)
if '{{' in texto:
    avisos.append('sobrou marcador {{ }} no PDF')

# 5. siglas e datas, lidas do HTML (o PDF tem rótulos em caixa alta que confundiriam)
fonte = open(html_path, encoding='utf-8').read()
fonte = re.sub(r'(?s)<head>.*?</head>|<style.*?</style>|<script.*?</script>|\{\{.*?\}\}', ' ', fonte)
corrido = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', fonte)))
siglas = {}
for s in re.findall(r'\b[A-ZÀ-Ý]{2,}\b', corrido):
    if s not in ('PROVA', 'PROEX') and not re.fullmatch(r'[IVXLC]+', s):
        siglas[s] = siglas.get(s, 0) + 1
print('Siglas para revisar:', ', '.join(f'{s} ({n}x)' for s, n in sorted(siglas.items())) or 'nenhuma')

MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto',
         'setembro', 'outubro', 'novembro', 'dezembro']
NOMES = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']
mes = '(' + '|'.join(MESES) + ')'
achadas = []   # (início, fim, data, ano presumido?)
for m in re.finditer(r'\b(\d{1,2})º? de ' + mes + r' de (\d{4})', corrido, re.I):
    achadas.append((m.start(), m.end(), datetime.date(int(m[3]), MESES.index(m[2].lower()) + 1, int(m[1])), False))
for m in re.finditer(r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b', corrido):
    achadas.append((m.start(), m.end(), datetime.date(int(m[3]), int(m[2]), int(m[1])), False))
ano = min((a[2].year for a in achadas), default=datetime.date.today().year)
for m in re.finditer(r'\b' + mes + r' (\d{1,2})\b(?! de \d)', corrido, re.I):   # cartão da data da prova
    achadas.append((m.start(), m.end(), datetime.date(ano, MESES.index(m[1].lower()) + 1, int(m[2])), True))
print('Datas:' if achadas else 'Datas: nenhuma')
dia = r'\b(?:segunda|terça|quarta|quinta|sexta)-feira\b|\bsábado\b|\bdomingo\b'
for ini, fim, d, presumido in sorted(achadas):
    certo = NOMES[d.weekday()]
    antes = corrido[max(0, ini - 40):ini]
    perto = [(m.start(), m[0]) for m in re.finditer(dia, corrido[fim:fim + 60], re.I)]      # logo depois
    perto += [(len(antes) - m.end(), m[0]) for m in re.finditer(dia, antes, re.I)]          # logo antes
    citado = min(perto)[1].lower() if perto else None   # o dia da semana mais próximo da data
    nota = f'  {d.strftime("%d/%m/%Y")} é {certo}' + (' (ano presumido)' if presumido else '')
    if citado and citado != certo:
        nota += f'  <- o texto diz "{citado}"'
        avisos.append(f'dia da semana errado: {d.strftime("%d/%m/%Y")} é {certo}, o texto diz {citado}')
    print(nota + ('  · confere' if citado == certo else ''))

# 6. páginas em espelho (capa sozinha, depois pares) na pasta paginas/
os.makedirs('paginas', exist_ok=True)
for f in os.listdir('paginas'):
    if f.startswith('pag-') and f.endswith('.png'):
        os.remove(os.path.join('paginas', f))
doc = pdfium.PdfDocument(pdf_path)
imgs = [doc[i].render(scale=82 / 72).to_pil() for i in range(len(doc))]
grupos = [[0]] + [list(range(i, min(i + 2, len(imgs)))) for i in range(1, len(imgs), 2)]
nomes = []
for g in grupos:
    folha = Image.new('RGB', (sum(imgs[i].width for i in g) + 14 * (len(g) - 1), max(imgs[i].height for i in g)), '#8E8E93')
    x = 0
    for i in g:
        folha.paste(imgs[i], (x, 0))
        x += imgs[i].width + 14
    nome = f'paginas/pag-{g[0] + 1:02d}' + (f'-{g[-1] + 1:02d}' if len(g) > 1 else '') + '.png'
    folha.save(nome)
    nomes.append(nome)
print('Imagens para olhar uma a uma:', ' '.join(nomes))
print('Texto do PDF salvo em texto.txt')

print('\nAvisos:' if avisos else '\nNenhum aviso automático.', *('\n  - ' + a for a in avisos))
print('Falta o olhar humano: imagens das páginas, cores contra a tabela e conteúdo contra a fonte.')
