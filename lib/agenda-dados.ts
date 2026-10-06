import type { SupabaseClient } from '@supabase/supabase-js'
import type { Database } from '@/lib/database.types'
import { agoraBrasilia } from '@/lib/agenda'

type Cliente = SupabaseClient<Database>
export type EventoBanco = Database['public']['Tables']['agenda_eventos']['Row']

const COLUNAS = 'id, semana, data, inicio, fim, materia, tipo, titulo, professor, local, grupos, cancelado, notas, ordem'

/** Grupo de prática do aluno (null se ainda não informou). */
export async function grupoDoAluno(supabase: Cliente, userId: string) {
  const { data } = await supabase.from('perfis').select('grupo').eq('id', userId).maybeSingle()
  return data?.grupo ?? null
}

export async function agendaDoDia(supabase: Cliente, data: string) {
  const { data: evs, error } = await supabase.from('agenda_eventos').select(COLUNAS).eq('data', data).order('ordem')
  if (error) return []
  return evs
}

/** Semana que contém hoje; no fim de semana, a próxima publicada (ou a última). */
export async function agendaDaSemana(supabase: Cliente) {
  const { data: hoje } = agoraBrasilia()
  const { data: semanas } = await supabase.from('agenda_semanas').select('semana, titulo, aviso').order('semana')
  if (!semanas?.length) return null
  const fimDaSemana = (s: string) => {
    const d = new Date(`${s}T12:00:00Z`)
    d.setUTCDate(d.getUTCDate() + 6)
    return d.toISOString().slice(0, 10)
  }
  const escolhida =
    semanas.find((s) => s.semana <= hoje && hoje <= fimDaSemana(s.semana)) ??
    semanas.find((s) => s.semana > hoje) ??
    semanas[semanas.length - 1]
  const { data: evs } = await supabase.from('agenda_eventos').select(COLUNAS).eq('semana', escolhida.semana).order('data').order('ordem')
  return { ...escolhida, eventos: evs ?? [] }
}
