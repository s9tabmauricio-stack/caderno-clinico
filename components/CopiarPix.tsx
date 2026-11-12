'use client'

import { useState } from 'react'

// Botão que copia a chave Pix (campanha da Baunilha, no Início)
export function CopiarPix({ chave }: { chave: string }) {
  const [copiado, setCopiado] = useState(false)
  async function copiar() {
    try {
      await navigator.clipboard.writeText(chave)
      setCopiado(true)
      setTimeout(() => setCopiado(false), 2500)
    } catch {
      window.prompt('Copie a chave Pix:', chave)
    }
  }
  return (
    <button type="button" className="btn ghost" onClick={copiar}>
      {copiado ? '✓ Chave Pix copiada' : 'Copiar chave Pix'}
    </button>
  )
}
