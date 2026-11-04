#!/usr/bin/env node
// Grava no banco os rascunhos revisados de uma aula, sem o assistente reescrever o texto.
//
// Uso:
//   node scripts/gravar-rascunho.mjs <aula-id>                 grava flashcards e questões
//   node scripts/gravar-rascunho.mjs <aula-id> --so-flashcards  (ou --so-questoes)
//   node scripts/gravar-rascunho.mjs <aula-id> --conferir       só lê e confere os rascunhos, não grava
//   node scripts/gravar-rascunho.mjs <aula-id> --sql --ultima-ordem N --ultimo-numero N
//        sem a chave: escreve os lotes de SQL em rascunhos/sql/ para colar no conector
//
// Lê rascunhos/flashcards/<aula-id>.md e rascunhos/questoes/<aula-id>.md (formato dos
// agentes flashcards e questoes, em .claude/agents/). Precisa da chave secreta do Supabase
// em SUPABASE_SECRET_KEY (variável do ambiente ou arquivo .env.local, que nunca vai para o Git).
// Regras (ids, ordem, PROVA, fonte) iguais às dos agentes. Para se algo não bater.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import {
  lerFlashcards, lerQuestoes, linhasFlashcards, linhasQuestoes, lotes, materiaDaAula,
  normalizar, sqlFlashcards, sqlQuestoes, ultimoNumeroDosIds,
} from './rascunho.mjs'

const URL_PADRAO = 'https://xtlpmtylifbalzxnfkib.supabase.co' // igual a lib/supabase/config.ts

const args = process.argv.slice(2)
const aulaId = args.find((a) => !a.startsWith('--') && !/^\d+$/.test(a))
const tem = (f) => args.includes(f)
const valor = (f) => { const i = args.indexOf(f); return i === -1 ? undefined : args[i + 1] }

function parar(msg) {
  console.error('PAROU: ' + msg)
  process.exit(1)
}

if (!aulaId) parar('diga o id da aula. Ex.: node scripts/gravar-rascunho.mjs gastro-a4')
try { materiaDaAula(aulaId) } catch (e) { parar(e.message) }

const fazCards = !tem('--so-questoes')
const fazQuestoes = !tem('--so-flashcards')
const arqCards = `rascunhos/flashcards/${aulaId}.md`
const arqQuestoes = `rascunhos/questoes/${aulaId}.md`
const ano = Number(valor('--ano') ?? new Date().getFullYear())

let cards = null
let questoes = null
try {
  if (fazCards && existsSync(arqCards)) cards = lerFlashcards(readFileSync(arqCards, 'utf8'))
  if (fazQuestoes && existsSync(arqQuestoes)) questoes = lerQuestoes(readFileSync(arqQuestoes, 'utf8'))
} catch (e) {
  parar(e.message)
}
if (!cards && !questoes) parar(`não achei ${fazCards ? arqCards : ''}${fazCards && fazQuestoes ? ' nem ' : ''}${fazQuestoes ? arqQuestoes : ''}.`)

if (cards) console.log(`Rascunho de flashcards: ${cards.length} cards, ${cards.filter((c) => c.frente.startsWith('PROVA')).length} com PROVA.`)
if (questoes) console.log(`Rascunho de questões: ${questoes.length} questões, ${questoes.filter((q) => q.prova).length} de PROVA.`)
if (tem('--conferir')) process.exit(0)

// ---------- Só SQL (sem a chave) ----------
if (tem('--sql')) {
  mkdirSync('rascunhos/sql', { recursive: true })
  const feitos = []
  const ultimaOrdem = valor('--ultima-ordem')
  const ultimoNumero = valor('--ultimo-numero')
  if (questoes && (ultimaOrdem === undefined || ultimoNumero === undefined)) {
    parar(`para as questões em SQL, rode antes no conector e passe --ultima-ordem e --ultimo-numero:\n` +
      `select (select coalesce(max(ordem), 0) from public.questoes where materia_id = '${materiaDaAula(aulaId)}') as ultima_ordem, ` +
      `(select coalesce(max((regexp_match(id, '-q(\\d+)'))[1]::int), 0) from public.questoes where aula_id = '${aulaId}') as ultimo_numero;`)
  }
  if (cards) {
    lotes(linhasFlashcards(aulaId, cards), 60).forEach((l, i) => {
      const arq = `rascunhos/sql/${aulaId}-flashcards-${i + 1}.sql`
      writeFileSync(arq, sqlFlashcards(l)); feitos.push(arq)
    })
  }
  if (questoes) {
    const linhas = linhasQuestoes(aulaId, questoes, { ultimaOrdem: Number(ultimaOrdem), ultimoNumero: Number(ultimoNumero), ano })
    lotes(linhas, 20).forEach((l, i) => {
      const arq = `rascunhos/sql/${aulaId}-questoes-${i + 1}.sql`
      writeFileSync(arq, sqlQuestoes(l)); feitos.push(arq)
    })
  }
  console.log('SQL pronto (rode cada arquivo no conector, em ordem):\n' + feitos.join('\n'))
  process.exit(0)
}

