'use client'

import { useState } from 'react'
import type { QuestaoAluno } from '@/lib/dados'
import { plural } from '@/lib/formato'
import { Questoes, type Resposta } from './Questoes'

type Situacao = 'todas' | 'abertas' | 'erradas'
type Filtros = { tema: string | null; prova: string | null; situacao: Situacao }

const ROTULO_PROVA = (p: string) => p.replace(/^p(\d)-t(\d+)$/i, 'P$1 T$2')

// O servidor lê este cookie na próxima visita e já abre o banco com o mesmos filtros
function lembrarFiltros(chave: string, f: Filtros) {
  const valor = encodeURIComponent(JSON.stringify(f))
  document.cookie = `mgf_${chave}=${valor}; path=/; max-age=15552000; samesite=lax`
}

function filtrar(lista: QuestaoAluno[], f: Filtros) {
  return lista.filter(
    (q) =>
      (!f.tema || q.tema === f.tema) &&
      (!f.prova || q.prova === f.prova) &&
      (f.situacao === 'todas' || (f.situacao === 'abertas' ? !q.resposta : q.resposta && !q.resposta.acertou)),
  )
}

export function BancoQuestoes({
  chave,
  questoes,
  userId,
  inicial,
  edicao,
}: {
  // id da matéria: nome do cookie em que os filtros escolhidos ficam lembrados
  chave: string
  questoes: QuestaoAluno[]
  userId: string
  // filtro já aplicado ao abrir (links do Desempenho)
  inicial?: Partial<Filtros>
  edicao?: { aulas: { id: string; titulo: string }[] }
}) {
  // Respostas dadas nesta visita (o resto veio do servidor)
  const [extras, setExtras] = useState<Record<string, Resposta | null>>({})
  const [filtros, setFiltros] = useState<Filtros>({ tema: null, prova: null, situacao: 'todas', ...inicial })
  const atuais = questoes.map((q) => (q.id in extras ? { ...q, resposta: extras[q.id] } : q))
  // A lista em estudo só muda quando o aluno troca o filtro, para não pular questões no meio
  const [lista, setLista] = useState(() => filtrar(questoes, filtros))
  const [versao, setVersao] = useState(0)
  const [aberto, setAberto] = useState(false)

  function aplicar(novo: Partial<Filtros>) {
    const f = { ...filtros, ...novo }
    setFiltros(f)
    lembrarFiltros(chave, f)
    const url = new URL(window.location.href)
    url.searchParams.set('tema', f.tema ?? '')
    url.searchParams.set('prova', f.prova ?? '')
    url.searchParams.set('mostrar', f.situacao)
    window.history.replaceState(null, '', url)
    setLista(filtrar(atuais, f))
    setVersao((v) => v + 1)
  }

  const contar = (campo: 'tema' | 'prova') => {
    const m = new Map<string, number>()
    questoes.forEach((q) => {
      const v = q[campo]
      if (v) m.set(v, (m.get(v) ?? 0) + 1)
    })
    return [...m.entries()]
  }
  const temas = contar('tema').sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
  const provas = contar('prova').sort((a, b) => a[0].localeCompare(b[0]))

  const respondidas = atuais.filter((q) => q.resposta)
  const certas = respondidas.filter((q) => q.resposta?.acertou).length
  const erradas = respondidas.length - certas

  // Filtros ligados, mostrados como etiquetas que se tiram com um toque
  const ativos = [
    filtros.situacao !== 'todas' && {
      rotulo: filtros.situacao === 'abertas' ? 'Não respondidas' : 'Só as que errei',
      tirar: () => aplicar({ situacao: 'todas' }),
    },
    filtros.tema && { rotulo: filtros.tema, tirar: () => aplicar({ tema: null }) },
    filtros.prova && { rotulo: ROTULO_PROVA(filtros.prova), tirar: () => aplicar({ prova: null }) },
  ].filter((f): f is { rotulo: string; tirar: () => void } => Boolean(f))

  const pill = (ativo: boolean, rotulo: string, onClick: () => void, n?: number) => (
    <button key={rotulo} className="pill" aria-pressed={ativo} onClick={onClick}>
      {rotulo}
      {n !== undefined && <small>{n}</small>}
    </button>
  )

  return (
    <>
      <div className="filtro-barra banco-barra">
        <button
          className="pill filtro-btn"
          aria-expanded={aberto}
          aria-controls="painel-filtros"
          onClick={() => setAberto(!aberto)}
        >
          Filtrar
          {ativos.length > 0 && <small>{ativos.length}</small>}
        </button>
        {ativos.map((f) => (
          <button key={f.rotulo} className="pill ativo" aria-label={`Tirar o filtro ${f.rotulo}`} onClick={f.tirar}>
            {f.rotulo} <span aria-hidden="true">✕</span>
          </button>
        ))}
        {/* Resumo numa linha só (antes eram três quadros), para a questão começar mais acima na tela */}
        <p className="banco-resumo">
          {ativos.length > 0 && (
            <>
              <b>{lista.length}</b> neste filtro ·{' '}
            </>
          )}
          <b>
            {respondidas.length}/{questoes.length}
          </b>{' '}
          {plural(respondidas.length, 'respondida', 'respondidas')}
          {respondidas.length > 0 && (
            <>
              {' '}
              · <b>{Math.round((100 * certas) / respondidas.length)}%</b> de acerto
            </>
          )}
          {erradas > 0 && (
            <>
              {' '}
              · <b>{erradas}</b> para rever
            </>
          )}
        </p>
      </div>

      {aberto && (
      <div className="filtros" id="painel-filtros" aria-label="Filtros">
        <div className="filtro">
          <span className="rot">Mostrar</span>
          {pill(filtros.situacao === 'todas', 'Todas', () => aplicar({ situacao: 'todas' }))}
          {pill(filtros.situacao === 'abertas', 'Não respondidas', () => aplicar({ situacao: 'abertas' }))}
          {pill(filtros.situacao === 'erradas', 'Só as que errei', () => aplicar({ situacao: 'erradas' }), erradas)}
        </div>
        {temas.length > 1 && (
          <div className="filtro">
            <span className="rot">Tema</span>
            {pill(!filtros.tema, 'Todos', () => aplicar({ tema: null }))}
            {temas.map(([t, n]) => pill(filtros.tema === t, t, () => aplicar({ tema: filtros.tema === t ? null : t }), n))}
          </div>
        )}
        {(provas.length > 1 || (provas.length === 1 && provas[0][1] < questoes.length)) && (
          <div className="filtro">
            <span className="rot">Prova</span>
            {pill(!filtros.prova, 'Todas', () => aplicar({ prova: null }))}
            {provas.map(([p, n]) =>
              pill(filtros.prova === p, ROTULO_PROVA(p), () => aplicar({ prova: filtros.prova === p ? null : p }), n),
            )}
          </div>
        )}
      </div>
      )}

      <Questoes
        key={versao}
        questoes={lista}
        userId={userId}
        ativo
        mostrarTema={!filtros.tema}
        edicao={edicao}
        vazio={
          filtros.situacao === 'erradas'
            ? 'Nenhuma questão errada neste filtro. Bom sinal.'
            : 'Nenhuma questão neste filtro.'
        }
        aoResponder={(id, r) => setExtras((e) => ({ ...e, [id]: r }))}
      />
    </>
  )
}
