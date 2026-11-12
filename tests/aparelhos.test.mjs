import test from 'node:test'
import assert from 'node:assert/strict'
import { CONFERIR_A_CADA_S, precisaConferir, rotuloLimite, valorCookieAparelho } from '../lib/aparelhos.ts'

const sid = '3f1c2a9e-0000-4000-8000-000000000001'

test('confere a sessão na primeira vez e quando o intervalo passa', () => {
  const agora = 1_800_000_000
  assert.equal(precisaConferir(undefined, sid, agora), true)
  assert.equal(precisaConferir(valorCookieAparelho(sid, agora), sid, agora + 10), false)
  assert.equal(precisaConferir(valorCookieAparelho(sid, agora), sid, agora + CONFERIR_A_CADA_S), true)
})

test('outra sessão ou cookie estragado obrigam a conferir', () => {
  const agora = 1_800_000_000
  assert.equal(precisaConferir(valorCookieAparelho('outra', agora), sid, agora), true)
  for (const c of ['', 'lixo', `${sid}.`, `${sid}.abc`, `.${agora}`, `${sid}.${agora + 3600}`]) assert.equal(precisaConferir(c, sid, agora), true, c)
})

test('rótulo do limite na Administração', () => {
  assert.equal(rotuloLimite(1), '1 aparelho')
  assert.equal(rotuloLimite(2), 'até 2 aparelhos')
  assert.equal(rotuloLimite(null), 'sem limite de aparelhos')
})
