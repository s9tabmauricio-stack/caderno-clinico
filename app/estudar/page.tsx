import type { Metadata } from 'next'
import Link from 'next/link'
import { Pagina } from '@/components/Pagina'
import { correspondeBusca } from '@/lib/navegacao'
import { Icone } from '@/components/Icones'
import {
  lerTudo,
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
export default async function EstudarPage(props: PageProps<'/estudar'>) {
  const { q } = await props.searchParams
  const busca = typeof q === 'string' ? q.trim().slice(0, 200) : ''
  const { supabase } = await sessao()
  const [materias, progresso, banco] = await Promise.all([
    carregarMaterias(supabase),
    carregarProgresso(supabase),
    carregarProgressoMaterias(supabase),
  ])

  const aulas = busca ? await lerTudo('as aulas para busca', (de, ate) =>
    supabase.from('aulas').select('id, titulo, resumo, materia_id').eq('publicada', true).order('id').range(de, ate),
  ) : []
  const resultados = aulas.filter((a) => correspondeBusca(busca, a.titulo, a.resumo, materias.find((m) => m.id === a.materia_id)?.nome))
  const retorno = `/estudar?${new URLSearchParams({ q: busca })}`

  return (
    <Pagina larga pendentes={pendentes(progresso).hoje}>
      <header className="top">
        <div>
          <div className="eyebrow">Apostilas, questões e flashcards</div>
          <h1 className="big">Matérias</h1>
        </div>
      </header>

      <form action="/estudar" className="busca-aulas" role="search">
        <label htmlFor="busca-aulas">Buscar aulas por título ou tema</label>
        <div className="busca-campos">
          <input id="busca-aulas" name="q" type="search" defaultValue={busca} key={busca} maxLength={200} placeholder="Ex.: pneumonia, nefrologia…" />
          <button className="btn" type="submit">Buscar</button>
          {busca && <Link className="btn ghost" href="/estudar">Limpar</Link>}
        </div>
        <p className="foot">Busca nos títulos, resumos e nomes das matérias.</p>
      </form>
      {busca && (
        <section className="busca-resultados" aria-label="Resultados da busca">
          <h2 className="sec">{resultados.length} {plural(resultados.length, 'aula encontrada', 'aulas encontradas')} para “{busca}”</h2>
          {resultados.length ? <div className="group">{resultados.map((a) => (
            <Link key={a.id} className="row" href={`/aula/${a.id}?${new URLSearchParams({ retorno })}`}>
              <span className="main">
                <span className="s">{materias.find((m) => m.id === a.materia_id)?.nome}</span>
                <span className="t">{a.titulo}</span>
                {a.resumo && <span className="s">{a.resumo}</span>}
              </span>
              {Icone.seta}
            </Link>
          ))}</div> : <p className="vazio">Nenhuma aula encontrada. Tente outro termo ou escolha uma matéria abaixo.</p>}
        </section>
      )}

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
                  <span className="gema nome-gema">{m.nome}</span>
                  <span className="mt-meta">
                    {prog.length} {plural(prog.length, 'aula', 'aulas')} · {pm?.total_questoes ?? 0} questões · {tm.cards} flashcards
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
