---
name: conferir-flashcards
description: Use quando o Mauricio pedir para conferir, verificar ou revisar os flashcards de uma aula que JÁ ESTÃO NO BANCO contra a apostila (ex.: "confere os cards da Pneumo 6"). Divide os cards em blocos conferidos ao mesmo tempo e devolve só os que têm problema. Para rascunhos que ainda não estão no banco, use o agente revisor.
---

# Conferir os flashcards de uma aula (já no banco) contra a apostila

Feita em 04/11/2026 porque a conferência de 115 cards num agente só, card por card, demorava demais. O que deixa rápido:
- **blocos ao mesmo tempo**: 3 ou 4 conferências em paralelo, uma por grupo de capítulos;
- **resposta só com problemas**: card certo não é reescrito nem listado;
- **nada é reescrito durante a conferência**: as correções vêm depois, uma lista para o Mauricio aprovar.

Os conferentes seguem a regra dos agentes de conteúdo: Opus com esforço extra-alto.

## 1. Preparar (quem coordena, uma vez)

1. **Fila**: anote "Conferir flashcards da `<aula-id>`" em `docs/fila.md` (regras no topo do arquivo).
2. **Texto da apostila** num arquivo, com o id da aula no nome:
   `python3 -I scripts/apostila-texto.py public/apostilas/<aula-id>/apostila.pdf > <scratchpad>/<aula-id>-apostila.txt`
   Veja o sumário (página 1) e anote as páginas de cada capítulo.
3. **Mapa dos cards**, sem trazer o texto deles (o texto quem lê é o conferente):
   `select ordem, left(frente, 60) from public.flashcards where aula_id = '<aula-id>' order by ordem;`
   Divida em **3 ou 4 blocos** de capítulos inteiros, de 25 a 40 cards cada (uma aula curta, com menos de 40 cards, vai num bloco só). Cada bloco = faixa de `ordem` + páginas dos capítulos.

## 2. Conferir (os blocos ao mesmo tempo)

Abra um conferente por bloco **na mesma mensagem** (ferramenta Agent, `model: opus`, `effort: xhigh`), com este pedido, trocando o que está entre `< >`:

> Confira os flashcards `<aula-id>` de ordem `<X>` a `<Y>` contra a apostila. Siga a seção "2. Conferir" de `.claude/skills/conferir-flashcards/SKILL.md`. Apostila em texto: `<arquivo>`. Seus capítulos: `<capítulos>`, páginas `<páginas>`.

O conferente:
1. Busca só os seus cards, numa consulta (conector do Supabase, projeto `xtlpmtylifbalzxnfkib`):
   `select ordem, id, frente, verso from public.flashcards where aula_id = '<aula-id>' and ordem between <X> and <Y> order by ordem;`
2. Lê o arquivo da apostila uma vez, todo (é curto): as suas páginas com atenção; o resto só para achar um assunto que apareça em outro capítulo, na "Página de véspera" ou no glossário. Não abre a transcrição, outras apostilas, as imagens das páginas nem outros arquivos.
3. Para cada card, confere contra a apostila:
   - **o verso bate** com o que a apostila diz (número, dose, critério, corte, nome, sentido da frase); a frente pergunta uma coisa só e o verso responde a ela;
   - **"PROVA · "**: tem quando a apostila marca o assunto com o selo PROVA (aparece no texto como "… PROVA" no fim do título) ou o professor frisou; na dúvida, fica com PROVA (regra do Mauricio);
   - **"Fora da aula: "**: tem quando, e só quando, o conteúdo vem de um quadro "COMPLEMENTO: FORA DA AULA";
   - **não repete** outro card do mesmo bloco.
4. **Cobertura** das suas páginas: ponto com selo PROVA ou enfatizado pelo professor que ficou sem card nenhum (confira também nos outros cards pela consulta do mapa, se precisar).
5. **Responde curto, só com problemas**, nesta tabela (nada de listar card certo):

   | Card | Problema | Apostila (página e trecho curto) | Proposta |
   |---|---|---|---|
   | `pneumo-a6-f12` | verso diz 5 passos, apostila lista 4 | p. 4: "…" | verso: "…" |

   Tipos de proposta: `verso: "<texto novo>"`, `frente: "<texto novo>"`, `tirar` (com o motivo) ou `card novo: <frente> ↳ <verso>` (cobertura). Depois da tabela, uma linha: "Bloco <X>–<Y>: N cards, M com problema."
   Não grave nada no banco.

## 3. Juntar e mostrar ao Mauricio

1. Junte as tabelas numa só, na ordem dos cards. Resumo numa linha: "Pneumo A6: 115 cards, 108 ok, 5 corrigir, 1 tirar, 1 card novo."
2. Mostre os problemas (card atual, o trecho da apostila e a proposta) e espere o "pode". Pode mostrar todos de uma vez quando forem curtos; se ele pedir, um por vez.

## 4. Corrigir (só depois do "pode")

O card mantém o mesmo id, para não perder o progresso dos alunos na Revisão.
- **Frente ou verso curto**: `update public.flashcards set verso = '<texto>' where id = '<id>';` (aspas simples dentro do texto viram duas). Alteração curta funciona pelo conector.
- **Texto longo** (o conector cancela) e **tirar card** (o conector não apaga): vão numa lista para o Mauricio fazer em Configurações → Conteúdo → a aula. Não tente contornar.
- **Card novo**: inclua no fim, com a próxima ordem livre: `insert into public.flashcards (id, aula_id, ordem, frente, verso) values ('<aula-id>-f<N>', '<aula-id>', <N>, '…', '…') on conflict (id) do nothing;` (id sem zeros à esquerda a partir do 100).
- Confira no fim: `select count(*), max(ordem) from public.flashcards where aula_id = '<aula-id>';`
- Apague os arquivos temporários e tire a linha da fila no PR.
