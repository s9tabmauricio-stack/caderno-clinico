import test from 'node:test'
import assert from 'node:assert/strict'
import { createClient } from '@supabase/supabase-js'
import { apagarClassificacoes } from '../lib/apagar-classificacoes.ts'

function cenario({ quantidade = 3, falhaLeitura = false, falhaExclusao = false } = {}) {
  const questoes = Array.from({ length: quantidade }, (_, i) => ({
    id: `q${i}`, materia_id: 'pneumo', aula_id: i === 0 ? 'pneumo-a1' : 'pneumo-a2',
  }))
  questoes.push({ id: 'outra', materia_id: 'gastro', aula_id: 'gastro-a1' })
  const marcas = ['aluno', 'colega'].flatMap((user_id) => questoes.map((q) => ({ user_id, questao_id: q.id })))
  const respostas = [{ user_id: 'aluno', questao_id: 'q0', tentativas: 2 }]
  const historico = [{ user_id: 'aluno', questao_id: 'q0' }]
  const revisoes = [{ user_id: 'aluno', flashcard_id: 'f1' }]
  const chamadas = []
  const supabase = createClient('https://teste.supabase.co', 'chave-de-teste', {
    auth: { persistSession: false, autoRefreshToken: false },
    global: { fetch: async (input, init) => {
      const url = new URL(String(input))
      const tabela = url.pathname.split('/').at(-1)
      const params = url.searchParams
      chamadas.push({ tabela, metodo: init.method, params })
      const erro = (mensagem) => new Response(JSON.stringify({ message: mensagem }), { status: 500 })
      if (init.method === 'GET' && tabela === 'questoes') {
        if (falhaLeitura) return erro('Falha na leitura')
        const coluna = params.has('materia_id') ? 'materia_id' : 'aula_id'
        const filtradas = questoes.filter((q) => `eq.${q[coluna]}` === params.get(coluna))
        const de = Number(params.get('offset') ?? 0)
        const limite = Number(params.get('limit'))
        return new Response(JSON.stringify(filtradas.slice(de, de + limite).map(({ id }) => ({ id }))))
      }
      assert.equal(tabela, 'classificacoes_questoes', 'Não deve alterar outras tabelas')
      assert.equal(init.method, 'DELETE')
      assert.equal(params.get('user_id'), 'eq.aluno')
      if (falhaExclusao) return erro('Falha ao apagar')
      const filtro = params.get('questao_id')
      const ids = filtro ? filtro.slice(4, -1).split(',') : null
      for (let i = marcas.length - 1; i >= 0; i--) {
        if (marcas[i].user_id === 'aluno' && (!ids || ids.includes(marcas[i].questao_id))) marcas.splice(i, 1)
      }
      return new Response(null, { status: 204 })
    } },
  })
  return { supabase, marcas, respostas, historico, revisoes, chamadas, questoes }
}

test('apaga todas as classificações só do aluno e preserva o progresso', async () => {
  const c = cenario()
  await apagarClassificacoes(c.supabase, 'aluno', { onde: 'tudo' })
  assert.equal(c.marcas.length, c.questoes.length)
  assert.ok(c.marcas.every((m) => m.user_id === 'colega'))
  assert.equal(c.chamadas.length, 1)
  assert.equal(c.respostas[0].tentativas, 2)
  assert.equal(c.historico.length, 1)
  assert.equal(c.revisoes.length, 1)
})

test('uma aula não apaga marcações das outras aulas ou colegas', async () => {
  const c = cenario()
  await apagarClassificacoes(c.supabase, 'aluno', { onde: 'aula', alvo: 'pneumo-a1' })
  assert.equal(c.marcas.filter((m) => m.user_id === 'aluno').length, 3)
  assert.ok(!c.marcas.some((m) => m.user_id === 'aluno' && m.questao_id === 'q0'))
  assert.equal(c.marcas.filter((m) => m.user_id === 'colega').length, 4)
})

test('uma matéria com mais de mil questões é apagada por inteiro em lotes curtos', async () => {
  const c = cenario({ quantidade: 1203 })
  await apagarClassificacoes(c.supabase, 'aluno', { onde: 'materia', alvo: 'pneumo' })
  assert.deepEqual(c.marcas.filter((m) => m.user_id === 'aluno'), [{ user_id: 'aluno', questao_id: 'outra' }])
  assert.equal(c.marcas.filter((m) => m.user_id === 'colega').length, 1204)
  assert.equal(c.chamadas.filter((ch) => ch.metodo === 'GET').length, 3)
  for (const ch of c.chamadas.filter((ch) => ch.metodo === 'DELETE')) {
    assert.ok(ch.params.get('questao_id').split(',').length <= 100)
  }
})

test('escopo sem questões não emite exclusão; alvo vazio é rejeitado', async () => {
  const c = cenario()
  await apagarClassificacoes(c.supabase, 'aluno', { onde: 'aula', alvo: 'vazia' })
  assert.equal(c.chamadas.filter((ch) => ch.metodo === 'DELETE').length, 0)
  await assert.rejects(apagarClassificacoes(c.supabase, 'aluno', { onde: 'materia', alvo: '' }))
})

test('falhas de leitura ou exclusão são propagadas, sem informar sucesso', async () => {
  for (const opcoes of [{ falhaLeitura: true }, { falhaExclusao: true }]) {
    const c = cenario(opcoes)
    await assert.rejects(apagarClassificacoes(c.supabase, 'aluno', { onde: 'materia', alvo: 'pneumo' }))
    assert.equal(c.marcas.length, 8)
  }
})
