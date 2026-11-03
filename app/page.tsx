import type { Metadata } from 'next'
import Link from 'next/link'
import { Pagina } from '@/components/Pagina'
import { Icone } from '@/components/Icones'
import {
  carregarMaterias,
  carregarProgresso,
  carregarProgressoMaterias,
  concluidoMateria,
  pendentes,
  sessao,
  totais,
  totaisQuestoes,
} from '@/lib/dados'
import { plural, saudacao } from '@/lib/formato'
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

// Início: agenda do dia inteira, cards, questões e matérias numa tela só
export default async function Inicio() {
  const { supabase, userId, email } = await sessao()
  const agora = agoraBrasilia()
  const [perfil, materias, progresso, banco, agendaHoje, agendaAmanha, todasProvas] = await Promise.all([
    supabase.from('perfis').select('nome, grupo').eq('id', userId).maybeSingle(),
    carregarMaterias(supabase),
    carregarProgresso(supabase),
    carregarProgressoMaterias(supabase),
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

  // Cards: para revisar hoje (vencidos), novos e em dia
  const pend = pendentes(progresso)
  const cardsAtivos = pend.novos + pend.vencidos + pend.emDia

  // Questões: certas, erradas e a fazer (pelo banco de cada matéria)
  const tq = totaisQuestoes(banco)
  const erradas = tq.respondidas - tq.acertos
  const afazer = tq.questoes - tq.respondidas
  const acerto = tq.respondidas ? Math.round((100 * tq.acertos) / tq.respondidas) : null
  // Erradas numa matéria só: o botão já abre o banco dela filtrado; em várias, o Desempenho mostra cada uma
  const comErradas = banco.filter((b) => b.respondidas > b.acertos)
  const refazer = comErradas.length === 1 ? `/materia/${comErradas[0].materia_id}/questoes?mostrar=erradas` : '/desempenho'

  const ultima = progresso
    .filter((p) => p.ultima_atividade)
    .sort((a, b) => (b.ultima_atividade ?? '').localeCompare(a.ultima_atividade ?? ''))[0]

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
        <div className="in-status">
          <div className="in-col">
            <div className="sec ag-h">
              <span>Cards</span>
              <Link href="/revisao">Revisão →</Link>
            </div>
            <section className="in-card destaque" aria-label="Cards">
              <div className="in-n">
                <span className="n">{pend.vencidos}</span>
                <span className="u">
                  para revisar hoje
                  {pend.vencidos === 0 && pend.emDia > 0 && <b className="ok"> · em dia ✓</b>}
                </span>
              </div>
              <div className="in-nums">
                <span>
                  <b>{pend.novos}</b>
                  {plural(pend.novos, 'novo', 'novos')}
                </span>
                <span>
                  <b className={pend.vencidos ? 'alerta' : ''}>{pend.vencidos}</b>a revisar
                </span>
                <span>
                  <b>{pend.emDia}</b>em dia
                </span>
              </div>
              <div className="bar" role="img" aria-label={`${pend.emDia} em dia, ${pend.vencidos} a revisar, ${pend.novos} novos`}>
                <span className="b-ac" style={{ width: `${cardsAtivos ? (100 * pend.emDia) / cardsAtivos : 0}%` }} />
                <span className="b-al" style={{ width: `${cardsAtivos ? (100 * pend.vencidos) / cardsAtivos : 0}%` }} />
              </div>
              {pend.vencidos > 0 ? (
                <Link className="btn-white" href="/revisao">
                  Começar revisão
                </Link>
              ) : pend.novos > 0 ? (
                <Link className="btn-white" href="/revisao">
                  <span>
                    Estudar <span className="longo">cards </span>novos
                  </span>
                </Link>
              ) : (
                <p className="in-fim">Nenhum card pendente por agora.</p>
              )}
            </section>
          </div>

          <div className="in-col">
            <div className="sec ag-h">
              <span>Questões</span>
              <Link href="/desempenho">Desempenho →</Link>
            </div>
            <section className="in-card" aria-label="Questões">
              <div className="in-n">
                <span className="n">{tq.respondidas}</span>
                <span className="u">
                  de {tq.questoes} {plural(tq.respondidas, 'respondida', 'respondidas')}
                  {acerto !== null && <b className={acerto >= 70 ? 'ok' : 'alerta'}> · {acerto}% de acerto</b>}
                </span>
              </div>
              <div className="in-nums">
                <span>
                  <b className="ok">{tq.acertos}</b>
                  {plural(tq.acertos, 'certa', 'certas')}
                </span>
                <span>
                  <b className="ruim">{erradas}</b>
                  {plural(erradas, 'errada', 'erradas')}
                </span>
                <span>
                  <b>{afazer}</b>a fazer
                </span>
              </div>
              <div className="bar" role="img" aria-label={`${tq.acertos} certas, ${erradas} erradas, ${afazer} a fazer`}>
                <span className="b-ok" style={{ width: `${tq.questoes ? (100 * tq.acertos) / tq.questoes : 0}%` }} />
                <span className="b-bad" style={{ width: `${tq.questoes ? (100 * erradas) / tq.questoes : 0}%` }} />
              </div>
              {erradas > 0 ? (
                <Link className="btn ghost" href={refazer}>
                  <span>
                    Refazer <span className="longo">{erradas === 1 ? 'a ' : `as ${erradas} `}</span>
                    {erradas === 1 ? 'errada' : 'erradas'}
                  </span>
                </Link>
              ) : (
                <Link className="btn ghost" href="/estudar">
                  Responder questões
                </Link>
              )}
            </section>
          </div>
        </div>

        <div className="in-esq">
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

        <section className="in-materias" aria-label="Matérias">
          <div className="sec ag-h">
            <span>Matérias</span>
            <Link href="/estudar">Estudar →</Link>
          </div>
          <div className="in-mats">
            {materias.map((m) => {
              const prog = progresso.filter((p) => p.materia_id === m.id)
              const tm = totais(prog)
              const pm = banco.find((b) => b.materia_id === m.id)
              const q = pm?.total_questoes ?? 0
              const p = concluidoMateria(prog, pm)
              const continuar = ultima?.materia_id === m.id ? ultima : null
              const meta = [
                `${prog.length} ${plural(prog.length, 'aula', 'aulas')}`,
                q ? `${q} ${plural(q, 'questão', 'questões')}` : null,
                tm.cards ? `${tm.cards} cards` : null,
              ].filter(Boolean)
              return (
                <div
                  key={m.id}
                  className={`in-mat${continuar ? ' destaque' : ''}`}
                  style={{ '--c1': m.cor_inicio ?? '#2563EB', '--c2': m.cor_fim ?? '#1E3A8A', '--glow': COR_MATERIA[m.id] } as React.CSSProperties}
                >
                  <Link className="in-mat-a" href={`/materia/${m.id}`}>
                    <span className="gema nome-gema">{m.nome}</span>
                    <span className="mt-meta">{meta.join(' · ')}</span>
                    {q + tm.cards > 0 ? (
                      <span className="in-mat-p">
                        <span className="mt-bar">
                          <span style={{ width: `${p}%` }} />
                        </span>
                        {p}%
                      </span>
                    ) : (
                      <span className="in-mat-p">
                        <span className="longo">Questões em breve</span>
                        <span className="curto">Em breve</span>
                      </span>
                    )}
                  </Link>
                  {continuar && (
                    <Link className="in-mat-c" href={`/aula/${continuar.aula_id}`}>
                      <span>Continuar: {continuar.titulo}</span>
                      {Icone.seta}
                    </Link>
                  )}
                </div>
              )
            })}
          </div>
        </section>
      </div>
    </Pagina>
  )
}
