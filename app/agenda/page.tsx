import type { Metadata } from 'next'
import Link from 'next/link'
import { Pagina } from '@/components/Pagina'
import { AgendaSemana } from '@/components/AgendaSemana'
import { carregarProgresso, pendentes, sessao } from '@/lib/dados'
import { agendaDaSemana, grupoDoAluno } from '@/lib/agenda-dados'
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
  const [semana, grupo, progresso] = await Promise.all([
    agendaDaSemana(supabase),
    grupoDoAluno(supabase, userId),
    carregarProgresso(supabase),
  ])

  return (
    <Pagina pendentes={pendentes(progresso).hoje}>
      <header className="top">
        <div>
          <div className="eyebrow">{semana ? periodo(semana.semana) : 'Cronograma da turma'}</div>
          <h1 className="big">Agenda</h1>
        </div>
      </header>

      {semana ? (
        <AgendaSemana semana={semana.semana} aviso={semana.aviso} eventos={semana.eventos} grupo={grupo} agora={agoraBrasilia()} />
      ) : (
        <p className="vazio">O cronograma da semana ainda não foi publicado.</p>
      )}

      {grupo === null && (
        <p className="foot">
          <Link href="/perfil">Informe seu grupo de prática no Perfil</Link> para filtrar as suas práticas.
        </p>
      )}
    </Pagina>
  )
}
