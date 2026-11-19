import test from 'node:test'
import assert from 'node:assert/strict'
import { temFaixaProva, corFaixaProva, cardDeProva } from '../lib/faixa-prova.ts'

test('faixa PROVA: o professor deu a entender que cai', () => {
  assert.equal(temFaixaProva({ cai_na_prova: true, prova: null }), true)
  assert.equal(temFaixaProva({ cai_na_prova: false, prova: null }), false)
})

test('faixa PROVA: provas antigas do curso sim, outras bancas não', () => {
  for (const p of ['p1', 'p2', 'P2', 'p2-t19', 'p2-t27', 'exame']) assert.equal(temFaixaProva({ cai_na_prova: false, prova: p }), true, p)
  for (const p of ['Revalida', 'Revalida 2022.1', 'Residência', 'PUC-SP', 'UFPR 2020', 'PROVA', '']) assert.equal(temFaixaProva({ cai_na_prova: false, prova: p }), false, p)
})

test('faixa PROVA no flashcard: só em Pneumo, tirando o "PROVA · " da frente', () => {
  assert.deepEqual(cardDeProva({ materia_id: 'pneumo', frente: 'PROVA · O que é pneumonia comunitária?' }), { faixa: true, frente: 'O que é pneumonia comunitária?' })
  assert.deepEqual(cardDeProva({ materia_id: 'pneumo', frente: 'O que é pneumonia comunitária?' }), { faixa: false, frente: 'O que é pneumonia comunitária?' })
  assert.deepEqual(cardDeProva({ materia_id: 'pneumo', frente: 'Fora da aula: qual a prova de função?' }), { faixa: false, frente: 'Fora da aula: qual a prova de função?' })
  assert.deepEqual(cardDeProva({ materia_id: 'gastro', frente: 'PROVA · Regra de Goodsall?' }), { faixa: false, frente: 'PROVA · Regra de Goodsall?' })
})

test('faixa PROVA vermelha: o professor disse que cai, mesmo em questão de prova antiga', () => {
  assert.equal(corFaixaProva({ cai_na_prova: true, prova: null, professor_disse_que_cai: true }), 'vermelha')
  assert.equal(corFaixaProva({ cai_na_prova: false, prova: 'p2-t28', professor_disse_que_cai: true }), 'vermelha')
  assert.equal(corFaixaProva({ cai_na_prova: true, prova: null, professor_disse_que_cai: false }), 'ambar')
  assert.equal(corFaixaProva({ cai_na_prova: false, prova: 'p2', professor_disse_que_cai: null }), 'ambar')
  assert.equal(corFaixaProva({ cai_na_prova: false, prova: 'Revalida' }), null)
})
