#!/usr/bin/env node
// Material de trabalho das aulas no Supabase (regra do Mauricio, 24/11/2026: dado de aula não mora no Git).
//
// A pasta apostilas-fonte/<aula-id>/ (fonte da aula, mapa, HTML da apostila, figuras) e
// apostilas-fonte/provas/ (compilados, transcrições e correções de prova) ficam guardadas no
// espaço privado "material" do Supabase Storage. No computador fica só uma cópia de trabalho,
// fora do Git (.gitignore). No Git continuam só as ferramentas: README.md, apostila.css e ferramentas/.
//
// Uso:
//   node scripts/material.mjs baixar <aula-id|matéria|provas|tudo> [...]   traz do Supabase para apostilas-fonte/
//     (matéria = todas as aulas dela, ex.: angio baixa angio-a1, angio-a2…)
//   node scripts/material.mjs enviar <aula-id|provas|tudo|arquivo> [...]   leva para o Supabase
//   node scripts/material.mjs listar [aula-id|provas]
//
// Só passa o que mudou (compara o conteúdo). Enviar nunca apaga nada no Supabase.
// Precisa de SUPABASE_SECRET_KEY (variável do ambiente ou arquivo .env.local, fora do Git).
import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs'
import { dirname, join, relative, sep } from 'node:path'
import { fileURLToPath } from 'node:url'

const URL_PADRAO = 'https://xtlpmtylifbalzxnfkib.supabase.co' // igual a lib/supabase/config.ts
const BALDE = 'material'
const RAIZ = join(dirname(fileURLToPath(import.meta.url)), '..', 'apostilas-fonte')
// O que continua no Git (ferramentas de gerar o PDF e o manual da pasta): nunca vai para o Supabase.
const DO_GIT = (rel) => rel === 'README.md' || rel === 'apostila.css' || rel.startsWith('ferramentas/')

function parar(msg) {
  console.error(`material: ${msg}`)
  process.exit(1)
}

const [comando, ...alvos] = process.argv.slice(2)
if (!['baixar', 'enviar', 'listar'].includes(comando)) {
  parar('use "baixar <aula-id|provas|tudo>", "enviar <aula-id|provas|tudo|arquivo>" ou "listar [aula-id]"')
}

try { process.loadEnvFile(join(RAIZ, '..', '.env.local')) } catch { /* sem .env.local: usa o ambiente */ }
const chave = process.env.SUPABASE_SECRET_KEY
if (!chave) parar('falta a chave SUPABASE_SECRET_KEY no ambiente (ou em .env.local).')
const base = `${process.env.NEXT_PUBLIC_SUPABASE_URL ?? URL_PADRAO}/storage/v1`
const cabecalho = { apikey: chave, Authorization: `Bearer ${chave}` }

const md5 = (buf) => createHash('md5').update(buf).digest('hex')
const caminhoUrl = (rel) => rel.split('/').map(encodeURIComponent).join('/')

const TIPOS = {
  md: 'text/markdown; charset=utf-8', txt: 'text/plain; charset=utf-8', html: 'text/html; charset=utf-8',
  css: 'text/css; charset=utf-8', py: 'text/x-python; charset=utf-8', sh: 'text/x-sh; charset=utf-8',
  sql: 'text/plain; charset=utf-8', json: 'application/json', svg: 'image/svg+xml',
  jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png', webp: 'image/webp', pdf: 'application/pdf',
}
const tipo = (rel) => TIPOS[rel.split('.').pop().toLowerCase()] ?? 'application/octet-stream'

async function pedir(url, opcoes, oque) {
  for (let tentativa = 1; ; tentativa++) {
    try {
      const r = await fetch(url, opcoes)
      if (r.ok) return r
      const texto = await r.text()
      if (r.status < 500 || tentativa >= 4) parar(`${oque}: ${r.status} ${texto.slice(0, 300)}`)
    } catch (e) {
      if (tentativa >= 4) parar(`${oque}: ${e.message}`)
    }
    await new Promise((ok) => setTimeout(ok, 1000 * tentativa))
  }
}

// Roda as tarefas de 8 em 8 ao mesmo tempo (um arquivo por vez fica lento).
async function emParalelo(itens, tarefa, ao_mesmo_tempo = 8) {
  let i = 0
  await Promise.all(Array.from({ length: Math.min(ao_mesmo_tempo, itens.length) }, async () => {
    while (i < itens.length) await tarefa(itens[i++])
  }))
}

// Lista os arquivos guardados abaixo de uma pasta (com subpastas), com o md5 de cada um.
async function listarRemoto(prefixo) {
  const arquivos = []
  const pastas = [prefixo]
  while (pastas.length) {
    const pasta = pastas.shift()
    for (let offset = 0; ; offset += 1000) {
      const r = await pedir(`${base}/object/list/${BALDE}`, {
        method: 'POST',
        headers: { ...cabecalho, 'Content-Type': 'application/json' },
        body: JSON.stringify({ prefix: pasta, limit: 1000, offset, sortBy: { column: 'name', order: 'asc' } }),
      }, `listar ${pasta || '(tudo)'}`)
      const itens = await r.json()
      for (const item of itens) {
        const rel = pasta ? `${pasta}/${item.name}` : item.name
        if (item.id === null) pastas.push(rel)
        else arquivos.push({ rel, md5: String(item.metadata?.eTag ?? '').replaceAll('"', ''), tamanho: item.metadata?.size ?? 0 })
      }
      if (itens.length < 1000) break
    }
  }
  return arquivos
}

