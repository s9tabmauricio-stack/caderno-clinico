import Link from 'next/link'
import { TabBar } from './TabBar'
import { Icone } from './Icones'
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

// Moldura comum das telas logadas: engrenagem do perfil no canto, conteúdo e barra de abas.
// Sem `pendentes`, a própria moldura conta as revisões (as telas de administração não precisam calcular).
// `larga`: telas de estudo, que no tablet deitado usam mais largura (o resto fica numa coluna só).
export async function Pagina({ pendentes, larga, children }: { pendentes?: number; larga?: boolean; children: React.ReactNode }) {
  const [novos, revisoes] = await Promise.all([recadosNovos(), pendentes ?? revisoesDeHoje()])
  return (
    <>
      <main className={`wrap${larga ? ' larga' : ''}`}>
        <Link
          className="avatar engrenagem"
          href={novos ? '/admin/recados' : '/perfil'}
          aria-label={novos ? `${novos} ${novos === 1 ? 'recado novo' : 'recados novos'} da turma` : 'Configurações'}
        >
          {Icone.engrenagem}
          {novos > 0 && <span className="bd">{novos > 99 ? '99+' : novos}</span>}
        </Link>
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
