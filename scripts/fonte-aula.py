#!/usr/bin/env python3
"""Fonte da aula: a transcrição e os slides guardados num arquivo só, no Git.

Regra do Mauricio (09/11/2026): cada aula tem um arquivo fonte. A apostila, as
questões e os flashcards saem dele, e as conferências também são feitas por ele.
O arquivo fica em apostilas-fonte/<aula-id>/fonte.md, com o texto como veio
(sem corrigir os erros da transcrição automática: quem corrige é a apostila).

Guardar (a transcrição e os slides que o Mauricio mandou):
  python3 -I scripts/fonte-aula.py guardar <aula-id> --transcricao <arq> [--slides <arq>]
  Pode repetir --transcricao (aula em partes) e --slides. Transcrição: .txt, .md,
  .srt, .vtt, .docx ou .pdf. Slides: .pdf ou .pptx. Texto colado na conversa:
  salve num .txt antes. Se a aula já tem fonte, use --acrescentar para juntar o
  que chegou depois (ex.: os slides); material igual ao que já está é pulado.

Ler um pedaço (para a conferência em blocos não ler a aula inteira):
  python3 -I scripts/fonte-aula.py trecho <aula-id> [--minutos 10-35] [--parte 1] [--slides 4-9,12]
  --minutos: só as falas desse intervalo (minutos, ou 1:05:00-1:20:00); --parte:
  só aquela parte da transcrição; --slides: só aquelas páginas. Sem nada, tudo.

Os slides originais (PDF/PPTX) não entram no Git (pesam): vão para a pasta da
aula no Drive (MEDGENIUS → 2 - Aulas). Página de slide sem texto (só imagem)
fica marcada no arquivo, para quem conferir saber que precisa olhar o original.
"""
import argparse
import datetime
import hashlib
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / 'apostilas-fonte'
MARCA_PARTE = re.compile(r'^<!-- parte (transcricao|slides) (\d+) \| (.*) -->$')
MARCA_SLIDE = re.compile(r'^<!-- slide (\d+) -->$')
TITULO_PARTE = re.compile(r'^## (Transcrição|Slides) \d+ · ')
TEMPO = re.compile(r'^\s*[\[(]?((?:\d{1,2}:)?\d{1,2}:\d{2})(?:[.,]\d+)?[\])]?')


def parar(msg):
    sys.stderr.write(f'PAROU: {msg}\n')
    sys.exit(1)


def numero(n):
    return f'{n:,}'.replace(',', '.')


def segundos(texto):
    partes = [int(p) for p in texto.split(':')]
    while len(partes) < 3:
        partes.insert(0, 0)
    h, m, s = partes
    return h * 3600 + m * 60 + s


def hms(s):
    return f'{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}'


def modulo(nome, pacote):
    """Importa um pacote; se faltar, instala (como o transcrever.py)."""
    try:
        return __import__(nome)
    except ImportError:
        sys.stderr.write(f'instalando {pacote}...\n')
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--break-system-packages', '-q', pacote], check=True)
        return __import__(nome)


def paginas_pdf(caminho):
    """Texto de cada página de um PDF: pdfplumber, senão pypdf, senão pdftotext."""
    try:
        import pdfplumber
        with pdfplumber.open(caminho) as pdf:
            return [(p.extract_text() or '') for p in pdf.pages]
    except ImportError:
        pass
    try:
        import pypdf
        return [(p.extract_text() or '') for p in pypdf.PdfReader(str(caminho)).pages]
    except ImportError:
        pass
    saida = subprocess.run(['pdftotext', '-layout', str(caminho), '-'], capture_output=True, text=True, check=True).stdout
    return saida.split('\f')[:-1] if saida.endswith('\f') else saida.split('\f')


