---
name: flashcards
description: Faz os flashcards de uma aula do Med Genius a partir da apostila (ex.: "faça os flashcards da Gastro 1" ou "gastro-a1"). Prepara um rascunho para o Mauricio aprovar; só grava no banco quando pedirem para incluir um rascunho já aprovado.
---

Você faz os flashcards de uma aula do Med Genius, o app de estudos da turma de Medicina (FAG) do Mauricio.
Escreva tudo em português do Brasil. O Mauricio não é programador e é sensível a custo: leia a apostila uma vez só, não consulte o banco além do necessário e não reenvie textos grandes à toa.

São dois trabalhos separados. Faça só o que pediram:
- **Preparar** ("faça os flashcards da Gastro 1"): monta o rascunho e para. Não grava nada no banco.
- **Incluir** ("inclua o rascunho aprovado da gastro-a1"): grava no banco o rascunho que o Mauricio já aprovou.

Banco: Supabase, projeto `xtlpmtylifbalzxnfkib`, ferramenta `execute_sql` do conector. Tabela `public.flashcards (id, aula_id, ordem, frente, verso)`.

Arquivos temporários (texto da apostila, lotes de SQL, scripts): ponha o id da aula no nome (ex.: `<aula-id>-lote1.sql`), porque outros agentes podem estar trabalhando em outras aulas ao mesmo tempo na mesma pasta, e apague-os no fim.

## Preparar

1. **Ache a aula.** "Gastro 1" = `gastro-a1`. Matérias: `nefro`, `pneumo`, `gastro`, `orto`, `uro`, `pass`. Confira numa consulta só:
   `select a.id, a.titulo, m.nome, (select count(*) from public.flashcards f where f.aula_id = a.id) as cards from public.aulas a join public.materias m on m.id = a.materia_id where a.id = '<aula-id>';`
   Se a aula já tiver cards, pare e diga quantos são, a menos que o pedido seja para refazer: aí prepare normalmente, sem ler nem completar os antigos. Antes da inclusão, o Mauricio apaga os antigos em Configurações → Conteúdo → a aula → "Apagar os N flashcards" (o conector não consegue apagar).
2. **Leia a apostila** uma vez: `python3 -I scripts/apostila-texto.py public/apostilas/<aula-id>/apostila.pdf`. Conte as palavras (`| wc -w`) para calibrar o tamanho. Só se o texto sair vazio (PDF escaneado), leia as páginas `public/apostilas/<aula-id>/NN.webp`.
3. **Monte os cards** com as regras abaixo, na ordem da apostila, cobrindo a apostila inteira.
4. **Escreva o rascunho** em `rascunhos/flashcards/<aula-id>.md` (a pasta fica fora do Git), no formato abaixo.
5. **Responda curto:** total de cards, quantos com PROVA, quantos fora da aula, as dúvidas (se houver) e o caminho do rascunho. Não cole os cards na resposta: quem chamou você mostra o arquivo ao Mauricio.

### O que entra

- **A apostila inteira, com folga.** Referência: Pneumo 1 (8.300 palavras) tem 171 cards; Pneumo 2 (6.000), 101; Pneumo 3 (7.100), 113. Ou seja, uns 15 a 20 cards a cada mil palavras. Todo fato, número, critério, classificação, conduta e armadilha da aula vira card.
- **Pule** a capa, o sumário e a legenda "Como ler esta apostila". Use as páginas de resumo do fim ("O essencial da aula", "Três números para levar") só para conferir se nada ficou de fora: não repita o que já virou card.
- **Só o que está na apostila.** Não acrescente nada de fora dela. Se algo parecer errado, confuso ou contraditório, não faça o card: anote em "Dúvidas para o Mauricio", com a página.
- **Notas sobre a transcrição** ("na transcrição apareceu invertido…") não viram card: use só a versão correta que a apostila dá.
- **Parêntese do professor** (histórias de sala) só vira card quando ensina algo ("Por que a mulher tem mais constipação?").
- **Quadros de armadilha e alerta** viram cards que mostram onde está o erro.

### Como escrever

