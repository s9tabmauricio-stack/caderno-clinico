# Como publicar (os três assistentes)

Resumo no `AGENTS.md`; aqui o passo a passo.

- **Um caminho só.** Comece de um `main` atualizado, num ramo `claude/<…>`, `codex/<…>` ou `antigravity/<…>` (nenhum gera prévia na Vercel, `vercel.json`). Rode `npm test` e `npx next build`, empurre o ramo e abra um PR para o `main`. O GitHub roda os testes e a compilação e junta sozinho (`.github/workflows/juntar-ao-main.yml`); se algo falhar, o PR fica aberto e nada vai para o ar.
- **PR em rascunho não é juntado**: use rascunho quando o Mauricio pediu para ver antes, e tire do rascunho no "pode publicar".
- Nunca empurre direto para o `main` nem use ramos com outro nome.
- **Antigravity:** `git fetch origin main && git checkout -B antigravity/<assunto> origin/main`; no fim, `git push -u origin antigravity/<assunto>` e `gh pr create --fill --base main`.
- **Codex:** ramo `codex/<assunto>` a partir do `main`.
- **Claude na nuvem** (claude.ai/code, app do celular): usa o ramo `claude/...` da sessão. Depois de juntado, o PR não recebe mais nada: o trabalho seguinte começa de novo do `main`, num PR novo.
- **Exceções, que publicam direto** (não esperam aprovação): a aula nova e o Claude no computador do Mauricio, com `git fetch origin main && git rebase origin/main && git push origin HEAD:main` (e empurram também o ramo da sessão).
- Commit que só mexe em documentos (`docs/`, arquivos `.md`, `.claude/`, `.agents/`) não gera publicação na Vercel (`ignoreCommand` no `vercel.json`), para não gastar o "Deployment Storage".
