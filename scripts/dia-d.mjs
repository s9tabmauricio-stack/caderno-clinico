#!/usr/bin/env node
// Flashcards Dia D (regra do Mauricio, 10/11/2026): baralho de véspera da aula, feito para resolver
// todas as questões das Provas da FAG dela. Etapas mecânicas, sem o assistente reescrever texto.
//
// Uso:
//   node scripts/dia-d.mjs exportar <aula-id>
//        tira do banco as questões FAG da aula para rascunhos/flashcards-dia-d/<aula-id>-questoes.md
//        (é o que o agente lê para fazer os cards)
//   node scripts/dia-d.mjs gravar <aula-id> [--conferir | --sql]
//        lê rascunhos/flashcards-dia-d/<aula-id>.md, confere que toda questão FAG tem card e grava em
//        flashcards_dia_d. --conferir só confere; --sql escreve o SQL em rascunhos/sql/ para o conector
//        (sem a chave, a lista das questões FAG vem do arquivo exportado ou de --questoes id1,id2,…).
//
// Sem acesso direto ao banco (ex.: Claude na nuvem, onde a rede só deixa passar o conector), o agente lê
// as questões FAG pelo conector e a gravação vai por --sql. Consulta (mesma regra de ehQuestaoFag):
//   select id, fonte, tema, enunciado, alternativas, correta, comentario, por_que_erradas from public.questoes
//   where aula_id = '<aula-id>' and substituida_por is null
//     and (trim(coalesce(prova, '')) ~* '^(p\d+(-t\d+)?|exame)$'
//          or coalesce(fonte, '') ~* 'material da turma|guia de estudo|compilados? da turma')
//   order by ordem;
// Precisa da chave SUPABASE_SECRET_KEY (ambiente ou .env.local), menos no --sql.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { coberturaDiaD, ehQuestaoFag, lerFlashcardsDiaD, linhasDiaD, lotes, materiaDaAula, sqlDiaD } from './rascunho.mjs'

const URL_PADRAO = 'https://xtlpmtylifbalzxnfkib.supabase.co' // igual a lib/supabase/config.ts
const PASTA = 'rascunhos/flashcards-dia-d'
const LETRAS = 'ABCDE'

const [comando, aulaId, ...resto] = process.argv.slice(2)
const tem = (f) => resto.includes(f)

function parar(msg) {
  console.error('PAROU: ' + msg)
  process.exit(1)
}

if (!['exportar', 'gravar'].includes(comando) || !aulaId) parar('uso: node scripts/dia-d.mjs exportar|gravar <aula-id>')
try { materiaDaAula(aulaId) } catch (e) { parar(e.message) }

const arqQuestoes = `${PASTA}/${aulaId}-questoes.md`
const arqCards = `${PASTA}/${aulaId}.md`

async function banco() {
  try { process.loadEnvFile('.env.local') } catch { /* sem .env.local: usa o ambiente */ }
  const chave = process.env.SUPABASE_SECRET_KEY
  if (!chave) parar('falta a chave SUPABASE_SECRET_KEY no ambiente (ou em .env.local). Sem ela, use --sql e o conector.')
  const { createClient } = await import('@supabase/supabase-js')
  return createClient(process.env.NEXT_PUBLIC_SUPABASE_URL ?? URL_PADRAO, chave, {
    auth: { persistSession: false, autoRefreshToken: false },
  })
}

async function consulta(promessa, oque) {
  const { data, error, count } = await promessa
  if (error) parar(`${oque}: ${error.message}`)
  return { data, count }
}

async function questoesFag(db) {
  const { data } = await consulta(
    db.from('questoes')
      .select('id, ordem, tema, enunciado, alternativas, correta, comentario, por_que_erradas, prova, fonte, cai_na_prova')
      .eq('aula_id', aulaId).is('substituida_por', null).order('ordem'),
    'ler as questões da aula')
  return data.filter(ehQuestaoFag)
}

// Ids das questões FAG sem a chave: --questoes id1,id2,… (da consulta no conector) ou o arquivo exportado
function idsDoExportado() {
  const i = resto.indexOf('--questoes')
  if (i !== -1) return resto[i + 1]?.split(',').map((s) => s.trim()).filter(Boolean) ?? []
  if (!existsSync(arqQuestoes)) parar(`não achei ${arqQuestoes}. Rode antes "exportar" ou passe --questoes id1,id2,… (ids das questões FAG da aula, pelo conector).`)
  const re = /^##\s+([a-z0-9]+(?:-[a-z0-9]+)+)\s+·/gm
  return [...readFileSync(arqQuestoes, 'utf8').matchAll(re)].map((m) => m[1])
}

