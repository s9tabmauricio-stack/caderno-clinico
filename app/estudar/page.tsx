import { redirect } from 'next/navigation'
import { sessao } from '@/lib/dados'
import { carregarMateriasPorProva } from '@/lib/materias'
import { MATERIA_PADRAO } from '@/lib/navegacao'

// Entrada de Matérias: abre a primeira matéria da barra (a mais à esquerda,
// que é a da próxima prova), sem exibir a antiga lista de matérias.
export default async function EstudarPage() {
  const { supabase } = await sessao()
  const materias = await carregarMateriasPorProva(supabase)
  redirect(`/materia/${encodeURIComponent(materias[0]?.id ?? MATERIA_PADRAO)}`)
}
