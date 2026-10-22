import type { Metadata } from 'next'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { Pagina, Voltar } from '@/components/Pagina'
import { ApagarCardsDaAula, EditorAula, EditorCard } from '@/components/admin/Editores'
import { clienteAdmin, ehAdmin } from '@/lib/admin'
import { sessao } from '@/lib/dados'

export const metadata: Metadata = { title: 'Editar aula' }

export default async function EditarAulaPage(props: PageProps<'/admin/conteudo/aula/[id]'>) {
  const { id } = await props.params
  const { email } = await sessao()
  if (!ehAdmin(email)) notFound()
  const admin = await clienteAdmin()
  const [{ data: aula }, { data: cards }, { count }] = await Promise.all([
    admin.from('aulas').select('id, materia_id, ordem, titulo, resumo, publicada').eq('id', id).maybeSingle(),
    admin.from('flashcards').select('id, frente, verso, ordem').eq('aula_id', id).order('ordem'),
    admin.from('questoes').select('id', { count: 'exact', head: true }).eq('aula_id', id).is('substituida_por', null),
  ])
  if (!aula) notFound()

  return (
    <Pagina>
      <Voltar href="/admin/conteudo" rotulo="Conteúdo" />
      <header className="top">
        <div>
          <div className="eyebrow">Editar aula</div>
          <h1 className="big">{aula.titulo}</h1>
        </div>
      </header>

      <EditorAula aula={aula} />

      <div className="sec ag-h">
        <span>Questões</span>
        <Link href={`/admin/conteudo/questoes/${aula.materia_id}?aula=${aula.id}`}>Editar as {count ?? 0} →</Link>
      </div>

      <div className="sec">Flashcards ({cards?.length ?? 0})</div>
      {cards?.length ? (
        <div className="ed-lista">
          <div className="ed-bloco">
            <p style={{ margin: 0 }}>Para refazer os flashcards desta aula, apague todos de uma vez.</p>
            <ApagarCardsDaAula aulaId={aula.id} total={cards.length} />
          </div>
          {cards.map((c: { id: string; frente: string; verso: string }, i: number) => (
            <EditorCard key={c.id} card={c} n={i + 1} />
          ))}
        </div>
      ) : (
        <p className="vazio">Esta aula ainda não tem flashcards.</p>
      )}
    </Pagina>
  )
}
