'use client'

import { useEffect, useMemo, useRef, useState } from 'react'
import { explicacoesPorAlternativa } from '@/lib/explicacoes'
import { explicarFalha } from '@/lib/falhas'
import { createClient } from '@/lib/supabase/client'
import type { QuestaoAluno } from '@/lib/dados'
import { plural } from '@/lib/formato'
import { temFaixaProva } from '@/lib/faixa-prova'
import { CLASSIFICACOES_QUESTAO, rotuloClassificacao, type ClassificacaoQuestao } from '@/lib/classificacao-questoes'
import { Icone } from './Icones'
import { ConversaTurma } from './ConversaTurma'
import { FaixaProva } from './FaixaProva'
import { PlacaPrioridade } from './PlacaPrioridade'
import { EditorQuestao } from './admin/Editores'

export type Resposta = NonNullable<QuestaoAluno['resposta']>
const LETRAS = 'ABCDEFGH'
const ORIGEM: Record<string, { rotulo: string; cls: string }> = {
  professor: { rotulo: 'Corrigida em sala', cls: 'sala' },
  inferido: { rotulo: 'Alternativa reconstruída', cls: 'rec' },
  montada: { rotulo: 'Alternativas montadas · gabarito não oficial', cls: 'rec' },
  resolvida: { rotulo: 'Gabarito não oficial', cls: 'rec' },
  adaptada: { rotulo: 'Adaptada à aula', cls: 'rec' },
}

type Props = {
  questoes: QuestaoAluno[]
  userId: string
  ativo: boolean
  mostrarTema?: boolean
  vazio?: string
  // avisa quem está em volta (o banco de questões) quando uma resposta muda
  aoResponder?: (id: string, resposta: Resposta | null) => void
  aoClassificar?: (id: string, classificacao: ClassificacaoQuestao | null) => void
  iniciarPelaPrimeira?: boolean
  // o que oferecer quando as questões acabam (ex.: estudar os flashcards da aula)
  proximoPasso?: React.ReactNode
  // só para o administrador: botão Editar na questão (aulas da matéria para o seletor)
  edicao?: { aulas: { id: string; titulo: string }[] }
}

