import test from 'node:test'
import assert from 'node:assert/strict'
import { retornoSeguro, rotuloRetorno } from '../lib/navegacao.ts'

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
  assert.equal(rotuloRetorno('/estudar'), 'Matérias')
  assert.equal(rotuloRetorno('/desempenho#materia-pneumo'), 'Desempenho')
  assert.equal(rotuloRetorno('/aula/pneumo-a2?aba=questoes'), 'Aula')
})
