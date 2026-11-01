---
name: melhorar
description: Melhora um pedido do Mauricio antes de executar. Reescreve o comando seguindo os manuais da Anthropic e recomenda modelo, esforço e se vale usar o ultracode. Use com /melhorar <pedido>, ou quando ele pedir "melhore meu pedido/comando/prompt" ou perguntar que modelo, esforço ou ultracode usar.
argument-hint: <o seu pedido, do jeito que vier>
---

# Melhorar o pedido e dizer como rodar

O Mauricio escreve rápido, às vezes pelo celular. Aqui você só devolve o pedido melhorado e a recomendação de como rodar. **Não execute o pedido neste turno.** Não explore o projeto e não use agentes nem workflows, mesmo com o ultracode ligado. A resposta deve ser curta e barata.

Pedido: $ARGUMENTS

Se o pedido vier vazio, use a última mensagem dele antes do /melhorar. Se não houver nenhuma, peça o pedido em uma linha.

## 1. Entender

- O manual (`AGENTS.md`) já está carregado: use o que ele diz. Pode conferir uma coisa rápida para acertar um nome (o id da aula, o arquivo da tela), sem sair lendo o projeto.
- Se faltar algo que só ele sabe e que muda o resultado (qual aula, o que está errado, como deve ficar), pergunte no máximo duas coisas, cada uma em uma frase e com opções. Fora isso, decida pelo manual.
- Nunca invente fatos. Um detalhe útil que só ele sabe, mas que não é essencial, entra no pedido entre colchetes para ele preencher: `[em qual questão você viu?]`.

## 2. Reescrever

Siga os manuais da Anthropic: coloque no pedido só o que o Claude não descobre lendo o projeto.

1. **O objetivo e o porquê.** O que ele quer e para quê ("os alunos reclamaram que…", "para a P2 de 10/11"). Com o motivo, o Claude acerta os casos que o pedido não cobre.
2. **Onde.** A tela, a aula (`gastro-a4`), a matéria ou o arquivo. Se for um erro, o sintoma exato. Se ele tem o material (print, PDF, áudio, mensagem do WhatsApp), o pedido diz para anexar em vez de descrever.
3. **Como saber que ficou pronto.** O que ele vai ver quando estiver certo e como o Claude confere sozinho: rodar `npx next build`, abrir a tela e tirar print no celular e no tablet, comparar com a apostila, contar no banco. Peça a prova: o comando e o resultado, ou o print.
4. **O tamanho.** Se ele quer a versão completa (estados vazios, erros, celular e tablet), o pedido diz isso. Se ele quer só aquilo, o pedido diz o que não mexer.
5. **As preferências**, se ele tiver uma entre dois caminhos razoáveis.
6. **O que ele quer ver antes.** Para conteúdo ou visual que ele queira aprovar: "me mostre antes de publicar".
7. **Peça o que fazer, não o que evitar**: "frases curtas" funciona melhor do que "não escreva textão".
8. **Se ele ainda não sabe bem o que quer**, troque o pedido por uma entrevista: "Me faça perguntas de múltipla escolha até dar para escrever o plano; escreva o plano em `rascunhos/` e espere minha aprovação."

Não coloque:

- **O que já está no manual** (limites do Supabase, nomes das telas, padrão dos flashcards). O Claude já lê o manual.
- **"Pense passo a passo", "seja minucioso", "não pare até terminar", IMPORTANTE ou MAIÚSCULAS.** Hoje isso não ajuda (o controle certo é o esforço) e pode fazer o Claude exagerar.
- **Um passo a passo detalhado quando basta dizer o resultado.** Vale ainda mais no Fable: descreva o resultado e deixe que ele planeje.
- **Dois assuntos juntos.** Separe em dois pedidos (regra dele: um assunto por vez).
- **Uma receita que já existe.** Se há skill ou agente para aquilo (`aula-nova`, `flashcards`, `questoes`, `conteudo`, `revisor`, `conferir-questoes`, `apostila-padrao`, `bula-padrao`), o pedido chama por ela e não reescreve a receita.

