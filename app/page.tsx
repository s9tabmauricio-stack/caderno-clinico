import type { Metadata } from 'next'
import Link from 'next/link'
import { Pagina } from '@/components/Pagina'
import { Icone } from '@/components/Icones'
import {
  carregarMaterias,
  carregarProgresso,
  carregarProgressoMaterias,
  concluido,
  pendentes,
  sessao,
  totais,
  totaisQuestoes,
} from '@/lib/dados'
import { plural, saudacao } from '@/lib/formato'
import { COR_MATERIA, agoraBrasilia, ehDoAluno, situacoes } from '@/lib/agenda'
import { agendaDoDia } from '@/lib/agenda-dados'
import { AgendaAvisos, AgendaLista } from '@/components/AgendaLista'

export const metadata: Metadata = { title: { absolute: 'Med Genius · Início' } }

export default async function Inicio() {
  const { supabase, userId, email } = await sessao()
  const agora = agoraBrasilia()
  const [perfil, materias, progresso, banco, agendaHoje] = await Promise.all([
    supabase.from('perfis').select('nome, grupo').eq('id', userId).maybeSingle(),
    carregarMaterias(supabase),
    carregarProgresso(supabase),
    carregarProgressoMaterias(supabase),
    agendaDoDia(supabase, agora.data),
  ])

  // Agenda de hoje: teóricas e avisos para todos, práticas só do grupo do aluno
  const grupo = perfil.data?.grupo ?? null
  // Evento de 10h ou mais (ex.: "coordenação disponível") é um aviso do dia, não uma aula
  const duracao = (e: { inicio: string | null; fim: string | null }) => {
    if (!e.inicio || !e.fim) return 0
    const m = (h: string) => Number(h.slice(0, 2)) * 60 + Number(h.slice(3, 5))
    return m(e.fim) - m(e.inicio)
  }
  const diaTodo = agendaHoje.filter((e) => !e.cancelado && e.tipo !== 'aviso' && duracao(e) >= 600)
  const aulasHoje = agendaHoje.filter(
    (e) => !e.cancelado && e.tipo !== 'aviso' && duracao(e) < 600 && ehDoAluno(e.grupos, grupo),
  )
  const sits = situacoes(aulasHoje, agora.minutos)
  const estados = Object.fromEntries(sits.map((x) => [x.evento.id, { situacao: x.situacao, falta: x.falta }]))
  const aulasRestantes = sits.filter((x) => x.situacao !== 'passou').map((x) => x.evento)
  const avisosHoje = [...agendaHoje.filter((e) => e.cancelado), ...diaTodo]

  const nomeCompleto = perfil.data?.nome || email.split('@')[0] || 'aluno'
  // Na saudação vai só o primeiro nome, para caber numa linha
  const nome = /^\d+$/.test(nomeCompleto) ? 'aluno' : nomeCompleto.trim().split(/\s+/)[0]
  const { texto, data } = saudacao()
  const pend = pendentes(progresso)
  const t = totais(progresso)
  const tq = totaisQuestoes(banco)
  const acerto = tq.respondidas ? `${Math.round((100 * tq.acertos) / tq.respondidas)}%` : '–'

  const ultima = progresso
    .filter((p) => p.ultima_atividade)
    .sort((a, b) => (b.ultima_atividade ?? '').localeCompare(a.ultima_atividade ?? ''))[0]
  const materiaDaUltima = ultima && materias.find((m) => m.id === ultima.materia_id)

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

      <div className="inicio-cols">
        <div>
          <section className="review" aria-label="Revisão de hoje">
            <div className="review-k">Revisão de hoje</div>
            {pend.vencidos > 0 ? (
              <>
                <div className="review-n">
                  <span className="n">{pend.vencidos}</span>
                  <span className="u">{plural(pend.vencidos, 'card para revisar', 'cards para revisar')}</span>
                </div>
                <p className="review-s">
                  {pend.hoje > pend.vencidos
                    ? `e mais ${pend.hoje - pend.vencidos} ${plural(pend.hoje - pend.vencidos, 'novo', 'novos')} para começar`
                    : 'Revisar agora ajuda a fixar o conteúdo.'}
                </p>
                <Link className="btn-white" href="/revisao">
                  Começar revisão
                </Link>
              </>
            ) : pend.hoje > 0 ? (
              <>
                <div className="review-n">
                  <span className="u" style={{ fontSize: 28, letterSpacing: '-.02em' }}>
                    Revisões em dia ✓
                  </span>
                </div>
                <p className="review-s">
                  {pend.hoje} {plural(pend.hoje, 'card novo esperando', 'cards novos esperando')} · sem pressa
                </p>
                <Link className="btn-white" href="/revisao">
                  Estudar cards novos
                </Link>
              </>
            ) : (
              <>
                <div className="review-n">
                  <span className="u" style={{ fontSize: 28, letterSpacing: '-.02em' }}>
                    Tudo em dia ✓
                  </span>
                </div>
                <p className="review-s">Nenhum card pendente por agora.</p>
              </>
            )}
          </section>

          <div className="sec ag-h">
            <span>{grupo ? 'Suas aulas hoje' : 'Aulas de hoje'}</span>
            <Link href="/agenda">Semana →</Link>
          </div>
          {aulasRestantes.length > 0 ? (
            <AgendaLista
              eventos={aulasRestantes}
              grupo={grupo}
              estados={estados}
              materias={materias.map((m) => m.id)}
            />
          ) : (
            <p className="vazio">{aulasHoje.length ? 'As aulas de hoje já terminaram.' : 'Nenhuma aula hoje.'}</p>
          )}
          <AgendaAvisos eventos={avisosHoje} />
          {grupo === null && agendaHoje.length > 0 && (
            <p className="foot">
              <Link href="/agenda">Escolha seu grupo de prática na Agenda</Link> para ver só as suas práticas.
            </p>
          )}
        </div>
        <div>
          <div className="sec">{ultima ? 'Continuar' : 'Matérias'}</div>
          <div className="group">
            {ultima && (
              <Link className="row" href={`/aula/${ultima.aula_id}`}>
                <span
                  className="num"
                  style={{ background: `${COR_MATERIA[ultima.materia_id] ?? 'var(--accent)'}33`, color: COR_MATERIA[ultima.materia_id] }}
                >
                  {ultima.ordem}
                </span>
                <span className="main">
                  <span className="t">{ultima.titulo}</span>
                  <span className="s">
                    {materiaDaUltima?.nome} · {concluido([ultima])}% concluído
                  </span>
                </span>
                {Icone.seta}
              </Link>
            )}
            {!ultima && (
            <Link className="row" href="/estudar">
              <span className="main">
                <span className="t">{ultima ? 'Todas as matérias' : 'Escolher uma matéria'}</span>
                <span className="s">
                  {materias.length} {plural(materias.length, 'matéria', 'matérias')} · apostilas, questões e flashcards
                </span>
              </span>
              {Icone.seta}
            </Link>
            )}
          </div>

          <div className="sec ag-h">
            <span>Seu progresso</span>
            <Link href="/desempenho">Desempenho →</Link>
          </div>
          <Link className="stats stats-link" href="/desempenho" aria-label="Ver o desempenho completo">
            <div className="stat">
              <div className="lab">Questões</div>
              <div className="n">
                {tq.respondidas}
                <small>/{tq.questoes}</small>
              </div>
              <div className="bar"><i style={{ width: `${tq.questoes ? Math.round((100 * tq.respondidas) / tq.questoes) : 0}%` }} /></div>
            </div>
            <div className="stat">
              <div className="lab">Acerto</div>
              <div className={`n ${tq.respondidas ? (tq.acertos / tq.respondidas >= 0.7 ? 'ok' : 'alerta') : ''}`}>{acerto}</div>
              <div className="bar"><i style={{ width: acerto === '–' ? '0%' : acerto }} /></div>
            </div>
            <div className="stat">
              <div className="lab">Cards</div>
              <div className="n">
                {t.estudados}
                <small>/{t.cards}</small>
              </div>
              <div className="bar"><i style={{ width: `${t.cards ? Math.round((100 * t.estudados) / t.cards) : 0}%` }} /></div>
            </div>
          </Link>
        </div>
      </div>
    </Pagina>
  )
}