function listarLocal(pasta) {
  const abs = join(RAIZ, pasta)
  if (!existsSync(abs)) return []
  if (statSync(abs).isFile()) return [pasta]
  const saida = []
  for (const nome of readdirSync(abs, { withFileTypes: true })) {
    const rel = pasta ? `${pasta}/${nome.name}` : nome.name
    if (nome.isDirectory()) saida.push(...listarLocal(rel))
    else saida.push(rel)
  }
  return saida
}

// "angio-a7", "provas", "tudo" ou um arquivo (apostilas-fonte/angio-a7/fonte.md ou angio-a7/fonte.md).
function normalizarAlvo(alvo) {
  if (alvo === 'tudo') return ''
  let rel = alvo.replaceAll('\\', '/')
  const abs = join(process.cwd(), rel)
  if (existsSync(abs) && abs.startsWith(RAIZ + sep)) rel = relative(RAIZ, abs).split(sep).join('/')
  rel = rel.replace(/^\.?\/?apostilas-fonte\//, '').replace(/\/+$/, '')
  if (!rel || rel.includes('..')) parar(`alvo estranho: ${alvo}`)
  return rel
}

if (!alvos.length && comando !== 'listar') parar(`diga o que ${comando} (ex.: angio-a7, provas ou tudo)`)

if (comando === 'listar') {
  const prefixo = alvos[0] ? normalizarAlvo(alvos[0]) : ''
  const arquivos = await listarRemoto(prefixo)
  for (const a of arquivos) console.log(`${String(Math.round(a.tamanho / 1024)).padStart(6)} KB  ${a.rel}`)
  const total = arquivos.reduce((s, a) => s + a.tamanho, 0)
  console.log(`${arquivos.length} arquivo(s), ${(total / 1048576).toFixed(1)} MB`)
} else if (comando === 'baixar') {
  let baixados = 0, iguais = 0
  for (const alvo of alvos) {
    const prefixo = normalizarAlvo(alvo)
    let arquivos
    if (/^[a-z][a-z0-9]*$/.test(prefixo) && prefixo !== 'provas') {
      // Matéria: as pastas <matéria>-aN guardadas.
      arquivos = (await listarRemoto('')).filter((a) => new RegExp(`^${prefixo}-a\\d+/`).test(a.rel))
    } else arquivos = await listarRemoto(prefixo)
    // Um arquivo só (ex.: provas/angio-p2-t26-transcricao.txt): a lista da pasta dele.
    if (!arquivos.length && prefixo.includes('/')) {
      arquivos = (await listarRemoto(prefixo.slice(0, prefixo.lastIndexOf('/')))).filter((a) => a.rel === prefixo)
    }
    if (!arquivos.length) { console.log(`${alvo}: nada guardado no Supabase`); continue }
    await emParalelo(arquivos, async (a) => {
      const destino = join(RAIZ, a.rel)
      if (existsSync(destino) && md5(readFileSync(destino)) === a.md5) { iguais++; return }
      const r = await pedir(`${base}/object/authenticated/${BALDE}/${caminhoUrl(a.rel)}`, { headers: cabecalho }, `baixar ${a.rel}`)
      const conteudo = Buffer.from(await r.arrayBuffer())
      mkdirSync(dirname(destino), { recursive: true })
      writeFileSync(destino, conteudo)
      baixados++
    })
  }
  console.log(`baixados ${baixados}, já iguais ${iguais} (em apostilas-fonte/)`)
} else {
  let enviados = 0, iguais = 0
  for (const alvo of alvos) {
    const prefixo = normalizarAlvo(alvo)
    const locais = listarLocal(prefixo).filter((rel) => !DO_GIT(rel) && !rel.endsWith('.DS_Store'))
    if (!locais.length) { console.log(`${alvo}: nada em apostilas-fonte/${prefixo}`); continue }
    const remotos = new Map((await listarRemoto(prefixo.includes('/') && statSync(join(RAIZ, prefixo)).isFile()
      ? prefixo.slice(0, prefixo.lastIndexOf('/')) : prefixo)).map((a) => [a.rel, a.md5]))
    await emParalelo(locais, async (rel) => {
      const conteudo = readFileSync(join(RAIZ, rel))
      if (remotos.get(rel) === md5(conteudo)) { iguais++; return }
      await pedir(`${base}/object/${BALDE}/${caminhoUrl(rel)}`, {
        method: 'POST',
        headers: { ...cabecalho, 'Content-Type': tipo(rel), 'x-upsert': 'true', 'cache-control': 'no-cache' },
        body: conteudo,
      }, `enviar ${rel}`)
      enviados++
    })
  }
  console.log(`enviados ${enviados}, já iguais ${iguais} (no Supabase, espaço "${BALDE}")`)
}
