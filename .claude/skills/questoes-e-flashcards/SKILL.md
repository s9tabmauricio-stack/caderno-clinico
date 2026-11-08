---
name: questoes-e-flashcards
description: Regras das questões e dos flashcards do Med Genius (formato no banco, origem, PROVA, ids, prova sem gabarito, Revalida). Use quando incluir, corrigir ou resolver questões ou flashcards à mão, fora dos agentes questoes, flashcards, conteudo e revisor (que já têm as regras), por exemplo questões de provas antigas.
---

# Questões e flashcards

Para montar a partir da apostila de uma aula, chame o agente (`questoes`, `flashcards` ou `conteudo`); não refaça a receita aqui. Para corrigir o que já está no banco, siga o "Limite do conector" do manual (versão `-v2`). Para trocar várias de uma vez (ex.: refazer as questões diretas de uma aula como caso clínico), o agente `questoes` escreve `rascunhos/questoes-refazer/<aula>.md` com `substitui: <id antigo>` no título de cada questão, o `revisor` confere e `node scripts/substituir-questoes.mjs <aula>` monta os lotes de SQL (versão `-v2`, ordem e PROVA da antiga, recados junto) para rodar no conector.

## Questões

- `alternativas`: lista de textos sem a letra; `correta`: índice (0 = A).
- `comentario`: aparece embaixo da alternativa certa.
- `por_que_erradas`: uma linha por letra (`B: …`, ou `A, C e E: …` para várias). Linhas sem letra viram o quadro "Sobre as alternativas".
- `origem`: `professor` (corrigida em sala), `unica`, `inferido` (alternativa reconstruída), `montada` (alternativas montadas, gabarito não oficial), `resolvida` (gabarito não oficial), `adaptada` (questão oficial alterada para seguir a aula; o comentário diz o que mudou).
- `prova`: de qual prova a questão veio (`p1`, `p2`, `p2-t19` = P2 da turma 19, `exame`, `Revalida 2022.1`, `Residência`…); junto com `fonte`, decide em qual dos três grupos do filtro "Fonte" do Banco a questão aparece: sem `prova` e fonte "Montada (aula …)" = Apostila; `p1`, `p2`, `p2-tNN`, `exame` ou fonte com "material da turma"/"guia de estudo" = Provas da FAG; qualquer outra (Residência, Revalida, banca) = Residência e concursos. `cai_na_prova` (sim/não): o professor disse ou deu a entender que o ponto cai na prova (selo PROVA da apostila, ou ênfase em aula). São coisas diferentes: nunca escreva `'PROVA'` no campo `prova` (regra do Mauricio, 03/11/2026).
- **Faixa PROVA** (fita âmbar e preta em volta da questão, `lib/faixa-prova.ts`): aparece quando `cai_na_prova = true` e também nas questões das provas antigas do curso (`prova` = `p1`, `p2`, `p2-t19`, `exame`…). Revalida, Residência e outras bancas não ganham a faixa. Na versão `-v2` de uma questão corrigida, copie o `cai_na_prova` da antiga.
- Quando a prova não tem gabarito: resolva com base na apostila da aula, marque como não oficial e **discuta as duvidosas com o Mauricio uma a uma, mostrando o texto completo da questão** antes de pedir decisão.
- Questões montadas pela aula (agente `questoes`): cobrem a apostila inteira com folga, com pelo menos uma questão para cada ponto de PROVA, cada coisa que o professor frisou, repetiu ou deu a entender que cai (os de PROVA ganham duas ou mais e levam `cai_na_prova = true`, que põe a faixa PROVA em volta da questão); só o que está na apostila; cinco alternativas, gabarito espalhado, `origem = 'montada'`, ids `<aula>-q01`… Na produção automática, a duvidosa não entra: fica no relatório.
- Revalida quase não cobra pneumonia hospitalar (procurado de 2016 a 2026/2).
- Provas do Revalida (INEP): o servidor manda o certificado incompleto; baixe com `curl --cacert` num arquivo que junte `/root/.ccr/ca-bundle.crt` e o intermediário "RNP ICPEdu GR46 OV TLS CA 2025" (http://secure.globalsign.com/cacert/rnpicpedugr46ovtlsca2025.crt, convertido para PEM). A prova de 2022.1 tem a fonte embaralhada no PDF: confira o texto na imagem da página.

## Flashcards

- Todas as aulas no ar têm cards no padrão novo. Quantos cada uma tem: conte no banco, não anote no manual.
- Feitos a partir da apostila da aula, na ordem dela, cobrindo a apostila inteira com folga (Pneumonia, `pneumo-a2`: 101 cards).
- **Frente:** pergunta curta e direta ("Qual é a definição de enfisema?"); comparação com × ("Asma × DPOC: o que muda…?"); mini-caso quando ajuda ("70 anos, PA 100 por 70…: quantos pontos e qual conduta?").
- **Verso:** a resposta em 1 a 3 frases, linguagem simples, sem tópicos.
- **"PROVA · "** no começo da frente quando o professor diz que cai na prova ou que é importante (marca PROVA da apostila, "isso vocês precisam saber", "a definição importa muito", slides de "questões de prova") **e também quando ele só dá a entender que é importante**: fez questão de perguntar à turma, repetiu, frisou, insistiu, chamou a atenção. Na dúvida, marque como PROVA, sem perguntar ao Mauricio (regra dele, 22/10/2026). Em Pneumo, o card marcado ganha a faixa PROVA na sessão de estudo (`cardDeProva` em `lib/faixa-prova.ts`; as marcas de Pneumo foram conferidas aula por aula contra a apostila em 03/11/2026). Outras matérias entram na faixa quando as marcas delas forem conferidas: é só pôr o id da matéria em `MATERIAS_COM_FAIXA_NO_CARD`.
- O que vem do "Complemento: fora da aula" da apostila entra avisando no próprio card ("Fora da aula: …").
- ids `<aula>-f01`, `-f02`… (acima de 99 seguem `-f100`, `-f101`); `ordem` = número do card. Mostrar a lista ao Mauricio antes de incluir (menos na produção automática de aula nova, em que o agente `revisor` aprova).
- **Agente `flashcards`** (`.claude/agents/flashcards.md`) faz tudo isso: "faça os flashcards da Gastro 1" monta o rascunho em `rascunhos/flashcards/<aula>.md` (pasta fora do Git) para o Mauricio aprovar; "inclua o rascunho aprovado da gastro-a1" grava no banco. Ele lê a apostila com `python3 -I scripts/apostila-texto.py <pdf>`, que mantém os selos PROVA dos títulos (o `pdftotext` os perde).
