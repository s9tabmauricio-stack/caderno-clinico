'use client'

import { useEffect, useMemo, useState } from 'react'
import { explicacoesPorAlternativa } from '@/lib/explicacoes'
import { createClient } from '@/lib/supabase/client'
import type { QuestaoAluno } from '@/lib/dados'
import { plural } from '@/lib/formato'
import { Icone } from './Icones'

export type Resposta = NonNullable<QuestaoAluno['resposta']>
const LETRAS = 'ABCDEFGH'
const ORIGEM: Record<string, { rotulo: string; cls: string }> = {
  professor: { rotulo: 'Corrigida em sala', cls: 'sala' },
  inferido: { rotulo: 'Alternativa reconstruída', cls: 'rec' },
  montada: { rotulo: 'Alternativas montadas · gabarito não oficial', cls: 'rec' },
  resolvida: { rotulo: 'Gabarito não oficial', cls: 'rec' },
}

type Props = {
  questoes: QuestaoAluno[]
  userId: string
  ativo: boolean
  mostrarTema?: boolean
  vazio?: string
  // avisa quem está em volta (o banco de questões) quando uma resposta muda
  aoResponder?: (id: string, resposta: Resposta | null) => void
}

export function Questoes({ questoes, userId, ativo, mostrarTema = true, vazio, aoResponder }: Props) {
  const supabase = useMemo(() => createClient(), [])
  const [respostas, setRespostas] = useState<Record<string, Resposta>>(() =>
    Object.fromEntries(questoes.filter((q) => q.resposta).map((q) => [q.id, q.resposta as Resposta])),
  )
  const primeiraAberta = (r: Record<string, Resposta>) => {
    const i = questoes.findIndex((q) => !r[q.id])
    return i === -1 ? questoes.length : i
  }
  const [idx, setIdx] = useState(() => primeiraAberta(respostas))
  const [escolha, setEscolha] = useState<number | null>(null)
  // alternativas que o aluno cortou (só enquanto está nesta questão)
  const [cortadas, setCortadas] = useState<number[]>([])
  const [refazendo, setRefazendo] = useState(false)
  const [erro, setErro] = useState('')
  const [falhaSalvar, setFalhaSalvar] = useState('')

  const q = questoes[idx]
  const resp = q ? respostas[q.id] : undefined
  const revelada = Boolean(resp) && !refazendo
  const expl = explicacoesPorAlternativa(q?.por_que_erradas ?? null)

  function irPara(i: number) {
    setIdx(i)
    setEscolha(null)
    setCortadas([])
    setRefazendo(false)
    setErro('')
  }

  function cortar(i: number) {
    if (cortadas.includes(i)) {
      setCortadas(cortadas.filter((x) => x !== i))
      return
    }
    setCortadas([...cortadas, i])
    if (escolha === i) setEscolha(null)
  }

  async function responder() {
    if (!q) return
    if (escolha === null) {
      setErro('Escolha uma alternativa antes de responder.')
      return
    }
    const nova: Resposta = { escolhida: escolha, acertou: escolha === q.correta, tentativas: (resp?.tentativas ?? 0) + 1 }
    setRespostas((r) => ({ ...r, [q.id]: nova }))
    aoResponder?.(q.id, nova)
    setRefazendo(false)
    setErro('')
    setFalhaSalvar('')
    const { error } = await supabase.from('respostas').upsert(
      {
        user_id: userId,
        questao_id: q.id,
        escolhida: nova.escolhida,
        correta: nova.acertou,
        tentativas: nova.tentativas,
        respondida_em: new Date().toISOString(),
      },
      { onConflict: 'user_id,questao_id' },
    )
    if (error) setFalhaSalvar('Não deu para salvar esta resposta. Confira a internet e responda de novo.')
  }

  async function apagar(ids: string[]) {
    if (!ids.length) return
    const restantes = { ...respostas }
    ids.forEach((id) => delete restantes[id])
    setRespostas(restantes)
    ids.forEach((id) => aoResponder?.(id, null))
    irPara(primeiraAberta(restantes))
    const { error } = await supabase.from('respostas').delete().eq('user_id', userId).in('questao_id', ids)
    if (error) setFalhaSalvar('Não deu para apagar as respostas antigas. Confira a internet e tente de novo.')
  }

  // Atalhos: A a E (ou 1 a 5) escolhem, Shift + letra corta, Enter responde ou avança
  useEffect(() => {
    if (!ativo) return
    function tecla(e: KeyboardEvent) {
      const alvo = e.target as HTMLElement
      if (e.metaKey || e.ctrlKey || e.altKey || alvo.closest('input, textarea, button, a')) return
      if (!q) return
      const k = e.key.toLowerCase()
      const mapa: Record<string, number> = { a: 0, b: 1, c: 2, d: 3, e: 4, '1': 0, '2': 1, '3': 2, '4': 3, '5': 4 }
      if (!revelada && k in mapa && mapa[k] < q.alternativas.length) {
        e.preventDefault()
        if (e.shiftKey) cortar(mapa[k])
        else if (!cortadas.includes(mapa[k])) {
          setEscolha(mapa[k])
          setErro('')
        }
      } else if (e.key === 'Enter') {
        e.preventDefault()
        if (revelada) irPara(idx + 1)
        else void responder()
      }
    }
    window.addEventListener('keydown', tecla)
    return () => window.removeEventListener('keydown', tecla)
  })

  if (!questoes.length) return <p className="vazio">{vazio ?? 'Esta aula ainda não tem questões.'}</p>

  const certas = questoes.filter((x) => respostas[x.id]?.acertou).length
  const feitas = questoes.filter((x) => respostas[x.id]).length
  const erradas = questoes.filter((x) => respostas[x.id] && !respostas[x.id].acertou).map((x) => x.id)

  const cabecalho = (
    <div className="qhead">
      <span className="qcount">{q ? `Questão ${idx + 1} de ${questoes.length}` : 'Resultado'}</span>
      <div className="qdots">
        {questoes.map((x, i) => {
          const r = respostas[x.id]
          return (
            <button
              key={x.id}
              className={`qd ${r ? (r.acertou ? 'ok' : 'bad') : ''} ${i === idx ? 'cur' : ''}`}
              onClick={() => irPara(i)}
              aria-label={`Questão ${i + 1}${r ? (r.acertou ? ', acertou' : ', errou') : ''}`}
            >
              {i + 1}
            </button>
          )
        })}
      </div>
    </div>
  )

  const aviso = falhaSalvar && (
    <div className="erro-salvar" role="alert">
      <p>{falhaSalvar}</p>
      <button className="link" onClick={() => setFalhaSalvar('')}>
        Fechar
      </button>
    </div>
  )

  if (!q) {
    const faltam = questoes.length - feitas
    const msg = faltam
      ? `${faltam} ${plural(faltam, 'questão ficou', 'questões ficaram')} sem resposta.`
      : certas === questoes.length
        ? 'Você gabaritou esta aula.'
        : `Você acertou ${certas} de ${questoes.length}. Releia o comentário das erradas e refaça.`
    return (
      <div>
        {cabecalho}
        <div className="qcard result">
          <div className="res-n">
            <span className="n">{certas}</span>
            <span className="of">de {questoes.length} certas</span>
          </div>
          <p className="res-t">{msg}</p>
          <div className="group">
            {questoes.map((x, i) => {
              const r = respostas[x.id]
              return (
                <button key={x.id} className="row" onClick={() => irPara(i)}>
                  {r ? (
                    <span className={`st ${r.acertou ? 'ok' : 'bad'}`}>{r.acertou ? Icone.certo : Icone.errado}</span>
                  ) : (
                    <span className="st">{i + 1}</span>
                  )}
                  <span className="main">
                    <span className="s2">{x.enunciado}</span>
                  </span>
                  {Icone.seta}
                </button>
              )
            })}
          </div>
          <div className="actions">
            {erradas.length > 0 && (
              <button className="btn" onClick={() => apagar(erradas)}>
                Refazer {erradas.length === 1 ? 'a errada' : `as ${erradas.length} erradas`}
              </button>
            )}
            <button className="btn ghost" onClick={() => apagar(questoes.map((x) => x.id))}>
              Refazer todas
            </button>
          </div>
        </div>
        {aviso}
      </div>
    )
  }

  return (
    <div>
      {cabecalho}
      <div className="qcard">
        {(q.fonte || (mostrarTema && q.tema) || (q.origem && ORIGEM[q.origem])) && (
          <div className="qmeta">
            {q.fonte && <span className="fonte">{q.fonte}</span>}
            {mostrarTema && q.tema && <span>{q.tema}</span>}
            {q.origem && ORIGEM[q.origem] && <span className={ORIGEM[q.origem].cls}>{ORIGEM[q.origem].rotulo}</span>}
          </div>
        )}
        <p className="qtext">{q.enunciado}</p>
        <div className="opts">
          {q.alternativas.map((texto, i) => {
            const cortada = cortadas.includes(i)
            if (revelada && resp) {
              // Certa em verde, todas as outras em vermelho; a marcada pelo aluno ganha destaque
              let cls = i === q.correta ? 'right' : 'wrong'
              if (i === resp.escolhida) cls += ' minha'
              return (
                <button key={i} className={`opt ${cls}`} disabled>
                  <span className="l">{LETRAS[i]}</span>
                  <span className="ot">
                    {i === resp.escolhida && <span className="sua">Sua resposta</span>}
                    {cortada && <span className="cort-tag">Você cortou</span>}
                    {texto}
                    {i === q.correta && q.comentario && <span className="oexp certa">{q.comentario}</span>}
                    {i !== q.correta && expl.porAlt[i] && <span className="oexp">{expl.porAlt[i]}</span>}
                  </span>
                </button>
              )
            }
            const sel = escolha === i
            return (
              <div key={i} className={`optw${sel ? ' sel' : ''}${cortada ? ' cortada' : ''}`}>
                <button
                  className={`opt${sel ? ' sel' : ''}`}
                  disabled={cortada}
                  aria-pressed={sel}
                  onClick={() => {
                    setEscolha(i)
                    setErro('')
                  }}
                >
                  <span className="l">{LETRAS[i]}</span>
                  <span className="ot">{texto}</span>
                </button>
                <button
                  className="elim"
                  onClick={() => cortar(i)}
                  aria-pressed={cortada}
                  aria-label={cortada ? `Trazer de volta a alternativa ${LETRAS[i]}` : `Cortar a alternativa ${LETRAS[i]}`}
                >
                  {cortada ? Icone.desfazer : Icone.tesoura}
                  <span>{cortada ? 'Voltar' : 'Cortar'}</span>
                </button>
              </div>
            )
          })}
        </div>

        {revelada && resp ? (
          <>
            <div className={`verdict ${resp.acertou ? 'ok' : 'bad'}`}>
              {resp.acertou ? Icone.certo : Icone.errado}
              <span>
                {resp.acertou
                  ? 'Você acertou.'
                  : `Você marcou ${LETRAS[resp.escolhida]}. A resposta é ${LETRAS[q.correta]}.`}
              </span>
            </div>
            {expl.resto && (
              <div className="erradas">
                <div className="kick">
                  <span className="dot" />
                  Sobre as alternativas
                </div>
                <p>{expl.resto}</p>
              </div>
            )}
            <div className="actions">
              <button
                className="btn ghost"
                onClick={() => {
                  setRefazendo(true)
                  setEscolha(null)
                  setCortadas([])
                }}
              >
                Refazer esta
              </button>
              <button className="btn" onClick={() => irPara(idx + 1)}>
                {idx === questoes.length - 1 ? 'Ver resultado' : 'Próxima questão'}
              </button>
            </div>
          </>
        ) : (
          <>
            {erro && (
              <p className="err" role="alert">
                {erro}
              </p>
            )}
            <div className="actions">
              <button className="btn" onClick={responder}>
                Responder
              </button>
            </div>
          </>
        )}
      </div>
      {aviso}
    </div>
  )
}
