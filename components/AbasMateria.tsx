import Link from 'next/link'

/** Duas seções da matéria, iguais nas duas telas: as aulas e o banco de questões. */
export function AbasMateria({ id, ativa, totalQuestoes }: { id: string; ativa: 'aulas' | 'banco'; totalQuestoes: number }) {
  return (
    <nav className="segm segm-nav" aria-label="Seções da matéria">
      <Link href={`/materia/${id}`} className={ativa === 'aulas' ? 'on' : ''} aria-current={ativa === 'aulas' ? 'page' : undefined}>
        Aulas
      </Link>
      <Link
        href={`/materia/${id}/questoes`}
        className={ativa === 'banco' ? 'on' : ''}
        aria-current={ativa === 'banco' ? 'page' : undefined}
      >
        Banco de questões <small>{totalQuestoes}</small>
      </Link>
    </nav>
  )
}
