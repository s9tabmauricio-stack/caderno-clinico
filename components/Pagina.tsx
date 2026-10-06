import Link from 'next/link'
import { TabBar } from './TabBar'
import { Icone } from './Icones'

// Moldura comum das telas logadas: conteúdo + barra de abas
export function Pagina({ pendentes, children }: { pendentes: number; children: React.ReactNode }) {
  return (
    <>
      <main className="wrap">
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