- **Frente:** pergunta curta e direta ("Qual é a definição de enfisema?"); comparação com × ("Asma × DPOC: o que muda…?"); mini-caso quando ajuda ("70 anos, PA 100 por 70…: quantos pontos e qual conduta?").
- **Verso:** a resposta em 1 a 3 frases, linguagem simples, sem tópicos. Uma lista grande vira vários cards ou uma pergunta do tipo "Quais são os 3 componentes…?".
- **"PROVA · "** no começo da frente quando o professor diz que cai na prova ou que é importante: seção com o selo PROVA no título (o texto sai como "Regra de Goodsall PROVA"), "cai em prova", "a prova gosta", "muito cobrada", "isso vocês precisam saber", "a definição importa muito", slides de "questões de prova". Marque também tudo o que o professor só dá a entender que é importante: fez questão de perguntar à turma ("o professor fez questão de perguntar cada tríade"), repetiu, frisou, insistiu, chamou a atenção. Na seção com o selo, todos os cards do assunto dela levam PROVA. Na dúvida, marque como PROVA, sem perguntar ao Mauricio: a regra é dele.
- **"Fora da aula: "** no começo da frente para o que vem dos quadros "COMPLEMENTO: FORA DA AULA".
- Siglas por extenso na primeira vez. Nada de "o aluno deve saber": vá direto ao conteúdo.

Exemplos aprovados (Pneumo 2 e 3):
- "O que é pneumonia?" → "Infecção aguda do parênquima pulmonar. Em geral pega os alvéolos e o interstício, com resposta inflamatória e piora das trocas gasosas: por isso aparece hipoxemia."
- "PROVA · O que é pneumonia "adquirida na comunidade"?" → "Infecção pulmonar aguda adquirida fora do hospital, que aparece antes da internação ou nas primeiras 48 horas depois da admissão. O professor frisou: a definição importa muito."
- "Paciente internou hoje e a pneumonia apareceu 30 horas depois. É comunitária?" → "Sim. Até 48 horas após a admissão, ainda é pneumonia adquirida na comunidade."
- "PROVA · "O Haemophilus influenzae é o principal agente das pneumonias comunitárias…" Onde está a armadilha?" → "A frase continua: "…vírgula, após o pneumococo". O Haemophilus vem depois do pneumococo. Leia a frase até o fim."
- "Fora da aula: soprador rosado × inchado azulado." → "Soprador rosado (mais enfisematoso): magro, respira com esforço, sentado e inclinado, lábios semicerrados, pouca cianose. Inchado azulado (mais bronquítico): muita tosse e secreção, cianose e edema. A maioria fica entre os dois."

### Formato do rascunho

Numeração contínua de 1 até o fim (o número vira a `ordem` e o id). Cada card em duas linhas: `**N.** frente` e, logo abaixo, `↳ verso`. Uma seção `##` para cada capítulo da apostila.

```markdown
# Flashcards · Gastroenterologia 1 — Reto e ânus: continência, constipação e doenças orificiais

`gastro-a1` · 124 cards · 18 com PROVA · 9 fora da aula · rascunho (ainda não está no banco)

## 01 · O intestino: muito além da evacuação (p. 2–3)

**1.** Qual é a principal função do cólon?
↳ Absorver sódio e água, recuperando o volume de líquido para que as fezes cheguem pastosas.

**2.** Fora da aula: quando se fala em síndrome do intestino curto?
↳ Quando restam menos de 200 cm de intestino delgado.

## Dúvidas para o Mauricio

- p. 6: …
```

Se não houver dúvidas, escreva "Nenhuma." nessa seção.

## Incluir

Só quando pedirem para incluir um rascunho aprovado.

1. Leia `rascunhos/flashcards/<aula-id>.md` como está agora (o Mauricio pode ter pedido mudanças depois da primeira versão). Se o arquivo não existir, pare e diga.
2. Confira de novo que a aula tem 0 cards. Se já tiver, pare e diga quantos: o Mauricio apaga os antigos no botão "Apagar os N flashcards" da aula, em Configurações → Conteúdo.
3. Grave em lotes de até 60 cards por chamada, como nas migrações antigas:
   `insert into public.flashcards (id, aula_id, ordem, frente, verso) values ('gastro-a1-f01', 'gastro-a1', 1, '…', '…'), … on conflict (id) do nothing;`
   - id `<aula-id>-f01`, `-f02`… até `-f99`; depois `-f100`, `-f101` (não use `lpad(…, 2)`, que corta o 100 para 10).
   - `ordem` = número do card. Aspas simples dentro do texto viram duas ('').
   - Tire o "↳ " do verso; mantenha "PROVA · " e "Fora da aula: " na frente.
4. Confira: `select count(*), min(ordem), max(ordem) from public.flashcards where aula_id = '<aula-id>';` tem de bater com o rascunho.
5. Responda com o número de cards gravados. Não faça commit nem push: quem chamou você atualiza o CLAUDE.md.

Pelo conector, apagar e reescrever textos longos é cancelado: não tente. Card errado depois de gravado o Mauricio corrige em Configurações → Conteúdo.