Deixe o pedido curto, em geral de 3 a 8 linhas, em português simples, do jeito que ele falaria.

## 3. Recomendar modelo, esforço e ultracode

Escolha o mais barato que dá conta do pedido (regra dele: custo). Os agentes de conteúdo (`apostila`, `conteudo`, `flashcards`, `questoes`, `revisor`) já rodam em Opus com esforço extra-alto por conta própria, porque está no arquivo de cada um. A conversa principal não precisa subir de modelo nem de esforço por causa deles.

**Modelo** (`/model <nome>`, ou o seletor de modelo do app). Os custos são por palavra e vêm da tabela de preços da Anthropic.

- **Sonnet** (`/model sonnet`, cerca de metade do custo do Opus). Para trabalho rotineiro e bem descrito: trocar um texto, uma cor ou uma ordem na tela, ajuste mecânico, pergunta sobre o que já está aberto.
- **Opus** (o padrão, `/model opus`). Para a maior parte do trabalho: tela ou função nova, bug, mudança no banco, aula nova, conteúdo.
- **Fable** (`/model fable`, cerca de 2,5 vezes o custo do Opus). Só para o que é difícil e aberto:
  - um bug que o Opus já errou mesmo com o contexto certo;
  - descobrir a causa de um problema estranho;
  - uma decisão grande sobre a estrutura do projeto;
  - uma tarefa longa que você normalmente quebraria em várias.

  Pode cobrar créditos à parte: o seletor mostra "Requires usage credits". Os filtros de segurança do Fable às vezes passam a resposta para outro modelo em assuntos de biologia.
- **Haiku** (`/model haiku`). Quase nunca na conversa principal; só para coisas mínimas, como uma pergunta rápida. Na dúvida, use o Sonnet.

Regra de bolso do manual da Anthropic: se o Claude errou por **falta de conhecimento**, suba o modelo. Se errou por **falta de capricho** (não leu os arquivos, não testou), suba o esforço. Antes de subir qualquer um dos dois, veja se faltou contexto no pedido.

**Esforço** (`/effort <nível>`, ou o controle de esforço do app, se aparecer):

- **baixo** (`low`): ida e volta rápida em que ele confere cada resultado, como ideia, rascunho, troca de texto ou renomear.
- **médio** (`medium`, o padrão do Opus e do Sonnet): o dia a dia com escopo claro, como uma função nova ou um ajuste de tela.
- **alto** (`high`): quando errar custa caro ou quando é fácil esquecer um caso. Por exemplo: bug no site, mudança no banco ou em várias telas, algo que a turma usa na hora da prova.
- **extra-alto** (`xhigh`): raciocínio mais fundo e mais caro, para um bug difícil ou uma mudança grande.
- **máximo** (`max`): quase nunca. Serve para um problema difícil que o Claude resolve sozinho, como procurar falha de segurança. Tende a pensar demais.
- Se só **uma** pergunta difícil precisa de mais, no meio de uma conversa comum, escreva `ultrathink` nessa mensagem em vez de mudar o esforço.

**Ultracode.** Com ele, o Claude monta um *workflow*: um roteiro que põe vários agentes trabalhando ao mesmo tempo e conferindo o trabalho uns dos outros.

- **Sim**, só quando a mesma tarefa se repete em muitas coisas ou precisa de conferência cruzada. Por exemplo: conferir todas as questões de uma matéria contra a apostila, revisar todas as telas, procurar um tipo de erro no projeto inteiro, pesquisar em muitas fontes.
  - Recomende a palavra no começo do pedido (`ultracode: …`): ela vale só para aquele pedido.
  - Não recomende `/effort ultracode`, que fica ligado na conversa toda e encarece cada pedido seguinte.
  - Sugira testar numa parte pequena primeiro (uma aula ou uma matéria, antes de todas).
  - Avise que, depois de começar, o workflow não para para perguntar nada.