def ler_transcricao(caminho):
    sufixo = caminho.suffix.lower()
    if sufixo in ('.txt', '.md', ''):
        return caminho.read_text(encoding='utf-8', errors='replace')
    if sufixo in ('.srt', '.vtt'):
        linhas, tempo = [], None
        for linha in caminho.read_text(encoding='utf-8', errors='replace').splitlines():
            linha = linha.strip()
            achou = re.match(r'^((?:\d{1,2}:)?\d{1,2}:\d{2})[.,]\d+\s*-->', linha)
            if achou:
                tempo = hms(segundos(achou.group(1)))
            elif linha and not linha.isdigit() and linha != 'WEBVTT' and tempo:
                linhas.append(f'[{tempo}] {linha}')
        return '\n'.join(linhas)
    if sufixo == '.docx':
        docx = modulo('docx', 'python-docx')
        return '\n'.join(p.text for p in docx.Document(str(caminho)).paragraphs)
    if sufixo == '.pdf':
        return '\n'.join(paginas_pdf(caminho))
    parar(f'{caminho.name}: transcrição em formato que este programa não lê ({sufixo}). Use .txt, .md, .srt, .vtt, .docx ou .pdf.')


def ler_slides(caminho):
    sufixo = caminho.suffix.lower()
    if sufixo == '.pdf':
        return paginas_pdf(caminho)
    if sufixo == '.pptx':
        pptx = modulo('pptx', 'python-pptx')
        slides = []
        for slide in pptx.Presentation(str(caminho)).slides:
            textos = []
            for forma in slide.shapes:
                if getattr(forma, 'has_text_frame', False) and forma.text_frame.text.strip():
                    textos.append(forma.text_frame.text.strip())
                if getattr(forma, 'has_table', False):
                    for linha in forma.table.rows:
                        textos.append(' | '.join(c.text.strip() for c in linha.cells))
            if slide.has_notes_slide and slide.notes_slide.notes_text_frame.text.strip():
                textos.append('Notas: ' + slide.notes_slide.notes_text_frame.text.strip())
            slides.append('\n'.join(textos))
        return slides
    parar(f'{caminho.name}: slides em formato que este programa não lê ({sufixo}). Use .pdf ou .pptx (no PowerPoint, "Salvar como PDF").')


def limpar(texto):
    texto = texto.replace('\r\n', '\n').replace('\r', '\n').replace('\x00', '')
    # Uma linha do material igual a uma marca nossa estragaria a leitura do arquivo.
    linhas = [(' ' + l) if (MARCA_PARTE.match(l) or MARCA_SLIDE.match(l) or TITULO_PARTE.match(l)) else l for l in texto.split('\n')]
    return '\n'.join(linhas).strip('\n')


def ler_partes(arquivo):
    """Partes de um fonte.md: lista de dicts (tipo, n, meta, corpo)."""
    partes, atual = [], None
    for linha in arquivo.read_text(encoding='utf-8').split('\n'):
        achou = MARCA_PARTE.match(linha)
        if achou:
            meta = dict(item.split('=', 1) for item in achou.group(3).split(' | ') if '=' in item)
            atual = {'tipo': achou.group(1), 'n': int(achou.group(2)), 'meta': meta, 'linhas': []}
            partes.append(atual)
            continue
        if atual is not None:
            atual['linhas'].append(linha)
    for parte in partes:
        linhas = parte.pop('linhas')
        # o título visível da parte seguinte ("## Slides 1 · ...") fica no fim desta: tira
        while linhas and (not linhas[-1].strip() or TITULO_PARTE.match(linhas[-1])):
            linhas.pop()
        parte['corpo'] = '\n'.join(linhas).strip('\n')
    return partes


