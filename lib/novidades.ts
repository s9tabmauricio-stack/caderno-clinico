// Novidades do app, mostradas no sininho ao lado da engrenagem (components/Novidades.tsx).
// Ficam na tabela `novidades`; o administrador escreve e apaga em Administração → Novidades (/admin/novidades).
// Quem ainda não viu o `id` de uma novidade vê a bolinha piscando até abrir o painel (guardado no aparelho).
import type { SupabaseClient } from '@supabase/supabase-js'

export type Novidade = { id: string; titulo: string; texto: string; criado_em: string }

export const CHAVE_NOVIDADES = 'mg-novidades-vistas'

/** As mais recentes primeiro (o painel mostra só as 15 últimas). */
export async function lerNovidades(supabase: SupabaseClient, limite = 15): Promise<Novidade[]> {
  const { data } = await supabase.from('novidades').select('id, titulo, texto, criado_em').order('criado_em', { ascending: false }).limit(limite)
  return data ?? []
}

/** Data e hora de Brasília: "17/11/2026 · 10:33". */
export const dataNovidade = (iso: string) => {
  const d = new Date(iso)
  const dia = new Intl.DateTimeFormat('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', timeZone: 'America/Sao_Paulo' }).format(d)
  const hora = new Intl.DateTimeFormat('pt-BR', { hour: '2-digit', minute: '2-digit', timeZone: 'America/Sao_Paulo' }).format(d)
  return `${dia} · ${hora}`
}