- **Não**, para todo o resto. Nunca na aula nova: a receita já organiza os agentes e proíbe agentes extras. O ultracode gasta bem mais, porque cada agente tem seu custo, e consome o limite do plano mais rápido.

**Conversa nova.** Recomende uma conversa nova (ou `/clear`) quando o pedido for de outro assunto ou quando o modelo recomendado for diferente do atual. Trocar de modelo no meio da conversa obriga o Claude a reler a conversa inteira sem o desconto do cache, e numa conversa focada ele erra menos.

## 4. Responder neste formato

```
**Pedido melhorado** (copie e mande):
> …

**O que mudei:** 1 a 3 itens curtos, em linguagem simples.

**Como rodar**
- Modelo: … · `/model …` · porque …
- Esforço: … · `/effort …` · porque …
- Ultracode: sim/não · porque …
- Conversa nova: sim · porque …   ← só quando valer
```

Termine com uma linha: "Se já estiver nesse modelo e esforço, diga **pode fazer** que eu faço agora." Quando ele disser "pode fazer", execute o pedido melhorado como um pedido comum.

## Exemplos

<examples>
<example>
Pedido: "o botao copiar ta copiando o gabarito junto"

**Pedido melhorado** (copie e mande):
> Na questão, o botão Copiar está levando o gabarito junto [em qual matéria/questão você viu?]. Ele deve copiar só o enunciado e as alternativas (A) …, B) …), sem gabarito nem comentário, tanto antes quanto depois de responder. Ache a causa e corrija. Para conferir, copie uma questão respondida e uma não respondida e me mostre o texto copiado nas duas.

**O que mudei:** disse como deve ficar e em que situações testar; pedi a prova (o texto copiado).

**Como rodar**
- Modelo: Opus · `/model opus` · é um bug numa tela que a turma toda usa.
- Esforço: alto · `/effort high` · precisa achar a causa e testar os dois casos.
- Ultracode: não · é uma correção só.
</example>

<example>
Pedido: "muda a cor do botao da revisao pra verde"

Antes de reescrever, avise numa frase: pelo manual, verde é só para "certo", e a ação principal usa titânio. Pergunte se ele quer mesmo o verde ou só um botão mais destacado. Se ele confirmar o verde:

**Pedido melhorado** (copie e mande):
> Na tela Revisão, deixe o botão principal verde, como o verde de "certo" do tema, nos modos dia e noite. Não mexa nos outros botões. Me mande um print no celular nos dois modos.

**Como rodar**
- Modelo: Sonnet · `/model sonnet` · troca simples e bem descrita.
- Esforço: baixo · `/effort low` · você vai conferir pelo print.
- Ultracode: não.
- Conversa nova: sim · troca de modelo.
</example>

<example>
Pedido: "confere se as questoes de nefro tao certas"

**Pedido melhorado** (copie e mande):
> ultracode: confira as questões da nefro-a1 contra a apostila da aula, usando a skill conferir-questoes. Para cada questão, diga se mantém, corrige ou tira, com o motivo e o trecho da apostila. Não grave nada no banco: só me entregue a lista. Se der certo, depois eu peço as outras aulas de Nefrologia.

**O que mudei:** comecei por uma aula só, para ver o custo antes das outras; pedi a lista sem gravar nada.

**Como rodar**
- Modelo: Opus · `/model opus` · é conteúdo médico, e a qualidade é regra sua.
- Esforço: alto · `/effort high` · cada gabarito precisa ser conferido.
- Ultracode: sim, com a palavra no começo do pedido · são muitas questões e vale conferência cruzada; teste numa aula antes das outras.
</example>
</examples>

## Fontes

Conferidas em 01/11/2026. Se algo mudar no Claude Code, atualize aqui.

- Boas práticas do Claude Code: https://code.claude.com/docs/en/best-practices
- Modelos e esforço: https://code.claude.com/docs/en/model-config
- Workflows e ultracode: https://code.claude.com/docs/en/workflows
- Como escrever pedidos (Anthropic): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Escolher modelo e esforço: https://claude.com/resources/articles/claude-model-and-effort-level-in-claude-code
