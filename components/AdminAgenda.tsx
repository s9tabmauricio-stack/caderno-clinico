'use client'

import { useActionState } from 'react'
import { publicarAgenda } from '@/app/admin/agenda/acoes'

export function AdminAgenda() {
  const [r, acao, enviando] = useActionState(publicarAgenda, null)
  return (
    <form action={acao} className="admin-form" noValidate>
      <label className="flabel" htmlFor="texto">
        Texto do cronograma
      </label>
      <textarea
        id="texto"
        name="texto"
        className="campo"
        rows={14}
        placeholder={'CRONOGRAMA SEMANAL\n\nSEGUNDA-FEIRA | 5/outubro\n\n🫁 7h30-9h: aula prática de pneumologia para o grupo 2 com Dra. ... no CAE.'}
        style={{ resize: 'vertical', fontSize: 14, lineHeight: 1.45 }}
      />
      <button className="btn" type="submit" disabled={enviando}>
        {enviando ? 'Publicando…' : 'Publicar semana'}
      </button>
      {r && (
        <p className={r.ok ? 'ok-msg' : 'err'} role="status">
          {r.texto}
        </p>
      )}
      {r?.dias && (
        <ul className="foot" style={{ margin: 0, paddingLeft: 18 }}>
          {r.dias.map((d) => (
            <li key={d.data}>
              {new Intl.DateTimeFormat('pt-BR', { weekday: 'long', day: 'numeric', month: 'numeric', timeZone: 'UTC' }).format(new Date(`${d.data}T12:00:00Z`))}:{' '}
              {d.aulas} aulas{d.avisos ? `, ${d.avisos} avisos` : ''}
            </li>
          ))}
        </ul>
      )}
    </form>
  )
}