// ---------- exportar ----------
if (comando === 'exportar') {
  const db = await banco()
  const fag = await questoesFag(db)
  if (!fag.length) parar(`a aula ${aulaId} não tem questões das Provas da FAG.`)
  const md = `# Questões das Provas da FAG · ${aulaId} (${fag.length})\n\n` +
    'Gabarito como está no banco. Prova sem gabarito oficial foi resolvida por nós: confira contra a fonte.\n\n' +
    fag.map((q) => [
      `## ${q.id} · ${q.fonte ?? q.prova}`,
      `Tema: ${q.tema ?? '—'}${q.cai_na_prova ? ' · PROVA' : ''}`,
      '',
      q.enunciado,
      '',
      ...q.alternativas.map((a, i) => `- ${LETRAS[i]}) ${a}${i === q.correta ? '   ← gabarito' : ''}`),
      '',
      `**Comentário:** ${q.comentario ?? ''}`,
      '',
      `**Por que as erradas:**\n${q.por_que_erradas ?? ''}`,
      '',
    ].join('\n')).join('\n---\n\n')
  mkdirSync(PASTA, { recursive: true })
  writeFileSync(arqQuestoes, md)
  console.log(`${fag.length} questões FAG em ${arqQuestoes}:\n${fag.map((q) => `  ${q.id} · ${q.fonte ?? q.prova}`).join('\n')}`)
  process.exit(0)
}

// ---------- gravar ----------
if (!existsSync(arqCards)) parar(`não achei ${arqCards}.`)
let cards
try { cards = lerFlashcardsDiaD(readFileSync(arqCards, 'utf8')) } catch (e) { parar(e.message) }

const semBanco = tem('--sql')
const db = semBanco ? null : await banco()
const idsFag = semBanco ? idsDoExportado() : (await questoesFag(db)).map((q) => q.id)
const { semCard, desconhecidas } = coberturaDiaD(cards, idsFag)
console.log(`Rascunho Dia D: ${cards.length} cards para ${idsFag.length} questões FAG.`)
if (desconhecidas.length) parar(`o rascunho cita questões que não são FAG desta aula (ou não existem mais): ${desconhecidas.join(', ')}.`)
if (semCard.length) parar(`estas questões FAG ficaram sem card: ${semCard.join(', ')}.`)
console.log('Toda questão FAG da aula tem pelo menos um card.')
if (tem('--conferir')) process.exit(0)

const linhas = linhasDiaD(aulaId, cards)

if (semBanco) {
  mkdirSync('rascunhos/sql', { recursive: true })
  const feitos = lotes(linhas, 60).map((l, i) => {
    const arq = `rascunhos/sql/${aulaId}-dia-d-${i + 1}.sql`
    writeFileSync(arq, sqlDiaD(l))
    return arq
  })
  console.log('SQL pronto (rode cada arquivo no conector, em ordem):\n' + feitos.join('\n'))
  process.exit(0)
}

const { data: aula } = await consulta(db.from('aulas').select('id').eq('id', aulaId).maybeSingle(), 'ler a aula')
if (!aula) parar(`a aula ${aulaId} não existe no banco.`)
const { count: antes } = await consulta(
  db.from('flashcards_dia_d').select('id', { count: 'exact', head: true }).eq('aula_id', aulaId), 'contar os cards Dia D')
if (antes > 0) parar(`a aula já tem ${antes} cards Dia D. O Mauricio apaga em Configurações → Conteúdo → a aula → "Apagar os N cards Dia D"; depois rode de novo.`)

let total = 0
for (const lote of lotes(linhas, 60)) {
  const { data } = await consulta(db.from('flashcards_dia_d').upsert(lote, { onConflict: 'id', ignoreDuplicates: true }).select('id'), 'gravar os cards Dia D')
  total += data.length
}
const { count } = await consulta(
  db.from('flashcards_dia_d').select('id', { count: 'exact', head: true }).eq('aula_id', aulaId), 'conferir os cards Dia D')
if (count !== cards.length) parar(`gravei ${total} cards, mas a aula tem ${count} no banco (esperava ${cards.length}).`)
console.log(`Cards Dia D gravados: ${total} (${linhas[0].id} a ${linhas.at(-1).id}).`)
