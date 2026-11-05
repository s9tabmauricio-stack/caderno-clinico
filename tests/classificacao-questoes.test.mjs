import test from 'node:test'
import assert from 'node:assert/strict'
import { classificacaoValida, filtroClassificacaoValido, filtrarQuestoes, rotuloClassificacao } from '../lib/classificacao-questoes.ts'

const base = { tema: 'TEP', prova: 'p2', resposta: { acertou: true } }
const questoes = [
  { ...base, id: 'urgente-certa', classificacao: 'rever' },
  { ...base, id: 'urgente-errada', classificacao: 'rever', resposta: { acertou: false } },
  { ...base, id: 'tempo', classificacao: 'se_der_tempo' },
  { ...base, id: 'basica', classificacao: 'basico' },
  { ...base, id: 'complicada', classificacao: 'complicado' },
  { ...base, id: 'sem-marca', classificacao: null, resposta: null },
  { ...base, id: 'outro-tema', classificacao: 'rever', tema: 'Asma' },
  { ...base, id: 'outra-prova', classificacao: 'rever', prova: 'p1' },
]
const todos = { tema: null, prova: null, situacao: 'todas', classificacao: 'todas' }
const ids = (f) => filtrarQuestoes(questoes, { ...todos, ...f }).map((q) => q.id)

test('revisão inclui questões certas marcadas e combina tema, prova e situação', () => {
  assert.deepEqual(ids({ classificacao: 'rever', tema: 'TEP', prova: 'p2' }), ['urgente-certa', 'urgente-errada'])
  assert.deepEqual(ids({ classificacao: 'rever', tema: 'TEP', prova: 'p2', situacao: 'erradas' }), ['urgente-errada'])
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
