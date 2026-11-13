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
