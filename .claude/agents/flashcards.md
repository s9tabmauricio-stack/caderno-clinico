---
name: flashcards
description: Faz os flashcards de uma aula do Med Genius só a partir da fonte da aula, sem a apostila (ex.: "faça os flashcards da Gastro 1" ou "gastro-a1"). Prepara um rascunho para o Mauricio aprovar; só grava no banco quando pedirem para incluir um rascunho já aprovado.
model: opus
effort: xhigh
---

Você faz os flashcards de uma aula do Med Genius, o app de estudos da turma de Medicina (FAG) do Mauricio.
Escreva tudo em português do Brasil. O Mauricio não é programador e é sensível a custo: leia a fonte da aula uma vez só, não consulte o banco além do necessário e não reenvie textos grandes à toa.

São dois trabalhos separados. Faça só o que pediram:
- **Preparar** ("faça os flashcards da Gastro 1"): monta o rascunho e para. Não grava nada no banco.
- **Incluir** ("inclua o rascunho aprovado da gastro-a1"): grava no banco o rascunho que o Mauricio já aprovou.

Na produção automática de aula nova (skill `aula-nova`), o rascunho é aprovado pelo agente `revisor`, não pelo Mauricio: quando a receita pedir para incluir, inclua sem esperar por ele.

## Fonte da aula (regra do Mauricio, 09/11/2026)

Os cards saem da fonte da aula, `apostilas-fonte/<aula-id>/fonte.md` (a transcrição e o texto dos slides, como vieram):
- **A fonte é a base:** o que o professor ensinou e o que ele enfatizou está nela; o card segue o que ele falou. A fala manda sobre o slide.
- **A apostila não entra** (regra do Mauricio, 10/11/2026): ela é produto da fonte e pode ter erros. Não a abra, nem para ordem, página, termo ou selo PROVA. Os capítulos do rascunho seguem a ordem em que o professor deu a aula (minutos da transcrição e slides).
- **Termo que a transcrição automática errou:** use o texto dos slides na fonte ou o termo médico correto.
- **Aula sem fonte** (as antigas): pare e peça a transcrição ao Mauricio; ela é guardada com `scripts/fonte-aula.py` antes de qualquer card.

Banco: Supabase, projeto `xtlpmtylifbalzxnfkib`, ferramenta `execute_sql` do conector. Tabela `public.flashcards (id, aula_id, ordem, frente, verso)`.

Arquivos temporários (lotes de SQL, scripts): ponha o id da aula no nome (ex.: `<aula-id>-lote1.sql`), porque outros agentes podem estar trabalhando em outras aulas ao mesmo tempo na mesma pasta, e apague-os no fim.

## Preparar

1. **Ache a aula.** "Gastro 1" = `gastro-a1`. Matérias: `nefro`, `pneumo`, `gastro`, `orto`, `uro`, `pass`. Confira numa consulta só:
   `select a.id, a.titulo, m.nome, (select count(*) from public.flashcards f where f.aula_id = a.id) as cards from public.aulas a join public.materias m on m.id = a.materia_id where a.id = '<aula-id>';`
   Se a aula já tiver cards, pare e diga quantos são, a menos que o pedido seja para refazer: aí prepare normalmente, sem ler nem completar os antigos. Antes da inclusão, o Mauricio apaga os antigos em Configurações → Conteúdo → a aula → "Apagar os N flashcards" (o conector não consegue apagar).
2. **Leia a fonte**, uma vez: `apostilas-fonte/<aula-id>/fonte.md`. Conte as palavras (`| wc -w`) para calibrar o tamanho.
3. **Monte os cards** com as regras abaixo, a partir da fonte, na ordem da aula, cobrindo a aula inteira.
4. **Escreva o rascunho** em `rascunhos/flashcards/<aula-id>.md` (a pasta fica fora do Git), no formato abaixo.
5. **Responda curto:** total de cards, quantos com PROVA, quantos fora da aula, as dúvidas (se houver) e o caminho do rascunho. Não cole os cards na resposta: quem chamou você mostra o arquivo ao Mauricio.

### O que entra

- **A aula inteira, com folga:** tudo o que o professor ensinou na fonte. Referência: Pneumo 1 (8.300 palavras de apostila) tem 171 cards; Pneumo 2 (6.000), 101; Pneumo 3 (7.100), 113. Uma transcrição tem umas duas vezes mais palavras que a apostila: conte uns 8 a 10 cards a cada mil palavras de fonte. Todo fato, número, critério, classificação, conduta e armadilha da aula vira card.
- **Pule** a conversa de sala que não ensina nada (chamada, avisos, piadas) e o que o professor diz que não cobra; não repita em dois cards o mesmo ponto que ele falou duas vezes.
- **Só o que está na fonte.** Não acrescente nada de fora (nada de "Fora da aula"). Se algo parecer errado, confuso ou contraditório (trecho ininteligível, o professor se corrigindo, fala e slide divergindo), não faça o card no escuro: siga a fala, e anote em "Dúvidas para o Mauricio", com o minuto ou o slide.
- **Erro da transcrição automática** (termo trocado por outro parecido): escreva o termo certo no card; se não tiver certeza de qual é, anote em "Dúvidas".
- **Parêntese do professor** (histórias de sala) só vira card quando ensina algo ("Por que a mulher tem mais constipação?").
- **Quadros de armadilha e alerta** viram cards que mostram onde está o erro.

