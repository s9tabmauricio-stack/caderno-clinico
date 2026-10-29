'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

const destinos = [
  ['/admin/central', 'Central'],
  ['/admin/recados', 'Recados da turma'],
  ['/admin', 'Alunos'],
  ['/admin/conteudo', 'Conteúdo'],
  ['/admin/agenda', 'Agenda da semana'],
] as const

export function NavegacaoAdmin() {
  const caminho = usePathname()
  if (caminho !== '/admin' && !caminho.startsWith('/admin/')) return null
  return (
    <nav className="filtro-barra nav-admin" aria-label="Administração">
      {destinos.map(([href, nome]) => (
        <Link key={href} className="pill" href={href}
          aria-current={caminho === href || (href !== '/admin' && caminho.startsWith(`${href}/`)) ? 'page' : undefined}>
          {nome}
        </Link>
      ))}
    </nav>
  )
}
