'use client'

import { apagarNovidade } from '@/app/admin/novidades/acoes'

/** Botão Apagar da lista de novidades: pergunta antes, porque não tem volta. */
export function BotaoApagarNovidade({ id, titulo }: { id: string; titulo: string }) {
  return (
    <form
      action={apagarNovidade}
      onSubmit={(e) => {
        if (!confirm(`Apagar a novidade "${titulo}"? Ela some do sininho de toda a turma e não dá para desfazer.`)) e.preventDefault()
      }}
    >
      <input type="hidden" name="id" value={id} />
      <button className="pill" type="submit" aria-label={`Apagar a novidade ${titulo}`}>
        Apagar
      </button>
    </form>
  )
}
