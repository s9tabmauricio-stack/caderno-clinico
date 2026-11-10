import test from 'node:test'
import assert from 'node:assert/strict'
import { ajustarProgressoDiaD, comecarDiaD, responderDiaD } from '../lib/dia-d-progresso.ts'

test('Sabia tira o card; Não sabia manda para o fim e marca o erro uma vez só', () => {
  let p = comecarDiaD(['a', 'b', 'c'])
  p = responderDiaD(p, false)
  assert.deepEqual(p, { fila: ['b', 'c', 'a'], erros: ['a'], feitos: 0 })
  p = responderDiaD(p, true)
  p = responderDiaD(p, true)
  p = responderDiaD(p, false)
  assert.deepEqual(p, { fila: ['a'], erros: ['a'], feitos: 2 })
  p = responderDiaD(p, true)
  assert.deepEqual(p, { fila: [], erros: ['a'], feitos: 3 })
  assert.equal(responderDiaD(p, true), p)
})

test('progresso guardado continua de onde parou e ignora cards que não existem mais', () => {
  const salvo = { fila: ['c', 'x', 'a'], erros: ['a', 'x', 'a'], feitos: 4 }
  assert.deepEqual(ajustarProgressoDiaD(salvo, ['a', 'b', 'c']), { fila: ['c', 'a'], erros: ['a'], feitos: 4 })
})

test('baralho fechado continua fechado; baralho refeito começa do zero', () => {
  assert.deepEqual(ajustarProgressoDiaD({ fila: [], erros: ['b'], feitos: 3 }, ['a', 'b']), { fila: [], erros: ['b'], feitos: 3 })
  assert.equal(ajustarProgressoDiaD({ fila: ['velho-1', 'velho-2'], erros: [], feitos: 1 }, ['novo-1']), null)
})

test('sem progresso ou com dado estragado, não há o que continuar', () => {
  assert.equal(ajustarProgressoDiaD(null, ['a']), null)
  assert.equal(ajustarProgressoDiaD({ fila: 'a', erros: [] }, ['a']), null)
  assert.deepEqual(ajustarProgressoDiaD({ fila: ['a'], erros: [], feitos: -2 }, ['a']), { fila: ['a'], erros: [], feitos: 0 })
})
