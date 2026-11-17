import { BarraMaterias } from '@/components/BarraMaterias'
import { carregarMateriasPorProva } from '@/lib/materias'
import type { Metadata } from 'next'
import { retornoDaMateria, rotuloRetorno } from '@/lib/navegacao'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { Pagina, Voltar } from '@/components/Pagina'
import { Icone } from '@/components/Icones'
import { carregarProgresso, concluido, pendentes, sessao } from '@/lib/dados'
import { createClient } from '@/lib/supabase/server'
import { fonteDaQuestao } from '@/lib/classificacao-questoes'

export async function generateMetadata(props: PageProps<'/materia/[id]'>): Promise<Metadata> {
  const { id } = await props.params
  const supabase = await createClient()
  const { data } = await supabase.from('materias').select('nome').eq('id', id).maybeSingle()
  return { title: data?.nome ?? 'Matéria' }
}

export default async function MateriaPage(props: PageProps<'/materia/[id]'>) {
  const { id } = await props.params
  const { retorno } = await props.searchParams
  const origem = retornoDaMateria(retorno)
  const { supabase } = await sessao()
  const [materia, aulas, progresso, materias, diaD, questoes] = await Promise.all([
    supabase.from('materias').select('id, nome, descricao').eq('id', id).maybeSingle(),
    supabase.from('aulas').select('id, ordem, titulo, resumo, data_aula, professor').eq('materia_id', id).eq('publicada', true).order('ordem'),
    carregarProgresso(supabase),
    carregarMateriasPorProva(supabase),
    supabase.from('flashcards_dia_d').select('aula_id').like('aula_id', `${id}-a%`),
    supabase.from('questoes_do_aluno').select('aula_id, prova, fonte').eq('materia_id', id).not('aula_id', 'is', null)
      // só as que podem ser da FAG (com prova, ou material da turma); a conta exata é a do fonteDaQuestao
      .or('prova.not.is.null,fonte.ilike.*turma*,fonte.ilike.*guia de estudo*'),
  ])
  if (!materia.data) notFound()
  // Quantos flashcards Dia D cada aula tem (o botão só aparece nas aulas que têm)
  const totalDiaD = new Map<string, number>()
  for (const c of diaD.data ?? []) totalDiaD.set(c.aula_id, (totalDiaD.get(c.aula_id) ?? 0) + 1)
  // Quantas questões das Provas da FAG cada aula tem (o botão só aparece nas aulas que têm)
  const totalFag = new Map<string, number>()
  for (const q of questoes.data ?? [])
    if (q.aula_id && fonteDaQuestao(q) === 'fag') totalFag.set(q.aula_id, (totalFag.get(q.aula_id) ?? 0) + 1)

  return (
    <Pagina larga pendentes={pendentes(progresso).hoje}>
      {origem && <Voltar href={origem} rotulo={rotuloRetorno(origem)} />}
      <header className="top top-materia">
        <div>
          <div className="eyebrow">Matérias</div>
          <BarraMaterias id={id} nome={materia.data.nome} materias={materias} secao="aulas" retorno={origem} />
        </div>
      </header>

      {aulas.data?.length ? (
        <div className="materia-aulas">
          {aulas.data.map((a) => {
            const p = progresso.find((x) => x.aula_id === a.id)
            const vencidos = p ? pendentes([p]).vencidos : 0
            const retornoMateria = `/materia/${id}${origem ? `?${new URLSearchParams({ retorno: origem })}` : ''}`
            const diaDAula = totalDiaD.get(a.id) ?? 0
            const fagAula = totalFag.get(a.id) ?? 0
            const hrefAula = (aba: 'apostila' | 'questoes' | 'flashcards' | 'diad', extra: Record<string, string> = {}) =>
              `/aula/${a.id}?${new URLSearchParams({ aba, ...extra, retorno: retornoMateria })}`
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
                <nav
                  className={`materia-aula-modos${fagAula || diaDAula ? ' com-crazy' : ''}`}
                  aria-label={`Materiais da aula ${a.ordem}: ${a.titulo}`}
                >
                  {/* Estudo do dia a dia (faixa verde) e modo CRAZY, a véspera da prova (faixa vermelha): pedido do Mauricio, 17/11/2026 */}
                  <div className="materia-aula-modo diario">
                    <div className="materia-aula-faixa">
                      <span className="materia-aula-faixa-ponto" aria-hidden />
                      Estudo diário <span className="materia-aula-faixa-sub">· no ritmo das aulas</span>
                    </div>
                    <div className="materia-aula-acoes">
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
                    </div>
                  </div>
                  {(fagAula > 0 || diaDAula > 0) && (
                    <div className="materia-aula-modo crazy">
                      <div className="materia-aula-faixa">
                        <span className="materia-aula-faixa-ponto" aria-hidden />
                        Modo CRAZY <span className="materia-aula-faixa-sub">· véspera da prova</span>
                      </div>
                      <div className="materia-aula-acoes">
                        {fagAula > 0 && (
                          <Link className="materia-aula-acao" href={hrefAula('questoes', { fonte: 'fag' })}>
                            <span className="materia-aula-acao-rotulo">{Icone.arquivo}<span>Provas da FAG <span className="materia-aula-quantidade">· {fagAula}</span></span></span>
                          </Link>
                        )}
                        {diaDAula > 0 && (
                          <Link className="materia-aula-acao" href={hrefAula('diad')}>
                            <span className="materia-aula-acao-rotulo">{Icone.agenda}<span>FastCards<wbr />Genius <span className="materia-aula-quantidade">· {diaDAula}</span></span></span>
                          </Link>
                        )}
                      </div>
                    </div>
                  )}
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
