'use client'

import { useState } from 'react'
import type { QuestaoAluno } from '@/lib/dados'
import { plural } from '@/lib/formato'
import { CLASSIFICACOES_QUESTAO, FONTES_QUESTAO, filtrarQuestoes, fonteDaQuestao, rotuloClassificacao, rotuloFonte, type ClassificacaoQuestao, type FiltrosQuestoes } from '@/lib/classificacao-questoes'
import { Questoes, type Resposta } from './Questoes'

type Filtros = FiltrosQuestoes

// O servidor lê este cookie na próxima visita e já abre o banco com o mesmos filtros
function lembrarFiltros(chave: string, f: Filtros) {
  const valor = encodeURIComponent(JSON.stringify(f))
  document.cookie = `mgf_${chave}=${valor}; path=/; max-age=15552000; samesite=lax`
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
  const [classificacoes, setClassificacoes] = useState<Record<string, ClassificacaoQuestao | null>>({})
  const [filtros, setFiltros] = useState<Filtros>({ tema: null, fonte: null, situacao: 'todas', classificacao: 'todas', ...inicial })
  const atuais = questoes.map((q) => ({
    ...q,
    resposta: q.id in extras ? extras[q.id] : q.resposta,
    classificacao: q.id in classificacoes ? classificacoes[q.id] : q.classificacao,
  }))
  // A lista em estudo só muda quando o aluno troca o filtro, para não pular questões no meio
  const [lista, setLista] = useState(() => filtrarQuestoes(questoes, filtros))
  const [versao, setVersao] = useState(0)
  const [aberto, setAberto] = useState(false)

  function aplicar(novo: Partial<Filtros>) {
    const f = { ...filtros, ...novo }
    setFiltros(f)
    lembrarFiltros(chave, f)
    const url = new URL(window.location.href)
    url.searchParams.set('tema', f.tema ?? '')
    url.searchParams.delete('prova')
    url.searchParams.set('fonte', f.fonte ?? '')
    url.searchParams.set('mostrar', f.situacao)
    url.searchParams.set('classificacao', f.classificacao)
    window.history.replaceState(null, '', url)
    setLista(filtrarQuestoes(atuais, f))
    setVersao((v) => v + 1)
  }

  const temasContados = new Map<string, number>()
  questoes.forEach((q) => {
    if (q.tema) temasContados.set(q.tema, (temasContados.get(q.tema) ?? 0) + 1)
  })
  const temas = [...temasContados.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
  // As três fontes, na ordem fixa, só as que têm questões nesta matéria
  const fontes = FONTES_QUESTAO.map(({ valor, rotulo }) => ({
    valor,
    rotulo,
    n: questoes.filter((q) => fonteDaQuestao(q) === valor).length,
  })).filter((f) => f.n > 0)

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
    filtros.fonte && { rotulo: rotuloFonte(filtros.fonte), tirar: () => aplicar({ fonte: null }) },
    filtros.classificacao !== 'todas' && {
      rotulo: filtros.classificacao === 'marcadas' ? 'Todas as marcadas' : rotuloClassificacao(filtros.classificacao),
      tirar: () => aplicar({ classificacao: 'todas' }),
    },
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
        <div className="filtro">
          <span className="rot">Minha revisão</span>
          {pill(filtros.classificacao === 'todas', 'Todas', () => aplicar({ classificacao: 'todas' }))}
          {pill(filtros.classificacao === 'marcadas', 'Todas as marcadas', () => aplicar({ classificacao: 'marcadas' }), atuais.filter((q) => q.classificacao !== null).length)}
          {CLASSIFICACOES_QUESTAO.map(({ valor, rotulo }) =>
            pill(filtros.classificacao === valor, rotulo, () => aplicar({ classificacao: valor }), atuais.filter((q) => q.classificacao === valor).length),
          )}
        </div>
        {temas.length > 1 && (
          <div className="filtro">
            <span className="rot">Tema</span>
            {pill(!filtros.tema, 'Todos', () => aplicar({ tema: null }))}
            {temas.map(([t, n]) => pill(filtros.tema === t, t, () => aplicar({ tema: filtros.tema === t ? null : t }), n))}
          </div>
        )}
        {fontes.length > 1 && (
          <div className="filtro">
            <span className="rot">Fonte</span>
            {pill(!filtros.fonte, 'Todas', () => aplicar({ fonte: null }))}
            {fontes.map(({ valor, rotulo, n }) =>
              pill(filtros.fonte === valor, rotulo, () => aplicar({ fonte: filtros.fonte === valor ? null : valor }), n),
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
        iniciarPelaPrimeira={filtros.classificacao !== 'todas'}
        mostrarTema={!filtros.tema}
        edicao={edicao}
        vazio={
          filtros.situacao === 'erradas'
            ? 'Nenhuma questão errada neste filtro. Bom sinal.'
            : 'Nenhuma questão neste filtro.'
        }
        aoResponder={(id, r) => setExtras((e) => ({ ...e, [id]: r }))}
        aoClassificar={(id, valor) => setClassificacoes((anteriores) => ({ ...anteriores, [id]: valor }))}
      />
    </>
  )
}
