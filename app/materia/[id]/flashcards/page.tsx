import { BarraMaterias } from '@/components/BarraMaterias'
import { carregarMateriasPorProva } from '@/lib/materias'
import type { Metadata } from 'next'
import { retornoDaMateria, rotuloRetorno } from '@/lib/navegacao'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { Pagina, Voltar } from '@/components/Pagina'
import { Flashcards } from '@/components/Flashcards'
import { carregarCardsDaMateria, carregarProgresso, pendentes, sessao } from '@/lib/dados'
import { createClient } from '@/lib/supabase/server'
import { plural } from '@/lib/formato'

export async function generateMetadata(props: PageProps<'/materia/[id]/flashcards'>): Promise<Metadata> {
  const { id } = await props.params
  const supabase = await createClient()
  const { data } = await supabase.from('materias').select('nome').eq('id', id).maybeSingle()
  return { title: data ? `Flashcards de ${data.nome}` : 'Flashcards' }
}

export default async function FlashcardsMateriaPage(props: PageProps<'/materia/[id]/flashcards'>) {
  const { id } = await props.params
  const { retorno } = await props.searchParams
  const origem = retornoDaMateria(retorno)
  const { supabase, userId } = await sessao()
  const [materia, cards, progresso, materias] = await Promise.all([
    supabase.from('materias').select('id, nome').eq('id', id).maybeSingle(),
    carregarCardsDaMateria(supabase, id),
    carregarProgresso(supabase),
    carregarMateriasPorProva(supabase),
  ])
  if (!materia.data) notFound()

  return (
    <Pagina larga pendentes={pendentes(progresso).hoje}>
      {origem && <Voltar href={origem} rotulo={rotuloRetorno(origem)} />}
      <header className="top top-materia">
        <div>
          <div className="eyebrow">Flashcards</div>
          <BarraMaterias id={id} nome={materia.data.nome} materias={materias} secao="flashcards" retorno={origem} />
          <p className="lead">
            {cards.length} {plural(cards.length, 'flashcard', 'flashcards')} de todas as aulas da matéria para consultar e estudar livremente. As avaliações também atualizam sua próxima revisão.
          </p>
        </div>
      </header>
      <p className="foot">Para fazer apenas a fila de hoje, <Link href={`/revisao?materia=${id}`}>abrir Revisão desta matéria</Link>.</p>
      <Flashcards cards={cards} userId={userId} modo="materia" ativo />
    </Pagina>
  )
}
