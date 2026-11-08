'use client'

import { useState } from 'react'
import type { QuestaoAluno } from '@/lib/dados'
import { plural } from '@/lib/formato'
import { CLASSIFICACOES_QUESTAO, FONTES_QUESTAO, filtrarQuestoes, fonteDaQuestao, rotuloClassificacao, type ClassificacaoQuestao, type FiltrosQuestoes, type FonteQuestao } from '@/lib/classificacao-questoes'
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
  const atuais = questoes.map((q) => ({
    ...q,
    resposta: q.id in extras ? extras[q.id] : q.resposta,
    classificacao: q.id in classificacoes ? classificacoes[q.id] : q.classificacao,
  }))
  // A barra de fonte sempre tem um grupo escolhido: sem um pedido, o primeiro que tem questões neste filtro
  const [filtros, setFiltros] = useState<Filtros>(() => {
    const f: Filtros = { tema: null, fonte: null, situacao: 'todas', classificacao: 'todas', ...inicial }
    if (f.fonte) return f
    const tem = (valor: FonteQuestao) => filtrarQuestoes(questoes, { ...f, fonte: valor }).length > 0
    const fonte = FONTES_QUESTAO.find((g) => tem(g.valor))?.valor ?? FONTES_QUESTAO.find((g) => questoes.some((q) => fonteDaQuestao(q) === g.valor))?.valor ?? 'fag'
    return { ...f, fonte }
  })
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
  // Barra de fonte: os três grupos, com quantas questões cada um tem nos outros filtros escolhidos
  const grupos = FONTES_QUESTAO.map((g) => ({ ...g, n: filtrarQuestoes(atuais, { ...filtros, fonte: g.valor }).length }))
  const grupo = grupos.find((g) => g.valor === filtros.fonte) ?? grupos[0]

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
      <div className="segm segm-fonte" role="tablist" aria-label="De onde vêm as questões">
        {grupos.map((g) => (
          <button
            key={g.valor}
            role="tab"
            aria-selected={filtros.fonte === g.valor}
            className={filtros.fonte === g.valor ? 'on' : ''}
            onClick={() => aplicar({ fonte: g.valor })}
          >
            {g.rotulo} <small>{g.n}</small>
          </button>
        ))}
      </div>

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
            : ativos.length
              ? `${grupo.vazio} neste filtro.`
              : `${grupo.vazio} nesta matéria.`
        }
        aoResponder={(id, r) => setExtras((e) => ({ ...e, [id]: r }))}
        aoClassificar={(id, valor) => setClassificacoes((anteriores) => ({ ...anteriores, [id]: valor }))}
      />
    </>
  )
}
