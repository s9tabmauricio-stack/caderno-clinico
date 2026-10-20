'use client'

import { useState } from 'react'
import Link from 'next/link'
import type { CardAluno, QuestaoAluno } from '@/lib/dados'
import { Icone } from './Icones'
import { Questoes } from './Questoes'
import { Flashcards } from './Flashcards'

export type Aba = 'apostila' | 'questoes' | 'flashcards'

type Props = {
  aulaId: string
  abaInicial: Aba
  apostilaHtml: string | null
  pdfUrl: string | null
  questoes: QuestaoAluno[]
  cards: CardAluno[]
  userId: string
  materiaId: string
  materiaNome?: string
  totalBanco: number
  // próxima aula publicada da matéria, se houver
  proximaAula: { id: string; titulo: string } | null
  edicao?: { aulas: { id: string; titulo: string }[] }
}

export function AulaAbas({
  aulaId,
  abaInicial,
  apostilaHtml,
  pdfUrl,
  questoes,
  cards,
  userId,
  materiaId,
  materiaNome,
  totalBanco,
  proximaAula,
  edicao,
}: Props) {
  const [aba, setAba] = useState<Aba>(abaInicial)

  function trocar(nova: Aba, rolar = false) {
    setAba(nova)
    const url = new URL(window.location.href)
    url.searchParams.set('aba', nova)
    window.history.replaceState(null, '', url)
    if (rolar) document.querySelector('.segm')?.scrollIntoView({ block: 'start', behavior: 'smooth' })
  }

  const abas: [Aba, string][] = [
    ['apostila', 'Apostila'],
    ['questoes', 'Questões'],
    ['flashcards', 'Flashcards'],
  ]

  // Próximo passo mostrado quando o aluno termina as questões ou os cards da aula
  const irParaProxima = proximaAula && (
    <Link className="btn ghost" href={`/aula/${proximaAula.id}`}>
      Próxima aula: {proximaAula.titulo}
    </Link>
  )
  const passoDepoisDasQuestoes = (cards.length > 0 || proximaAula) && (
    <>
      {cards.length > 0 && (
        <button className="btn" onClick={() => trocar('flashcards', true)}>
          Estudar os {cards.length} flashcards
        </button>
      )}
      {irParaProxima}
    </>
  )
  const passoDepoisDosCards = (questoes.length > 0 || proximaAula) && (
    <>
      {questoes.length > 0 && (
        <button className="btn" onClick={() => trocar('questoes', true)}>
          Fazer as {questoes.length} questões
        </button>
      )}
      {irParaProxima}
    </>
  )

  return (
    <>
      <div className="segm" role="tablist" aria-label="Conteúdo da aula">
        {abas.map(([chave, rotulo]) => (
          <button
            key={chave}
            role="tab"
            id={`aba-${chave}`}
            aria-selected={aba === chave}
            aria-controls={`painel-${chave}`}
            className={aba === chave ? 'on' : ''}
            onClick={() => trocar(chave)}
          >
            {rotulo}
          </button>
        ))}
      </div>

      <div className="pane" role="tabpanel" id="painel-apostila" aria-labelledby="aba-apostila" hidden={aba !== 'apostila'}>
        {pdfUrl && (
          <div className="pdfbar">
            <span className="pdf-ic">{Icone.arquivo}</span>
            <span className="main">
              <span className="t">Apostila completa em PDF</span>
              <span className="s">Abre numa nova aba.</span>
            </span>
            <a className="btn ghost sm" href={pdfUrl} target="_blank" rel="noopener">
              Abrir
            </a>
          </div>
        )}
        {apostilaHtml ? (
          <article className="ap" dangerouslySetInnerHTML={{ __html: apostilaHtml }} />
        ) : (
          <p className="vazio">O resumo desta aula ainda não foi publicado.</p>
        )}
        <div className="next-steps">
          {questoes.length > 0 && (
            <button className="btn" onClick={() => trocar('questoes', true)}>
              Fazer as {questoes.length} questões
            </button>
          )}
          {cards.length > 0 && (
            <button className="btn ghost" onClick={() => trocar('flashcards', true)}>
              Estudar os flashcards
            </button>
          )}
        </div>
      </div>

      <div className="pane" role="tabpanel" id="painel-questoes" aria-labelledby="aba-questoes" hidden={aba !== 'questoes'}>
        <Questoes
          questoes={questoes}
          userId={userId}
          ativo={aba === 'questoes'}
          rotulo={materiaNome}
          edicao={edicao}
          proximoPasso={passoDepoisDasQuestoes || undefined}
          vazio="Nenhuma questão das provas anteriores é sobre o assunto desta aula. Treine pelo banco de questões da matéria."
        />
        {totalBanco > questoes.length && (
          <Link className="btn ghost wide" style={{ marginTop: 16 }} href={`/materia/${materiaId}/questoes?de=aula:${aulaId}`}>
            Ver as {totalBanco} questões do banco da matéria
          </Link>
        )}
      </div>

      <div
        className="pane estreito"
        role="tabpanel"
        id="painel-flashcards"
        aria-labelledby="aba-flashcards"
        hidden={aba !== 'flashcards'}
      >
        <Flashcards cards={cards} userId={userId} modo="aula" ativo={aba === 'flashcards'} proximoPasso={passoDepoisDosCards || undefined} />
      </div>
    </>
  )
}
