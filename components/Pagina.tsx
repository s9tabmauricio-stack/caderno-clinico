import Link from 'next/link'
import { TabBar } from './TabBar'
import { Icone } from './Icones'
import { sessao } from '@/lib/dados'
import { ehAdmin } from '@/lib/admin'

/** Recados da turma ainda não vistos (só conta para o administrador). */
export async function recadosNovos() {
  const { supabase, email } = await sessao()
  if (!ehAdmin(email)) return 0
  const { count } = await supabase.from('recados').select('id', { count: 'exact', head: true }).eq('status', 'novo')
  return count ?? 0
}

// Moldura comum das telas logadas: engrenagem do perfil no canto, conteúdo e barra de abas
export async function Pagina({ pendentes, children }: { pendentes: number; children: React.ReactNode }) {
  const novos = await recadosNovos()
  return (
    <>
      <main className="wrap">
        <Link
          className="avatar engrenagem"
          href="/perfil"
          aria-label={novos ? `Configurações, ${novos} ${novos === 1 ? 'recado novo' : 'recados novos'} da turma` : 'Configurações'}
        >
          {Icone.engrenagem}
          {novos > 0 && <span className="bd">{novos > 99 ? '99+' : novos}</span>}
        </Link>
        <div className="view">{children}</div>
      </main>
      <TabBar pendentes={pendentes} />
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
