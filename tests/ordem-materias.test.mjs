import test from 'node:test'
import assert from 'node:assert/strict'
import { ordenarMateriasPorProva } from '../lib/ordem-materias.ts'

test('ordena pela primeira prova futura válida e preserva matérias sem prova ao final', () => {
  const materias = ['nefro', 'pneumo', 'orto', 'uro', 'pass'].map(id => ({ id }))
  const prova = (materia, data, cancelado = false) => ({ materia, data, inicio: '18:00', cancelado })
  const provas = [prova('orto', '2026-11-19'), prova('nefro', '2026-11-12'), prova('pneumo', '2026-11-10'), prova('orto', '2026-11-13'), prova('uro', '2026-11-06', true), prova('pass', '2026-11-01')]
  assert.deepEqual(ordenarMateriasPorProva(materias, provas, Date.parse('2026-11-05T12:00:00Z')).map(m => m.id), ['pneumo', 'nefro', 'orto', 'uro', 'pass'])
  assert.equal(materias[0].id, 'nefro')
})
