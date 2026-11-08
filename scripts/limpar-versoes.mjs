#!/usr/bin/env node
// Limpa as versões antigas de questões corrigidas (as que têm substituida_por preenchido),
// fazendo o mesmo que o botão Administração → Conteúdo → Limpeza. Existe porque o conector do
// Supabase cancela qualquer comando que apaga (trava de confirmação que a conversa não mostra).
//
// Uso:
//   node scripts/limpar-versoes.mjs            só mostra o que seria apagado (não apaga nada)
//   node scripts/limpar-versoes.mjs --apagar   apaga de verdade (só quando o Mauricio pedir)
//
// Só mexe em versões antigas: aulas, questões no ar e flashcards ficam de fora.
// Os recados da turma passam para a versão que está no ar; as respostas e o histórico
// dados na versão antiga são apagados junto (o aluno vê a questão como não respondida).
// Precisa da chave secreta do Supabase em SUPABASE_SECRET_KEY (variável do ambiente ou
// arquivo .env.local, que nunca vai para o Git).

const URL_PADRAO = 'https://xtlpmtylifbalzxnfkib.supabase.co' // igual a lib/supabase/config.ts
const apagar = process.argv.includes('--apagar')

function parar(msg) {
  console.error('PAROU: ' + msg)
  process.exit(1)
}

try { process.loadEnvFile('.env.local') } catch { /* sem .env.local: usa o ambiente */ }
const chave = process.env.SUPABASE_SECRET_KEY
if (!chave) parar('falta a chave SUPABASE_SECRET_KEY no ambiente (ou em .env.local). Sem ela, o Mauricio limpa pelo botão em Administração → Conteúdo → Limpeza.')

const { createClient } = await import('@supabase/supabase-js')
const db = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL ?? URL_PADRAO, chave, {
  auth: { persistSession: false, autoRefreshToken: false },
})

async function consulta(promessa, oque) {
  const { data, error, count } = await promessa
  if (error) parar(`${oque}: ${error.message}`)
  return { data, count }
}

function blocos(lista, n = 100) {
  const saida = []
  for (let i = 0; i < lista.length; i += n) saida.push(lista.slice(i, i + n))
  return saida
}

const { data: antigas } = await consulta(
  db.from('questoes').select('id, aula_id, materia_id, ordem, substituida_por').not('substituida_por', 'is', null).order('materia_id').order('aula_id').order('ordem'),
  'ler as versões antigas',
)
if (!antigas.length) {
  console.log('Nenhuma versão antiga para limpar.')
  process.exit(0)
}

const ids = antigas.map((q) => q.id)
const respostas = new Map()
for (const parte of blocos(ids)) {
  const { data } = await consulta(db.from('respostas').select('questao_id').in('questao_id', parte), 'contar as respostas')
  for (const r of data) respostas.set(r.questao_id, (respostas.get(r.questao_id) ?? 0) + 1)
}

// Versão no ar de cada antiga (segue a corrente: v1 → v2 → v3).
const proxima = new Map(antigas.map((q) => [q.id, q.substituida_por]))
function versaoNoAr(id) {
  let atual = proxima.get(id)
  for (let i = 0; i < 20 && proxima.has(atual); i++) atual = proxima.get(atual)
  return atual
}

const porAula = new Map()
for (const q of antigas) {
  const onde = q.aula_id ?? `${q.materia_id} (sem aula)`
  const g = porAula.get(onde) ?? { qtd: 0, resp: 0, lista: [] }
  g.qtd++
  g.resp += respostas.get(q.id) ?? 0
  g.lista.push(`${q.id} → ${versaoNoAr(q.id)}${respostas.get(q.id) ? ` (${respostas.get(q.id)} resp.)` : ''}`)
  porAula.set(onde, g)
}
const totalResp = [...respostas.values()].reduce((a, b) => a + b, 0)
console.log(`${antigas.length} versões antigas; ${totalResp} respostas de alunos somem junto.\n`)
for (const [onde, g] of porAula) {
  console.log(`${onde}: ${g.qtd} versões antigas, ${g.resp} respostas`)
  for (const l of g.lista) console.log('  ' + l)
}

if (!apagar) {
  console.log('\nNada foi apagado. Para apagar de verdade: node scripts/limpar-versoes.mjs --apagar')
  process.exit(0)
}

// Mesma ordem do botão Limpeza (app/admin/conteudo/acoes.ts).
for (const q of antigas) {
  await consulta(db.from('recados').update({ questao_id: versaoNoAr(q.id) }).eq('questao_id', q.id), `mover os recados de ${q.id}`)
}
for (const parte of blocos(ids)) {
  await consulta(db.from('respostas').delete().in('questao_id', parte), 'apagar as respostas das versões antigas')
}
for (const parte of blocos(ids)) {
  await consulta(db.from('questoes').update({ substituida_por: null }).in('substituida_por', parte), 'soltar a corrente de versões')
}
for (const parte of blocos(ids)) {
  await consulta(db.from('questoes').delete().in('id', parte), 'apagar as versões antigas')
}
const { count } = await consulta(
  db.from('questoes').select('id', { count: 'exact', head: true }).not('substituida_por', 'is', null),
  'conferir',
)
console.log(`\nApagadas. Versões antigas que sobraram: ${count}.`)
