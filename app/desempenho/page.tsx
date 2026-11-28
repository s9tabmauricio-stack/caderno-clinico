import type { Metadata } from 'next'
import Link from 'next/link'
import { Pagina } from '@/components/Pagina'
import { Icone } from '@/components/Icones'
import {
  carregarMaterias,
  carregarProgresso,
  carregarProgressoMaterias,
  carregarTemas,
  carregarTentativas,
  pendentes,
  sessao,
  totais,
  totaisQuestoes,
  totaisTentativas,
} from '@/lib/dados'
import { plural } from '@/lib/formato'

export const metadata: Metadata = { title: 'Desempenho' }

type Tema = Awaited<ReturnType<typeof carregarTemas>>[number]
const taxa = (a: number, n: number) => (n ? Math.round((100 * a) / n) : null)

export default async function DesempenhoPage({ searchParams }: PageProps<'/desempenho'>) {
  const { abrir } = await searchParams
  const { supabase } = await sessao()
  const [progresso, materias, banco, temas, tentativas] = await Promise.all([
    carregarProgresso(supabase),
    carregarMaterias(supabase),
    carregarProgressoMaterias(supabase),
    carregarTemas(supabase),
    carregarTentativas(supabase),
  ])
  const t = totais(progresso)
  const tq = totaisQuestoes(banco)
  const tt = totaisTentativas(tentativas)
  const pct = (a: number, n: number) => {
    const v = taxa(a, n)
    return v === null ? '–' : `${v}%`
  }
  const nomeMateria = new Map(materias.map((m) => [m.id, m.nome]))
  const linkTema = (x: Tema) =>
    `/materia/${x.materia_id}/questoes?tema=${encodeURIComponent(x.tema)}&de=desempenho&retorno=${encodeURIComponent(`/desempenho?abrir=${x.materia_id}#materia-${x.materia_id}`)}`

  // Os temas em que mais erra (pelo menos 3 respondidas e menos de 70% de acerto), no máximo 3.
  const fracos = temas
    .filter((x) => x.respondidas >= 3 && x.acertos / x.respondidas < 0.7)
    .sort((a, b) => a.acertos / a.respondidas - b.acertos / b.respondidas || b.respondidas - a.respondidas)
    .slice(0, 3)

  const lista = materias
    .map((m) => ({ m, s: totaisQuestoes(banco.filter((b) => b.materia_id === m.id)) }))
    .filter(({ s }) => s.questoes > 0)

  return (
    <Pagina larga pendentes={pendentes(progresso).hoje}>
      <header className="top">
        <div>
          <div className="eyebrow">Suas estatísticas</div>
          <h1 className="big">Desempenho</h1>
        </div>
      </header>

      <div className="stats quatro">
        <div className="stat">
          <div className="lab">Respondidas</div>
          <div className="n">
            {tq.respondidas}
            <small>/{tq.questoes}</small>
          </div>
        </div>
        <div className="stat" title="Pela última resposta de cada questão">
          <div className="lab">Acerto atual</div>
          <div className="n">{pct(tq.acertos, tq.respondidas)}</div>
        </div>
        <div className="stat" title="Só a primeira resposta de cada questão; refazer não muda">
          <div className="lab">Acerto na 1ª vez</div>
          <div className="n">{pct(tt.acertos_primeira, tt.primeiras)}</div>
        </div>
        <div className="stat">
          <div className="lab">Cards</div>
          <div className="n">
            {t.estudados}
            <small>/{t.cards}</small>
          </div>
        </div>
      </div>

      {fracos.length > 0 && (
        <>
          <div className="sec">Para reforçar</div>
          <div className="perf perf-fracos">
            {fracos.map((x) => (
              <Link key={`${x.materia_id}-${x.tema}`} className="pa" href={linkTema(x)}>
                <span>
                  {x.tema}
                  <small className="pa-m">{nomeMateria.get(x.materia_id)}</small>
                </span>
                <span className="pa-r">
                  <span className="pa-bad">{pct(x.acertos, x.respondidas)}</span>
                  {Icone.seta}
                </span>
              </Link>
            ))}
          </div>
        </>
      )}

      <div className="sec">Por matéria</div>
      <div className="perfs">
        {lista.map(({ m, s }) => {
          const temasM = temas
            .filter((x) => x.materia_id === m.id)
            .sort((a, b) => (taxa(a.acertos, a.respondidas) ?? 101) - (taxa(b.acertos, b.respondidas) ?? 101))
          const h = totaisTentativas(tentativas.filter((x) => x.materia_id === m.id))
          const erradas = s.respondidas - s.acertos
          const sem = s.questoes - s.respondidas
          const retorno = encodeURIComponent(`/desempenho?abrir=${m.id}#materia-${m.id}`)
          return (
            <details key={m.id} id={`materia-${m.id}`} className="perf perf-d" open={abrir === m.id}>
              <summary>
                <div className="perf-h">
                  <span className="t">{m.nome}</span>
                  <span className="pv">
                    {s.respondidas ? `${pct(s.acertos, s.respondidas)} de acerto` : 'Sem respostas'}
                    <span className="perf-seta" aria-hidden="true">{Icone.seta}</span>
                  </span>
                </div>
                <div className="bar" role="img" aria-label={`${s.acertos} certas, ${erradas} erradas, ${sem} sem responder`}>
                  <span className="b-ok" style={{ width: `${(100 * s.acertos) / s.questoes}%` }} />
                  <span className="b-bad" style={{ width: `${(100 * erradas) / s.questoes}%` }} />
                </div>
                <div className="perf-s perf-cont">
                  <span><i className="d-ok" />{s.acertos} {plural(s.acertos, 'certa', 'certas')}</span>
                  <span><i className="d-bad" />{erradas} {plural(erradas, 'errada', 'erradas')}</span>
                  <span><i className="d-sem" />{sem} sem responder</span>
                </div>
              </summary>
              <div className="perf-corpo">
                {h.tentativas > 0 && (
                  <div className="perf-s">
                    Na 1ª vez: {pct(h.acertos_primeira, h.primeiras)} de acerto · {h.tentativas}{' '}
                    {plural(h.tentativas, 'resposta', 'respostas')} no total
                  </div>
                )}
                {erradas > 0 && (
                  <Link className="btn ghost sm perf-treino" href={`/materia/${m.id}/questoes?mostrar=erradas&de=desempenho&retorno=${retorno}`}>
                    Refazer {erradas === 1 ? 'a errada' : `as ${erradas} erradas`}
                  </Link>
                )}
                {temasM.length > 0 && (
                  <div className="perf-aulas">
                    <p className="perf-dica">Temas, do mais fraco ao mais forte. Toque para treinar só ele.</p>
                    {temasM.map((x) => {
                      const v = taxa(x.acertos, x.respondidas)
                      return (
                        <Link key={x.tema} className="pa" href={linkTema(x)}>
                          <span>{x.tema}</span>
                          <span className="pa-r">
                            <span className={v === null ? undefined : v < 50 ? 'pa-bad' : v >= 80 ? 'pa-ok' : undefined}>
                              {x.respondidas ? `${x.acertos}/${x.respondidas}` : `${x.total_questoes} novas`}
                            </span>
                            {Icone.seta}
                          </span>
                        </Link>
                      )
                    })}
                  </div>
                )}
              </div>
            </details>
          )
        })}
      </div>
      {tq.respondidas === 0 && <p className="foot">Responda as questões de uma aula para ver as barras se encherem.</p>}
    </Pagina>
  )
}
