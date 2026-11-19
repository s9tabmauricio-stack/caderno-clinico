'use client'

import Link from 'next/link'
import { useMemo, useRef, useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { fmtHa, NOME_ADMIN } from '@/lib/recados'
import { LIMITE_MENSAGEM, type Mensagem as Msg } from '@/lib/mensagens'

const balao = (
  <svg viewBox="0 0 24 24" aria-hidden="true">
    <path d="M4.5 6.5A2.5 2.5 0 0 1 7 4h10a2.5 2.5 0 0 1 2.5 2.5v7A2.5 2.5 0 0 1 17 16h-6l-4.5 4v-4H7a2.5 2.5 0 0 1-2.5-2.5z" />
    <path d="M8.5 9h7M8.5 12h4.5" />
  </svg>
)

/** Para o administrador: o balão leva às mensagens recebidas, com o número das novas. */
export function MensagensAdmin({ novas }: { novas: number }) {
  return (
    <Link
      className="avatar engrenagem novidades mensagem"
      href="/admin/mensagens"
      aria-label={novas ? `Mensagens: ${novas} novas` : 'Mensagens'}
      title="Mensagens dos alunos"
    >
      {balao}
      {novas > 0 && <span className="bd">{novas}</span>}
    </Link>
  )
}

/** Para o aluno: balão no topo que abre uma caixinha para mandar mensagem ao administrador. */
export function Mensagem() {
  const supabase = useMemo(() => createClient(), [])
  const painel = useRef<HTMLDialogElement>(null)
  const [texto, setTexto] = useState('')
  const [enviando, setEnviando] = useState(false)
  const [aviso, setAviso] = useState<{ ok: boolean; texto: string } | null>(null)
  const [minhas, setMinhas] = useState<Msg[] | null>(null)

  async function abrir() {
    painel.current?.showModal()
    setAviso(null)
    const { data } = await supabase
      .from('mensagens')
      .select('id, user_id, autor, texto, status, criado_em')
      .order('criado_em', { ascending: false })
      .limit(10)
    setMinhas(data ?? [])
  }

  async function enviar() {
    const limpo = texto.trim()
    if (!limpo) {
      setAviso({ ok: false, texto: 'Escreva alguma coisa antes de enviar.' })
      return
    }
    setEnviando(true)
    setAviso(null)
    const { data, error } = await supabase
      .from('mensagens')
      .insert({ texto: limpo })
      .select('id, user_id, autor, texto, status, criado_em')
      .single()
    setEnviando(false)
    if (error) {
      setAviso({ ok: false, texto: 'Não deu para enviar. Confira a internet e tente de novo.' })
      return
    }
    setMinhas((ms) => [data, ...(ms ?? [])])
    setTexto('')
    setAviso({ ok: true, texto: `Enviada! O ${NOME_ADMIN} vai ler.` })
  }

  return (
    <>
      <button type="button" className="avatar engrenagem novidades mensagem" aria-label={`Mandar mensagem para o ${NOME_ADMIN}`} title={`Mandar mensagem para o ${NOME_ADMIN}`} onClick={abrir}>
        {balao}
      </button>
      <dialog ref={painel} className="nov-painel" aria-label="Mensagem" onClick={(e) => e.target === e.currentTarget && painel.current?.close()}>
        <div className="nov-caixa msg-caixa">
          <div className="nov-topo">
            <h2>Mensagem para o {NOME_ADMIN}</h2>
            <button type="button" className="nov-fechar" onClick={() => painel.current?.close()} aria-label="Fechar">
              ×
            </button>
          </div>
          <p className="msg-sub">Dúvida, sugestão ou erro no app? Só o {NOME_ADMIN} lê.</p>
          <textarea
            className="campo turma-campo"
            value={texto}
            maxLength={LIMITE_MENSAGEM}
            rows={4}
            placeholder="Escreva aqui…"
            onChange={(e) => setTexto(e.target.value)}
          />
          <div className="turma-acoes">
            <span />
            <button type="button" className="btn sm" disabled={enviando} onClick={enviar}>
              {enviando ? 'Enviando…' : 'Enviar'}
            </button>
          </div>
          {aviso && (
            <p className={aviso.ok ? 'ok-msg' : 'err'} role="status">
              {aviso.texto}
            </p>
          )}
          {minhas && minhas.length > 0 && (
            <>
              <h3 className="msg-tit">Suas mensagens</h3>
              <ul>
                {minhas.map((m) => (
                  <li key={m.id}>
                    <span className="nov-data">
                      {fmtHa(m.criado_em)} · {m.status === 'lida' ? `✓ Lida pelo ${NOME_ADMIN}` : 'Enviada'}
                    </span>
                    <p>{m.texto}</p>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      </dialog>
    </>
  )
}
