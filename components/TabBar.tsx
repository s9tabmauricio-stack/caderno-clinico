'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Icone } from './Icones'

const ABAS = [
  { href: '/', chave: 'inicio', rotulo: 'Início', icone: Icone.inicio },
  { href: '/revisao', chave: 'revisao', rotulo: 'Revisão', icone: Icone.cards },
  { href: '/desempenho', chave: 'desempenho', rotulo: 'Desempenho', icone: Icone.grafico },
  { href: '/perfil', chave: 'perfil', rotulo: 'Perfil', icone: Icone.pessoa },
] as const

export function TabBar({ pendentes }: { pendentes: number }) {
  const caminho = usePathname()
  const ativa = caminho.startsWith('/revisao')
    ? 'revisao'
    : caminho.startsWith('/desempenho')
      ? 'desempenho'
      : caminho.startsWith('/perfil')
        ? 'perfil'
        : 'inicio'

  return (
    <nav className="tabbar" aria-label="Navegação principal">
      {ABAS.map((a) => (
        <Link
          key={a.chave}
          href={a.href}
          className={`tab ${ativa === a.chave ? 'on' : ''}`}
          aria-current={ativa === a.chave ? 'page' : undefined}
        >
          {a.icone}
          <span>{a.rotulo}</span>
          {a.chave === 'revisao' && pendentes > 0 && (
            <span className="badge" aria-label={`${pendentes} para revisar`}>
              {pendentes}
            </span>
          )}
        </Link>
      ))}
    </nav>
  )
}
