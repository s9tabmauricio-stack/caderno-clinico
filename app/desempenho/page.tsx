import type { Metadata } from 'next'
import { Pagina } from '@/components/Pagina'
import {
  carregarMaterias,
  carregarProgresso,
  carregarProgressoMaterias,
  carregarTemas,
  pendentes,
  sessao,
  totais,
  totaisQuestoes,
} from '@/lib/dados'
import { plural } from '@/lib/formato'

export const metadata: Metadata = { title: 'Desempenho' }

export default async function DesempenhoPage() {
  const { supabase } = await sessao()
  const [progresso, materias, banco, temas] = await Promise.all([
    carregarProgresso(supabase),
    carregarMaterias(supabase),
    carregarProgressoMaterias(supabase),
    carregarTemas(supabase),
  ])
  const t = totais(progresso)
  const tq = totaisQuestoes(banco)
  const acerto = tq.respondidas ? `${Math.round((100 * tq.acertos) / tq.respondidas)}%` : '–'

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
            {tq.respondidas}
            <small>/{tq.questoes}</small>
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
          const s = totaisQuestoes(banco.filter((b) => b.materia_id === m.id))
          const temasM = temas.filter((x) => x.materia_id === m.id)
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
              {temasM.length > 0 && (
                <div className="perf-aulas">
                  {temasM.map((x) => (
                    <div key={x.tema} className="pa">
                      <span>{x.tema}</span>
                      <span>
                        {x.respondidas ? `${x.acertos} de ${x.respondidas} certas` : `${x.total_questoes} sem responder`}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )
        })}
      </div>
      {tq.respondidas === 0 && <p className="foot">Responda as questões de uma aula para ver as barras se encherem.</p>}
    </Pagina>
  )
}
