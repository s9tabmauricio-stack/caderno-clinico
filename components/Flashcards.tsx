'use client'

import { useEffect, useMemo, useRef, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'
import type { CardAluno } from '@/lib/dados'
import { avaliar, intervalos, vencido, type EstadoCard, type Nota } from '@/lib/srs'
import { fmtIntervalo, fmtQuando, plural } from '@/lib/formato'
import { explicarFalha } from '@/lib/falhas'
import { cardDeProva } from '@/lib/faixa-prova'
import { avancarSemCard, type SessaoCards } from '@/lib/suspensao-flashcards'
import { Icone } from './Icones'
import { FaixaProva } from './FaixaProva'

type Props = {
  cards: CardAluno[]
  userId: string
  // "aula": todos os cards de uma aula; "materia": todos os cards de uma matéria; "revisao": a fila do dia (vencidos + novos)
  modo: 'aula' | 'materia' | 'revisao'
  ativo: boolean
  emDia?: number // em "revisao", quantos cards estão em dia (não vêm na lista)
  // em "aula": o que oferecer quando os cards acabam ou já estão em dia (ex.: fazer as questões)
  proximoPasso?: React.ReactNode
}

type Sessao = SessaoCards

type HistoricoItem = { tipo: 'suspensao'; cardId: string; sessaoAnterior: Sessao } | {
  tipo: 'avaliacao'
  cardId: string
  sessaoAnterior: Sessao
  estadoAnterior: EstadoCard | null
  tinhaEmLocais: boolean
  valorLocalAnterior?: EstadoCard
  eraNovoNoBanco: boolean
}

export function Flashcards({ cards, userId, modo, ativo, emDia, proximoPasso }: Props) {
  const supabase = useMemo(() => createClient(), [])
  const router = useRouter()
  // Estados alterados nesta visita; o resto vem do servidor
  const [locais, setLocais] = useState<Record<string, EstadoCard>>({})
  const [sessao, setSessao] = useState<Sessao | null>(null)
  const [historico, setHistorico] = useState<HistoricoItem[]>([])
  const [falhaSalvar, setFalhaSalvar] = useState('')
  const [agora, setAgora] = useState(() => Date.now())
  const [suspensoes, setSuspensoes] = useState<Record<string, boolean>>({})
  const [mostrarSuspensos, setMostrarSuspensos] = useState(false)
  const [salvando, setSalvando] = useState(false)
  const trava = useRef(false)
  const [notificacao, setNotificacao] = useState<{ texto: string; detalhe: string; reativado?: string } | null>(null)

  const estadoDe = (c: CardAluno) => locais[c.id] ?? c.estado
  const estaSuspenso = (c: CardAluno) => suspensoes[c.id] ?? c.suspenso
  const cardsAtivos = cards.filter((c) => !estaSuspenso(c))
  const cardsSuspensos = cards.filter(estaSuspenso)
  const statusDe = (c: CardAluno) => {
    const s = estadoDe(c)
    return !s ? 'novo' : vencido(s, agora) ? 'revisar' : 'emdia'
  }

  const novos = cardsAtivos.filter((c) => statusDe(c) === 'novo')
  const paraRevisar = cardsAtivos
    .filter((c) => statusDe(c) === 'revisar')
    .sort((a, b) => (estadoDe(a)?.proxima_revisao ?? '').localeCompare(estadoDe(b)?.proxima_revisao ?? ''))
  const emDiaAqui = cardsAtivos.filter((c) => statusDe(c) === 'emdia').length
  const pendentes = paraRevisar.length + novos.length

  const proxima = cardsAtivos
    .map((c) => estadoDe(c))
    .filter((s): s is EstadoCard => s !== null && new Date(s.proxima_revisao).getTime() > agora)
    .map((s) => s.proxima_revisao)
    .sort()[0]

  // Em "materia": os cards separados por aula (já vêm na ordem das aulas)
  const porAula = new Map<string, { id: string; ordem: number; titulo: string; lista: CardAluno[] }>()
  if (modo === 'materia') {
    for (const c of cardsAtivos) {
      const grupo = porAula.get(c.aula_id)
      if (grupo) grupo.lista.push(c)
      else porAula.set(c.aula_id, { id: c.aula_id, ordem: c.aula_ordem, titulo: c.aula_titulo, lista: [c] })
    }
  }

  function comecar(todos: boolean) {
    if (trava.current) return
    const lista = todos ? cardsAtivos : [...paraRevisar, ...novos]
    if (!lista.length) return
    const ids = lista.map((c) => c.id)
    setFalhaSalvar('')
    setHistorico([])
    setNotificacao(null)
    setSessao({ fila: ids.slice(1), atual: ids[0], virado: false, feitos: 0, erros: 0 })
  }

  async function avaliarCard(nota: Nota) {
    if (trava.current || !sessao?.atual || !sessao.virado) return
    const card = cards.find((c) => c.id === sessao.atual)
    if (!card) return
    trava.current = true
    setSalvando(true)
    setFalhaSalvar('')
    setNotificacao(null)
    try {
      const t = Date.now()
      const anterior = estadoDe(card)
      const novo = avaliar(anterior, nota, t)
      const { error } = await supabase
        .from('revisoes')
        .upsert({ user_id: userId, flashcard_id: card.id, ...novo }, { onConflict: 'user_id,flashcard_id' })
      if (error) {
        const { texto } = await explicarFalha(supabase, 'a última revisão')
        setFalhaSalvar(texto)
        return
      }
      // Só avança e oferece desfazer depois de confirmar a gravação.
      setHistorico((h) => [...h, {
        tipo: 'avaliacao', cardId: card.id, sessaoAnterior: sessao, estadoAnterior: anterior,
        tinhaEmLocais: card.id in locais, valorLocalAnterior: locais[card.id], eraNovoNoBanco: card.estado === null,
      }])
      setLocais((l) => ({ ...l, [card.id]: novo }))
      const fila = [...sessao.fila]
      if (nota === 0) fila.push(card.id)
      setSessao({
        fila: fila.slice(1), atual: fila[0] ?? null, virado: false,
        feitos: sessao.feitos + 1, erros: sessao.erros + (nota === 0 ? 1 : 0),
      })
      setAgora(t)
    } catch {
      setFalhaSalvar('Não deu para salvar a revisão. Confira sua internet antes de continuar.')
    } finally {
      trava.current = false
      setSalvando(false)
    }
  }

  // A suspensão tem tabela própria: não altera revisões nem seu histórico.
  async function gravarSuspensao(cardId: string, suspenso: boolean) {
    const resultado = suspenso
      ? await supabase.from('flashcards_suspensos').upsert(
          { user_id: userId, flashcard_id: cardId },
          { onConflict: 'user_id,flashcard_id' },
        )
      : await supabase.from('flashcards_suspensos').delete().eq('user_id', userId).eq('flashcard_id', cardId)
    if (resultado.error) throw resultado.error
    setSuspensoes((s) => ({ ...s, [cardId]: suspenso }))
  }

  async function suspenderCard() {
    if (trava.current || !sessao?.atual || !sessao.virado) return
    trava.current = true
    setSalvando(true)
    setFalhaSalvar('')
    try {
      const cardId = sessao.atual
      await gravarSuspensao(cardId, true)
      setHistorico((h) => [...h, { tipo: 'suspensao', cardId, sessaoAnterior: sessao }])
      setSessao(avancarSemCard(sessao, cardId))
      setNotificacao({ texto: 'Card suspenso', detalhe: 'Fora das suas revisões até você reativar.' })
    } catch {
      setFalhaSalvar('Não deu para suspender o card. Confira sua internet e tente novamente.')
    } finally {
      trava.current = false
      setSalvando(false)
    }
  }

  async function reativarCard(cardId: string) {
    if (trava.current) return
    trava.current = true
    setSalvando(true)
    setFalhaSalvar('')
    try {
      await gravarSuspensao(cardId, false)
      setNotificacao({ texto: 'Card reativado', detalhe: 'Voltou aos seus cards ativos com o histórico preservado.', reativado: cardId })
      router.refresh()
    } catch {
      setFalhaSalvar('Não deu para reativar o card. Confira sua internet e tente novamente.')
    } finally {
      trava.current = false
      setSalvando(false)
    }
  }

  async function desfazerReativacao(cardId: string) {
    if (trava.current) return
    trava.current = true
    setSalvando(true)
    setFalhaSalvar('')
    try {
      await gravarSuspensao(cardId, true)
      setNotificacao(null)
      router.refresh()
    } catch {
      setFalhaSalvar('Não deu para desfazer a reativação. Confira sua internet e tente novamente.')
    } finally {
      trava.current = false
      setSalvando(false)
    }
  }

  async function desfazer() {
    if (trava.current || !historico.length) return
    const ultimo = historico[historico.length - 1]
    trava.current = true
    setSalvando(true)
    setFalhaSalvar('')
    try {
      if (ultimo.tipo === 'suspensao') {
        await gravarSuspensao(ultimo.cardId, false)
      } else {
        if (ultimo.eraNovoNoBanco && !ultimo.tinhaEmLocais) {
          const { error } = await supabase.from('revisoes').delete().eq('user_id', userId).eq('flashcard_id', ultimo.cardId)
          if (error) throw error
        } else if (ultimo.estadoAnterior) {
          const { error } = await supabase.from('revisoes').upsert(
            { user_id: userId, flashcard_id: ultimo.cardId, ...ultimo.estadoAnterior },
            { onConflict: 'user_id,flashcard_id' },
          )
          if (error) throw error
        }
      }
      setHistorico((h) => h.slice(0, -1))
      setNotificacao(null)
      setSessao(ultimo.sessaoAnterior)
      if (ultimo.tipo === 'avaliacao') setLocais((l) => {
        const copia = { ...l }
        if (ultimo.tinhaEmLocais && ultimo.valorLocalAnterior) copia[ultimo.cardId] = ultimo.valorLocalAnterior
        else delete copia[ultimo.cardId]
        return copia
      })
    } catch {
      setFalhaSalvar('Não deu para desfazer a última ação. Confira sua internet e tente novamente.')
    } finally {
      trava.current = false
      setSalvando(false)
    }
  }

  function encerrar() {
    if (trava.current) return
    setSessao(null)
    setHistorico([])
    setNotificacao(null)
    setAgora(Date.now())
    router.refresh() // atualiza contadores e a fila do dia
  }

  // Atalhos: espaço mostra a resposta; 1 a 4 avaliam; Z desfaz
  useEffect(() => {
    if (!ativo || !sessao) return
    function tecla(e: KeyboardEvent) {
      const alvo = e.target as HTMLElement
      if (trava.current || alvo.closest('input, textarea, [contenteditable="true"]')) return
      if ((e.key === 'z' || e.key === 'Z') && !e.altKey) {
        e.preventDefault()
        void desfazer()
        return
      }
      if (e.metaKey || e.ctrlKey || e.altKey || alvo.closest('button, a')) return
      if (!sessao?.virado && (e.key === ' ' || e.key === 'Enter') && sessao?.atual) {
        e.preventDefault()
        setSessao((s) => (s ? { ...s, virado: true } : s))
      } else if (sessao?.virado && sessao?.atual && ['1', '2', '3', '4'].includes(e.key)) {
        e.preventDefault()
        void avaliarCard((Number(e.key) - 1) as Nota)
      }
    }
    window.addEventListener('keydown', tecla)
    return () => window.removeEventListener('keydown', tecla)
  })

  const aviso = <>
    {notificacao && (
      <div className="fc-notificacao" role="status">
        <span className="fc-notificacao-ic">{notificacao.reativado ? Icone.certo : Icone.suspender}</span>
        <span className="main"><strong>{notificacao.texto}</strong><span>{notificacao.detalhe}</span></span>
        <button type="button" className="link" disabled={salvando} onClick={() => notificacao.reativado ? desfazerReativacao(notificacao.reativado) : desfazer()}>Desfazer</button>
        <button type="button" className="fc-fechar" aria-label="Fechar aviso" onClick={() => setNotificacao(null)}>{Icone.errado}</button>
      </div>
    )}
    {falhaSalvar && <div className="erro-salvar" role="alert">
      <p>{falhaSalvar}</p>
      <button className="link" onClick={() => setFalhaSalvar('')}>
        Fechar
      </button>
    </div>}
  </>

  if (!cards.length && modo === 'aula') return <p className="vazio">Esta aula ainda não tem flashcards.</p>
  if (!cards.length && modo === 'materia') return <p className="vazio">Esta matéria ainda não tem flashcards.</p>

  // ---------- Sessão em andamento ----------
  if (sessao) {
    if (!sessao.atual) {
      return (
        <div className="done">
          <div className="done-ic">{Icone.certo}</div>
          <h2>Sessão concluída</h2>
          <p>
            Você fez {sessao.feitos} {plural(sessao.feitos, 'revisão', 'revisões')}
            {sessao.erros > 0 &&
              `, e ${sessao.erros} ${plural(sessao.erros, 'card voltou', 'cards voltaram')} para a fila depois de um erro`}
            .{proxima && ` O próximo card volta ${fmtQuando(proxima, agora)}.`}
          </p>
          <div className="done-acoes">
            {historico.length > 0 && (
              <button type="button" className="btn ghost" disabled={salvando} onClick={desfazer}>
                {Icone.desfazer}
                <span>Desfazer última ação</span>
              </button>
            )}
            <button className="btn" disabled={salvando} onClick={encerrar}>
              {modo === 'aula' ? 'Voltar aos cards da aula' : modo === 'materia' ? 'Voltar aos cards da matéria' : 'Concluir'}
            </button>
          </div>
          {modo === 'aula' && proximoPasso && <div className="next-steps">{proximoPasso}</div>}
          {aviso}
        </div>
      )
    }

    const card = cards.find((c) => c.id === sessao.atual)!
    const restam = sessao.fila.length + 1
    const progresso = Math.round((100 * sessao.feitos) / (sessao.feitos + restam))
    const iv = intervalos(estadoDe(card))
    const prova = cardDeProva(card)
    const botao = (nota: Nota, rotulo: string, tempo: string) => (
      <button className={`grade g${nota}`} disabled={salvando} onClick={() => avaliarCard(nota)}>
        <b>{rotulo}</b>
        <span>{tempo}</span>
      </button>
    )

    return (
      <div>
        <div className="sess-top">
          <span>
            {restam} {plural(restam, 'card restante', 'cards restantes')}
          </span>
          <div className="sess-acoes">
            {historico.length > 0 && (
              <button
                type="button"
                className="link link-desfazer"
                onClick={desfazer}
                title="Desfazer última ação (Z ou Ctrl+Z)"
                aria-label="Desfazer última ação"
                disabled={salvando}
              >
                {Icone.desfazer}
                <span>Desfazer</span>
              </button>
            )}
            <button className="link" disabled={salvando} onClick={encerrar}>
              Encerrar
            </button>
          </div>
        </div>
        <div
          className="pbar"
          role="progressbar"
          aria-label="Progresso da sessão"
          aria-valuenow={progresso}
          aria-valuemin={0}
          aria-valuemax={100}
        >
          <span style={{ width: `${progresso}%` }} />
        </div>
        <FaixaProva ligada={prova.faixa}>
          <div
            className="flash"
            onClick={sessao.virado ? undefined : () => setSessao({ ...sessao, virado: true })}
            data-act={sessao.virado ? undefined : 'virar'}
          >
            <div className="side">
              {card.materia_nome} · {card.aula_titulo}
            </div>
            <div className="front">{prova.frente}</div>
            {sessao.virado ? (
              <div className="verso">{card.verso}</div>
            ) : (
              <div className="tap">Toque no card para ver a resposta</div>
            )}
          </div>
        </FaixaProva>
        {sessao.virado ? (
          <>
          <div className="fc-suspender-acoes">
            <button type="button" className="fc-suspender" disabled={salvando} onClick={suspenderCard} title="Retirar este card das suas revisões até você reativar">
              {Icone.suspender}<span>Suspender</span>
            </button>
          </div>
          <div className="grades" role="group" aria-label="Como foi lembrar?">
            {botao(0, 'Errei', '10 min')}
            {botao(1, 'Difícil', fmtIntervalo(iv.dificil))}
            {botao(2, 'Bom', fmtIntervalo(iv.bom))}
            {botao(3, 'Fácil', fmtIntervalo(iv.facil))}
          </div>
          </>
        ) : (
          <button className="btn wide" onClick={() => setSessao({ ...sessao, virado: true })}>
            Mostrar resposta
          </button>
        )}
        <p className="hint">No teclado: espaço mostra a resposta; 1 a 4 avaliam; Z desfaz.</p>
        {aviso}
      </div>
    )
  }

  // ---------- Resumo antes de começar ----------
  const contagem = (
    <div className="counts">
      <div className="cp">
        <span className="n">{novos.length}</span>
        <span className="l">Novos</span>
      </div>
      <div className="cp">
        <span className="n">{paraRevisar.length}</span>
        <span className="l">Para revisar</span>
      </div>
      <div className="cp">
        <span className="n">{modo === 'revisao' ? (emDia ?? 0) : emDiaAqui}</span>
        <span className="l">Em dia</span>
      </div>
    </div>
  )

  return (
    <>
      {modo !== 'revisao' && (
        <div className="fc-filtros" role="group" aria-label="Situação dos flashcards">
          <button type="button" className="pill" aria-pressed={!mostrarSuspensos} onClick={() => setMostrarSuspensos(false)}>Ativos <span>{cardsAtivos.length}</span></button>
          <button type="button" className="pill" aria-pressed={mostrarSuspensos} onClick={() => setMostrarSuspensos(true)}>{Icone.suspender} Suspensos <span>{cardsSuspensos.length}</span></button>
        </div>
      )}
      {!mostrarSuspensos && <div className="fc-sum">
        {contagem}
        {pendentes > 0 ? (
          <button className="btn wide" onClick={() => comecar(false)}>
            {modo === 'revisao' ? 'Revisar' : 'Estudar'} {pendentes} {plural(pendentes, 'card', 'cards')}
          </button>
        ) : (
          <>
            <p className="muted">
              {cardsSuspensos.length > 0 && !cardsAtivos.length ? 'Todos os cards estão suspensos. Abra Suspensos para reativar.' : <>
              {modo === 'aula' ? 'Tudo em dia nesta aula.' : modo === 'materia' ? 'Tudo em dia nesta matéria.' : 'Tudo em dia.'}
              {proxima && ` O próximo card volta ${fmtQuando(proxima, agora)}.`}
              </>}
            </p>
            {modo !== 'revisao' && cardsAtivos.length > 0 && (
              <button className="btn ghost wide" onClick={() => comecar(true)}>
                Treinar todos mesmo assim
              </button>
            )}
            {modo === 'aula' && proximoPasso && <div className="next-steps">{proximoPasso}</div>}
          </>
        )}
      </div>}

      {mostrarSuspensos && (
        <section aria-label="Flashcards suspensos">
          <p className="foot fc-suspensos-nota">Estes cards não aparecem nas suas revisões. Ao reativar, o histórico e os intervalos ficam preservados.</p>
          {cardsSuspensos.length === 0 ? <p className="vazio">Nenhum card suspenso {modo === 'aula' ? 'nesta aula' : 'nesta matéria'}.</p> : (
            <div className="group">
              {cardsSuspensos.map((c) => (
                <div className="row static fc-suspenso" key={c.id}>
                  <span className="main"><span className="t2">{c.frente}</span><span className="s">{c.aula_titulo}</span></span>
                  <div className="fc-suspenso-acoes">
                    <span className="chip novo">{Icone.suspender} Suspenso</span>
                    <button type="button" className="btn sm" disabled={salvando} onClick={() => reativarCard(c.id)} aria-label={`Reativar: ${c.frente}`}>{Icone.desfazer}<span>Reativar</span></button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      )}

      {modo === 'aula' && !mostrarSuspensos && (
        <>
          <div className="sec">Cards desta aula</div>
          <div className="group">
            {cardsAtivos.map((c) => {
              const st = statusDe(c)
              const s = estadoDe(c)
              const rotulo = st === 'novo' ? 'Novo' : st === 'revisar' ? 'Revisar agora' : `Volta ${fmtQuando(s!.proxima_revisao, agora)}`
              return (
                <div key={c.id} className="row static">
                  <span className="main">
                    <span className="t2">{c.frente}</span>
                  </span>
                  <span className={`chip ${st}`}>{rotulo}</span>
                </div>
              )
            })}
          </div>
        </>
      )}
      {modo === 'materia' && !mostrarSuspensos && (
        <>
          <div className="sec">Cards por aula</div>
          <div className="group">
            {[...porAula.values()].map(({ id, ordem, titulo, lista }) => {
              const novosAula = lista.filter((c) => statusDe(c) === 'novo').length
              const revisarAula = lista.filter((c) => statusDe(c) === 'revisar').length
              return (
                <Link key={id} className="row" href={`/aula/${id}?aba=flashcards`}>
                  <span className="num">{ordem}</span>
                  <span className="main">
                    <span className="t">{titulo}</span>
                    <span className="meta">
                      {lista.length} {plural(lista.length, 'flashcard', 'flashcards')}
                      {novosAula > 0 && ` · ${novosAula} ${plural(novosAula, 'novo', 'novos')}`}
                      {revisarAula > 0 && <span className="chip revisar">{revisarAula} para revisar</span>}
                    </span>
                  </span>
                  {Icone.seta}
                </Link>
              )
            })}
          </div>
        </>
      )}
      {aviso}
    </>
  )
}