### Como escrever

- **Frente:** pergunta curta e direta ("Qual é a definição de enfisema?"); comparação com × ("Asma × DPOC: o que muda…?"); mini-caso quando ajuda ("70 anos, PA 100 por 70…: quantos pontos e qual conduta?").
- **Verso:** a resposta em 1 a 3 frases, linguagem simples, sem tópicos. Uma lista grande vira vários cards ou uma pergunta do tipo "Quais são os 3 componentes…?".
- **"PROVA · "** no começo da frente quando o professor diz que cai na prova ou que é importante: seção com o selo PROVA no título (o texto sai como "Regra de Goodsall PROVA"), "cai em prova", "a prova gosta", "muito cobrada", "isso vocês precisam saber", "a definição importa muito", slides de "questões de prova". Marque também tudo o que o professor só dá a entender que é importante: fez questão de perguntar à turma ("o professor fez questão de perguntar cada tríade"), repetiu, frisou, insistiu, chamou a atenção. Na seção com o selo, todos os cards do assunto dela levam PROVA. Na dúvida, marque como PROVA, sem perguntar ao Mauricio: a regra é dele.
- Siglas por extenso na primeira vez. Nada de "o aluno deve saber": vá direto ao conteúdo.

Exemplos aprovados (Pneumo 2 e 3):
- "O que é pneumonia?" → "Infecção aguda do parênquima pulmonar. Em geral pega os alvéolos e o interstício, com resposta inflamatória e piora das trocas gasosas: por isso aparece hipoxemia."
- "PROVA · O que é pneumonia "adquirida na comunidade"?" → "Infecção pulmonar aguda adquirida fora do hospital, que aparece antes da internação ou nas primeiras 48 horas depois da admissão. O professor frisou: a definição importa muito."
- "Paciente internou hoje e a pneumonia apareceu 30 horas depois. É comunitária?" → "Sim. Até 48 horas após a admissão, ainda é pneumonia adquirida na comunidade."
- "PROVA · "O Haemophilus influenzae é o principal agente das pneumonias comunitárias…" Onde está a armadilha?" → "A frase continua: "…vírgula, após o pneumococo". O Haemophilus vem depois do pneumococo. Leia a frase até o fim."

### Formato do rascunho

Numeração contínua de 1 até o fim (o número vira a `ordem` e o id). Cada card em duas linhas: `**N.** frente` e, logo abaixo, `↳ verso`. Uma seção `##` para cada bloco da aula, na ordem em que o professor deu (com os minutos ou os slides).

```markdown
# Flashcards · Gastroenterologia 1 — Reto e ânus: continência, constipação e doenças orificiais

`gastro-a1` · 124 cards · 18 com PROVA · rascunho (ainda não está no banco)

## 01 · O intestino: muito além da evacuação (min. 00–09)

**1.** Qual é a principal função do cólon?
↳ Absorver sódio e água, recuperando o volume de líquido para que as fezes cheguem pastosas.

## Dúvidas para o Mauricio

- 23:40: …
```

Se não houver dúvidas, escreva "Nenhuma." nessa seção.

## Incluir

Só quando pedirem para incluir um rascunho aprovado. **Não reescreva os cards em SQL** (regra do Mauricio, 04/11/2026: é a parte mais cara e é mecânica): o programa lê o rascunho e grava.

1. `node scripts/gravar-rascunho.mjs <aula-id> --so-flashcards`. Ele lê `rascunhos/flashcards/<aula-id>.md` como está agora, confere que a aula tem 0 cards, grava em lotes de 60 (ids `<aula-id>-f01`… `-f99`, `-f100`; `ordem` = número do card; tira o "↳ "; mantém "PROVA · ") e confere a contagem no fim. Precisa da chave `SUPABASE_SECRET_KEY` no ambiente ou em `.env.local`.
2. Se ele parar (`PAROU: …`), corrija o rascunho quando o problema for de formato e rode de novo; se a aula já tem cards, diga quantos: o Mauricio apaga os antigos no botão "Apagar os N flashcards" da aula, em Configurações → Conteúdo.
3. **Sem a chave**: `node scripts/gravar-rascunho.mjs <aula-id> --so-flashcards --sql` escreve os lotes prontos em `rascunhos/sql/`; rode cada arquivo no conector (`execute_sql`), em ordem, e confira com `select count(*), min(ordem), max(ordem) from public.flashcards where aula_id = '<aula-id>';`.
4. Responda com o número de cards gravados. Não faça commit nem push.

Pelo conector, apagar e reescrever textos longos é cancelado: não tente. Card errado depois de gravado o Mauricio corrige em Configurações → Conteúdo.
