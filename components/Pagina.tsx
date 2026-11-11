import Link from 'next/link'
import { TabBar } from './TabBar'
import { NavegacaoAdmin } from './NavegacaoAdmin'
import { Icone } from './Icones'
import { TemaRapido } from './TemaEscolha'
import { carregarProgresso, pendentes as contarPendentes, sessao } from '@/lib/dados'
import { ehAdmin } from '@/lib/admin'

/** Recados da turma ainda não vistos (só conta para o administrador). */
export async function recadosNovos() {
  const { supabase, email } = await sessao()
  if (!ehAdmin(email)) return 0
  const { count } = await supabase.from('recados').select('id', { count: 'exact', head: true }).eq('status', 'novo')
  return count ?? 0
}

/** Flashcards para revisar hoje (o número do selo da aba Revisão). */
async function revisoesDeHoje() {
  const { supabase } = await sessao()
  return contarPendentes(await carregarProgresso(supabase)).hoje
}

// Moldura comum das telas logadas: Auto | Dia | Noite e engrenagem do perfil no canto, conteúdo e barra de abas.
// Sem `pendentes`, a própria moldura conta as revisões (as telas de administração não precisam calcular).
// `larga`: telas de estudo, que no tablet deitado usam mais largura (o resto fica numa coluna só).
export async function Pagina({ pendentes, larga, children }: { pendentes?: number; larga?: boolean; children: React.ReactNode }) {
  const [novos, revisoes, { email }] = await Promise.all([recadosNovos(), pendentes ?? revisoesDeHoje(), sessao()])
  return (
    <>
      <main className={`wrap${larga ? ' larga' : ''}`}>
        <nav className="atalhos-globais" aria-label="Conta e administração">
          {ehAdmin(email) && (
            <>
              <Link className="pill" href="/admin/central">Administração</Link>
              <Link className="pill" href="/admin/recados">
                Recados <span className="cnt" aria-label={`${novos} novos`}>{novos}</span>
              </Link>
            </>
          )}
          <TemaRapido />
          <Link className="avatar engrenagem" href="/perfil" aria-label="Configurações" title="Configurações">
            {Icone.engrenagem}
          </Link>
        </nav>
        {ehAdmin(email) && <NavegacaoAdmin />}
        <div className="view">{children}</div>
      </main>
      <TabBar pendentes={revisoes} />
    </>
  )
}

export function Voltar({ href, rotulo }: { href: string; rotulo: string }) {
  return (
    <Link className="back" href={href}>
      {Icone.voltar}
      <span>{rotulo}</span>
    </Link>
  )
}
