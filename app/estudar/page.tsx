import type { Metadata } from 'next'
import { redirect } from 'next/navigation'
import { SeletorPeriodos } from '@/components/BarraMaterias'
import { Pagina } from '@/components/Pagina'
import { carregarProgresso, pendentes, sessao } from '@/lib/dados'
import { carregarMateriasPorProva } from '@/lib/materias'
import { rotuloPeriodo } from '@/lib/periodos'

export const metadata: Metadata = { title: 'Matérias' }

// Entrada de Matérias: abre a primeira matéria da barra (a da próxima prova) do período pedido,
// ou do período atual da turma. Período ainda sem matérias mostra só o seletor e um aviso.
export default async function EstudarPage(props: PageProps<'/estudar'>) {
  const { periodo: pedido } = await props.searchParams
  const { supabase } = await sessao()
  const { materias, periodos, atual } = await carregarMateriasPorProva(supabase)
  const numero = Number(Array.isArray(pedido) ? pedido[0] : pedido)
  const periodo = periodos.includes(numero) ? numero : atual
  const primeira = materias.find((m) => m.periodo === periodo)
  if (primeira) redirect(`/materia/${encodeURIComponent(primeira.id)}`)

  const progresso = await carregarProgresso(supabase)
  const anteriores = periodos.filter((p) => periodo !== null && p < periodo)
  return (
    <Pagina larga pendentes={pendentes(progresso).hoje}>
      <header className="top top-materia">
        <div>
          <div className="eyebrow">Matérias</div>
          <h1 className="materia-titulo-acessivel">{periodo ? rotuloPeriodo(periodo) : 'Matérias'}</h1>
          <SeletorPeriodos periodos={periodos} ativo={periodo} />
        </div>
      </header>
      <p className="vazio">
        {periodo ? `O ${rotuloPeriodo(periodo)} ainda não tem matérias. Elas aparecem aqui assim que a primeira aula for publicada.` : 'Ainda não há matérias.'}
        {anteriores.length > 0 && ` As do ${rotuloPeriodo(anteriores[0])} continuam no seletor acima.`}
      </p>
    </Pagina>
  )
}
