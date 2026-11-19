// Fita de aviso em volta do que cai na prova (questão ou flashcard), com "PROVA" escrito em cima e embaixo.
// Âmbar e preta por padrão; vermelha e preta quando o professor disse que cai (corFaixaProva em lib/faixa-prova.ts).
export function FaixaProva({
  ligada,
  vermelha = false,
  children,
}: {
  ligada: boolean
  vermelha?: boolean
  children: React.ReactNode
}) {
  if (!ligada) return <>{children}</>
  const fita = (
    <div className="fita" aria-hidden="true">
      <span>{Array.from({ length: 12 }, () => 'PROVA').join(' • ')}</span>
    </div>
  )
  return (
    <div
      className={`fita-prova${vermelha ? ' fita-prova--professor' : ''}`}
      role="group"
      aria-label={vermelha ? 'O professor disse que cai na prova' : 'Cai na prova'}
    >
      {fita}
      {children}
      {fita}
    </div>
  )
}
