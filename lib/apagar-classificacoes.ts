import type { SupabaseClient } from '@supabase/supabase-js'
import type { Database } from './database.types'

export type EscopoClassificacoes =
  | { onde: 'tudo' }
  | { onde: 'materia' | 'aula'; alvo: string }

// Usa o cliente do aluno: a RLS e o filtro de usuário protegem as marcações dos colegas.
export async function apagarClassificacoes(
  supabase: SupabaseClient<Database>,
  userId: string,
  escopo: EscopoClassificacoes,
) {
  if (escopo.onde === 'tudo') {
    const { error } = await supabase.from('classificacoes_questoes').delete().eq('user_id', userId)
    if (error) throw error
    return
  }
  if (!escopo.alvo) throw new Error('Escolha uma matéria ou aula.')

  // Pagina antes de apagar, para incluir matérias com mais de mil questões.
  const ids: string[] = []
  const tamanhoPagina = 500
  for (let de = 0; ; de += tamanhoPagina) {
    const { data, error } = await supabase
      .from('questoes')
      .select('id')
      .eq(escopo.onde === 'materia' ? 'materia_id' : 'aula_id', escopo.alvo)
      .order('id')
      .range(de, de + tamanhoPagina - 1)
    if (error) throw error
    ids.push(...(data ?? []).map((q) => q.id))
    if (!data || data.length < tamanhoPagina) break
  }

  // Lotes curtos evitam ultrapassar o limite de tamanho da URL da API.
  for (let de = 0; de < ids.length; de += 100) {
    const { error } = await supabase
      .from('classificacoes_questoes')
      .delete()
      .eq('user_id', userId)
      .in('questao_id', ids.slice(de, de + 100))
    if (error) throw error
  }
}
