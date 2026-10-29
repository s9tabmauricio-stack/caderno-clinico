import type { Metadata } from 'next'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { Pagina, Voltar } from '@/components/Pagina'
import { Icone } from '@/components/Icones'
import { LimparVersoes } from '@/components/admin/Editores'
import { chaveConfigurada, clienteAdmin, ehAdmin } from '@/lib/admin'
import { sessao } from '@/lib/dados'

export const metadata: Metadata = { title: 'Conteúdo' }

type Materia = { id: string; nome: string; descricao: string | null; cor_inicio: string | null; cor_fim: string | null }
type Aula = { id: string; materia_id: string; ordem: number; titulo: string; publicada: boolean }
type Questao = { materia_id: string; aula_id: string | null; substituida_por: string | null }
type Card = { aula_id: string }

type Situacao = 'completa' | 'sem-cards' | 'sem-questoes' | 'so-apostila'
const SITUACAO: Record<Situacao, string> = {
  completa: 'Completa',
  'sem-cards': 'Falta flashcards',
  'sem-questoes': 'Falta questões',
  'so-apostila': 'Só apostila',
}

function situacao(nQ: number, nC: number): Situacao {
  if (nQ > 0 && nC > 0) return 'completa'
  if (nQ > 0) return 'sem-cards'
  if (nC > 0) return 'sem-questoes'
  return 'so-apostila'
}

const plural = (n: number, um: string, varios: string) => `${n} ${n === 1 ? um : varios}`

