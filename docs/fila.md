# Fila: quem está mexendo em quê

Claude, Codex e Antigravity podem fazer qualquer trabalho do app. Para dois não mexerem na mesma coisa ao mesmo tempo, cada um anota aqui o que vai fazer.

## Regras

1. **Antes de começar**, leia a fila como está no `main` agora:
   `git fetch origin main && git show origin/main:docs/fila.md`.
   Se outro assistente já está na mesma tela, aula, matéria ou arquivo, **não comece**: avise o Mauricio e espere.
2. **Anote** uma linha na tabela, num commit que muda **só este arquivo**, empurrado direto para o `main`:
   `git fetch origin main && git checkout -B fila origin/main`, edite, `git commit -am "Fila: <assunto>" && git push origin fila:main`, e volte ao seu ramo.
   É a única exceção à regra "nunca empurre direto para o `main`". A Vercel não publica commit que só mexe em documentos (`vercel.json`), então a anotação não gasta nada.
   Se você não consegue empurrar para o `main` (o Codex, por exemplo), escreva na descrição do PR "Fila: <assunto>"; quem publicar em seguida atualiza a tabela.
3. **Trabalhe** no seu ramo (`claude/…`, `codex/…`, `antigravity/…`), como diz o `AGENTS.md`.
4. **Ao publicar**, o mesmo PR que entrega o trabalho apaga a sua linha.
5. **Linha com mais de 3 dias** é dada como abandonada: pergunte ao Mauricio antes de assumir o assunto ou de apagar a linha.
6. "Onde" é o que vai mudar: a tela (`Revisão`, `Início`…), a aula (`gastro-a4`), a matéria, ou o arquivo (`lib/srs.ts`). Seja específico; "o app inteiro" bloqueia todo mundo.

## Em andamento

| Assunto | Quem | Ramo | Onde | Desde |
|---|---|---|---|---|
| Agenda: publicar o cronograma colado na conversa na hora | Claude | claude/bold-gates-kuv9jp | scripts/publicar-agenda.mjs, AGENTS.md | 08/11/2026 |
