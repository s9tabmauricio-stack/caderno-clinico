'use client'

import { useEffect, useMemo, useRef, useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { plural } from '@/lib/formato'
import { comecarDiaD, responderDiaD, type ProgressoDiaD } from '@/lib/dia-d-progresso'
import { Icone } from './Icones'

// Flashcards Dia D (regra do Mauricio, 10/11/2026): baralho de véspera da aula, feito para resolver
// as questões das Provas da FAG. Fica fora da Revisão do dia: "Não sabia" manda o card para o fim da
// fila, até o aluno acertar todos. O progresso fica na conta do aluno (tabela progresso_dia_d), para
// ele sair da aula e continuar de onde parou, em qualquer aparelho.

export type CardDiaD = { id: string; frente: string; verso: string; questoes: string[] }

type Props = {
  aulaId: string
  userId: string
  cards: CardDiaD[]
  // progresso guardado na conta, já acertado com os cards de hoje (null = nunca começou ou recomeçou)
  progresso: ProgressoDiaD | null
  // id da questão FAG → como ela aparece na aula (ex.: "P2 · nº 10")
  rotulos: Record<string, string>
  ativo: boolean
  // depois de fechar o baralho: ir para as questões das Provas da FAG da aula
  irParaQuestoes?: () => void
}

export function FlashcardsDiaD({ aulaId, userId, cards, progresso: inicial, rotulos, ativo, irParaQuestoes }: Props) {
  const supabase = useMemo(() => createClient(), [])
  // progresso: o que está guardado na conta; aberto: mostrando o baralho (cards ou fim) em vez do resumo
  const [progresso, setProgresso] = useState<ProgressoDiaD | null>(inicial)
  const [aberto, setAberto] = useState(false)
  const [virado, setVirado] = useState(false)
  const [falhaSalvar, setFalhaSalvar] = useState('')
  // As gravações vão uma de cada vez, na ordem: a última resposta é sempre a que fica no banco.
  const gravacoes = useRef<Promise<void>>(Promise.resolve())
  const totalQuestoes = new Set(cards.flatMap((c) => c.questoes)).size
  const rotuloDe = (c: CardDiaD) => c.questoes.map((id) => rotulos[id]).filter(Boolean).join(' · ')

  function guardar(p: ProgressoDiaD) {
    setProgresso(p)
    gravacoes.current = gravacoes.current.then(async () => {
      const { error } = await supabase
        .from('progresso_dia_d')
        .upsert({ user_id: userId, aula_id: aulaId, ...p, atualizado_em: new Date().toISOString() }, { onConflict: 'user_id,aula_id' })
      setFalhaSalvar(error ? 'Não deu para guardar o seu progresso do Dia D. Confira sua internet; ele fica guardado na próxima resposta.' : '')
    })
  }

  function abrir() {
    setAberto(true)
    setVirado(false)
    document.querySelector('.segm')?.scrollIntoView({ block: 'start', behavior: 'smooth' })
  }

  function comecar(ids: string[]) {
    guardar(comecarDiaD(ids))
    abrir()
  }

  function responder(sabia: boolean) {
    if (!progresso?.fila.length) return
    guardar(responderDiaD(progresso, sabia))
    setVirado(false)
  }

  const sessao = aberto ? progresso : null

  // Atalhos: espaço mostra a resposta; 1 = não sabia; 2 = sabia
  useEffect(() => {
    if (!ativo || !sessao?.fila.length) return
    function tecla(e: KeyboardEvent) {
      const alvo = e.target as HTMLElement
      if (e.metaKey || e.ctrlKey || e.altKey || alvo.closest('input, textarea, button, a, [contenteditable="true"]')) return
      if (!virado && (e.key === ' ' || e.key === 'Enter')) {
        e.preventDefault()
        setVirado(true)
      } else if (virado && (e.key === '1' || e.key === '2')) {
        e.preventDefault()
        responder(e.key === '2')
      }
    }
    window.addEventListener('keydown', tecla)
    return () => window.removeEventListener('keydown', tecla)
  })

  if (!cards.length) return <p className="vazio">Esta aula ainda não tem flashcards do Dia D.</p>

  const aviso = falhaSalvar && (
    <div className="erro-salvar" role="alert">
      <p>{falhaSalvar}</p>
    </div>
  )

  // ---------- Baralho fechado ----------
  if (sessao && !sessao.fila.length) {
    const errados = sessao.erros
    return (
      <div className="done">
        <div className="done-ic">{Icone.certo}</div>
        <h2>Dia D fechado</h2>
        <p>
          Você passou pelos {sessao.feitos} {plural(sessao.feitos, 'card', 'cards')}
          {errados.length > 0
            ? `; ${errados.length} ${plural(errados.length, 'precisou', 'precisaram')} de mais de uma volta.`
            : ' e sabia todos de primeira.'}
        </p>
        <div className="done-acoes">
          {errados.length > 0 && (
            <button className="btn ghost" onClick={() => comecar(errados)}>
              {errados.length === 1 ? 'Repetir o que errei' : `Repetir os ${errados.length} que errei`}
            </button>
          )}
          <button className="btn ghost" onClick={() => setAberto(false)}>
            Voltar ao Dia D
          </button>
        </div>
        {irParaQuestoes && (
          <div className="next-steps">
            <button className="btn" onClick={irParaQuestoes}>
              Fazer as questões das Provas da FAG
            </button>
          </div>
        )}
        {aviso}
      </div>
    )
  }

  // ---------- Sessão em andamento ----------
  if (sessao) {
    const card = cards.find((c) => c.id === sessao.fila[0])
    if (!card) return null
    const restam = sessao.fila.length
    const progresso = Math.round((100 * sessao.feitos) / (sessao.feitos + restam))
    const ajuda = rotuloDe(card)
    return (
      <div>
        <div className="sess-top">
          <span>
            {restam} {plural(restam, 'card restante', 'cards restantes')}
          </span>
          <div className="sess-acoes">
            <button className="link" onClick={() => setAberto(false)}>
              Pausar
            </button>
          </div>
        </div>
        <div className="pbar" role="progressbar" aria-label="Progresso do Dia D" aria-valuenow={progresso} aria-valuemin={0} aria-valuemax={100}>
          <span style={{ width: `${progresso}%` }} />
        </div>
        <div
          className="flash"
          onClick={virado ? undefined : () => setVirado(true)}
          data-act={virado ? undefined : 'virar'}
        >
          <div className="side">Dia D · Provas da FAG</div>
          <div className="front">{card.frente}</div>
          {virado ? (
            <>
              <div className="verso">{card.verso}</div>
              {ajuda && <div className="diad-ajuda">Ajuda na questão {ajuda}</div>}
            </>
          ) : (
            <div className="tap">Toque no card para ver a resposta</div>
          )}
        </div>
        {virado ? (
          <div className="grades grades-2" role="group" aria-label="Você sabia?">
            <button className="grade g0" onClick={() => responder(false)}>
              <b>Não sabia</b>
              <span>volta no fim</span>
            </button>
            <button className="grade g2" onClick={() => responder(true)}>
              <b>Sabia</b>
              <span>próximo</span>
            </button>
          </div>
        ) : (
          <button className="btn wide" onClick={() => setVirado(true)}>
            Mostrar resposta
          </button>
        )}
        <p className="hint">No teclado: espaço mostra a resposta; 1 = não sabia; 2 = sabia. Seu progresso fica guardado: pode sair e continuar depois.</p>
        {aviso}
      </div>
    )
  }

  // ---------- Resumo antes de começar ----------
  return (
    <>
      <p className="foot">
        Baralho de véspera: cada card ensina o que cai nas Provas da FAG desta aula. Não entra na Revisão do dia; o card que você
        não souber volta no fim, até fechar todos.
      </p>
      <div className="fc-sum">
        <div className="counts counts-2">
          <div className="cp">
            <span className="n">{cards.length}</span>
            <span className="l">{plural(cards.length, 'Card', 'Cards')}</span>
          </div>
          <div className="cp">
            <span className="n">{totalQuestoes}</span>
            <span className="l">{plural(totalQuestoes, 'Questão da FAG', 'Questões da FAG')}</span>
          </div>
        </div>
        {progresso?.fila.length ? (
          <>
            <button className="btn wide" onClick={abrir}>
              Continuar de onde parei · {progresso.fila.length} {plural(progresso.fila.length, 'card restante', 'cards restantes')}
            </button>
            <button className="btn ghost wide" onClick={() => comecar(cards.map((c) => c.id))}>
              Recomeçar do zero
            </button>
          </>
        ) : progresso ? (
          <>
            <button className="btn wide" onClick={abrir}>
              Ver como fechei o Dia D
            </button>
            <button className="btn ghost wide" onClick={() => comecar(cards.map((c) => c.id))}>
              Estudar os {cards.length} {plural(cards.length, 'card', 'cards')} de novo
            </button>
          </>
        ) : (
          <button className="btn wide" onClick={() => comecar(cards.map((c) => c.id))}>
            Estudar os {cards.length} {plural(cards.length, 'card', 'cards')} do Dia D
          </button>
        )}
      </div>
      {aviso}
      <div className="sec">Cards do Dia D</div>
      <div className="group">
        {cards.map((c) => (
          <div key={c.id} className="row static">
            <span className="main">
              <span className="t2">{c.frente}</span>
              {rotuloDe(c) && <span className="s">{rotuloDe(c)}</span>}
            </span>
          </div>
        ))}
      </div>
    </>
  )
}
