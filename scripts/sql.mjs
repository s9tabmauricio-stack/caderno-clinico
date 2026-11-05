#!/usr/bin/env node
// Roda SQL no banco do Med Genius sem o conector do Supabase (feito para o Codex,
// que não tem o conector; serve para qualquer assistente). Faz o mesmo que o
// execute_sql do conector: ler, incluir, alterar e mudar a estrutura.
//
// Uso:
//   node scripts/sql.mjs "select id, titulo from aulas order by id"
//   node scripts/sql.mjs arquivo.sql
//   echo "select 1" | node scripts/sql.mjs
//
// Precisa do token pessoal do Supabase em SUPABASE_ACCESS_TOKEN (variável do ambiente
// ou .env.local, que nunca vai para o Git). Como configurar o Codex: docs/codex.md.
// Imprime o resultado em JSON. As regras do banco (AGENTS.md, "Limite do conector")
// valem igual: corrigir questão = versão nova + substituida_por.
import { existsSync, readFileSync } from 'node:fs'

const PROJETO = 'xtlpmtylifbalzxnfkib'

function parar(msg) {
  console.error('PAROU: ' + msg)
  process.exit(1)
}

try { process.loadEnvFile('.env.local') } catch { /* sem .env.local: usa o ambiente */ }
const token = process.env.SUPABASE_ACCESS_TOKEN
if (!token) parar('falta SUPABASE_ACCESS_TOKEN no ambiente (ou em .env.local). Veja docs/codex.md.')

const arg = process.argv.slice(2).join(' ').trim()
let sql = arg
if (arg && /\.sql$/i.test(arg) && existsSync(arg)) sql = readFileSync(arg, 'utf8')
if (!sql && !process.stdin.isTTY) sql = readFileSync(0, 'utf8')
if (!sql.trim()) parar('diga o SQL. Ex.: node scripts/sql.mjs "select id from aulas"')

let resp
try {
  resp = await fetch(`https://api.supabase.com/v1/projects/${PROJETO}/database/query`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: sql }),
  })
} catch (e) {
  parar(`sem conexão com api.supabase.com (${e.cause?.message ?? e.message}). No Codex, libere a internet do agente para api.supabase.com (docs/codex.md).`)
}
const texto = await resp.text()
if (!resp.ok) parar(`o Supabase recusou (${resp.status}): ${texto}`)
try {
  console.log(JSON.stringify(JSON.parse(texto), null, 2))
} catch {
  console.log(texto)
}
