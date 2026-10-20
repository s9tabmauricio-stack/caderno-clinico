import Link from 'next/link'
import { COR_MATERIA, fmtFalta, fmtHora, type Situacao } from '@/lib/agenda'
import type { EventoBanco } from '@/lib/agenda-dados'
import { Icone } from './Icones'

type Estado = { situacao: Situacao; falta: number }

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
        const detalhes = [
          e.grupos?.length && e.grupos.length <= 6 ? `${e.grupos.length > 1 ? 'Grupos' : 'Grupo'} ${juntar(e.grupos)}` : null,
          e.professor,
          e.local,
        ].filter(Boolean)
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
              <span className="t">
                {e.cancelado && <span className="tg cancel">Cancelada</span>}
                {st?.situacao === 'agora' && <span className="tg agora">Agora</span>}
                {st?.situacao === 'proxima' && <span className="tg prox">{fmtFalta(st.falta)}</span>}
                {meu && <span className="tg meu">Seu grupo</span>}
                {e.titulo}
              </span>
              {detalhes.length > 0 && <span className="s">{detalhes.join(' · ')}</span>}
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
