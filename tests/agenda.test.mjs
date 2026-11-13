import test from 'node:test'
import assert from 'node:assert/strict'
import { lerCronograma } from '../lib/agenda.ts'

const texto = `*SEGUNDA-FEIRA | 9/novembro*

🚨🫁 *18h: prova teórica de pneumologia no CEDETEC.*

🚨🦴 *20h40: prova prática de ortopedia.*

🚻 *13h45-15h: aula teórica de urologia com Dr. Fábio no auditório do B1.*
`

test('agenda: "prova teórica" e "prova prática" viram prova; aula teórica continua teórica', () => {
  const s = lerCronograma(texto, 2026)
  const tipo = (m) => s.eventos.find((e) => e.materia === m)?.tipo
  assert.equal(tipo('pneumo'), 'prova')
  assert.equal(tipo('orto'), 'prova')
  assert.equal(tipo('uro'), 'teorica')
})

test('agenda: no sábado e no domingo mostra a próxima semana já publicada', async () => {
  const { escolherSemana } = await import('../lib/agenda.ts')
  const semanas = [{ semana: '2026-11-02' }, { semana: '2026-11-09' }]
  assert.equal(escolherSemana(semanas, '2026-11-06').semana, '2026-11-02') // sexta
  assert.equal(escolherSemana(semanas, '2026-11-07').semana, '2026-11-09') // sábado
  assert.equal(escolherSemana(semanas, '2026-11-08').semana, '2026-11-09') // domingo
  assert.equal(escolherSemana(semanas, '2026-11-09').semana, '2026-11-09') // segunda
  assert.equal(escolherSemana([{ semana: '2026-11-02' }], '2026-11-08').semana, '2026-11-02') // sem a próxima
})

test('provas: quanto falta conta dias e horas, não só a data', async () => {
  const { fmtFaltaProva, agoraBrasilia } = await import('../lib/agenda.ts')
  // Sexta 13/11/2026, 02h35 em Brasília
  const agora = agoraBrasilia(new Date('2026-11-13T05:35:00Z'))
  assert.equal(fmtFaltaProva({ data: '2026-11-16', inicio: '17:50' }, agora), 'Em 3 dias e 15h')
  assert.equal(fmtFaltaProva({ data: '2026-11-17', inicio: '18:30' }, agora), 'Em 4 dias e 15h')
  assert.equal(fmtFaltaProva({ data: '2026-11-14', inicio: '02:35' }, agora), 'Em 1 dia')
  assert.equal(fmtFaltaProva({ data: '2026-11-13', inicio: '20:40' }, agora), 'Em 18h05')
  assert.equal(fmtFaltaProva({ data: '2026-11-16', inicio: null }, agora), 'Em 3 dias')
})

test('provas: tempo para estudar entre uma prova e a seguinte', async () => {
  const { fmtEntreProvas } = await import('../lib/agenda.ts')
  const p = (data, inicio) => ({ data, inicio })
  assert.deepEqual(fmtEntreProvas(p('2026-11-13', '20:40'), p('2026-11-16', '17:50')), { texto: '2 dias e 21h para estudar', apertado: false })
  assert.deepEqual(fmtEntreProvas(p('2026-11-16', '17:50'), p('2026-11-17', '18:30')), { texto: 'só 1 dia para estudar', apertado: true })
  assert.deepEqual(fmtEntreProvas(p('2026-11-17', '18:30'), p('2026-11-19', '14:00')), { texto: '1 dia e 19h para estudar', apertado: true })
  assert.deepEqual(fmtEntreProvas(p('2026-11-19', '14:00'), p('2026-11-23', '13:45')), { texto: '3 dias e 23h para estudar', apertado: false })
  assert.deepEqual(fmtEntreProvas(p('2026-11-19', '07:30'), p('2026-11-19', '14:00')), { texto: 'só 6h30 para estudar', apertado: true })
  // sem horário em uma das duas, conta só os dias
  assert.deepEqual(fmtEntreProvas(p('2026-11-19', null), p('2026-11-23', '13:45')), { texto: '4 dias para estudar', apertado: false })
  assert.deepEqual(fmtEntreProvas(p('2026-11-19', null), p('2026-11-19', '13:45')), { texto: 'No mesmo dia', apertado: true })
})
