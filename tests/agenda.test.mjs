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
  assert.deepEqual(fmtEntreProvas(p('2026-11-13', '20:40'), p('2026-11-16', '17:50')), { texto: '2 dias e 21h10 para estudar', apertado: false })
  assert.deepEqual(fmtEntreProvas(p('2026-11-16', '17:50'), p('2026-11-17', '18:30')), { texto: '1 dia e 40 min para estudar', apertado: true })
  assert.deepEqual(fmtEntreProvas(p('2026-11-17', '18:30'), p('2026-11-19', '14:00')), { texto: '1 dia e 19h30 para estudar', apertado: true })
  assert.deepEqual(fmtEntreProvas(p('2026-11-19', '14:00'), p('2026-11-23', '13:45')), { texto: '3 dias e 23h45 para estudar', apertado: false })
  assert.deepEqual(fmtEntreProvas(p('2026-11-19', '07:30'), p('2026-11-19', '14:00')), { texto: '6h30 para estudar', apertado: true })
  assert.deepEqual(fmtEntreProvas(p('2026-11-17', '18:30'), p('2026-11-19', '18:30')), { texto: '2 dias para estudar', apertado: false })
  // sem horário em uma das duas, conta só os dias
  assert.deepEqual(fmtEntreProvas(p('2026-11-19', null), p('2026-11-23', '13:45')), { texto: '4 dias para estudar', apertado: false })
  assert.deepEqual(fmtEntreProvas(p('2026-11-19', null), p('2026-11-19', '13:45')), { texto: 'No mesmo dia', apertado: true })
})

test('agenda: "1º/outubro" é dia, e horário sem texto vira aula com os grupos das letras', () => {
  const s = lerCronograma(`*QUINTA-FEIRA | 1º/outubro*

🦴 *19h-19h50*  
- Grupo A: Dr. Eduardo. 
- Grupo B: Dr. Flávio.

*Grupos:*
- A = práticas 1 a 7
- ⁠B = práticas 8 a 14
`, 2026)
  assert.deepEqual(s.dias, ['2026-10-01'])
  const aula = s.eventos.find((e) => e.inicio === '19:00')
  assert.equal(aula.fim, '19:50')
  assert.equal(aula.materia, 'orto')
  assert.equal(aula.titulo, 'Aula de ortopedia')
  assert.deepEqual(aula.grupos, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
  assert.equal(aula.notas.length, 2)
})

test('agenda: cancelamento com explicação, recado da semana e dia sem atividades', () => {
  const s = lerCronograma(`*CRONOGRAMA SEMANAL*
_16/novembro — 20/novembro_

❌ *Não haverá mais aulas práticas regulares nesta semana!* As práticas já foram encerradas para todos os grupos.

*QUARTA-FEIRA | 18/novembro*

❌🫁 Não haverá mais aula teórica de pneumologia e nem discussão de casos clínicos. A disciplina já foi encerrada.

❌🫁 Não haverá aula prática de pneumologia com Dr. Vinicius A. Guerra.

*SEXTA-FEIRA | 20/novembro — Dia Nacional de Zumbi e da Consciência Negra*

❌ Não haverá nenhuma atividade.
`, 2026)
  assert.match(s.aviso, /^Não haverá mais aulas práticas regulares/)
  const [pneumo, pratica, sexta] = s.eventos
  assert.equal(pneumo.titulo, 'Teórica de pneumologia e discussão de casos clínicos')
  assert.deepEqual(pneumo.notas, ['A disciplina já foi encerrada.'])
  assert.equal(pneumo.cancelado, true)
  assert.equal(pratica.professor, 'Dr. Vinicius A. Guerra')
  assert.deepEqual(pratica.notas, [])
  assert.equal(sexta.tipo, 'aviso')
  assert.equal(sexta.titulo, 'Dia Nacional de Zumbi e da Consciência Negra')
  assert.deepEqual(sexta.notas, ['Não haverá nenhuma atividade.'])
})

test('agenda: matérias do 6º período da T29 são reconhecidas pelo nome', () => {
  const s = lerCronograma(`*TERÇA-FEIRA | 1/dezembro*

13h30: aula teórica de dermatologia com Dra. Ana.

15h: aula teórica de reumatologia com Dr. Beto.

16h: aula teórica de hematologia com Dra. Carla.

17h: aula teórica de endocrinologia com Dr. Davi.

19h: aula teórica de cardiologia com Dr. Edu.

20h: PROEX no B1.

21h: aula teórica de neurologia sobre hematoma subdural com Dr. Fábio.
`, 2026)
  const materias = s.eventos.map((e) => e.materia)
  assert.deepEqual(materias, ['derma', 'reumato', 'hemato', 'endocrino', 'cardio', 'proex', 'neuro'])
})
