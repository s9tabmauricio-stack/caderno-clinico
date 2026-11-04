# Pneumologia · Aula 6 · Tabagismo

Professor: Dr. Cássio. Data: 28/10/2026, quarta-feira. Identificação confirmada pelo Mauricio na conversa.

## Entrega

- `Pneumologia - Aula 6 - Dr. Cássio - Tabagismo.pdf`: versão final, 16 páginas A4 em retrato.
- `apostila.html`: origem exata do PDF.
- `apostila.css`: cópia sem mudanças do CSS atual do projeto.
- `fig/`: seis diagramas SVG; `gerar_figuras.py` reproduz os desenhos.
- `fonts/`: fonte Inter e licença.
- `identificacao.json` e `gerar_apostila.py`: identificação e conteúdo para regenerar o HTML.
- `mapa.md`: trilha, cobertura e decisões editoriais.
- `revisao-clinica.md`: conferência das notas externas e referências verificadas.
- `render.py`, `checar.py`: extraídos literalmente do padrão enviado pelo Mauricio.
- `apostila-padrao-SKILL.md`, `apostila-molde.md`: instruções aplicadas.

## Conferência final

- Revisão de cobertura contra a transcrição: sem perdas materiais identificadas.
- `render.py`: 16 páginas, quatro linhas de anotações, nenhum espaço vazio no pé das páginas intermediárias acima de 90 pt.
- `checar.py`: nenhum aviso automático; apenas fontes Inter, rodapé correto, nenhum marcador pendente, nenhuma sigla para revisar. Data de 28/10/2026 conferida.
- Todas as 16 páginas foram inspecionadas visualmente: cabeçalhos, sumário, figuras, caixas, rodapés e página de véspera.
- A página de véspera ocupa uma página inteira. Glossário e anotações vêm na página seguinte.
- O selo PROVA fica somente na orientação de usar a expressão “apoio comportamental”. A evidência e o horário ficam registrados no mapa interno.
- A redação foi revista para leitura autônoma: conceitos ensinados diretamente, sem menção à origem em áudio, transcrição ou etapas da produção. As citações preservam ensinamentos humanos, experiência profissional e orientação para a prova, com autoria e sem minutagem.

## Limites da fonte e itens a conferir

Fonte principal: transcrição enviada na conversa, com 49min24s. Áudio original e slides atualizados não foram recebidos. Os horários permanecem apenas nos registros internos, nunca no PDF.

O trecho “histamina [dopamina]” em 06:24 permanece sem confirmação pelo áudio. O texto preserva a explicação sobre recompensa sem reconstruir a lista de neurotransmissores.

Os estudos dos percentuais de sucesso, recaída e epidemiologia não foram identificados pelo professor. Os números foram mantidos como falas atribuídas, com o grau de certeza preservado, sem gráficos de eficácia. A disponibilidade comercial de vareniclina e pastilhas foi registrada como relato da época da aula, sem afirmar situação atual.

As notas roxas esclarecem limites de formulação, concentração e absorção, técnica da goma, cortes documentais e diferenças de conceitos. Não ampliam o material para um protocolo completo de prescrição.

## Reprodução

O ambiente local está documentado em `AMBIENTE-PDF.md`, com dependências fixadas em `requirements-pdf.txt`. Para usar a pasta em outro local, ajuste apenas os caminhos do `fontconfig.xml` ou configure o Fontconfig para localizar a pasta `fonts/`. O HTML e o CSS usam caminhos relativos para suas fontes e imagens.

```bash
python gerar_apostila.py
python render.py apostila.html "Pneumologia - Aula 6 - Dr. Cássio - Tabagismo.pdf"
python checar.py "Pneumologia - Aula 6 - Dr. Cássio - Tabagismo.pdf" apostila.html
```

Os arquivos de publicação ficam em `public/apostilas/pneumo-a6/`: PDF e 16 páginas em WebP. A aula do site tem o identificador `pneumo-a6`.
