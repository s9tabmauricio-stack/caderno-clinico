import type { Metadata } from 'next'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { Pagina, Voltar } from '@/components/Pagina'
import { Icone } from '@/components/Icones'
import { LimparVersoes } from '@/components/admin/Editores'
import { chaveConfigurada, clienteAdmin, ehAdmin } from '@/lib/admin'
import { sessao } from '@/lib/dados'

export const metadata: Metadata = { title: 'Conteúdo' }

type Linha = { id: string; aula_id?: string | null; materia_id?: string; substituida_por?: string | null }

export default async function ConteudoPage() {
  const { email } = await sessao()
  if (!ehAdmin(email)) notFound()
  if (!chaveConfigurada()) {
    return (
      <Pagina pendentes={0}>
        <Voltar href="/perfil" rotulo="Perfil" />
        <p className="vazio">Falta a chave secreta do Supabase na Vercel (SUPABASE_SECRET_KEY).</p>
      </Pagina>
    )
  }
  const admin = await clienteAdmin()
  const [{ data: materias }, { data: aulas }, { data: questoes }, { data: cards }] = await Promise.all([
    admin.from('materias').select('id, nome').order('ordem'),
    admin.from('aulas').select('id, materia_id, ordem, titulo, publicada').order('ordem'),
    admin.from('questoes').select('id, materia_id, aula_id, substituida_por'),
    admin.from('flashcards').select('id, aula_id'),
  ])
  const qs = (questoes ?? []) as Linha[]
  const antigas = qs.filter((q) => q.substituida_por).length
  const ativas = qs.filter((q) => !q.substituida_por)

  return (
    <Pagina pendentes={0}>
      <Voltar href="/perfil" rotulo="Perfil" />
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

      {(materias ?? []).map((m: { id: string; nome: string }) => {
        const aulasM = (aulas ?? []).filter((a: { materia_id: string }) => a.materia_id === m.id)
        const totalQ = ativas.filter((q) => q.materia_id === m.id).length
        return (
          <section key={m.id}>
            <div className="sec">{m.nome}</div>
            <div className="group">
              <Link className="row" href={`/admin/conteudo/questoes/${m.id}`}>
                <span className="main">
                  <span className="t">Banco de questões</span>
                  <span className="s">{totalQ} questões</span>
                </span>
                {Icone.seta}
              </Link>
              {aulasM.map((a: { id: string; ordem: number; titulo: string; publicada: boolean }) => {
                const nQ = ativas.filter((q) => q.aula_id === a.id).length
                const nC = (cards ?? []).filter((c: Linha) => c.aula_id === a.id).length
                return (
                  <Link key={a.id} className="row" href={`/admin/conteudo/aula/${a.id}`}>
                    <span className="num">{a.ordem}</span>
                    <span className="main">
                      <span className="t">{a.titulo}</span>
                      <span className="s">
                        {a.publicada ? 'Publicada' : 'Escondida'} · {nQ} questões · {nC} flashcards
                      </span>
                    </span>
                    {Icone.seta}
                  </Link>
                )
              })}
            </div>
          </section>
        )
      })}
    </Pagina>
  )
}
