import type { SupabaseClient } from '@supabase/supabase-js'
import type { Database } from '@/lib/database.types'
import { agoraBrasilia, escolherSemana } from '@/lib/agenda'

type Cliente = SupabaseClient<Database>
export type EventoBanco = Database['public']['Tables']['agenda_eventos']['Row']

const COLUNAS = 'id, semana, data, inicio, fim, materia, tipo, titulo, professor, local, grupos, cancelado, notas, ordem, fixo'

/** Prova incluída à parte (fixo) sai do dia quando o cronograma do WhatsApp já traz a prova daquela matéria no mesmo dia. */
function semProvaRepetida(evs: EventoBanco[]) {
  const ehProva = (e: EventoBanco) => /prova/i.test(e.titulo) && !/vista/i.test(e.titulo)
  return evs.filter((e) => !e.fixo || !evs.some((o) => !o.fixo && o.data === e.data && o.materia === e.materia && ehProva(o)))
}

/** Grupo de prática do aluno (null se ainda não informou). */
export async function grupoDoAluno(supabase: Cliente, userId: string) {
  const { data } = await supabase.from('perfis').select('grupo').eq('id', userId).maybeSingle()
  return data?.grupo ?? null
}

export async function agendaDoDia(supabase: Cliente, data: string) {
  // Pelo horário, para as provas incluídas à parte caírem no lugar certo entre as aulas do cronograma
  const { data: evs, error } = await supabase
    .from('agenda_eventos')
    .select(COLUNAS)
    .eq('data', data)
    .order('inicio', { nullsFirst: true })
    .order('ordem')
  if (error) return []
  return semProvaRepetida(evs)
}

/** Semana que contém hoje; no sábado e no domingo, a próxima publicada (ou a última). */
export async function agendaDaSemana(supabase: Cliente) {
  const { data: hoje } = agoraBrasilia()
  // Semana sem cronograma (texto vazio) só existe por causa das provas: entra quando chegar, nunca como "a próxima"
  const { data: semanas } = await supabase
    .from('agenda_semanas')
    .select('semana, titulo, aviso')
    .or(`texto.not.is.null,semana.lte.${hoje}`)
    .order('semana')
  if (!semanas?.length) return null
  const escolhida = escolherSemana(semanas, hoje)
  const { data: evs } = await supabase
    .from('agenda_eventos')
    .select(COLUNAS)
    .eq('semana', escolhida.semana)
    .order('data')
    .order('inicio', { nullsFirst: true })
    .order('ordem')
  return { ...escolhida, eventos: semProvaRepetida(evs ?? []) }
}

/** Provas incluídas à parte (P2 e outras), de hoje em diante. */
export async function proximasProvas(supabase: Cliente) {
  const { data: hoje } = agoraBrasilia()
  const { data: evs } = await supabase
    .from('agenda_eventos')
    .select(COLUNAS)
    .eq('fixo', true)
    .eq('tipo', 'prova')
    .gte('data', hoje)
    .order('data')
    .order('inicio')
  return evs ?? []
}
