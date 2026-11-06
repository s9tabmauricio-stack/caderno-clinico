import test from 'node:test'
import assert from 'node:assert/strict'
import { daProximaProva, ritmoDiario } from '../lib/preparacao-prova.ts'

test('preparação exclui outras matérias e não usa totais gerais sem prova vinculada', () => {
  const itens = [{ materia_id: 'pneumo', total: 10 }, { materia_id: 'nefro', total: 500 }]
  assert.deepEqual(daProximaProva(itens, 'pneumo'), [itens[0]])
  for (const materia of [undefined, '', 'desconhecida']) {
    assert.deepEqual(daProximaProva(itens, materia), [])
  }
})

test('ritmo distribui pendências antes da prova sem divisão por zero', () => {
  assert.equal(ritmoDiario(10, 3), 4)
  assert.equal(ritmoDiario(10, 1), 10)
  assert.equal(ritmoDiario(10, 0), 10)
  assert.equal(ritmoDiario(0, 3), 0)
})
