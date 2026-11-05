# Nefrologia · Aula 6 · Infecção urinária

Professora: Dra. Andressa. Data: 21 de outubro de 2026. Nome e identificação confirmados pelo Mauricio.

O PDF segue o molde do MedGenius, com mapa anterior à escrita, cinco figuras originais, notas clínicas em roxo, página de véspera, glossário e espaço de anotações. A fonte recebida reúne as duas partes da aula.

## Arquivos

- `apostila.html`: fonte exata do PDF.
- `montar_apostila.py`: texto e composição; recria o HTML.
- `gerar_figuras.py`: recria os cinco SVGs; requer a imagem PNG preservada em `fig/` e a fonte Inter.
- `fig/`: ilustração PNG e diagramas SVG. O SVG de anatomia incorpora o PNG para manter a portabilidade.
- `mapa.md`: cobertura e rastreabilidade do conteúdo.
- `revisao-clinica.md`: divergências e referências dos complementos.
- `imagens-gpt.md`: orientação usada para gerar e revisar a ilustração.
- `validacao.txt`: verificações finais.

## Gerar novamente

Na raiz do projeto, preparar uma pasta de trabalho com os arquivos oficiais:

```bash
apostilas-fonte/ferramentas/preparar.sh /tmp/nefro-a6
cp -r apostilas-fonte/nefro-a6/* /tmp/nefro-a6/
cd /tmp/nefro-a6
python3 gerar_figuras.py
python3 montar_apostila.py
python3 render.py apostila.html 'Nefrologia - Aula 6 - Dra. Andressa - Infecção urinária.pdf'
python3 checar.py 'Nefrologia - Aula 6 - Dra. Andressa - Infecção urinária.pdf' apostila.html
```

O CSS, `render.py`, `checar.py` e as fontes são cópias oficiais, sem modificação. As alterações desta apostila ficam no HTML e nos programas de composição e figuras. Não há alteração do aplicativo, do banco ou da aula publicada.
