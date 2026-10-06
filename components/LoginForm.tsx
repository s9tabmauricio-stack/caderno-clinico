'use client'

import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { Icone } from './Icones'

function traduzirErro(mensagem: string, status?: number) {
  if (status === 429 || /rate limit|too many/i.test(mensagem))
    return 'Muitos pedidos de link em pouco tempo. Espere alguns minutos e tente de novo.'
  if (/not authorized|not allowed/i.test(mensagem))
    return 'Este e-mail ainda não pode receber o link: o envio de e-mails do site está em modo de teste.'
  if (/invalid/i.test(mensagem)) return 'Esse e-mail não parece válido. Confira e tente de novo.'
  return 'Não foi possível enviar o link agora. Tente de novo em instantes.'
}

export function LoginForm({ googleAtivo }: { googleAtivo: boolean }) {
  const [email, setEmail] = useState('')
  const [estado, setEstado] = useState<'form' | 'enviando' | 'enviado'>('form')
  const [erro, setErro] = useState('')

  async function enviar(e: React.FormEvent) {
    e.preventDefault()
    const v = email.trim().toLowerCase()
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) {
      setErro('Digite um e-mail válido, como nome@exemplo.com.')
      return
    }
    setErro('')
    setEstado('enviando')
    const supabase = createClient()
    const { error } = await supabase.auth.signInWithOtp({
      email: v,
      options: { emailRedirectTo: `${window.location.origin}/auth/callback` },
    })
    if (error) {
      setErro(traduzirErro(error.message, error.status))
      setEstado('form')
      return
    }
    setEmail(v)
    setEstado('enviado')
  }

  async function entrarComGoogle() {
    const supabase = createClient()
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: { redirectTo: `${window.location.origin}/auth/callback` },
    })
    if (error) setErro('Não foi possível abrir o login do Google. Tente de novo.')
  }

  if (estado === 'enviado') {
    return (
      <div className="login-card enviado" role="status">
        <span className="pdf-ic">{Icone.email}</span>
        <h2>Confira seu e-mail</h2>
        <p>
          Enviamos um link de acesso para <b>{email}</b>. Abra o e-mail <b>neste mesmo navegador</b> e toque no link para
          entrar.
        </p>
        <p className="fine" style={{ margin: 0 }}>
          Não chegou? Olhe a caixa de spam ou{' '}
          <button className="link" style={{ padding: 0 }} onClick={() => setEstado('form')}>
            peça outro link
          </button>
          .
        </p>
      </div>
    )
  }

  return (
    <>
      <div className="login-card">
        {googleAtivo && (
          <>
            <button className="btn google wide" type="button" onClick={entrarComGoogle}>
              Continuar com Google
            </button>
            <div className="or">ou entre com seu e-mail</div>
          </>
        )}
        <form onSubmit={enviar} noValidate>
          <label htmlFor="email" className="flabel">
            E-mail
          </label>
          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            inputMode="email"
            placeholder="voce@exemplo.com"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value)
              setErro('')
            }}
            aria-invalid={erro ? true : undefined}
            aria-describedby={erro ? 'emailErr' : undefined}
          />
          {erro && (
            <p id="emailErr" className="err" role="alert">
              {erro}
            </p>
          )}
          <button className="btn wide" type="submit" disabled={estado === 'enviando'}>
            {estado === 'enviando' ? 'Enviando…' : 'Receber link de acesso'}
          </button>
        </form>
      </div>
      <p className="fine">Sem senha: você recebe um link no e-mail e entra com um toque. Seu progresso fica salvo na sua conta.</p>
    </>
  )
}
