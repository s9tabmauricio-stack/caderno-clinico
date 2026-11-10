'use client'

import { useActionState, useState } from 'react'
import { useFormStatus } from 'react-dom'
import { apagarAula, apagarCard, apagarCardsDaAula, apagarCardsDiaDaAula, apagarQuestao, limparVersoesAntigas, salvarAula, salvarCard, salvarQuestao, type Msg } from '@/app/admin/conteudo/acoes'

const LETRAS = 'ABCDE'

function Mensagem({ m }: { m: Msg }) {
  if (!m) return null
  return (
    <p className={m.ok ? 'ok-msg' : 'err'} role="status">
      {m.texto}
    </p>
  )
}

function BotaoEnviar({ rotulo, enviando }: { rotulo: string; enviando: string }) {
  const { pending } = useFormStatus()
  return (
    <button className="btn sm" type="submit" disabled={pending}>
      {pending ? enviando : rotulo}
    </button>
  )
}

/** Botão de apagar em dois toques: o primeiro pede confirmação, o segundo apaga. */
export function Apagar({
  acao,
  id,
  rotulo = 'Apagar',
  aviso,
}: {
  acao: (form: FormData) => Promise<void>
  id?: string
  rotulo?: string
  aviso: string
}) {
  const [confirmar, setConfirmar] = useState(false)
  if (!confirmar)
    return (
      <button type="button" className="btn danger sm" onClick={() => setConfirmar(true)}>
        {rotulo}
      </button>
    )
  return (
    <form action={acao} className="confirma">
      {id && <input type="hidden" name="id" value={id} />}
      <span>{aviso}</span>
      <button type="button" className="btn ghost sm" onClick={() => setConfirmar(false)}>
        Cancelar
      </button>
      <ConfirmarApagar />
    </form>
  )
}
function ConfirmarApagar() {
  const { pending } = useFormStatus()
  return (
    <button className="btn danger sm" type="submit" disabled={pending}>
      {pending ? 'Apagando…' : 'Apagar de vez'}
    </button>
  )
}

export function LimparVersoes({ total }: { total: number }) {
  return <Apagar acao={limparVersoesAntigas} rotulo={`Apagar ${total} ${total === 1 ? 'versão antiga' : 'versões antigas'}`} aviso="Apaga as versões antigas e as respostas dadas a elas." />
}

// ---------- Questão ----------

export type QuestaoAdmin = {
  id: string
  aula_id: string | null
  enunciado: string
  alternativas: string[]
  correta: number
  comentario: string | null
  por_que_erradas: string | null
  tema: string | null
  prova: string | null
  fonte: string | null
  cai_na_prova: boolean
}

export function EditorQuestao({ q, aulas }: { q: QuestaoAdmin; aulas: { id: string; titulo: string }[] }) {
  const [m, acao] = useActionState(salvarQuestao, null)
  const [n, setN] = useState(q.alternativas.length)
  return (
    <div className="ed-bloco">
      <form action={acao} className="ed-form" noValidate>
        <input type="hidden" name="id" value={q.id} />
        <label className="flabel">Enunciado</label>
        <textarea name="enunciado" className="campo" rows={5} defaultValue={q.enunciado} />
        <label className="flabel">Alternativas (uma por linha)</label>
        <textarea
          name="alternativas"
          className="campo"
          rows={Math.max(4, q.alternativas.length + 1)}
          defaultValue={q.alternativas.join('\n')}
          onChange={(e) => setN(e.target.value.split('\n').filter((l) => l.trim()).length)}
        />
        <div className="ed-linha">
          <label className="flabel">
            Certa
            <select name="correta" className="campo" defaultValue={q.correta}>
              {Array.from({ length: Math.max(n, 2) }, (_, i) => (
                <option key={i} value={i}>
                  {LETRAS[i] ?? i + 1}
                </option>
              ))}
            </select>
          </label>
          <label className="flabel">
            Aula
            <select name="aula_id" className="campo" defaultValue={q.aula_id ?? ''}>
              <option value="">Só no banco da matéria</option>
              {aulas.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.titulo}
                </option>
              ))}
            </select>
          </label>
        </div>
        <label className="flabel">Comentário (aparece embaixo da certa)</label>
        <textarea name="comentario" className="campo" rows={5} defaultValue={q.comentario ?? ''} />
        <label className="flabel">Por que as outras estão erradas (uma linha por letra, como “B: …”)</label>
        <textarea name="por_que_erradas" className="campo" rows={5} defaultValue={q.por_que_erradas ?? ''} />
        <div className="ed-linha">
          <label className="flabel">
            Tema
            <input name="tema" className="campo" defaultValue={q.tema ?? ''} />
          </label>
          <label className="flabel">
            Prova
            <input name="prova" className="campo" defaultValue={q.prova ?? ''} />
          </label>
          <label className="flabel">
            Fonte
            <input name="fonte" className="campo" defaultValue={q.fonte ?? ''} />
          </label>
        </div>
        <label className="ed-check">
          <input type="checkbox" name="cai_na_prova" defaultChecked={q.cai_na_prova} /> Cai na prova (o professor disse
          ou deu a entender que cai; põe a faixa PROVA em volta da questão)
        </label>
        <div className="ed-acoes">
          <BotaoEnviar rotulo="Salvar questão" enviando="Salvando…" />
          <Mensagem m={m} />
        </div>
      </form>
      <Apagar acao={apagarQuestao} id={q.id} rotulo="Apagar questão" aviso="Apaga a questão e as respostas dos alunos." />
    </div>
  )
}