def escrever(aula, partes, destino):
    hoje = datetime.date.today().strftime('%d/%m/%Y')
    cab = [
        f'# Fonte da aula · {aula}',
        '',
        f'Guardada com `scripts/fonte-aula.py` (última mudança em {hoje}). É o material da aula como veio, sem correção:',
        'os erros da transcrição automática ficam aqui e quem corrige é a apostila. A apostila, as questões, os flashcards',
        'e as conferências saem deste arquivo; onde ele e a apostila divergem, vale o que o professor falou (AGENTS.md).',
        'Não edite à mão: para juntar material novo, rode o programa com --acrescentar.',
        '',
        '## O que tem aqui',
        '',
    ]
    for p in partes:
        m = p['meta']
        if p['tipo'] == 'transcricao':
            extra = f", duração até {m['duracao']}" if m.get('duracao') else ', sem marcação de tempo'
            cab.append(f"- Transcrição {p['n']}: `{m.get('arquivo', '?')}` ({m.get('palavras', '?')} palavras{extra}).")
        else:
            so_img = m.get('so_imagem', '')
            aviso = f'; só imagem, sem texto: {so_img} (ver o original no Drive)' if so_img else ''
            cab.append(f"- Slides {p['n']}: `{m.get('arquivo', '?')}` ({m.get('paginas', '?')} páginas{aviso}).")
    corpo = []
    for p in partes:
        meta = ' | '.join(f'{k}={v}' for k, v in p['meta'].items())
        titulo = 'Transcrição' if p['tipo'] == 'transcricao' else 'Slides'
        corpo += ['', f"## {titulo} {p['n']} · {p['meta'].get('arquivo', '')}", f"<!-- parte {p['tipo']} {p['n']} | {meta} -->", '', p['corpo']]
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text('\n'.join(cab + corpo).rstrip('\n') + '\n', encoding='utf-8', newline='\n')


def guardar(a):
    if not re.fullmatch(r'[a-z]+-a\d+', a.aula):
        parar(f'id de aula fora do padrão: {a.aula} (ex.: pneumo-a7)')
    if not a.transcricao and not a.slides:
        parar('nada para guardar: passe --transcricao e/ou --slides')
    destino = PASTA / a.aula / 'fonte.md'
    partes = []
    if destino.exists():
        if not a.acrescentar:
            parar(f'{destino.relative_to(RAIZ)} já existe. Para juntar material novo, rode de novo com --acrescentar; para refazer do zero, apague o arquivo antes.')
        partes = ler_partes(destino)
    ja_tem = {p['meta'].get('sha') for p in partes}
    novos = []
    for tipo, lista in (('transcricao', a.transcricao), ('slides', a.slides)):
        for nome in lista:
            caminho = Path(nome)
            if not caminho.is_file():
                parar(f'arquivo não encontrado: {nome}')
            sha = hashlib.sha256(caminho.read_bytes()).hexdigest()[:12]
            if sha in ja_tem:
                print(f'pulado (já está na fonte): {caminho.name}')
                continue
            ja_tem.add(sha)
            n = 1 + max([p['n'] for p in partes if p['tipo'] == tipo], default=0)
            meta = {'arquivo': caminho.name.replace('|', '/'), 'sha': sha}
            if tipo == 'transcricao':
                texto = limpar(ler_transcricao(caminho))
                if not texto.strip():
                    parar(f'{caminho.name}: não saiu texto nenhum')
                meta['palavras'] = numero(len(texto.split()))
                tempos = [segundos(t.group(1)) for t in map(TEMPO.match, texto.split('\n')) if t]
                if tempos:
                    meta['duracao'] = hms(max(tempos))
                corpo = texto
            else:
                paginas = [limpar(p) for p in ler_slides(caminho)]
                if not paginas:
                    parar(f'{caminho.name}: nenhuma página')
                vazias = [str(i) for i, p in enumerate(paginas, 1) if len(p.strip()) < 15]
                meta['paginas'] = str(len(paginas))
                if vazias:
                    meta['so_imagem'] = ', '.join(vazias)
                blocos = []
                for i, p in enumerate(paginas, 1):
                    blocos += [f'### Slide {i} de {len(paginas)}', f'<!-- slide {i} -->', p.strip() or '(só imagem, sem texto)', '']
                corpo = '\n'.join(blocos).strip('\n')
            parte = {'tipo': tipo, 'n': n, 'meta': meta, 'corpo': corpo}
            partes.append(parte)
            novos.append(parte)
    if not novos:
        print('nada novo: a fonte continua como estava')
        return
    escrever(a.aula, partes, destino)
    print(f'fonte guardada: {destino.relative_to(RAIZ)}')
    for p in novos:
        m = p['meta']
        if p['tipo'] == 'transcricao':
            print(f"  transcrição {p['n']}: {m['arquivo']}, {m['palavras']} palavras" + (f", até {m['duracao']}" if m.get('duracao') else ', sem marcação de tempo'))
        else:
            print(f"  slides {p['n']}: {m['arquivo']}, {m['paginas']} páginas" + (f"; só imagem: {m['so_imagem']}" if m.get('so_imagem') else ''))
    if a.slides:
        print('O arquivo original dos slides não vai para o Git: guarde na pasta da aula no Drive (MEDGENIUS → 2 - Aulas).')


