import test from 'node:test'
import assert from 'node:assert/strict'
import { coberturaDiaD, ehQuestaoFag, lerFlashcardsDiaD, linhasDiaD, sqlDiaD } from '../scripts/rascunho.mjs'
import { fonteDaQuestao } from '../lib/classificacao-questoes.ts'

const RASCUNHO = `# Flashcards Dia D · Pneumologia 1 — Asma

\`pneumo-a1\` · 4 cards · 2 questões das Provas da FAG · rascunho

## pneumo-a1-q07 · P2 · nº 10 — Espirometria

**1.** Qual é o critério de resposta ao broncodilatador
na espirometria do adulto?
↳ Aumento do VEF1 de pelo menos 12% e 200 mL.

**2.** Capacidade vital forçada baixa com relação VEF1/CVF normal sugere o quê?
↳ Padrão restritivo.
+ também: pneumo-a1-q12

## pneumo-a1-q12-v2 · P2 T23 · nº 9 — Asma grave

**3.** Qual é o primeiro passo na asma de difícil controle?
↳ Conferir a técnica inalatória e a adesão.

**4.** Fora da aula: o que é asma grave?
↳ A que exige o passo 4 ou 5 para ficar controlada.

## Dúvidas para o Mauricio

- **9.** isto não é card
`

test('lê os cards do Dia D com as questões de cada um', () => {
  const cards = lerFlashcardsDiaD(RASCUNHO, 'pneumo-a1')
  assert.equal(cards.length, 4)
  assert.equal(cards[0].frente, 'Qual é o critério de resposta ao broncodilatador na espirometria do adulto?')
  assert.deepEqual(cards[0].questoes, ['pneumo-a1-q07'])
  assert.deepEqual(cards[1].questoes, ['pneumo-a1-q07', 'pneumo-a1-q12'])
  assert.equal(cards[1].verso, 'Padrão restritivo.')
  assert.deepEqual(cards[2].questoes, ['pneumo-a1-q12-v2'])
})

test('card fora de uma seção de questão para o programa', () => {
  assert.throws(() => lerFlashcardsDiaD('## Sem id\n\n**1.** Frente?\n↳ Verso.\n', 'pneumo-a1'), /fora de uma seção/)
})

test('cobertura: questão FAG sem card e id que não é FAG', () => {
  const cards = lerFlashcardsDiaD(RASCUNHO, 'pneumo-a1')
  const r = coberturaDiaD(cards, ['pneumo-a1-q07', 'pneumo-a1-q12-v2', 'pneumo-a1-q20'])
  assert.deepEqual(r.semCard, ['pneumo-a1-q20'])
  assert.deepEqual(r.desconhecidas, ['pneumo-a1-q12'])
})

test('linhas e SQL do Dia D', () => {
  const linhas = linhasDiaD('pneumo-a1', lerFlashcardsDiaD(RASCUNHO, 'pneumo-a1'))
  assert.equal(linhas[0].id, 'pneumo-a1-d01')
  assert.equal(linhas[3].ordem, 4)
  const sql = sqlDiaD(linhas.slice(1, 2))
  assert.match(sql, /insert into public\.flashcards_dia_d \(id, aula_id, ordem, frente, verso, questoes\)/)
  assert.match(sql, /array\['pneumo-a1-q07', 'pneumo-a1-q12'\]::text\[\]/)
})

test('a regra de questão FAG do programa é a mesma da tela', () => {
  const casos = [
    { prova: 'p2', fonte: 'P2 · nº 10' },
    { prova: 'p2-t23', fonte: 'P2 T23 · nº 9' },
    { prova: 'exame', fonte: 'Exame 2025/2' },
    { prova: ' P1 ', fonte: null },
    { prova: null, fonte: 'Material da turma (Drive)' },
    { prova: null, fonte: 'Guia de estudo da P2' },
    { prova: 'Residência', fonte: 'UFPR 2020' },
    { prova: 'Revalida', fonte: 'Revalida 2024' },
    { prova: null, fonte: 'Montada (aula 2026)' },
    { prova: null, fonte: null },
  ]
  for (const q of casos) assert.equal(ehQuestaoFag(q), fonteDaQuestao(q) === 'fag', JSON.stringify(q))
})
