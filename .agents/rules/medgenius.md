---
trigger: always_on
---

# Med Genius: regras do Antigravity

Antes de qualquer trabalho, leia e siga o arquivo `AGENTS.md` na raiz do projeto (o manual vale para todos os assistentes) e os documentos que ele indica para o assunto.

Resumo do que vale para você:
- Responda em português do Brasil, em linguagem simples: o Mauricio não é programador.
- Trabalhe só num ramo `antigravity/<assunto>` criado a partir do `main` atualizado. Nunca empurre para o `main`.
- Antes de enviar: `npm test` e `npx next build`. Depois `git push -u origin antigravity/<assunto>` e `gh pr create --fill --base main`; o GitHub junta sozinho se o site compilar.
- Você tem o conector do Supabase (só o projeto `xtlpmtylifbalzxnfkib`). Siga as mesmas regras do Claude no `AGENTS.md`: veja a estrutura antes de mudar, corrija questões com versão nova (`-v2` + `substituida_por`), nunca apague nem reescreva textos longos (isso fica para o Mauricio em Conteúdo), não mexa em contas, senhas ou chaves. Mudança na estrutura do banco (tabelas, colunas, permissões) só com o "pode" do Mauricio.
- Um assunto por vez; não mexa numa tela que outro assistente esteja mudando.
