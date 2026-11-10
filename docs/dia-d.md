# Flashcards Dia D

Regra do Mauricio (10/11/2026): cada aula pode ter uma 4ª aba, **Flashcards Dia D**, ao lado de Apostila | Questões | Flashcards. É o baralho de véspera da prova: os cards ensinam o que é preciso para resolver **todas as questões das Provas da FAG** da aula (o grupo "Provas da FAG" da barra de fonte: P1, P2, P2 de outras turmas, exame e material da turma).

## Como funciona na tela

- A aba só aparece na aula que tem cards Dia D (`components/FlashcardsDiaD.tsx`, ligado em `components/AulaAbas.tsx`; endereço direto `/aula/<id>?aba=diad`).
- Não entra na Revisão do dia e não grava nada do aluno: ele vira o card e marca **Sabia** (2) ou **Não sabia** (1). O que ele não sabia volta no fim da fila, até fechar todos. No fim: repetir os que errou ou ir para as questões das Provas da FAG da aula.
- Cada card mostra, depois de virado, em qual questão ajuda ("Ajuda na questão P2 · nº 10").
- Editar ou apagar: Configurações → Conteúdo → a aula → seção "Flashcards Dia D" (editar card por card ou "Apagar os N cards Dia D" para refazer).

## Banco

Tabela `flashcards_dia_d (id, aula_id, ordem, frente, verso, questoes text[])`: id `<aula-id>-d01`…, `questoes` = ids das questões FAG que o card ajuda a resolver. Alunos só leem; escrita pela chave secreta ou pelo conector. Estrutura em `supabase/estrutura-atual.sql`.

## Fazer o Dia D de uma aula

1. **Cards:** agente `flashcards` (ele já roda no Opus extra-alto), com o pedido de "Flashcards Dia D". O que pedir a ele:
   - ler as questões FAG da aula pelo conector (consulta no topo de `scripts/dia-d.mjs`) ou pelo arquivo de `node scripts/dia-d.mjs exportar <aula-id>` (só onde o programa alcança o Supabase);
   - fazer os cards a partir da fonte da aula (`apostilas-fonte/<aula-id>/fonte.md`; aula sem fonte: a apostila), com a apostila de guia;
   - para cada questão, o conceito que dá a resposta certa e por que cada alternativa errada está errada, sem decorar gabarito; sem o prefixo "PROVA · " (no Dia D tudo é de prova);
   - conferir o gabarito de cada questão contra a fonte e pôr em "Dúvidas para o Mauricio" a que não bater;
   - escrever em `rascunhos/flashcards-dia-d/<aula-id>.md` no formato abaixo.
2. **Revisão:** agente `revisor`, conferindo o rascunho contra a fonte e as questões.
3. **Gravar** (programa, sem agente): `node scripts/dia-d.mjs gravar <aula-id>`. Ele confere que toda questão FAG tem card e que todo id citado é FAG da aula, e para se a aula já tiver cards Dia D. Sem acesso direto ao banco: `--sql --questoes id1,id2,…` escreve o SQL em `rascunhos/sql/` para rodar no conector. `--conferir` só confere.

### Formato do rascunho

Uma seção `##` por questão FAG, começando pelo id da questão; os cards dela embaixo, numerados de 1 até o fim. Card que ajuda em mais de uma questão leva `+ também: <id>` abaixo do verso.

```markdown
# Flashcards Dia D · Pneumologia 1 — Asma

`pneumo-a1` · 40 cards · 15 questões das Provas da FAG · rascunho

## pneumo-a1-q07 · P2 · nº 10 — Espirometria

**1.** Qual é o critério de resposta ao broncodilatador na espirometria do adulto?
↳ Aumento do VEF1 de pelo menos 12% e 200 mL em relação ao basal.

**2.** CVF baixa com relação VEF1/CVF normal sugere qual padrão?
↳ Padrão restritivo.
+ também: pneumo-a1-q12

## Dúvidas para o Mauricio

- Nenhuma.
```
