#!/usr/bin/env node
// Troca questões que já estão no banco por versões novas (-v2), sem o assistente reescrever o texto.
//
// Uso:
//   node scripts/substituir-questoes.mjs <aula-id>
//
// Lê rascunhos/questoes-refazer/<aula-id>.md: formato do agente questoes, com o id da questão
// antiga no título ("### 3 · PROVA · substitui: angio-a1-q07 · tema: …"). Escreve os lotes de SQL
// em rascunhos/sql/<aula-id>-substituir-N.sql, para rodar no conector do Supabase em ordem.
// Cada questão nova herda da antiga a ordem, o tema, a fonte e a marca PROVA; a antiga fica
// com substituida_por preenchido e os recados vão para a nova. O Mauricio limpa as antigas
// depois em Conteúdo → Limpeza.
import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { idNovaVersao, lerQuestoes, lotes, materiaDaAula, sqlSubstituicoes } from './rascunho.mjs'

function parar(msg) {
  console.error('PAROU: ' + msg)
  process.exit(1)
}

const aulaId = process.argv[2]
if (!aulaId) parar('diga o id da aula. Ex.: node scripts/substituir-questoes.mjs angio-a1')
try { materiaDaAula(aulaId) } catch (e) { parar(e.message) }

const arquivo = `rascunhos/questoes-refazer/${aulaId}.md`
if (!existsSync(arquivo)) parar(`não achei ${arquivo}.`)

let questoes
try {
  questoes = lerQuestoes(readFileSync(arquivo, 'utf8'))
  const vistos = new Set()
  for (const q of questoes) {
    if (!q.substitui) throw new Error(`Questão ${q.n}: falta o "substitui: <id>" no título.`)
    if (!q.substitui.startsWith(`${aulaId}-q`)) throw new Error(`Questão ${q.n}: ${q.substitui} não é da aula ${aulaId}.`)
    if (vistos.has(q.substitui)) throw new Error(`Questão ${q.n}: ${q.substitui} aparece duas vezes.`)
    vistos.add(q.substitui)
  }
} catch (e) {
  parar(e.message)
}

mkdirSync('rascunhos/sql', { recursive: true })
const partes = lotes(questoes, 10)
partes.forEach((lote, i) => {
  writeFileSync(`rascunhos/sql/${aulaId}-substituir-${i + 1}.sql`, sqlSubstituicoes(lote))
})
console.log(`${questoes.length} questões para substituir, em ${partes.length} lotes: rascunhos/sql/${aulaId}-substituir-1.sql a -${partes.length}.sql.`)
// Assinatura para conferir que o banco ficou igual ao rascunho, letra por letra.
const md5 = (t) => createHash('md5').update(t).digest('hex')
const jsonbTexto = (lista) => '[' + lista.map((a) => JSON.stringify(a)).join(', ') + ']' // como o Postgres escreve jsonb
const novos = questoes.map((q) => ({ id: idNovaVersao(q.substitui), q })).sort((a, b) => (a.id < b.id ? -1 : 1))
const assinatura = md5(novos.map(({ id, q }) =>
  `${id}:${q.correta}:${md5(q.enunciado)}${md5(jsonbTexto(q.alternativas))}${md5(q.comentario)}${md5(q.por_que_erradas)}`).join('|'))
const ids = novos.map((n) => `'${n.id}'`).join(', ')
console.log(`Depois de rodar, confira no conector (a assinatura deve dar ${assinatura}):`)
console.log(`select count(*) as gravadas, md5(string_agg(id || ':' || correta || ':' || md5(enunciado) || md5(alternativas::text) || md5(comentario) || md5(por_que_erradas), '|' order by id)) as assinatura from public.questoes where id in (${ids}) and substituida_por is null;`)
