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
  totais,
  totaisQuestoes,
} from '@/lib/dados'
import { plural, saudacao } from '@/lib/formato'

export const metadata: Metadata = { title: 'Início' }

export default async function Inicio() {
  const { supabase, userId, email } = await sessao()
  const [perfil, materias, progresso, banco] = await Promise.all([
    supabase.from('perfis').select('nome').eq('id', userId).maybeSingle(),
    carregarMaterias(supabase),
    carregarProgresso(supabase),
    carregarProgressoMaterias(supabase),
  ])

  const nome = perfil.data?.nome || email.split('@')[0] || 'aluno'
  const { texto, data } = saudacao()
  const pend = pendentes(progresso)
  const t = totais(progresso)
  const tq = totaisQuestoes(banco)
  const acerto = tq.respondidas ? `${Math.round((100 * tq.acertos) / tq.respondidas)}%` : '–'

  const ultima = progresso
    .filter((p) => p.ultima_atividade)
    .sort((a, b) => (b.ultima_atividade ?? '').localeCompare(a.ultima_atividade ?? ''))[0]
  const materiaDaUltima = ultima && materias.find((m) => m.id === ultima.materia_id)

  return (
    <Pagina pendentes={pend.hoje}>
      <header className="top">
        <div>
          <div className="eyebrow">{data}</div>
          <h1 className="big">
            {texto}, {nome}
          </h1>
        </div>
        <Link className="avatar" href="/perfil" aria-label="Abrir perfil">
          {nome.charAt(0).toUpperCase()}
        </Link>
      </header>

      <section className="review" aria-label="Revisão de hoje">
        <div className="review-k">Revisão de hoje</div>
        {pend.hoje > 0 ? (
          <>
            <div className="review-n">
              <span className="n">{pend.hoje}</span>
              <span className="u">{plural(pend.hoje, 'flashcard', 'flashcards')}</span>
            </div>
            <p className="review-s">
              {pend.vencidos} para revisar · {Math.min(pend.novos, pend.hoje - pend.vencidos)}{' '}
              {plural(pend.hoje - pend.vencidos, 'novo', 'novos')}
            </p>
            <Link className="btn-white" href="/revisao">
              Começar revisão
            </Link>
          </>
        ) : (
          <>
            <div className="review-n">
              <span className="u" style={{ fontSize: 26, letterSpacing: '-.02em' }}>
                Tudo em dia
              </span>
            </div>
            <p className="review-s">Nenhum card pendente por agora.</p>
          </>
        )}
      </section>

      {ultima && (
        <>
          <div className="sec">Continuar</div>
          <div className="group">
            <Link className="row" href={`/aula/${ultima.aula_id}`}>
              <span className="num">{ultima.ordem}</span>
              <span className="main">
                <span className="t">{ultima.titulo}</span>
                <span className="s">
                  {materiaDaUltima?.nome} · {concluido([ultima])}% concluído
                </span>
              </span>
              {Icone.seta}
            </Link>
          </div>
        </>
      )}

      <div className="sec">Matérias</div>
      {materias.length ? (
        <div className="tiles">
          {materias.map((m) => {
            const prog = progresso.filter((p) => p.materia_id === m.id)
            const tm = totais(prog)
            const pm = banco.find((b) => b.materia_id === m.id)
            const p = concluidoMateria(prog, pm)
            return (
              <Link
                key={m.id}
                className="mtile"
                href={`/materia/${m.id}`}
                style={{ '--c1': m.cor_inicio ?? '#0B5BD3', '--c2': m.cor_fim ?? '#3B4FC9' } as React.CSSProperties}
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
            )
          })}
        </div>
      ) : (
        <p className="vazio">Nenhuma matéria publicada ainda.</p>
      )}

      <div className="sec">Seu progresso</div>
      <div className="stats">
        <div className="stat">
          <div className="lab">Questões</div>
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
    </Pagina>
  )
}
