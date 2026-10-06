'use client'

export default function Erro({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <main className="wrap">
      <div className="centro view">
        <h1>Não foi possível carregar</h1>
        <p>Confira sua conexão com a internet e tente de novo.</p>
        <button className="btn" onClick={() => reset()}>
          Tentar de novo
        </button>
      </div>
    </main>
  )
}
