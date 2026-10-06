import type { Metadata } from 'next'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { Pagina, Voltar } from '@/components/Pagina'
import { Icone } from '@/components/Icones'
import { carregarProgresso, carregarProgressoMaterias, carregarTemas, concluido, pendentes, sessao } from '@/lib/dados'
import { plural } from '@/lib/formato'
import { createClient } from '@/lib/supabase/server'

export async function generateMetadata(props: PageProps<'/materia/[id]'>): Promise<Metadata> {
  const { id } = await props.params
  const supabase = await createClient()
  const { data } = await supabase.from('materias').select('nome').eq('id', id).maybeSingle()
  return { title: data?.nome ?? 'Matéria' }
}

export default async function MateriaPage(props: PageProps<'/materia/[id]'>) {
  const { id } = await props.params
  const { supabase } = await sessao()
  const [materia, aulas, progresso, banco, temas] = await Promise.all([
    supabase.from('materias').select('id, nome, descricao').eq('id', id).maybeSingle(),
    supabase.from('aulas').select('id, ordem, titulo, resumo').eq('materia_id', id).eq('publicada', true).order('ordem'),
    carregarProgresso(supabase),
    carregarProgressoMaterias(supabase),
    carregarTemas(supabase),
  ])
  if (!materia.data) notFound()
  const pm = banco.find((b) => b.materia_id === id)
  const nTemas = temas.filter((t) => t.materia_id === id).length

  return (
    <Pagina pendentes={pendentes(progresso).hoje}>
      <Voltar href="/" rotulo="Início" />
      <header className="top">
        <div>
          <div className="eyebrow">Matéria</div>
          <h1 className="big">{materia.data.nome}</h1>
          {materia.data.descricao && <p className="lead">{materia.data.descricao}</p>}
        </div>
      </header>

      {pm && pm.total_questoes > 0 && (
        <>
          <div className="sec">Banco de questões</div>
          <div className="group">
            <Link className="row banco-row" href={`/materia/${id}/questoes`}>
              <span className="num">{Icone.certo}</span>
              <span className="main">
                <span className="t">
                  {pm.total_questoes} {plural(pm.total_questoes, 'questão', 'questões')} de provas anteriores
                </span>
                <span className="s">
                  {nTemas} {plural(nTemas, 'tema', 'temas')} · {pm.respondidas} {plural(pm.respondidas, 'respondida', 'respondidas')}
                  {pm.respondidas > 0 && ` · ${Math.round((100 * pm.acertos) / pm.respondidas)}% de acerto`}
                </span>
              </span>
              {Icone.seta}
            </Link>
          </div>
        </>
      )}

      <div className="sec">Aulas</div>
      {aulas.data?.length ? (
        <div className="group">
          {aulas.data.map((a) => {
            const p = progresso.find((x) => x.aula_id === a.id)
            return (
              <Link key={a.id} className="row" href={`/aula/${a.id}`}>
                <span className="num">{a.ordem}</span>
                <span className="main">
                  <span className="t">{a.titulo}</span>
                  {a.resumo && <span className="s">{a.resumo}</span>}
                  <span className="meta">
                    Apostila · {p?.total_questoes ?? 0} questões · {p?.total_cards ?? 0} flashcards
                    {p && p.cards_vencidos > 0 && <span className="chip revisar">{p.cards_vencidos} para revisar</span>}
                  </span>
                </span>
                <span className="pct">{p ? concluido([p]) : 0}%</span>
                {Icone.seta}
              </Link>
            )
          })}
        </div>
      ) : (
        <p className="vazio">As aulas desta matéria aparecem aqui assim que forem publicadas.</p>
      )}
    </Pagina>
  )
}
