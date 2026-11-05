import test from 'node:test'
import assert from 'node:assert/strict'
import { linkMateria, retornoSeguro, rotuloRetorno } from '../lib/navegacao.ts'

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

test('troca de matéria mantém cada seção e o retorno interno', () => {
  const origem = '/desempenho#materia-pneumo'
  for (const [secao, sufixo] of [['aulas', ''], ['banco', '/questoes'], ['flashcards', '/flashcards']]) {
    const url = new URL(linkMateria('nefro', secao, origem), 'https://medgenius.local')
    assert.equal(url.pathname, `/materia/nefro${sufixo}`)
    assert.equal(url.searchParams.get('retorno'), origem)
    assert.equal([...url.searchParams].length, 1)
    assert.equal(linkMateria('nefro', secao), `/materia/nefro${sufixo}`)
  }
  assert.equal(linkMateria('pneumo', 'aulas', 'https://example.com'), '/materia/pneumo')
})
