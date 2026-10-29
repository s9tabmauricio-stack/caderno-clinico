'use client'

import Link from 'next/link'
import { useSearchParams } from 'next/navigation'
import { retornoSeguro } from '@/lib/navegacao'

type Aba = 'aulas' | 'banco' | 'flashcards'

/** Seções da matéria, iguais nas três telas: as aulas, o banco de questões e os flashcards (só aparecem as que têm conteúdo). */
export function AbasMateria({
  id,
  ativa,
  totalQuestoes,
  totalCards,
}: {
  id: string
  ativa: Aba
  totalQuestoes: number
  totalCards: number
}) {
  const parametros = useSearchParams()
  const retorno = retornoSeguro(parametros.get('retorno')) ?? (parametros.get('de') === 'desempenho' ? '/desempenho' : null)
  const abas: [Aba, string, string, number | null][] = [
    ['aulas', `/materia/${id}`, 'Aulas', null],
    ['banco', `/materia/${id}/questoes`, 'Banco de questões', totalQuestoes],
    ['flashcards', `/materia/${id}/flashcards`, 'Flashcards', totalCards],
  ]
  const visiveis = abas.filter(([chave, , , total]) => chave === ativa || total === null || total > 0)
  if (visiveis.length < 2) return null

  return (
    <nav className="segm segm-nav" aria-label="Seções da matéria">
      {visiveis.map(([chave, href, rotulo, total]) => (
        <Link key={chave} href={retorno ? `${href}?${new URLSearchParams({ retorno })}` : href} className={ativa === chave ? 'on' : ''} aria-current={ativa === chave ? 'page' : undefined}>
          {rotulo} {total !== null && <small>{total}</small>}
        </Link>
      ))}
    </nav>
  )
}
