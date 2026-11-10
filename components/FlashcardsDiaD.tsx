'use client'

import { useEffect, useState } from 'react'
import { plural } from '@/lib/formato'
import { Icone } from './Icones'

// Flashcards Dia D (regra do Mauricio, 10/11/2026): baralho de véspera da aula, feito para resolver
// as questões das Provas da FAG. Fica fora da Revisão do dia e não grava nada: "Não sabia" só manda
// o card para o fim da fila desta sessão, até o aluno acertar todos.

export type CardDiaD = { id: string; frente: string; verso: string; questoes: string[] }

type Props = {
  cards: CardDiaD[]
  // id da questão FAG → como ela aparece na aula (ex.: "P2 · nº 10")
  rotulos: Record<string, string>
  ativo: boolean
  // depois de fechar o baralho: ir para as questões das Provas da FAG da aula
  irParaQuestoes?: () => void
}

type Sessao = { fila: string[]; virado: boolean; feitos: number; erros: string[] }

export function FlashcardsDiaD({ cards, rotulos, ativo, irParaQuestoes }: Props) {
  const [sessao, setSessao] = useState<Sessao | null>(null)
  const totalQuestoes = new Set(cards.flatMap((c) => c.questoes)).size
  const rotuloDe = (c: CardDiaD) => c.questoes.map((id) => rotulos[id]).filter(Boolean).join(' · ')

  function comecar(ids: string[]) {
    setSessao({ fila: ids, virado: false, feitos: 0, erros: [] })
    document.querySelector('.segm')?.scrollIntoView({ block: 'start', behavior: 'smooth' })
  }

  function responder(sabia: boolean) {
    setSessao((s) => {
      if (!s || !s.fila.length) return s
      const [atual, ...resto] = s.fila
      return {
        fila: sabia ? resto : [...resto, atual],
        virado: false,
        feitos: s.feitos + (sabia ? 1 : 0),
        erros: sabia || s.erros.includes(atual) ? s.erros : [...s.erros, atual],
      }
    })
  }

  // Atalhos: espaço mostra a resposta; 1 = não sabia; 2 = sabia
  useEffect(() => {
    if (!ativo || !sessao?.fila.length) return
    function tecla(e: KeyboardEvent) {
      const alvo = e.target as HTMLElement
      if (e.metaKey || e.ctrlKey || e.altKey || alvo.closest('input, textarea, button, a, [contenteditable="true"]')) return
      if (!sessao?.virado && (e.key === ' ' || e.key === 'Enter')) {
        e.preventDefault()
        setSessao((s) => (s ? { ...s, virado: true } : s))
      } else if (sessao?.virado && (e.key === '1' || e.key === '2')) {
        e.preventDefault()
        responder(e.key === '2')
      }
    }
    window.addEventListener('keydown', tecla)
    return () => window.removeEventListener('keydown', tecla)
  })

  if (!cards.length) return <p className="vazio">Esta aula ainda não tem flashcards do Dia D.</p>

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
          <button className="btn ghost" onClick={() => setSessao(null)}>
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
      </div>
    )
  }

  // ---------- Sessão em andamento ----------
  if (sessao) {
    const card = cards.find((c) => c.id === sessao.fila[0])!
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
            <button className="link" onClick={() => setSessao(null)}>
              Encerrar
            </button>
          </div>
        </div>
        <div className="pbar" role="progressbar" aria-label="Progresso do Dia D" aria-valuenow={progresso} aria-valuemin={0} aria-valuemax={100}>
          <span style={{ width: `${progresso}%` }} />
        </div>
        <div
          className="flash"
          onClick={sessao.virado ? undefined : () => setSessao({ ...sessao, virado: true })}
          data-act={sessao.virado ? undefined : 'virar'}
        >
          <div className="side">Dia D · Provas da FAG</div>
          <div className="front">{card.frente}</div>
          {sessao.virado ? (
            <>
              <div className="verso">{card.verso}</div>
              {ajuda && <div className="diad-ajuda">Ajuda na questão {ajuda}</div>}
            </>
          ) : (
            <div className="tap">Toque no card para ver a resposta</div>
          )}
        </div>
        {sessao.virado ? (
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
          <button className="btn wide" onClick={() => setSessao({ ...sessao, virado: true })}>
            Mostrar resposta
          </button>
        )}
        <p className="hint">No teclado: espaço mostra a resposta; 1 = não sabia; 2 = sabia.</p>
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
        <button className="btn wide" onClick={() => comecar(cards.map((c) => c.id))}>
          Estudar os {cards.length} {plural(cards.length, 'card', 'cards')} do Dia D
        </button>
      </div>
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
