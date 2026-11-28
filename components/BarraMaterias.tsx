import Link from 'next/link'
import type { Materia } from '@/lib/dados'
import { linkMateria, type SecaoMateria } from '@/lib/navegacao'
import { rotuloPeriodo } from '@/lib/periodos'

/** O que carregarMateriasPorProva devolve: as matérias da turma, cada uma com o período, e os períodos. */
export type MateriasDaBarra = {
  materias: (Pick<Materia, 'id' | 'nome'> & { periodo: number | null })[]
  periodos: number[]
  atual: number | null
}

/** Seletor de períodos (só aparece com mais de um); cada um abre a primeira matéria daquele período. */
export function SeletorPeriodos({ periodos, ativo }: { periodos: number[]; ativo: number | null }) {
  if (periodos.length < 2) return null
  return (
    <nav className="segm segm-materias segm-periodos" aria-label="Períodos do curso">
      {periodos.map((p) => (
        <Link
          key={p}
          href={`/estudar?periodo=${p}`}
          className={p === ativo ? 'on' : undefined}
          aria-current={p === ativo ? 'page' : undefined}
        >
          {rotuloPeriodo(p)}
        </Link>
      ))}
    </nav>
  )
}

export function BarraMaterias({ id, nome, materias, secao, retorno }: {
  id: string
  nome: string
  materias: MateriasDaBarra
  secao: SecaoMateria
  retorno?: string | null
}) {
  // A barra mostra só as matérias do período da matéria aberta
  const periodo = materias.materias.find((m) => m.id === id)?.periodo ?? materias.atual
  const lista = materias.materias.filter((m) => m.periodo === periodo)
  return (
    <>
      <h1 className="materia-titulo-acessivel">{nome}</h1>
      <SeletorPeriodos periodos={materias.periodos} ativo={periodo} />
      <nav className="segm segm-materias" aria-label="Matérias por ordem da próxima prova">
        {lista.map((materia) => (
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
