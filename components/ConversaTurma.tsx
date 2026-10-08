'use client'

import { useEffect, useMemo, useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { fmtHa, NOME_ADMIN, primeiroNome, situacaoErro, tituloRecado, type Recado } from '@/lib/recados'

type Tipo = 'insight' | 'erro'
const LIMITE = 1000
const CAMPOS = 'id, questao_id, user_id, autor, tipo, texto, status, criado_em'

/** Conversa da turma embaixo de uma questão já respondida: dicas para os colegas e avisos de erro. */
export function ConversaTurma({ questaoId, userId }: { questaoId: string; userId: string }) {
  const supabase = useMemo(() => createClient(), [])
  const [recados, setRecados] = useState<Recado[] | null>(null)
  const [uteis, setUteis] = useState<{ recado_id: string; user_id: string }[]>([])
  const [meuNome, setMeuNome] = useState('Você')
  const [tipo, setTipo] = useState<Tipo | null>(null)
  const [texto, setTexto] = useState('')
  const [enviando, setEnviando] = useState(false)
  const [aviso, setAviso] = useState<{ ok: boolean; texto: string } | null>(null)
  const [apagando, setApagando] = useState<string | null>(null)

  useEffect(() => {
    let vivo = true
    ;(async () => {
      const [{ data, error }, { data: perfil }] = await Promise.all([
        supabase.from('recados').select(CAMPOS).eq('questao_id', questaoId).order('criado_em'),
        supabase.from('perfis').select('nome').eq('id', userId).maybeSingle(),
      ])
      if (!vivo) return
      if (error) {
        setRecados([])
        setAviso({ ok: false, texto: 'Não deu para carregar a conversa. Confira a internet.' })
        return
      }
      setMeuNome(primeiroNome(perfil?.nome))
      setRecados(data)
      if (data.length) {
        const { data: votos } = await supabase.from('recados_uteis').select('recado_id, user_id').in('recado_id', data.map((r) => r.id))
        if (vivo) setUteis(votos ?? [])
      }
    })()
    return () => {
      vivo = false
    }
  }, [supabase, questaoId, userId])

  async function enviar() {
    if (!tipo) return
    const limpo = texto.trim()
    if (!limpo) {
      setAviso({ ok: false, texto: 'Escreva alguma coisa antes de enviar.' })
      return
    }
    setEnviando(true)
    setAviso(null)
    const { data, error } = await supabase
      .from('recados')
      .insert({ questao_id: questaoId, user_id: userId, tipo, texto: limpo })
      .select(CAMPOS)
      .single()
    setEnviando(false)
    if (error) {
      setAviso({ ok: false, texto: 'Não deu para enviar. Confira a internet e tente de novo.' })
      return
    }
    setRecados((rs) => [...(rs ?? []), data])
    setTipo(null)
    setTexto('')
    setAviso({
      ok: true,
      texto:
        tipo === 'erro'
          ? `Enviado. O ${NOME_ADMIN} foi avisado. Se mudar de ideia, toque em Apagar no seu recado.`
          : 'Enviado. Se mudar de ideia, toque em Apagar no seu recado.',
    })
  }

  async function apagar(id: string) {
    const { error } = await supabase.from('recados').delete().eq('id', id).eq('user_id', userId)
    setApagando(null)
    if (error) {
      setAviso({ ok: false, texto: 'Não deu para apagar. Confira a internet e tente de novo.' })
      return
    }
    setRecados((rs) => (rs ?? []).filter((r) => r.id !== id))
    setAviso({ ok: true, texto: 'Recado apagado.' })
  }

  async function util(id: string) {
    const marcado = uteis.some((u) => u.recado_id === id && u.user_id === userId)
    setUteis((us) => (marcado ? us.filter((u) => !(u.recado_id === id && u.user_id === userId)) : [...us, { recado_id: id, user_id: userId }]))
    const { error } = marcado
      ? await supabase.from('recados_uteis').delete().eq('recado_id', id).eq('user_id', userId)
      : await supabase.from('recados_uteis').insert({ recado_id: id, user_id: userId })
    if (error) {
      // desfaz o toque se não salvou
      setUteis((us) => (marcado ? [...us, { recado_id: id, user_id: userId }] : us.filter((u) => !(u.recado_id === id && u.user_id === userId))))
    }
  }

  const lista = recados ?? []

  return (
    <section className="turma" aria-label="Conversa da turma">
      <h3>
        Conversa da turma {lista.length > 0 && <span className="n">{lista.length}</span>}
      </h3>
      <p className="turma-sub">
        {recados === null
          ? 'Carregando…'
          : lista.length
            ? 'Dicas e avisos dos colegas sobre esta questão.'
            : 'Ninguém comentou ainda. Deixe a primeira dica ou avise se viu um erro.'}
      </p>

      {lista.map((r) => {
        const meu = r.user_id === userId
        const votos = uteis.filter((u) => u.recado_id === r.id)
        const votei = votos.some((u) => u.user_id === userId)
        const sit = r.tipo === 'erro' ? situacaoErro(r.status) : null
        return (
          <div key={r.id} className={`msg${meu ? ' meu' : ''}`}>
            <div className={`av ${r.tipo === 'erro' ? 'erro' : ''}`}>{r.autor.charAt(0).toUpperCase()}</div>
            <div className="mb">
              <div className="mh">
                <span className={`tag ${r.tipo === 'erro' ? 'erro' : 'ins'}`}>
                  {r.tipo === 'erro' ? '⚠️' : '💡'} {meu ? (r.tipo === 'erro' ? 'Você achou um erro' : 'Você deixou uma dica') : tituloRecado(r)}
                </span>
                <span className="when">{fmtHa(r.criado_em)}</span>
              </div>
              <p className="mt">{r.texto}</p>
              {sit && <span className={`situacao ${sit.cls}`}>{sit.texto}</span>}
              <div className="acts">
                {r.tipo === 'insight' &&
                  (meu ? (
                    votos.length > 0 && <span className="util">👍 Útil · {votos.length}</span>
                  ) : (
                    <button type="button" className={`util${votei ? ' on' : ''}`} aria-pressed={votei} onClick={() => util(r.id)}>
                      👍 Útil{votos.length > 0 && ` · ${votos.length}`}
                    </button>
                  ))}
                {meu &&
                  (apagando === r.id ? (
                    <span className="conf">
                      Apagar seu recado?
                      <button type="button" className="apagar" onClick={() => apagar(r.id)}>
                        Sim, apagar
                      </button>
                      <button type="button" onClick={() => setApagando(null)}>
                        Cancelar
                      </button>
                    </span>
                  ) : (
                    <button type="button" className="apagar" onClick={() => setApagando(r.id)}>
                      🗑️ Apagar
                    </button>
                  ))}
              </div>
            </div>
          </div>
        )
      })}

      <div className="comp">
        <div className="tipos" role="group" aria-label="Tipo de recado">
          <button type="button" className={`tipo ins${tipo === 'insight' ? ' on' : ''}`} aria-pressed={tipo === 'insight'} onClick={() => setTipo(tipo === 'insight' ? null : 'insight')}>
            <span className="e">💡</span>Insight para os colegas
          </button>
          <button type="button" className={`tipo erro${tipo === 'erro' ? ' on' : ''}`} aria-pressed={tipo === 'erro'} onClick={() => setTipo(tipo === 'erro' ? null : 'erro')}>
            <span className="e">⚠️</span>Erro na questão
          </button>
        </div>
        {tipo && (
          <>
            <textarea
              className="campo turma-campo"
              value={texto}
              maxLength={LIMITE}
              rows={3}
              autoFocus
              placeholder={
                tipo === 'erro'
                  ? 'O que está errado? O gabarito, uma alternativa, o comentário…'
                  : 'Um macete, um jeito de lembrar, onde isso caiu na aula…'
              }
              onChange={(e) => setTexto(e.target.value)}
            />
            <p className="turma-dica">
              Vai aparecer como <b className={tipo}>“{tipo === 'erro' ? `${meuNome} achou um erro` : `${meuNome} deixou uma dica`}”</b>
              {tipo === 'erro' ? ` e o ${NOME_ADMIN} é avisado.` : ' para a turma.'}
            </p>
            <div className="turma-acoes">
              <button type="button" className="btn ghost sm" onClick={() => setTipo(null)}>
                Cancelar
              </button>
              <button type="button" className="btn sm" disabled={enviando} onClick={enviar}>
                {enviando ? 'Enviando…' : 'Enviar'}
              </button>
            </div>
          </>
        )}
        <p className="sem-medo">🗑️ Pode postar sem medo: você apaga o seu recado quando quiser.</p>
        {aviso && (
          <p className={aviso.ok ? 'ok-msg' : 'err'} role="status">
            {aviso.texto}
          </p>
        )}
      </div>
    </section>
  )
}
