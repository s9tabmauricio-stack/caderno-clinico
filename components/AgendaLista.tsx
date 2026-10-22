import Link from 'next/link'
import { COR_MATERIA, fmtDuracao, fmtHora, type Situacao } from '@/lib/agenda'
import type { EventoBanco } from '@/lib/agenda-dados'
import { Icone } from './Icones'

type Estado = { situacao: Situacao; falta: number; feito?: number }

/**
 * Lista de aulas no estilo das listas do app (hora, faixa de cor da matéria, título e detalhes).
 * Com `materias` (ids das matérias do app), cada aula abre a página da sua matéria.
 */
export function AgendaLista({
  eventos,
  grupo,
  estados,
  materias,
}: {
  eventos: EventoBanco[]
  grupo: number | null
  estados?: Record<number, Estado>
  materias?: string[]
}) {
  return (
    <div className="group agenda">
      {eventos.map((e) => {
        const st = estados?.[e.id]
        const meu = grupo !== null && !!e.grupos?.length && e.grupos.includes(grupo)
        // Do grupo do aluno: "Seu grupo" no lugar da lista de grupos
        const grupos =
          meu ? null : e.grupos?.length && e.grupos.length <= 6 ? `${e.grupos.length > 1 ? 'Grupos' : 'Grupo'} ${juntar(e.grupos)}` : null
        const detalhes = [grupos, e.professor, e.local].filter(Boolean)
        const href = !e.cancelado && e.materia && materias?.includes(e.materia) ? `/materia/${e.materia}` : null
        const classes = `row ev ${st?.situacao ?? ''} ${e.cancelado ? 'cancel' : ''}`
        const conteudo = (
          <>
            <span className="hora">
              {e.inicio ? fmtHora(e.inicio) : '—'}
              {e.fim && <small>{fmtHora(e.fim)}</small>}
            </span>
            <span className="barra" style={{ background: COR_MATERIA[e.materia ?? ''] ?? 'var(--line-strong)' }} />
            <span className="main">
              {e.cancelado ? (
                <span className="olho cancel">Cancelada</span>
              ) : st?.situacao === 'agora' ? (
                <span className="olho agora">
                  <i aria-hidden />
                  Agora<span> · termina em {fmtDuracao(st.falta)}</span>
                </span>
              ) : st?.situacao === 'proxima' ? (
                <span className="olho prox">
                  Próxima<span> · em {fmtDuracao(st.falta)}</span>
                </span>
              ) : null}
              <span className="t">{e.titulo}</span>
              {(meu || detalhes.length > 0) && (
                <span className="s">
                  {meu && <span className="meu">Seu grupo</span>}
                  {meu && detalhes.length > 0 && ' · '}
                  {detalhes.join(' · ')}
                </span>
              )}
              {!!e.notas?.length && (
                <span className="notas">
                  {e.notas.map((n, i) => (
                    <span key={i}>{n}</span>
                  ))}
                </span>
              )}
            </span>
            {href && Icone.seta}
            {st?.situacao === 'agora' && st.feito !== undefined && (
              <span className="prog" style={{ width: `${Math.round(st.feito * 100)}%` }} aria-hidden />
            )}
          </>
        )
        return href ? (
          <Link key={e.id} className={classes} href={href}>
            {conteudo}
          </Link>
        ) : (
          <div key={e.id} className={`${classes} static`}>
            {conteudo}
          </div>
        )
      })}
    </div>
  )
}

/** Próximas provas: a data no lugar da hora e, embaixo do título, o horário e quanto falta. */
export function AgendaProvas({ eventos, hoje, materias }: { eventos: EventoBanco[]; hoje: string; materias?: string[] }) {
  if (!eventos.length) return null
  const base = new Date(`${hoje}T12:00:00Z`).getTime()
  return (
    <div className="group agenda">
      {eventos.map((e) => {
        const dt = new Date(`${e.data}T12:00:00Z`)
        const dias = Math.round((dt.getTime() - base) / 86_400_000)
        const falta = dias === 0 ? 'Hoje' : dias === 1 ? 'Amanhã' : `Em ${dias} dias`
        const detalhes = [fmtHora(e.inicio), e.local, falta].filter(Boolean)
        const href = e.materia && materias?.includes(e.materia) ? `/materia/${e.materia}` : null
        const conteudo = (
          <>
            <span className="hora">
              {new Intl.DateTimeFormat('pt-BR', { day: '2-digit', month: '2-digit', timeZone: 'UTC' }).format(dt)}
              <small>{new Intl.DateTimeFormat('pt-BR', { weekday: 'short', timeZone: 'UTC' }).format(dt).replace('.', '')}</small>
            </span>
            <span className="barra" style={{ background: COR_MATERIA[e.materia ?? ''] ?? 'var(--line-strong)' }} />
            <span className="main">
              <span className="t">{e.titulo}</span>
              <span className="s">{detalhes.join(' · ')}</span>
              {!!e.notas?.length && (
                <span className="notas">
                  {e.notas.map((n, i) => (
                    <span key={i}>{n}</span>
                  ))}
                </span>
              )}
            </span>
            {href && Icone.seta}
          </>
        )
        return href ? (
          <Link key={e.id} className="row ev" href={href}>
            {conteudo}
          </Link>
        ) : (
          <div key={e.id} className="row ev static">
            {conteudo}
          </div>
        )
      })}
    </div>
  )
}

function juntar(ns: number[]) {
  return ns.length === 1 ? String(ns[0]) : `${ns.slice(0, -1).join(', ')} e ${ns[ns.length - 1]}`
}

/** Avisos do dia (cancelamentos e recados) num quadro discreto, uma linha por aviso. */
export function AgendaAvisos({ eventos }: { eventos: EventoBanco[] }) {
  if (!eventos.length) return null
  return (
    <div className="ag-aviso">
      {eventos.map((e) => (
        <div key={e.id} className={`ag-item ${e.cancelado ? 'c' : 'i'}`}>
          <span className="ic" aria-hidden>
            {e.cancelado ? '✕' : 'i'}
          </span>
          <span>
            <b>
              {e.cancelado ? 'Cancelada: ' : ''}
              {e.titulo}
            </b>
            {e.cancelado && e.professor ? ` com ${e.professor}` : ''}
            {e.cancelado && e.local ? ` (${e.local})` : ''}
            {!!e.notas?.length && <span className="ag-aviso-n">{e.notas.join(' · ')}</span>}
          </span>
        </div>
      ))}
    </div>
  )
}

/** Eventos que duram o dia todo (ex.: "coordenação disponível das 8h às 22h30"), num cartão pequeno acima da lista. */
export function AgendaDiaTodo({ eventos, materias }: { eventos: EventoBanco[]; materias?: string[] }) {
  if (!eventos.length) return null
  return (
    <div className="ag-dia">
      {eventos.map((e) => {
        const detalhes = [`${fmtHora(e.inicio)} às ${fmtHora(e.fim)}`, e.professor, e.local].filter(Boolean)
        const href = e.materia && materias?.includes(e.materia) ? `/materia/${e.materia}` : null
        const conteudo = (
          <>
            <span className="ic">Dia todo</span>
            <span className="main">
              <span className="t">{e.titulo}</span>
              <span className="s">{detalhes.join(' · ')}</span>
            </span>
            {href && Icone.seta}
          </>
        )
        return href ? (
          <Link key={e.id} className="row" href={href}>
            {conteudo}
          </Link>
        ) : (
          <div key={e.id} className="row static">
            {conteudo}
          </div>
        )
      })}
    </div>
  )
}
