#!/usr/bin/env node
// Copia as skills de .claude/skills/ (a original, que o Claude lê) para .agents/skills/
// (onde o Codex e o Antigravity procuram skills sozinhos). As duas pastas usam o mesmo
// formato (SKILL.md), então a cópia é igualzinha.
//
// Edite sempre em .claude/skills/ e depois rode este programa. O npm test avisa se as
// duas pastas ficarem diferentes (tests/manual-assistentes.test.mjs).
//
// Uso:
//   node scripts/sincronizar-skills.mjs             refaz a cópia (o que saiu da original sai da cópia)
//   node scripts/sincronizar-skills.mjs --conferir  só diz o que está diferente, sem mexer em nada
//
// Não usa atalho de pasta (link simbólico) porque no Windows ele vira um arquivo comum.

import { cpSync, existsSync, readdirSync, readFileSync, rmSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const RAIZ = resolve(fileURLToPath(new URL('..', import.meta.url)))
export const ORIGEM = join(RAIZ, '.claude', 'skills')
export const COPIA = join(RAIZ, '.agents', 'skills')

// Caminhos relativos de todos os arquivos da pasta, sempre com "/".
function arquivos(pasta, prefixo = '') {
  if (!existsSync(pasta)) return []
  const lista = []
  for (const item of readdirSync(pasta, { withFileTypes: true })) {
    const relativo = prefixo + item.name
    if (item.isDirectory()) lista.push(...arquivos(join(pasta, item.name), relativo + '/'))
    else lista.push(relativo)
  }
  return lista.sort()
}

// Lê o arquivo ignorando a diferença de fim de linha do Windows (CRLF) e do Linux (LF).
const conteudo = (caminho) => readFileSync(caminho).toString('latin1').replace(/\r\n/g, '\n')

// Lista o que está diferente entre a original e a cópia (vazia quando estão iguais).
export function diferencas() {
  const daOrigem = arquivos(ORIGEM)
  const daCopia = arquivos(COPIA)
  const naCopia = new Set(daCopia)
  const naOrigem = new Set(daOrigem)
  const lista = []
  for (const arquivo of daOrigem) {
    if (!naCopia.has(arquivo)) lista.push(`falta na cópia: ${arquivo}`)
    else if (conteudo(join(ORIGEM, arquivo)) !== conteudo(join(COPIA, arquivo))) lista.push(`diferente: ${arquivo}`)
  }
  for (const arquivo of daCopia) {
    if (!naOrigem.has(arquivo)) lista.push(`sobra na cópia: ${arquivo}`)
  }
  return lista
}

export function sincronizar() {
  rmSync(COPIA, { recursive: true, force: true })
  cpSync(ORIGEM, COPIA, { recursive: true })
}

const rodandoDireto = process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)
if (rodandoDireto) {
  const antes = diferencas()
  if (process.argv.includes('--conferir')) {
    if (antes.length === 0) console.log('As skills de .agents/skills/ estão iguais às de .claude/skills/.')
    else {
      console.log('Diferenças entre .claude/skills/ (original) e .agents/skills/ (cópia):')
      for (const linha of antes) console.log('  ' + linha)
      process.exitCode = 1
    }
  } else if (antes.length === 0) {
    console.log('Nada a fazer: a cópia em .agents/skills/ já está igual à original.')
  } else {
    sincronizar()
    console.log(`Cópia refeita em .agents/skills/ (${antes.length} diferença(s) corrigida(s)):`)
    for (const linha of antes) console.log('  ' + linha)
  }
}
