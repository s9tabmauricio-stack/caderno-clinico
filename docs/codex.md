# Codex com acesso ao banco

O Codex (no site do ChatGPT, chatgpt.com/codex) não tem o conector do Supabase que o Claude e o Antigravity usam.
No lugar dele, usa o programa `scripts/sql.mjs`, que roda qualquer SQL no banco (ler, incluir, alterar e mudar
a estrutura), igual ao `execute_sql` do conector. Para isso, o ambiente do Codex precisa de duas coisas, que só
o Mauricio configura (uma vez).

## 1. Criar o token do Supabase

1. Entre em https://supabase.com/dashboard/account/tokens (logado na conta dona do projeto `xtlpmtylifbalzxnfkib`).
2. **Generate new token**, nome `codex`, copie o valor (começa com `sbp_`). Ele só aparece uma vez.

O token dá acesso a todos os projetos dessa conta do Supabase: guarde só no Codex. Se vazar, apague-o na
mesma página e crie outro.

## 2. Configurar o ambiente do Codex

Em chatgpt.com/codex → **Settings → Environments** → o ambiente do `caderno-clinico` → **Edit**:

1. **Environment variables** (não em "Secrets": os segredos somem depois da preparação e o agente não os vê):
   - `SUPABASE_ACCESS_TOKEN` = o token do passo 1;
   - `SUPABASE_SECRET_KEY` = a mesma chave secreta da Vercel (para o `scripts/gravar-rascunho.mjs`).
2. **Agent internet access** → **On**, com a lista de endereços permitidos:
   - `api.supabase.com`
   - `xtlpmtylifbalzxnfkib.supabase.co`
3. Salve. Vale para as próximas tarefas.

Para conferir, peça ao Codex: `node scripts/sql.mjs "select id, titulo from aulas order by id limit 3"`.

## Como o Codex usa

- Onde as receitas (`.claude/skills/`, `.claude/agents/`) mandam usar o conector (`execute_sql`), o Codex roda
  `node scripts/sql.mjs "<o mesmo SQL>"` (ou grava o SQL num arquivo `.sql` e passa o caminho).
- Rascunhos revisados de flashcards e questões vão pelo `node scripts/gravar-rascunho.mjs <aula-id>`, como para todos.
- As regras do banco são as mesmas (seção "Limite do conector do Supabase" do `AGENTS.md`): corrigir questão é
  versão nova + `substituida_por`; apagar conteúdo é com o Mauricio em Conteúdo → Limpeza; mudou a estrutura,
  atualize `supabase/estrutura-atual.sql` no mesmo trabalho.
- Se o programa disser que falta o token ou que não há conexão, o ambiente não está configurado: avise o Mauricio
  apontando este arquivo e pare a parte do banco.
