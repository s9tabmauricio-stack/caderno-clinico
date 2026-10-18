import type { Metadata } from 'next'
import { Pagina } from '@/components/Pagina'
import { Flashcards } from '@/components/Flashcards'
import { carregarMaterias, carregarProgresso, paraCard, pendentes, sessao, totais } from '@/lib/dados'
import { plural } from '@/lib/formato'

export const metadata: Metadata = { title: 'Revisão' }

export default async function RevisaoPage() {
  const { supabase, userId } = await sessao()
  const agora = new Date().toISOString()

  // Fila do dia: todos os vencidos (do mais atrasado ao mais recente) e todos os novos, sem limite
  const [vencidos, novos, progresso, materias] = await Promise.all([
    supabase
      .from('flashcards_do_aluno')
      .select('*')
      .lte('proxima_revisao', agora)
      .order('proxima_revisao')
      .limit(1000),
    supabase
      .from('flashcards_do_aluno')
      .select('*')
      .is('proxima_revisao', null)
      .order('materia_ordem')
      .order('aula_ordem')
      .order('ordem')
      .limit(1000),
    carregarProgresso(supabase),
    carregarMaterias(supabase),
  ])
  if (vencidos.error || novos.error) throw new Error('Não foi possível carregar a revisão.')

  const fila = [...(vencidos.data ?? []), ...(novos.data ?? [])].map(paraCard)
  const pend = pendentes(progresso)

  return (
    <Pagina pendentes={pend.hoje}>
      <header className="top">
        <div>
          <div className="eyebrow">Flashcards de hoje</div>
          <h1 className="big">Revisão</h1>
        </div>
      </header>
      <p className="lead" style={{ margin: '-8px 0 18px' }}>
        Errou, volta em minutos. Acertou, volta em dias. Todos os cards do dia entram, sem limite.
      </p>

      <Flashcards key={fila.map((c) => c.id).join()} cards={fila} userId={userId} modo="revisao" ativo emDia={pend.emDia} />

      <div className="sec">Por matéria</div>
      <div className="group">
        {materias.map((m) => {
          const t = totais(progresso.filter((p) => p.materia_id === m.id))
          const novosM = t.cards - t.estudados
          const emDia = t.estudados - t.vencidos
          return (
            <div key={m.id} className="row static">
              <span className="main">
                <span className="t">{m.nome}</span>
                <span className="s">
                  {t.vencidos} para revisar · {novosM} {plural(novosM, 'novo', 'novos')} · {emDia} em dia
                </span>
              </span>
            </div>
          )
        })}
      </div>
    </Pagina>
  )
}
