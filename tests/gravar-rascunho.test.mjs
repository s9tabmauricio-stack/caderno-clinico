import test from 'node:test'
import assert from 'node:assert/strict'
import {
  lerFlashcards, lerQuestoes, linhasFlashcards, linhasQuestoes, materiaDaAula, numeroId,
  sqlFlashcards, sqlQuestoes, ultimoNumeroDosIds,
} from '../scripts/rascunho.mjs'

const CARDS = `# Flashcards · Gastroenterologia 1 — Reto e ânus

\`gastro-a1\` · 2 cards · 1 com PROVA · rascunho

## 01 · O intestino (p. 2–3)

**1.** Qual é a principal função do cólon?
↳ Absorver sódio e água.

**2.** PROVA · O que é a "regra de Goodsall"?
↳ Fístula anterior: trajeto reto; posterior: curvo até a linha média. D'Ávila frisou.

## Dúvidas para o Mauricio

- p. 6: **3.** isto não é card
`

const QUESTOES = `# Questões · Gastroenterologia 4

\`gastro-a4\` · 2 questões · 1 de PROVA · rascunho

## 01 · Hemorroidas (p. 3–5)

### 1 · PROVA · tema: Doença hemorroidária
Homem de 45 anos com sangramento vermelho-vivo ao evacuar.
Qual é a classificação?
- A) Grau I
- B*) Grau II
- C) Grau III
- D) Grau IV
- E) Trombose

**Comentário:** Prolapsa e volta sozinha: grau II.
**Por que as erradas:**
A: não prolapsa.
C, D e E: precisam de redução manual ou outra coisa.

### 2 · tema: Fissura anal
Qual é o tratamento inicial da fissura aguda?
- A) Cirurgia
- B) Toxina
- C) Antibiótico
- D) Nada
- E*) Fibras e banho de assento

**Comentário:** Começa clínico.
**Por que as erradas:**
A, B, C e D: não são o começo.

## Revisão

### 9 · tema: lixo que não entra
`

test('lê os flashcards e ignora as dúvidas', () => {
  const cards = lerFlashcards(CARDS)
  assert.equal(cards.length, 2)
  assert.equal(cards[1].frente, 'PROVA · O que é a "regra de Goodsall"?')
  assert.equal(cards[1].verso, "Fístula anterior: trajeto reto; posterior: curvo até a linha média. D'Ávila frisou.")
  const linhas = linhasFlashcards('gastro-a1', cards)
  assert.deepEqual(linhas[0], { id: 'gastro-a1-f01', aula_id: 'gastro-a1', ordem: 1, frente: 'Qual é a principal função do cólon?', verso: 'Absorver sódio e água.' })
})

test('ids passam do 99 para o 100 sem cortar', () => {
  assert.equal(numeroId(7), '07')
  assert.equal(numeroId(99), '99')
  assert.equal(numeroId(100), '100')
  assert.equal(materiaDaAula('pneumo-a12'), 'pneumo')
  assert.throws(() => materiaDaAula('pneumo12'))
})

test('flashcard sem verso ou fora de sequência para', () => {
  assert.throws(() => lerFlashcards('**1.** Frente sem verso\n'), /verso/)
  assert.throws(() => lerFlashcards('**1.** a\n↳ b\n\n**3.** c\n↳ d\n'), /esperava o número 2/)
})

test('lê as questões: PROVA, tema, certa, comentário e por que as erradas', () => {
  const qs = lerQuestoes(QUESTOES)
  assert.equal(qs.length, 2)
  assert.equal(qs[0].prova, true)
  assert.equal(qs[1].prova, false)
  assert.equal(qs[0].tema, 'Doença hemorroidária')
  assert.equal(qs[0].enunciado, 'Homem de 45 anos com sangramento vermelho-vivo ao evacuar.\nQual é a classificação?')
  assert.equal(qs[0].correta, 1)
  assert.equal(qs[1].correta, 4)
  assert.deepEqual(qs[0].alternativas, ['Grau I', 'Grau II', 'Grau III', 'Grau IV', 'Trombose'])
  assert.equal(qs[0].por_que_erradas, 'A: não prolapsa.\nC, D e E: precisam de redução manual ou outra coisa.')
})

test('questões continuam a ordem da matéria e a numeração da aula', () => {
  const linhas = linhasQuestoes('gastro-a4', lerQuestoes(QUESTOES), { ultimaOrdem: 310, ultimoNumero: 12, ano: 2026 })
  assert.equal(linhas[0].id, 'gastro-a4-q13')
  assert.equal(linhas[1].id, 'gastro-a4-q14')
  assert.equal(linhas[0].ordem, 311)
  assert.equal(linhas[0].materia_id, 'gastro')
  assert.equal(linhas[0].fonte, 'Montada (aula 2026)')
  assert.equal(linhas[0].origem, 'montada')
  assert.equal(linhas[0].prova, null)
  assert.equal(linhas[0].cai_na_prova, true)
  assert.equal(ultimoNumeroDosIds(['x-q07', 'x-q12-v2', 'x-q03']), 12)
})

test('questão com defeito para com o número dela', () => {
  const sem5 = QUESTOES.replace('- E) Trombose\n', '')
  assert.throws(() => lerQuestoes(sem5), /Questão 1: tem 4 alternativas/)
  const duasCertas = QUESTOES.replace('- A) Grau I', '- A*) Grau I')
  assert.throws(() => lerQuestoes(duasCertas), /Questão 1: tem 2 alternativas com \*/)
})

test('SQL dobra as aspas e usa chr(10) nas quebras', () => {
  const sqlC = sqlFlashcards(linhasFlashcards('gastro-a1', lerFlashcards(CARDS)))
  assert.match(sqlC, /D''Ávila/)
  assert.match(sqlC, /on conflict \(id\) do nothing returning id;/)
  const sqlQ = sqlQuestoes(linhasQuestoes('gastro-a4', lerQuestoes(QUESTOES), { ultimaOrdem: 0, ultimoNumero: 0, ano: 2026 }))
  assert.match(sqlQ, /'A: não prolapsa\.' \|\| chr\(10\) \|\| 'C, D e E/)
  assert.match(sqlQ, /'\["Grau I","Grau II","Grau III","Grau IV","Trombose"\]'::jsonb, 1,/)
  assert.match(sqlQ, /'gastro-a4-q01'/)
})
