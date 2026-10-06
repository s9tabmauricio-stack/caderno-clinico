import type { Metadata } from 'next'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { Pagina, Voltar } from '@/components/Pagina'
import { Icone } from '@/components/Icones'
import { carregarProgresso, concluido, pendentes, sessao } from '@/lib/dados'
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
  const [materia, aulas, progresso] = await Promise.all([
    supabase.from('materias').select('id, nome, descricao').eq('id', id).maybeSingle(),
    supabase.from('aulas').select('id, ordem, titulo, resumo').eq('materia_id', id).eq('publicada', true).order('ordem'),
    carregarProgresso(supabase),
  ])
  if (!materia.data) notFound()

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
