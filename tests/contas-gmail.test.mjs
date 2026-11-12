import test from 'node:test'
import assert from 'node:assert/strict'
import { chaveConfere, lerPedidoConta } from '../lib/contas-gmail.ts'
import { rotaPublica } from '../lib/auth.ts'

test('e-mail da FAG com 6 números vira pedido de conta', () => {
  assert.deepEqual(lerPedidoConta({ email: ' Joao.Silva@Minha.FAG.edu.br ', senha: '123456', nome: 'João' }), {
    email: 'joao.silva@minha.fag.edu.br',
    senha: '123456',
    nome: 'João',
  })
})

test('robô recusa e-mail de fora, senha fora do formato e corpo vazio', () => {
  for (const corpo of [
    { email: 'joao@gmail.com', senha: '123456' },
    { email: 'joao@minha.fag.edu.br.evil.com', senha: '123456' },
    { email: 'joao@fag.edu.br', senha: '123456' },
    { email: 'a@b@minha.fag.edu.br', senha: '123456' },
    { email: '@minha.fag.edu.br', senha: '123456' },
    { email: 'joao@minha.fag.edu.br', senha: '12345' },
    { email: 'joao@minha.fag.edu.br', senha: '1234567' },
    { email: 'joao@minha.fag.edu.br', senha: 'abcdef' },
    { email: 'joao@minha.fag.edu.br' },
    null,
    'texto',
  ]) assert.ok('erro' in lerPedidoConta(corpo), JSON.stringify(corpo))
})

test('chave do robô só confere quando é idêntica', () => {
  assert.equal(chaveConfere('abc123', 'abc123'), true)
  for (const r of ['', 'abc12', 'abc124', 'abc1234']) assert.equal(chaveConfere(r, 'abc123'), false)
  assert.equal(chaveConfere('', ''), false)
})

test('a rota do robô não pede login (tem chave própria)', () => {
  assert.equal(rotaPublica('/api/contas-gmail'), true)
  assert.equal(rotaPublica('/api/outra'), false)
})
