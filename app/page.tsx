import type { Metadata } from 'next'
import Link from 'next/link'
import { Pagina } from '@/components/Pagina'
import { Icone } from '@/components/Icones'
import {
  carregarMaterias,
  carregarProgresso,
  carregarProgressoMaterias,
  concluido,
  concluidoMateria,
  pendentes,
  sessao,
} from '@/lib/dados'
import { plural, saudacao } from '@/lib/formato'
import { COR_MATERIA, agoraBrasilia, ehDoAluno, situacoes } from '@/lib/agenda'
import { agendaDoDia } from '@/lib/agenda-dados'
import { AgendaAvisos, AgendaLista, coresDasMaterias } from '@/components/AgendaLista'

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
  // Revisão de hoje: quantos cards vencidos em cada matéria e o tempo aproximado (cerca de 30 s por card)
  const porMateria = materias
    .map((m) => ({
      nome: m.id === 'pass' ? 'PASS' : m.id.charAt(0).toUpperCase() + m.id.slice(1),
      n: progresso.filter((p) => p.materia_id === m.id).reduce((s, p) => s + p.cards_vencidos, 0),
    }))
    .filter((x) => x.n > 0)
  const minutos = Math.max(1, Math.round(pend.vencidos / 2))
  const resumoRevisao = [...porMateria.map((x) => `${x.nome} ${x.n}`), `cerca de ${minutos} min`].join(' · ')
  // Seu progresso: % concluído de cada matéria (questões do banco + flashcards estudados)
  const progressoMaterias = materias.map((m) => ({
    id: m.id,
    nome: m.nome,
    pct: concluidoMateria(
      progresso.filter((p) => p.materia_id === m.id),
      banco.find((b) => b.materia_id === m.id),
    ),
  }))

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
                  <span className="u">{plural(pend.vencidos, 'card', 'cards')}</span>
                </div>
                <p className="review-s">{resumoRevisao}</p>
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

          <h2 className="sec">{grupo ? 'Suas aulas hoje' : 'Aulas de hoje'}</h2>
          {aulasRestantes.length > 0 ? (
            <AgendaLista
              eventos={aulasRestantes}
              grupo={grupo}
              estados={estados}
              materias={materias.map((m) => m.id)}
              cores={coresDasMaterias(materias)}
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
          <h2 className="sec">{ultima ? 'Continuar' : 'Matérias'}</h2>
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

          <h2 className="sec">Seu progresso</h2>
          <Link className="group progresso" href="/desempenho" aria-label="Seu progresso: ver o desempenho completo">
            {progressoMaterias.map((m) => (
              <span key={m.id} className="pm">
                <span className="pm-h">
                  <span>{m.nome}</span>
                  <span className="pm-p">{m.pct}%</span>
                </span>
                <span className="pm-bar">
                  <i style={{ width: `${m.pct}%` }} />
                </span>
              </span>
            ))}
          </Link>
        </div>
      </div>
    </Pagina>
  )
}
