import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import { Pagina, Voltar } from '@/components/Pagina'
import { Flashcards } from '@/components/Flashcards'
import { AbasMateria } from '@/components/AbasMateria'
import { carregarCardsDaMateria, carregarProgresso, carregarProgressoMaterias, pendentes, sessao } from '@/lib/dados'
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
  const { supabase, userId } = await sessao()
  const [materia, cards, progresso, banco] = await Promise.all([
    supabase.from('materias').select('id, nome').eq('id', id).maybeSingle(),
    carregarCardsDaMateria(supabase, id),
    carregarProgresso(supabase),
    carregarProgressoMaterias(supabase),
  ])
  if (!materia.data) notFound()
  const totalBanco = banco.find((b) => b.materia_id === id)?.total_questoes ?? 0

  return (
    <Pagina larga pendentes={pendentes(progresso).hoje}>
      <Voltar href="/estudar" rotulo="Matérias" />
      <header className="top">
        <div>
          <div className="eyebrow">Flashcards</div>
          <h1 className="big">{materia.data.nome}</h1>
          <p className="lead">
            {cards.length} {plural(cards.length, 'flashcard', 'flashcards')} de todas as aulas da matéria. Errou, volta em minutos;
            acertou, volta em dias.
          </p>
        </div>
      </header>
      <AbasMateria id={id} ativa="flashcards" totalQuestoes={totalBanco} totalCards={cards.length} />
      <Flashcards cards={cards} userId={userId} modo="materia" ativo />
    </Pagina>
  )
}
