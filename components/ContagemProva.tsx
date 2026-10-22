'use client'

import { useEffect, useState } from 'react'

/** Contagem regressiva até a prova em dias, horas e minutos (atualiza sozinha a cada 10 segundos). */
export function ContagemProva({ alvo, agora }: { alvo: number; agora: number }) {
  // Começa na hora do servidor, para a tela não piscar ao carregar
  const [t, setT] = useState(agora)
  useEffect(() => {
    const id = setInterval(() => setT(Date.now()), 10_000)
    return () => clearInterval(id)
  }, [])

  const falta = Math.floor(Math.max(0, alvo - t) / 60_000)
  if (falta <= 0) return <p className="pv-boa">Boa prova! 🍀</p>
  const d = Math.floor(falta / 1440)
  const h = Math.floor((falta % 1440) / 60)
  const m = falta % 60
  return (
    <div className="pv-conta" role="timer" aria-label={`Faltam ${d} dias, ${h} horas e ${m} minutos`}>
      <span>
        <b>{d}</b>
        {d === 1 ? 'dia' : 'dias'}
      </span>
      <span>
        <b>{String(h).padStart(2, '0')}</b>
        {h === 1 ? 'hora' : 'horas'}
      </span>
      <span>
        <b>{String(m).padStart(2, '0')}</b>
        min
      </span>
    </div>
  )
}