// ---------- Aula ----------

export function EditorAula({
  aula,
}: {
  aula: { id: string; titulo: string; resumo: string | null; publicada: boolean; ordem: number }
}) {
  const [m, acao] = useActionState(salvarAula, null)
  return (
    <div className="ed-bloco">
      <form action={acao} className="ed-form" noValidate>
        <input type="hidden" name="id" value={aula.id} />
        <div className="ed-linha">
          <label className="flabel" style={{ flex: '0 0 90px' }}>
            Ordem
            <input name="ordem" className="campo" inputMode="numeric" defaultValue={aula.ordem} />
          </label>
          <label className="flabel" style={{ flex: 1 }}>
            Título
            <input name="titulo" className="campo" defaultValue={aula.titulo} />
          </label>
        </div>
        <label className="flabel">Resumo</label>
        <textarea name="resumo" className="campo" rows={3} defaultValue={aula.resumo ?? ''} />
        <label className="ed-check">
          <input type="checkbox" name="publicada" defaultChecked={aula.publicada} /> Publicada (aparece para os alunos)
        </label>
        <div className="ed-acoes">
          <BotaoEnviar rotulo="Salvar aula" enviando="Salvando…" />
          <Mensagem m={m} />
        </div>
      </form>
      <Apagar
        acao={apagarAula}
        id={aula.id}
        rotulo="Apagar aula"
        aviso="Apaga a aula com as questões, os flashcards e o progresso dos alunos nela."
      />
    </div>
  )
}

// ---------- Flashcard ----------

export function EditorCard({ card, n, aviso = 'Apaga o card e as revisões dos alunos.' }: { card: { id: string; frente: string; verso: string }; n: number; aviso?: string }) {
  const [m, acao] = useActionState(salvarCard, null)
  return (
    <div className="ed-bloco">
      <form action={acao} className="ed-form" noValidate>
        <input type="hidden" name="id" value={card.id} />
        <label className="flabel">Card {n} · frente</label>
        <textarea name="frente" className="campo" rows={2} defaultValue={card.frente} />
        <label className="flabel">Verso</label>
        <textarea name="verso" className="campo" rows={3} defaultValue={card.verso} />
        <div className="ed-acoes">
          <BotaoEnviar rotulo="Salvar" enviando="Salvando…" />
          <Mensagem m={m} />
        </div>
      </form>
      <Apagar acao={apagarCard} id={card.id} rotulo="Apagar card" aviso={aviso} />
    </div>
  )
}

export function ApagarCardsDiaDaAula({ aulaId, total }: { aulaId: string; total: number }) {
  return (
    <Apagar
      acao={apagarCardsDiaDaAula}
      id={aulaId}
      rotulo={total === 1 ? 'Apagar o card Dia D' : `Apagar os ${total} cards Dia D`}
      aviso="Apaga todos os flashcards Dia D desta aula. Os flashcards normais e as questões ficam."
    />
  )
}

export function ApagarCardsDaAula({ aulaId, total }: { aulaId: string; total: number }) {
  return (
    <Apagar
      acao={apagarCardsDaAula}
      id={aulaId}
      rotulo={total === 1 ? 'Apagar o flashcard' : `Apagar os ${total} flashcards`}
      aviso="Apaga todos os flashcards desta aula e as revisões dos alunos neles. A aula e as questões ficam."
    />
  )
}
