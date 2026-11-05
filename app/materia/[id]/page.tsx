import type { Metadata } from 'next'
import { retornoSeguro, rotuloRetorno } from '@/lib/navegacao'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { Pagina, Voltar } from '@/components/Pagina'
import { Icone } from '@/components/Icones'
import { AbasMateria } from '@/components/AbasMateria'
import { carregarProgresso, carregarProgressoMaterias, concluido, pendentes, sessao, totais } from '@/lib/dados'
import { createClient } from '@/lib/supabase/server'

export async function generateMetadata(props: PageProps<'/materia/[id]'>): Promise<Metadata> {
  const { id } = await props.params
  const supabase = await createClient()
  const { data } = await supabase.from('materias').select('nome').eq('id', id).maybeSingle()
  return { title: data?.nome ?? 'Matéria' }
}

export default async function MateriaPage(props: PageProps<'/materia/[id]'>) {
  const { id } = await props.params
  const { retorno } = await props.searchParams
  const origem = retornoSeguro(retorno)
  const { supabase } = await sessao()
  const [materia, aulas, progresso, banco] = await Promise.all([
    supabase.from('materias').select('id, nome, descricao').eq('id', id).maybeSingle(),
    supabase.from('aulas').select('id, ordem, titulo, resumo, data_aula, professor').eq('materia_id', id).eq('publicada', true).order('ordem'),
    carregarProgresso(supabase),
    carregarProgressoMaterias(supabase),
  ])
  if (!materia.data) notFound()
  const pm = banco.find((b) => b.materia_id === id)
  const totalCards = totais(progresso.filter((p) => p.materia_id === id)).cards

  return (
    <Pagina larga pendentes={pendentes(progresso).hoje}>
      <Voltar href={origem ?? "/estudar"} rotulo={origem ? rotuloRetorno(origem) : "Matérias"} />
      <header className="top">
        <div>
          <div className="eyebrow">Matéria</div>
          <h1 className="big">{materia.data.nome}</h1>
          {materia.data.descricao && <p className="lead">{materia.data.descricao}</p>}
        </div>
      </header>

      <AbasMateria id={id} ativa="aulas" totalQuestoes={pm?.total_questoes ?? 0} totalCards={totalCards} />

      {aulas.data?.length ? (
        <div className="group">
          {aulas.data.map((a) => {
            const p = progresso.find((x) => x.aula_id === a.id)
            const vencidos = p ? pendentes([p]).vencidos : 0
            const retornoMateria = `/materia/${id}${origem ? `?${new URLSearchParams({ retorno: origem })}` : ''}`
            const hrefAula = (aba: 'apostila' | 'questoes' | 'flashcards') =>
              `/aula/${a.id}?${new URLSearchParams({ aba, retorno: retornoMateria })}`
            return (
              <article key={a.id} className="materia-aula">
                <Link className="row materia-aula-topo" href={hrefAula('apostila')}>
                  <span className="materia-aula-numero">
                    <span className="num">{a.ordem}</span>
                    {a.data_aula && (
                      <time className="materia-aula-data" dateTime={a.data_aula}>
                        {a.data_aula.slice(5).split('-').reverse().join('/')}
                      </time>
                    )}
                  </span>
                  <span className="main">
                    {a.professor && <span className="materia-aula-professor">{a.professor}</span>}
                    <span className="t">{a.titulo}</span>
                    {a.resumo && <span className="s">{a.resumo}</span>}
                  </span>
                  <span className="pct">{p ? concluido([p]) : 0}%</span>
                  {Icone.seta}
                </Link>
                <nav className="materia-aula-acoes" aria-label={`Materiais da aula ${a.ordem}: ${a.titulo}`}>
                  <Link className="materia-aula-acao" href={hrefAula('apostila')}>
                    <span className="materia-aula-acao-rotulo">{Icone.estudar}<span>Apostila</span></span>
                  </Link>
                  <Link className="materia-aula-acao" href={hrefAula('questoes')}>
                    <span className="materia-aula-acao-rotulo">{Icone.questoes}<span>Questões <span className="materia-aula-quantidade">· {p?.total_questoes ?? 0}</span></span></span>
                  </Link>
                  <Link className="materia-aula-acao" href={hrefAula('flashcards')}>
                    <span className="materia-aula-acao-rotulo">{Icone.cards}<span>Flashcards <span className="materia-aula-quantidade">· {p?.total_cards ?? 0}</span></span></span>
                    {vencidos > 0 && <span className="chip revisar">{vencidos} para revisar</span>}
                  </Link>
                </nav>
              </article>
            )
          })}
        </div>
      ) : (
        <p className="vazio">As aulas desta matéria aparecem aqui assim que forem publicadas.</p>
      )}
    </Pagina>
  )
}
