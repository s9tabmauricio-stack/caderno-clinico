'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Icone } from './Icones'

const ABAS = [
  { href: '/', chave: 'inicio', rotulo: 'Início', icone: Icone.inicio },
  { href: '/agenda', chave: 'agenda', rotulo: 'Agenda', icone: Icone.agenda },
  { href: '/estudar', chave: 'estudar', rotulo: 'Matérias', icone: Icone.estudar },
  { href: '/revisao', chave: 'revisao', rotulo: 'Revisão', icone: Icone.cards },
  { href: '/desempenho', chave: 'desempenho', rotulo: 'Desempenho', icone: Icone.grafico },
] as const

export function TabBar({ pendentes }: { pendentes: number }) {
  const caminho = usePathname()
  const ativa = caminho.startsWith('/agenda')
    ? 'agenda'
    : caminho.startsWith('/estudar') || caminho.startsWith('/materia') || caminho.startsWith('/aula')
    ? 'estudar'
    : caminho.startsWith('/revisao')
    ? 'revisao'
    : caminho.startsWith('/desempenho')
      ? 'desempenho'
      : caminho.startsWith('/perfil') || caminho.startsWith('/admin')
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
