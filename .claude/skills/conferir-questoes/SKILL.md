---
name: "conferir-questoes"
description: "Use quando o Mauricio pedir para conferir as questões de uma aula do MedGenius (ex.: Nefrologia aula 1): resolve só pela fonte da aula (transcrição e slides), sem a apostila, e diz o que manter, corrigir ou tirar da aula."
---

# Conferir as questões de uma aula do MedGenius contra a fonte da aula

Objetivo: em cada aula do MedGenius, deixar só questões do tema da aula que dá para responder pelo que o professor ensinou, com o gabarito, o comentário e o "por que as erradas" batendo com a fonte da aula. O gabarito que veio com a prova original não decide nada.

**A referência é a fonte da aula** (regra do Mauricio, 09/11/2026): `apostilas-fonte/<aula-id>/fonte.md`, a transcrição e o texto dos slides. **A apostila não entra** (regra do Mauricio, 10/11/2026): é produto da fonte e pode ter erros; não a abra. Dentro da fonte, a fala manda sobre o slide; termo que a transcrição automática errou, vale o slide ou o termo médico correto. **Aula sem fonte** (as antigas): pare e peça a transcrição ao Mauricio.

## Onde está cada coisa

- **Aula**: id `<matéria>-a<N>`. Matérias: `nefro` (Nefrologia), `pneumo` (Pneumologia), `gastro` (Gastroenterologia), `orto` (Ortopedia), `uro` (Urologia), `pass` (PASS), `angio` (Angiologia); na dúvida, `select id, nome from materias`. "Nefrologia aula 1" = `nefro-a1`. Se ele disser só "aula 1", perguntar a matéria (cada matéria tem a sua aula 1).
- **Fonte da aula**: `apostilas-fonte/<aula-id>/fonte.md`. Leia uma vez. Página de slide marcada "só imagem": peça o original ao Mauricio só se a questão depender dela.
- **Questões**: Supabase, projeto `xtlpmtylifbalzxnfkib`, tabela `questoes`. Só leitura nesta etapa:

```sql
select q.id, q.ordem, q.enunciado, q.alternativas, q.correta, q.comentario, q.por_que_erradas,
       q.tema, q.origem, q.fonte,
       (select count(*) from respostas r where r.questao_id = q.id) as respondida_por,
       (select string_agg(rc.texto, ' | ') from recados rc
         where rc.questao_id = q.id and rc.tipo = 'erro') as erros_apontados
from questoes q
where q.aula_id = '<aula-id>' and q.substituida_por is null
order by q.ordem;
```

- `alternativas` é a lista sem letra; `correta` é o índice (0 = A, 1 = B...). Mostrar sempre com letra.
- `erros_apontados` são colegas avisando erro na questão: levar em conta.
- `origem = professor` quer dizer que o professor corrigiu em sala. Se a fonte discordar, não decidir sozinho: mostrar e perguntar.
- Sem o conector do Supabase (o Codex): rode o mesmo SQL com `node scripts/sql.mjs "<SQL>"` (`docs/codex.md`). Se o ambiente não estiver configurado, avise e peça ao Mauricio a lista das questões (Configurações → Conteúdo).

## Fluxo

1. **Identificar a aula** (`<aula-id>`) e confirmar o título com `select titulo from aulas where id = '<aula-id>'`.
2. **Ler a fonte inteira**, uma vez. Anotar o que o professor ensinou, os números, o que ele enfatizou (sinais de PROVA do `docs/apostila-molde.md`) e o que ele disse que cobra e que não cobra.
3. **Buscar as questões** com o SQL acima.
4. **Resolver cada questão só pela fonte**, sem olhar `correta`:
   - achar o trecho que responde (minuto ou slide na fonte);
   - definir a alternativa certa;
   - ver se outra alternativa também fica certa pela fonte;
   - ver se algum valor, dose, ponto de corte ou critério diverge da fonte.
   Só depois comparar com `correta`.
5. **Conferir o comentário e o "por que as erradas"**: o aluno lê esses textos depois de responder, então nada neles pode contradizer a fonte.
6. **Classificar:**
   - **Manter**: tudo bate.
   - **Corrigir**: gabarito errado, duas alternativas certas, dado divergente ou comentário que contradiz a fonte. Escrever a mudança exata.
   - **Fora desta aula**: a fonte não traz o que a questão cobra. Procurar nas fontes das outras aulas da matéria (`grep` em `apostilas-fonte/<materia>-a*/fonte.md`, sem ler tudo) para ver se ela é de outra aula.
   - **Só "Fora da aula"**: a resposta só existia num complemento da apostila (questão antiga). Ele decide.
7. **Cobertura**: listar os pontos que o professor disse que caem ou enfatizou e que ficaram sem nenhuma questão.
8. **Questões sem aula** (`aula_id is null` na mesma matéria): só dizer quantas existem e oferecer ver se alguma é desta aula.

## Resposta (no chat)

1. Resumo em uma linha: "Nefrologia aula 1: 12 questões, 9 manter, 2 corrigir, 1 fora da aula."
2. Tabela: Nº | Veredito | Pela fonte | No site | Onde está (minuto ou slide) | Observação.
3. Depois, uma questão problemática por vez: texto completo (enunciado e alternativas com letra), o problema, o trecho da fonte e a proposta. Esperar a decisão antes de passar para a próxima.
4. Pontos PROVA sem questão.

## Mudar o site: só depois do "sim" dele, uma questão por vez

- Nada é gravado durante a conferência.
- **Corrigir** (jeito aprovado do projeto): incluir uma versão nova `<id>-v2` (ou o próximo número), com todos os campos copiados, a correção aplicada e a mesma `ordem`; marcar a antiga com `update questoes set substituida_por = '<id>-v2' where id = '<id>'`; levar os recados com `update recados set questao_id = '<id>-v2' where questao_id = '<id>'`. As respostas antigas dos alunos ficam na versão antiga até a limpeza, que as apaga.
- **Tirar da aula**: se ela é de outra aula, `update questoes set aula_id = '<outra-aula>' where id = '<id>'`. Se não é de nenhuma, oferecer `aula_id = null` (ela continua no Banco de questões da matéria) ou que ele a apague em Conteúdo.
- Apagar e reescrever textos longos pelo conector são cancelados: isso ele faz em Configurações → Conteúdo. Não tentar contornar.
- No fim, oferecer a limpeza das versões antigas: ele aperta o botão em Administração → Conteúdo → Limpeza, ou pede e o assistente roda `node scripts/limpar-versoes.mjs` (mostra o que sai) e depois `--apagar`.

## Regras

- A referência é a fonte da aula, não o gabarito original, a apostila nem o conhecimento geral. Se a fonte parecer errada ou desatualizada, avisar à parte, sem mudar o veredito.
- Nunca inventar minuto ou slide. Se o trecho não existe, a questão não é respondível pela aula.
- Ele é sensível a custo: não reler a fonte nem reenviar textos longos sem necessidade; aula com muitas questões vai em blocos, mas todas são conferidas.
- Linguagem simples: ele não é programador.