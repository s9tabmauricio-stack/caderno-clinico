import type { Metadata } from 'next'
import { Pagina } from '@/components/Pagina'
import { carregarMaterias, carregarProgresso, pendentes, sessao, totais } from '@/lib/dados'
import { plural } from '@/lib/formato'

export const metadata: Metadata = { title: 'Desempenho' }

export default async function DesempenhoPage() {
  const { supabase } = await sessao()
  const [progresso, materias] = await Promise.all([carregarProgresso(supabase), carregarMaterias(supabase)])
  const t = totais(progresso)
  const acerto = t.respondidas ? `${Math.round((100 * t.acertos) / t.respondidas)}%` : '–'

  return (
    <Pagina pendentes={pendentes(progresso).hoje}>
      <header className="top">
        <div>
          <div className="eyebrow">Suas estatísticas</div>
          <h1 className="big">Desempenho</h1>
        </div>
      </header>

      <div className="stats">
        <div className="stat">
          <div className="lab">Respondidas</div>
          <div className="n">
            {t.respondidas}
            <small>/{t.questoes}</small>
          </div>
        </div>
        <div className="stat">
          <div className="lab">Acerto</div>
          <div className="n">{acerto}</div>
        </div>
        <div className="stat">
          <div className="lab">Cards</div>
          <div className="n">
            {t.estudados}
            <small>/{t.cards}</small>
          </div>
        </div>
      </div>

      <div className="sec">Por matéria</div>
      <div className="legend">
        <span>
          <i style={{ background: 'var(--ok)' }} />
          Certas
        </span>
        <span>
          <i style={{ background: 'var(--bad)' }} />
          Erradas
        </span>
        <span>
          <i style={{ background: 'var(--seg)' }} />
          Sem responder
        </span>
      </div>

      <div className="perfs">
        {materias.map((m) => {
          const aulas = progresso.filter((p) => p.materia_id === m.id)
          const s = totais(aulas)
          const erradas = s.respondidas - s.acertos
          const sem = s.questoes - s.respondidas
          return (
            <div key={m.id} className="perf">
              <div className="perf-h">
                <span className="t">{m.nome}</span>
                <span className="pv">
                  {s.respondidas ? `${Math.round((100 * s.acertos) / s.respondidas)}% de acerto` : 'Sem respostas'}
                </span>
              </div>
              <div className="bar" role="img" aria-label={`${s.acertos} certas, ${erradas} erradas, ${sem} sem responder`}>
                <span className="b-ok" style={{ width: `${s.questoes ? (100 * s.acertos) / s.questoes : 0}%` }} />
                <span className="b-bad" style={{ width: `${s.questoes ? (100 * erradas) / s.questoes : 0}%` }} />
              </div>
              <div className="perf-s">
                {s.acertos} {plural(s.acertos, 'certa', 'certas')} · {erradas} {plural(erradas, 'errada', 'erradas')} · {sem} sem
                responder
              </div>
              <div className="perf-aulas">
                {aulas.map((a) => (
                  <div key={a.aula_id} className="pa">
                    <span>{a.titulo}</span>
                    <span>{a.respondidas ? `${a.acertos} de ${a.respondidas} certas` : 'não iniciada'}</span>
                  </div>
                ))}
              </div>
            </div>
          )
        })}
      </div>
      {t.respondidas === 0 && <p className="foot">Responda as questões de uma aula para ver as barras se encherem.</p>}
    </Pagina>
  )
}
