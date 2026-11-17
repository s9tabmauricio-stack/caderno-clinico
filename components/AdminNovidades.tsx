'use client'

import { useActionState, useEffect, useRef } from 'react'
import { publicarNovidade } from '@/app/admin/novidades/acoes'

export function AdminNovidades() {
  const [r, acao, enviando] = useActionState(publicarNovidade, null)
  const form = useRef<HTMLFormElement>(null)
  // Publicou: limpa os campos para a próxima
  useEffect(() => {
    if (r?.ok) form.current?.reset()
  }, [r])
  return (
    <form ref={form} action={acao} className="admin-form" noValidate>
      <label className="flabel" htmlFor="titulo">
        Título
      </label>
      <input id="titulo" name="titulo" className="campo" maxLength={120} placeholder="Ex.: Questões de Gastro novas" />
      <label className="flabel" htmlFor="texto">
        Texto
      </label>
      <textarea
        id="texto"
        name="texto"
        className="campo"
        rows={4}
        maxLength={1000}
        placeholder="Uma ou duas frases dizendo o que mudou e onde achar."
        style={{ resize: 'vertical', fontSize: 14, lineHeight: 1.45 }}
      />
      <button className="btn" type="submit" disabled={enviando}>
        {enviando ? 'Publicando…' : 'Publicar novidade'}
      </button>
      {r && (
        <p className={r.ok ? 'ok-msg' : 'err'} role="status">
          {r.texto}
        </p>
      )}
    </form>
  )
}
