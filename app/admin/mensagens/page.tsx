import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import { Pagina, Voltar } from '@/components/Pagina'
import { Apagar } from '@/components/admin/Editores'
import { chaveConfigurada, clienteAdmin, ehAdmin } from '@/lib/admin'
import { sessao } from '@/lib/dados'
import { fmtHa } from '@/lib/recados'
import type { Mensagem } from '@/lib/mensagens'
import { apagarMensagem, marcarMensagem, marcarTodasLidas } from './acoes'

export const metadata: Metadata = { title: 'Mensagens' }

function Marcar({ id, status, rotulo, principal }: { id: string; status: string; rotulo: string; principal?: boolean }) {
  return (
    <form action={marcarMensagem}>
      <input type="hidden" name="id" value={id} />
      <input type="hidden" name="status" value={status} />
      <button className={`btn sm${principal ? '' : ' ghost'}`} type="submit">
        {rotulo}
      </button>
    </form>
  )
}

export default async function MensagensPage() {
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
  const { data } = await (await clienteAdmin())
    .from('mensagens')
    .select('id, user_id, autor, texto, status, criado_em')
    .order('criado_em', { ascending: false })
    .limit(500)
  const mensagens = (data ?? []) as Mensagem[]
  const novas = mensagens.filter((m) => m.status === 'nova').length

  return (
    <Pagina>
      <Voltar href="/admin/central" rotulo="Administração" />
      <header className="top">
        <div>
          <div className="eyebrow">Administração</div>
          <h1 className="big">Mensagens</h1>
          <p className="lead">O que os alunos mandam pelo balão do topo. Só você lê; o aluno vê quando você marca como lida.</p>
        </div>
      </header>

      {novas > 1 && (
        <form action={marcarTodasLidas} className="marcar-todos">
          <button className="btn ghost sm" type="submit">
            Marcar as {novas} como lidas
          </button>
        </form>
      )}

      {mensagens.length ? (
        mensagens.map((m) => (
          <article key={m.id} className={`recado${m.status === 'nova' ? ' novo' : ''}`}>
            <div className="mh">
              {m.status === 'nova' && <span className="dotn" aria-label="Nova" />}
              <span className="tag ins">✉️ {m.autor}</span>
              <span className="when">{fmtHa(m.criado_em)}</span>
              {m.status === 'lida' && <span className="situacao ok">✓ Lida</span>}
            </div>
            <p className="mt">{m.texto}</p>
            <div className="bt">
              {m.status === 'nova' ? (
                <Marcar id={m.id} status="lida" rotulo="Marcar como lida" principal />
              ) : (
                <Marcar id={m.id} status="nova" rotulo="Marcar como nova" />
              )}
              <Apagar acao={apagarMensagem} id={m.id} aviso="Apaga a mensagem (o aluno também deixa de vê-la)." />
            </div>
          </article>
        ))
      ) : (
        <p className="vazio">Nenhuma mensagem ainda. Quando um aluno tocar no balão do topo e escrever, aparece aqui.</p>
      )}
    </Pagina>
  )
}
