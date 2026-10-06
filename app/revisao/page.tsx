import type { Metadata } from 'next'
import { Pagina } from '@/components/Pagina'
import { Flashcards } from '@/components/Flashcards'
import { carregarMaterias, carregarProgresso, paraCard, pendentes, sessao, totais } from '@/lib/dados'
import { LIMITE_NOVOS, plural } from '@/lib/formato'

export const metadata: Metadata = { title: 'Revisão' }

export default async function RevisaoPage() {
  const { supabase, userId } = await sessao()
  const agora = new Date().toISOString()

  // Fila do dia: todos os vencidos (do mais atrasado ao mais recente) e até LIMITE_NOVOS novos
  const [vencidos, novos, progresso, materias] = await Promise.all([
    supabase
      .from('flashcards_do_aluno')
      .select('*')
      .lte('proxima_revisao', agora)
      .order('proxima_revisao')
      .limit(500),
    supabase
      .from('flashcards_do_aluno')
      .select('*')
      .is('proxima_revisao', null)
      .order('materia_ordem')
      .order('aula_ordem')
      .order('ordem')
      .limit(LIMITE_NOVOS),
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
          <div className="eyebrow">Flashcards</div>
          <h1 className="big">Revisão</h1>
        </div>
      </header>
      <p className="lead" style={{ margin: '-8px 0 18px' }}>
        O card que você erra volta em minutos. O que você acerta volta em dias, e o intervalo cresce a cada acerto. Entram
        até {LIMITE_NOVOS} cards novos por sessão.
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
