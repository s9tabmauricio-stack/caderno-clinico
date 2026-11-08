// Confere a ligação dos três assistentes (Claude, Codex e Antigravity) com o manual único,
// o AGENTS.md. Se um teste daqui falhar, a mensagem diz o que arrumar.
import test from 'node:test'
import assert from 'node:assert/strict'
import { readdirSync, readFileSync, statSync } from 'node:fs'
import { join } from 'node:path'
import { ORIGEM, diferencas } from '../scripts/sincronizar-skills.mjs'

const ler = (caminho) => readFileSync(caminho, 'utf8').replace(/\r\n/g, '\n')

test('o CLAUDE.md só aponta para o AGENTS.md', () => {
  const linhas = ler('CLAUDE.md').split('\n').map((l) => l.trim()).filter(Boolean)
  assert.equal(linhas[0], '@AGENTS.md', 'a primeira linha do CLAUDE.md tem de ser @AGENTS.md (é assim que o Claude lê o manual)')
  const regras = linhas.filter((l) => l !== '@AGENTS.md' && !l.startsWith('<!--'))
  assert.deepEqual(regras, [], 'o CLAUDE.md não leva regras: escreva no AGENTS.md')
})

test('o AGENTS.md cabe no que o Codex lê (32 KB)', () => {
  const tamanho = statSync('AGENTS.md').size
  assert.ok(tamanho <= 32 * 1024, `o AGENTS.md tem ${tamanho} bytes; o Codex só lê os primeiros 32.768. Leve detalhes para docs/ ou para as skills.`)
})

test('a regra do Antigravity está sempre ligada e só aponta para o AGENTS.md', () => {
  const pasta = '.agents/rules'
  const regras = readdirSync(pasta).filter((nome) => nome.endsWith('.md'))
  assert.deepEqual(regras, ['medgenius.md'], 'o Antigravity deve ter uma regra só (.agents/rules/medgenius.md); regras novas vão no AGENTS.md')
  const texto = ler(join(pasta, 'medgenius.md'))
  assert.match(texto, /^---\ntrigger: always_on\n---\n/, 'a regra precisa começar com "trigger: always_on" para o Antigravity ler sempre')
  assert.match(texto, /AGENTS\.md/, 'a regra tem de mandar ler o AGENTS.md')
  assert.ok(texto.length <= 1500, 'a regra do Antigravity só aponta para o manual: as regras ficam no AGENTS.md, não repetidas aqui')
})

test('as skills de .agents/skills/ (Codex e Antigravity) são cópia exata de .claude/skills/', () => {
  const lista = diferencas()
  assert.deepEqual(lista, [], 'edite as skills só em .claude/skills/ e rode: node scripts/sincronizar-skills.mjs\n' + lista.join('\n'))
})

test('cada skill tem nome igual ao da pasta e uma descrição', () => {
  const pastas = readdirSync(ORIGEM, { withFileTypes: true }).filter((item) => item.isDirectory()).map((item) => item.name)
  assert.ok(pastas.length > 0, `nenhuma skill encontrada em ${ORIGEM}`)
  for (const pasta of pastas) {
    const texto = ler(join(ORIGEM, pasta, 'SKILL.md'))
    const cabecalho = texto.match(/^---\n([\s\S]*?)\n---\n/)
    assert.ok(cabecalho, `${pasta}/SKILL.md precisa começar com o cabeçalho entre linhas ---`)
    const nome = cabecalho[1].match(/^name:\s*"?([^"\n]+?)"?\s*$/m)?.[1]
    assert.equal(nome, pasta, `${pasta}/SKILL.md: o "name" tem de ser igual ao nome da pasta (o Codex e o Antigravity exigem)`)
    assert.match(cabecalho[1], /^description:\s*\S/m, `${pasta}/SKILL.md: falta a "description" (é por ela que o assistente sabe quando usar a skill)`)
  }
})
