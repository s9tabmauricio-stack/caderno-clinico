#!/usr/bin/env node
// Publica na Agenda o cronograma semanal colado do WhatsApp, igual ao botão de Administração → Agenda.
//
// Uso:
//   node scripts/publicar-agenda.mjs <arquivo.txt>             publica a semana
//   node scripts/publicar-agenda.mjs <arquivo.txt> --conferir  só mostra o que leu, não grava
//   (sem arquivo, lê o texto da entrada padrão)
//
// Usa o mesmo leitor das telas (lib/agenda.ts). A semana publicada substitui a versão anterior
// da mesma semana; as provas incluídas à parte (fixo) ficam. Precisa da chave secreta do Supabase
// em SUPABASE_SECRET_KEY (variável do ambiente ou arquivo .env.local, que nunca vai para o Git).
// Sem a chave: cole o texto em /admin/agenda.
import { readFileSync } from 'node:fs'
import { lerCronograma } from '../lib/agenda.ts'

const URL_PADRAO = 'https://xtlpmtylifbalzxnfkib.supabase.co' // igual a lib/supabase/config.ts

const args = process.argv.slice(2)
const arquivo = args.find((a) => !a.startsWith('--'))
const conferir = args.includes('--conferir')

function parar(msg) {
  console.error('PAROU: ' + msg)
  process.exit(1)
}

const texto = readFileSync(arquivo ?? 0, 'utf8').trim()
if (!texto) parar('o texto do cronograma está vazio.')

const ano = Number(process.env.ANO_AGENDA) || new Date().getFullYear()
const s = lerCronograma(texto, ano)
const aulas = s.eventos.filter((e) => e.tipo !== 'aviso' && !e.cancelado)
if (!s.dias.length || !aulas.length) {
  parar('não encontrei dias nem horários. O texto precisa de linhas como "SEGUNDA-FEIRA | 5/outubro" e "8h-10h: aula ...".')
}

const hora = (h) => h ?? '--:--'
console.log(`Semana de ${s.semana}${s.titulo ? ` (${s.titulo})` : ''}`)
for (const d of s.dias) {
  console.log(`\n${d}`)
  for (const e of s.eventos.filter((x) => x.data === d)) {
    const grupos = e.grupos ? ` · grupos ${e.grupos.join(', ')}` : ''
    console.log(`  ${e.cancelado ? 'CANCELADA ' : ''}${hora(e.inicio)}-${hora(e.fim)} [${e.materia ?? '?'}/${e.tipo}] ${e.titulo}${e.professor ? ` · ${e.professor}` : ''}${e.local ? ` · ${e.local}` : ''}${grupos}`)
  }
}
const resumo = `${aulas.length} aulas, ${s.eventos.filter((e) => e.cancelado).length} cancelamentos, ` +
  `${s.eventos.filter((e) => e.tipo === 'prova' && !e.cancelado).length} provas e ${s.eventos.filter((e) => e.tipo === 'aviso').length} avisos`
if (conferir) {
  console.log(`\nSó conferência (nada gravado): ${resumo}.`)
  process.exit(0)
}

try { process.loadEnvFile('.env.local') } catch { /* sem .env.local: usa o ambiente */ }
const chave = process.env.SUPABASE_SECRET_KEY
if (!chave) parar('falta a chave SUPABASE_SECRET_KEY no ambiente (ou em .env.local). Sem ela, cole o texto em /admin/agenda.')

const { createClient } = await import('@supabase/supabase-js')
const db = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL ?? URL_PADRAO, chave, {
  auth: { persistSession: false, autoRefreshToken: false },
})

const r1 = await db.from('agenda_semanas')
  .upsert({ semana: s.semana, titulo: s.titulo, aviso: s.aviso, texto, atualizado_em: new Date().toISOString() })
if (r1.error) parar(`não deu para salvar a semana: ${r1.error.message}`)
const r2 = await db.from('agenda_eventos').delete().eq('semana', s.semana).eq('fixo', false)
if (r2.error) parar(`não deu para tirar a versão anterior: ${r2.error.message}`)
const r3 = await db.from('agenda_eventos').insert(s.eventos.map((e) => ({ ...e, semana: s.semana })))
if (r3.error) parar(`não deu para salvar as aulas: ${r3.error.message}`)

console.log(`\nSemana publicada: ${resumo}.`)
