'use client'

import { useCallback, useRef, useSyncExternalStore } from 'react'
import { CHAVE_NOVIDADES, dataNovidade, type Novidade } from '@/lib/novidades'

// O que o aluno já viu fica guardado neste aparelho (lista de ids, em localStorage).
const ouvintes = new Set<() => void>()
function assinar(avisar: () => void) {
  ouvintes.add(avisar)
  return () => ouvintes.delete(avisar)
}
function vistas(): string[] {
  try {
    return JSON.parse(localStorage.getItem(CHAVE_NOVIDADES) ?? '[]')
  } catch {
    return []
  }
}
// Guarda os ids da lista atual (as apagadas saem da memória do aparelho)
function marcarVistas(lista: Novidade[]) {
  try {
    localStorage.setItem(CHAVE_NOVIDADES, JSON.stringify(lista.map((n) => n.id)))
  } catch {
    // aba anônima: a bolinha volta na próxima visita
  }
  ouvintes.forEach((f) => f())
}

const sino = (
  <svg viewBox="0 0 24 24" aria-hidden="true">
    <path d="M6 16.5V11a6 6 0 0 1 12 0v5.5l1.5 2H4.5z" />
    <path d="M10 20.5a2 2 0 0 0 4 0" />
  </svg>
)

/** Sininho de Novidades ao lado da engrenagem; bolinha piscando até o aluno abrir. */
export function Novidades({ lista }: { lista: Novidade[] }) {
  // Quantas ainda não foram vistas (no servidor, nenhuma: a bolinha aparece só no aparelho)
  const naoVistas = useCallback(() => {
    const v = vistas()
    return lista.filter((n) => !v.includes(n.id)).length
  }, [lista])
  const novas = useSyncExternalStore(assinar, naoVistas, () => 0)
  const painel = useRef<HTMLDialogElement>(null)
  if (lista.length === 0) return null
  return (
    <>
      <button
        type="button"
        className={`avatar engrenagem novidades${novas ? ' tem' : ''}`}
        aria-label={novas ? `Novidades: ${novas} para ver` : 'Novidades'}
        title="Novidades"
        onClick={() => {
          painel.current?.showModal()
          marcarVistas(lista)
        }}
      >
        {sino}
        {novas > 0 && <span className="bd">{novas}</span>}
      </button>
      <dialog ref={painel} className="nov-painel" aria-label="Novidades" onClick={(e) => e.target === e.currentTarget && painel.current?.close()}>
        <div className="nov-caixa">
          <div className="nov-topo">
            <h2>Novidades</h2>
            <button type="button" className="nov-fechar" onClick={() => painel.current?.close()} aria-label="Fechar">
              ×
            </button>
          </div>
          <ul>
            {lista.map((n) => (
              <li key={n.id}>
                <span className="nov-data">{dataNovidade(n.criado_em)}</span>
                <strong>{n.titulo}</strong>
                <p>{n.texto}</p>
              </li>
            ))}
          </ul>
        </div>
      </dialog>
    </>
  )
}
