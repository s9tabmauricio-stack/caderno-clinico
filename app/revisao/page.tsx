import type { Metadata } from 'next'
import Link from 'next/link'
import { Pagina } from '@/components/Pagina'
import { Flashcards } from '@/components/Flashcards'
import { carregarMaterias, carregarProgresso, paraCard, pendentes, sessao } from '@/lib/dados'

export const metadata: Metadata = { title: 'Revisão' }

export default async function RevisaoPage(props: PageProps<'/revisao'>) {
  const { materia } = await props.searchParams
  const { supabase, userId } = await sessao()
  const agora = new Date().toISOString()

  const [progresso, materias] = await Promise.all([carregarProgresso(supabase), carregarMaterias(supabase)])
  // ?materia=<id> revisa só os cards dessa matéria; um id que não existe é ignorado
  const alvo = typeof materia === 'string' ? materias.find((m) => m.id === materia) : undefined

  // Fila do dia: todos os vencidos (do mais atrasado ao mais recente) e todos os novos, sem limite
  let consultaVencidos = supabase
    .from('flashcards_do_aluno')
    .select('*')
    .lte('proxima_revisao', agora)
    .order('proxima_revisao')
    .limit(1000)
  let consultaNovos = supabase
    .from('flashcards_do_aluno')
    .select('*')
    .is('proxima_revisao', null)
    .order('materia_ordem')
    .order('aula_ordem')
    .order('ordem')
    .limit(1000)
  if (alvo) {
    consultaVencidos = consultaVencidos.eq('materia_id', alvo.id)
    consultaNovos = consultaNovos.eq('materia_id', alvo.id)
  }
  const [vencidos, novos] = await Promise.all([consultaVencidos, consultaNovos])
  if (vencidos.error || novos.error) throw new Error('Não foi possível carregar a revisão.')

  const fila = [...(vencidos.data ?? []), ...(novos.data ?? [])].map(paraCard)
  const pend = pendentes(progresso)
  // Quantos cards estão em dia na fila mostrada (da matéria escolhida ou de todas)
  const emDiaDaFila = alvo ? pendentes(progresso.filter((p) => p.materia_id === alvo.id)).emDia : pend.emDia

  return (
    <Pagina pendentes={pend.hoje}>
      <header className="top">
        <div>
          <div className="eyebrow">{alvo ? `Flashcards de hoje · ${alvo.nome}` : 'Flashcards de hoje'}</div>
          <h1 className="big">Revisão</h1>
        </div>
      </header>
      <p className="lead" style={{ margin: '-8px 0 14px' }}>
        Errou, volta em minutos. Acertou, volta em dias. Todos os cards do dia entram, sem limite.
      </p>

      <nav className="filtro-barra revisao" aria-label="Revisar por matéria">
        <Link className="pill todas" href="/revisao" aria-current={alvo ? undefined : 'true'}>
          Todas
          {pend.hoje > 0 && <small>{pend.hoje}</small>}
        </Link>
        {materias.map((m) => {
          const t = pendentes(progresso.filter((p) => p.materia_id === m.id))
          return (
            <Link
              key={m.id}
              className="pill"
              href={`/revisao?materia=${m.id}`}
              aria-current={alvo?.id === m.id ? 'true' : undefined}
            >
              {m.nome}
              {t.hoje > 0 && <small>{t.hoje}</small>}
            </Link>
          )
        })}
      </nav>

      <Flashcards
        key={fila.map((c) => c.id).join()}
        cards={fila}
        userId={userId}
        modo="revisao"
        ativo
        emDia={emDiaDaFila}
      />
    </Pagina>
  )
}
