import type { Metadata } from 'next'
import { cookies } from 'next/headers'
import { notFound } from 'next/navigation'
import { Pagina, Voltar } from '@/components/Pagina'
import { BancoQuestoes } from '@/components/BancoQuestoes'
import { AbasMateria } from '@/components/AbasMateria'
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
  const { tema, mostrar, de } = await props.searchParams
  const { supabase, userId, email } = await sessao()
  const [materia, questoes, progresso] = await Promise.all([
    supabase.from('materias').select('id, nome').eq('id', id).maybeSingle(),
    supabase.from('questoes_do_aluno').select('*').eq('materia_id', id).order('prova').order('ordem').limit(1000),
    carregarProgresso(supabase),
  ])
  if (!materia.data) notFound()
  if (questoes.error) throw new Error(`Não foi possível carregar as questões: ${questoes.error.message}`)
  const lista = (questoes.data ?? []).map(paraQuestao)
  // Filtros: um link com filtro (ex.: Desempenho → tema) vale sozinho; sem ele, abre com o último tema e prova deste aluno
  const comFiltroNoLink = typeof tema === 'string' || typeof mostrar === 'string'
  let lembrados: { tema?: unknown; prova?: unknown } = {}
  try {
    if (!comFiltroNoLink) lembrados = JSON.parse(decodeURIComponent((await cookies()).get(`mgf_${id}`)?.value ?? '{}')) ?? {}
  } catch {}
  const existe = (campo: 'tema' | 'prova', v: unknown) => (typeof v === 'string' && lista.some((q) => q[campo] === v) ? v : null)
  const inicial = {
    tema: existe('tema', tema) ?? existe('tema', lembrados.tema),
    prova: existe('prova', lembrados.prova),
    situacao: mostrar === 'erradas' ? ('erradas' as const) : mostrar === 'abertas' ? ('abertas' as const) : ('todas' as const),
  }

  // "Voltar" leva de volta a quem mandou o aluno para cá (Matérias, Desempenho ou a aula)
  let voltar = { href: '/estudar', rotulo: 'Matérias' }
  if (de === 'desempenho') voltar = { href: '/desempenho', rotulo: 'Desempenho' }
  else if (typeof de === 'string' && /^aula:[\w-]{1,60}$/.test(de)) {
    const aulaId = de.slice(5)
    const { data: aula } = await supabase.from('aulas').select('titulo').eq('id', aulaId).eq('materia_id', id).maybeSingle()
    if (aula) voltar = { href: `/aula/${aulaId}?aba=questoes`, rotulo: aula.titulo }
  }
  // Administrador: botão Editar nas questões
  const edicao = ehAdmin(email)
    ? { aulas: (await supabase.from('aulas').select('id, titulo').eq('materia_id', id).order('ordem')).data ?? [] }
    : undefined

  return (
    <Pagina larga pendentes={pendentes(progresso).hoje}>
      <Voltar href={voltar.href} rotulo={voltar.rotulo} />
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
      {lista.length > 0 && <AbasMateria id={id} ativa="banco" totalQuestoes={lista.length} />}
      {lista.length ? (
        <BancoQuestoes
          key={`${inicial.tema}|${inicial.prova}|${inicial.situacao}`}
          chave={id}
          questoes={lista}
          userId={userId}
          inicial={inicial}
          edicao={edicao}
        />
      ) : (
        <p className="vazio">Esta matéria ainda não tem questões no banco.</p>
      )}
    </Pagina>
  )
}
