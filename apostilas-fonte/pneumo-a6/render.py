# arquivo: render.py
# uso: python3 render.py apostila.html "Disciplina - Aula N - Professor - Tema.pdf"
# Gera o PDF em duas passagens (páginas do sumário + área de anotações na última página)
# e mede o espaço livre no pé de cada página. Rodar de novo depois de cada ajuste.
import os, re, sys, html, logging, weasyprint, pdfplumber
logging.getLogger('weasyprint').setLevel(logging.ERROR)
LIMITE = 90        # pt livres aceitos no pé de cada página (a última não conta)
MAX_LINHAS = 26    # linhas da área de anotações, no máximo

src_path, out_path = sys.argv[1], sys.argv[2]
base = os.path.dirname(os.path.abspath(src_path))
src = open(src_path, encoding='utf-8').read()

# rodapé: texto do <meta name="rodape"> no <head>; a capa fica sem rodapé
m = re.search(r'<meta\s+name="rodape"\s+content="([^"]+)"', src)
if not m:
    sys.exit('Falta no <head>: <meta name="rodape" content="Mauricio Faria · Disciplina · Aula N — título curto">')
rod = html.unescape(m.group(1)).replace('\\', '\\\\').replace('"', '\\"')
estilo = ('<style>@page { @bottom-left { content: "%s"; } } '
          '@page cover { @bottom-left { content: none; } }</style>' % rod)
src = src.replace('</head>', estilo + '\n</head>', 1) if '</head>' in src else estilo + src
if '{{NOTAS}}' not in src:
    print('AVISO: falta o marcador {{NOTAS}} no fim da última seção')

def notas(n):
    return '' if n <= 0 else ('<div class="notes"><div class="kick">Anotações</div>'
                              + '<div class="line"></div>' * n + '</div>')
def montar(n, paginas=None):
    h = src.replace('{{NOTAS}}', notas(n))
    return re.sub(r'\{\{(s\d\d)\}\}', lambda x: str((paginas or {}).get(x.group(1), 0)), h)
def render(h):
    return weasyprint.HTML(string=h, base_url=base).render()

# maior área de anotações que cabe sem criar página nova (busca binária: poucas passagens)
total = len(render(montar(0)).pages)
lo, hi = 0, MAX_LINHAS
while lo < hi:
    mid = (lo + hi + 1) // 2
    if len(render(montar(mid)).pages) == total:
        lo = mid
    else:
        hi = mid - 1
doc = render(montar(lo))
paginas = {}
for i, p in enumerate(doc.pages):
    for a in p.anchors:
        paginas.setdefault(a, i + 1)
faltam = sorted(set(re.findall(r'\{\{(s\d\d)\}\}', src)) - set(paginas))
if faltam:
    print('AVISO: o sumário cita seções sem id correspondente:', ', '.join(faltam))
doc = render(montar(lo, paginas))
doc.write_pdf(out_path)
print(f'{out_path}: {len(doc.pages)} páginas | {lo} linhas de anotação')

# espaço livre no pé de cada página (sem a capa e sem a última)
def linhas(p, de_baixo=False):
    t = [l for l in (p.crop((0, 0, p.width, 791)).extract_text() or '').splitlines() if l.strip()]
    return t[-2:] if de_baixo else t[:2]
with pdfplumber.open(out_path) as pdf:
    pags, livres, buracos = pdf.pages, [], []
    for i in range(1, len(pags) - 1):
        p = pags[i]
        ys = [o['bottom'] for o in p.chars + p.rects + p.curves + p.lines if o['bottom'] < 790]
        livre = round(791 - max(ys)) if ys else 700
        livres.append(f'{i + 1}:{livre}' + ('!' if livre > LIMITE else ''))
        if livre > LIMITE:
            buracos.append((i, livre))
    print('Espaço livre no pé (pt; ! = acima de %d):' % LIMITE, ' '.join(livres) or '—')
    for i, livre in buracos:
        print(f'\nPágina {i + 1}: {livre} pt livres')
        print('  termina com:   ', ' / '.join(linhas(pags[i], True)))
        print(f'  página {i + 2} começa:', ' / '.join(linhas(pags[i + 1])))
    if not buracos:
        print('Nenhum buraco acima do limite.')
