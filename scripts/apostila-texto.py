#!/usr/bin/env python3
"""Texto de uma apostila em PDF, página por página, para fazer flashcards e questões.

Uso: python3 -I scripts/apostila-texto.py public/apostilas/<aula-id>/apostila.pdf [--paginas 5-8,15,16]

Com --paginas, só as páginas pedidas (para a conferência em blocos ler só o seu pedaço).

Usa o pdfplumber porque o pdftotext perde os selos brancos "PROVA" (que aparecem
no fim do título da seção, ex.: "Regra de Goodsall PROVA") e os títulos espaçados
dos quadros ("COMPLEMENTO: FORA DA AULA", "PARÊNTESE DO PROFESSOR", "ARMADILHA").
Sem o pdfplumber, cai no pdftotext.
"""
import subprocess
import sys

caminho = sys.argv[1]
paginas = None
if '--paginas' in sys.argv:
    paginas = set()
    for parte in sys.argv[sys.argv.index('--paginas') + 1].split(','):
        ini, _, fim = parte.partition('-')
        paginas.update(range(int(ini), int(fim or ini) + 1))
try:
    import pdfplumber
except ImportError:
    sys.stderr.write('pdfplumber ausente: usando pdftotext (os selos PROVA podem sumir)\n')
    sys.stdout.write(subprocess.run(['pdftotext', caminho, '-'], capture_output=True, text=True, check=True).stdout)
    sys.exit()

with pdfplumber.open(caminho) as pdf:
    for n, pagina in enumerate(pdf.pages, 1):
        if paginas and n not in paginas:
            continue
        print(f'\n===== página {n} de {len(pdf.pages)} =====')
        print(pagina.extract_text() or '')
