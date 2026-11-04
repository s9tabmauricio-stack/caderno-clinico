# Pneumologia · Aula 6 · Tabagismo

Professor: Dr. Cássio. Data: 28/10/2026, quarta-feira. Identificação confirmada pelo Mauricio na conversa. 16 páginas A4.

## O que tem aqui

- `apostila.html`: origem exata do PDF publicado em `public/apostilas/pneumo-a6/`.
- `fig/` e `gerar_figuras.py`: os seis diagramas SVG e o programa que os desenha (usa a pasta `fonts/` que o `preparar.sh` copia).
- `mapa.md`: trilha, cobertura e decisões editoriais.
- `revisao-clinica.md`: conferência das notas externas e referências verificadas.

CSS, `render.py`, `checar.py` e a fonte Inter ficam numa cópia só, em `apostilas-fonte/ferramentas/` (desde 04/11/2026; antes havia cópias nesta pasta).

## Itens a conferir (da produção)

- O trecho "histamina [dopamina]" (06:24) não foi confirmado pelo áudio; o texto preserva a explicação sobre recompensa sem a lista de neurotransmissores.
- Os estudos dos percentuais de sucesso, recaída e epidemiologia não foram identificados pelo professor: os números ficaram como falas atribuídas.
- A disponibilidade comercial de vareniclina e pastilhas foi registrada como relato da época da aula.

## Gerar de novo

```bash
apostilas-fonte/ferramentas/preparar.sh /tmp/gerar-pneumo-a6 && cp -r apostilas-fonte/pneumo-a6/* /tmp/gerar-pneumo-a6/
```

```bash
cd /tmp/gerar-pneumo-a6 && python3 render.py apostila.html "Pneumologia - Aula 6 - Dr. Cássio - Tabagismo.pdf" && python3 checar.py "Pneumologia - Aula 6 - Dr. Cássio - Tabagismo.pdf" apostila.html
```

Conferido em 04/11/2026: dá as mesmas 16 páginas, sem buracos e sem avisos do `checar.py`.
