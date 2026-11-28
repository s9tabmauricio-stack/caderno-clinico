import test from 'node:test'
import assert from 'node:assert/strict'
import { organizarPeriodos } from '../lib/periodos.ts'

test('T29 no 6º período: o 6º aparece mesmo vazio, o 5º fica como anterior', () => {
  const r = organizarPeriodos([{ id: 'nefro', periodo: 5 }, { id: 'pneumo', periodo: 5 }], [6])
  assert.equal(r.atual, 6)
  assert.deepEqual(r.periodos, [6, 5])
  assert.equal(r.materias.filter((m) => m.periodo === 6).length, 0)
})

test('matéria sem período cai no período atual; administrador vê os períodos de todas as turmas', () => {
  const r = organizarPeriodos([{ id: 'neuro', periodo: 6 }, { id: 'nova', periodo: null }, { id: 'nefro', periodo: 5 }], [7, 6])
  assert.equal(r.atual, 7)
  assert.deepEqual(r.periodos, [7, 6, 5])
  assert.equal(r.materias.find((m) => m.id === 'nova').periodo, 7)
})
