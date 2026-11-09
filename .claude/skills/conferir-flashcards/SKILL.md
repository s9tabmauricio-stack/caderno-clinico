---
name: conferir-flashcards
description: Use quando o Mauricio pedir para conferir, verificar ou revisar os flashcards de uma aula que JÁ ESTÃO NO BANCO contra a fonte da aula (transcrição e slides) e a apostila (ex.: "confere os cards da Pneumo 6"). Divide os cards em blocos conferidos ao mesmo tempo e devolve só os que têm problema. Para rascunhos que ainda não estão no banco, use o agente revisor.
---

# Conferir os flashcards de uma aula (já no banco) contra a fonte da aula

**A referência é a fonte da aula** (regra do Mauricio, 09/11/2026): `apostilas-fonte/<aula-id>/fonte.md`, a transcrição e o texto dos slides. A apostila ajuda a achar a página, corrige os termos que a transcrição automática errou e traz o selo PROVA e os complementos "Fora da aula". Fonte e apostila divergem: o card segue a fonte (a fala manda sobre o slide) e a apostila entra na lista do que corrigir. **Aula sem fonte** (as antigas): só a apostila, como antes (pule o passo 5 da preparação).

Feita em 04/11/2026 porque a conferência de 115 cards num agente só, card por card, demorava demais. O que deixa rápido:
- **blocos ao mesmo tempo**: 3 ou 4 conferências em paralelo, uma por grupo de capítulos;
- **resposta só com problemas**: card certo não é reescrito nem listado;
- **cada conferente lê só o seu pedaço**: as páginas do seu bloco (mais o glossário e a "Página de véspera") e o trecho da fonte que vai com elas, não a aula inteira;
- **nada é reescrito durante a conferência**: as correções vêm depois, uma lista para o Mauricio aprovar.

Os conferentes seguem a regra dos agentes de conteúdo: Opus com esforço extra-alto. Preparar e juntar (seções 1 e 3) são mecânicos: ficam com quem coordena, sem agente.

**Antigravity e Codex** (sem agentes ao mesmo tempo): façam os blocos um depois do outro, seguindo a seção 2 para cada um, e juntem no fim. O Codex não tem o conector: lê e grava com `node scripts/sql.mjs "<SQL>"` (`docs/codex.md`).

## 1. Preparar (quem coordena, uma vez)

1. **Fila**: anote "Conferir flashcards da `<aula-id>`" em `docs/fila.md` (regras no topo do arquivo).
2. **Texto da apostila** num arquivo, com o id da aula no nome:
   `python3 -I scripts/apostila-texto.py public/apostilas/<aula-id>/apostila.pdf > <scratchpad>/<aula-id>-apostila.txt`
   Veja o sumário (página 1) e anote as páginas de cada capítulo.
3. **Mapa dos cards**, sem trazer o texto deles (o texto quem lê é o conferente):
   `select ordem, left(frente, 60) from public.flashcards where aula_id = '<aula-id>' order by ordem;`
   Divida em **3 ou 4 blocos** de capítulos inteiros, de 25 a 40 cards cada (uma aula curta, com menos de 40 cards, vai num bloco só). Cada bloco = faixa de `ordem` + páginas dos capítulos.
4. **Um arquivo de texto por bloco**, com as páginas dele mais as do fim (véspera e glossário):
   `python3 -I scripts/apostila-texto.py public/apostilas/<aula-id>/apostila.pdf --paginas 5-8,15-16 > <scratchpad>/<aula-id>-bloco1.txt`
5. **Trecho da fonte por bloco**: os minutos e os slides de cada capítulo estão no `apostilas-fonte/<aula-id>/mapa.md` (sem mapa, ache os minutos procurando os termos dos títulos dos capítulos na fonte com `grep`). Com 3 minutos de folga para cada lado:
   `python3 -I scripts/fonte-aula.py trecho <aula-id> --minutos 12-41 --slides 6-15 > <scratchpad>/<aula-id>-bloco1-fonte.txt`
   Transcrição sem marcação de tempo: o bloco recebe a fonte inteira (`apostilas-fonte/<aula-id>/fonte.md`).

## 2. Conferir (os blocos ao mesmo tempo)

Abra um conferente por bloco **na mesma mensagem** (ferramenta Agent, `model: opus`, `effort: xhigh`), com este pedido, trocando o que está entre `< >`:

