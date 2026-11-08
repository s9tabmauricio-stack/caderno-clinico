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