def faixa_paginas(texto):
    paginas = set()
    for pedaco in texto.split(','):
        ini, _, fim = pedaco.partition('-')
        paginas.update(range(int(ini), int(fim or ini) + 1))
    return paginas


def trecho(a):
    arquivo = PASTA / a.aula / 'fonte.md'
    if not arquivo.exists():
        parar(f'a aula {a.aula} não tem fonte guardada ({arquivo.relative_to(RAIZ)}): confira pela apostila, como antes')
    partes = ler_partes(arquivo)
    ini = fim = None
    if a.minutos:
        de, _, ate = a.minutos.partition('-')
        conv = lambda t: segundos(t) if ':' in t else int(float(t) * 60)
        ini, fim = conv(de), conv(ate or de)
    paginas = faixa_paginas(a.slides) if a.slides else None
    so_slides = paginas is not None and not a.minutos and a.parte is None
    so_falas = (a.minutos or a.parte is not None) and paginas is None
    for p in partes:
        m = p['meta']
        if p['tipo'] == 'transcricao':
            if so_slides or (a.parte is not None and p['n'] != a.parte):
                continue
            print(f"===== transcrição {p['n']}: {m.get('arquivo', '')} =====")
            linhas = p['corpo'].split('\n')
            if ini is None:
                print(p['corpo'])
            elif not any(TEMPO.match(l) for l in linhas):
                sys.stderr.write(f"transcrição {p['n']} sem marcação de tempo: vai inteira\n")
                print(p['corpo'])
            else:
                agora = 0
                for linha in linhas:
                    t = TEMPO.match(linha)
                    if t:
                        agora = segundos(t.group(1))
                    if ini <= agora <= fim:
                        print(linha)
        else:
            if so_falas:
                continue
            print(f"===== slides {p['n']}: {m.get('arquivo', '')} =====")
            atual, guardar_linha = None, paginas is None
            for linha in p['corpo'].split('\n'):
                s = MARCA_SLIDE.match(linha)
                if s:
                    atual = int(s.group(1))
                    guardar_linha = paginas is None or atual in paginas
                    continue
                if linha.startswith('### Slide '):
                    continue
                if guardar_linha and atual is not None:
                    if not linha.strip():
                        continue
                    print(f'[slide {atual}] {linha}')


def main():
    p = argparse.ArgumentParser(description='Guarda e lê a fonte de uma aula (apostilas-fonte/<aula-id>/fonte.md).')
    sub = p.add_subparsers(dest='acao', required=True)
    g = sub.add_parser('guardar')
    g.add_argument('aula')
    g.add_argument('--transcricao', action='append', default=[])
    g.add_argument('--slides', action='append', default=[])
    g.add_argument('--acrescentar', action='store_true')
    t = sub.add_parser('trecho')
    t.add_argument('aula')
    t.add_argument('--minutos')
    t.add_argument('--parte', type=int)
    t.add_argument('--slides')
    a = p.parse_args()
    guardar(a) if a.acao == 'guardar' else trecho(a)


if __name__ == '__main__':
    main()
