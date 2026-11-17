import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import { Pagina, Voltar } from '@/components/Pagina'
import { AdminNovidades } from '@/components/AdminNovidades'
import { chaveConfigurada, ehAdmin } from '@/lib/admin'
import { sessao } from '@/lib/dados'
import { dataNovidade, lerNovidades } from '@/lib/novidades'
import { apagarNovidade } from './acoes'

export const metadata: Metadata = { title: 'Novidades' }

export default async function AdminNovidadesPage() {
  const { supabase, email } = await sessao()
  if (!ehAdmin(email)) notFound()
  const lista = await lerNovidades(supabase, 50)

  return (
    <Pagina>
      <Voltar href="/admin/central" rotulo="Administração" />
      <header className="top">
        <div>
          <div className="eyebrow">Administração</div>
          <h1 className="big">Novidades</h1>
        </div>
      </header>
      {chaveConfigurada() ? (
        <>
          <p className="foot" style={{ marginTop: 0, marginBottom: 12 }}>
            O que você publicar aqui aparece no sininho ao lado da engrenagem, com a bolinha piscando até cada aluno abrir. O
            sininho mostra as 15 mais recentes.
          </p>
          <AdminNovidades />
          {lista.length > 0 && (
            <>
              <div className="sec">Publicadas</div>
              <div className="group">
                {lista.map((n) => (
                  <div key={n.id} className="row static">
                    <span className="main">
                      <span className="t">{n.titulo}</span>
                      <span className="s">
                        {dataNovidade(n.criado_em)} · {n.texto}
                      </span>
                    </span>
                    <form action={apagarNovidade}>
                      <input type="hidden" name="id" value={n.id} />
                      <button className="pill" type="submit" aria-label={`Apagar a novidade ${n.titulo}`}>
                        Apagar
                      </button>
                    </form>
                  </div>
                ))}
              </div>
            </>
          )}
        </>
      ) : (
        <p className="vazio">Falta a chave secreta do Supabase na Vercel (SUPABASE_SECRET_KEY).</p>
      )}
    </Pagina>
  )
}
