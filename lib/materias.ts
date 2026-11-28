import { agoraBrasilia } from '@/lib/agenda'
import { proximasProvas } from '@/lib/agenda-dados'
import { carregarMaterias } from '@/lib/dados'
import { ordenarMateriasPorProva } from '@/lib/ordem-materias'
import { organizarPeriodos, periodosAtuais } from '@/lib/periodos'
import type { SupabaseServidor } from '@/lib/supabase/server'

/** Matérias da turma pela ordem da próxima prova, cada uma com o seu período, e a lista de períodos. */
export async function carregarMateriasPorProva(supabase: SupabaseServidor) {
  const agora = agoraBrasilia()
  const [materias, provas, atuais] = await Promise.all([
    carregarMaterias(supabase),
    proximasProvas(supabase),
    periodosAtuais(supabase),
  ])
  return organizarPeriodos(ordenarMateriasPorProva(materias, provas, agora.ms), atuais)
}
