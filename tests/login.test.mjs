import test from 'node:test'
import assert from 'node:assert/strict'
import { formatarLogin, loginParaEmail } from '../lib/cpf.ts'

test('CPF vira o e-mail interno de sempre', () => {
  assert.deepEqual(loginParaEmail('086.994.266-23'), { email: '08699426623@caderno-clinico.vercel.app', cpf: '08699426623' })
  assert.deepEqual(loginParaEmail(' 08699426623 '), { email: '08699426623@caderno-clinico.vercel.app', cpf: '08699426623' })
})

test('e-mail entra como está, em minúsculas', () => {
  assert.deepEqual(loginParaEmail('  Joao.Silva@Gmail.com '), { email: 'joao.silva@gmail.com', cpf: null })
})

test('CPF curto, longo ou e-mail incompleto dão erro', () => {
  for (const v of ['', '123', '086.994.266-2', '086994266231', 'joao@', 'joao@gmail', '@gmail.com', 'jo ao@gmail.com']) assert.ok('erro' in loginParaEmail(v), v)
})

test('o campo formata CPF e deixa e-mail em paz', () => {
  assert.equal(formatarLogin('08699426623'), '086.994.266-23')
  assert.equal(formatarLogin('0869942'), '086.994.2')
  assert.equal(formatarLogin('joao@gmail.com'), 'joao@gmail.com')
  assert.equal(formatarLogin('123abc'), '123abc')
  assert.equal(formatarLogin('123456789012@x.com'), '123456789012@x.com')
})