> Confira os flashcards `<aula-id>` de ordem `<X>` a `<Y>` contra a fonte da aula. Siga a seção "2. Conferir" de `.claude/skills/conferir-flashcards/SKILL.md`. Trecho da fonte: `<arquivo do bloco-fonte>`. Texto das suas páginas da apostila: `<arquivo do bloco>`. Seus capítulos: `<capítulos>`, páginas `<páginas>`.

O conferente:
1. Busca só os seus cards, numa consulta (conector do Supabase, projeto `xtlpmtylifbalzxnfkib`):
   `select ordem, id, frente, verso from public.flashcards where aula_id = '<aula-id>' and ordem between <X> and <Y> order by ordem;`
2. Lê uma vez o trecho da fonte e o arquivo do seu bloco (as suas páginas, a "Página de véspera" e o glossário). Só se um card falar de assunto de outro capítulo, procura na fonte inteira (`apostilas-fonte/<aula-id>/fonte.md`) e no texto inteiro da apostila (`<aula-id>-apostila.txt`) com `grep`, sem ler tudo. Não abre outras apostilas, as imagens das páginas nem outros arquivos.
3. Para cada card, confere contra a fonte:
   - **o verso bate** com o que o professor falou ou o slide mostrou (número, dose, critério, corte, nome, sentido da frase); a frente pergunta uma coisa só e o verso responde a ela. Se a apostila diz diferente da fonte, o card segue a fonte e a linha leva "possível erro na apostila: p. X";
   - **"PROVA · "**: tem quando a apostila marca o assunto com o selo PROVA (aparece no texto como "… PROVA" no fim do título) ou o professor frisou na fonte; na dúvida, fica com PROVA (regra do Mauricio);
   - **"Fora da aula: "**: tem quando, e só quando, o conteúdo vem de um quadro "COMPLEMENTO: FORA DA AULA";
   - **não repete** outro card do mesmo bloco.
4. **Cobertura** das suas páginas: ponto com selo PROVA ou enfatizado pelo professor que ficou sem card nenhum (confira também nos outros cards pela consulta do mapa, se precisar).
5. **Responde curto, só com problemas**, nesta tabela (nada de listar card certo):

   | Card | Problema | Fonte (minuto ou slide e trecho curto; página da apostila) | Proposta |
   |---|---|---|---|
   | `pneumo-a6-f12` | verso diz 5 passos, o professor lista 4 | 23:10: "…"; p. 4 | verso: "…" |

   Tipos de proposta: `verso: "<texto novo>"`, `frente: "<texto novo>"`, `tirar` (com o motivo) ou `card novo: <frente> ↳ <verso>` (cobertura). Depois da tabela, uma linha: "Bloco <X>–<Y>: N cards, M com problema."
   Não grave nada no banco.

## 3. Juntar e mostrar ao Mauricio

1. Junte as tabelas numa só, na ordem dos cards. Resumo numa linha: "Pneumo A6: 115 cards, 108 ok, 5 corrigir, 1 tirar, 1 card novo."
2. Mostre os problemas (card atual, o trecho da fonte e a proposta) e espere o "pode". Erros da apostila que apareceram (onde ela diverge da fonte) vão numa lista à parte: corrigi-los é com a skill `conferir-apostila`. Pode mostrar todos de uma vez quando forem curtos; se ele pedir, um por vez.

## 4. Corrigir (só depois do "pode")

O card mantém o mesmo id, para não perder o progresso dos alunos na Revisão.
- **Frente ou verso curto**: `update public.flashcards set verso = '<texto>' where id = '<id>';` (aspas simples dentro do texto viram duas). Alteração curta funciona pelo conector.
- **Texto longo** (o conector cancela) e **tirar card** (o conector não apaga): vão numa lista para o Mauricio fazer em Configurações → Conteúdo → a aula. Não tente contornar.
- **Card novo**: inclua no fim, com a próxima ordem livre: `insert into public.flashcards (id, aula_id, ordem, frente, verso) values ('<aula-id>-f<N>', '<aula-id>', <N>, '…', '…') on conflict (id) do nothing;` (id sem zeros à esquerda a partir do 100).
- Confira no fim: `select count(*), max(ordem) from public.flashcards where aula_id = '<aula-id>';`
- Apague os arquivos temporários e tire a linha da fila no PR.
