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
} from '@/lib/dados'
import { plural } from '@/lib/formato'
import { COR_MATERIA } from '@/lib/agenda'

export const metadata: Metadata = { title: 'Matérias' }

// Porta de entrada do conteúdo: cada matéria leva às aulas (apostila, questões e flashcards)
// e, logo abaixo, direto ao banco de questões dela.
export default async function EstudarPage() {
  const { supabase } = await sessao()
  const [materias, progresso, banco] = await Promise.all([
    carregarMaterias(supabase),
    carregarProgresso(supabase),
    carregarProgressoMaterias(supabase),
  ])

  return (
    <Pagina larga pendentes={pendentes(progresso).hoje}>
      <header className="top">
        <div>
          <div className="eyebrow">Apostilas, questões e flashcards</div>
          <h1 className="big">Matérias</h1>
        </div>
      </header>

      {materias.length ? (
        <div className="tiles">
          {materias.map((m) => {
            const prog = progresso.filter((p) => p.materia_id === m.id)
            const tm = totais(prog)
            const pm = banco.find((b) => b.materia_id === m.id)
            const p = concluidoMateria(prog, pm)
            return (
              <div key={m.id} className="ecard">
                <Link
                  className="mtile"
                  href={`/materia/${m.id}`}
                  style={{ '--c1': m.cor_inicio ?? '#2563EB', '--c2': m.cor_fim ?? '#1E3A8A', '--glow': COR_MATERIA[m.id] } as React.CSSProperties}
                >
                  <span>
                    <span className="mt-name">{m.nome}</span>
                    <span className="mt-meta">
                      {prog.length} {plural(prog.length, 'aula', 'aulas')} · {pm?.total_questoes ?? 0} questões · {tm.cards} flashcards
                    </span>
                  </span>
                  <span>
                    <span className="mt-bar">
                      <span style={{ width: `${p}%` }} />
                    </span>
                    <span className="mt-p">{p}% concluído</span>
                  </span>
                </Link>
                {pm && pm.total_questoes > 0 && (
                  <Link className="ecard-banco" href={`/materia/${m.id}/questoes`}>
                    <span className="main">
                      <span className="t">Banco de questões</span>
                      <span className="s">
                        {pm.total_questoes} {plural(pm.total_questoes, 'questão', 'questões')}
                        {pm.respondidas > 0 && ` · ${Math.round((100 * pm.acertos) / pm.respondidas)}% de acerto`}
                      </span>
                    </span>
                    {Icone.seta}
                  </Link>
                )}
              </div>
            )
          })}
        </div>
      ) : (
        <p className="vazio">Nenhuma matéria publicada ainda.</p>
      )}
    </Pagina>
  )
}
