import type { Metadata } from 'next'
import { Pagina } from '@/components/Pagina'
import { AgendaSemana } from '@/components/AgendaSemana'
import { AgendaProvas } from '@/components/AgendaLista'
import { carregarMaterias, carregarProgresso, pendentes, sessao } from '@/lib/dados'
import { agendaDaSemana, grupoDoAluno, proximasProvas } from '@/lib/agenda-dados'
import { agoraBrasilia } from '@/lib/agenda'

export const metadata: Metadata = { title: 'Agenda' }

function periodo(semana: string) {
  const ini = new Date(`${semana}T12:00:00Z`)
  const fim = new Date(ini)
  fim.setUTCDate(fim.getUTCDate() + 4)
  const f = (d: Date, mes: boolean) =>
    new Intl.DateTimeFormat('pt-BR', { day: 'numeric', ...(mes ? { month: 'long' } : {}), timeZone: 'UTC' }).format(d)
  return ini.getUTCMonth() === fim.getUTCMonth() ? `${f(ini, false)} a ${f(fim, true)}` : `${f(ini, true)} a ${f(fim, true)}`
}

export default async function AgendaPage() {
  const { supabase, userId } = await sessao()
  const [semana, grupo, progresso, materias, provas] = await Promise.all([
    agendaDaSemana(supabase),
    grupoDoAluno(supabase, userId),
    carregarProgresso(supabase),
    carregarMaterias(supabase),
    proximasProvas(supabase),
  ])
  const agora = agoraBrasilia()
  const idsMaterias = materias.map((m) => m.id)

  return (
    <Pagina pendentes={pendentes(progresso).hoje}>
      <header className="top">
        <div>
          <div className="eyebrow">{semana ? periodo(semana.semana) : 'Cronograma da turma'}</div>
          <h1 className="big">Agenda</h1>
        </div>
      </header>

      {semana ? (
        <AgendaSemana
          semana={semana.semana}
          aviso={semana.aviso}
          eventos={semana.eventos}
          grupo={grupo}
          agora={agora}
          userId={userId}
          materias={idsMaterias}
        />
      ) : (
        <p className="vazio">O cronograma da semana ainda não foi publicado.</p>
      )}

      {provas.length > 0 && (
        <>
          <div className="sec" id="provas">
            Próximas provas
          </div>
          <AgendaProvas eventos={provas} hoje={agora.data} materias={idsMaterias} />
        </>
      )}
    </Pagina>
  )
}
