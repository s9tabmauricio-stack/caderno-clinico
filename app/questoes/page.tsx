import type { Metadata } from 'next'
import Link from 'next/link'
import { Pagina } from '@/components/Pagina'
import { Icone } from '@/components/Icones'
import { carregarMaterias, carregarProgresso, carregarProgressoMaterias, pendentes, sessao, totaisQuestoes } from '@/lib/dados'
import { plural } from '@/lib/formato'

export const metadata: Metadata = { title: 'Questões' }

export default async function QuestoesPage() {
  const { supabase } = await sessao()
  const [materias, progresso, banco] = await Promise.all([
    carregarMaterias(supabase),
    carregarProgresso(supabase),
    carregarProgressoMaterias(supabase),
  ])
  const tq = totaisQuestoes(banco)
  const comQuestoes = materias.filter((m) => (banco.find((b) => b.materia_id === m.id)?.total_questoes ?? 0) > 0)

  return (
    <Pagina pendentes={pendentes(progresso).hoje}>
      <header className="top">
        <div>
          <div className="eyebrow">Banco de questões</div>
          <h1 className="big">Questões</h1>
          <p className="lead">
            {tq.questoes} {plural(tq.questoes, 'questão', 'questões')} de provas anteriores · {tq.respondidas}{' '}
            {plural(tq.respondidas, 'respondida', 'respondidas')}
          </p>
        </div>
      </header>

      {comQuestoes.length ? (
        <div className="group">
          {comQuestoes.map((m) => {
            const pm = banco.find((b) => b.materia_id === m.id)!
            return (
              <Link key={m.id} className="row banco-row" href={`/materia/${m.id}/questoes`}>
                <span className="num">{Icone.certo}</span>
                <span className="main">
                  <span className="t">{m.nome}</span>
                  <span className="s">
                    {pm.total_questoes} {plural(pm.total_questoes, 'questão', 'questões')} · {pm.respondidas}{' '}
                    {plural(pm.respondidas, 'respondida', 'respondidas')}
                    {pm.respondidas > 0 && ` · ${Math.round((100 * pm.acertos) / pm.respondidas)}% de acerto`}
                  </span>
                </span>
                {Icone.seta}
              </Link>
            )
          })}
        </div>
      ) : (
        <p className="vazio">O banco de questões ainda está vazio.</p>
      )}
    </Pagina>
  )
}
