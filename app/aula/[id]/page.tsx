import type { Metadata } from 'next'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { Pagina, Voltar } from '@/components/Pagina'
import { AulaAbas, type Aba } from '@/components/AulaAbas'
import { carregarProgresso, carregarProgressoMaterias, paraCard, paraQuestao, pendentes, sessao } from '@/lib/dados'
import { createClient } from '@/lib/supabase/server'
import { retornoSeguro, rotuloRetorno } from '@/lib/navegacao'
import { ehAdmin } from '@/lib/admin'

const dataCurta = (d: string) => d.split('-').reverse().join('/')

export async function generateMetadata(props: PageProps<'/aula/[id]'>): Promise<Metadata> {
  const { id } = await props.params
  const supabase = await createClient()
  const { data } = await supabase.from('aulas').select('titulo').eq('id', id).maybeSingle()
  return { title: data?.titulo ?? 'Aula' }
}

export default async function AulaPage(props: PageProps<'/aula/[id]'>) {
  const { id } = await props.params
  const { aba, retorno } = await props.searchParams
  const origem = retornoSeguro(retorno)
  const abaInicial: Aba = aba === 'questoes' || aba === 'flashcards' ? aba : 'apostila'

  const { supabase, userId, email } = await sessao()
  const [aula, questoes, cards, progresso, banco] = await Promise.all([
    supabase
      .from('aulas')
      .select('id, materia_id, ordem, titulo, data_aula, professor, apostila_html, pdf_caminho, materias(nome)')
      .eq('id', id)
      .eq('publicada', true)
      .maybeSingle(),
    supabase.from('questoes_do_aluno').select('*').eq('aula_id', id).order('ordem'),
    supabase.from('flashcards_do_aluno').select('*').eq('aula_id', id).order('ordem'),
    carregarProgresso(supabase),
    carregarProgressoMaterias(supabase),
  ])
  if (!aula.data) notFound()
  if (questoes.error) throw new Error(`Não foi possível carregar as questões: ${questoes.error.message}`)
  if (cards.error) throw new Error(`Não foi possível carregar os flashcards: ${cards.error.message}`)

  // Link temporário (1 hora) para o PDF da apostila, se já tiver sido enviado
  let pdfUrl: string | null = null
  if (aula.data.pdf_caminho) {
    const { data } = await supabase.storage.from('apostilas').createSignedUrl(aula.data.pdf_caminho, 3600)
    pdfUrl = data?.signedUrl ?? null
  }

  const materiaNome = aula.data.materias?.nome ?? 'Matéria'
  const materiaId = aula.data.materia_id
  const totalBanco = banco.find((b) => b.materia_id === materiaId)?.total_questoes ?? 0
  // Próxima aula publicada da matéria (para o "próximo passo" no fim das questões e dos cards)
  // e, só para o administrador, as aulas da matéria (seletor do botão Editar nas questões)
  const [proxima, aulasDaMateria] = await Promise.all([
    supabase
      .from('aulas')
      .select('id, titulo')
      .eq('materia_id', materiaId)
      .eq('publicada', true)
      .gt('ordem', aula.data.ordem)
      .order('ordem')
      .limit(1)
      .maybeSingle(),
    ehAdmin(email) ? supabase.from('aulas').select('id, titulo').eq('materia_id', materiaId).order('ordem') : null,
  ])
  const edicao = aulasDaMateria ? { aulas: aulasDaMateria.data ?? [] } : undefined

  return (
    <Pagina larga pendentes={pendentes(progresso).hoje}>
      <Voltar href={origem ?? `/materia/${aula.data.materia_id}`} rotulo={origem ? rotuloRetorno(origem) : materiaNome} />
      <header className="top">
        <div>
          <div className="eyebrow">
            <Link href={`/materia/${materiaId}`}>{materiaNome}</Link> · Aula {aula.data.ordem}
            {aula.data.data_aula && ` · ${dataCurta(aula.data.data_aula)}`}
            {aula.data.professor && ` · ${aula.data.professor}`}
          </div>
          <h1 className="big">{aula.data.titulo}</h1>
        </div>
      </header>
      <AulaAbas
        aulaId={id}
        abaInicial={abaInicial}
        apostilaHtml={aula.data.apostila_html}
        pdfUrl={pdfUrl}
        questoes={(questoes.data ?? []).map(paraQuestao)}
        cards={(cards.data ?? []).map(paraCard)}
        userId={userId}
        materiaId={materiaId}
        totalBanco={totalBanco}
        proximaAula={proxima.data}
        edicao={edicao}
      />
    </Pagina>
  )
}