// ---------- Gravar com a chave ----------
try { process.loadEnvFile('.env.local') } catch { /* sem .env.local: usa o ambiente */ }
const chave = process.env.SUPABASE_SECRET_KEY
if (!chave) parar('falta a chave SUPABASE_SECRET_KEY no ambiente (ou em .env.local). Sem ela, use --sql e o conector.')

const { createClient } = await import('@supabase/supabase-js')
const db = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL ?? URL_PADRAO, chave, {
  auth: { persistSession: false, autoRefreshToken: false },
})

async function consulta(promessa, oque) {
  const { data, error, count } = await promessa
  if (error) parar(`${oque}: ${error.message}`)
  return { data, count }
}

const { data: aula } = await consulta(db.from('aulas').select('id, materia_id').eq('id', aulaId).maybeSingle(), 'ler a aula')
if (!aula) parar(`a aula ${aulaId} não existe no banco. Inclua a aula (skill subir-apostila) antes.`)

// Confere tudo antes de gravar qualquer coisa.
let linhasC = null
let linhasQ = null
if (cards) {
  const { count } = await consulta(db.from('flashcards').select('id', { count: 'exact', head: true }).eq('aula_id', aulaId), 'contar os cards')
  if (count > 0) parar(`a aula já tem ${count} flashcards. O Mauricio apaga os antigos em Configurações → Conteúdo → a aula → "Apagar os N flashcards"; depois rode de novo.`)
  linhasC = linhasFlashcards(aulaId, cards)
}
let antesQ = 0
if (questoes) {
  const { data: daAula } = await consulta(db.from('questoes').select('id, enunciado, substituida_por').eq('aula_id', aulaId), 'ler as questões da aula')
  const ativas = daAula.filter((q) => !q.substituida_por)
  antesQ = ativas.length
  const existentes = new Set(ativas.map((q) => normalizar(q.enunciado)))
  const repetidas = questoes.filter((q) => existentes.has(normalizar(q.enunciado))).map((q) => q.n)
  if (repetidas.length) parar(`as questões ${repetidas.join(', ')} do rascunho já estão no banco (o rascunho já foi gravado?).`)
  const { data: ultima } = await consulta(
    db.from('questoes').select('ordem').eq('materia_id', aula.materia_id).order('ordem', { ascending: false }).limit(1), 'ler a última ordem')
  linhasQ = linhasQuestoes(aulaId, questoes, {
    ultimaOrdem: ultima[0]?.ordem ?? 0,
    ultimoNumero: ultimoNumeroDosIds(daAula.map((q) => q.id)),
    ano,
  })
  if (aula.materia_id !== linhasQ[0].materia_id) parar(`a matéria da aula no banco (${aula.materia_id}) não bate com o id (${linhasQ[0].materia_id}).`)
}

async function gravar(tabela, linhas, tamanho) {
  let total = 0
  for (const lote of lotes(linhas, tamanho)) {
    const { data } = await consulta(db.from(tabela).upsert(lote, { onConflict: 'id', ignoreDuplicates: true }).select('id'), `gravar ${tabela}`)
    const gravados = new Set(data.map((d) => d.id))
    const fora = lote.filter((l) => !gravados.has(l.id)).map((l) => l.id)
    if (fora.length) parar(`${fora.length} ficaram de fora em ${tabela} (id já existia): ${fora.join(', ')}. Gravados até aqui: ${total + gravados.size}.`)
    total += gravados.size
  }
  return total
}

if (linhasC) {
  const n = await gravar('flashcards', linhasC, 60)
  const { count } = await consulta(db.from('flashcards').select('id', { count: 'exact', head: true }).eq('aula_id', aulaId), 'conferir os cards')
  if (count !== cards.length) parar(`gravei ${n} cards, mas a aula tem ${count} no banco (esperava ${cards.length}).`)
  console.log(`Flashcards gravados: ${n} (${linhasC[0].id} a ${linhasC.at(-1).id}).`)
}
if (linhasQ) {
  const n = await gravar('questoes', linhasQ, 20)
  const { count } = await consulta(
    db.from('questoes').select('id', { count: 'exact', head: true }).eq('aula_id', aulaId).is('substituida_por', null), 'conferir as questões')
  if (count !== antesQ + questoes.length) parar(`gravei ${n} questões, mas a aula tem ${count} ativas (esperava ${antesQ + questoes.length}).`)
  console.log(`Questões gravadas: ${n} (${linhasQ[0].id} a ${linhasQ.at(-1).id}); a aula tem ${count} ativas.`)
}
