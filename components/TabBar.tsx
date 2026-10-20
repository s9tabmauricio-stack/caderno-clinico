'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

const ic = (d: React.ReactNode) => (
  <svg viewBox="0 0 24 24" aria-hidden="true">
    {d}
  </svg>
)

// Ícones de traço fino, iguais aos da proposta visual-v4
const ABAS = [
  { href: '/', chave: 'inicio', rotulo: 'Início', icone: ic(<path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z" />) },
  {
    href: '/agenda',
    chave: 'agenda',
    rotulo: 'Agenda',
    icone: ic(
      <>
        <rect x="3" y="5" width="18" height="16" rx="2" />
        <path d="M16 3v4M8 3v4M3 10h18" />
      </>,
    ),
  },
  {
    href: '/estudar',
    chave: 'estudar',
    rotulo: 'Estudar',
    icone: ic(
      <>
        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z" />
        <path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5" />
      </>,
    ),
  },
  {
    href: '/revisao',
    chave: 'revisao',
    rotulo: 'Revisão',
    icone: ic(
      <>
        <rect x="3" y="6" width="14" height="14" rx="2" />
        <path d="M7 3h12a2 2 0 0 1 2 2v12" />
      </>,
    ),
  },
  { href: '/desempenho', chave: 'desempenho', rotulo: 'Desempenho', icone: ic(<path d="M4 20V10M10 20V4M16 20v-7M22 20H2" />) },
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