export function Questoes({ questoes, userId, ativo, mostrarTema = true, vazio, aoResponder, aoClassificar, iniciarPelaPrimeira, proximoPasso, edicao }: Props) {
  const supabase = useMemo(() => createClient(), [])
  const [respostas, setRespostas] = useState<Record<string, Resposta>>(() =>
    Object.fromEntries(questoes.filter((q) => q.resposta).map((q) => [q.id, q.resposta as Resposta])),
  )
  const primeiraAberta = (r: Record<string, Resposta>) => {
    const i = questoes.findIndex((q) => !r[q.id])
    return i === -1 ? questoes.length : i
  }
  const [idx, setIdx] = useState(() => iniciarPelaPrimeira ? 0 : primeiraAberta(respostas))
  const [classificacoes, setClassificacoes] = useState<Record<string, ClassificacaoQuestao | null>>(() =>
    Object.fromEntries(questoes.map((q) => [q.id, q.classificacao])),
  )
  const [salvandoClassificacao, setSalvandoClassificacao] = useState(false)
  const classificacaoPendente = useRef(false)
  const [escolha, setEscolha] = useState<number | null>(null)
  // alternativas que o aluno cortou (só enquanto está nesta questão)
  const [cortadas, setCortadas] = useState<number[]>([])
  const [refazendo, setRefazendo] = useState(false)
  const [editando, setEditando] = useState(false)
  // botão Copiar: 'ok' = copiou; 'erro' = o aparelho não deixou copiar
  const [copiado, setCopiado] = useState<'ok' | 'erro' | null>(null)
  const [erro, setErro] = useState('')
  // Gravação que não deu certo: de qual questão (null = apagar respostas), o motivo e como tentar de novo
  const [falha, setFalha] = useState<{ questaoId: string | null; texto: string; sessao: boolean; tentar?: () => void } | null>(null)
  const [tentando, setTentando] = useState(false)
  // "Refazer todas" apaga todas as respostas da lista: pede confirmação antes
  const [confirmarTodas, setConfirmarTodas] = useState(false)

  const q = questoes[idx]
  const resp = q ? respostas[q.id] : undefined
  const revelada = Boolean(resp) && !refazendo
  const expl = explicacoesPorAlternativa(q?.por_que_erradas ?? null)

  function irPara(i: number) {
    setIdx(i)
    setEscolha(null)
    setCortadas([])
    setRefazendo(false)
    setEditando(false)
    setErro('')
    setConfirmarTodas(false)
  }

  // Copia só o enunciado e as alternativas (sem gabarito nem comentário), para o aluno conferir em outra IA
  async function copiarQuestao() {
    const texto = [q.enunciado.trim(), '', ...q.alternativas.map((t, i) => `${LETRAS[i]}) ${t}`)].join('\n')
    let ok = false
    try {
      await navigator.clipboard.writeText(texto)
      ok = true
    } catch {
      // celulares antigos ou sem permissão: cópia pelo jeito antigo
      const area = document.createElement('textarea')
      area.value = texto
      area.setAttribute('readonly', '')
      area.style.position = 'fixed'
      area.style.opacity = '0'
      document.body.appendChild(area)
      area.select()
      try {
        ok = document.execCommand('copy')
      } catch {}
      area.remove()
    }
    setCopiado(ok ? 'ok' : 'erro')
    setTimeout(() => setCopiado(null), 2000)
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
    await salvar(q.id, nova)
  }

  async function salvar(id: string, r: Resposta) {
    setFalha(null)
    const { error } = await supabase.from('respostas').upsert(
      {
        user_id: userId,
        questao_id: id,
        escolhida: r.escolhida,
        correta: r.acertou,
        tentativas: r.tentativas,
        respondida_em: new Date().toISOString(),
      },
      { onConflict: 'user_id,questao_id' },
    )
    if (error) setFalha({ questaoId: id, ...(await explicarFalha(supabase, 'esta resposta')), tentar: () => salvar(id, r) })
  }

  async function classificar(id: string, valor: ClassificacaoQuestao | null) {
    if (classificacaoPendente.current) return
    classificacaoPendente.current = true
    setSalvandoClassificacao(true)
    setFalha(null)
    try {
      const { error } = valor === null
        ? await supabase.from('classificacoes_questoes').delete().eq('user_id', userId).eq('questao_id', id)
        : await supabase.from('classificacoes_questoes').upsert({
            user_id: userId, questao_id: id, classificacao: valor, atualizada_em: new Date().toISOString(),
          }, { onConflict: 'user_id,questao_id' }).select('classificacao').single()
      if (error) throw error
      setClassificacoes((anteriores) => ({ ...anteriores, [id]: valor }))
      aoClassificar?.(id, valor)
    } catch {
      setFalha({ questaoId: id, ...(await explicarFalha(supabase, 'esta marcação')), tentar: () => classificar(id, valor) })
    } finally {
      classificacaoPendente.current = false
      setSalvandoClassificacao(false)
    }
  }

  async function tentarDeNovo() {
    if (!falha?.tentar || tentando) return
    setTentando(true)
    await falha.tentar()
    setTentando(false)
  }

  async function apagar(ids: string[]) {
    if (!ids.length) return
    const restantes = { ...respostas }
    ids.forEach((id) => delete restantes[id])
    setRespostas(restantes)
    ids.forEach((id) => aoResponder?.(id, null))
    irPara(primeiraAberta(restantes))
    setFalha(null)
    const { error } = await supabase.from('respostas').delete().eq('user_id', userId).in('questao_id', ids)
    if (error) setFalha({ questaoId: null, texto: 'Não deu para apagar as respostas antigas. Confira a internet e tente de novo.', sessao: false })
  }

  // Atalhos: A a E (ou 1 a 5) escolhem, Shift + letra corta, Enter responde ou avança
  useEffect(() => {
    if (!ativo || editando) return
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

  // Faixa de quadradinhos: rola de lado para deixar a questão atual no meio
  const faixa = useRef<HTMLDivElement>(null)
  // Ao trocar de questão, a tela volta ao "Questão X de Y" se ele tiver ficado para cima
  // (depois de ler o comentário, o aluno está lá embaixo e cairia no meio da próxima questão)
  const topo = useRef<HTMLDivElement>(null)
  const primeira = useRef(true)
  useEffect(() => {
    const el = faixa.current
    const atual = el?.querySelector<HTMLElement>('.qd.cur')
    if (el && atual) el.scrollTo({ left: atual.offsetLeft - (el.clientWidth - atual.offsetWidth) / 2, behavior: 'smooth' })
    if (primeira.current) {
      primeira.current = false
      return
    }
    const cab = topo.current
    if (cab && cab.getBoundingClientRect().top < 0) {
      const suave = !window.matchMedia('(prefers-reduced-motion: reduce)').matches
      cab.scrollIntoView({ block: 'start', behavior: suave ? 'smooth' : 'auto' })
    }
  }, [idx])

  if (!questoes.length) return <p className="vazio">{vazio ?? 'Esta aula ainda não tem questões.'}</p>

  const certas = questoes.filter((x) => respostas[x.id]?.acertou).length
  const feitas = questoes.filter((x) => respostas[x.id]).length
  const erradas = questoes.filter((x) => respostas[x.id] && !respostas[x.id].acertou).map((x) => x.id)

  const cabecalho = (
    <div className="qhead" ref={topo}>
      <span className="qcount">{q ? `Questão ${idx + 1} de ${questoes.length}` : 'Resultado'}</span>
      <div className="qdots" ref={faixa}>
        {questoes.map((x, i) => {
          const r = respostas[x.id]
          const classificacao = classificacoes[x.id]
          const prova = temFaixaProva(x)
          const descricao = `Questão ${i + 1}${r ? (r.acertou ? ', acertou' : ', errou') : ''}${prova ? ', PROVA' : ''}${classificacao ? `, ${rotuloClassificacao(classificacao)}` : ''}`
          return (
            <span className="qd-item" key={x.id}>
              <button
                className={`qd ${r ? (r.acertou ? 'ok' : 'bad') : ''} ${i === idx ? 'cur' : ''}`}
                onClick={() => irPara(i)}
                aria-label={descricao}
                aria-current={i === idx ? 'step' : undefined}
                title={descricao}
              >
                {prova && <span className="qd-prova" aria-hidden="true">PROVA</span>}
                {i + 1}
                {classificacao && <span className="qd-prioridade"><PlacaPrioridade valor={classificacao} /></span>}
              </button>
            </span>
          )
        })}
      </div>
    </div>
  )

  // Aviso de gravação que falhou: aparece logo abaixo do resultado da questão (ou no topo, se o aluno já
  // passou para outra), com o motivo e o botão para tentar de novo
  const nDaFalha = falha?.questaoId ? questoes.findIndex((x) => x.id === falha.questaoId) + 1 : 0
  const aviso = falha && (
    <div className="erro-salvar" role="alert">
      <p>
        {nDaFalha > 0 && falha.questaoId !== q?.id && <b>Questão {nDaFalha}: </b>}
        {falha.texto}
      </p>
      <div className="erro-acoes">
        {falha.sessao ? (
          <a className="btn sm" href="/login">
            Entrar de novo
          </a>
        ) : (
          falha.tentar && (
            <button className="btn sm" onClick={tentarDeNovo} disabled={tentando}>
              {tentando ? 'Salvando…' : 'Tentar de novo'}
            </button>
          )
        )}
        <button className="link" onClick={() => setFalha(null)}>
          Fechar
        </button>
      </div>
    </div>
  )
  // Na questão da falha, já respondida na tela: o aviso vai logo abaixo do "Você acertou/marcou"
  const avisoAqui = falha !== null && falha.questaoId === q?.id && revelada

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
                    {classificacoes[x.id] && <span className="s3">{rotuloClassificacao(classificacoes[x.id]!)}</span>}
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
            {!confirmarTodas && (
              <button
                className="btn ghost"
                onClick={() => (feitas > 0 ? setConfirmarTodas(true) : apagar(questoes.map((x) => x.id)))}
              >
                Refazer todas
              </button>
            )}
          </div>
          {confirmarTodas && (
            <div className="confirmar" role="alertdialog" aria-labelledby="confirmar-todas">
              <p id="confirmar-todas">
                Apagar {feitas === 1 ? 'a sua resposta' : `as suas ${feitas} respostas`} e refazer {questoes.length === 1 ? 'a questão' : `as ${questoes.length} questões`}?
              </p>
              <div className="actions">
                <button className="btn ghost" onClick={() => setConfirmarTodas(false)}>
                  Cancelar
                </button>
                <button className="btn" onClick={() => apagar(questoes.map((x) => x.id))}>
                  Apagar e refazer
                </button>
              </div>
            </div>
          )}
          <p className="foot">Refazer não apaga o histórico: o Desempenho continua contando a sua primeira resposta.</p>
          {proximoPasso && (
            <>
              <p className="foot res-prox">Próximo passo</p>
              <div className="next-steps">{proximoPasso}</div>
            </>
          )}
        </div>
        {aviso}
      </div>
    )
  }

  return (
    <div>
      {cabecalho}
      {!avisoAqui && aviso}
      <FaixaProva ligada={temFaixaProva(q)}>
        <div className="qcard">
          <div className="qmeta">
            {q.fonte && <span className="fonte">{q.fonte}</span>}
            {mostrarTema && q.tema && <span>{q.tema}</span>}
            {q.origem && ORIGEM[q.origem] && <span className={ORIGEM[q.origem].cls}>{ORIGEM[q.origem].rotulo}</span>}
            {!editando && (
              <button
                type="button"
                className={`editar-q copiar-q${copiado === 'ok' ? ' on' : ''}`}
                onClick={copiarQuestao}
                title="Copia o enunciado e as alternativas, sem a resposta"
                aria-live="polite"
              >
                {copiado === 'ok' ? Icone.certo : Icone.copiar}
                {copiado === 'ok' ? 'Copiada' : copiado === 'erro' ? 'Não deu para copiar' : 'Copiar'}
              </button>
            )}
            {edicao && (
              <button
                type="button"
                className={`editar-q${editando ? ' on' : ''}`}
                aria-pressed={editando}
                onClick={() => setEditando(!editando)}
              >
                {editando ? Icone.errado : Icone.lapis}
                {editando ? 'Fechar edição' : 'Editar'}
              </button>
            )}
          </div>
          {editando && edicao ? (
            <div className="editar-painel">
              <p className="editar-aviso">Só você vê isto. O que salvar aqui muda a questão para toda a turma.</p>
              <EditorQuestao key={q.id} q={q} aulas={edicao.aulas} />
              <div className="actions">
                <button className="btn ghost" onClick={() => setEditando(false)}>
                  Voltar para a questão
                </button>
              </div>
            </div>
          ) : (
            <>
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
                  {avisoAqui && aviso}
                  {expl.resto && (
                    <div className="erradas">
                      <div className="kick">
                        <span className="dot" />
                        Sobre as alternativas
                      </div>
                      <p>{expl.resto}</p>
                    </div>
                  )}
                  <fieldset className="qclassificacao" disabled={salvandoClassificacao}>
                    <legend>Marcar como</legend>
                    <div className="qclassificacao-opcoes">
                      {CLASSIFICACOES_QUESTAO.map(({ valor, rotulo }) => (
                        <button
                          key={valor}
                          type="button"
                          className={`qclassificacao-btn prioridade--${valor}`}
                          aria-pressed={classificacoes[q.id] === valor}
                          onClick={() => void classificar(q.id, classificacoes[q.id] === valor ? null : valor)}
                        >
                          <PlacaPrioridade valor={valor} />
                          <span>{rotulo}</span>
                        </button>
                      ))}
                    </div>
                    <p className="qclassificacao-ajuda" role="status">
                      {salvandoClassificacao ? 'Salvando marcação…' : 'Só você vê. Toque na opção marcada para desmarcar.'}
                    </p>
                  </fieldset>
                  <div className="actions qacoes">
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
                  <div className="actions qacoes">
                    <button className="btn" onClick={responder}>
                      Responder
                    </button>
                  </div>
                </>
              )}
            </>
          )}
        </div>
      </FaixaProva>
      {revelada && <ConversaTurma key={q.id} questaoId={q.id} userId={userId} />}
    </div>
  )
}
