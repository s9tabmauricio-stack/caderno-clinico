'use server'

import { revalidatePath } from 'next/cache'
import { clienteAdmin } from '@/lib/admin'
import { lerCronograma } from '@/lib/agenda'

export type ResultadoAgenda = { ok: boolean; texto: string; dias?: { data: string; aulas: number; avisos: number }[] } | null

export async function publicarAgenda(_: ResultadoAgenda, form: FormData): Promise<ResultadoAgenda> {
  const texto = String(form.get('texto') ?? '').trim()
  if (!texto) return { ok: false, texto: 'Cole o texto do cronograma.' }
  const s = lerCronograma(texto)
  const aulas = s.eventos.filter((e) => e.tipo !== 'aviso' && !e.cancelado)
  if (!s.dias.length || !aulas.length) {
    return { ok: false, texto: 'Não encontrei dias nem horários. Confira se o texto tem linhas como "SEGUNDA-FEIRA | 5/outubro" e "8h-10h: aula ...".' }
  }
  try {
    const admin = await clienteAdmin()
    const r1 = await admin
      .from('agenda_semanas')
      .upsert({ semana: s.semana, titulo: s.titulo, aviso: s.aviso, texto, atualizado_em: new Date().toISOString() })
    if (r1.error) return { ok: false, texto: `Não deu para salvar: ${r1.error.message}` }
    // A semana publicada substitui a versão anterior da mesma semana (as provas incluídas à parte ficam)
    const r2 = await admin.from('agenda_eventos').delete().eq('semana', s.semana).eq('fixo', false)
    if (r2.error) return { ok: false, texto: `Não deu para atualizar: ${r2.error.message}` }
    const r3 = await admin.from('agenda_eventos').insert(s.eventos.map((e) => ({ ...e, semana: s.semana })))
    if (r3.error) return { ok: false, texto: `Não deu para salvar as aulas: ${r3.error.message}` }
  } catch (e) {
    return { ok: false, texto: (e as Error).message }
  }
  revalidatePath('/')
  revalidatePath('/agenda')
  revalidatePath('/admin/agenda')
  return {
    ok: true,
    texto: `Semana publicada: ${aulas.length} aulas, ${s.eventos.filter((e) => e.cancelado).length} cancelamentos e ${s.eventos.filter((e) => e.tipo === 'aviso').length} avisos.`,
    dias: s.dias.map((d) => ({
      data: d,
      aulas: s.eventos.filter((e) => e.data === d && e.tipo !== 'aviso' && !e.cancelado).length,
      avisos: s.eventos.filter((e) => e.data === d && (e.tipo === 'aviso' || e.cancelado)).length,
    })),
  }
}
