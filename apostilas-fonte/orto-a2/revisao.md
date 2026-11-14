# Revisão de produção · orto-a2

Aula 2 de Ortopedia, Artrose, 08/10/2026. Professor confirmado pelo Mauricio: Dr. Gustavo Alves Colombo. A indicação do usuário prevalece sobre o nome Dr. André registrado na agenda e sobre o número 3 no nome do PDF de slides.

## Conferência de conteúdo

Conferência feita contra a transcrição integral guardada em fonte.md, conforme a cobertura e os registros PROVA do mapa. Valores, sequência clínica e citações cotejados com a fonte; aprofundamentos para residência distinguidos da prioridade para a disciplina. Termos automáticos corrigidos sem editar a fonte original. Sem doses ou esquemas de infiltração criados. Os complementos sobre conceito atual de osteoartrite, obesidade, nomenclatura dos eixos, segurança e evidência das terapias, anquilose, percentuais epidemiológicos, rizartrose e registro clínico aparecem em roxo.

## Limitação material

O PDF Aula 3 - G - Artrose.pdf excedeu o limite de 32 MiB de download_file. Não foi possível lê-lo, extrair seu texto ou incorporar radiografias. A apostila foi concluída a partir da transcrição; não há afirmação de cobertura dos slides. O mapa registra a pendência e o caminho para incorporá-los quando acessíveis. As quatro figuras são esquemas explicativos vetoriais; nenhuma imagem de exame foi inventada.

## Verificação

- PDF A4, fonte Inter, rodapé, sumário clicável e marcadores conferidos pelo render.py e checar.py oficiais.
- Critério de paginação: nenhuma página intermediária com espaço livre superior a 90 pt; anotações na última página.
- Páginas inspecionadas visualmente, com ajuste de títulos e correção do cabeçalho do ombro que havia ficado isolado.
- npm test: 66 testes aprovados.
- npx next build: compilação e TypeScript aprovados, 24 páginas estáticas geradas.

## Como regenerar

Na raiz do repositório, rode apostilas-fonte/ferramentas/preparar.sh <pasta-temporaria>, copie os arquivos desta pasta para lá e execute python3 montar.py, python3 render.py apostila.html apostila.pdf e python3 checar.py apostila.pdf apostila.html. As ferramentas e o CSS oficiais não foram alterados. montar.py gera as figuras e o HTML legível como produto; o PDF público corresponde a esse HTML.
