import test from 'node:test'
import assert from 'node:assert/strict'
import { fmtFalta, fmtPeriodo, marcoDoInicio, marcosDaSemana, marcosDoDia, porMes } from '../lib/calendario.ts'

const marcos = [
  { id: 1, inicio: '2027-04-05', fim: '2027-04-16', tipo: 'provas', titulo: 'Semana de provas' },
  { id: 2, inicio: '2027-04-21', fim: null, tipo: 'feriado', titulo: 'Tiradentes' },
  { id: 3, inicio: '2027-04-24', fim: null, tipo: 'notas', titulo: 'Prazo das notas' },
  { id: 4, inicio: '2027-06-28', fim: '2027-07-02', tipo: 'exames', titulo: 'Semana de exames' },
]

test('calendário: o dia mostra o que vale nele, sem prazo de nota', () => {
  assert.deepEqual(marcosDoDia(marcos, '2027-04-16').map((m) => m.id), [1])
  assert.deepEqual(marcosDoDia(marcos, '2027-04-21').map((m) => m.id), [2])
  assert.deepEqual(marcosDoDia(marcos, '2027-04-24'), [])
  assert.deepEqual(marcosDaSemana(marcos, '2027-04-19').map((m) => m.id), [2])
})

test('calendário: Início mostra o que vale hoje e o próximo que vai começar', () => {
  const r = marcoDoInicio(marcos, '2027-04-10')
  assert.deepEqual(r.agora.map((m) => m.id), [1])
  assert.equal(r.proximo?.id, 2)
  assert.equal(marcoDoInicio(marcos, '2027-07-03').proximo, null)
})

test('calendário: datas por extenso e contagem', () => {
  assert.equal(fmtPeriodo(marcos[1]), '21 de abr')
  assert.equal(fmtPeriodo(marcos[0]), '5 a 16 de abr')
  assert.equal(fmtPeriodo(marcos[3]), '28 de jun a 2 de jul')
  assert.equal(fmtFalta('2027-04-20', '2027-04-21'), 'amanhã')
  assert.equal(fmtFalta('2027-04-01', '2027-04-21'), 'em 20 dias')
  assert.deepEqual(porMes(marcos).map(([k, l]) => [k, l.length]), [['2027-04', 3], ['2027-06', 1]])
})
