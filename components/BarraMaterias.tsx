import Link from 'next/link'
import type { Materia } from '@/lib/dados'
import { linkMateria, type SecaoMateria } from '@/lib/navegacao'

export function BarraMaterias({ id, nome, materias, secao, retorno }: {
  id: string
  nome: string
  materias: Pick<Materia, 'id' | 'nome'>[]
  secao: SecaoMateria
  retorno?: string | null
}) {
  return (
    <>
      <h1 className="materia-titulo-acessivel">{nome}</h1>
      <nav className="segm segm-materias" aria-label="Matérias por ordem da próxima prova">
        {materias.map((materia) => (
          <Link
            key={materia.id}
            href={linkMateria(materia.id, secao, retorno)}
            className={materia.id === id ? 'on' : undefined}
            aria-current={materia.id === id ? 'page' : undefined}
          >
            {materia.nome}
          </Link>
        ))}
      </nav>
    </>
  )
}
