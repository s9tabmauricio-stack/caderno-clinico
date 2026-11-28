// Períodos do curso (28/11/2026): cada matéria é de um período (materias.periodo) e cada turma tem um
// período atual (turmas.periodo_atual). A aba Matérias abre no período atual; os anteriores ficam no seletor.
import type { SupabaseServidor } from '@/lib/supabase/server'

/** Períodos atuais de quem vê: o da própria turma; sem turma (administrador), os de todas. Sem perfil = T29. */
export async function periodosAtuais(supabase: SupabaseServidor): Promise<number[]> {
  const [{ data: perfil }, { data: turmas }] = await Promise.all([
    supabase.from('perfis').select('turma').maybeSingle(),
    supabase.from('turmas').select('id, periodo_atual'),
  ])
  const lista = turmas ?? []
  const turma = perfil ? perfil.turma : 't29'
  const atuais = (turma ? lista.filter((t) => t.id === turma) : lista).map((t) => t.periodo_atual)
  return [...new Set(atuais)].sort((a, b) => b - a)
}

/** Dá a cada matéria o seu período (vazio = o período atual mais alto) e lista os períodos, do mais novo ao mais antigo. */
export function organizarPeriodos<T extends { periodo?: number | null }>(materias: T[], atuais: number[]) {
  const atual = atuais.length ? Math.max(...atuais) : null
  const comPeriodo = materias.map((m) => ({ ...m, periodo: m.periodo ?? atual }))
  const periodos = [...new Set([...atuais, ...comPeriodo.map((m) => m.periodo)])]
    .filter((p): p is number => typeof p === 'number')
    .sort((a, b) => b - a)
  return { materias: comPeriodo, periodos, atual: atual ?? periodos[0] ?? null }
}

export function rotuloPeriodo(p: number) {
  return `${p}º período`
}

/** Matéria do app para uma aula da agenda: a da turma daquela agenda cuja chave (chave_agenda, ou o id) é a da agenda.
 *  Com duas, a de período mais alto. Sem nenhuma, fica a chave da agenda (a aula aparece sem link). */
export function materiaDaTurma(
  chave: string | null,
  turma: string,
  materias: { id: string; chave_agenda: string | null; turmas: string[]; periodo: number | null }[],
) {
  if (!chave) return chave
  const candidatas = materias
    .filter((m) => (m.chave_agenda ?? m.id) === chave && m.turmas.includes(turma))
    .sort((a, b) => (b.periodo ?? 0) - (a.periodo ?? 0))
  return candidatas[0]?.id ?? chave
}
