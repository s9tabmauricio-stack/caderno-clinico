---
trigger: always_on
---

# Med Genius: regras do Antigravity

Antes de qualquer trabalho, leia e siga o arquivo `AGENTS.md` na raiz do projeto (o manual vale para todos os assistentes) e os documentos que ele indica para o assunto.

Resumo do que vale para você:
- Responda em português do Brasil, em linguagem simples: o Mauricio não é programador.
- **Fila** (`docs/fila.md`): antes de começar, leia a fila no `main` (`git fetch origin main && git show origin/main:docs/fila.md`). Se outro assistente já está na mesma tela, aula ou arquivo, não comece e avise o Mauricio. Se estiver livre, anote sua linha (o passo a passo está no topo do arquivo). Ao publicar, o seu PR apaga a linha.
- Trabalhe só num ramo `antigravity/<assunto>` criado a partir do `main` atualizado. Nunca empurre para o `main`; a única exceção é a anotação da fila.
- Antes de enviar: `npm test` e `npx next build`. Depois `git push -u origin antigravity/<assunto>` e `gh pr create --fill --base main`; o GitHub (`.github/workflows/juntar-ao-main.yml`) junta sozinho se os testes passarem e o site compilar. Se o Mauricio pediu para ver antes, abra como rascunho (`--draft`).
- Conteúdo (apostila, questões, flashcards, provas): siga a skill do assunto em `.claude/skills/` e os agentes em `.claude/agents/` como manual; valem para você também.
  - Gravar flashcards e questões revisados: `node scripts/gravar-rascunho.mjs <aula-id>` (chave `SUPABASE_SECRET_KEY` no `.env.local`, fora do Git); não reescreva o conteúdo em SQL.
  - Gerar o PDF de uma apostila: `apostilas-fonte/ferramentas/preparar.sh <pasta>` copia CSS, `render.py`, `checar.py` e a fonte; nunca os redigite.
- Tudo o que o app precisa fica no projeto (desenhos das telas em `docs/quadros/`). Passo a passo de publicação: `docs/publicar.md`.
- Você tem o conector do Supabase (só o projeto `xtlpmtylifbalzxnfkib`). Siga as mesmas regras do Claude no `AGENTS.md`: veja a estrutura antes de mudar, corrija questões com versão nova (`-v2` + `substituida_por`), nunca apague nem reescreva textos longos (isso fica para o Mauricio em Conteúdo), não mexa em contas, senhas ou chaves. Mudança na estrutura do banco (tabelas, colunas, permissões) não precisa mais do "pode" do Mauricio (regra dele, 05/11/2026): veja a estrutura antes, atualize `supabase/estrutura-atual.sql` depois e conte a ele em uma frase o que mudou.
- Um assunto por vez, sempre anotado na fila.
