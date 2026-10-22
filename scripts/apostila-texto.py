#!/usr/bin/env python3
"""Texto de uma apostila em PDF, página por página, para fazer flashcards e questões.

Uso: python3 -I scripts/apostila-texto.py public/apostilas/<aula-id>/apostila.pdf

Usa o pdfplumber porque o pdftotext perde os selos brancos "PROVA" (que aparecem
no fim do título da seção, ex.: "Regra de Goodsall PROVA") e os títulos espaçados
dos quadros ("COMPLEMENTO: FORA DA AULA", "PARÊNTESE DO PROFESSOR", "ARMADILHA").
Sem o pdfplumber, cai no pdftotext.
"""
import subprocess
import sys

caminho = sys.argv[1]
try:
    import pdfplumber
except ImportError:
    sys.stderr.write('pdfplumber ausente: usando pdftotext (os selos PROVA podem sumir)\n')
    sys.stdout.write(subprocess.run(['pdftotext', caminho, '-'], capture_output=True, text=True, check=True).stdout)
    sys.exit()

with pdfplumber.open(caminho) as pdf:
    for n, pagina in enumerate(pdf.pages, 1):
        print(f'\n===== página {n} de {len(pdf.pages)} =====')
        print(pagina.extract_text() or '')
