import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import { Pagina, Voltar } from '@/components/Pagina'
import { BancoQuestoes } from '@/components/BancoQuestoes'
import { carregarProgresso, paraQuestao, pendentes, sessao } from '@/lib/dados'
import { createClient } from '@/lib/supabase/server'
import { plural } from '@/lib/formato'
import { ehAdmin } from '@/lib/admin'

export async function generateMetadata(props: PageProps<'/materia/[id]/questoes'>): Promise<Metadata> {
  const { id } = await props.params
  const supabase = await createClient()
  const { data } = await supabase.from('materias').select('nome').eq('id', id).maybeSingle()
  return { title: data ? `Questões de ${data.nome}` : 'Banco de questões' }
}

export default async function BancoPage(props: PageProps<'/materia/[id]/questoes'>) {
  const { id } = await props.params
  const { tema, mostrar } = await props.searchParams
  const { supabase, userId, email } = await sessao()
  const [materia, questoes, progresso] = await Promise.all([
    supabase.from('materias').select('id, nome').eq('id', id).maybeSingle(),
    supabase.from('questoes_do_aluno').select('*').eq('materia_id', id).order('prova').order('ordem').limit(1000),
    carregarProgresso(supabase),
  ])
  if (!materia.data) notFound()
  if (questoes.error) throw new Error(`Não foi possível carregar as questões: ${questoes.error.message}`)
  const lista = (questoes.data ?? []).map(paraQuestao)
  // Filtro vindo do link (ex.: Desempenho → tema); tema que não existe nesta matéria é ignorado
  const inicial = {
    tema: typeof tema === 'string' && lista.some((q) => q.tema === tema) ? tema : null,
    situacao: mostrar === 'erradas' ? ('erradas' as const) : mostrar === 'abertas' ? ('abertas' as const) : ('todas' as const),
  }
  // Administrador: botão Editar nas questões
  const edicao = ehAdmin(email)
    ? { aulas: (await supabase.from('aulas').select('id, titulo').eq('materia_id', id).order('ordem')).data ?? [] }
    : undefined

  return (
    <Pagina pendentes={pendentes(progresso).hoje}>
      <Voltar href={`/materia/${id}`} rotulo={materia.data.nome} />
      <header className="top">
        <div>
          <div className="eyebrow">Banco de questões</div>
          <h1 className="big">{materia.data.nome}</h1>
          <p className="lead">
            {lista.length} {plural(lista.length, 'questão', 'questões')} de provas anteriores, com gabarito comentado e o porquê
            de cada alternativa errada.
          </p>
        </div>
      </header>
      {lista.length ? (
        <BancoQuestoes key={`${inicial.tema}|${inicial.situacao}`} questoes={lista} userId={userId} inicial={inicial} edicao={edicao} />
      ) : (
        <p className="vazio">Esta matéria ainda não tem questões no banco.</p>
      )}
    </Pagina>
  )
}
