'use client'

import { useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'
import { ehDiaTodo, ehDoAluno, situacoes } from '@/lib/agenda'
import type { EventoBanco } from '@/lib/agenda-dados'
import { AgendaAvisos, AgendaDiaTodo, AgendaLista } from './AgendaLista'

const DIAS = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']

export function AgendaSemana({
  semana,
  aviso,
  eventos,
  grupo,
  agora,
  userId,
  materias,
}: {
  semana: string
  aviso: string | null
  eventos: EventoBanco[]
  grupo: number | null
  agora: { data: string; minutos: number }
  userId: string
  materias: string[]
}) {
  const supabase = useMemo(() => createClient(), [])
  const router = useRouter()
  // Grupo escolhido aqui, valendo na hora (o servidor confirma no próximo carregamento)
  const [escolhido, setEscolhido] = useState<number | null>(null)
  const [salvandoGrupo, setSalvandoGrupo] = useState(false)
  const [erroGrupo, setErroGrupo] = useState('')
  const grupoAtual = escolhido ?? grupo

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

  async function escolherGrupo(valor: string) {
    const n = Number(valor)
    if (!Number.isInteger(n) || n < 1 || n > 99) return
    setSalvandoGrupo(true)
    setErroGrupo('')
    const { error } = await supabase.from('perfis').update({ grupo: n }).eq('id', userId)
    setSalvandoGrupo(false)
    if (error) {
      setErroGrupo('Não deu para salvar o grupo. Confira a internet e tente de novo.')
      return
    }
    setEscolhido(n)
    setFiltro('meu')
    router.refresh()
  }

  const doDia = eventos.filter((e) => e.data === dia)
  const diaTodo = doDia.filter(ehDiaTodo)
  const aulas = doDia.filter(
    (e) => !e.cancelado && e.tipo !== 'aviso' && !ehDiaTodo(e) && (filtro === 'todas' || ehDoAluno(e.grupos, grupoAtual)),
  )
  const avisos = doDia.filter((e) => e.cancelado || e.tipo === 'aviso')
  const estados =
    dia === agora.data
      ? Object.fromEntries(situacoes(aulas, agora.minutos).map((x) => [x.evento.id, { situacao: x.situacao, falta: x.falta, feito: x.feito }]))
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
        {grupoAtual !== null && (
          <button className="pill" aria-pressed={filtro === 'meu'} onClick={() => setFiltro('meu')}>
            Meu grupo ({grupoAtual})
          </button>
        )}
        <button className="pill" aria-pressed={filtro === 'todas'} onClick={() => setFiltro('todas')}>
          Todas as aulas
        </button>
        <select
          className={`ag-grupo${grupoAtual === null ? ' vazio-grupo' : ''}`}
          aria-label="Seu grupo de prática"
          value={grupoAtual ?? ''}
          disabled={salvandoGrupo}
          onChange={(e) => void escolherGrupo(e.target.value)}
        >
          {grupoAtual === null && <option value="">Escolher meu grupo</option>}
          {Array.from({ length: 29 }, (_, i) => i + 1)
            .concat(grupoAtual !== null && grupoAtual > 29 ? [grupoAtual] : [])
            .map((n) => (
              <option key={n} value={n}>
                Grupo {n}
              </option>
            ))}
        </select>
      </div>
      {grupoAtual === null && <p className="foot">Escolha seu grupo para ver as teóricas da turma e só as suas práticas.</p>}
      {erroGrupo && (
        <p className="err" role="alert">
          {erroGrupo}
        </p>
      )}

      <AgendaAvisos eventos={avisos} />

      <div className="sec" style={{ textTransform: 'none', letterSpacing: 0, fontSize: 14 }}>
        {nomeDia.charAt(0).toUpperCase() + nomeDia.slice(1)}
      </div>
      <AgendaDiaTodo eventos={diaTodo} materias={materias} />
      {aulas.length ? (
        <AgendaLista eventos={aulas} grupo={grupoAtual} estados={estados} materias={materias} />
      ) : (
        <p className="vazio">{doDia.length > diaTodo.length ? 'Nenhuma aula do seu grupo neste dia.' : 'Nenhuma aula neste dia.'}</p>
      )}

      {aviso && <p className="foot">⚠️ {aviso}</p>}
    </>
  )
}
