import test from 'node:test'
import assert from 'node:assert/strict'
import { correspondeBusca, retornoSeguro, rotuloRetorno } from '../lib/navegacao.ts'

test('busca ignora acentos, caixa e espaços e combina título com matéria', () => {
  assert.equal(correspondeBusca('  PNEUMONIA clinica ', 'Pneumonia hospitalar', null, 'Clínica médica'), true)
  assert.equal(correspondeBusca('nefrologia', 'Introdução', 'Doenças renais', 'Nefrologia'), true)
  assert.equal(correspondeBusca('pneumonia renal', 'Pneumonia hospitalar'), false)
  assert.equal(correspondeBusca('asma', null, undefined), false)
})

test('retorno preserva busca, filtros, aba e âncora', () => {
  for (const href of ['/estudar?q=pneumonia+hospitalar', '/desempenho#materia-pneumo', '/aula/pneumo-a2?aba=questoes&retorno=%2Festudar%3Fq%3Dpneumonia', '/materia/pneumo/questoes?tema=DPOC&prova=p1&mostrar=erradas']) {
    assert.equal(retornoSeguro(href), href)
  }
})

test('retorno rejeita destinos externos, rotas indevidas e entradas ambíguas', () => {
  for (const href of [undefined, ['/', '/estudar'], 'https://example.com', '//example.com', 'javascript:alert(1)', '/admin', '/auth/sair', '/estudar-malicioso', '/aula/a/../../auth/sair', '/estudar\\example.com', '/estudar\n', '/estudar?q=' + 'a'.repeat(2000)]) {
    assert.equal(retornoSeguro(href), null)
  }
})

test('rótulos explicam para onde o aluno volta', () => {
  assert.equal(rotuloRetorno('/estudar?q=pneumonia'), 'Resultados da busca')
  assert.equal(rotuloRetorno('/desempenho#materia-pneumo'), 'Desempenho')
  assert.equal(rotuloRetorno('/aula/pneumo-a2?aba=questoes'), 'Aula')
})
