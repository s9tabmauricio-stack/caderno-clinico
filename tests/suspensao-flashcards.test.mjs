import test from 'node:test'
import assert from 'node:assert/strict'
import { avancarSemCard } from '../lib/suspensao-flashcards.ts'
import { contarPendentes } from '../lib/pendencias.ts'

test('suspender avança sem contar avaliação ou erro e remove repetições da fila', () => {
  const anterior = { atual: 'a', fila: ['b', 'a', 'c', 'a'], virado: true, feitos: 5, erros: 2 }
  assert.deepEqual(avancarSemCard(anterior, 'a'), {
    atual: 'b', fila: ['c'], virado: false, feitos: 5, erros: 2,
  })
  assert.deepEqual(anterior.fila, ['b', 'a', 'c', 'a'])
  assert.equal(anterior.virado, true)
})

test('suspender o último card conclui a sessão sem inventar revisão', () => {
  assert.deepEqual(avancarSemCard({ atual: 'a', fila: [], virado: true, feitos: 0, erros: 0 }, 'a'), {
    atual: null, fila: [], virado: false, feitos: 0, erros: 0,
  })
})

test('pendências descontam suspensos novos, vencidos e em dia sem alterar os totais do histórico', () => {
  const aula = {
    total_cards: 10, cards_estudados: 6, cards_vencidos: 3,
    cards_suspensos: 4, cards_suspensos_estudados: 2, cards_suspensos_vencidos: 1,
  }
  assert.deepEqual(contarPendentes([aula]), { novos: 2, vencidos: 2, hoje: 4, emDia: 2 })
  assert.equal(aula.total_cards, 10)
  assert.equal(aula.cards_estudados, 6)
})

test('reativar devolve a pendência conforme o estado original, inclusive card ainda novo', () => {
  const base = { total_cards: 1, cards_estudados: 0, cards_vencidos: 0 }
  assert.equal(contarPendentes([{ ...base, cards_suspensos: 1 }]).hoje, 0)
  assert.deepEqual(contarPendentes([base]), { novos: 1, vencidos: 0, hoje: 1, emDia: 0 })
  assert.deepEqual(contarPendentes([{ ...base, cards_estudados: 1, cards_vencidos: 1 }]), { novos: 0, vencidos: 1, hoje: 1, emDia: 0 })
  assert.deepEqual(contarPendentes([{ ...base, cards_estudados: 1 }]), { novos: 0, vencidos: 0, hoje: 0, emDia: 1 })
})

test('fila vazia ou todos suspensos não geram pendências', () => {
  const vazia = { novos: 0, vencidos: 0, hoje: 0, emDia: 0 }
  assert.deepEqual(contarPendentes([]), vazia)
  assert.deepEqual(contarPendentes([{
    total_cards: 5, cards_estudados: 3, cards_vencidos: 2,
    cards_suspensos: 5, cards_suspensos_estudados: 3, cards_suspensos_vencidos: 2,
  }]), vazia)
})
