'use client'

import { useState } from 'react'
import type { DiaCentral } from '@/lib/central'

const ddmm = (dia: string) => `${dia.slice(8, 10)}/${dia.slice(5, 7)}`

// Atividade da turma nos últimos 14 dias: questões respondidas ou cards revisados por dia.
export function GraficoCentral({ dias }: { dias: DiaCentral[] }) {
  const [serie, setSerie] = useState<'questoes' | 'cards'>('questoes')
  const max = Math.max(1, ...dias.map((d) => d[serie]))
  const total = dias.reduce((s, d) => s + d[serie], 0)
  const nome = serie === 'questoes' ? 'questões respondidas' : 'cards revisados'
  return (
    <div className="ct-graf">
      <div className="ct-graf-h">
        <span className="main">
          <span className="t">Últimos 14 dias</span>
          <span className="s">
            {total} {nome} pela turma
          </span>
        </span>
        <div className="segm" role="group" aria-label="O que mostrar">
          <button type="button" className={serie === 'questoes' ? 'on' : ''} aria-pressed={serie === 'questoes'} onClick={() => setSerie('questoes')}>
            Questões
          </button>
          <button type="button" className={serie === 'cards' ? 'on' : ''} aria-pressed={serie === 'cards'} onClick={() => setSerie('cards')}>
            Cards
          </button>
        </div>
      </div>
      <div className="ct-barras" role="img" aria-label={dias.map((d) => `${ddmm(d.dia)}: ${d[serie]}`).join(', ')}>
        {dias.map((d) => (
          <div key={d.dia} className="ct-barra" title={`${ddmm(d.dia)}: ${d[serie]} ${nome}`}>
            <span>{d[serie] || ''}</span>
            <i className={d[serie] ? '' : 'zero'} style={{ height: d[serie] ? `${Math.max(6, (d[serie] / max) * 82)}%` : undefined }} />
          </div>
        ))}
      </div>
      <div className="ct-eixo">
        <span>{dias.length ? ddmm(dias[0].dia) : ''}</span>
        <span>{dias.length > 7 ? ddmm(dias[Math.floor(dias.length / 2)].dia) : ''}</span>
        <span>hoje</span>
      </div>
    </div>
  )
}
