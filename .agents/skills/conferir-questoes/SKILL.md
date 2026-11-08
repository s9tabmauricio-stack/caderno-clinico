---
name: "conferir-questoes"
description: "Use quando o Mauricio pedir para conferir as questões de uma aula do MedGenius contra a apostila (ex.: Nefrologia aula 1): resolve pela apostila e diz o que manter, corrigir ou tirar da aula."
---

# Conferir as questões de uma aula do MedGenius contra a apostila

Objetivo: em cada aula do MedGenius, deixar só questões do tema da aula que dá para responder pela apostila dela, com o gabarito, o comentário e o "por que as erradas" batendo com a apostila. O gabarito que veio com a prova original não decide nada.

## Onde está cada coisa

- **Aula**: id `<matéria>-a<N>`. Matérias: `nefro` (Nefrologia), `pneumo` (Pneumologia), `gastro` (Gastroenterologia), `orto` (Ortopedia), `uro` (Urologia), `pass` (PASS), `angio` (Angiologia); na dúvida, `select id, nome from materias`. "Nefrologia aula 1" = `nefro-a1`. Se ele disser só "aula 1", perguntar a matéria (cada matéria tem a sua aula 1).
- **Apostila**: `public/apostilas/<aula-id>/apostila.pdf`, no próprio projeto. Leia o texto uma vez com `python3 -I scripts/apostila-texto.py public/apostilas/<aula-id>/apostila.pdf` (guarda os selos PROVA, que o `pdftotext` perde). Para tabela, régua ou figura, olhe só a imagem daquela página (`public/apostilas/<aula-id>/NN.webp`).
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
- `origem = professor` quer dizer que o professor corrigiu em sala. Se a apostila discordar, não decidir sozinho: mostrar e perguntar.
- Sem o conector do Supabase (o Codex): rode o mesmo SQL com `node scripts/sql.mjs "<SQL>"` (`docs/codex.md`). Se o ambiente não estiver configurado, avise e peça ao Mauricio a lista das questões (Configurações → Conteúdo).

## Fluxo

1. **Identificar a aula** (`<aula-id>`) e confirmar o título com `select titulo from aulas where id = '<aula-id>'`.
2. **Ler a apostila inteira.** Anotar seções (número e título) e página, valores, doses, critérios, marcas PROVA, caixas "Complemento: fora da aula" e o que o professor disse que cobra e que não cobra.
3. **Buscar as questões** com o SQL acima.
4. **Resolver cada questão só pela apostila**, sem olhar `correta`:
   - achar o trecho que responde (seção e página);
   - definir a alternativa certa;
   - ver se outra alternativa também fica certa pela apostila;
   - ver se algum valor, dose, ponto de corte ou critério diverge da apostila.
   Só depois comparar com `correta`.
5. **Conferir o comentário e o "por que as erradas"**: o aluno lê esses textos depois de responder, então nada neles pode contradizer a apostila.
6. **Classificar:**
   - **Manter**: tudo bate.
   - **Corrigir**: gabarito errado, duas alternativas certas, dado divergente ou comentário que contradiz a apostila. Escrever a mudança exata.
   - **Fora da apostila**: a apostila não traz o que a questão cobra. Procurar no texto das outras apostilas da matéria (`scripts/apostila-texto.py` + `grep`, sem ler tudo) para ver se ela é de outra aula.
   - **Só pelo complemento**: a resposta está apenas numa caixa roxa. Ele decide.
7. **Cobertura**: listar os pontos com marca PROVA que ficaram sem nenhuma questão.
8. **Questões sem aula** (`aula_id is null` na mesma matéria): só dizer quantas existem e oferecer ver se alguma é desta aula.

## Resposta (no chat)

1. Resumo em uma linha: "Nefrologia aula 1: 12 questões, 9 manter, 2 corrigir, 1 fora da apostila."
2. Tabela: Nº | Veredito | Pela apostila | No site | Onde está na apostila | Observação.
3. Depois, uma questão problemática por vez: texto completo (enunciado e alternativas com letra), o problema, o trecho da apostila e a proposta. Esperar a decisão antes de passar para a próxima.
4. Pontos PROVA sem questão.
5. "Possível erro na apostila", só se houver.

## Mudar o site: só depois do "sim" dele, uma questão por vez

- Nada é gravado durante a conferência.
- **Corrigir** (jeito aprovado do projeto): incluir uma versão nova `<id>-v2` (ou o próximo número), com todos os campos copiados, a correção aplicada e a mesma `ordem`; marcar a antiga com `update questoes set substituida_por = '<id>-v2' where id = '<id>'`; levar os recados com `update recados set questao_id = '<id>-v2' where questao_id = '<id>'`. As respostas antigas dos alunos ficam na versão antiga até a limpeza, que as apaga.
- **Tirar da aula**: se ela é de outra aula, `update questoes set aula_id = '<outra-aula>' where id = '<id>'`. Se não é de nenhuma, oferecer `aula_id = null` (ela continua no Banco de questões da matéria) ou que ele a apague em Conteúdo.
- Apagar e reescrever textos longos pelo conector são cancelados: isso ele faz em Configurações → Conteúdo. Não tentar contornar.
- No fim, oferecer a limpeza das versões antigas: ele aperta o botão em Administração → Conteúdo → Limpeza, ou pede e o assistente roda `node scripts/limpar-versoes.mjs` (mostra o que sai) e depois `--apagar`.

## Regras

- A referência é a apostila, não o gabarito original nem o conhecimento geral. Se a apostila parecer errada ou desatualizada, avisar à parte, sem mudar o veredito.
- Nunca inventar seção ou página. Se o trecho não existe, a questão não é respondível pela apostila.
- Ele é sensível a custo: não reler a apostila nem reenviar textos longos sem necessidade; aula com muitas questões vai em blocos, mas todas são conferidas.
- Linguagem simples: ele não é programador.