// Resumo do que está no ar (por matéria e por aula) e porta para editar aulas, questões e flashcards
export default async function ConteudoPage() {
  const { email } = await sessao()
  if (!ehAdmin(email)) notFound()
  if (!chaveConfigurada()) {
    return (
      <Pagina>
        <Voltar href="/admin/central" rotulo="Administração" />
        <p className="vazio">Falta a chave secreta do Supabase na Vercel (SUPABASE_SECRET_KEY).</p>
      </Pagina>
    )
  }
  const admin = await clienteAdmin()
  const [{ data: materias }, { data: aulas }, { data: questoes }, { data: cards }] = await Promise.all([
    admin.from('materias').select('id, nome, descricao, cor_inicio, cor_fim').order('ordem'),
    admin.from('aulas').select('id, materia_id, ordem, titulo, publicada').order('ordem'),
    admin.from('questoes').select('materia_id, aula_id, substituida_por'),
    admin.from('flashcards').select('aula_id'),
  ])
  const ms = (materias ?? []) as Materia[]
  const todasAulas = (aulas ?? []) as Aula[]
  const todasQuestoes = (questoes ?? []) as Questao[]
  const cs = (cards ?? []) as Card[]

  // Versões antigas de questões corrigidas não aparecem para os alunos e não entram nas contas
  const antigas = todasQuestoes.filter((q) => q.substituida_por).length
  const qs = todasQuestoes.filter((q) => !q.substituida_por)

  const qPorAula = new Map<string, number>()
  for (const q of qs) if (q.aula_id) qPorAula.set(q.aula_id, (qPorAula.get(q.aula_id) ?? 0) + 1)
  const cPorAula = new Map<string, number>()
  for (const c of cs) cPorAula.set(c.aula_id, (cPorAula.get(c.aula_id) ?? 0) + 1)

  // Só conta para os alunos o que está publicado (as visões escondem o resto)
  const publicadas = todasAulas.filter((a) => a.publicada)
  const idsPublicadas = new Set(publicadas.map((a) => a.id))
  const totalQ = qs.filter((q) => !q.aula_id || idsPublicadas.has(q.aula_id)).length
  const totalC = cs.filter((c) => idsPublicadas.has(c.aula_id)).length
  const sits = publicadas.map((a) => situacao(qPorAula.get(a.id) ?? 0, cPorAula.get(a.id) ?? 0))
  const completas = sits.filter((s) => s === 'completa').length
  const semQ = sits.filter((s) => s === 'sem-cards' || s === 'so-apostila').length
  const semC = sits.filter((s) => s === 'sem-questoes' || s === 'so-apostila').length
  const escondidas = todasAulas.length - publicadas.length

  return (
    <Pagina>
      <Voltar href="/admin/central" rotulo="Administração" />
      <header className="top">
        <div>
          <div className="eyebrow">Administração</div>
          <h1 className="big">Conteúdo</h1>
        </div>
      </header>

      {antigas > 0 && (
        <>
          <div className="sec">Limpeza</div>
          <div className="ed-bloco">
            <p style={{ margin: 0 }}>
              Há {antigas} {antigas === 1 ? 'versão antiga de questão corrigida' : 'versões antigas de questões corrigidas'}. Elas não
              aparecem para os alunos.
            </p>
            <LimparVersoes total={antigas} />
          </div>
        </>
      )}

      <div className="stats">
        <div className="stat">
          <div className="lab">Aulas no ar</div>
          <div className="n">{publicadas.length}</div>
        </div>
        <div className="stat">
          <div className="lab">Questões</div>
          <div className="n">{totalQ}</div>
        </div>
        <div className="stat">
          <div className="lab">Flashcards</div>
          <div className="n">{totalC}</div>
        </div>
        <div className="stat">
          <div className="lab">Completas</div>
          <div className="n ok">
            {completas}
            <small> de {publicadas.length}</small>
          </div>
        </div>
        <div className="stat">
          <div className="lab">Sem questões</div>
          <div className={`n${semQ ? ' alerta' : ''}`}>{semQ}</div>
        </div>
        <div className="stat">
          <div className="lab">Sem flashcards</div>
          <div className={`n${semC ? ' alerta' : ''}`}>{semC}</div>
        </div>
      </div>
      <p className="painel-nota">
        “Completa” = aula com apostila, questões e flashcards.
        {escondidas > 0 && ` ${plural(escondidas, 'aula escondida não entra', 'aulas escondidas não entram')} nos totais.`}
      </p>

      <div className="legend painel-legenda">
        <span><i className="sit-completa" />Completa</span>
        <span><i className="sit-parcial" />Falta questões ou flashcards</span>
        <span><i className="sit-so-apostila" />Só apostila</span>
      </div>

      {ms.map((m) => {
        const aulasM = todasAulas.filter((a) => a.materia_id === m.id)
        const pubM = aulasM.filter((a) => a.publicada)
        const qM = qs.filter((q) => q.materia_id === m.id && (!q.aula_id || idsPublicadas.has(q.aula_id))).length
        const todasQM = qs.filter((q) => q.materia_id === m.id).length
        const bancoM = qs.filter((q) => q.materia_id === m.id && !q.aula_id).length
        const cM = pubM.reduce((s, a) => s + (cPorAula.get(a.id) ?? 0), 0)
        const sitM = pubM.map((a) => situacao(qPorAula.get(a.id) ?? 0, cPorAula.get(a.id) ?? 0))
        const nComp = sitM.filter((s) => s === 'completa').length
        const nSo = sitM.filter((s) => s === 'so-apostila').length
        const nParc = sitM.length - nComp - nSo
        const pct = (n: number) => `${sitM.length ? (n / sitM.length) * 100 : 0}%`
        return (
          <section
            key={m.id}
            className="painel-m"
            style={{ '--c1': m.cor_inicio ?? '#4FDDFF', '--c2': m.cor_fim ?? '#9B7BFF' } as React.CSSProperties}
          >
            <div className="painel-h">
              <span className="pdot" />
              <span className="main">
                <span className="t">{m.nome}</span>
                {m.descricao && <span className="s">{m.descricao}</span>}
              </span>
            </div>
            <div className="painel-nums">
              <span><b>{pubM.length}</b> {pubM.length === 1 ? 'aula' : 'aulas'}</span>
              <span><b>{qM}</b> questões</span>
              <span><b>{cM}</b> flashcards</span>
            </div>
            {sitM.length > 0 && (
              <div className="bar" role="img" aria-label={`${nComp} completas, ${nParc} parciais, ${nSo} só com apostila`}>
                <span className="sit-completa" style={{ width: pct(nComp) }} />
                <span className="sit-parcial" style={{ width: pct(nParc) }} />
                <span className="sit-so-apostila" style={{ width: pct(nSo) }} />
              </div>
            )}

            <div className="painel-aulas">
              {aulasM.length === 0 && <p className="painel-vazio">Nenhuma aula cadastrada.</p>}
              {aulasM.map((a) => {
                const nQ = qPorAula.get(a.id) ?? 0
                const nC = cPorAula.get(a.id) ?? 0
                const sit = situacao(nQ, nC)
                return (
                  <Link key={a.id} className="painel-a" href={`/admin/conteudo/aula/${a.id}`}>
                    <span className="num">{a.ordem}</span>
                    <span className="main">
                      <span className="t">{a.titulo}</span>
                      <span className="meta">
                        <span className={`qtd${nQ ? '' : ' zero'}`}>{plural(nQ, 'questão', 'questões')}</span>
                        <span className={`qtd${nC ? '' : ' zero'}`}>{plural(nC, 'flashcard', 'flashcards')}</span>
                        {a.publicada ? (
                          <span className={`chip sit sit-${sit === 'sem-cards' || sit === 'sem-questoes' ? 'parcial' : sit}`}>
                            {SITUACAO[sit]}
                          </span>
                        ) : (
                          <span className="chip novo">Escondida</span>
                        )}
                      </span>
                    </span>
                    {Icone.seta}
                  </Link>
                )
              })}
              {todasQM > 0 && (
                <Link className="painel-a" href={`/admin/conteudo/questoes/${m.id}`}>
                  <span className="num banco">B</span>
                  <span className="main">
                    <span className="t">Banco de questões</span>
                    <span className="meta">
                      <span className="qtd">{plural(todasQM, 'questão', 'questões')}</span>
                      {bancoM > 0 && <span className="qtd">{plural(bancoM, 'sem aula definida', 'sem aula definida')}</span>}
                    </span>
                  </span>
                  {Icone.seta}
                </Link>
              )}
            </div>
          </section>
        )
      })}
    </Pagina>
  )
}
