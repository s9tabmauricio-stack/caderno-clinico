'use client'

import { useEffect, useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'
import type { CardAluno } from '@/lib/dados'
import { avaliar, intervalos, vencido, type EstadoCard, type Nota } from '@/lib/srs'
import { fmtIntervalo, fmtQuando, plural } from '@/lib/formato'
import { Icone } from './Icones'

type Props = {
  cards: CardAluno[]
  userId: string
  // "aula": todos os cards de uma aula; "revisao": a fila do dia (vencidos + novos)
  modo: 'aula' | 'revisao'
  ativo: boolean
  emDia?: number // em "revisao", quantos cards estão em dia (não vêm na lista)
}

type Sessao = { fila: string[]; atual: string | null; virado: boolean; feitos: number; erros: number }

export function Flashcards({ cards, userId, modo, ativo, emDia }: Props) {
  const supabase = useMemo(() => createClient(), [])
  const router = useRouter()
  // Estados alterados nesta visita; o resto vem do servidor
  const [locais, setLocais] = useState<Record<string, EstadoCard>>({})
  const [sessao, setSessao] = useState<Sessao | null>(null)
  const [falhaSalvar, setFalhaSalvar] = useState('')
  const [agora, setAgora] = useState(() => Date.now())

  const estadoDe = (c: CardAluno) => locais[c.id] ?? c.estado
  const statusDe = (c: CardAluno) => {
    const s = estadoDe(c)
    return !s ? 'novo' : vencido(s, agora) ? 'revisar' : 'emdia'
  }

  const novos = cards.filter((c) => statusDe(c) === 'novo')
  const paraRevisar = cards
    .filter((c) => statusDe(c) === 'revisar')
    .sort((a, b) => (estadoDe(a)?.proxima_revisao ?? '').localeCompare(estadoDe(b)?.proxima_revisao ?? ''))
  const emDiaAqui = cards.filter((c) => statusDe(c) === 'emdia').length
  const pendentes = paraRevisar.length + novos.length

  const proxima = cards
    .map((c) => estadoDe(c))
    .filter((s): s is EstadoCard => s !== null && new Date(s.proxima_revisao).getTime() > agora)
    .map((s) => s.proxima_revisao)
    .sort()[0]

  function comecar(todos: boolean) {
    const lista = todos ? cards : [...paraRevisar, ...novos]
    if (!lista.length) return
    const ids = lista.map((c) => c.id)
    setFalhaSalvar('')
    setSessao({ fila: ids.slice(1), atual: ids[0], virado: false, feitos: 0, erros: 0 })
  }

  async function avaliarCard(nota: Nota) {
    if (!sessao?.atual || !sessao.virado) return
    const card = cards.find((c) => c.id === sessao.atual)
    if (!card) return
    const t = Date.now()
    const novo = avaliar(estadoDe(card), nota, t)
    setLocais((l) => ({ ...l, [card.id]: novo }))
    const fila = [...sessao.fila]
    if (nota === 0) fila.push(card.id)
    setSessao({
      fila: fila.slice(1),
      atual: fila[0] ?? null,
      virado: false,
      feitos: sessao.feitos + 1,
      erros: sessao.erros + (nota === 0 ? 1 : 0),
    })
    setAgora(t)
    const { error } = await supabase
      .from('revisoes')
      .upsert({ user_id: userId, flashcard_id: card.id, ...novo }, { onConflict: 'user_id,flashcard_id' })
    if (error) setFalhaSalvar('Não deu para salvar a última revisão. Confira a internet; o card vai aparecer de novo.')
  }

  function encerrar() {
    setSessao(null)
    setAgora(Date.now())
    router.refresh() // atualiza contadores e a fila do dia
  }

  // Atalhos: espaço mostra a resposta; 1 a 4 avaliam
  useEffect(() => {
    if (!ativo || !sessao?.atual) return
    function tecla(e: KeyboardEvent) {
      const alvo = e.target as HTMLElement
      if (e.metaKey || e.ctrlKey || e.altKey || alvo.closest('input, textarea')) return
      if ((e.key === ' ' || e.key === 'Enter') && alvo.closest('button, a')) return
      if (!sessao?.virado && (e.key === ' ' || e.key === 'Enter')) {
        e.preventDefault()
        setSessao((s) => (s ? { ...s, virado: true } : s))
      } else if (sessao?.virado && ['1', '2', '3', '4'].includes(e.key)) {
        e.preventDefault()
        void avaliarCard((Number(e.key) - 1) as Nota)
      }
    }
    window.addEventListener('keydown', tecla)
    return () => window.removeEventListener('keydown', tecla)
  })

  const aviso = falhaSalvar && (
    <div className="erro-salvar" role="alert">
      <p>{falhaSalvar}</p>
      <button className="link" onClick={() => setFalhaSalvar('')}>
        Fechar
      </button>
    </div>
  )

  if (!cards.length && modo === 'aula') return <p className="vazio">Esta aula ainda não tem flashcards.</p>

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
          <button className="btn" onClick={encerrar}>
            {modo === 'aula' ? 'Voltar aos cards da aula' : 'Concluir'}
          </button>
          {aviso}
        </div>
      )
    }

    const card = cards.find((c) => c.id === sessao.atual)!
    const restam = sessao.fila.length + 1
    const progresso = Math.round((100 * sessao.feitos) / (sessao.feitos + restam))
    const iv = intervalos(estadoDe(card))
    const botao = (nota: Nota, rotulo: string, tempo: string) => (
      <button className={`grade g${nota}`} onClick={() => avaliarCard(nota)}>
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
          <button className="link" onClick={encerrar}>
            Encerrar
          </button>
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
        <div
          className="flash"
          onClick={sessao.virado ? undefined : () => setSessao({ ...sessao, virado: true })}
          data-act={sessao.virado ? undefined : 'virar'}
        >
          <div className="side">
            {card.materia_nome} · {card.aula_titulo}
          </div>
          <div className="front">{card.frente}</div>
          {sessao.virado ? (
            <div className="verso">{card.verso}</div>
          ) : (
            <div className="tap">Toque no card para ver a resposta</div>
          )}
        </div>
        {sessao.virado ? (
          <div className="grades" role="group" aria-label="Como foi lembrar?">
            {botao(0, 'Errei', '10 min')}
            {botao(1, 'Difícil', fmtIntervalo(iv.dificil))}
            {botao(2, 'Bom', fmtIntervalo(iv.bom))}
            {botao(3, 'Fácil', fmtIntervalo(iv.facil))}
          </div>
        ) : (
          <button className="btn wide" onClick={() => setSessao({ ...sessao, virado: true })}>
            Mostrar resposta
          </button>
        )}
        <p className="hint">No teclado: espaço mostra a resposta; as teclas 1 a 4 avaliam.</p>
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
      <div className="fc-sum">
        {contagem}
        {pendentes > 0 ? (
          <button className="btn wide" onClick={() => comecar(false)}>
            {modo === 'aula' ? 'Estudar' : 'Revisar'} {pendentes} {plural(pendentes, 'card', 'cards')}
          </button>
        ) : (
          <>
            <p className="muted">
              {modo === 'aula' ? 'Tudo em dia nesta aula.' : 'Tudo em dia.'}
              {proxima && ` O próximo card volta ${fmtQuando(proxima, agora)}.`}
            </p>
            {modo === 'aula' && (
              <button className="btn ghost wide" onClick={() => comecar(true)}>
                Treinar todos mesmo assim
              </button>
            )}
          </>
        )}
      </div>

      {modo === 'aula' && (
        <>
          <div className="sec">Cards desta aula</div>
          <div className="group">
            {cards.map((c) => {
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
      {aviso}
    </>
  )
}
