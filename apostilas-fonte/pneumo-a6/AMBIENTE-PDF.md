# Ambiente de geração do PDF

Diretório de trabalho: `/workspace/medgenius-tabagismo`.

Os arquivos `render.py` e `checar.py` foram extraídos, sem alterações, dos blocos `arquivo:` de `apostila-padrao-SKILL.md`. O `apostila.css` é uma cópia exata da versão atual do repositório, em `/workspace/caderno-clinico/apostilas-fonte/apostila.css`.

O ambiente virtual `.venv` contém WeasyPrint, pdfplumber, pypdfium2, Pillow e fontTools. As versões instaladas estão em `requirements-pdf.txt`.

## Comandos

Execute dentro deste diretório, ajustando apenas o nome do PDF:

```bash
FONTCONFIG_FILE=/workspace/medgenius-tabagismo/fontconfig.xml .venv/bin/python render.py apostila.html 'Pneumologia - Tabagismo.pdf'
FONTCONFIG_FILE=/workspace/medgenius-tabagismo/fontconfig.xml .venv/bin/python checar.py 'Pneumologia - Tabagismo.pdf' apostila.html
```

O `FONTCONFIG_FILE` permite encontrar as fontes locais e gravar o cache em `font-cache/`, sem alterar fontes ou cache globais.

## Fontes

Fontes estáticas em `fonts/`, com eixo óptico 14:

- `Inter-Regular.ttf`: peso 400, família Inter.
- `Inter-Medium.ttf`: peso 500, família Inter Medium.
- `Inter-SemiBold.ttf`: peso 600, família Inter SemiBold.
- `Inter-Bold.ttf`: peso 700, família Inter.

Fonte variável de origem: `font-source/Inter-variable.ttf`, obtida de `https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz,wght%5D.ttf`. Licença em `fonts/OFL.txt`.

Para medir textos de SVGs com Pillow, use os caminhos absolutos dos arquivos estáticos, com `.venv/bin/python`.

## Validação executada

- Imports das bibliotecas de geração e revisão concluídos.
- `fc-match` resolve as famílias Regular, Medium e SemiBold para os arquivos locais.
- PDF técnico temporário gerado com os quatro pesos; todas as fontes incorporadas são Inter.
- Rasterização do PDF técnico com pypdfium2 concluída.
- Comparação literal dos dois scripts contra os blocos da skill e do CSS contra a origem, sem diferenças.

Essa validação cobre o ambiente; a conferência da apostila final deve ser executada depois que o HTML estiver pronto.
