'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useSearchParams } from 'next/navigation'
import type { CardAluno, QuestaoAluno } from '@/lib/dados'
import { FONTES_QUESTAO, fonteDaQuestao, fonteValida, type FonteQuestao } from '@/lib/classificacao-questoes'
import { Icone } from './Icones'
import { Questoes } from './Questoes'
import { Flashcards } from './Flashcards'
import { Apostila } from './Apostila'
import { FlashcardsDiaD, type CardDiaD } from './FlashcardsDiaD'

export type Aba = 'apostila' | 'questoes' | 'flashcards' | 'diad'


type Props = {
  aulaId: string
  abaInicial: Aba
  apostilaHtml: string | null
  pdfUrl: string | null
  questoes: QuestaoAluno[]
  cards: CardAluno[]
  // Flashcards Dia D: baralho de véspera para as questões das Provas da FAG (a aba só aparece se houver)
  cardsDiaD: CardDiaD[]
  userId: string
  materiaId: string
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
  cardsDiaD,
  userId,
  materiaId,
  totalBanco,
  proximaAula,
  edicao,
}: Props) {
  const parametros = useSearchParams()
  const contexto = new URLSearchParams(parametros.toString())
  contexto.set('aba', 'questoes')
  const voltarParaAula = `/aula/${aulaId}?${contexto}`
  const [aba, setAba] = useState<Aba>(abaInicial)

  // Segunda barra, só na aba Questões: de onde veio a questão (regra do Mauricio, 08/11/2026).
  // Respostas e marcações dadas nesta visita ficam guardadas aqui, para valerem ao trocar de grupo.
  const [extras, setExtras] = useState<Record<string, QuestaoAluno['resposta']>>({})
  const [marcas, setMarcas] = useState<Record<string, QuestaoAluno['classificacao']>>({})
  const atuais = questoes.map((q) => ({
    ...q,
    resposta: q.id in extras ? extras[q.id] : q.resposta,
    classificacao: q.id in marcas ? marcas[q.id] : q.classificacao,
  }))
  const grupos = FONTES_QUESTAO.map((g) => ({ ...g, lista: atuais.filter((q) => fonteDaQuestao(q) === g.valor) }))
  const [fonte, setFonte] = useState<FonteQuestao>(() => {
    const pedida = fonteValida(parametros.get('fonte'))
    return pedida ?? grupos.find((g) => g.lista.length)?.valor ?? 'fag'
  })
  // A lista em estudo só muda quando o aluno troca de grupo, para não pular questões no meio
  const [lista, setLista] = useState(() => grupos.find((g) => g.valor === fonte)!.lista)
  const grupo = grupos.find((g) => g.valor === fonte)!
  const proximoGrupo = grupos.slice(grupos.indexOf(grupo) + 1).find((g) => g.lista.length)

  function trocarFonte(nova: FonteQuestao, rolar = false) {
    setFonte(nova)
    setLista(grupos.find((g) => g.valor === nova)!.lista)
    const url = new URL(window.location.href)
    url.searchParams.set('fonte', nova)
    window.history.replaceState(null, '', url)
    if (rolar) document.querySelector('.segm')?.scrollIntoView({ block: 'start', behavior: 'smooth' })
  }

  function trocar(nova: Aba, rolar = false) {
    setAba(nova)
    const url = new URL(window.location.href)
    url.searchParams.set('aba', nova)
    window.history.replaceState(null, '', url)
    if (rolar) document.querySelector('.segm')?.scrollIntoView({ block: 'start', behavior: 'smooth' })
  }

  const abas: [Aba, React.ReactNode][] = [
    ['apostila', 'Apostila'],
    ['questoes', 'Questões'],
    ['flashcards', 'Flashcards'],
  ]
  if (cardsDiaD.length) abas.push(['diad', <>Flashcards <span className="nw">Dia D</span></>])
  // Rótulo de cada questão da aula (ex.: "P2 · nº 10"), mostrado no card do Dia D que ajuda nela
  const rotulosQuestoes = Object.fromEntries(questoes.map((q) => [q.id, q.fonte ?? q.prova ?? '']))

  // Próximo passo mostrado quando o aluno termina as questões ou os cards da aula
  const irParaProxima = proximaAula && (
    <Link className="btn ghost" href={`/aula/${proximaAula.id}`}>
      Próxima aula: {proximaAula.titulo}
    </Link>
  )
  const passoDepoisDasQuestoes = (proximoGrupo || cards.length > 0 || proximaAula) && (
    <>
      {proximoGrupo && (
        <button className="btn" onClick={() => trocarFonte(proximoGrupo.valor, true)}>
          Ir para {proximoGrupo.rotulo} ({proximoGrupo.lista.length})
        </button>
      )}
      {cards.length > 0 && (
        <button className={proximoGrupo ? 'btn ghost' : 'btn'} onClick={() => trocar('flashcards', true)}>
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
      <div className={`segm segm-aula${abas.length > 3 ? ' quatro' : ''}`} role="tablist" aria-label="Conteúdo da aula">
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

      {aba === 'questoes' && questoes.length > 0 && (
        <div className="segm segm-fonte" role="tablist" aria-label="De onde vêm as questões">
          {grupos.map((g) => (
            <button
              key={g.valor}
              role="tab"
              aria-selected={fonte === g.valor}
              aria-controls="painel-questoes"
              className={fonte === g.valor ? 'on' : ''}
              onClick={() => trocarFonte(g.valor)}
            >
              {g.rotulo} <small>{g.lista.length}</small>
            </button>
          ))}
        </div>
      )}

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
          <Apostila html={apostilaHtml} />
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
          key={fonte}
          questoes={lista}
          userId={userId}
          ativo={aba === 'questoes'}
          edicao={edicao}
          proximoPasso={passoDepoisDasQuestoes || undefined}
          vazio={questoes.length ? `${grupo.vazio} nesta aula.` : 'Esta aula ainda não tem questões. Treine pelo banco de questões da matéria.'}
          aoResponder={(id, r) => setExtras((e) => ({ ...e, [id]: r }))}
          aoClassificar={(id, valor) => setMarcas((m) => ({ ...m, [id]: valor }))}
        />
        {totalBanco > questoes.length && (
          <Link className="btn ghost wide" style={{ marginTop: 16 }} href={`/materia/${materiaId}/questoes?${new URLSearchParams({ de: `aula:${aulaId}`, retorno: voltarParaAula })}`}>
            Ver as {totalBanco} questões do banco da matéria
          </Link>
        )}
      </div>

      <div className="pane" role="tabpanel" id="painel-flashcards" aria-labelledby="aba-flashcards" hidden={aba !== 'flashcards'}>
        <p className="foot">Estude livremente os cards desta aula. Suas avaliações atualizam a próxima revisão. <Link href={`/revisao?materia=${materiaId}`}>Ver a fila de hoje</Link>.</p>
        <Flashcards cards={cards} userId={userId} modo="aula" ativo={aba === 'flashcards'} proximoPasso={passoDepoisDosCards || undefined} />
      </div>

      {cardsDiaD.length > 0 && (
        <div className="pane" role="tabpanel" id="painel-diad" aria-labelledby="aba-diad" hidden={aba !== 'diad'}>
          <FlashcardsDiaD
            cards={cardsDiaD}
            rotulos={rotulosQuestoes}
            ativo={aba === 'diad'}
            irParaQuestoes={() => {
              trocarFonte('fag')
              trocar('questoes', true)
            }}
          />
        </div>
      )}
    </>
  )
}
