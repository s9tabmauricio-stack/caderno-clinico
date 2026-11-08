import test from 'node:test'
import assert from 'node:assert/strict'
import { classificacaoValida, filtroClassificacaoValido, filtrarQuestoes, fonteDaQuestao, fonteValida, ordenarPorFonte, rotuloClassificacao } from '../lib/classificacao-questoes.ts'

const base = { tema: 'TEP', prova: 'p2', fonte: 'P2 · nº 4', resposta: { acertou: true } }
const questoes = [
  { ...base, id: 'urgente-certa', classificacao: 'rever' },
  { ...base, id: 'urgente-errada', classificacao: 'rever', resposta: { acertou: false } },
  { ...base, id: 'tempo', classificacao: 'se_der_tempo' },
  { ...base, id: 'basica', classificacao: 'basico' },
  { ...base, id: 'complicada', classificacao: 'complicado' },
  { ...base, id: 'sem-marca', classificacao: null, resposta: null },
  { ...base, id: 'outro-tema', classificacao: 'rever', tema: 'Asma' },
  { ...base, id: 'outra-fonte', classificacao: 'rever', prova: null, fonte: 'Montada (aula 2026)' },
]
const todos = { tema: null, fonte: null, situacao: 'todas', classificacao: 'todas' }
const ids = (f) => filtrarQuestoes(questoes, { ...todos, ...f }).map((q) => q.id)

test('revisão inclui questões certas marcadas e combina tema, fonte e situação', () => {
  assert.deepEqual(ids({ classificacao: 'rever', tema: 'TEP', fonte: 'fag' }), ['urgente-certa', 'urgente-errada'])
  assert.deepEqual(ids({ classificacao: 'rever', tema: 'TEP', fonte: 'fag', situacao: 'erradas' }), ['urgente-errada'])
  assert.deepEqual(ids({ classificacao: 'marcadas', situacao: 'abertas' }), [])
})

test('cada prioridade e todas as marcadas podem ser reencontradas', () => {
  assert.deepEqual(ids({ classificacao: 'se_der_tempo' }), ['tempo'])
  assert.deepEqual(ids({ classificacao: 'basico' }), ['basica'])
  assert.deepEqual(ids({ classificacao: 'complicado' }), ['complicada'])
  assert.equal(ids({ classificacao: 'marcadas' }).length, 7)
  assert.equal(ids({}).length, 8)
})

test('trocar e remover a marcação atualiza os filtros sem alterar resposta ou tentativas', () => {
  const original = questoes[0]
  const trocada = { ...original, classificacao: 'basico' }
  const removida = { ...original, classificacao: null }
  assert.equal(filtrarQuestoes([trocada], { ...todos, classificacao: 'rever' }).length, 0)
  assert.equal(filtrarQuestoes([trocada], { ...todos, classificacao: 'basico' }).length, 1)
  assert.equal(filtrarQuestoes([removida], { ...todos, classificacao: 'marcadas' }).length, 0)
  assert.equal(trocada.resposta, original.resposta)
  assert.equal(original.classificacao, 'rever')
})

test('cookies antigos e filtros inválidos voltam para todas as questões', () => {
  for (const invalido of [undefined, null, '', 'urgente', [], {}, '<script>']) {
    assert.equal(classificacaoValida(invalido), null)
    assert.equal(filtroClassificacaoValido(invalido), 'todas')
  }
  assert.equal(filtroClassificacaoValido('marcadas'), 'marcadas')
  assert.equal(filtroClassificacaoValido('rever'), 'rever')
  assert.equal(filtroClassificacaoValido('complicado'), 'complicado')
  // As marcas e os links antigos do amarelo continuam válidos, com o texto novo.
  assert.equal(classificacaoValida('se_der_tempo'), 'se_der_tempo')
  assert.equal(rotuloClassificacao('se_der_tempo'), 'É bom rever cara')
})

test('cada questão cai numa das três fontes', () => {
  const f = (prova, fonte) => fonteDaQuestao({ prova, fonte })
  assert.equal(f(null, 'Montada (aula 2026)'), 'apostila')
  assert.equal(f(null, null), 'apostila')
  for (const p of ['p1', 'p2', 'p2-t23', 'exame']) assert.equal(f(p, 'qualquer'), 'fag')
  assert.equal(f(null, 'Guia de estudo do 2º bimestre (material da turma)'), 'fag')
  assert.equal(f('Residência', 'HOB-DF 2025'), 'concursos')
  assert.equal(f('Revalida 2024.1', 'Revalida INEP 2024.1 · nº 45'), 'concursos')
  assert.equal(f('UFPR 2020', 'UFPR Residência Médica 2020 · nº 19'), 'concursos')
  assert.equal(fonteValida('fag'), 'fag')
  assert.equal(fonteValida('p2'), null)
  assert.deepEqual(ids({ fonte: 'apostila' }), ['outra-fonte'])
})

test('questões aparecem com as da FAG primeiro, depois residência, depois as montadas', () => {
  const lista = [
    { id: 'm1', prova: null, fonte: 'Montada (aula 2026)' },
    { id: 'r1', prova: 'Residência', fonte: 'USP 2020' },
    { id: 'f1', prova: 'p2', fonte: 'P2 · nº 4' },
    { id: 'm2', prova: null, fonte: null },
    { id: 'f2', prova: null, fonte: 'Guia de estudo' },
    { id: 'r2', prova: 'Revalida 2022.1', fonte: 'INEP' },
  ]
  assert.deepEqual(ordenarPorFonte(lista).map((q) => q.id), ['f1', 'f2', 'r1', 'r2', 'm1', 'm2'])
})
