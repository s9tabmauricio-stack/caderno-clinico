import Link from 'next/link'
import { TIPOS_CALENDARIO, fimDo, fmtDiaSemana, fmtFalta, fmtPeriodo, nomeMes, porMes, type Marco } from '@/lib/calendario'

const tipo = (m: Marco) => TIPOS_CALENDARIO[m.tipo] ?? { rotulo: m.tipo, emoji: '📅', cor: 'neutro' }

/** Faixas do calendário acadêmico num dia da Agenda (feriado, semana de provas…). */
export function CalendarioDia({ marcos }: { marcos: Marco[] }) {
  if (!marcos.length) return null
  return (
    <div className="cal-dia">
      {marcos.map((m) => (
        <div key={m.id} className={`cal-faixa cal-${tipo(m).cor}`}>
          <span aria-hidden>{tipo(m).emoji}</span>
          <span>
            <b>{m.titulo}</b>
            {m.tipo === 'feriado' || m.tipo === 'recesso' ? <span className="cal-s"> · sem aula</span> : null}
            {m.fim && m.fim !== m.inicio ? <span className="cal-s"> · {fmtPeriodo(m)}</span> : null}
          </span>
        </div>
      ))}
    </div>
  )
}

/** Linha do Início: o que vale hoje e o próximo marco do calendário. */
export function CalendarioInicio({ agora, proximo, hoje }: { agora: Marco[]; proximo: Marco | null; hoje: string }) {
  if (!agora.length && !proximo) return null
  return (
    <Link className="cal-inicio" href="/agenda#calendario">
      <span className="in-k">Calendário</span>
      {agora.map((m) => (
        <span key={m.id}>
          <span aria-hidden>{tipo(m).emoji} </span>
          <b>{fimDo(m) === m.inicio ? 'Hoje' : `Até ${fmtPeriodo({ ...m, inicio: fimDo(m), fim: null })}`}:</b> {m.titulo}
        </span>
      ))}
      {proximo && (
        <span>
          <span aria-hidden>{tipo(proximo).emoji} </span>
          {proximo.titulo} · {[fmtDiaSemana(proximo), fmtPeriodo(proximo)].filter(Boolean).join(', ')} ·{' '}
          <b className={fmtFalta(hoje, proximo.inicio).startsWith('em') ? '' : 'alerta'}>{fmtFalta(hoje, proximo.inicio)}</b>
        </span>
      )}
    </Link>
  )
}

/** Lista do ano na Agenda, mês a mês; os meses que já passaram ficam recolhidos. */
export function CalendarioAno({ marcos, hoje }: { marcos: Marco[]; hoje: string }) {
  if (!marcos.length) return null
  const meses = porMes(marcos)
  const mesAtual = hoje.slice(0, 7)
  const passados = meses.filter(([k]) => k < mesAtual)
  const futuros = meses.filter(([k]) => k >= mesAtual)

  const mes = ([k, lista]: [string, Marco[]]) => (
    <div key={k} className="cal-mes">
      <div className="cal-mes-t">{nomeMes(k)}</div>
      <div className="group cal-lista">
        {lista.map((m) => {
          const passou = fimDo(m) < hoje
          const valendo = m.inicio <= hoje && fimDo(m) >= hoje
          return (
            <div key={m.id} className={`row cal-row cal-${tipo(m).cor}${passou ? ' passou' : ''}${valendo ? ' valendo' : ''}`}>
              <span className="cal-quando">{fmtPeriodo(m)}</span>
              <span className="main">
                <span className="t">{m.titulo}</span>
                <span className="s">
                  <span className="cal-tag">{tipo(m).rotulo}</span>
                  {valendo ? ' · agora' : m.inicio > hoje ? ` · ${fmtFalta(hoje, m.inicio)}` : ''}
                </span>
              </span>
            </div>
          )
        })}
      </div>
    </div>
  )

  return (
    <div className="cal-ano">
      {futuros.map(mes)}
      {passados.length > 0 && (
        <details className="cal-passados">
          <summary>Meses que já passaram ({passados.length})</summary>
          {passados.map(mes)}
        </details>
      )}
    </div>
  )
}
