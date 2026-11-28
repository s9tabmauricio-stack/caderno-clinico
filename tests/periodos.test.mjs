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

test('cada turma com a sua matéria: "neuro" da agenda da T29 abre neuro29, da T28 abre neuro', async () => {
  const { materiaDaTurma } = await import('../lib/periodos.ts')
  const materias = [
    { id: 'neuro', chave_agenda: null, turmas: ['t28'], periodo: 6 },
    { id: 'neuro29', chave_agenda: 'neuro', turmas: ['t29'], periodo: 6 },
    { id: 'nefro', chave_agenda: null, turmas: ['t29'], periodo: 5 },
  ]
  assert.equal(materiaDaTurma('neuro', 't29', materias), 'neuro29')
  assert.equal(materiaDaTurma('neuro', 't28', materias), 'neuro')
  assert.equal(materiaDaTurma('nefro', 't29', materias), 'nefro')
  assert.equal(materiaDaTurma('cardio', 't29', materias), 'cardio')
  assert.equal(materiaDaTurma(null, 't29', materias), null)
})
