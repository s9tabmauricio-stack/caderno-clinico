import type { Metadata } from 'next'
import Link from 'next/link'
import { Pagina } from '@/components/Pagina'
import {
  carregarMaterias,
  carregarProgresso,
  pendentes,
  sessao,
} from '@/lib/dados'
import { saudacao } from '@/lib/formato'
import { agoraBrasilia, COR_MATERIA, ehDiaTodo, ehDoAluno, fmtHora, inicioMs, situacoes } from '@/lib/agenda'
import { agendaDoDia, proximasProvas } from '@/lib/agenda-dados'
import { AgendaAvisos, AgendaDiaTodo, AgendaLista, AgendaProvas } from '@/components/AgendaLista'
import { ContagemProva } from '@/components/ContagemProva'

export const metadata: Metadata = { title: { absolute: 'Med Genius · Início' } }

// Dia seguinte (AAAA-MM-DD), para mostrar a primeira aula de amanhã no pé da agenda
function amanha(data: string) {
  const d = new Date(`${data}T12:00:00Z`)
  d.setUTCDate(d.getUTCDate() + 1)
  return d.toISOString().slice(0, 10)
}

// Início: agenda do dia inteira e próximas provas
export default async function Inicio() {
  const { supabase, userId, email } = await sessao()
  const agora = agoraBrasilia()
  const [perfil, materias, progresso, agendaHoje, agendaAmanha, todasProvas] = await Promise.all([
    supabase.from('perfis').select('nome, grupo').eq('id', userId).maybeSingle(),
    carregarMaterias(supabase),
    carregarProgresso(supabase),
    agendaDoDia(supabase, agora.data),
    agendaDoDia(supabase, amanha(agora.data)),
    proximasProvas(supabase),
  ])

  // Agenda de hoje (o dia inteiro, as que já passaram ficam apagadas): teóricas e avisos para todos, práticas só do grupo do aluno
  const grupo = perfil.data?.grupo ?? null
  const ehAula = (e: (typeof agendaHoje)[number]) =>
    !e.cancelado && e.tipo !== 'aviso' && !ehDiaTodo(e) && ehDoAluno(e.grupos, grupo)
  const diaTodo = agendaHoje.filter(ehDiaTodo)
  const aulasHoje = agendaHoje.filter(ehAula)
  const estados = Object.fromEntries(
    situacoes(aulasHoje, agora.minutos).map((x) => [x.evento.id, { situacao: x.situacao, falta: x.falta, feito: x.feito }]),
  )
  const avisosHoje = agendaHoje.filter((e) => e.cancelado)
  const proximaAmanha = agendaAmanha.filter((e) => ehAula(e) && e.inicio).sort((a, b) => (a.inicio ?? '').localeCompare(b.inicio ?? ''))[0]
  const idsMaterias = materias.map((m) => m.id)

  // Provas: a próxima (que ainda não começou) com a contagem regressiva e as três seguintes em lista
  const provas = todasProvas.filter((p) => inicioMs(p) > agora.ms)
  const [prova, ...depois] = provas
  const diasAteProva = prova ? Math.round((Date.parse(`${prova.data}T12:00:00Z`) - Date.parse(`${agora.data}T12:00:00Z`)) / 86_400_000) : 0
  const diaDaProva = prova
    ? diasAteProva === 0
      ? 'Hoje'
      : diasAteProva === 1
        ? 'Amanhã'
        : new Intl.DateTimeFormat('pt-BR', { weekday: 'long', day: 'numeric', month: 'long', timeZone: 'UTC' })
            .format(new Date(`${prova.data}T12:00:00Z`))
            .replace(/^./, (c) => c.toUpperCase())
    : ''

  const nomeCompleto = perfil.data?.nome || email.split('@')[0] || 'aluno'
  // Na saudação vai só o primeiro nome, para caber numa linha
  const nome = /^\d+$/.test(nomeCompleto) ? 'aluno' : nomeCompleto.trim().split(/\s+/)[0]
  const { texto, data } = saudacao()

  // Mantém o selo de revisões pendentes na navegação.
  const pend = pendentes(progresso)

  return (
    <Pagina larga pendentes={pend.hoje}>
      <header className="top">
        <div>
          <div className="eyebrow">{data}</div>
          <h1 className="big saudacao">
            {texto}, {nome}
          </h1>
        </div>
      </header>

      <div className="inicio">
        <section className="in-agenda" aria-label="Agenda de hoje">
          <div className="sec ag-h">
            <span>{grupo ? 'Sua agenda hoje' : 'Agenda de hoje'}</span>
            <Link href="/agenda">Semana →</Link>
          </div>
          <AgendaDiaTodo eventos={diaTodo} materias={idsMaterias} />
          {aulasHoje.length > 0 ? (
            <AgendaLista eventos={aulasHoje} grupo={grupo} estados={estados} materias={idsMaterias} />
          ) : (
            <p className="vazio">Nenhuma aula hoje.</p>
          )}
          <AgendaAvisos eventos={avisosHoje} />
          {proximaAmanha && (
            <p className="in-amanha">
              <span className="in-k">Amanhã</span>
              <span>
                <b>{fmtHora(proximaAmanha.inicio)}</b> {proximaAmanha.titulo}
                {proximaAmanha.professor ? ` · ${proximaAmanha.professor}` : ''}
              </span>
            </p>
          )}
          {grupo === null && agendaHoje.length > 0 && (
            <p className="foot">
              <Link href="/agenda">Escolha seu grupo de prática na Agenda</Link> para ver só as suas práticas.
            </p>
          )}
        </section>

        {prova && (
          <section className="in-provas" aria-label="Provas">
            <div className="sec ag-h">
              <span>{provas.length > 1 ? 'Próximas provas' : 'Próxima prova'}</span>
              <Link href="/agenda#provas">Todas →</Link>
            </div>
            <div className="in-card in-prova" style={{ '--glow': COR_MATERIA[prova.materia ?? ''] } as React.CSSProperties}>
              <div className="pv-topo">
                <span className="pv-barra" style={{ background: COR_MATERIA[prova.materia ?? ''] ?? 'var(--line-strong)' }} />
                <span>
                  <span className="pv-t">{prova.titulo}</span>
                  <span className="pv-s">
                    <b className={diasAteProva <= 1 ? 'alerta' : ''}>{diaDaProva}</b>
                    {[fmtHora(prova.inicio), prova.local].filter(Boolean).map((x) => ` · ${x}`).join('')}
                  </span>
                </span>
              </div>
              <ContagemProva alvo={inicioMs(prova)} agora={agora.ms} />
              {prova.materia && idsMaterias.includes(prova.materia) && (
                <Link className="btn ghost" href={`/materia/${prova.materia}`}>
                  Estudar para a prova
                </Link>
              )}
              {depois.length > 0 && <AgendaProvas eventos={depois} hoje={agora.data} materias={idsMaterias} />}
            </div>
          </section>
        )}
      </div>
    </Pagina>
  )
}
