import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import { Pagina, Voltar } from '@/components/Pagina'
import { EditorQuestao, type QuestaoAdmin } from '@/components/admin/Editores'
import { clienteAdmin, ehAdmin } from '@/lib/admin'
import { sessao } from '@/lib/dados'

export const metadata: Metadata = { title: 'Editar questões' }

export default async function EditarQuestoesPage(props: PageProps<'/admin/conteudo/questoes/[materia]'>) {
  const { materia } = await props.params
  const { aula } = await props.searchParams
  const { email } = await sessao()
  if (!ehAdmin(email)) notFound()
  const admin = await clienteAdmin()
  let consulta = admin
    .from('questoes')
    .select('id, aula_id, ordem, enunciado, alternativas, correta, comentario, por_que_erradas, tema, prova, fonte')
    .eq('materia_id', materia)
    .is('substituida_por', null)
    .order('ordem')
  if (typeof aula === 'string') consulta = consulta.eq('aula_id', aula)
  const [{ data: mat }, { data: aulas }, { data: questoes }] = await Promise.all([
    admin.from('materias').select('nome').eq('id', materia).maybeSingle(),
    admin.from('aulas').select('id, titulo').eq('materia_id', materia).order('ordem'),
    consulta,
  ])
  if (!mat) notFound()
  const lista = (questoes ?? []) as (QuestaoAdmin & { ordem: number })[]

  return (
    <Pagina pendentes={0}>
      <Voltar href="/admin/conteudo" rotulo="Conteúdo" />
      <header className="top">
        <div>
          <div className="eyebrow">{typeof aula === 'string' ? 'Questões da aula' : 'Banco de questões'}</div>
          <h1 className="big">{mat.nome}</h1>
        </div>
      </header>
      {lista.length ? (
        <div className="ed-lista">
          {lista.map((q, i) => (
            <details key={q.id} className="ed-q">
              <summary>
                <span className="num">{i + 1}</span>
                <span className="main">
                  <span className="t">{q.enunciado.slice(0, 110)}{q.enunciado.length > 110 ? '…' : ''}</span>
                  <span className="s">{[q.fonte, q.tema].filter(Boolean).join(' · ') || q.id}</span>
                </span>
              </summary>
              <EditorQuestao q={q} aulas={aulas ?? []} />
            </details>
          ))}
        </div>
      ) : (
        <p className="vazio">Nenhuma questão aqui ainda.</p>
      )}
    </Pagina>
  )
}
