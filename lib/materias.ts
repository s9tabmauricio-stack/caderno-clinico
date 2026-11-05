import { agoraBrasilia } from '@/lib/agenda'
import { proximasProvas } from '@/lib/agenda-dados'
import { carregarMaterias } from '@/lib/dados'
import { ordenarMateriasPorProva } from '@/lib/ordem-materias'
import type { SupabaseServidor } from '@/lib/supabase/server'

export async function carregarMateriasPorProva(supabase: SupabaseServidor) {
  const agora = agoraBrasilia()
  const [materias, provas] = await Promise.all([
    carregarMaterias(supabase),
    proximasProvas(supabase),
  ])
  return ordenarMateriasPorProva(materias, provas, agora.ms)
}
