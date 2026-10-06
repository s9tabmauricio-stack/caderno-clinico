'use client'

import { useMemo, useState } from 'react'
import { ehDoAluno, situacoes } from '@/lib/agenda'
import type { EventoBanco } from '@/lib/agenda-dados'
import { AgendaAvisos, AgendaLista } from './AgendaLista'

const DIAS = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']

export function AgendaSemana({
  semana,
  aviso,
  eventos,
  grupo,
  agora,
}: {
  semana: string
  aviso: string | null
  eventos: EventoBanco[]
  grupo: number | null
  agora: { data: string; minutos: number }
}) {
  // Segunda a sexta, mais sábado/domingo se tiverem algo
  const dias = useMemo(() => {
    const base = new Date(`${semana}T12:00:00Z`)
    const lista: string[] = []
    for (let i = 0; i < 7; i++) {
      const d = new Date(base)
      d.setUTCDate(d.getUTCDate() + i)
      const iso = d.toISOString().slice(0, 10)
      if (i < 5 || eventos.some((e) => e.data === iso)) lista.push(iso)
    }
    return lista
  }, [semana, eventos])

  const [dia, setDia] = useState(() => (dias.includes(agora.data) ? agora.data : dias.find((d) => eventos.some((e) => e.data === d)) ?? dias[0]))
  const [filtro, setFiltro] = useState<'meu' | 'todas'>(grupo === null ? 'todas' : 'meu')

  const doDia = eventos.filter((e) => e.data === dia)
  const aulas = doDia.filter((e) => !e.cancelado && e.tipo !== 'aviso' && (filtro === 'todas' || ehDoAluno(e.grupos, grupo)))
  const avisos = doDia.filter((e) => e.cancelado || e.tipo === 'aviso')
  const estados =
    dia === agora.data
      ? Object.fromEntries(situacoes(aulas, agora.minutos).map((x) => [x.evento.id, { situacao: x.situacao, falta: x.falta }]))
      : undefined

  const nomeDia = new Intl.DateTimeFormat('pt-BR', { weekday: 'long', day: 'numeric', month: 'long', timeZone: 'UTC' }).format(
    new Date(`${dia}T12:00:00Z`),
  )

  return (
    <>
      <div className="segm segm-dias" role="tablist" aria-label="Dias da semana" style={{ gridTemplateColumns: `repeat(${dias.length}, minmax(0,1fr))` }}>
        {dias.map((d) => {
          const dt = new Date(`${d}T12:00:00Z`)
          return (
            <button
              key={d}
              role="tab"
              aria-selected={d === dia}
              className={`${d === dia ? 'on' : ''} ${d === agora.data ? 'hoje' : ''}`}
              onClick={() => setDia(d)}
            >
              {DIAS[dt.getUTCDay()]}
              <b>{dt.getUTCDate()}</b>
            </button>
          )
        })}
      </div>

      <div className="ag-filtros" role="group" aria-label="Filtro">
        <button className="pill" aria-pressed={filtro === 'meu'} disabled={grupo === null} onClick={() => setFiltro('meu')}>
          {grupo === null ? 'Meu grupo' : `Meu grupo (${grupo})`}
        </button>
        <button className="pill" aria-pressed={filtro === 'todas'} onClick={() => setFiltro('todas')}>
          Todas as aulas
        </button>
      </div>

      <AgendaAvisos eventos={avisos} />

      <div className="sec" style={{ textTransform: 'none', letterSpacing: 0, fontSize: 14 }}>
        {nomeDia.charAt(0).toUpperCase() + nomeDia.slice(1)}
      </div>
      {aulas.length ? (
        <AgendaLista eventos={aulas} grupo={grupo} estados={estados} />
      ) : (
        <p className="vazio">{doDia.length ? 'Nenhuma aula do seu grupo neste dia.' : 'Nenhuma aula neste dia.'}</p>
      )}

      {aviso && <p className="foot">⚠️ {aviso}</p>}
    </>
  )
}
