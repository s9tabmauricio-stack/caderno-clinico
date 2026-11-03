---
name: questoes-e-flashcards
description: Regras das questões e dos flashcards do Med Genius (formato no banco, origem, PROVA, ids, prova sem gabarito, Revalida). Use quando incluir, corrigir ou resolver questões ou flashcards à mão, fora dos agentes questoes, flashcards, conteudo e revisor (que já têm as regras), por exemplo questões de provas antigas.
---

# Questões e flashcards

Para montar a partir da apostila de uma aula, chame o agente (`questoes`, `flashcards` ou `conteudo`); não refaça a receita aqui. Para corrigir o que já está no banco, siga o "Limite do conector" do manual (versão `-v2`).

## Questões

- `alternativas`: lista de textos sem a letra; `correta`: índice (0 = A).
- `comentario`: aparece embaixo da alternativa certa.
- `por_que_erradas`: uma linha por letra (`B: …`, ou `A, C e E: …` para várias). Linhas sem letra viram o quadro "Sobre as alternativas".
- `origem`: `professor` (corrigida em sala), `unica`, `inferido` (alternativa reconstruída), `montada` (alternativas montadas, gabarito não oficial), `resolvida` (gabarito não oficial), `adaptada` (questão oficial alterada para seguir a aula; o comentário diz o que mudou).
- Quando a prova não tem gabarito: resolva com base na apostila da aula, marque como não oficial e **discuta as duvidosas com o Mauricio uma a uma, mostrando o texto completo da questão** antes de pedir decisão.
- Questões montadas pela aula (agente `questoes`): cobrem a apostila inteira com folga, com pelo menos uma questão para cada ponto de PROVA, cada coisa que o professor frisou, repetiu ou deu a entender que cai (os de PROVA ganham duas ou mais e levam `prova = 'PROVA'`, que mostra a etiqueta `PROVA` no topo do cartão); só o que está na apostila; cinco alternativas, gabarito espalhado, `origem = 'montada'`, ids `<aula>-q01`… Na produção automática, a duvidosa não entra: fica no relatório.
- Revalida quase não cobra pneumonia hospitalar (procurado de 2016 a 2026/2).
- Provas do Revalida (INEP): o servidor manda o certificado incompleto; baixe com `curl --cacert` num arquivo que junte `/root/.ccr/ca-bundle.crt` e o intermediário "RNP ICPEdu GR46 OV TLS CA 2025" (http://secure.globalsign.com/cacert/rnpicpedugr46ovtlsca2025.crt, convertido para PEM). A prova de 2022.1 tem a fonte embaralhada no PDF: confira o texto na imagem da página.

## Flashcards

- Todas as aulas no ar têm cards no padrão novo. Quantos cada uma tem: conte no banco, não anote no manual.
- Feitos a partir da apostila da aula, na ordem dela, cobrindo a apostila inteira com folga (Pneumonia, `pneumo-a2`: 101 cards).
- **Frente:** pergunta curta e direta ("Qual é a definição de enfisema?"); comparação com × ("Asma × DPOC: o que muda…?"); mini-caso quando ajuda ("70 anos, PA 100 por 70…: quantos pontos e qual conduta?").
- **Verso:** a resposta em 1 a 3 frases, linguagem simples, sem tópicos.
- **"PROVA · "** no começo da frente quando o professor diz que cai na prova ou que é importante (marca PROVA da apostila, "isso vocês precisam saber", "a definição importa muito", slides de "questões de prova") **e também quando ele só dá a entender que é importante**: fez questão de perguntar à turma, repetiu, frisou, insistiu, chamou a atenção. Na dúvida, marque como PROVA, sem perguntar ao Mauricio (regra dele, 22/10/2026).
- O que vem do "Complemento: fora da aula" da apostila entra avisando no próprio card ("Fora da aula: …").
- ids `<aula>-f01`, `-f02`… (acima de 99 seguem `-f100`, `-f101`); `ordem` = número do card. Mostrar a lista ao Mauricio antes de incluir (menos na produção automática de aula nova, em que o agente `revisor` aprova).
- **Agente `flashcards`** (`.claude/agents/flashcards.md`) faz tudo isso: "faça os flashcards da Gastro 1" monta o rascunho em `rascunhos/flashcards/<aula>.md` (pasta fora do Git) para o Mauricio aprovar; "inclua o rascunho aprovado da gastro-a1" grava no banco. Ele lê a apostila com `python3 -I scripts/apostila-texto.py <pdf>`, que mantém os selos PROVA dos títulos (o `pdftotext` os perde).
