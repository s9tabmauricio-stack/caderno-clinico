import test from 'node:test'
import assert from 'node:assert/strict'
import { destinoAposLogin, rotaPublica } from '../lib/auth.ts'

test('somente rotas de autenticação são públicas', () => {
  for (const path of ['/login', '/auth', '/auth/callback', '/auth/confirm', '/auth/erro', '/auth/sair']) assert.equal(rotaPublica(path), true)
  for (const path of ['/', '/admin', '/agenda', '/login-extra', '/authentic', '/aula/pneumo-a2']) assert.equal(rotaPublica(path), false)
})

test('login preserva a página solicitada e seus filtros', () => {
  for (const path of ['/', '/agenda', '/admin/conteudo', '/aula/pneumo-a2?aba=questoes', '/estudar?q=doenca%20pulmonar', '/desempenho#materia-pneumo']) assert.equal(destinoAposLogin(path), path)
})

test('login rejeita URLs externas, barras ambíguas, controles e ciclos de autenticação', () => {
  for (const path of [null, undefined, ['/agenda'], 'https://example.com', '//example.com', '/%2fexample.com', '/\\example.com', '/%5cexample.com', '/%0aexample.com', '/login', '/auth/sair', '/a/../login', '/a/%2e%2e/auth/sair', '/%61uth/callback', '/%', '/' + 'a'.repeat(2001)]) assert.equal(destinoAposLogin(path), '/', String(path))
})
