import type { Metadata } from 'next'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { Pagina, Voltar } from '@/components/Pagina'
import { Apagar } from '@/components/admin/Editores'
import { chaveConfigurada, clienteAdmin, ehAdmin } from '@/lib/admin'
import { sessao } from '@/lib/dados'
import { fmtHa, tituloRecado, type Recado } from '@/lib/recados'
import { apagarRecado, marcarRecado, marcarTodosVistos } from './acoes'

export const metadata: Metadata = { title: 'Recados da turma' }

const FILTROS = [
  { id: 'novos', rotulo: 'Novos' },
  { id: 'erros', rotulo: 'Erros abertos' },
  { id: 'insights', rotulo: 'Dicas' },
  { id: 'corrigidos', rotulo: 'Corrigidos' },
  { id: 'todos', rotulo: 'Todos' },
] as const
type Filtro = (typeof FILTROS)[number]['id']

const passa: Record<Filtro, (r: Recado) => boolean> = {
  novos: (r) => r.status === 'novo',
  erros: (r) => r.tipo === 'erro' && r.status !== 'corrigido',
  insights: (r) => r.tipo === 'insight',
  corrigidos: (r) => r.status === 'corrigido',
  todos: () => true,
}

type Questao = { id: string; enunciado: string; materia_id: string; aula_id: string | null }

function Marcar({ id, status, rotulo, principal }: { id: string; status: string; rotulo: string; principal?: boolean }) {
  return (
    <form action={marcarRecado}>
      <input type="hidden" name="id" value={id} />
      <input type="hidden" name="status" value={status} />
      <button className={`btn sm${principal ? '' : ' ghost'}`} type="submit">
        {rotulo}
      </button>
    </form>
  )
}

export default async function RecadosPage(props: PageProps<'/admin/recados'>) {
  const { f } = await props.searchParams
  const { email } = await sessao()
  if (!ehAdmin(email)) notFound()
  if (!chaveConfigurada()) {
    return (
      <Pagina pendentes={0}>
        <Voltar href="/perfil" rotulo="Configurações" />
        <p className="vazio">Falta a chave secreta do Supabase na Vercel (SUPABASE_SECRET_KEY).</p>
      </Pagina>
    )
  }
  const admin = await clienteAdmin()
  const { data } = await admin
    .from('recados')
    .select('id, questao_id, user_id, autor, tipo, texto, status, criado_em')
    .order('criado_em', { ascending: false })
    .limit(500)
  const recados = (data ?? []) as Recado[]
  const ids = [...new Set(recados.map((r) => r.questao_id))]
  const [{ data: qs }, { data: materias }, { data: aulas }] = await Promise.all([
    ids.length
      ? admin.from('questoes').select('id, enunciado, materia_id, aula_id').in('id', ids)
      : Promise.resolve({ data: [] as Questao[] }),
    admin.from('materias').select('id, nome'),
    admin.from('aulas').select('id, titulo'),
  ])
  const questao = new Map(((qs ?? []) as Questao[]).map((q) => [q.id, q]))
  const nomeMateria = new Map((materias ?? []).map((m: { id: string; nome: string }) => [m.id, m.nome]))
  const tituloAula = new Map((aulas ?? []).map((a: { id: string; titulo: string }) => [a.id, a.titulo]))

  const novos = recados.filter(passa.novos).length
  const filtro: Filtro = FILTROS.some((x) => x.id === f) ? (f as Filtro) : novos ? 'novos' : 'todos'
  const lista = recados.filter(passa[filtro])

  return (
    <Pagina pendentes={0}>
      <Voltar href="/perfil" rotulo="Configurações" />
      <header className="top">
        <div>
          <div className="eyebrow">Administração</div>
          <h1 className="big">Recados da turma</h1>
          <p className="lead">Dicas e avisos de erro que os alunos deixam embaixo das questões.</p>
        </div>
      </header>

      <nav className="filtros-rec" aria-label="Filtrar recados">
        {FILTROS.map((x) => (
          <Link key={x.id} href={`/admin/recados?f=${x.id}`} className={x.id === filtro ? 'on' : ''}>
            {x.rotulo} · {recados.filter(passa[x.id]).length}
          </Link>
        ))}
      </nav>

      {filtro === 'novos' && novos > 1 && (
        <form action={marcarTodosVistos} className="marcar-todos">
          <button className="btn ghost sm" type="submit">
            Marcar os {novos} como vistos
          </button>
        </form>
      )}

      {lista.length ? (
        lista.map((r) => {
          const q = questao.get(r.questao_id)
          const onde = q
            ? [nomeMateria.get(q.materia_id), q.aula_id ? tituloAula.get(q.aula_id) : 'Banco de questões'].filter(Boolean).join(' · ')
            : 'Questão apagada'
          const link = q
            ? `/admin/conteudo/questoes/${q.materia_id}?${q.aula_id ? `aula=${q.aula_id}&` : ''}q=${encodeURIComponent(q.id)}#q-${q.id}`
            : null
          return (
            <article key={r.id} className={`recado${r.status === 'novo' ? ' novo' : ''}`}>
              <div className="mh">
                {r.status === 'novo' && <span className="dotn" aria-label="Novo" />}
                <span className={`tag ${r.tipo === 'erro' ? 'erro' : 'ins'}`}>
                  {r.tipo === 'erro' ? '⚠️' : '💡'} {tituloRecado(r)}
                </span>
                <span className="when">{fmtHa(r.criado_em)}</span>
                {r.status === 'corrigido' && <span className="situacao ok">✓ Corrigido</span>}
                {r.status === 'visto' && r.tipo === 'erro' && <span className="situacao vendo">Vendo</span>}
              </div>
              <p className="mt">{r.texto}</p>
              <span className="qref">
                <b>{onde}</b>
                {q && (
                  <>
                    <br />
                    {q.enunciado.slice(0, 140)}
                    {q.enunciado.length > 140 ? '…' : ''}
                  </>
                )}
              </span>
              <div className="bt">
                {r.tipo === 'erro' && r.status !== 'corrigido' && (
                  <Marcar id={r.id} status="corrigido" rotulo="Marcar como corrigido" principal />
                )}
                {r.status === 'novo' && <Marcar id={r.id} status="visto" rotulo={r.tipo === 'erro' ? 'Estou vendo' : 'Visto'} />}
                {r.status === 'corrigido' && <Marcar id={r.id} status="visto" rotulo="Reabrir" />}
                {link && (
                  <Link className="btn ghost sm" href={link}>
                    Abrir questão
                  </Link>
                )}
                <Apagar acao={apagarRecado} id={r.id} aviso="Apaga o recado para toda a turma." />
              </div>
            </article>
          )
        })
      ) : (
        <p className="vazio">
          {filtro === 'novos' ? 'Nenhum recado novo. Quando alguém deixar uma dica ou achar um erro, aparece aqui.' : 'Nada por aqui.'}
        </p>
      )}
    </Pagina>
  )
}
