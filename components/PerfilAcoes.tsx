'use client'

import { useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'
import { cpfDoEmail, formatarCpf } from '@/lib/cpf'

export function PerfilAcoes({ userId, nomeInicial, email }: { userId: string; nomeInicial: string; email: string }) {
  const supabase = useMemo(() => createClient(), [])
  const router = useRouter()
  const [nome, setNome] = useState(nomeInicial)
  const [msgNome, setMsgNome] = useState<{ ok: boolean; texto: string } | null>(null)
  const [confirmar, setConfirmar] = useState(false)
  const [msgApagar, setMsgApagar] = useState<{ ok: boolean; texto: string } | null>(null)
  const [senha, setSenha] = useState('')
  const [senha2, setSenha2] = useState('')
  const [msgSenha, setMsgSenha] = useState<{ ok: boolean; texto: string } | null>(null)
  const cpf = cpfDoEmail(email)

  async function trocarSenha(e: React.FormEvent) {
    e.preventDefault()
    if (senha.length < 6) {
      setMsgSenha({ ok: false, texto: 'A senha precisa ter pelo menos 6 caracteres.' })
      return
    }
    if (senha !== senha2) {
      setMsgSenha({ ok: false, texto: 'As duas senhas não são iguais.' })
      return
    }
    const { error } = await supabase.auth.updateUser({ password: senha })
    if (error) {
      setMsgSenha({
        ok: false,
        texto: /different|same/i.test(error.message)
          ? 'A nova senha precisa ser diferente da atual.'
          : 'Não deu para trocar a senha. Tente de novo.',
      })
      return
    }
    setSenha('')
    setSenha2('')
    setMsgSenha({ ok: true, texto: 'Senha trocada. Use a nova senha no próximo acesso.' })
  }

  async function salvarNome(e: React.FormEvent) {
    e.preventDefault()
    const v = nome.trim()
    if (!v) {
      setMsgNome({ ok: false, texto: 'Digite um nome.' })
      return
    }
    const { error } = await supabase.from('perfis').update({ nome: v }).eq('id', userId)
    setMsgNome(error ? { ok: false, texto: 'Não deu para salvar o nome. Tente de novo.' } : { ok: true, texto: 'Nome salvo.' })
    if (!error) router.refresh()
  }

  async function apagarProgresso() {
    const [r1, r2] = await Promise.all([
      supabase.from('respostas').delete().eq('user_id', userId),
      supabase.from('revisoes').delete().eq('user_id', userId),
    ])
    setConfirmar(false)
    setMsgApagar(
      r1.error || r2.error
        ? { ok: false, texto: 'Não deu para apagar tudo. Confira a internet e tente de novo.' }
        : { ok: true, texto: 'Progresso apagado. Você começa do zero.' },
    )
    router.refresh()
  }

  return (
    <>
      <div className="group">
        <div className="row static">
          <span className="avatar lg" aria-hidden="true">
            {(nome || email).charAt(0).toUpperCase()}
          </span>
          <span className="main">
            <span className="t">{nomeInicial}</span>
            <span className="s">{cpf ? `CPF ${formatarCpf(cpf)}` : email}</span>
          </span>
        </div>
      </div>

      <div className="sec">Como você quer ser chamado</div>
      <form className="linha-form" onSubmit={salvarNome} noValidate>
        <label htmlFor="nome" className="sr-only">
          Nome
        </label>
        <input
          id="nome"
          className="campo"
          value={nome}
          maxLength={60}
          autoComplete="given-name"
          onChange={(e) => {
            setNome(e.target.value)
            setMsgNome(null)
          }}
        />
        <button className="btn" type="submit">
          Salvar
        </button>
      </form>
      {msgNome && (
        <p className={msgNome.ok ? 'ok-msg' : 'err'} role="status">
          {msgNome.texto}
        </p>
      )}

      <div className="sec">Trocar senha</div>
      <form className="senha-form" onSubmit={trocarSenha} noValidate>
        <label htmlFor="nova-senha" className="sr-only">
          Nova senha
        </label>
        <input
          id="nova-senha"
          className="campo"
          type="password"
          autoComplete="new-password"
          placeholder="Nova senha"
          value={senha}
          onChange={(e) => {
            setSenha(e.target.value)
            setMsgSenha(null)
          }}
        />
        <label htmlFor="nova-senha2" className="sr-only">
          Repita a nova senha
        </label>
        <input
          id="nova-senha2"
          className="campo"
          type="password"
          autoComplete="new-password"
          placeholder="Repita a nova senha"
          value={senha2}
          onChange={(e) => {
            setSenha2(e.target.value)
            setMsgSenha(null)
          }}
        />
        <button className="btn" type="submit">
          Trocar senha
        </button>
      </form>
      {msgSenha && (
        <p className={msgSenha.ok ? 'ok-msg' : 'err'} role="status">
          {msgSenha.texto}
        </p>
      )}

      <div className="sec">Progresso</div>
      <div className="group">
        {confirmar ? (
          <div className="row static confirm">
            <span className="main">
              <span className="t">Apagar todas as suas respostas e revisões?</span>
              <span className="s">Não dá para desfazer.</span>
            </span>
            <button className="btn ghost sm" onClick={() => setConfirmar(false)}>
              Cancelar
            </button>
            <button className="btn danger sm" onClick={apagarProgresso}>
              Apagar
            </button>
          </div>
        ) : (
          <button
            className="row"
            onClick={() => {
              setConfirmar(true)
              setMsgApagar(null)
            }}
          >
            <span className="main">
              <span className="t danger">Apagar meu progresso</span>
              <span className="s">Zera questões respondidas e flashcards estudados.</span>
            </span>
          </button>
        )}
      </div>
      {msgApagar && (
        <p className={msgApagar.ok ? 'ok-msg' : 'err'} role="status">
          {msgApagar.texto}
        </p>
      )}
    </>
  )
}
