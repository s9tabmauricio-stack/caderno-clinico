// Fita de aviso âmbar e preta em volta do que cai na prova (questão ou flashcard), com "PROVA" escrito em cima e embaixo
export function FaixaProva({ ligada, children }: { ligada: boolean; children: React.ReactNode }) {
  if (!ligada) return <>{children}</>
  const fita = (
    <div className="fita" aria-hidden="true">
      <span>{Array.from({ length: 12 }, () => 'PROVA').join(' • ')}</span>
    </div>
  )
  return (
    <div className="fita-prova" role="group" aria-label="Cai na prova">
      {fita}
      {children}
      {fita}
    </div>
  )
}
